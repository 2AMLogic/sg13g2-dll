#!/usr/bin/env python3
"""Summarize the edgedet-srlatch-ss envelope into record.md.

usage: summarize.py OUT_DIR   (reads OUT_DIR/esrl.envelope.json)

Exit 1 on a harness fault (missing envelope, an errored engine run, a
non-measurement diagnostic): the bench's own verdict -- latch sets or not --
is data, reported either way. A `.meas` crossing card that finds no crossing
errors in the envelope; that is the measurement's answer ("no rising edge on
Q") and is tolerated here, while `q_pre`/`pt_max`/`q_end`/`qb_end` (the
always-valued scalars) must resolve. Results are simulated, never measured.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "harness"))

import evidence  # noqa: E402

TAG = "esrl"
CROSS_MEAS = ("to_r", "t_pt_r", "t_pt_f", "t_q_r", "t_lock_r")


def ps(seconds):
    return "-" if seconds is None else f"{seconds * 1e12:.1f}"


def mv(volts):
    return "-" if volts is None else f"{volts * 1e3:.2f}"


def verdict(ms, vdd):
    half = 0.5 * vdd
    q_pre, pt_max = ms.get("q_pre"), ms.get("pt_max")
    q_end, qb_end = ms.get("q_end"), ms.get("qb_end")
    if q_pre is None or pt_max is None or q_end is None or qb_end is None:
        return "INCONCLUSIVE (a mandatory scalar measurement did not resolve)"
    if q_pre > half:
        return "RESET FAILED (Q was not 0 before the edge)"
    if pt_max < half:
        return "NO PULSE (the one-shot did not generate a pt crossing 50 % of Vdd)"
    if q_end > half and qb_end < half:
        if ms.get("t_q_r") is not None and ms.get("t_pt_f") is not None \
                and ms["t_q_r"] <= ms["t_pt_f"]:
            note = "Q rose while pt was still high"
        else:
            note = "Q rose outside the pt pulse window (after pt fell)"
        return f"SETS AND HOLDS ({note}; Q holds after pt falls, QB complementary)"
    return "DOES NOT SET (Q is not at the rail after pt fell)"


def main(out):
    env_path = os.path.join(out, f"{TAG}.envelope.json")
    if not os.path.exists(env_path):
        print(f"{TAG}: FAIL -- {env_path} missing (submit failed; see {TAG}.stderr)",
              file=sys.stderr)
        return 1
    env = evidence.load(env_path)

    problems = []
    if "error" in env:
        problems.append(f"{TAG}: {env['error'].get('code')}: {env['error'].get('message')}")
    for c in env.get("corners", []):
        for d in c.get("diagnostics", []):
            # A crossing card that found no crossing is the answer, not a fault.
            if d.get("code") == "measurement" and any(n in str(d.get("message")) for n in CROSS_MEAS):
                continue
            problems.append(
                f"{TAG} {c['corner_id']}: [{d.get('code')}] {str(d.get('message'))[:120]}")

    lines = [
        f"# {TAG} record (issue #189)", "",
        "**DIAGNOSTIC BENCH, not a graded spec result.** `sim/corners.json` states the reduced",
        "set \"is never a recorded result\"; this bench answers one question (#148 acceptance",
        "criterion 3, the follow-up the issue #145 ss probes left open): **can the three-stage",
        "`edgedet` one-shot set the plain `srlatch` at ss when its input is driven directly?**",
        "Simulated, never measured.", "",
        "## Method", "",
        "- Deck `decks/esrl.spice` = `design/netlist/lock_detector.spice` (the committed export,",
        "  the same `edgedet`/`srlatch` subcircuits the lock detector and supervisor instantiate)",
        "  + `decks/esrl_body.spice`: the latch is reset to a known Q = 0 (active-high R held",
        "  0..~3 ns, then released), and `to` is driven by one ideal rising edge (30 ps slew, the",
        "  smoke decks' own edge rate) at 5 ns -- bypassing the counter that stalls at ss,",
        "  exactly the substitution #148 names. `lockq` drives the lock detector's own",
        "  output-chain load (`inv_lv` + `inv2x_lv` + the row-12 20 fF on LOCK).",
        "- Two units in one request (`requests/esrl.request.json`, composed by",
        "  `sim/harness/gridspec.py` from the reduced set): the **question unit** at ss and a",
        "  **tt control** on the identical deck, the #145 probe convention.",
        "- All crossings graded at 50 % of the corner's own rail (the deck's `v(half)` node),",
        "  never a per-corner literal; pulse widths are derived from the rise/fall crossing",
        "  times (a file-scope `.meas` result is not readable by an in-control expression, so",
        "  the subtraction is made here, from the two recorded crossings).",
        "- The errored `.meas` crossing cards in the envelope, when present, are crossings that",
        "  do not exist (e.g. no Q rise); `q_pre`, `pt_max`, `q_end` and `qb_end` are",
        "  always-valued scalars and must resolve for a verdict.",
        "",
        "## Environment", "",
        *evidence.environment_lines({TAG: env.get("environment", {})}),
        f"- corners (as recorded): {evidence.corners_of(env)}",
        "",
        "## Result", "",
        "| corner | Q before edge (mV) | `to` rise (ps) | pt rise (ps) | pt fall (ps) |"
        " pt width (ps) | Q rise (ps) | LOCK rise (ps) | Q end (mV) | QB end (mV) | verdict |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for c in env.get("corners", []):
        ms = {m["name"]: m.get("value") if m.get("status") == "pass" else None
              for m in c.get("measurements", [])}
        width = (ms["t_pt_f"] - ms["t_pt_r"]) \
            if ms.get("t_pt_f") is not None and ms.get("t_pt_r") is not None else None
        vdd = (c.get("supply_v") or {}).get("Vdd")
        lines.append(
            f"| {c['corner_id']} | {mv(ms.get('q_pre'))} | {ps(ms.get('to_r'))} |"
            f" {ps(ms.get('t_pt_r'))} | {ps(ms.get('t_pt_f'))} | {ps(width)} |"
            f" {ps(ms.get('t_q_r'))} | {ps(ms.get('t_lock_r'))} |"
            f" {mv(ms.get('q_end'))} | {mv(ms.get('qb_end'))} | {verdict(ms, vdd)} |")

    lines += [
        "", "## What this does and does not show", "",
        "- **Shows (measured)**: whether the committed three-stage one-shot, driven on `to`,",
        "  generates a pt pulse at this corner, and whether that pulse sets the plain",
        "  `srlatch` with Q held after pt falls (QB complementary) under the lock detector's",
        "  own loads.",
        "- **Does not show**: the one-shot inside the stalled supervisor/lock-detector loop",
        "  (neither block delivers an edge at ss on the committed stimulus -- that is the",
        "  upstream failure the issue #145 probes measured); any other corner, frequency or",
        "  load; metastability.",
        "- Results are simulated, never measured.",
        "",
    ]
    if problems:
        lines += ["## Problems", "", *[f"- {p}" for p in problems], ""]
    with open(os.path.join(out, "record.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    if problems:
        print(f"{TAG}: FAIL -- {len(problems)} problem(s) recorded in record.md", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
