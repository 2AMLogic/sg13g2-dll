#!/usr/bin/env bash
# Run the pinned klt in a throwaway uv environment (never a host install).
# Pin: released klayout-tools 0.8.0 from PyPI.
set -euo pipefail
exec uvx --from "klayout-tools==0.8.0" klt "$@"
