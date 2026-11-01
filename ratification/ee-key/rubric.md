# Verdict rubric

Three tokens, applied per row (`SKILL.md` Step 4) and rolled up to one
overall `approve`/`request-changes` verdict (`SKILL.md`'s "Output format").

Deliberately self-contained: nothing below names, numbers, or references
this repo's own internal fleet-operations detail — only device physics, the target
repo's own cited evidence, and `klayout-tools`' public
`docs/design-evidence-tiers.md`.

## `sound`

The row's claim is independently re-derivable from cited design sources
(schematic, netlist, sizing table) and/or backed by `sim/` evidence that
passes the relevant `design-evidence-tiers.md` T1 items for that row
(provenance-fresh, corner coverage matching the claim, Monte Carlo present
if the row is statistical). A row whose value is a **mechanical consequence**
of an already-ratified row plus the merged design's own structure — with no
new measurement needed — is also `sound`, provided the derivation is
actually checked against the source rather than merely asserted.

## `insufficient-evidence`

The row's value is not physically implausible, but the evidence backing it
falls short of what `design-evidence-tiers.md`'s T1 checklist requires for
the claim being made — an "informal, uncommitted" sanity check the design
doc itself disclaims as non-evidentiary, a single-corner/single-temperature
check standing in for a PVT claim, a plumbing-only `sim/` record (the DUT
never completed simulation) standing in for a design measurement, or a
statistical row backed only by a deterministic corner sweep. This is not a
verdict that the value is wrong — it is a statement that this key cannot
certify it as `sound` on the evidence actually on record, and the row should
stay unratified (or be flagged) until the gap closes.

## `unsound`

The row's claim contradicts what the cited design source, PDK physics, or
existing `sim/` evidence actually shows — a re-derivation that does not
match the PR's stated conclusion, a claim that ignores a device limit or
corner-dependent effect the block's own topology is known to be sensitive
to, or a row ratified on the back of evidence that itself failed (see the
relax-after-measured-FAIL check, `SKILL.md` Step 5) without an independent
physical justification for why the weaker value still holds. Absence of any
evidence at all for a claim with no plausible mechanical derivation is
`unsound` by default, the same way the market key's own rubric treats an
uncited value as `uncompetitive` by default rather than extending it the
benefit of the doubt.

## The EE-key / market-key jurisdiction boundary

This key reviews **every** row a ratification PR proposes for technical
soundness — unlike the market key, there is no row-classification split
into "in scope"/"out of scope" here, because every spec row makes a physical
engineering claim whether or not a buyer could observe it externally. What
this key does **not** do is rule on whether a technically sound value is
*competitive* — a row can be `sound` (physically well-derived, adequately
evidenced) and still be weak against the market, or `unsound` and still
happen to beat every public comp; the two questions are independent by
design.
Scoring competitiveness,
favorably or unfavorably, is itself a rubric violation for this key — it
lets the EE key exercise judgment over ground the two-key design reserves
for the market key, defeating the incentive-separation the mechanism exists
to protect.

## Application to this block (sg13g2-dll)

Block class: delay-locked loop. Kind: analog. Rows are those of
[`spec/target-spec.md`](../../spec/target-spec.md); the DLL-specific checks
below sharpen `sound` for each. The three verdict tokens are unchanged.

| Spec row(s) | What `sound` requires beyond the general definition |
|---|---|
| 3, 4 (output phases, phase-spacing error) | Spacing traced to the delay-cell topology (0004) and matched loads; the graded number is post-layout extracted (`klt pex`), and a schematic-only result is `insufficient-evidence` for row 4. Monte Carlo is a separate result, not a substitute for corners. |
| 5, "Locked" predicate | The predicate is re-derived from the spec text (tap N versus input + T, 64 cycles, Vctrl ripple) and the testbench implements that predicate, not a looser one. |
| 2, 7, 8, 12 (lock range, lock time, false lock, LOCK output) | Every start state of the false-lock criterion, at every one of the five frequencies, at every corner the row names. A run from a friendly initial condition alone is `insufficient-evidence`. The exclusion mechanism (0005) and the false-lock argument (0008) are re-checked against the netlist, and delay-range limits are shown to bracket exactly one period over the lock range. A harmonic lock or a rail park that the testbench would score as a pass is `unsound`. |
| 6 (added jitter) | The figure is stated with its method next to it (transient noise, run length, seeds, estimator, corners). A jitter number without its method, or one presented as measured, is `unsound`; one whose noise-source equivalents were not validated on a known case is `insufficient-evidence`. |
| 9, 10 (supply, power) | Devices are the `sg13_lv_*` family on the 1.2 V rail (0007), within the model's stated voltage range at the +10 % corner; power is graded at the worst of the 45 corners, including bias and tap buffers, not only at typical. |
| 11 (signoff) | `klt drc`, `klt lvs` and `klt pex` records are provenance-fresh against the layout in the PR. |

A row whose evidence is a plumbing-only `sim/` record (the loop never
completed a simulation) is `insufficient-evidence`, not `sound`.
`sim/` results are append-only: a record replaced instead of appended is a
provenance finding.
