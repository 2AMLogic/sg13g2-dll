#!/usr/bin/env python3
"""Write record.md for a lock-detector-smoke run directory.

    summarize.py OUT_DIR KLT_EXIT_CODE

Reads OUT_DIR/ld.envelope.json. If the envelope is missing, the run errored, or
any measurement has no value, the record is NOT-RUN and quotes the first error
message verbatim; otherwise it lists each measurement against its smoke limits.
Exit 0 only when every gate passed; 6 otherwise.
"""
import json
import os
import sys


def main(argv):
    out, klt_rc = argv[1], int(argv[2])
    env_path = os.path.join(out, "ld.envelope.json")
    lines = ["# lock-detector-smoke record", "",
             "Typical corner (mos_tt, res_typ, 1.2 V, 27 C), 1 GHz, single unit, `klt sim --backend local`.",
             "Simulated, never measured. Limits are smoke gates, not spec numbers.", ""]
    ok = False
    try:
        env = json.load(open(env_path, encoding="utf-8"))
    except (OSError, ValueError):
        env = None
    errs = []
    if env is None:
        errs.append(f"no envelope written (klt exit {klt_rc}); see ld.stderr")
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
        lines += ["| measurement | value (s) | status |", "|---|---|---|"]
        for m in meas:
            lines.append(f"| {m['name']} | {m['value']:.4g} | {m.get('status')} |")
        ok = all(m.get("status") == "pass" for m in meas)
        lines += ["", "RESULT: " + ("PASS" if ok else "FAIL")]
    else:
        lines += ["RESULT: NOT-RUN", "", "Backend/engine error (verbatim):", ""]
        lines += ["    " + e for e in (errs or ["(no message)"])]
    open(os.path.join(out, "record.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0 if ok else 6


if __name__ == "__main__":
    sys.exit(main(sys.argv))
