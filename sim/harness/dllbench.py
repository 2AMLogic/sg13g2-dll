#!/usr/bin/env python3
"""Build and grade the DLL row benches (issue #28).

A bench directory (`sim/<row>/`) holds a `bench.json` naming what it measures;
this module turns it into `klt sim` grid requests through `gridspec.py` (one
request per input frequency; nothing here launches a simulator) and grades the
returned envelopes against `spec/target-spec.md`.

  dllbench.py build BENCH_DIR OUT [--dut sim/standin/dut.json] [--f0 HZ] [--tol 0.02]
  dllbench.py check OUT                    # structural check of a built bench, no simulator
  dllbench.py grade BENCH_DIR OUT          # reads OUT/manifest.json + OUT/<tag>.envelope.json
  dllbench.py rows                         # the spec rows, from spec/target-spec.md

Measurement scheme (all times are of rising edges at Vdd/2 of the corner's own
supply; the deck normalises every measured node by Vdd):
  * delay d_k,n  = in edge j -> tap k edge j, for the 64 consecutive cycles
    j = J-63 .. J, J = floor(2.95 us / T). Edge indices, not times, pair the
    edges, so a delay of 2 T reads as 2 T.
  * Locked predicate (spec "Locked"): |d_8,n - T| <= tol*T for all 64 cycles
    and the control voltage moves < 5 mV over them.
  * "profile" selects the extra measurements: `predicate` (rows 2, 8, 12),
    `samples` (row 7: every 16th cycle for the lock time), `phase` (rows 3-5),
    `power` (row 10).
Stdlib only. Every number is simulated, never measured.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.dirname(HERE)
ROOT = os.path.dirname(SIM)
sys.path.insert(0, HERE)

import evidence  # noqa: E402
import gridspec  # noqa: E402

TSTOP = 3.2e-6
WINDOW = 64
J_END_TIME = 2.95e-6
SAMPLE_STEP = 16
VC_PP_MAX = 5e-3
RAIL_MARGIN = 0.05
TAPS = 9  # tap0 .. tap8
AXES = ("vic", "vton", "vtdis", "vtre", "vtclk")
AXIS_NODE = {"vic": "vic", "vton": "ton", "vtdis": "tdis", "vtre": "tre", "vtclk": "tclk"}
NEVER = 100000

# Row-8 start states (spec "False-lock criterion"). Values for the five swept
# sources; state 4's preset depends on the frequency and the DUT's delay law.
STATES = ("s1_min_rail", "s2_max_rail", "s3_mid", "s4a_half_T", "s4b_one_and_half_T",
          "s5a_power_up", "s5b_enable_while_running", "s5c_reenable", "s5d_clock_late")


class BenchError(ValueError):
    pass


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def fnum(x):
    return f"{x:.9g}"


def window_end(period):
    """Last edge index of the 64-cycle window."""
    return int(J_END_TIME / period)


def vc_for_delay(dut, period, mult):
    """vc/Vdd at which the DUT's tap-N delay is mult*T (clipped to the rails)."""
    law = dut["delay_law"]
    return min(1.0, max(0.0, (mult * period - law["min_s"]) / law["span_s"]))


def state_axes(name, period, dut):
    """The five start-state source values for a named row-8 start state."""
    base = {"vic": -1.0, "vton": -1.0, "vtdis": NEVER, "vtre": NEVER, "vtclk": -1.0}
    over = {
        "s1_min_rail": {"vic": 0.0},
        "s2_max_rail": {"vic": 1.0},
        "s3_mid": {"vic": 0.5},
        "s4a_half_T": {"vic": vc_for_delay(dut, period, 0.5)},
        "s4b_one_and_half_T": {"vic": vc_for_delay(dut, period, 1.5)},
        "s5a_power_up": {},
        "s5b_enable_while_running": {"vton": 200.0},
        "s5c_reenable": {"vtdis": 800.0, "vtre": 900.0},
        "s5d_clock_late": {"vtclk": 200.0},
    }
    if name not in over:
        raise BenchError(f"unknown start state {name!r}; known: {', '.join(STATES)}")
    base.update(over[name])
    return base


