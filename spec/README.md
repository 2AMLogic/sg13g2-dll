# spec

| File | Content |
|---|---|
| [`target-spec.md`](target-spec.md) | One row per parameter: min/typ/max, grading condition, corner set |
| [`decisions/DR-001-spec-ratification.md`](decisions/DR-001-spec-ratification.md) | Ratifies the spec; device flavor and rail; the lock predicate; jitter method |
| [`decisions/DR-002-delay-cell-topology.md`](decisions/DR-002-delay-cell-topology.md) | Delay-cell topology, proven at the 500 MHz fallback before 1 GHz |
| [`decisions/DR-003-false-lock-exclusion.md`](decisions/DR-003-false-lock-exclusion.md) | Harmonic-lock exclusion mechanism and the false-lock criterion |
| [`decisions/DR-004-pfd-cp-reuse.md`](decisions/DR-004-pfd-cp-reuse.md) | Adopt-or-keep for `sg13g2-pll`'s PFD and charge pump; `klt` array capability |

Machine-readable corner set: [`../sim/corners.json`](../sim/corners.json).

Ratification is a human-reviewed merge of DR-001. Until that merge every
record is `proposed`. A ratified row is relaxed only by a new decision record.
