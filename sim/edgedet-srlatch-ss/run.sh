#!/usr/bin/env bash
# run.sh -- edgedet + srlatch isolated-pair bench (issue #189): can the
# three-stage `edgedet` one-shot still set the plain `srlatch` at ss, when its
# input is driven directly (bypassing the counter that stalls at ss)? This is
# the question the issue #145 ss probes could not reach and #148 acceptance
# criterion 3 re-states. Two `klt sim` units in one request: the reduced_set ss
# corner plus a tt control (the #145 probe convention), submitted to the batch
# fleet (multi-unit -> batch, NO local fallback, a failed submit fails the run).
# Results are simulated, never measured, and append-only.
#
#   design/netlist.sh && sim/edgedet-srlatch-ss/run.sh
#
# Env: ESRL_RESULTS_DIR       results directory for this invocation
#                       (default <bench dir>/results/<UTC stamp>)
#      ESRL_CAPACITY_WAIT_S   wait for fleet capacity (default 600)
# Exit: 0 record written (the bench answers either way -- a latch that does
#       not set is the answer, not a failed run); 3 missing prerequisite;
#       1 harness fault (missing envelope, an errored corner, a diagnostic)
#       -- record.md says which.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SIM_DIR="$(cd "${HERE}/.." && pwd)"
DESIGN_DIR="$(cd "${SIM_DIR}/../design" && pwd)"
# shellcheck source=/dev/null
source "${SIM_DIR}/harness/preflight.sh"
sim_preflight
"${DESIGN_DIR}/netlist.sh" --check

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="${ESRL_RESULTS_DIR:-${HERE}/results/${STAMP}}"
sim_stage_inputs "${HERE}" "${OUT}" requests
{ cat "${DESIGN_DIR}/netlist/lock_detector.spice"; cat "${HERE}/decks/esrl_body.spice"; } \
    > "${OUT}/decks/esrl.spice"

# Corners: the reduced set's own ss and tt entries (never restated here), as
# one units list in one request -- gridspec stays the one reader of
# sim/corners.json -- with the lock-detector bench's own passive sections
# added beside each MOS section (cornerRES res_typ + cornerCAP cap_typ, the
# same sections sim/lock-detector-smoke/requests/ld.request.json carries, per
# sim/corners.json whose corner axes are MOS x supply x temperature only).
python3 -I -c '
import json, sys
sys.path.insert(0, sys.argv[1])
import gridspec
res = {"lib": "libs.tech/ngspice/models/cornerRES.lib", "section": "res_typ"}
cap = {"lib": "libs.tech/ngspice/models/cornerCAP.lib", "section": "cap_typ"}
units = []
for u in gridspec.load_reduced_set(sys.argv[2])["units"]:
    if u["process"] in ("mos_ss", "mos_tt"):
        u = dict(u)
        u["process"] = {"name": u["process"], "sections": [u["process"], dict(res), dict(cap)]}
        units.append(u)
base = json.load(open(sys.argv[3]))
req = gridspec.build_request(base, corners={"units": units})
json.dump(req, open(sys.argv[4], "w"), indent=2, sort_keys=False)
' "${SIM_DIR}/harness" "${SIM_DIR}/corners.json" \
  "${OUT}/requests/esrl.base.request.json" "${OUT}/requests/esrl.request.json"

rc=0
sim_submit "${OUT}" esrl "${OUT}/requests/esrl.request.json" \
    --wait-for-capacity "${ESRL_CAPACITY_WAIT_S:-600}" || rc=$?
python3 -I "${HERE}/summarize.py" "${OUT}" || rc=$?
[[ ${rc} -eq 0 ]] || { echo "run.sh: exit ${rc} -- see ${OUT}/record.md" >&2; exit "${rc}"; }
echo "run.sh: PASS -- ${OUT}/record.md" >&2