def enable_ref_ns(axes):
    """Reference time for lock time: the later of enable assertion and the first
    input edge; the re-enable time when the state re-enables."""
    if axes["vtre"] < NEVER:
        return axes["vtre"]
    return max(axes["vton"], axes["vtclk"], 0.0)


# ---- measurements ---------------------------------------------------------

def meas(name, spice, unit, **limits):
    m = {"name": name, "spice": f".meas tran {name} {spice}", "unit": unit}
    if limits:
        m["limits"] = limits
    return m


def delay_meas(k, n, j):
    return meas(f"d{k}_{n:02d}", f"trig v(inn) val=0.5 rise={j} targ v(tn{k}) val=0.5 rise={j}", "s")


def predicate_measurements(period, tol, t0, t1, j0):
    out = [delay_meas(8, n, j0 + n - 1) for n in range(1, WINDOW + 1)]
    out.append(meas("c_01", f"param='abs(d8_01-{fnum(period)})'", "s"))
    for n in range(2, WINDOW + 1):
        out.append(meas(f"c_{n:02d}", f"param='max(c_{n-1:02d},abs(d8_{n:02d}-{fnum(period)}))'", "s"))
    out.append(meas("perr", f"param='c_{WINDOW:02d}/{fnum(period)}'", "", max=tol))
    out.append(meas("vcmax", f"max v(vc) from={fnum(t0)} to={fnum(t1)}", "V"))
    out.append(meas("vcmin", f"min v(vc) from={fnum(t0)} to={fnum(t1)}", "V"))
    out.append(meas("vcpp", "param='vcmax-vcmin'", "V", max=VC_PP_MAX))
    out.append(meas("rail_hi", f"min v(vrh) from={fnum(t0)} to={fnum(t1)}", "V", min=RAIL_MARGIN))
    out.append(meas("rail_lo", f"min v(vc) from={fnum(t0)} to={fnum(t1)}", "V", min=RAIL_MARGIN))
    out.append(meas("lock_end", f"find v(lockn) at={fnum(t1)}", ""))
    return out


def sample_measurements(j_end):
    out = []
    for j in range(SAMPLE_STEP, j_end + 1, SAMPLE_STEP):
        out.append(meas(f"te_{j}", f"when v(inn)=0.5 rise={j}", "s"))
        out.append(meas(f"ds_{j}", f"trig v(inn) val=0.5 rise={j} targ v(tn8) val=0.5 rise={j}", "s"))
        out.append(meas(f"ls_{j}", f"find v(lockn) when v(inn)=0.5 rise={j}", ""))
    return out


def phase_measurements(period, tol, j0):
    out = []
    for k in range(TAPS - 1):  # tap8 is already in the predicate set
        out += [delay_meas(k, n, j0 + n - 1) for n in range(1, WINDOW + 1)]
    for k in range(TAPS):
        terms = "+".join(f"d{k}_{n:02d}" for n in range(1, WINDOW + 1))
        out.append(meas(f"s{k}", f"param='({terms})/{WINDOW}'", "s"))
    for k in range(TAPS - 1):
        out.append(meas(f"sp{k}", f"param='s{k+1}-s{k}'", "s"))
        out.append(meas(f"sperr{k}", f"param='abs(sp{k}-{fnum(period/8)})/{fnum(period)}'", "", max=tol))
    out.append(meas("sterr", f"param='abs(s8-{fnum(period)})/{fnum(period)}'", "", max=tol))
    return out


def power_measurements(pmax_mw, t0, t1):
    return [meas("pavg", f"avg v(pw) from={fnum(t0)} to={fnum(t1)}", "mW", max=pmax_mw)]


def evidence_measurements():
    out = [meas("ic_seen", "find v(icseen) at=50p", "")]
    for a in AXES[1:]:
        out.append(meas(f"{a}_seen", f"find v({AXIS_NODE[a]}) at=50p", ""))
    out.append(meas("tclk_edge", "when v(inn)=0.5 rise=1", "s"))
    return out


