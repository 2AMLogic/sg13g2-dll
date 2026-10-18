#!/usr/bin/env python3
"""Read `klt sim` envelopes and grade harness evidence.

Checks are pure (dict in, list of problems out) so they are unit-testable
without a simulator. The CLI writes a Markdown record naming what each
envelope is: corner sweep, initial-condition sweep, or Monte Carlo (with
seed, sample count and the negative-control verdict). All numbers are
simulated, never measured.

usage: evidence.py --out record.md [--expect-ic SOURCE=MEAS]
           [--control CONTROL.json [--control-repeat CONTROL2.json]] ENVELOPE.json...
Exit 1 if any problem is found.
"""

from __future__ import annotations

import argparse
import json
import os
import sys


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def kind(env, ic_source=None):
    """Classify an envelope: 'mc', 'ic' (sweeps `ic_source`), or 'corners'."""
    if (env.get("environment") or {}).get("monte_carlo"):
        return "mc"
    if ic_source and any(ic_source in (c.get("supply_v") or {}) for c in env.get("corners", [])):
        return "ic"
    return "corners"


def basic_problems(name, env):
    """Envelope-level problems: error, non-pass status, diagnostics."""
    if "error" in env:
        return [f"{name}: {env['error'].get('code')}: {env['error'].get('message')}"]
    out = []
    if env.get("status") != "pass":
        out.append(f"{name}: status={env.get('status')} passed={env.get('passed')}/{env.get('corner_count')}")
    for c in env.get("corners", []):
        for d in c.get("diagnostics", []):
            out.append(f"{name} {c['corner_id']}: [{d.get('code')}] {str(d.get('message'))[:120]}")
    return out


def mc_facts(env):
    """Seed, sample count, vary and scope as recorded in the envelope."""
    mc = (env.get("environment") or {}).get("monte_carlo") or {}
    return {k: mc.get(k) for k in ("seed", "n", "vary", "seed_scope")}


def mc_sigmas(env):
    """{"<measurement> @ <corner>": stddev} -- the spread within ONE process
    corner. The pooled stddev also contains corner-to-corner spread, which is
    not Monte Carlo variation, so it is only a fallback when the envelope has
    no per-corner block."""
    out = {}
    for m in env.get("measurements", []):
        block = m.get("monte_carlo")
        if block is None:
            continue
        per = block.get("by_corner")
        if per:
            for c in per:
                out[f"{m['name']} @ {c['corner_id']}"] = c.get("stddev")
        else:
            out[m["name"]] = block.get("stddev")
    return out


def check_mc_recorded(name, env):
    problems = []
    facts = mc_facts(env)
    for k in ("seed", "n"):
        if facts.get(k) is None:
            problems.append(f"{name}: envelope does not record monte_carlo {k}")
    if not mc_sigmas(env):
        problems.append(f"{name}: no per-measurement monte_carlo statistics")
    return problems


def check_negative_control(name, env):
    """Every measurement sigma is exactly 0 with the mismatch switch off."""
    problems = check_mc_recorded(name, env)
    for meas, sigma in mc_sigmas(env).items():
        if sigma is None or sigma != 0:
            problems.append(f"{name}: negative control sigma({meas})={sigma}, expected exactly 0")
    return problems


def check_signal_present(name, env):
    """The positive side: a mismatch-on run must show nonzero spread somewhere."""
    if any(s not in (None, 0) for s in mc_sigmas(env).values()):
        return []
    return [f"{name}: mismatch-on Monte Carlo shows zero spread in every measurement"]


def _values(env):
    return {
        c["corner_id"]: {m["name"]: m.get("value") for m in c.get("measurements", [])}
        for c in env.get("corners", [])
    }


def check_reproducible(name, env_a, env_b):
    """Same request, same seed -> identical per-corner measurement values."""
    a, b = _values(env_a), _values(env_b)
    if a.keys() != b.keys():
        return [f"{name}: repeat run has different corners"]
    return [f"{name}: {cid} measurement values differ between repeat runs" for cid in a if a[cid] != b[cid]]


def check_ic_applied(name, env, source, meas, tol=0.02):
    """The start-state axis took effect: measurement `meas` equals the swept
    `source` value in every row, and at least two distinct states ran."""
    problems = []
    for c in env.get("corners", []):
        want = (c.get("supply_v") or {}).get(source)
        got = {m["name"]: m.get("value") for m in c.get("measurements", [])}.get(meas)
        if want is None or got is None:
            problems.append(f"{name} {c['corner_id']}: missing {source!r} or measurement {meas!r}")
            continue
        if abs(got - want) > tol:
            problems.append(f"{name} {c['corner_id']}: {meas}={got} but {source}={want}")
    states = {(c.get("supply_v") or {}).get(source) for c in env.get("corners", [])}
    if len(states - {None}) < 2:
        problems.append(f"{name}: an initial-condition sweep needs >= 2 distinct start states, saw {len(states - {None})}")
    return problems


def render(items, ic_source=None):
    lines = ["# Harness evidence record", "", "SIMULATED results, never measured.", ""]
    for path, env in items:
        name = os.path.basename(path)
        if "error" in env:
            lines += [f"## {name}", f"- error: {env['error'].get('message')}", ""]
            continue
        k = kind(env, ic_source)
        lines.append(f"## {name} ({k})")
        lines.append(f"- status: {env.get('status')}; corners: {env.get('passed')}/{env.get('corner_count')} pass")
        e = env.get("environment") or {}
        backend = e.get("backend")
        backend = backend.get("resolved") if isinstance(backend, dict) else backend
        lines.append(f"- engine: {e.get('engine')} {e.get('engine_version')}; backend: {backend}")
        job = (e.get("remote") or {}).get("job_id")
        if job:
            lines.append(f"- batch job: {job}")
        if k == "mc":
            f = mc_facts(env)
            lines.append(f"- Monte Carlo: seed={f['seed']} n={f['n']} vary={f['vary']} seed_scope={f['seed_scope']}")
            lines.append("- sigma within one process corner: " + ", ".join(f"{m}={s}" for m, s in mc_sigmas(env).items()))
        lines.append("")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("envelopes", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--expect-ic", metavar="SOURCE=MEAS", help="envelopes sweeping this source are start-state sweeps; MEAS must equal the source value")
    ap.add_argument("--control", help="negative-control envelope (mismatch switch off)")
    ap.add_argument("--control-repeat", help="second run of the same control request")
    args = ap.parse_args(argv)
    ic_source, _, ic_meas = (args.expect_ic or "").partition("=")
    items = [(p, load(p)) for p in args.envelopes]
    problems = []
    for name, env in items:
        problems += basic_problems(name, env)
        if "error" in env:
            continue
        if kind(env, ic_source) == "mc":
            problems += check_mc_recorded(name, env) + check_signal_present(name, env)
        if kind(env, ic_source) == "ic":
            problems += check_ic_applied(name, env, ic_source, ic_meas)
    if args.control:
        ctl = load(args.control)
        items.append((args.control, ctl))
        problems += basic_problems(args.control, ctl)
        if "error" not in ctl:
            problems += check_negative_control(args.control, ctl)
            if args.control_repeat:
                problems += check_reproducible(args.control, ctl, load(args.control_repeat))
    text = render(items, ic_source) + "\n## Verdict: " + ("FAIL" if problems else "PASS") + "\n"
    if problems:
        text += "\n" + "\n".join(f"- {p}" for p in problems) + "\n"
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(text)
    for p in problems:
        print(f"evidence: {p}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
