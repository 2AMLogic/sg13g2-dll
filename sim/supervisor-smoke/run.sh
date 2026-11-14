#!/usr/bin/env bash
# run.sh -- supervisor smoke bench (issue #53): one typical-corner transient,
# one `klt sim` unit. Shows (i) RST asserts for a delay in (1.5 T, 2 T),
# (ii) the 16-cycle rail time-out asserts RST, (iii) the first REF edge after
# a release is masked. Results are simulated, never measured, and append-only.
#
#   design/netlist.sh && sim/supervisor-smoke/run.sh
#
# The backend policy for a single unit, the SS_RESULTS_DIR knob and the exit
# codes are all defined once in the shared runner: sim/harness/smoke-run.sh.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "${HERE}/../harness/smoke-run.sh"
smoke_main "${HERE}" supervisor.spice sup sup_1GHz.spice
