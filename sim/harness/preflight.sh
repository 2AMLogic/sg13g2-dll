# Source me:  source sim/harness/preflight.sh
#
# Shared preflight for the bench run.sh scripts (pdk-smoke, harness-example,
# and any DLL bench): PDK/OSDI present, klt on PATH, pins current, and the
# append-only results directory staged with the request/deck copies.
#
#   sim_preflight                          # checks; exits 3 on a missing prerequisite
#   sim_stage_inputs BENCH_DIR OUT REQ_DST # refuses an existing OUT; copies decks and
#                                          # requests (@OSDI_DIR@ substituted) into OUT/REQ_DST
# Sources env.sh, so PDK_ROOT / SG13G2_OSDI_DIR are set in the caller.
# shellcheck shell=bash

_SIM_HARNESS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "${_SIM_HARNESS_DIR}/env.sh"

sim_preflight() {
  if [[ -z "${PDK_ROOT:-}" || ! -d "${SG13G2_OSDI_DIR:-/nonexistent}" ]]; then
    echo "run.sh: FAIL -- no SG13G2 install / OSDI directory (${SG13G2_OSDI_DIR:-unset})." >&2
    echo "run.sh: build the models first: sim/harness/common/build-osdi.sh" >&2
    exit 3
  fi
  local m
  for m in psp103.osdi psp103_nqs.osdi r3_cmc.osdi mosvar.osdi; do
    if [[ ! -f "${SG13G2_OSDI_DIR}/${m}" ]]; then
      echo "run.sh: FAIL -- OSDI model ${SG13G2_OSDI_DIR}/${m} is missing; refusing to fall back to any other model." >&2
      echo "run.sh: build the models first: sim/harness/common/build-osdi.sh" >&2
      exit 3
    fi
  done
  command -v klt >/dev/null || { echo "run.sh: FAIL -- klt not on PATH" >&2; exit 3; }
  "${_SIM_HARNESS_DIR}/../check-pins.sh"
}

sim_stage_inputs() {
  local bench="$1" out="$2" req_dst="$3" r
  [[ ! -e "${out}" ]] || { echo "run.sh: FAIL -- ${out} exists; results are append-only." >&2; exit 3; }
  mkdir -p "${out}/${req_dst}"
  cp -r "${bench}/decks" "${out}/decks"
  for r in "${bench}"/requests/*.request.json; do
    sed "s#@OSDI_DIR@#${SG13G2_OSDI_DIR}#g" "${r}" > "${out}/${req_dst}/$(basename "${r}")"
  done
}
