#!/usr/bin/env bash
# run.sh -- lock-detector smoke bench (issue #54): one typical-corner transient, one
# `klt sim` unit. Shows LOCK stays 0 while the delay error is out of window and while
# VCTRL moves, rises within the row-12 bound once both hold, and falls after a
# glitch. Results are simulated, never measured, and append-only.
#
#   design/netlist.sh && sim/lock-detector-smoke/run.sh
#
# The backend policy for a single unit, the SS_RESULTS_DIR knob and the exit
# codes are all defined once in the shared runner: sim/harness/smoke-run.sh.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "${HERE}/../harness/smoke-run.sh"
smoke_main "${HERE}" lock_detector.spice ld ld_1GHz.spice
