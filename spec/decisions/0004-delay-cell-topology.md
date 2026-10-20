# 0004 — Delay-cell topology, proven at 500 MHz before 1 GHz

- **Status**: proposed (ratified with 0001)
- **Date**: 2026-10-17
- **Decided by**: Builder agent, issue #2
- **Related**: 0001 (rail), 0005 (false lock)

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
range per corner, compared with the range 0005 needs (below).

## Delay-range requirement handed to sizing

At each corner the total delay must span from **below 0.833 ns** (T at
1.2 f0 for 1 GHz) up to **above 1.25 ns** (T at 0.8 f0), so the loop can lock
across the row-2 range. Corresponding 500 MHz fallback numbers are twice
those. This is a requirement on sizing, not a claim that the topology meets it;
no simulation exists yet.

PDK constraints on that sizing (independent review, 2026-10-20, IHP-Open-PDK
`v0.3.0`): the hv model is valid for L ≥ 0.45 µm (nmos) / 0.40 µm (pmos) and
W ≥ 0.30 µm (`cornerMOShv.lib` header), and the process specification states
the 3.3 V VGS rating for LG ≥ 0.6 µm / 0.5 µm (`SG13G2_os_process_spec.pdf`
Rev. 1.2 §2.4–2.5). The sibling's `vco_stage` (`sg13g2-pll`
`design/netlist/vco.spice` at `83e59fe`) draws its switching pair at
`l=0.28u`, below both; the family is adopted, those lengths are not. For
scale, this repo's pinned smoke
(`sim/pdk-smoke/results/20261017T220308Z/record.md`) measured a minimum-size
hv inverter (w = 0.3 µm, l = 0.45 / 0.40 µm, 5 fF load, 100 ps input edges)
at tphl / tplh = 76 / 150 ps (mos_tt) and 87 / 178 ps (mos_ss), both at
3.3 V and 27 °C, unstarved. A tap at 1 GHz is 125 ps and, from the range
above, must reach 104 ps at mos_ss / 2.97 V / 125 °C.
