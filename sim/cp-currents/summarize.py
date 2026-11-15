#!/usr/bin/env python3
"""Grade the charge-pump / cp_bias bench (issue #30) and write record.md.

    summarize.py OUT_DIR DELAY_SANITY_RUN_DIR KLT_EXIT_CODE

Reads OUT_DIR/cp.envelope.json (one `klt sim` request, three reduced_set corners).
Criteria, fixed before any result existed (change them only through a decision record):
  K1 current    |I_up| and |I_dn| each in 5..40 uA at every corner (0008: "a few tens of uA")
  K2 mismatch   | |I_up| - |I_dn| | / mean(|I_up|, |I_dn|) <= 0.25
  K3 leakage    |i_leak| (idle, VOUT = 0.6 V) <= 2 % of min(|I_up|, |I_dn|)
  K4 bounded    K_dl * max(|I_up|, |I_dn|) / C_loop <= 0.1 per corner (0008 "Bounded step":
                the relative delay change for a full-period pulse, required << 1).
                K_dl = secant |d(d8)/dVc| at the 1 GHz Vc step whose mid delay is nearest
                T = 1 ns, read from the 1GHz_<corner>.envelope.json files of the pinned
                delay-sanity run (same corner); C_loop = 1.0 pF
                (26 um x 26 um MIM, nominal density, NOT extracted).
  K5 dump       VDUMP follows VOUT: (vd_hi - vd_lo) / 0.6 V in 0.8..1.2 (offset reported)
  K6 present    every measurement has a value at every corner
Charge per 200 ps pulse is reported against I * 200 ps (informational, not graded).
Simulated, never measured. Exit 0 all pass, 6 otherwise (NOT-RUN included).
"""
import json
import os
import sys

C_LOOP = 1.0e-12
T = 1.0e-9
PULSE_S = 200e-12
NEEDED = ["i_up", "i_dn", "i_leak", "i_both", "i_vdd_idle", "q_up", "q_dn", "vd_mid", "vd_lo", "vd_hi"]
CORNERS = ("ss", "tt", "ff")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def cite(path):
    """`path` relative to the repo root when it is inside it, else absolute."""
    rel = os.path.relpath(os.path.abspath(path), REPO)
    return os.path.abspath(path) if rel.startswith(os.pardir) else rel


def kdl_from_envelopes(run_dir):
    """({'ss'|'tt'|'ff': (K_dl in s/V, Vc_lo, Vc_hi)}, [problem, ...]) for a delay-sanity run.

    Reads run_dir/1GHz_<corner>.envelope.json: the Vc of each corner unit
    (supply_v.VC) against its d8 measurement, the same two numbers
    sim/delay-sanity/summarize.py renders into its record.md -- at full
    precision, rather than re-parsing that table's rounded picoseconds.
    """
    out, bad = {}, []
    for corner in CORNERS:
        p = os.path.join(run_dir, f"1GHz_{corner}.envelope.json")
        try:
            env = json.load(open(p, encoding="utf-8"))
        except (OSError, ValueError) as exc:
            bad.append(f"delay-sanity input {cite(p)} unreadable: {exc}")
            continue
        pts = []
        for cr in env.get("corners", []):
            vc = (cr.get("supply_v") or {}).get("VC")
            d8 = {m["name"]: m.get("value") for m in cr.get("measurements", [])}.get("d8")
            if vc is not None and d8 is not None:
                pts.append((vc, d8))
        pts.sort()
        if len(pts) < 2:
            bad.append(f"delay-sanity input {cite(p)}: {len(pts)} Vc point(s) with a d8 value, need 2 for a secant")
            continue
        secants = [(abs((d0 + d1) / 2 - T), abs(d1 - d0) / (v1 - v0), v0, v1)
                   for (v0, d0), (v1, d1) in zip(pts, pts[1:])]
        out[corner] = min(secants, key=lambda s: s[0])[1:]
    return out, bad


