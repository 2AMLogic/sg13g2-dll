#!/usr/bin/env bash
# run.sh -- jitter bench placeholder (see README.md). Row 6 needs a DLL jitter deck; the noise method it must implement is spec/decisions/0014-row-6-noise-method.md.
set -euo pipefail
echo "run.sh: BLOCKED -- row 6 has no DLL jitter deck: the noise method is fixed by spec/decisions/0014-row-6-noise-method.md (proposed), but no deck or request implementing it exists in sim/jitter/; not inventing one." >&2
exit 4
