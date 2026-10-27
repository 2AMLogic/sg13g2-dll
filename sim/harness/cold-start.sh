#!/usr/bin/env bash
# cold-start.sh -- the one bounded command a third party runs from a fresh clone
# with the PDK installed (T1 item 9; sim/inventory.json `cold_start`). It checks
# the pins, runs the simulator-free unit tests, and builds every bench's grid
# requests into a scratch directory through gridspec.py, checking each request's
# size. It submits nothing: the benches' own run.sh do the (fleet) grids.
# Exit 0 on success, 3 on a missing prerequisite, nonzero on any failed check.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SIM_DIR="$(cd "${HERE}/.." && pwd)"
# shellcheck source=/dev/null
source "${HERE}/preflight.sh"
sim_preflight
python3 -I -m unittest discover -s "${HERE}/tests" >&2
scratch="$(mktemp -d)"
trap 'rm -rf "${scratch}"' EXIT
for bench in lock-range phase lock-time false-lock power; do
  python3 -I "${HERE}/dllbench.py" build "${SIM_DIR}/${bench}" "${scratch}/${bench}" \
      --osdi-dir "${SG13G2_OSDI_DIR}" >&2
  python3 -I "${HERE}/dllbench.py" check "${scratch}/${bench}" >&2
done
echo "cold-start: PASS (pins, unit tests, 5 benches built and checked; no simulation run)" >&2
