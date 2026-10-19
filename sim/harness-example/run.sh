#!/usr/bin/env bash
# run.sh -- grid-harness example (issue #4): the pdk-smoke inverter through all
# three harness modes, every grid as a `klt sim` request.
#
#   sim/harness/common/build-osdi.sh      # once per PDK install
#   sim/harness-example/run.sh            # the example
#
#   pvt   inv_ic base x corners.pvt.example.json            (corner sweep)
#   ic    inv_ic base x corners.pvt.example.json x vic axis (start-state sweep: source vic via supply_v)
#   mc    inv_mc base x corners.mc.example.json, seed/n recorded (Monte Carlo
#         combined with process corners)
#   ctl   the mc request on the non-mismatch model sections, run twice
#         (deterministic negative control: sigma == 0, repeat identical)
#
# Grids go through `klt sim` (the host daemon's KLT_SIM_BACKEND routes
# multi-unit requests to the batch fleet). There is NO local fallback: if the
# batch submit fails this script fails. Results are simulated, never measured.
#
# Env: EXAMPLE_BACKEND       override klt's own routing (default: unset)
#      EXAMPLE_CAPACITY_WAIT_S   wait for fleet capacity (default 900)
#      EXAMPLE_RESULTS_DIR   default sim/harness-example/results/<UTC stamp>
#      EXAMPLE_MC_SEED / EXAMPLE_MC_N   default 20261018 / 8
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SIM_DIR="$(cd "${HERE}/.." && pwd)"
GRID="${SIM_DIR}/harness/gridspec.py"

# shellcheck source=/dev/null
source "${SIM_DIR}/harness/preflight.sh"
sim_preflight

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="${EXAMPLE_RESULTS_DIR:-${HERE}/results/${STAMP}}"
sim_stage_inputs "${HERE}" "${OUT}" base
mkdir -p "${OUT}/requests"
cp "${HERE}"/corners.*.example.json "${OUT}/"

SEED="${EXAMPLE_MC_SEED:-20261018}"
N="${EXAMPLE_MC_N:-8}"
B="${OUT}/base"
R="${OUT}/requests"
python3 -I "${GRID}" "${B}/inv_ic.base.request.json" -o "${R}/pvt.request.json" \
    --corners "${HERE}/corners.pvt.example.json"
python3 -I "${GRID}" "${B}/inv_ic.base.request.json" -o "${R}/ic.request.json" \
    --corners "${HERE}/corners.pvt.example.json" --ic vic=0,0.3,0.6,0.9,1.2
python3 -I "${GRID}" "${B}/inv_mc.base.request.json" -o "${R}/mc.request.json" \
    --corners "${HERE}/corners.mc.example.json" \
    --mc-n "${N}" --mc-seed "${SEED}" --mc-vary mismatch \
    --control-process mos_tt --control-process mos_ss
mv "${R}/mc.request.control.json" "${R}/ctl.request.json"

BACKEND_ARGS=()
[[ -z "${EXAMPLE_BACKEND:-}" ]] || BACKEND_ARGS=(--backend "${EXAMPLE_BACKEND}")

rc=0
for tag in pvt ic mc ctl ctl_repeat; do
  req="${R}/${tag}.request.json"
  [[ "${tag}" != ctl_repeat ]] || req="${R}/ctl.request.json"
  echo "run.sh: klt sim ${tag}" >&2
  klt sim "${req}" "${BACKEND_ARGS[@]}" \
      --wait-for-capacity "${EXAMPLE_CAPACITY_WAIT_S:-900}" --format json \
      -o "${OUT}/artifacts/${tag}" --report-out "${OUT}/${tag}.envelope.json" \
      > /dev/null 2> "${OUT}/${tag}.stderr" || rc=$?
  tail -3 "${OUT}/${tag}.stderr" >&2 || true
done

python3 -I "${SIM_DIR}/harness/evidence.py" --out "${OUT}/record.md" \
    --expect-ic vic=v0 \
    --control "${OUT}/ctl.envelope.json" --control-repeat "${OUT}/ctl_repeat.envelope.json" \
    "${OUT}/pvt.envelope.json" "${OUT}/ic.envelope.json" "${OUT}/mc.envelope.json" || rc=$?

if [[ ${rc} -ne 0 ]]; then
  echo "run.sh: FAIL (exit ${rc}) -- see ${OUT}" >&2
  exit "${rc}"
fi
echo "run.sh: PASS -- ${OUT}/record.md" >&2
