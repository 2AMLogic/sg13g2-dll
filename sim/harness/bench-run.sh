# Source me:  source sim/harness/bench-run.sh
#
# Shared runner for the DLL row benches (issue #28). A bench's run.sh sources
# this file and calls `bench_main "<bench dir>"`.
#
# Builds the bench's grid requests through sim/harness/dllbench.py and
# gridspec.py, submits each through `klt sim` (the host daemon's KLT_SIM_BACKEND
# routes multi-unit requests to the batch fleet; there is NO local fallback, a
# failed submit fails the run), then grades the envelopes into record.md.
# Nothing here launches ngspice.
#
# Env: BENCH_DUT        DUT descriptor (default sim/standin/dut.json, the STAND-IN)
#      BENCH_F0_HZ      column frequency: 1e9 target (default), 5e8 fallback, 2e9 stretch
#      BENCH_TOL        phase tolerance as a fraction of T (default 0.02)
#      BENCH_PMAX_MW    power limit (default 5)
#      BENCH_BACKEND    override klt's own routing (default: unset)
#      BENCH_CAPACITY_WAIT_S   wait for fleet capacity (default 900)
#      BENCH_RESULTS_DIR       default <bench>/results/<UTC stamp>
#      BENCH_BUILD_ONLY=1      build the requests, submit nothing
# Exit: 0 pass; 1 harness fault (diagnostic, missing envelope, axis not applied);
#       3 missing prerequisite; 6 harness fine but some corner fails its row.
# shellcheck shell=bash

_BENCH_HARNESS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bench_main() {
  local bench="$1"
  bench="$(cd "${bench}" && pwd)"
  # shellcheck source=/dev/null
  source "${_BENCH_HARNESS_DIR}/preflight.sh"
  sim_preflight
  local stamp out rc=0 tag req
  stamp="$(date -u +%Y%m%dT%H%M%SZ)"
  out="${BENCH_RESULTS_DIR:-${bench}/results/${stamp}}"
  python3 -I "${_BENCH_HARNESS_DIR}/dllbench.py" build "${bench}" "${out}" \
      --dut "${BENCH_DUT:-${_BENCH_HARNESS_DIR}/../standin/dut.json}" \
      --f0 "${BENCH_F0_HZ:-1e9}" --tol "${BENCH_TOL:-0.02}" --pmax-mw "${BENCH_PMAX_MW:-5}" \
      --osdi-dir "${SG13G2_OSDI_DIR}" || exit $?
  if [[ -n "${BENCH_BUILD_ONLY:-}" ]]; then
    echo "run.sh: requests built in ${out} (BENCH_BUILD_ONLY, nothing submitted)" >&2
    return 0
  fi
  local backend=()
  [[ -z "${BENCH_BACKEND:-}" ]] || backend=(--backend "${BENCH_BACKEND}")
  for req in "${out}"/requests/*.request.json; do
    tag="$(basename "${req}" .request.json)"
    echo "run.sh: klt sim ${tag}" >&2
    klt sim "${req}" "${backend[@]}" --wait-for-capacity "${BENCH_CAPACITY_WAIT_S:-900}" --format json \
        -o "${out}/artifacts/${tag}" --report-out "${out}/${tag}.envelope.json" \
        > /dev/null 2> "${out}/${tag}.stderr" || rc=$?
    tail -3 "${out}/${tag}.stderr" >&2 || true
  done
  python3 -I "${_BENCH_HARNESS_DIR}/dllbench.py" grade "${bench}" "${out}" || rc=$?
  if [[ ${rc} -ne 0 ]]; then
    echo "run.sh: exit ${rc} -- see ${out}/record.md" >&2
    return "${rc}"
  fi
  echo "run.sh: PASS -- ${out}/record.md" >&2
}
