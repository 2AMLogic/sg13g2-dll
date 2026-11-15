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

## Update 2026-11-15 (issue #113): both proposed redraws ran; neither closes C2 at ss with C1 intact

- **Status of this record**: the sections above are unchanged; this section appends the measured outcome
  of the follow-up issue. All figures below are simulated, never measured. Criteria C1-C3 are unchanged
  (`sim/pfd-fit/grade.py`); C2 was **not** relaxed.

Three gate runs now exist, all on the batch fleet, ngspice 47, reduced corner set:

1. **2026-11-05** (`results/20261105T125120Z`, the finding above): reset path NAND + 3 inverters on the
   shared `srlatch`. C1/C3 pass everywhere; C2 fails at 1 GHz tt (296..300 ps) and ss (472..478 ps).
2. **2026-11-15, option (2) + sized cells** (`results/20261115T001809Z`, jobs `klt-sim-42d4f35cd4e9` /
   `klt-sim-1934c6f376e3` / `klt-sim-0f13684829b1`): reset path NAND + 1 inverter on PFD-local
   `nand2x_lv`/`inv4x_lv` and `srlatch_fast` (the `srlatch` topology with 2x NANDs and a 2x R-inverter);
   seven loop stages shortened to five. **C1/C3 pass at every corner at both frequencies.** C2 passes at
   tt (223..226 ps), ff (150..152 ps) and at 500 MHz everywhere (limit 500 ps); **C2 still fails at
   ss/1 GHz: 352..358 ps.** This is the committed design.
3. **2026-11-15, three-gate reset loop** (`results/20261115T003632Z`, jobs `klt-sim-dc27f9cf6ad5` /
   `klt-sim-58c1ccea779c` / `klt-sim-69be85c983ed`): an active-low-RN latch variant fed directly from
   NAND(UP,DN) (loop of three gates), probed first at ss with a single-corner local run (228.5 ps at
   offset 0). On the full grid it reached **C2's width target** at tt (138..139 ps), ff (93..94 ps) and
   ss in settled cycles (229..235 ps) — but **fails C1 at tt, ss and ff at both frequencies**
   (ratios 0.21..0.22 at +10 ps and 1.5..1.9 in the -10..-40 ps band). It is recorded as evidence, not
   adopted; `srlatch_fast`'s committed form is the variant in run 2. At ss an unsettled start-up cycle
   also produced no UP pulse at all (width 0), which alone fails C2's 30 ps floor.

### Why the two criteria fight (measured anchors, no new model)

The UP/DN pulse ends when both the lane's own set pulse has ended *and* the shared reset has propagated.
Crossing times from run 2's envelope and the local probe put the set-release chain (edgedet pulse end ->
`srlatch`/`srlatch_fast` input inverter) at ~+403 ps after the edge at ss (probe variant: +438.6 ps), and
the reset loop at +353 ps (run 2) above the lane's rise. When the loop is shortened below the set-release
margin, the lanes' falls decouple from the reset and (wUP - wDN) stops tracking the offset — exactly the
run-3 C1 ratios above. When the loop is long enough to bind C1 at the +-10 ps offsets, the width *is* the
loop, which measured 353..472 ps at ss across the three runs. No state measured in these runs has C1
passing at ss with a width under 250 ps, and shortening the loop trades C1 failure for C2 progress at a
measured boundary between 229 and 353 ps. Closing ss inside option space (1)/(2) would require the
set-release chain itself to arrive ~150 ps earlier at ss, i.e. a shorter edge-detector pulse or a
different latch family — **a PFD topology change, not a reset-path redraw**, and out of this issue's
scope.

### Consequence and paths forward (a human decides; no agent relaxes 0006)

- `reuse.lock.json` `pfd` stays `adopting` (0006's path to `kept` requires the fit gate to pass).
- The committed design (run 2's cell set) passes C1/C3 and C2 everywhere except ss/1 GHz; the 500 MHz
  fallback target passes the whole gate unchanged.
- Option (3) of the original proposal — a ratified ss-specific relaxation of C2 — and the topology
  change sketched above both need human ratification and a new decision record; neither is done here.

