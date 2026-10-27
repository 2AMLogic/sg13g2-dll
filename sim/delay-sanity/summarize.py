#!/usr/bin/env python3
"""Summarize delay-sanity envelopes into record.md (simulated, never measured).

usage: summarize.py OUT_DIR   (reads OUT_DIR/<freq>_<corner>.envelope.json)
Exit 1 if an envelope is missing/errored, a corner has a diagnostic, or the
tap-step range at any (freq, corner) does not cover T/8 (the gap is recorded
either way). Per-tap spacing = d_k - d_(k-1) (d_0 = 0: T0 is the reference).
"""
import json, os, sys

FREQS = {"500MHz": 2.0e-9, "1GHz": 1.0e-9}
CORNERS = ("ss", "tt", "ff")
RAIL_MARGIN = 0.1  # decision 0004: locked Vc at least 100 mV from either rail


def main(out):
    lines = ["# delay-sanity record", "", "SIMULATED results, never measured. Reduced corner set "
             "(`sim/corners.json` reduced_set: tt/1.2 V/27 C, ss/1.08 V/125 C, ff/1.32 V/-40 C); "
             "NOT the 45-corner grade. Delay = single-event T0->Tk, first rising edge, 50 % of Vdd, "
             "ideal control sources (VBN=Vc, VBP=Vdd-Vc), 20 fF ideal load on every tap buffer.", ""]
    bad = []
    for fname, period in FREQS.items():
        target = period / 8
        lines += [f"## {fname}: T/8 = {target*1e12:.1f} ps, total delay target span "
                  f"{period/1.2*1e9:.3f}..{period/0.8*1e9:.3f} ns (decision 0004 +/-20 %)", ""]
        for c in CORNERS:
            p = os.path.join(out, f"{fname}_{c}.envelope.json")
            try:
                env = json.load(open(p))
            except OSError:
                bad.append(f"{p}: missing"); continue
            if "error" in env:
                bad.append(f"{fname}/{c}: {env['error']}"); continue
            rows = []
            for cr in env.get("corners", []):
                for d in cr.get("diagnostics", []):
                    bad.append(f"{fname}/{c} {cr['corner_id']}: [{d.get('code')}] {str(d.get('message'))[:100]}")
                m = {x["name"]: x.get("value") for x in cr.get("measurements", [])}
                vdd = cr["supply_v"].get("Vdd")
                rows.append((cr["supply_v"].get("VC"), vdd, m))
            lines += [f"### corner {c} (status {env.get('status')}, {env.get('passed')}/{env.get('corner_count')} pass; "
                      f"backend {(env.get('environment') or {}).get('backend', '?')}; "
                      f"job {((env.get('environment') or {}).get('remote') or {}).get('job_id', '-')})", "",
                      "| Vc (V) | d8 total (ps) | mean step (ps) | min..max tap spacing (ps) |", "|---|---|---|---|"]
            steps = []
            for vc, vdd, m in sorted(rows, key=lambda r: r[0]):
                d = [m.get(f"d{k}") for k in range(1, 9)]
                if any(x is None for x in d):
                    lines.append(f"| {vc:.2f} | no edge / no value | - | - |"); continue
                sp = [d[0]] + [d[i] - d[i - 1] for i in range(1, 8)]
                step = d[7] / 8
                if RAIL_MARGIN <= vc <= vdd - RAIL_MARGIN:
                    steps.append(step)
                lines.append(f"| {vc:.2f} | {d[7]*1e12:.1f} | {step*1e12:.1f} | {min(sp)*1e12:.1f}..{max(sp)*1e12:.1f} |")
            if steps:
                lo, hi = min(steps), max(steps)
                ok = lo <= target <= hi
                lines += ["", f"Mean tap step over Vc >=100 mV from both rails: {lo*1e12:.1f}..{hi*1e12:.1f} ps; "
                          f"T/8 {target*1e12:.1f} ps **{'covered' if ok else 'NOT covered (gap)'}**; "
                          f"total d8 {lo*8e9:.3f}..{hi*8e9:.3f} ns vs 0004 span "
                          f"{period/1.2*1e9:.3f}..{period/0.8*1e9:.3f} ns "
                          f"**{'spans' if lo*8 <= period/1.2 and hi*8 >= period/0.8 else 'does not span'}**.", ""]
                if not ok:
                    bad.append(f"{fname}/{c}: T/8 not covered ({lo*1e12:.1f}..{hi*1e12:.1f} ps)")
            else:
                lines += ["", "No usable delay points.", ""]
                bad.append(f"{fname}/{c}: no usable points")
    lines += ["## Verdict", "", ("FAIL" if bad else "PASS") + ("" if not bad else ":")] + [f"- {b}" for b in bad]
    open(os.path.join(out, "record.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines[-(len(bad) + 3):]))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
