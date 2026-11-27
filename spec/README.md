# spec

| File | Content |
|---|---|
| [`target-spec.md`](target-spec.md) | One row per parameter: min/typ/max, grading condition, corner set |
| [`decisions/0001-spec-ratification.md`](decisions/0001-spec-ratification.md) | Ratifies the spec; device flavor and rail; the lock predicate; jitter method |
| [`decisions/0002-consumer-requirements-aib.md`](decisions/0002-consumer-requirements-aib.md) | Dispositions of the `sg13g2-aib` consumer requirements G1–G5 (input to ratification; proposed) |
| [`decisions/0003-sim-harness-reuse.md`](decisions/0003-sim-harness-reuse.md) | Sim grid harness kept thin; no stamped copies (recorded, decides no spec number) |
| [`decisions/0004-delay-cell-topology.md`](decisions/0004-delay-cell-topology.md) | Delay-cell topology, proven at the 500 MHz fallback before 1 GHz |
| [`decisions/0005-false-lock-exclusion.md`](decisions/0005-false-lock-exclusion.md) | Harmonic-lock exclusion mechanism and the false-lock criterion |
| [`decisions/0006-pfd-cp-reuse.md`](decisions/0006-pfd-cp-reuse.md) | Adopt-or-keep for `sg13g2-pll`'s PFD and charge pump; `klt` array capability |
| [`decisions/0007-rail-1p2v-thin-oxide.md`](decisions/0007-rail-1p2v-thin-oxide.md) | Operator ruling 2026-10-20: rail to 1.2 V thin-oxide; 0002 reconciliation (G1, G2, G4, G5); 20 fF tap load; review calls D/E/G folded in |
| [`decisions/0008-false-lock-argument.md`](decisions/0008-false-lock-argument.md) | False-lock argument for the PFD/charge-pump polarity and edge pairing, and the PFD redraw; reasoned, not simulated (proposed) |
| [`decisions/0009-ratification-of-target-spec.md`](decisions/0009-ratification-of-target-spec.md) | Two-key ratification path for `target-spec.md`; ratified only by the operator merging its PR (proposed) |
| [`decisions/0010-delay-tap-one-stage-fallback.md`](decisions/0010-delay-tap-one-stage-fallback.md) | Two stages per tap does not reach 1 GHz at ss; proposes one stage per tap; simulated (proposed) |
| [`decisions/0011-pfd-reset-path-too-slow-at-1ghz.md`](decisions/0011-pfd-reset-path-too-slow-at-1ghz.md) | PFD fit gate fails at 1 GHz (reset pulse too wide); `pfd` stays `adopting`; simulated (proposed) |
| [`decisions/0012-cp-bias-currents-below-bounded-step-assumption.md`](decisions/0012-cp-bias-currents-below-bounded-step-assumption.md) | Charge pump delivers 2-6 uA, not the assumed 20 uA; `cp` stays `adopting`; simulated (proposed) |
| [`decisions/0013-consumer-requirements-aib-recompare.md`](decisions/0013-consumer-requirements-aib-recompare.md) | `sg13g2-aib` requirements re-compared with the columns corrected (consumer target = this spec's fallback); dispositions of the 250 MHz point, row 3's fallback phase count and row 6's fallback jitter limit, plus a dated correction to 0002's jitter fit; changes no row (proposed) |
| [`decisions/0014-row-6-noise-method.md`](decisions/0014-row-6-noise-method.md) | Row 6 noise method: one thermal `trnoise` equivalent per delay stage, calibrated per deck, validated on a known case (proposed) |
| [`decisions/0015-pfd-buffered-lane-output.md`](decisions/0015-pfd-buffered-lane-output.md) | PFD latch output moves behind a driver (`srlatch_buf`); the latch family and the gate are unchanged (proposed) |
| [`decisions/0016-ctl-1g-rest-states.md`](decisions/0016-ctl-1g-rest-states.md) | The sibling-polarity `ctl_1g` control has two dead rest states; 0008/0011 named one (proposed) |
| [`decisions/0017-row-4-monte-carlo-limit-commit-later.md`](decisions/0017-row-4-monte-carlo-limit-commit-later.md) | Commit to a Monte Carlo phase-spacing limit on row 4, value set later by a record once a post-layout locked-loop result exists; sets no number, edits no row; auto-selected, not an operator ruling (proposed) |

Machine-readable corner set: [`../sim/corners.json`](../sim/corners.json)
(schema 1, consumed by `../sim/harness/gridspec.py`).

Ratification is a human-reviewed merge of 0001. Until that merge every
record is `proposed`. A ratified row is relaxed only by a new decision record.
