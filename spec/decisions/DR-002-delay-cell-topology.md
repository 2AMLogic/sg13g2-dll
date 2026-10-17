# DR-002: Delay-cell topology, proven at 500 MHz before 1 GHz

- **Status**: proposed (ratified with DR-001)
- **Date**: 2026-10-17
- **Decided by**: Builder agent, issue #2
- **Related**: DR-001 (rail), DR-003 (false lock)

## Decision

1. **Topology**: single-ended **current-starved inverter** chain, one stage per
   tap pair; delay is set by a control voltage on the starving devices (the
   same family as the sibling VCO's `vco_stage`, headed by PMOS and tailed by
   NMOS, all `sg13_hv_*`). The delay line is a regular array of identical
   cells with identical loads, including a dummy load on the last tap, so
   every tap sees the same fan-out.
2. **Sequence**: topology and the false-lock argument are proven first at the
   **500 MHz fallback**, and only then at 1 GHz. 1 GHz remains the architecture
   driver; 2 GHz does not enter this decision.
3. **Phase count and stage count**: 8 taps from 16 inverting stages is not
   required by this record; the number of stages per tap and whether the
   delay line is differential is a sizing decision for the schematic issues. This
   record fixes only the family and the symmetry rule.

## Rejected

- **Differential / CML delay cell**: needs a tail-current reference and a
  second signal path; the matching and area cost is not justified before a
  single-ended line has shown it cannot meet the 2 % rows.
- **Digital (tapped inverter, mux-selected) delay line**: quantized delay
  fights the 1 % locked predicate and adds mux asymmetry between taps.

## Why 500 MHz first

At the fallback every delay budget is twice as loose, so a structural error
(loading, false lock, rail) can be separated from a speed shortfall. The
record is falsifiable: the first schematic issue reports the achievable delay
range per corner, compared with the range DR-003 needs (below).

## Delay-range requirement handed to sizing

At each corner the total delay must span from **below 0.833 ns** (T at
1.2 f0 for 1 GHz) up to **above 1.25 ns** (T at 0.8 f0), so the loop can lock
across the row-2 range. Corresponding 500 MHz fallback numbers are twice
those. This is a requirement on sizing, not a claim that the topology meets it;
no simulation exists yet.