def main(argv):
    out, delay_run, klt_rc = argv[1], argv[2], int(argv[3])
    lines = ["# cp-currents record", "",
             "Charge pump (`design/cp.sch`) with `cp_bias`, VOUT held by an ideal source at 0.6 V, "
             "reduced corner set (tt/1.2 V/27 C, ss/1.08 V/125 C, ff/1.32 V/-40 C), one `klt sim` request.",
             "Simulated, never measured. Criteria K1-K6 are in `sim/cp-currents/summarize.py`.", ""]
    try:
        env = json.load(open(os.path.join(out, "cp.envelope.json"), encoding="utf-8"))
    except (OSError, ValueError):
        env = None
    kdl, errs = kdl_from_envelopes(delay_run)
    if env is None:
        errs.append(f"no envelope written (klt exit {klt_rc}); see cp.stderr")
    else:
        if env.get("error"):
            errs.append(str(env["error"].get("message", env["error"])))
        for c in env.get("corners", []):
            errs += [d.get("message", "") for d in c.get("diagnostics", []) if d.get("severity") == "error"]
    corners = env.get("corners", []) if env else []
    vals = []
    for c in corners:
        v = {m["name"]: m.get("value") for m in c.get("measurements", [])}
        vals.append((c, v))
    if errs or not vals or any(any(v.get(n) is None for n in NEEDED) for _, v in vals):
        lines += ["RESULT: NOT-RUN or incomplete (K6)", "", "Errors (verbatim):", ""]
        lines += ["    " + e for e in (errs or ["(a measurement has no value)"])]
        open(os.path.join(out, "record.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
        print("\n".join(lines))
        return 6
    lines += [f"Delay-sanity run for K_dl: `{cite(delay_run)}` "
              f"(1GHz_{{{','.join(CORNERS)}}}.envelope.json; copies in `delay-sanity/`).", "",
              "| corner | I_up uA | I_dn uA | mismatch | leak nA | I(Vdd) idle uA | both-on net uA | "
              "Q_up fC (I*200ps) | Q_dn fC (I*200ps) | VDUMP-VOUT mV (0.3/0.6/0.9 V) | dump slope | "
              "K_dl ns/V | K_dl*I/C |", "|" + "---|" * 13]
    fails = []
    for c, v in vals:
        pr = c.get("process") or c.get("corner") or ""
        name = f"{pr}/{c.get('supply_v', {}).get('Vdd', '?')}V/{c.get('temperature_c', '?')}C"
        key = {"mos_tt": "tt", "mos_ss": "ss", "mos_ff": "ff"}.get(str(pr).split("/")[0], None)
        iu, idn = v["i_up"], -v["i_dn"]
        mean = (abs(iu) + abs(idn)) / 2
        mis = abs(abs(iu) - abs(idn)) / mean
        slope = (v["vd_hi"] - v["vd_lo"]) / 0.6
        k = kdl.get(key)
        ratio = k[0] * max(abs(iu), abs(idn)) / C_LOOP if k else float("nan")
        if not all(5e-6 <= abs(x) <= 40e-6 for x in (iu, idn)):
            fails.append(f"{name}: K1 current {iu*1e6:.1f}/{idn*1e6:.1f} uA outside 5..40 uA")
        if mis > 0.25:
            fails.append(f"{name}: K2 mismatch {mis:.2f} > 0.25")
        if abs(v["i_leak"]) > 0.02 * min(abs(iu), abs(idn)):
            fails.append(f"{name}: K3 leakage {v['i_leak']*1e9:.1f} nA")
        if not (ratio <= 0.1):
            fails.append(f"{name}: K4 K_dl*I/C = {ratio:.3f} > 0.1")
        if not (0.8 <= slope <= 1.2):
            fails.append(f"{name}: K5 dump slope {slope:.2f}")
        off = [(v['vd_lo'] - 0.3) * 1e3, (v['vd_mid'] - 0.6) * 1e3, (v['vd_hi'] - 0.9) * 1e3]
        lines.append(f"| {name} | {iu*1e6:.2f} | {idn*1e6:.2f} | {mis:.2f} | {v['i_leak']*1e9:.2f} | "
                     f"{-v['i_vdd_idle']*1e6:.1f} | {v['i_both']*1e6:.2f} | {v['q_up']*1e15:.2f} ({iu*PULSE_S*1e15:.2f}) | "
                     f"{-v['q_dn']*1e15:.2f} ({idn*PULSE_S*1e15:.2f}) | {off[0]:.0f}/{off[1]:.0f}/{off[2]:.0f} | {slope:.2f} | "
                     f"{(k[0]*1e9 if k else float('nan')):.2f} | {ratio:.3f} |")
    lines += ["", "Charge-per-pulse columns are NOT a usable result: the DN window contains an unexplained late current spike "
              "(see the qw_dn_min measurement in the envelope), the UP charge is dominated by switching injection, and "
              "neither was graded. K1-K5 do not depend on them.", ""]
    lines += ["K_dl is a secant between the two 1 GHz Vc points of the delay-sanity envelopes whose mid "
              "delay is nearest T; the ss line does not reach T at 1 GHz (decision 0010), so its K_dl is at the fastest-reachable end.", ""]
    lines += ["RESULT: " + ("PASS" if not fails else "FAIL")] + [f"- {f}" for f in fails]
    open(os.path.join(out, "record.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0 if not fails else 6


if __name__ == "__main__":
    sys.exit(main(sys.argv))
