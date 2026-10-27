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
Exit 0 all graded corners pass, 1 any fail, 2 an envelope could not be read.
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


def series(corner, name):
    for m in corner.get("measurements", []):
        if m.get("name") == name and m.get("crossings"):
            return m["crossings"]["times"], m["crossings"]["edges"]
    return None, None


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


def tag_freq(tag):
    return mb.FREQS[tag.split("_", 1)[1]]


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
                continue
            verdict = "PASS" if not g["fails"] else "FAIL"
            ok &= not g["fails"]
            r = g["reset_ps"]
            out.append(f"- `{cid}`: **{verdict}**; reset-pulse width {r[0]:.0f}..{r[1]:.0f} ps")
            for f in g["fails"]:
                out.append(f"  - {f}")
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
            env = json.load(open(path))
            period = 1.0 / tag_freq(tag)
            if "error" in env:
                raise ValueError(env["error"].get("message"))
            per = {c["corner_id"]: grade_corner(c, period) for c in env["corners"]}
        except (OSError, ValueError, KeyError) as e:
            print(f"grade: cannot read {path}: {e}", file=sys.stderr)
            return 2
        results[tag] = (env, per)
    text, ok = render(results)
    open(a.out, "w").write(text)
    # the control is expected to FAIL; only pfd_* decide the exit status
    graded = {t: v for t, v in results.items() if t.startswith("pfd_")}
    bad = any(g.get("fails") or "error" in g for _, per in graded.values() for g in per.values())
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
