# 0009 — Ratification of spec/target-spec.md (two-key path)

- **Status**: proposed — becomes ratified only by the operator's approval and merge of the PR that carries this record. Agents do not approve it or mark anything ratified.
- **Date**: 2026-10-27
- **Decided by**: Builder agent, issue #41 (operator ruling recorded in the issue: this repo's spec is ratified by the standard path, 2AMLogic/2am#5346)
- **Consumes**: [`../target-spec.md`](../target-spec.md); [0001](0001-spec-ratification.md); [0007](0007-rail-1p2v-thin-oxide.md); [0008](0008-false-lock-argument.md); `../../ratification/`
- **Related**: #6 (T1 items 5–8 blocked until ratification)

## What is being ratified

`spec/target-spec.md` as it stands in this PR, unchanged in every row and value:
the 12 rows, the Locked predicate, the false-lock criterion, the jitter method
and the 45-corner set, with the 1.2 V thin-oxide rail of 0007 and the false-lock
argument of 0008. This record does not restate them and does not change any of
them; the only edit to the spec file is its status line.

This record carries out the "Ratification" section of 0001, which left the
spec `proposed` pending a human-reviewed merge. It does not replace 0001 and
does not duplicate 0007 or 0008.

## Decisions

| # | Question | Decision |
|---|---|---|
| 1 | Path | Two non-author review keys, then the operator. EE key (`ratification/ee-key/`): technical soundness. Market key (`ratification/market-key/`): competitive positioning of externally observable rows. |
| 2 | Key installation | Both trees copied as a unit from `2AMLogic/gf180-gate-driver` `ratification/`; only the two `rubric.md` files carry a DLL section appended. Skill text and MANIFESTs are unedited. |
| 3 | Verdicts | Each key posts one `RATIFY-KEY` marker on the PR in the grammar of 2AMLogic/2am `ratification/protocol.md` §1–2 (`ee`: `approve\|request-changes`; `market`: `competitive\|adequate-for-catalog\|uncompetitive\|escalate`), from an identity that did not author the PR. |
| 4 | Decision | The operator's approval of the PR is the ratification. Neither key's verdict ratifies, and a favorable verdict does not oblige approval. |
| 5 | Spec values | No row is relaxed or changed to make a key pass. A `request-changes` or `uncompetitive` verdict goes to the operator, not to an edit of the spec. |
| 6 | After the ruling | The operator updates #6 so items 5–8 can be filed or released; the status line and 0001 are marked ratified in the operator's merge or a follow-up the operator directs. |

## Known limits the keys should see

- No DLL comp table exists in `ratification/market-key/comps/`; the market key will report `no-comp-found` for rows without a cited public standard or part.
- Jitter (row 6) is simulated, thermal-noise class, from a method that must be validated before its first result (see the spec); it is not measured.
- The `klt` handling of a matched-array placement and extraction is unverified (0001, "Open question").

## Rejected

- Writing new keys from scratch: diverges from the shared protocol.
- A single combined review directory: the protocol fixes the two-key layout.
