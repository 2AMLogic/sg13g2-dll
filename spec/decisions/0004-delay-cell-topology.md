# 0004 — Delay-cell topology, proven at 500 MHz before 1 GHz

- **Status**: proposed (ratified with 0001)
- **Date**: 2026-10-17
- **Decided by**: Builder agent, issue #2
- **Related**: 0001 (rail), 0005 (false lock)

## Decision

1. **Topology**: single-ended **current-starved inverter** chain, one stage per
   tap pair; delay is set by a control voltage on the starving devices (the
   same family as the sibling VCO's `vco_stage`, headed by PMOS and tailed by
   NMOS; drawn on **`sg13_lv_*`** since [0007](0007-rail-1p2v-thin-oxide.md),
   originally `sg13_hv_*`). The delay line is a regular array of identical
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

PDK constraints on that sizing (IHP-Open-PDK `v0.3.0`; rail per 0007): the lv
model is valid for L = 0.13–10 µm and W = 0.15–10 µm (`cornerMOSlv.lib`
header) and the devices are rated "VGS ≤ 1.65 V @ 125 °C"
(`SG13G2_os_process_spec.pdf` Rev. 1.2 §2.1–2.2), so the 1.32 V corner is
inside the rating. The sibling's `vco_stage` (`sg13g2-pll`
`design/netlist/vco.spice` at `83e59fe`) is hv at `l=0.28u`; the family is
adopted, its devices and lengths are not. For scale, this repo's pinned smoke
(`sim/pdk-smoke/results/20261017T220308Z/record.md`) measured a minimum-size
lv inverter (w = 0.15 µm, l = 0.13 µm, 5 fF load, 50 ps input edges) at
tphl / tplh = 33 / 48 ps (mos_tt) and 40 / 60 ps (mos_ss), 1.2 V, 27 °C,
unstarved; the hv inverter in the same run was 87 / 178 ps at mos_ss, which is
why the rail moved. A tap at 1 GHz is 125 ps and, from the range above, must
reach 104 ps at mos_ss / 1.08 V / 125 °C into the 20 fF load of 0007.

Control-voltage margin (review finding M4): row 8 fails a run whose control
voltage parks within 50 mV of a rail, and 0005 resets on the same condition,
so sizing must place the locked control voltage **at least 100 mV from either
rail at every one of the 45 corners and all five row-2 frequencies**, with the
achieved margin reported beside the delay range. A line that needs the
exclusion zone to lock has not met this record.
