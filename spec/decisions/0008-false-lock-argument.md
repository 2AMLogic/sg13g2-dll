# 0008 — False-lock argument for the PFD/charge-pump loop, and the PFD redraw

- **Status**: proposed (builds on 0005, which is proposed until 0001 is merged by a human)
- **Date**: 2026-10-27
- **Decided by**: Builder agent, issue #24
- **Related**: 0005 (mechanism), 0006 (PFD/CP reuse, fit gate), 0007 (rail)

0005 chose the exclusion mechanism and left the full argument to precede
sizing. This record gives it for the **PFD/charge-pump polarity and edge
pairing**, which is what the PFD/CP schematics of issue #24 fix. It is a
**reasoned** argument: no simulation backs it yet (see "What is not
established"). The lock detector and supervisor are not drawn by this record's
PR; their requirements are stated here.

## Edge pairing decides the loop's sign

Let d be the total delay (tap N), T the period, REF_k the input edge at kT, FB_k
the same edge after the line (at kT + d). A tri-state PFD pairs edges by the
order it sees them.

- **Paired REF_k with FB_k** (REF first): UP is high for d. For 0 < d < T the
  error looks positive and growing with d, whatever the sign convention, so a
  loop that corrects it settles at d → 0 (or runs to the far rail), never at T.
  This is the minimum-delay false lock 0005 part 2 warns about.
- **Paired FB_k with REF_{k+1}** (FB first, as when the PFD has already seen
  REF_k before FB_k arrives and treats REF_k as consumed): DN is high for
  T − d. The error is positive-DN for d < T and, once d > T so that REF_{k+1}
  arrives before FB_k, UP for d − T. The error crosses zero **at d = T** and has
  the right sign on both sides.

So lock at one period needs (a) the second pairing and (b) a loop that raises
delay on DN and lowers it on UP.

## Polarity chosen (interface assumption for the delay line, issue #23)

- DN pulse (FB leads REF) → charge pump sinks → VCTRL falls → **delay rises**.
- UP pulse (FB lags REF) → charge pump sources → VCTRL rises → **delay falls**.
- Hence the delay cell must be faster at high VCTRL (NMOS-starved tail gate on
  VCTRL, as `vco_stage` in the sibling), and the **minimum-delay start** of 0005
  part 1 is VCTRL forced to the **high** rail. If issue #23 picks the opposite
  control polarity, the charge pump's UP/DN legs swap at the top level; this
  record and `design/README.md` then change together.

## Start-up requirement on the (not yet drawn) supervisor

0005 part 1 forces minimum delay before the PFD may act. That is necessary and,
by the argument above, not sufficient: the **first REF edge after the PFD is
released must be masked** so that FB_0 meets REF_1, not REF_0. A flip-flop
clocked by the falling REF edge that enables REF into the PFD does this (REF_0
has passed, so the enable arrives mid-period, before REF_1). The same masking is
re-applied on every supervisor reset (0005 part 3, rail time-out), because a
reset at an arbitrary phase re-creates the wrong pairing. The supervisor
schematic must implement it and the false-lock testbench (issue #28) must
measure it from every start state of the spec.

## Bounded step (0005 part 2), as a sizing constraint

Per input cycle the control voltage moves by at most
ΔV = I_cp · t_pulse / C_loop, with t_pulse ≤ T (a full-period error). The delay
changes by K_dl · ΔV, with K_dl the line's delay-per-volt (issue #23, not yet
known). The constraint is K_dl · I_cp · T / C_loop ≪ T, i.e.
K_dl · I_cp / C_loop ≪ 1. First-pass values in `design/`: C_loop = one 26 µm ×
26 µm MIM capacitor (≈ 1 pF at the MIM density the PDK documents; not
extracted here), I_cp set by `cp_bias` to a few tens of µA. For I_cp = 20 µA and
T = 1 ns, ΔV ≤ 20 mV per cycle, 5 % of T per cycle if K_dl were 2.5 ns/V. These
are arithmetic on assumed values; the charge-pump current and K_dl are to be
**simulated and replaced**, not trusted.

## PFD redraw: what differs from the sibling

The PFD is `sg13g2-pll`'s topology (edge detectors → set/reset latches,
shared reset from AND(UP, DN)) redrawn on `sg13_lv_*` (0006 amended by 0007).
Reading the sibling's exported netlist at `83e59fe` (`design/netlist/pfd.spice`),
its reset path is NAND(UP, DN) followed by **two** inverters (`XI1`, `XI2`),
which leaves the reset equal to NAND(UP, DN): high except when both outputs are
high, the opposite of the latch's active-high reset. As read, the latches are
held in reset and UP/DN would follow the edge-detector pulses instead of the
phase difference. The redraw uses NAND followed by **three** inverters, giving
reset = AND(UP, DN) delayed. This is a reading of the netlist, **not a
simulation of the sibling**: the control bench `sim/pfd-fit/decks/ctl_1g.spice`
(sibling polarity on the same lv cells) exists to confirm or refute it and has
not been run. The sibling's charge-pump dump buffer biases from `ICN`; the
redraw uses `IBN`, since the follower tail needs a mirror gate voltage, not a
cascode gate.

## What is not established

- **No simulation has been run for any part of this PR.** The batch backend
  returned `InvalidAccessKeyId` on submit from the dispatch host and the local
  ngspice (42) cannot load the OSDI v0.4 models, so the 0006 fit gate (PFD dead
  zone and reset-pulse width at 1 GHz and 500 MHz) has **not** been run. The
  bench, grader and runner are committed and the grader is unit-tested on a
  synthetic ideal PFD only.
- The pairing argument is not shown in a transient; issue #28 owns that.
- Pass criteria for the fit gate (fixed in `sim/pfd-fit/grade.py` before any
  result): no dead zone above 10 ps (signed pulse-width difference within
  0.5–1.5× the input offset for every |offset| ≥ 10 ps), and a reset-pulse width
  of 30 ps to 0.25 T, on the three `reduced_set` corners. A failure is recorded
  in a new decision record proposing a replacement, never a silent edit.
