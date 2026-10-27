#!/usr/bin/env bash
# run.sh -- 0006 PFD fit gate (issue #24): design/pfd.sch at 1 GHz and 500 MHz on
# the reduced_set corners of sim/corners.json, plus the control (sibling reset
# polarity) at 1 GHz. Results are simulated, never measured.
#
#   sim/harness/common/build-osdi.sh      # once per PDK install
#   design/netlist.sh --check             # pfd.spice must be current (run.sh also checks)
#   sim/pfd-fit/run.sh
#
# Every request goes through `klt sim`; multi-unit requests ride the batch fleet
# and there is NO local fallback: a failed submit fails this script (the local
# ngspice cannot load the OSDI models anyway). Writes
# sim/pfd-fit/results/<UTC stamp>/ (decks incl. the pfd.spice copy that ran,
# requests, envelopes, fit-gate.md) and refuses an existing directory.
# Exit: 0 gate passes, 1 gate fails or a run failed, 3 prerequisite missing.
#
# Env: PFDFIT_BACKEND, PFDFIT_CAPACITY_WAIT_S (default 900), PFDFIT_RESULTS_DIR
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SIM_DIR="$(cd "${HERE}/.." && pwd)"
REPO_ROOT="$(cd "${SIM_DIR}/.." && pwd)"

# shellcheck source=/dev/null
source "${SIM_DIR}/harness/preflight.sh"
sim_preflight
"${REPO_ROOT}/design/netlist.sh" --check
python3 -I "${HERE}/make_bench.py" --check

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="${PFDFIT_RESULTS_DIR:-${HERE}/results/${STAMP}}"
sim_stage_inputs "${HERE}" "${OUT}" requests
cp "${REPO_ROOT}/design/netlist/pfd.spice" "${OUT}/decks/pfd.spice"

BACKEND_ARGS=()
[[ -z "${PFDFIT_BACKEND:-}" ]] || BACKEND_ARGS=(--backend "${PFDFIT_BACKEND}")

rc=0
for tag in pfd_1g pfd_500m ctl_1g; do
  echo "run.sh: klt sim ${tag}" >&2
  klt sim "${OUT}/requests/${tag}.request.json" "${BACKEND_ARGS[@]}" \
      --wait-for-capacity "${PFDFIT_CAPACITY_WAIT_S:-900}" --format json \
      -o "${OUT}/artifacts/${tag}" --report-out "${OUT}/${tag}.envelope.json" \
      > /dev/null 2> "${OUT}/${tag}.stderr" || rc=$?
  tail -3 "${OUT}/${tag}.stderr" >&2 || true
done

python3 -I "${HERE}/grade.py" --out "${OUT}/fit-gate.md" \
    "${OUT}/pfd_1g.envelope.json" "${OUT}/pfd_500m.envelope.json" "${OUT}/ctl_1g.envelope.json" || rc=$?
if [[ ${rc} -ne 0 ]]; then
  echo "run.sh: FAIL (exit ${rc}) -- see ${OUT}" >&2
  exit 1
fi
echo "run.sh: PASS -- ${OUT}/fit-gate.md" >&2
