#!/usr/bin/env bash
# run.sh -- charge-pump / cp_bias currents (issue #30): UP/DN current per corner,
# charge per pulse, dump-buffer tracking, over the reduced_set corners of
# sim/corners.json. One `klt sim` request (3 units -> batch fleet; NO local fallback:
# a failed submit fails the run). Simulated, never measured; results are append-only.
#
#   design/netlist.sh && sim/cp-currents/run.sh
#
# Env: CPI_BACKEND, CPI_CAPACITY_WAIT_S (default 900), CPI_RESULTS_DIR, CPI_DELAY_RUN
# Exit: 0 pass, 3 missing prerequisite, 6 a criterion failed or the run is NOT-RUN.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SIM_DIR="$(cd "${HERE}/.." && pwd)"
DESIGN_DIR="$(cd "${SIM_DIR}/../design" && pwd)"
# shellcheck source=/dev/null
source "${SIM_DIR}/harness/preflight.sh"
sim_preflight
"${DESIGN_DIR}/netlist.sh" --check

# K_dl (criterion K4) comes from the 1 GHz envelopes of ONE pinned delay-sanity
# run. A pin, not "the newest": a later, unrelated delay-sanity run must not
# silently move the K4 verdict of a cp-currents re-run, and the run that was
# graded against has to be stated rather than inferred. Change it with a diff
# here, or point CPI_DELAY_RUN at another delay-sanity results directory.
DELAY_RUN="${CPI_DELAY_RUN:-${SIM_DIR}/delay-sanity/results/20261105T080322Z}"
if [[ -n "${CPI_DELAY_RECORD:-}" ]]; then
  echo "run.sh: FAIL -- CPI_DELAY_RECORD is gone; K_dl is read from the envelopes now." >&2
  echo "run.sh: set CPI_DELAY_RUN to a delay-sanity results directory instead." >&2
  exit 3
fi
for c in ss tt ff; do
  [[ -f "${DELAY_RUN}/1GHz_${c}.envelope.json" ]] || {
    echo "run.sh: FAIL -- ${DELAY_RUN}/1GHz_${c}.envelope.json missing; K_dl has no input" >&2; exit 3; }
done

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="${CPI_RESULTS_DIR:-${HERE}/results/${STAMP}}"
sim_stage_inputs "${HERE}" "${OUT}" requests
{ cat "${DESIGN_DIR}/netlist/cp_bias.spice"; cat "${DESIGN_DIR}/netlist/cp.spice"; cat "${HERE}/decks/cp_body.spice"; } > "${OUT}/decks/cp_bench.spice"
# the K_dl inputs themselves, so a result directory carries what it graded against
mkdir -p "${OUT}/delay-sanity"
for c in ss tt ff; do cp "${DELAY_RUN}/1GHz_${c}.envelope.json" "${OUT}/delay-sanity/"; done
# the corner source itself, so a result directory still states what it ran at
cp "${SIM_DIR}/corners.json" "${OUT}/"
# corners come from sim/corners.json reduced_set, not from a copy in the request
python3 -I "${SIM_DIR}/harness/gridspec.py" "${OUT}/requests/cp.base.request.json" \
    -o "${OUT}/requests/cp.request.json" --reduced-set

BACKEND_ARGS=()
[[ -z "${CPI_BACKEND:-}" ]] || BACKEND_ARGS=(--backend "${CPI_BACKEND}")

rc=0
sim_submit "${OUT}" cp "${OUT}/requests/cp.request.json" \
    "${BACKEND_ARGS[@]}" --wait-for-capacity "${CPI_CAPACITY_WAIT_S:-900}" || rc=$?
python3 -I "${HERE}/summarize.py" "${OUT}" "${DELAY_RUN}" "${rc}" || exit $?
