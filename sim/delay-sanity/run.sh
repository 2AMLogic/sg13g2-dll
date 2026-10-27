#!/usr/bin/env bash
# run.sh -- delay-line sanity bench (issue #23): delay vs control voltage per
# tap at 500 MHz and 1 GHz over the reduced corner set, every grid a `klt sim`
# request (multi-unit -> batch fleet; NO local fallback, a failed submit fails
# the run). Results are simulated, never measured, and append-only.
#
#   design/netlist.sh && sim/delay-sanity/run.sh
#
# Env: DS_CAPACITY_WAIT_S (default 900), DS_RESULTS_DIR, DS_VC (comma list)
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SIM_DIR="$(cd "${HERE}/.." && pwd)"
DESIGN_DIR="$(cd "${SIM_DIR}/../design" && pwd)"
# shellcheck source=/dev/null
source "${SIM_DIR}/harness/preflight.sh"
sim_preflight
"${DESIGN_DIR}/netlist.sh" --check

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="${DS_RESULTS_DIR:-${HERE}/results/${STAMP}}"
sim_stage_inputs "${HERE}" "${OUT}" base
mkdir -p "${OUT}/requests"
cp "${HERE}"/corners.*.json "${OUT}/"
VC="${DS_VC:-0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.08}"

declare -A VTH=([tt]=0.6 [ss]=0.54 [ff]=0.66)
declare -A PERIOD=([500MHz]=2n [1GHz]=1n)
declare -A HALF=([500MHz]=1n [1GHz]=0.5n)

# decks: the committed delay_line export + the bench body
for f in 500MHz 1GHz; do
  { cat "${DESIGN_DIR}/netlist/delay_line.spice"
    sed -e "s#@PERIOD@#${PERIOD[$f]}#" -e "s#@HALF@#${HALF[$f]}#" "${HERE}/decks/dl_bench.body.spice"
  } > "${OUT}/decks/dl_${f}.spice"
done

rc=0
for f in 500MHz 1GHz; do
  for c in ss tt ff; do
    tag="${f}_${c}"
    sed -e "s#@VTH@#${VTH[$c]}#g" -e "s#@FREQ@#${f}#g" \
        "${OUT}/base/dl.base.request.json" > "${OUT}/base/${tag}.base.request.json"
    python3 -I "${SIM_DIR}/harness/gridspec.py" "${OUT}/base/${tag}.base.request.json" \
        -o "${OUT}/requests/${tag}.request.json" --corners "${HERE}/corners.${c}.json" --ic "VC=${VC}"
    echo "run.sh: klt sim ${tag}" >&2
    klt sim "${OUT}/requests/${tag}.request.json" \
        --wait-for-capacity "${DS_CAPACITY_WAIT_S:-900}" --format json \
        -o "${OUT}/artifacts/${tag}" --report-out "${OUT}/${tag}.envelope.json" \
        > /dev/null 2> "${OUT}/${tag}.stderr" || rc=$?
    tail -2 "${OUT}/${tag}.stderr" >&2 || true
  done
done
python3 -I "${HERE}/summarize.py" "${OUT}" || rc=$?
[[ ${rc} -eq 0 ]] || { echo "run.sh: FAIL (exit ${rc}) -- see ${OUT}" >&2; exit "${rc}"; }
echo "run.sh: PASS -- ${OUT}/record.md" >&2
