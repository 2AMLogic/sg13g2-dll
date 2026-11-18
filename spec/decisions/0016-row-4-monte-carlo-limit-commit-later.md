# 0016 — Row 4 gains a Monte Carlo spacing limit later (commit now, value later)

- **Status**: proposed — an agent-written record. It is not ratified, and it does not edit `spec/target-spec.md`. Any wording it proposes enters the spec only through the two-key ratification path of [0009](0009-ratification-of-target-spec.md) (#41) and the operator's merge.
- **Date**: 2026-11-18
- **Decided by**: Builder agent, issue #73. The choice recorded here was **auto-selected** in an attended `/fleet:decide` session under `--yolo 70` (confidence 72 %). It is **not an operator ruling**, and the operator may reverse it.
- **Consumes**: [`../target-spec.md`](../target-spec.md) row 4; [0009](0009-ratification-of-target-spec.md) EE change A; [0013](0013-consumer-requirements-aib-recompare.md)
- **Related**: #72 (items 1, 2, 4 of the same consumer report; it sets no limit and no σ), #41 (ratification), `2AMLogic/sg13g2-aib` T-21 (consumer's placement-error row, as reported in #72; not re-opened here)

## Problem

Row 4 of the spec (as of `9181feb`) bounds only the systematic phase-spacing error and says, in its corner-set cell: "Monte Carlo is a separate recorded result with **no limit**: this row bounds the systematic (corner, end-cell, load) spacing only, and a consumer must budget random mismatch separately."
0009, EE change A, records why: "A statistical limit is an operator choice and is not added here."

The `sg13g2-aib` consumer cannot derive its worst-case placement-error row from "no limit". It asks for a limit on the Monte Carlo spacing result or a stated σ.

## Decision

| # | Question | Decision |
|---|---|---|
| 1 | Will row 4 (or a new row) gain a statistical spacing limit? | Yes. The project commits to adding one. |
| 2 | What is its value? | **Not set here.** No limit and no σ is stated by this record. |
| 3 | When and how is the value set? | By a later decision record, once the precondition below holds, on the usual ratification path. |
| 4 | What is the answer to the consumer meanwhile? | "A limit is coming; it is not derivable yet." The consumer's row stays open until the value record lands. The current row 4 text keeps its force: random mismatch is budgeted separately. |
| 5 | Does this change the spec? | No. `spec/target-spec.md` is unchanged. This record relates to 0009 EE change A as follows: that change declined to add a limit *in that revision*; this record does not contradict it, and only commits to a future, separately ratified addition. |

### Precondition for setting the value

A Monte Carlo spacing result that is all of:

- **post-layout**: extracted from the matched delay-line array, not a schematic;
- **locked-loop**: taken with the loop locked, not an open-loop sweep at a fixed control voltage;
- stated with its method next to the number, in the manner of the jitter-method rule: corner(s), sample count n, seeds, the estimator, and the σ-estimate uncertainty at that n.

Which corner set and which n the limit is graded at is chosen by the value record, not here.

### Proposed row-4 wording (for the later value record to adopt or change)

Replace "Monte Carlo is a separate recorded result with **no limit**" by a statement that Monte Carlo spacing is graded post-layout, locked, against a limit set by the value record. This wording is a proposal only and is not applied here.

## Existing evidence (non-spec context only)

`sim/delay-sizing/results/20261107T231500Z-comparison/comparison.md` line 54 records a schematic-level sizing probe: ss/1.08 V/125 °C, 1 GHz, Vc = 1.0 V, mismatch-only, n = 32, ideal bias, no layout parasitics. Per-tap step σ: A 8.2..15.1 ps, B 12.5..16.9 ps; σ(d8): A 15.3 ps, B 19.1 ps; σ estimates carry about 13 % relative uncertainty at n = 32. It is simulated, unlocked and pre-layout. It is **not a spec result and no figure in it is offered as a σ to budget against**; it does not meet the precondition above.

## Standing obligation

A locked-loop, post-layout Monte Carlo bench is needed to meet the precondition. It is not built here and is tracked as a separate issue (#173, `loom:triage`). Until it produces a result and the value record is ratified, the consumer's worst-case placement-error row is not derivable from this repo.

## Rejected

- **Keep "no limit" indefinitely and mark the consumer's row not derivable**: leaves the consumer without a path to an answer.
- **Set a provisional number now from the schematic probe**: the probe is at 1 GHz, unlocked and pre-layout, so any number would be one no testbench supports; ranked last at curation.
- **Edit row 4 now**: spec edits need ratification, and this choice is not an operator ruling.
