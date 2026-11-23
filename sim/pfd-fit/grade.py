#!/usr/bin/env python3
"""Grade the 0006 PFD fit gate from `klt sim` envelopes (pure reduction).

    grade.py --out fit-gate.md [--require-pass] ENVELOPE.json ...

Envelope tags are `pfd_<f>` (the DLL's pfd.sch) or `ctl_<f>` (the control: the
sibling's reset polarity). Frequencies come from make_bench.FREQS.

Criteria, fixed before any result existed (change them only through a decision record):
  C1 response   for every tested |offset| >= 10 ps, sign(wUP - wDN) == sign(offset)
                and 0.5 <= (wUP - wDN) / offset <= 1.5   ("no dead zone above 10 ps")
  C2 reset      at offset 0, min(wUP, wDN) >= 30 ps and <= 0.25 T   (reset-pulse width)
  C3 present    every offset has both an UP and a DN pulse measured, no missing series
  The +-5 ps points are reported, not graded.
The control must FAIL C1-C3 for a stated reason, read off the DUT-internal probes
make_bench.control_probes puts in its request (decisions 0008/0011: the sibling's
reset polarity holds the latch in reset): the edge detectors fire on every input
edge, each set pulse reaches its latch storage node, reset is asserted at rest, and
no lane pulse is released.
Exit 0 all graded corners pass and the control failed for that reason, 1 any fail or
a bench defect (a control that fails for another reason, passes, lacks the probes or
is absent), 2 an envelope could not be read.
Widths are measured at VDD/2 of each corner's own supply. Simulated, never measured.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_bench as mb  # noqa: E402

MIN_RESET_S = 30e-12
MAX_RESET_FRAC = 0.25
RESP_LO, RESP_HI = 0.5, 1.5
GRADED_MIN_OFFSET_PS = 10
PORTS = ("t_ref", "t_fb", "t_up", "t_dn")
STATED_REASON = ("edge detectors fire on every input edge, set pulses reach the latch "
                 "storage nodes, reset is asserted at rest and no lane pulse is "
                 "released: the latch is held in reset")


def series(corner, name):
    for m in corner.get("measurements", []):
        if m.get("name") == name and m.get("crossings"):
            return m["crossings"]["times"], m["crossings"]["edges"]
    return None, None


def scalar(corner, name):
    """Value of a level measurement (a `.meas` card); None if the envelope does not carry it."""
    for m in corner.get("measurements", []):
        if m.get("name") == name and "crossings" not in m:
            return m.get("value")
    return None


def pulse_width(times, edges, t_from, t_to):
    """Width of the first high pulse whose rising edge lies in [t_from, t_to); 0.0 if none."""
    for i, (t, e) in enumerate(zip(times, edges)):
        if e == "rise" and t_from <= t < t_to:
            for t2, e2 in zip(times[i + 1:], edges[i + 1:]):
                if e2 == "fall":
                    return t2 - t
            return None
    return 0.0


def grade_corner(corner, period):
    offs = mb.offsets()
    tr, _ = series(corner, "t_ref")
    tf, _ = series(corner, "t_fb")
    up, ue = series(corner, "t_up")
    dn, de = series(corner, "t_dn")
    if None in (tr, tf, up, dn) or len(tr) < len(offs) or len(tf) < len(offs):
        return {"error": "missing or short crossing series"}
    rows = []
    for k, o in enumerate(offs):
        first = min(tr[k], tf[k])
        wu = pulse_width(up, ue, first, first + period)
        wd = pulse_width(dn, de, first, first + period)
        rows.append({"k": k, "offset_ps": o, "actual_ps": (tf[k] - tr[k]) * 1e12,
                     "w_up_ps": None if wu is None else wu * 1e12,
                     "w_dn_ps": None if wd is None else wd * 1e12})
    fails = []
    reset = [min(r["w_up_ps"], r["w_dn_ps"]) for r in rows
             if r["offset_ps"] == 0 and r["w_up_ps"] is not None and r["w_dn_ps"] is not None]
    for r in rows:
        if r["w_up_ps"] is None or r["w_dn_ps"] is None:
            fails.append(f"C3 cycle {r['k']}: unterminated pulse")
            continue
        r["diff_ps"] = r["w_up_ps"] - r["w_dn_ps"]
        o = r["actual_ps"]
        if abs(r["offset_ps"]) >= GRADED_MIN_OFFSET_PS:
            ratio = r["diff_ps"] / o if o else float("nan")
            r["ratio"] = ratio
            if not (RESP_LO <= ratio <= RESP_HI):
                fails.append(f"C1 offset {r['offset_ps']} ps: (wUP-wDN)/offset = {ratio:.2f}")
    if not reset:
        fails.append("C3 no offset-0 cycle measured")
    else:
        lo, hi = min(reset), max(reset)
        if lo * 1e-12 < MIN_RESET_S or hi * 1e-12 > MAX_RESET_FRAC * period:
            fails.append(f"C2 reset-pulse width {lo:.0f}..{hi:.0f} ps outside "
                         f"{MIN_RESET_S * 1e12:.0f} ps..{MAX_RESET_FRAC * period * 1e12:.0f} ps")
    return {"rows": rows, "reset_ps": (min(reset), max(reset)) if reset else None, "fails": fails}


def control_defects(g, corner, period):
    """(defects, evidence) for one control corner: why its lanes are dead.

    `defects` is empty when the control failed for the stated reason (see the
    module docstring) and otherwise names every clause the envelope contradicts,
    a control that passed, or a probe the envelope does not carry. `evidence` is
    what the probes read: crossing counts, the offsets at which reset deasserted
    and the node levels.
    """
    offs = mb.offsets()
    names = PORTS + tuple(f"t_{n}" for n in mb.CONTROL_NODES)
    counts = {n: None if s is None else len(s) for n, s in ((n, series(corner, n)[0]) for n in names)}
    levels = {n: scalar(corner, n) for n in mb.CONTROL_LEVELS}
    evidence = {"counts": counts, "levels": levels, "dip_offsets_ps": [], "reset_dips": 0}
    if "error" in g:
        return [f"control corner not graded ({g['error']})"], evidence
    missing = [n for n in names if counts[n] is None] + [n for n, v in levels.items() if v is None]
    if missing:
        return ["no DUT-internal probes in the envelope (" + ", ".join(missing)
                + "); regenerate ctl_1g and re-run"], evidence
    half = corner["supply_v"]["Vdd"] / 2
    rs, rse = series(corner, "t_reset")
    evidence["dip_offsets_ps"] = sorted({offs[k] for t, e in zip(rs, rse) if e == "fall"
                                         for k in [int((t - mb.T0) // period)] if 0 <= k < len(offs)})
    evidence["reset_dips"] = rse.count("fall")
    defects = []
    for lane, set_n, qn_n, n_in in (("UP", "t_set_up", "t_up_qn", counts["t_ref"]),
                                    ("DN", "t_set_dn", "t_dn_qn", counts["t_fb"])):
        if counts[set_n] < 2 * n_in:
            defects.append(f"edge detectors did not fire: {set_n} has {counts[set_n]} crossings "
                           f"for {n_in} input edges")
        if counts[qn_n] < 2 * n_in:
            defects.append(f"set pulses did not reach the {lane} latch storage node: {qn_n} has "
                           f"{counts[qn_n]} crossings for {n_in} input edges")
    if levels["v_reset_rest"] < half:
        defects.append(f"reset not asserted at rest ({levels['v_reset_rest']:.3f} V < {half:.3f} V)")
    if counts["t_up"] or counts["t_dn"]:
        defects.append(f"lane pulses were released (t_up {counts['t_up']}, t_dn {counts['t_dn']} crossings)")
    elif max(levels["v_up_max"], levels["v_dn_max"]) >= half:
        defects.append("lanes are stuck high, not held low "
                       f"(UP max {levels['v_up_max']:.3f} V, DN max {levels['v_dn_max']:.3f} V)")
    if not g["fails"]:
        defects.insert(0, "control passed C1-C3")
    return defects, evidence


def tag_freq(tag):
    return mb.FREQS[tag.split("_", 1)[1]]


def probe_line(ev):
    c, lv = ev["counts"], ev["levels"]
    if None in c.values() or None in lv.values():
        return "not in the envelope"
    dips = ev["dip_offsets_ps"]
    if dips:
        where = (f"at offset {dips[0]:+d} ps" if len(dips) == 1
                 else f"at offsets {dips[0]:+d}..{dips[-1]:+d} ps")
        reset = f"deasserted on {ev['reset_dips']} cycles {where}"
    else:
        reset = "never deasserted"
    return (f"set_up {c['t_set_up']}, set_dn {c['t_set_dn']} crossings ({c['t_ref']} REF, {c['t_fb']} FB edges); "
            f"up_qn {c['t_up_qn']}, dn_qn {c['t_dn_qn']}; "
            f"reset {lv['v_reset_rest']:.3f} V at rest, {lv['v_reset_min']:.3f}..{lv['v_reset_max']:.3f} V across "
            f"the sweep with {c['t_reset']} crossings, {reset}; "
            f"UP max {lv['v_up_max']:.3f} V, DN max {lv['v_dn_max']:.3f} V, "
            f"t_up {c['t_up']}, t_dn {c['t_dn']} crossings")


def control_line(g):
    if g["defects"]:
        return f"**BENCH DEFECT** -- did not fail for the stated reason: {'; '.join(g['defects'])}"
    return f"FAILS FOR THE STATED REASON ({STATED_REASON})"


def render(results):
    out = ["# PFD fit-gate record (decision 0006)", "",
           "Simulated, never measured. Criteria C1-C3 are in `sim/pfd-fit/grade.py`.", ""]
    ok = True
    for tag, (env, per) in results.items():
        env_ = env.get("environment", {})
        out += [f"## {tag}", "",
                f"- engine: {env_.get('engine')} {env_.get('engine_version')}; backend/host: "
                f"{env_.get('engine_host')}; remote job: {(env_.get('remote') or {}).get('job_id')}",
                f"- envelope status: {env.get('status')}", ""]
        for cid, g in per.items():
            if "error" in g:
                out.append(f"- `{cid}`: NOT GRADED ({g['error']})")
                ok = False
            else:
                verdict = "PASS" if not g["fails"] else "FAIL"
                ok &= not g["fails"]
                r = g["reset_ps"]
                out.append(f"- `{cid}`: **{verdict}**; reset-pulse width {r[0]:.0f}..{r[1]:.0f} ps")
                for f in g["fails"]:
                    out.append(f"  - {f}")
                if "probes" in g:
                    out.append(f"  - internal probes: {probe_line(g['probes'])}")
            if "defects" in g:
                out.append(f"  - control: {control_line(g)}")
        out += ["", "| corner | offset ps | wUP ps | wDN ps | wUP-wDN ps |", "|---|---|---|---|---|"]
        for cid, g in per.items():
            for r in g.get("rows", []):
                if r["k"] >= mb.WARM and r["k"] < mb.WARM + len(mb.OFFSETS_PS):
                    out.append(f"| {cid} | {r['actual_ps']:.1f} | {r['w_up_ps']:.1f} | {r['w_dn_ps']:.1f} | "
                               f"{r.get('diff_ps', float('nan')):.1f} |")
        out.append("")
    return "\n".join(out) + "\n", ok


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("envelopes", nargs="+")
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    results = {}
    for path in a.envelopes:
        tag = os.path.basename(path).split(".")[0]
        try:
            with open(path) as fh:
                env = json.load(fh)
            period = 1.0 / tag_freq(tag)
            if "error" in env:
                raise ValueError(env["error"].get("message"))
            per = {c["corner_id"]: grade_corner(c, period) for c in env["corners"]}
            if tag.startswith("ctl_"):
                for c in env["corners"]:
                    defects, evidence = control_defects(per[c["corner_id"]], c, period)
                    per[c["corner_id"]]["defects"], per[c["corner_id"]]["probes"] = defects, evidence
        except (OSError, ValueError, KeyError) as e:
            print(f"grade: cannot read {path}: {e}", file=sys.stderr)
            return 2
        results[tag] = (env, per)
    text, _ = render(results)
    with open(a.out, "w") as fh:
        fh.write(text)
    # the control must FAIL for the stated reason; only the pfd_* lane grades decide C1-C3
    graded = {t: v for t, v in results.items() if t.startswith("pfd_")}
    bad = any(g.get("fails") or "error" in g for _, per in graded.values() for g in per.values())
    controls = [per for t, (_, per) in results.items() if t.startswith("ctl_")]
    defects = [f"control {cid}: {d}" for per in controls for cid, g in per.items() for d in g["defects"]]
    if not controls:
        defects.append("no control (ctl_*) envelope among the inputs")
    for d in defects:
        print(f"grade: BENCH DEFECT -- {d}", file=sys.stderr)
    return 1 if bad or defects else 0


if __name__ == "__main__":
    sys.exit(main())
