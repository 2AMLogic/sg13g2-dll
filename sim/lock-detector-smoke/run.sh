#!/usr/bin/env bash
# run.sh -- lock-detector smoke bench (issue #54): one typical-corner transient, one
# `klt sim` unit. Shows LOCK stays 0 while the delay error is out of window and while
# VCTRL moves, rises within the row-12 bound once both hold, and falls after a
# glitch. Results are simulated, never measured, and append-only.
#
#   design/netlist.sh && sim/lock-detector-smoke/run.sh
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
{ cat "${DESIGN_DIR}/netlist/lock_detector.spice"; cat "${HERE}/decks/ld_body.spice"; } > "${OUT}/decks/ld_1GHz.spice"

rc=0
sim_submit "${OUT}" ld "${OUT}/requests/ld.request.json" --backend local || rc=$?
python3 -I "${SIM_DIR}/harness/smoke_summarize.py" "${OUT}" "${rc}" lock-detector-smoke ld || exit $?
