"""Grade the three klt sim envelopes and write record.md (issue #3).

usage: summarize.py <results-dir> <repo-root>
Exits non-zero unless every expected corner passed with zero diagnostics.
All figures are simulated, never measured.
"""
import hashlib
import json
import os
import subprocess
import sys

EXPECT = {"inv_lv": 3, "inv_hv": 3, "npn_op": 1}


def main(out, root):
    problems, rows, env = [], [], {}
    for tag, n in EXPECT.items():
        path = os.path.join(out, tag + ".envelope.json")
        if not os.path.isfile(path):
            problems.append(f"{tag}: no envelope (klt sim failed before reporting; see {tag}.stderr)")
            continue
        d = json.load(open(path))
        if "error" in d:
            problems.append(f"{tag}: {d['error'].get('message')}")
            continue
        env[tag] = d["environment"]
        if d.get("corner_count") != n or d.get("passed") != n or d.get("status") != "pass":
            problems.append(f"{tag}: expected {n}/{n} pass, got status={d.get('status')} passed={d.get('passed')}/{d.get('corner_count')}")
        for c in d.get("corners", []):
            for x in c.get("diagnostics", []):
                problems.append(f"{tag} {c['corner_id']}: [{x['code']}] {x['message'][:160]}")
            vals = ", ".join(f"{m['name']}={m['value']:.4g}" if m.get("value") is not None else f"{m['name']}=none" for m in c["measurements"])
            rows.append(f"| {tag} | {c['corner_id']} | {c['status']} | {vals} |")
    pin = json.load(open(os.path.join(root, "sim", "pdk.json")))
    commit = subprocess.run(["git", "-C", root, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    dirty = bool(subprocess.run(["git", "-C", root, "status", "--porcelain", "--", "sim", "reuse.lock.json"], capture_output=True, text=True).stdout.strip())
    e = next(iter(env.values()), {})
    engines = sorted({f"{v.get('engine')} {v.get('engine_version')}" for v in env.values()})
    osdi = {o["name"]: o["sha256"] for o in e.get("osdi_preload", [])}
    remote = {
        t: {k: (v.get("remote") or {}).get(k) for k in ("job_id", "instance_type", "ami_id", "lifecycle")}
        for t, v in env.items()
    }
    lines = [
        "# pdk-smoke record",
        "",
        "SIMULATED results, never measured. Device-family load check only; no design.",
        "",
        f"- Verdict: **{'FAIL' if problems else 'PASS'}**",
        f"- sg13g2-dll commit: `{commit}`" + (" (working tree dirty under sim/)" if dirty else ""),
        f"- PDK pin: IHP-Open-PDK `{pin['release_tag']}` (`sim/pdk.json`)",
        f"- OSDI models (sha256 of the binaries the run loaded): " + "; ".join(f"`{k}` {v[:16]}…" for k, v in osdi.items()),
        f"- OSDI build: `sim/harness/common/build-osdi.sh` (OpenVAF-Reloaded {pin['osdi_toolchain']['compiler_tag']}), see `reuse.lock.json`",
        f"- ngspice (as run, on the batch fleet): {', '.join(engines)}; the dispatch worker's local ngspice 42 cannot load these OSDI v0.4 models",
        f"- klt: {subprocess.run(['klt', '--version'], capture_output=True, text=True).stdout.strip()}",
        f"- backend: batch fleet; jobs: {json.dumps(remote)}",
        "",
        "| request | corner | status | measurements (V, s, A) |",
        "|---|---|---|---|",
        *rows,
        "",
    ]
    if problems:
        lines += ["## Problems", *[f"- {p}" for p in problems], ""]
    open(os.path.join(out, "record.md"), "w").write("\n".join(lines))
    for p in problems:
        print("summarize: " + p, file=sys.stderr)
    return 1 if problems else 0


sys.exit(main(*sys.argv[1:3]))