def measurements(profile, period, tol, pmax_mw):
    j_end = window_end(period)
    j0 = j_end - WINDOW + 1
    t0 = (j0 - 1) * period
    t1 = j_end * period
    out = predicate_measurements(period, tol, t0, t1, j0)
    if profile == "samples":
        out += sample_measurements(j_end)
    elif profile == "phase":
        out += phase_measurements(period, tol, j0)
    elif profile == "power":
        out += power_measurements(pmax_mw, t0, t1)
    elif profile != "predicate":
        raise BenchError(f"unknown profile {profile!r}")
    return out + evidence_measurements()


# ---- build ----------------------------------------------------------------

def render_deck(template, period, dut, include_rel):
    sub = {
        "PERIOD_NS": fnum(period * 1e9),
        "HALF_NS": fnum(period * 1e9 / 2),
        "DUT_NAME": dut["name"],
        "DUT_NOTE": "STAND-IN, not the item-1 netlist" if dut.get("stand_in") else "item-1 netlist",
        "DUT_INCLUDE": f".include {include_rel}",
        "DUT_SUBCKT": dut["subckt"],
    }
    text = template
    for k, v in sub.items():
        text = text.replace(f"@{k}@", v)
    left = re.findall(r"@[A-Z_]+@", text)
    if left:
        raise BenchError(f"unfilled deck placeholders: {sorted(set(left))}")
    return text


def base_request(deck_rel, profile, period, tol, pmax_mw):
    return {
        "_comment": [
            "DLL row bench base request (issue #28), written by sim/harness/dllbench.py.",
            "Limits are the spec's target-column pass windows; a stand-in DUT result is a result about the stand-in only. Simulated, never measured.",
            "@OSDI_DIR@ is substituted by run.sh.",
        ],
        "engine": "ngspice",
        "netlist": deck_rel,
        "netlist_source": "schematic",
        "models": {"pdk": "ihp-sg13g2", "lib": "libs.tech/ngspice/models/cornerMOSlv.lib"},
        "analysis": {"kind": "tran", "args": f"{fnum(5e-12)} {fnum(TSTOP)} 0 {fnum(1e-11)}"},
        "measurements": measurements(profile, period, tol, pmax_mw),
        "options": {
            "osdi_preload": [f"@OSDI_DIR@/{m}" for m in ("psp103.osdi", "psp103_nqs.osdi", "r3_cmc.osdi", "mosvar.osdi")],
            "stage_model_inputs": True,
            "keep_artifacts": True,
        },
    }


