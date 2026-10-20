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

Machine-readable corner set: [`../sim/corners.json`](../sim/corners.json)
(schema 1, consumed by `../sim/harness/gridspec.py`).

Ratification is a human-reviewed merge of 0001. Until that merge every
record is `proposed`. A ratified row is relaxed only by a new decision record.
