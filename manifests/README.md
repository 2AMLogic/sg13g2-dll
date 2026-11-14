# Block manifest and tier-verdict record

- `sg13g2-dll.json` — block manifest (`kind: analog`). The evidence map cites
  item 10 only; every other T1 row is `no_evidence`. Evidence PRs add
  citations here and regenerate the record in the same diff.
- `sg13g2-dll.signoff.json` — verdict of record, output of
  `klt signoff --manifest manifests/sg13g2-dll.json --tiers-doc manifests/design-evidence-tiers.md --format json`.
- `design-evidence-tiers.md` — the checklist the grader parses, vendored
  byte-identical from `2AMLogic/klayout-tools` `docs/design-evidence-tiers.md`
  at tag `v0.8.0` (commit `c572046be644e0407f693f2410f3abb799d68a3a`).
- `item-10-inventory.json` — repo-hygiene inventory; `evidence/item-10-repo-hygiene.json`
  is its `klt signoff --attest 10` envelope, cited by the manifest under
  `evidence."10"` with the inventory's content hash pinned.

The pin covers the records in this directory and nothing else.
`scripts/check-signoff.sh` is the only caller of `scripts/klt.sh`, which runs
released klayout-tools 0.8.0 from PyPI (`klayout-tools==0.8.0`) in a throwaway
uv environment, so `klt signoff` grading is reproducible at a stated version.
The netlist export (`design/netlist.sh`) and the simulation benches do not go
through that wrapper — they run the `klt` on `PATH`. Only some bench runs record
which version that was (see `sim/README.md`); the netlist export records none,
because it strips klt's `** klt-netlist-inputs:` provenance header on purpose
(`design/NOTES.md`). CI (`.github/workflows/signoff.yml`) runs
`scripts/check-signoff.sh`; regenerate with `scripts/check-signoff.sh --write`.
