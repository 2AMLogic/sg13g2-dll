#!/usr/bin/env bash
# Re-run the T1 signoff and byte-compare with the committed records.
#   scripts/check-signoff.sh          # check (CI)
#   scripts/check-signoff.sh --write  # regenerate both records
# `klt signoff --manifest` exits 0 (all met) or 3 (some unmet); both are clean runs.
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
KLT=scripts/klt.sh
M=manifests
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT

run() { # $1=out ; rest = klt args
  local out=$1; shift
  "$KLT" "$@" > "$out"; local rc=$?
  if [ "$rc" -ne 0 ] && [ "$rc" -ne 3 ]; then echo "klt $* exited $rc" >&2; exit 1; fi
}
attest() { run "$1" signoff --attest 10 --inventory $M/item-10-inventory.json --format json; }
grade()  { run "$1" signoff --manifest $M/sg13g2-dll.json --tiers-doc $M/design-evidence-tiers.md --format json; }

if [ "${1:-}" = "--write" ]; then
  attest $M/evidence/item-10-repo-hygiene.json
  grade  $M/sg13g2-dll.signoff.json
  exit 0
fi
attest "$tmp/e.json"; grade "$tmp/s.json"
rc=0
for p in "e.json $M/evidence/item-10-repo-hygiene.json" "s.json $M/sg13g2-dll.signoff.json"; do
  set -- $p
  if ! cmp -s "$tmp/$1" "$2"; then
    echo "DRIFT: $2 is stale; run scripts/check-signoff.sh --write and commit" >&2
    diff <(python3 -m json.tool "$tmp/$1") <(python3 -m json.tool "$2") >&2
    rc=1
  fi
done
[ $rc -eq 0 ] && echo "signoff records are fresh"
exit $rc