def build(bench_dir, out, dut_path, f0, tol, pmax_mw, osdi_dir, corners=None):
    cfg = load(os.path.join(bench_dir, "bench.json"))
    dut = load(dut_path)
    dut_dir = os.path.dirname(os.path.abspath(dut_path))
    with open(os.path.join(HERE, "dll_tb.spice.in"), encoding="utf-8") as fh:
        template = fh.read()
    if os.path.exists(out):
        raise BenchError(f"{out} exists; results are append-only")
    for sub in ("decks/dut", "base", "requests"):
        os.makedirs(os.path.join(out, sub))
    shutil.copy(os.path.join(dut_dir, dut["netlist"]), os.path.join(out, "decks", "dut", dut["netlist"]))
    corner_set = gridspec.load_corners(corners or os.path.join(SIM, "corners.json"))
    states = list(STATES) if cfg["start_states"] == "all" else list(cfg["start_states"])
    manifest = {"bench": cfg["bench"], "rows": cfg["rows"], "profile": cfg["profile"], "f0_hz": f0,
                "tol": tol, "dut": dut["name"], "stand_in": bool(dut.get("stand_in")),
                "attestable": bool(dut.get("attestable")), "requests": []}
    for scale in cfg["freq_scales"]:
        freq = f0 * scale
        period = 1.0 / freq
        tag = f"f{int(round(scale * 100)):03d}"
        deck_rel = f"decks/tb_{tag}.spice"
        with open(os.path.join(out, deck_rel), "w", encoding="utf-8") as fh:
            fh.write(render_deck(template, period, dut, f"dut/{dut['netlist']}"))
        axes = [state_axes(s, period, dut) for s in states]
        base = base_request(f"../{deck_rel}", cfg["profile"], period, tol, pmax_mw)
        base_path = os.path.join(out, "base", f"{tag}.base.request.json")
        gridspec.write_request(base, base_path)
        ic = {a: [row[a] for row in axes] for a in AXES}
        req = gridspec.build_request(base, corner_set, ic)
        req_path = os.path.join(out, "requests", f"{tag}.request.json")
        gridspec.write_request(gridspec.rebase_netlist(req, os.path.dirname(base_path), req_path), req_path)
        manifest["requests"].append({
            "tag": tag, "freq_hz": freq, "period_s": period,
            "window": {"j_end": window_end(period), "samples": cfg["profile"] == "samples"},
            "states": [{"name": s, "ic": a, "ref_ns": enable_ref_ns(a)} for s, a in zip(states, axes)],
        })
    with open(os.path.join(out, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
        fh.write("\n")
    for r in os.listdir(os.path.join(out, "base")):
        p = os.path.join(out, "base", r)
        with open(p, encoding="utf-8") as fh:
            text = fh.read().replace("@OSDI_DIR@", osdi_dir)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(text)
    for r in os.listdir(os.path.join(out, "requests")):
        p = os.path.join(out, "requests", r)
        with open(p, encoding="utf-8") as fh:
            text = fh.read().replace("@OSDI_DIR@", osdi_dir)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(text)
    return manifest


# ---- grading --------------------------------------------------------------

def mvals(corner):
    return {m["name"]: m.get("value") for m in corner.get("measurements", [])}


def state_of(manifest_req, corner):
    sv = corner.get("supply_v") or {}
    for st in manifest_req["states"]:
        if all(abs(sv.get(a, math.nan) - st["ic"][a]) < 1e-6 for a in AXES):
            return st
    return None


def lock_time(period, st, vals, j_end):
    """First sampled time at which the predicate holds and keeps holding to the
    end, counted from the later of enable and the first input edge. Resolution
    is SAMPLE_STEP cycles. None when it never settles."""
    tol = vals["_tol"]
    samples = []
    for j in range(SAMPLE_STEP, j_end + 1, SAMPLE_STEP):
        te, ds = vals.get(f"te_{j}"), vals.get(f"ds_{j}")
        if te is None or ds is None:
            samples.append((j, None, False))
        else:
            samples.append((j, te, abs(ds - period) <= tol * period))
    tail = None
    for j, te, ok in reversed(samples):
        if not ok:
            break
        if te is not None and te >= st["ref_ns"] * 1e-9:
            tail = (j, te)
    if tail is None or vals.get("perr") is None or vals["perr"] > tol:
        return None
    return tail[1] - st["ref_ns"] * 1e-9


def grade_corner(profile, period, st, vals, tol):
    """Per-corner facts: predicate, delay in periods, rails, LOCK, lock time."""
    f = {"state": st["name"]}
    perr, vcpp = vals.get("perr"), vals.get("vcpp")
    f["locked"] = perr is not None and vcpp is not None and perr <= tol and vcpp <= VC_PP_MAX
    d = vals.get("d8_64")
    f["delay_periods"] = None if d is None else round(d / period)
    f["on_rail"] = (vals.get("rail_hi") is None or vals.get("rail_lo") is None
                    or vals["rail_hi"] < RAIL_MARGIN or vals["rail_lo"] < RAIL_MARGIN)
    f["one_period"] = f["locked"] and f["delay_periods"] == 1
    f["row8_pass"] = f["one_period"] and not f["on_rail"]
    lk = vals.get("lock_end")
    f["lock_ok"] = None if lk is None else (lk > 0.5) == f["row8_pass"]
    if profile == "samples":
        f["lock_time_s"] = lock_time(period, st, dict(vals, _tol=tol), window_end(period))
    return f


def axis_problems(name, env, manifest_req):
    """The start-state axes took effect (each swept source reads back its value)."""
    problems = []
    probes = {a: ("ic_seen" if a == "vic" else f"{a}_seen") for a in AXES}
    for src, m in probes.items():
        problems += evidence.check_ic_applied(name, env, src, m, tol=0.02 if src == "vic" else 1e-6)
    for c in env.get("corners", []):
        st = state_of(manifest_req, c)
        if st is None:
            problems.append(f"{name} {c['corner_id']}: corner's start-state sources match no state in the manifest")
            continue
        edge = mvals(c).get("tclk_edge")
        want = max(st["ic"]["vtclk"], 0.0) * 1e-9
        if edge is not None and not (want <= edge <= want + 0.5 * manifest_req["period_s"]):
            problems.append(f"{name} {c['corner_id']}: first input edge at {edge:.3g} s, expected near {want:.3g} s")
    return problems


def grade(bench_dir, out):
    cfg = load(os.path.join(bench_dir, "bench.json"))
    manifest = load(os.path.join(out, "manifest.json"))
    tol = manifest["tol"]
    problems, items, lines = [], [], []
    summary = {}
    for req in manifest["requests"]:
        path = os.path.join(out, f"{req['tag']}.envelope.json")
        if not os.path.isfile(path):
            problems.append(f"{req['tag']}: no envelope (klt sim failed before reporting; see {req['tag']}.stderr)")
            continue
        env = evidence.load(path)
        items.append((path, env))
        problems += evidence.basic_problems(os.path.basename(path), env)
        if "error" in env:
            continue
        problems += axis_problems(os.path.basename(path), env, req)
        for c in env.get("corners", []):
            st = state_of(req, c)
            if st is None:
                continue
            f = grade_corner(manifest["profile"], req["period_s"], st, mvals(c), tol)
            key = (req["tag"], st["name"])
            s = summary.setdefault(key, {"n": 0, "locked": 0, "one_period": 0, "row8": 0, "lock_ok": 0,
                                         "lock_time_max": None, "no_lock_time": 0, "multi": 0})
            s["n"] += 1
            s["locked"] += f["locked"]
            s["one_period"] += f["one_period"]
            s["row8"] += f["row8_pass"]
            s["lock_ok"] += bool(f["lock_ok"])
            if f["locked"] and f["delay_periods"] not in (None, 1):
                s["multi"] += 1
            if "lock_time_s" in f:
                if f["lock_time_s"] is None:
                    s["no_lock_time"] += 1
                else:
                    s["lock_time_max"] = max(s["lock_time_max"] or 0.0, f["lock_time_s"])
    standin = manifest["stand_in"]
    lines += [f"# {cfg['bench']} bench record", "", "SIMULATED results, never measured.", ""]
    if standin:
        lines += ["**DUT is the behavioural STAND-IN, not the item-1 netlist.** These numbers describe the model "
                  "in `sim/standin/`; they do not grade the block and do not satisfy T1 item 9.", ""]
    lines += [f"- spec rows: {', '.join(str(r) for r in cfg['rows'])}; profile `{manifest['profile']}`; "
              f"tolerance {tol:g} of T; f0 {manifest['f0_hz']:.6g} Hz; DUT `{manifest['dut']}`",
              "- window: the last 64 input cycles before 2.95 us (edge indices, rising edges at Vdd/2 of each corner's own supply)", ""]
    lines += ["| request | start state | corners | locked | exactly 1 T | row-8 pass | LOCK consistent | delay != 1 T | lock time max (s) | no lock time |",
              "|---|---|---|---|---|---|---|---|---|---|"]
    for (tag, name), s in sorted(summary.items()):
        lt = "-" if s["lock_time_max"] is None else f"{s['lock_time_max']:.4g}"
        lines.append(f"| {tag} | {name} | {s['n']} | {s['locked']} | {s['one_period']} | {s['row8']} | "
                     f"{s['lock_ok']} | {s['multi']} | {lt} | {s['no_lock_time']} |")
    lines += ["", evidence.render(items, title="Envelope summary").split("\n", 3)[3]]
    failing = [env.get("failed", 0) + env.get("errored", 0) for _, env in items if "error" not in env]
    rows_ok = not problems and not any(failing)
    lines += ["", "## Verdict", "",
              f"- harness: {'FAIL' if problems else 'PASS'}",
              f"- rows {', '.join(str(r) for r in cfg['rows'])} on this DUT: {'all corners pass' if rows_ok else 'NOT all corners pass (a result, not a harness fault)'}"]
    if problems:
        lines += [""] + [f"- {p}" for p in problems]
    with open(os.path.join(out, "record.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    for p in problems:
        print(f"dllbench: {p}", file=sys.stderr)
    if problems:
        return 1
    return 0 if rows_ok else 6


def check(out):
    """Structural check of a built bench (no simulator): every request is a
    45-corner-class grid crossed with its start states, measurement names are
    unique, and the false-lock axes are all present."""
    manifest = load(os.path.join(out, "manifest.json"))
    corners = gridspec.load_corners(os.path.join(SIM, "corners.json"))
    n_corner_rows = len(corners["process"]) * len(corners["temperature_c"]) * len(corners["supply_v"]["Vdd"])
    problems = []
    for req in manifest["requests"]:
        r = load(os.path.join(out, "requests", f"{req['tag']}.request.json"))
        names = [m["name"] for m in r["measurements"]]
        if len(names) != len(set(names)):
            problems.append(f"{req['tag']}: duplicate measurement names")
        sv = r["corners"]["supply_v"]
        if set(sv) != {"Vdd", *AXES}:
            problems.append(f"{req['tag']}: supply_v axes {sorted(sv)}")
        want = len(corners["supply_v"]["Vdd"]) * len(req["states"])
        if {len(v) for v in sv.values()} != {want}:
            problems.append(f"{req['tag']}: supply_v rows != {want}")
        units = len(r["corners"]["process"]) * len(r["corners"]["temperature_c"]) * want
        if units != n_corner_rows * len(req["states"]):
            problems.append(f"{req['tag']}: {units} units, expected {n_corner_rows * len(req['states'])}")
        if not any("limits" in m for m in r["measurements"]):
            problems.append(f"{req['tag']}: no measurement carries a limit")
        print(f"check: {req['tag']}: {units} units, {len(names)} measurements", file=sys.stderr)
    for p in problems:
        print(f"dllbench: {p}", file=sys.stderr)
    return 1 if problems else 0


def spec_rows(path=None):
    """Row numbers present in spec/target-spec.md's table."""
    with open(path or os.path.join(ROOT, "spec", "target-spec.md"), encoding="utf-8") as fh:
        return sorted({int(m.group(1)) for m in re.finditer(r"^\| (\d+) \|", fh.read(), re.M)})


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("bench_dir")
    b.add_argument("out")
    b.add_argument("--dut", default=os.path.join(SIM, "standin", "dut.json"))
    b.add_argument("--f0", type=float, default=1e9, help="column frequency in Hz (1e9 target, 5e8 fallback, 2e9 stretch)")
    b.add_argument("--tol", type=float, default=0.02, help="phase tolerance as a fraction of T (0.02 target, 0.05 fallback, 0.01 stretch)")
    b.add_argument("--pmax-mw", type=float, default=5.0)
    b.add_argument("--osdi-dir", default="@OSDI_DIR@")
    b.add_argument("--corners")
    g = sub.add_parser("grade")
    g.add_argument("bench_dir")
    g.add_argument("out")
    c = sub.add_parser("check")
    c.add_argument("out")
    sub.add_parser("rows")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "build":
            build(a.bench_dir, a.out, a.dut, a.f0, a.tol, a.pmax_mw, a.osdi_dir, a.corners)
        elif a.cmd == "check":
            return check(a.out)
        elif a.cmd == "grade":
            return grade(a.bench_dir, a.out)
        else:
            print(" ".join(str(r) for r in spec_rows()))
    except (BenchError, gridspec.GridError, OSError, KeyError, json.JSONDecodeError) as exc:
        print(f"dllbench: FAIL -- {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
