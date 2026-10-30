# 0009 — Ratification of spec/target-spec.md (two-key path)

- **Status**: proposed — becomes ratified only by the operator's approval and merge of the PR that carries this record. Agents do not approve it or mark anything ratified.
- **Date**: 2026-10-27
- **Decided by**: Builder agent, issue #41 (operator ruling recorded in the issue: this repo's spec is ratified by the standard path, 2AMLogic/2am#5346)
- **Consumes**: [`../target-spec.md`](../target-spec.md); [0001](0001-spec-ratification.md); [0007](0007-rail-1p2v-thin-oxide.md); [0008](0008-false-lock-argument.md); `../../ratification/`
- **Related**: #6 (T1 items 5–8 blocked until ratification)

## What is being ratified

`spec/target-spec.md` as it stands in this PR: the 12 rows, the Locked
predicate, the false-lock criterion, the jitter method and the 45-corner set,
with the 1.2 V thin-oxide rail of 0007 and the false-lock argument of 0008. No
target, fallback or stretch **value** differs from the README table. Besides
its status line, the spec file carries the text-only revision recorded under
"Revision after the EE-key review" below.

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

## Revision after the EE-key review

The EE key's first review (head `6a77813`) returned `request-changes` on four
wordings. The operator ruled on 2026-10-29 (fleet:decide q91) that they are
fixed in text only, with no target value changed, and both keys re-run. The
changes, all in `spec/target-spec.md`:

| EE change | Row | Text change |
|---|---|---|
| A | 4 | Renamed "Systematic phase-spacing error (excludes random mismatch)". Monte Carlo stays a recorded result with no limit; the row says a consumer budgets random mismatch separately. The value (≤ 2 % T) is unchanged. A statistical limit is an operator choice and is not added here. |
| B | 5, Locked | The predicate tolerance is per column (2 / 5 / 1 % T), equal to that column's row 5 limit, as `dllbench.py --tol` already grades. The claim that row 5 is "not a consequence of the predicate" is withdrawn: row 5 is implied by lock at every column. This supersedes the wording in 0001 decision 4 and 0007 call E; those records are not edited. |
| C | 7, 8 | A graded run lasts 2 × the column's lock-time limit (2 µs target and stretch, 10 µs fallback), and row 8's "not locked by" uses it. The 5 µs fallback lock time is unchanged. |
| D | 12, Locked | LOCK may lag the predicate by ≤ 128 cycles in both directions (the two clauses no longer contradict). The predicate at t is over the 64 cycles ending at t. |

Not done here: `sim/harness/dllbench.py` still runs every column to
`TSTOP = 3.2 µs` with a fixed 64-cycle window, which is neither the 2 µs nor
the 10 µs run above. It runs against the stand-in DUT only and no recorded
result depends on it; aligning it is tracked in #49. The EE key's
non-blocking observations (row 3 stretch structure, rows 7 and 10 post-layout
re-sim, 5 mV sampling, 0005's stale rail text, 0004's stale 1 % wording, the
`ratification/` MANIFEST note) are left for the operator to direct.

## Known limits the keys should see

- No DLL comp table exists in `ratification/market-key/comps/`; the market key will report `no-comp-found` for rows without a cited public standard or part.
- Jitter (row 6) is simulated, thermal-noise class, from a method that must be validated before its first result (see the spec); it is not measured.
- The `klt` handling of a matched-array placement and extraction is unverified (0001, "Open question").

## Rejected

- Writing new keys from scratch: diverges from the shared protocol.
- A single combined review directory: the protocol fixes the two-key layout.
