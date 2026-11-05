# 0011 — PFD fit gate fails at 1 GHz (reset pulse too wide); `pfd` stays `adopting`

- **Status**: proposed (needs a follow-up issue; the spec is not changed here)
- **Date**: 2026-11-05
- **Decided by**: Builder agent, issue #30
- **Related**: 0006 (the gate), 0008 (reset polarity, "PFD redraw"), 0007 (lv devices)

## Finding (simulated, never measured)

`sim/pfd-fit/results/20261105T125120Z/fit-gate.md` (batch fleet, ngspice 46, jobs
`klt-sim-eb16fa919cbc` / `klt-sim-c9bb349b8d7c` / `klt-sim-937e4b7536d6`; reduced corner
set; criteria C1-C3 unchanged from `sim/pfd-fit/grade.py`).

- **C1 (no dead zone above 10 ps) and C3 pass** at every corner at both frequencies:
  (wUP - wDN) tracks the input offset to within about 1 ps down to the +-5 ps points.
- **C2 (reset-pulse width 30 ps .. 0.25 T) fails at 1 GHz** in two of three corners:
  tt/1.2 V/27 C 296..300 ps and ss/1.08 V/125 C 472..478 ps against the 250 ps limit; ff/1.32 V/-40 C
  passes (197..199 ps). At 500 MHz (limit 500 ps) all three corners pass.
- The reset pulse is set by the NAND + three-inverter reset path, not by the frequency, so the
  same 300 ps (tt) is simply a larger fraction of T at 1 GHz (30 % tt, 47 % ss).
- **Control (`ctl_1g`, sibling reset polarity on the same lv cells)** fails C1 at all three corners
  ((wUP - wDN)/offset between -0.33 and +0.15, i.e. no usable phase response). The 0008 claim that
  the sibling's NAND + two-inverter reset does not work holds on these cells. This confirms the
  reading in 0008; it is not a statement about the sibling's own (hv) implementation.

## Consequence

`reuse.lock.json` `pfd` stays `adopting`. 0006 makes a gate failure a new decision record, not a
silent patch; this is it. No schematic or spec row changes here.

## Proposal (for a follow-up issue; not simulated)

Shorten the reset path so the pulse falls inside 30 ps .. 250 ps at ss/1.08 V/125 C as well. Options,
in the order I would try them: (1) size up the reset-path inverters / the NAND (keeps the three-inverter
polarity of 0008); (2) a faster NAND + one-inverter or AND-type reset, which keeps the polarity the
control showed is needed but must be re-checked against C2's 30 ps floor at ff; (3) keep the cell and ask
for a ratified relaxation of C2 for ss (the gate is fixed by 0006 and agents do not relax it). The 500 MHz
fallback target already passes unchanged. Any redraw re-runs `sim/pfd-fit/run.sh`.
