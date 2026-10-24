#!/usr/bin/env bash
# Run the pinned klt in a throwaway uv environment (never a host install).
# Pin: klayout-tools main @ KLT_COMMIT. Released 0.7.0 has no
# `klt signoff --attest`; move to a release once one carries it.
set -euo pipefail
KLT_COMMIT="fc02bdf0b6aa62e3553927511ee2de328fd1d186"
exec uvx --from "git+https://github.com/2AMLogic/klayout-tools@${KLT_COMMIT}" klt "$@"
