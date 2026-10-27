#!/usr/bin/env bash
# run.sh -- jitter bench placeholder (see README.md). Row 6 needs a noise-method decision record first.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if ! grep -ril 'noise method' "${HERE}/../../spec/decisions" > /dev/null 2>&1; then
  echo "run.sh: BLOCKED -- no decision record fixes the jitter noise method (spec/target-spec.md row 6); not inventing one." >&2
  exit 4
fi
echo "run.sh: a noise-method record exists but this bench has no deck yet; add it with that record's follow-up." >&2
exit 4
