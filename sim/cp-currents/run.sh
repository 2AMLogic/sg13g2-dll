#!/usr/bin/env bash
# run.sh -- charge-pump / cp_bias currents (issue #30): UP/DN current per corner,
# charge per pulse, dump-buffer tracking, over the reduced_set corners of
# sim/corners.json. One `klt sim` request (3 units -> batch fleet; NO local fallback:
# a failed submit fails the run). Simulated, never measured; results are append-only.
#
#   design/netlist.sh && sim/cp-currents/run.sh
#
# Env: CPI_BACKEND, CPI_CAPACITY_WAIT_S (default 900), CPI_RESULTS_DIR, CPI_DELAY_RECORD
# Exit: 0 pass, 3 missing prerequisite, 6 a criterion failed or the run is NOT-RUN.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SIM_DIR="$(cd "${HERE}/.." && pwd)"
DESIGN_DIR="$(cd "${SIM_DIR}/../design" && pwd)"
# shellcheck source=/dev/null
source "${SIM_DIR}/harness/preflight.sh"
sim_preflight
"${DESIGN_DIR}/netlist.sh" --check

DELAY_RECORD="${CPI_DELAY_RECORD:-$(ls -d "${SIM_DIR}"/delay-sanity/results/*/ | sort | tail -1)record.md}"
[[ -f "${DELAY_RECORD}" ]] || { echo "run.sh: FAIL -- no delay-sanity record.md for K_dl" >&2; exit 3; }

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="${CPI_RESULTS_DIR:-${HERE}/results/${STAMP}}"
sim_stage_inputs "${HERE}" "${OUT}" requests
{ cat "${DESIGN_DIR}/netlist/cp_bias.spice"; cat "${DESIGN_DIR}/netlist/cp.spice"; cat "${HERE}/decks/cp_body.spice"; } > "${OUT}/decks/cp_bench.spice"
cp "${DELAY_RECORD}" "${OUT}/delay-sanity.record.md"
# the corner source itself, so a result directory still states what it ran at
cp "${SIM_DIR}/corners.json" "${OUT}/"
# corners come from sim/corners.json reduced_set, not from a copy in the request
python3 -I "${SIM_DIR}/harness/gridspec.py" "${OUT}/requests/cp.base.request.json" \
    -o "${OUT}/requests/cp.request.json" --reduced-set

BACKEND_ARGS=()
[[ -z "${CPI_BACKEND:-}" ]] || BACKEND_ARGS=(--backend "${CPI_BACKEND}")

rc=0
klt sim "${OUT}/requests/cp.request.json" "${BACKEND_ARGS[@]}" \
    --wait-for-capacity "${CPI_CAPACITY_WAIT_S:-900}" --format json \
    -o "${OUT}/artifacts" --report-out "${OUT}/cp.envelope.json" \
    > /dev/null 2> "${OUT}/cp.stderr" || rc=$?
tail -3 "${OUT}/cp.stderr" >&2 || true
python3 -I "${HERE}/summarize.py" "${OUT}" "${OUT}/delay-sanity.record.md" "${rc}" || exit $?
