#!/usr/bin/env bash
# check-pins.sh -- re-hash the vendored build script against reuse.lock.json and
# check sim/pdk.json against the installed PDK tree (issue #3). Exit non-zero
# on any mismatch. No network. Usage: sim/check-pins.sh [--lock-only]
set -euo pipefail
SIM_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${SIM_DIR}/.." && pwd)"
exec python3 -I - "${ROOT}" "${1:-}" <<'PY'
import hashlib, json, os, sys
root, flag = sys.argv[1], sys.argv[2]
bad = []
lock = json.load(open(os.path.join(root, "reuse.lock.json")))
for imp in lock["imports"]:
    if imp["mode"] != "vendored":
        continue
    for f in imp["files"]:
        p = os.path.join(root, f["local"])
        got = hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.isfile(p) else "<missing>"
        if got != f["sha256"] and not f.get("diverged"):
            bad.append(f"{f['local']}: sha256 {got} != reuse.lock.json {f['sha256']}")
        if f.get("diverged") and not os.path.isfile(os.path.join(root, f["diverged"])):
            bad.append(f"{f['local']}: diverged record {f['diverged']} missing")
if flag != "--lock-only":
    pin = json.load(open(os.path.join(root, "sim", "pdk.json")))
    pdk_root = os.environ.get("PDK_ROOT", "")
    base = os.path.join(pdk_root, os.environ.get("PDK", "ihp-sg13g2"))
    ver = os.path.join(base, ".fetched-version")
    if not os.path.isfile(ver):
        bad.append(f"installed PDK has no {ver}; cannot compare with sim/pdk.json")
    else:
        got = open(ver).read().strip().lstrip("v")
        want = pin["release_tag"].lstrip("v")
        if got != want:
            bad.append(f"installed PDK version {got} != sim/pdk.json release_tag {pin['release_tag']}")
    for rel in pin["installed_tree_must_contain"]:
        if not os.path.exists(os.path.join(base, rel)):
            bad.append(f"installed PDK lacks {rel} (sim/pdk.json installed_tree_must_contain)")
for b in bad:
    print("check-pins: FAIL " + b, file=sys.stderr)
print("check-pins: " + ("FAIL" if bad else "ok"), file=sys.stderr)
sys.exit(1 if bad else 0)
PY
