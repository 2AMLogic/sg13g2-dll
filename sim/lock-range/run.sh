#!/usr/bin/env bash
# run.sh -- lock-range bench (see README.md). Grid requests go through klt sim; no local fallback.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "${HERE}/../harness/bench-run.sh"
bench_main "${HERE}"
