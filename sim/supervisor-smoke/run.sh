#!/usr/bin/env bash
# run.sh -- supervisor smoke bench (issue #53): one typical-corner transient,
# one `klt sim` unit. Shows (i) RST asserts for a delay in (1.5 T, 2 T),
# (ii) the 16-cycle rail time-out asserts RST, (iii) the first REF edge after
# a release is masked. Results are simulated, never measured, and append-only.
#
#   design/netlist.sh && sim/supervisor-smoke/run.sh
#
# Backend: a single unit is allowed to run locally, so this passes
# `--backend local` explicitly; it is NEVER widened into a corner/MC grid here.
# If the run cannot complete (model load failure, backend refusal), the script
# writes a NOT-RUN record that quotes the engine/backend error and exits 6.
# Exit: 0 pass, 3 missing prerequisite, 6 ran but a gate failed or NOT-RUN.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SIM_DIR="$(cd "${HERE}/.." && pwd)"
DESIGN_DIR="$(cd "${SIM_DIR}/../design" && pwd)"
# shellcheck source=/dev/null
source "${SIM_DIR}/harness/preflight.sh"
sim_preflight
"${DESIGN_DIR}/netlist.sh" --check

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="${SS_RESULTS_DIR:-${HERE}/results/${STAMP}}"
sim_stage_inputs "${HERE}" "${OUT}" requests
{ cat "${DESIGN_DIR}/netlist/supervisor.spice"; cat "${HERE}/decks/sup_body.spice"; } > "${OUT}/decks/sup_1GHz.spice"

rc=0
klt sim "${OUT}/requests/sup.request.json" --backend local --format json \
    -o "${OUT}/artifacts" --report-out "${OUT}/sup.envelope.json" \
    > /dev/null 2> "${OUT}/sup.stderr" || rc=$?
python3 -I "${SIM_DIR}/harness/smoke_summarize.py" "${OUT}" "${rc}" supervisor-smoke sup || exit $?
