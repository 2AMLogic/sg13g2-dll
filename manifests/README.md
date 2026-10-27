# Block manifest and tier-verdict record

- `sg13g2-dll.json` — block manifest (`kind: analog`). The evidence map is
  empty: every T1 row is `no_evidence`. Evidence PRs add citations here and
  regenerate the record in the same diff.
- `sg13g2-dll.signoff.json` — verdict of record, output of
  `klt signoff --manifest manifests/sg13g2-dll.json --tiers-doc manifests/design-evidence-tiers.md --format json`.
- `design-evidence-tiers.md` — the checklist the grader parses, vendored
  byte-identical from `2AMLogic/klayout-tools` `docs/design-evidence-tiers.md`
  at tag `v0.8.0` (commit `c572046be644e0407f693f2410f3abb799d68a3a`).
- `item-10-inventory.json` — repo-hygiene inventory; `evidence/item-10-repo-hygiene.json`
  is its `klt signoff --attest 10` envelope. Not yet cited by the manifest.

klt is pinned in `scripts/klt.sh` to released klayout-tools 0.8.0 on PyPI
(`klayout-tools==0.8.0`), run in a throwaway uv environment. CI (`.github/workflows/signoff.yml`) runs
`scripts/check-signoff.sh`; regenerate with `scripts/check-signoff.sh --write`.
