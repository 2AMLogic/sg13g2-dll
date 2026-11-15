#!/usr/bin/env bash
# run.sh -- SG13G2 device-family smoke (issue #3): a minimum-size `sg13_lv_*`
# inverter transient at mos_tt/mos_ff/mos_ss. The hv inverter and npn13G2 legs
# were removed with issue #96; decision 0007 put the block on 1.2 V
# thin-oxide CMOS with no hv rail and no SiGe HBT.
#
#   sim/harness/common/build-osdi.sh      # once per PDK install
#   sim/pdk-smoke/run.sh                  # the smoke
#
# Grids go through `klt sim` (the host daemon's KLT_SIM_BACKEND routes
# multi-unit requests to the batch fleet). There is NO local fallback: if the
# batch submit fails this script fails. It also refuses to run, with a
# non-zero exit, when the OSDI models are missing, and it fails when any
# corner reports a model-load diagnostic or does not pass. Results are
# simulated, never measured.
#
# Env: SMOKE_BACKEND (default: klt's own routing / KLT_SIM_BACKEND)
#      SMOKE_CAPACITY_WAIT_S (default 900) wait for fleet capacity
#      SMOKE_RESULTS_DIR (default sim/pdk-smoke/results/<UTC stamp>)
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SIM_DIR="$(cd "${HERE}/.." && pwd)"
REPO_ROOT="$(cd "${SIM_DIR}/.." && pwd)"

# shellcheck source=/dev/null
source "${SIM_DIR}/harness/preflight.sh"
sim_preflight

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="${SMOKE_RESULTS_DIR:-${HERE}/results/${STAMP}}"
sim_stage_inputs "${HERE}" "${OUT}" requests

BACKEND_ARGS=()
[[ -z "${SMOKE_BACKEND:-}" ]] || BACKEND_ARGS=(--backend "${SMOKE_BACKEND}")

rc=0
sim_submit "${OUT}" inv_lv "${OUT}/requests/inv_lv.request.json" \
    "${BACKEND_ARGS[@]}" --wait-for-capacity "${SMOKE_CAPACITY_WAIT_S:-900}" || rc=$?

python3 -I "${SIM_DIR}/harness/evidence.py" --out "${OUT}/record.md" \
    --title "pdk-smoke record" --provenance "${REPO_ROOT}" \
    --expect inv_lv=3 \
    "${OUT}/inv_lv.envelope.json" || rc=$?
if [[ ${rc} -ne 0 ]]; then
  echo "run.sh: FAIL (exit ${rc}) -- see ${OUT}" >&2
  exit "${rc}"
fi
echo "run.sh: PASS -- ${OUT}/record.md" >&2
