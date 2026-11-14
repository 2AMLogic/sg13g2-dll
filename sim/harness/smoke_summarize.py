#!/usr/bin/env python3
"""Write record.md for a single-unit smoke-bench run directory.

    smoke_summarize.py OUT_DIR KLT_EXIT_CODE BENCH PREFIX

Reads OUT_DIR/PREFIX.envelope.json. If the envelope is missing, the run errored,
or any measurement has no value, the record is NOT-RUN and quotes the first error
message verbatim; otherwise it lists each measurement against its smoke limits,
with the unit the envelope recorded for it.
Exit 0 only when every gate passed; 6 otherwise.

The run conditions (corner, supply, temperature, engine, backend) are read from
the envelope, never stated as a constant: a bench run at another corner or on
another backend records what it actually ran on, and a run that produced no
envelope records no conditions at all rather than a plausible-looking guess.

BENCH names the bench in the record title; PREFIX is the file prefix the bench's
run.sh uses for its envelope and stderr (e.g. ``ld`` -> ld.envelope.json).
"""
import json
import os
import sys


def run_conditions(env):
    """The run conditions this envelope recorded, as record lines ([] if none)."""
    if not env:
        return []
    e = env.get("environment") or {}
    backend = e.get("backend")
    backend = backend.get("resolved") if isinstance(backend, dict) else backend
    parts = []
    corners = env.get("corners") or []
    if corners:
        c = corners[0]
        bits = [str(c["process"])] if c.get("process") else []
        bits += [f"{n} {v:g} V" for n, v in sorted((c.get("supply_v") or {}).items()) if v is not None]
        if c.get("temperature_c") is not None:
            bits.append(f"{c['temperature_c']:g} C")
        if bits:
            parts.append("corner " + ", ".join(bits)
                         + (f" (+{len(corners) - 1} more)" if len(corners) > 1 else ""))
    engine = " ".join(str(x) for x in (e.get("engine"), e.get("engine_version")) if x)
    if engine:
        parts.append(f"engine {engine}")
    if backend:
        parts.append(f"backend {backend}")
    return [f"Run conditions, as the envelope recorded them: {'; '.join(parts)}."] if parts else []


def build_record(out, klt_rc, bench, prefix):
    """Return (record lines, ok) for the run in `out`."""
    env_path = os.path.join(out, f"{prefix}.envelope.json")
    ok = False
    try:
        with open(env_path, encoding="utf-8") as f:
            env = json.load(f)
    except (OSError, ValueError):
        env = None
    lines = [f"# {bench} record", ""] + run_conditions(env) + [
        "Simulated, never measured. Limits are smoke gates, not spec numbers.", ""]
    errs = []
    if env is None:
        errs.append(f"no envelope written (klt exit {klt_rc}); see {prefix}.stderr")
    else:
        if env.get("error"):
            errs.append(str(env["error"].get("message", env["error"])))
        for c in env.get("corners", []):
            errs += [d.get("message", "") for d in c.get("diagnostics", []) if d.get("severity") == "error"]
    meas = []
    if env:
        for c in env.get("corners", []):
            meas += c.get("measurements", [])
    if env and not errs and meas and all(m.get("value") is not None for m in meas):
        lines += ["| measurement | value | unit | status |", "|---|---|---|---|"]
        for m in meas:
            lines.append(f"| {m['name']} | {m['value']:.4g} | {m.get('unit') or '?'} | {m.get('status')} |")
        ok = all(m.get("status") == "pass" for m in meas)
        lines += ["", "RESULT: " + ("PASS" if ok else "FAIL")]
    else:
        lines += ["RESULT: NOT-RUN", "", "Backend/engine error (verbatim):", ""]
        lines += ["    " + e for e in (errs or ["(no message)"])]
    return lines, ok


def main(argv):
    out, klt_rc, bench, prefix = argv[1], int(argv[2]), argv[3], argv[4]
    lines, ok = build_record(out, klt_rc, bench, prefix)
    with open(os.path.join(out, "record.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0 if ok else 6


if __name__ == "__main__":
    sys.exit(main(sys.argv))
