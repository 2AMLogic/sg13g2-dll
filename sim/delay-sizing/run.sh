#!/usr/bin/env bash
# run.sh -- delay-tap sizing comparison (issue #67): candidate A (one inverting
# starved stage per tap) vs candidate B (two stages, widened starving devices)
# on the delay-sanity bench method. Every grid is a `klt sim` request (multi-unit
# -> batch fleet; NO local fallback). Results are simulated, never measured, and
# append-only.
#
#   design/netlist.sh && sim/delay-sizing/run.sh probe   # scale probe + bench regression, ss/1 GHz
#   DS_B_SCALE=4 sim/delay-sizing/run.sh full            # A,B x ss/tt/ff x 1 GHz/500 MHz
#   DS_B_SCALE=4 sim/delay-sizing/run.sh fine            # finer Vc near the ff dead-zone edge
#   DS_B_SCALE=4 sim/delay-sizing/run.sh mc              # Monte Carlo matching, ss/1 GHz
#
# Env: DS_CAPACITY_WAIT_S (default 600), DS_RESULTS_DIR, DS_VC (comma list),
#      DS_B_SCALE (B starving-device width factor, default 2), DS_MC_N (32),
#      DS_MC_SEED (20261107), DS_MC_VC (1.0)
set -euo pipefail

MODE="${1:?usage: run.sh probe|full|fine|mc}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SIM_DIR="$(cd "${HERE}/.." && pwd)"
DESIGN_DIR="$(cd "${SIM_DIR}/../design" && pwd)"
# shellcheck source=/dev/null
source "${SIM_DIR}/harness/preflight.sh"
sim_preflight
"${DESIGN_DIR}/netlist.sh" --check

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="${DS_RESULTS_DIR:-${HERE}/results/${STAMP}-${MODE}}"
[[ ! -e "${OUT}" ]] || { echo "run.sh: FAIL -- ${OUT} exists; results are append-only." >&2; exit 3; }
mkdir -p "${OUT}/requests" "${OUT}/base"
# the corner source itself, plus the Monte Carlo set this bench owns, so a
# result directory still states what it ran at
cp "${SIM_DIR}/corners.json" "${HERE}/corners.ss_mismatch.json" "${OUT}/"
VC="${DS_VC:-0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.08}"
SCALE="${DS_B_SCALE:-2}"
echo "klt $(klt --version) ; B scale ${SCALE} ; mode ${MODE}" > "${OUT}/tool-versions.txt"

rc=0
# submit TAG VARIANT FREQ CORNER VCLIST [gridspec extra args...]
submit() {
  local tag="$1" var="$2" f="$3" c="$4" vc="$5"; shift 5
  local vdd vth corner_args=()
  # logic threshold = half this corner's rail, read from sim/corners.json
  vdd="$(sim_reduced_corner_vdd "mos_${c}")"
  vth="$(awk -v v="${vdd}" 'BEGIN{printf "%g", v/2}')"
  # CORNERS_FILE is the Monte Carlo escape hatch (corners.ss_mismatch.json names a
  # mismatch model section, which is not in the reduced set); otherwise the harness
  # reads the corner out of sim/corners.json.
  if [[ -n "${CORNERS_FILE:-}" ]]; then
    corner_args=(--corners "${CORNERS_FILE}")
  else
    corner_args=(--reduced-corner "mos_${c}")
  fi
  python3 -I "${HERE}/make_bench.py" --variant "${var}" --freq "${f}" --vth "${vth}" \
      --b-scale "${SCALE}" --out "${OUT}"
  sed -i "s#@OSDI_DIR@#${SG13G2_OSDI_DIR}#g" "${OUT}/base/${var}_${f}.base.request.json"
  python3 -I "${SIM_DIR}/harness/gridspec.py" "${OUT}/base/${var}_${f}.base.request.json" \
      -o "${OUT}/requests/${tag}.request.json" "${corner_args[@]}" --ic "VC=${vc}" "$@"
  echo "run.sh: klt sim ${tag}" >&2
  klt sim "${OUT}/requests/${tag}.request.json" \
      --wait-for-capacity "${DS_CAPACITY_WAIT_S:-600}" --format json \
      -o "${OUT}/artifacts/${tag}" --report-out "${OUT}/${tag}.envelope.json" \
      > /dev/null 2> "${OUT}/${tag}.stderr" || rc=$?
  tail -2 "${OUT}/${tag}.stderr" >&2 || true
}

case "${MODE}" in
  probe)
    PV="${DS_VC:-0.8,1.0,1.08}"
    submit base_ss_1GHz base 1GHz ss "${PV}"
    submit a_ss_1GHz a 1GHz ss "${PV}"
    for s in 1.5 2 3 4; do
      SCALE="${s}" submit "b${s}_ss_1GHz" b 1GHz ss "${PV}"
    done ;;
  full)
    for v in a b; do for f in 1GHz 500MHz; do for c in ss tt ff; do
      submit "${v}_${f}_${c}" "${v}" "${f}" "${c}" "${VC}"
    done; done; done ;;
  fine)
    # finer Vc grid at ff (where the 0.1 V grid of `full` steps over the dead-zone edge)
    FV="${DS_VC:-0.40,0.44,0.48,0.52,0.56,0.60,0.64,0.68,0.72}"
    for v in a b; do for f in 1GHz 500MHz; do
      submit "${v}_${f}_ff" "${v}" "${f}" ff "${FV}"
    done; done ;;
  mc)
    for v in a b; do
      CORNERS_FILE="${HERE}/corners.ss_mismatch.json" submit "${v}_mc_ss_1GHz" "${v}" 1GHz ss "${DS_MC_VC:-1.0}" \
          --mc-n "${DS_MC_N:-32}" --mc-seed "${DS_MC_SEED:-20261107}" --mc-vary mismatch \
          --control-process mos_ss
      mv "${OUT}/requests/${v}_mc_ss_1GHz.request.control.json" "${OUT}/requests/${v}_ctl_ss_1GHz.request.json"
      for t in ctl ctl_repeat; do
        r="${v}_${t}_ss_1GHz"; req="${OUT}/requests/${v}_ctl_ss_1GHz.request.json"
        echo "run.sh: klt sim ${r}" >&2
        klt sim "${req}" --wait-for-capacity "${DS_CAPACITY_WAIT_S:-600}" --format json \
            -o "${OUT}/artifacts/${r}" --report-out "${OUT}/${r}.envelope.json" \
            > /dev/null 2> "${OUT}/${r}.stderr" || rc=$?
      done
    done ;;
  *) echo "run.sh: unknown mode ${MODE}" >&2; exit 2 ;;
esac
python3 -I "${HERE}/summarize.py" "${MODE}" "${OUT}" || rc=$?
[[ ${rc} -eq 0 ]] || { echo "run.sh: FAIL (exit ${rc}) -- see ${OUT}" >&2; exit "${rc}"; }
echo "run.sh: PASS -- ${OUT}/record.md" >&2
