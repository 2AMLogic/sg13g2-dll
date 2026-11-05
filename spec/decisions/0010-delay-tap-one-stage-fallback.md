# 0010 — Delay line: two stages per tap does not reach 1 GHz at ss; propose one stage per tap

- **Status**: proposed (needs ratification; the spec is not changed here)
- **Date**: 2026-11-05
- **Decided by**: Builder agent, issue #23
- **Related**: 0004 (topology, falsifiable), 0007 (lv devices)

## Finding (simulated, never measured)

`sim/delay-sanity/results/20261105T080322Z/` (batch fleet, runner klt 0.9.0,
reduced corner set tt/1.2 V/27 C, ss/1.08 V/125 C, ff/1.32 V/-40 C; ideal bias
sources, ideal 20 fF tap loads, single-event delay). See `GRADING.md` there.

- 500 MHz: the drawn cell (two current-starved stages per tap) spans T/8 =
  250 ps at all three corners.
- 1 GHz, ss/1.08 V/125 C: the **fastest** tap step is 150.7 ps (Vc = 1.08 V).
  Neither T/8 = 125 ps nor the 104 ps tap 0004 asks for is reachable.
  tt (101.9 ps) and ff (71.4 ps) do reach 125 ps.
- Vc <= 0.5 V (ss at 1 GHz: <= 0.6 V) produces no output edge at any corner, so
  the usable control window is narrow and sits just above a dead zone.

0004 item 3 left stages-per-tap to sizing and made the record falsifiable;
this is that falsification for two stages per tap at 1 GHz / ss. It is a
topology-sizing result, not a defect in the spec.

## Proposal

Move to **one inverting current-starved stage per tap** (halves the minimum
tap step: roughly 75 ps at ss/1 GHz, an extrapolation to be confirmed by
simulation, not a result) and handle the alternating tap polarity at the PFD /
tap-selection side; 0004 does not reject this (it fixes only the family and the symmetry rule). The
alternative of keeping two stages and widening the starving devices is not
excluded but trades matching and area for speed; sizing should compare both
before the layout issues (#25-#27) start.

## Consequences

- `design/delay_cell.sch` and the tap/line schematics change in a follow-up
  issue; this record changes no schematic and no spec row.
- Tap polarity handling must be added to the false-lock argument (0008) and the
  PFD interface (#30).
- The 500 MHz fallback is unaffected by the finding; 1 GHz remains the target.
