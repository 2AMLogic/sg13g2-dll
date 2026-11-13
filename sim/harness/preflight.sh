# Source me:  source sim/harness/preflight.sh
#
# Shared preflight for the bench run.sh scripts (pdk-smoke, harness-example,
# and any DLL bench): PDK/OSDI present, klt on PATH, pins current, and the
# append-only results directory staged with the request/deck copies.
#
#   sim_preflight                          # checks; exits 3 on a missing prerequisite
#   sim_stage_inputs BENCH_DIR OUT REQ_DST # refuses an existing OUT; copies decks and
#                                          # requests (@OSDI_DIR@ substituted) into OUT/REQ_DST
#   sim_submit OUT TAG REQUEST [args...]   # submits REQUEST through `klt sim`; the per-bench
#                                          # policy args (--backend, --wait-for-capacity) are
#                                          # the caller's. Returns klt's own exit status.
#   sim_reduced_corner_vdd SECTION         # prints the Vdd of that reduced_set corner of
#                                          # sim/corners.json (gridspec.py is the only reader)
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

# The one fleet-submit definition every bench runner shares: announce the tag,
# submit REQUEST through `klt sim`, keep the artifacts under OUT/artifacts/TAG and
# the report in OUT/TAG.envelope.json, capture stderr to OUT/TAG.stderr and echo
# its tail so a failed submit always states its reason, then return klt's own exit
# status so the caller keeps its `|| rc=$?`.
#
# Everything that differs by bench is a caller argument, not a knob here: the
# backend override (`--backend local` for a single-unit smoke, a per-bench
# BACKEND_ARGS array otherwise) and `--wait-for-capacity`, which every batch
# submit passes.
sim_submit() {
  local out="${1:?usage: sim_submit OUT TAG REQUEST [klt sim args...]}"
  local tag="${2:?usage: sim_submit OUT TAG REQUEST [klt sim args...]}"
  local req="${3:?usage: sim_submit OUT TAG REQUEST [klt sim args...]}"
  shift 3
  local rc=0
  echo "run.sh: klt sim ${tag}" >&2
  klt sim "${req}" "$@" --format json \
      -o "${out}/artifacts/${tag}" --report-out "${out}/${tag}.envelope.json" \
      > /dev/null 2> "${out}/${tag}.stderr" || rc=$?
  tail -3 "${out}/${tag}.stderr" >&2 || true
  return "${rc}"
}

# Print the Vdd of one reduced_set corner of sim/corners.json, by model section
# (e.g. mos_ss). Goes through gridspec.load_reduced_corner so the corner values
# have exactly one reader, and a section not in the reduced set fails loudly.
sim_reduced_corner_vdd() {
  local section="${1:?usage: sim_reduced_corner_vdd SECTION}"
  python3 -I -c '
import sys
sys.path.insert(0, sys.argv[1])
import gridspec
try:
    corner = gridspec.load_reduced_corner(sys.argv[2], sys.argv[3])
except gridspec.GridError as exc:
    sys.exit(f"sim_reduced_corner_vdd: FAIL -- {exc}")
print(repr(corner["supply_v"]["Vdd"][0]))
' "${_SIM_HARNESS_DIR}" "${_SIM_HARNESS_DIR}/../corners.json" "${section}"
}
