# Source me:  source sim/harness/smoke-run.sh
#
# Shared runner for the single-unit smoke benches (issue #121), the counterpart
# of sim/harness/bench-run.sh for the row benches. A bench's run.sh sources this
# file and calls
#
#   smoke_main "<bench dir>" <netlist> <tag> <deck>
#
#   <bench dir>  the bench directory, normally "${HERE}"
#   <netlist>    the netlisted sub-block to prepend, a file under design/netlist
#                (e.g. lock_detector.spice)
#   <tag>        the file prefix of this bench's single unit: smoke_main reads
#                <bench>/decks/<tag>_body.spice and <out>/requests/<tag>.request.json
#                and writes <out>/<tag>.envelope.json and <out>/<tag>.stderr
#   <deck>       the name of the concatenated deck written into <out>/decks
#                (e.g. ld_1GHz.spice). The operating point is part of that name,
#                so it is the bench's to choose and not this runner's.
#
# The bench name in the record title is the bench directory's own basename.
#
# Backend: each of these benches is ONE `klt sim` unit, and a single unit is
# allowed to run locally, so this runner passes `--backend local` explicitly.
# It is NEVER widened into a corner or Monte Carlo grid here: a grid is a
# `klt sim` request carrying `corners`/`monte_carlo`, which goes to the batch
# fleet, and sim/harness/bench-run.sh is the runner for those. This is the one
# definition of that policy -- the bench READMEs point here rather than restate it.
#
# If the run cannot complete (model load failure, backend refusal), the record
# is NOT-RUN and quotes the engine/backend error verbatim. Nothing here launches
# ngspice. Results are simulated, never measured, and append-only.
#
# Env: SS_RESULTS_DIR   results directory for this invocation
#                       (default <bench dir>/results/<UTC stamp>)
# Exit: 0 pass, 3 missing prerequisite, 6 ran but a gate failed or NOT-RUN.
# shellcheck shell=bash

_SMOKE_HARNESS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

smoke_main() {
  local bench="${1:?usage: smoke_main BENCH_DIR NETLIST TAG DECK}"
  local netlist="${2:?usage: smoke_main BENCH_DIR NETLIST TAG DECK}"
  local tag="${3:?usage: smoke_main BENCH_DIR NETLIST TAG DECK}"
  local deck="${4:?usage: smoke_main BENCH_DIR NETLIST TAG DECK}"
  bench="$(cd "${bench}" && pwd)"
  local design_dir
  design_dir="$(cd "${_SMOKE_HARNESS_DIR}/../../design" && pwd)"
  # shellcheck source=/dev/null
  source "${_SMOKE_HARNESS_DIR}/preflight.sh"
  sim_preflight
  "${design_dir}/netlist.sh" --check

  local stamp out rc=0
  stamp="$(date -u +%Y%m%dT%H%M%SZ)"
  out="${SS_RESULTS_DIR:-${bench}/results/${stamp}}"
  sim_stage_inputs "${bench}" "${out}" requests
  { cat "${design_dir}/netlist/${netlist}"; cat "${bench}/decks/${tag}_body.spice"; } \
      > "${out}/decks/${deck}"

  sim_submit "${out}" "${tag}" "${out}/requests/${tag}.request.json" --backend local || rc=$?
  python3 -I "${_SMOKE_HARNESS_DIR}/smoke_summarize.py" \
      "${out}" "${rc}" "$(basename "${bench}")" "${tag}" || exit $?
}
