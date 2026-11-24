# 0017 — `vmov_cmp` takes its threshold from a replica-referenced stage, not from a width trim and an inverter trip

- **Status**: proposed. **This record relaxes no `spec/` row and redefines nothing in row 12**:
  the lock predicate, its 128-cycle timing and the 20 fF `LOCK` load are untouched. It changes how
  the VCTRL-movement clause of row 12 is sensed inside `vmov_cmp`. Its merge ratifies nothing.
- **Date**: 2026-11-24
- **Decided by**: Builder agent, issue #196 (part of #148)
- **Consumes**: [0015](0015-pfd-buffered-lane-output.md) (premise: the 1 GHz target is retained;
  nothing here depends on the PFD change beyond that); the #189 DC probe
  `sim/lock-detector-smoke/results/20261121T004307Z-dcprobe/` (the baseline this record is written against)
- **Related**: #148 (parent), #195 (sibling supervisor-sampler remedy, a different block), #41 (full PVT and
  Monte Carlo grade, which this record does not pre-empt)

## Problem, as measured before this change

The #189 settled DC sweep (`vmov_cmp` alone, equal OTA inputs, reduced-set corners) gave the
`STILL = 1` quiet window of the committed sensor as `[0, 0.4774)` V at ss / 1.080 V / 125 °C,
`[0, 0.6125)` V at tt and `[0, 0.8523)` V at ff. The smoke stimulus sits at `VCTRL = 0.600 V`
(ripple band 0.585–0.615 V), so it is outside the window at ss and 12.5 mV inside the edge at tt.
At ss both OTA outputs rested at 0.580 V, a few mV above the trip of the `inv_lv` that follows
each of them, so `STILL` could not assert whatever the ripple did.

Mechanism: the sensor's threshold was the sum of two things that both move with the corner.
(1) A 0.1 µm width trim (3.59 µm against 4 µm) of the OTA mirror-diode device, which sets
where the OTA output sits at equal inputs. (2) The trip voltage of a minimum inverter reading
that output. Nothing tied one to the other, so the "quiet" state sat at a different distance
from the inverter trip at every corner.

## Decision

Keep the four pins (`VCTRL`, `STILL`, `VDD`, `VSS`), the two source followers, the R-C low-pass
and the two OTAs, and the sole consumer (`XMOV` in `lock_detector`). Change two things inside
`vmov_cmp` (`design/tools/cells.py`):

1. **Both OTAs become balanced** (mirror-diode and output device both 4 µm / 1 µm; the 3.59 µm
   trim is removed). At equal inputs the OTA output `oa`/`ob` rests at its own mirror-diode
   node `da`/`db`.
2. **The inverter that read the OTA output is replaced by a replica-referenced stage** per OTA:
   a PMOS diode `MQPxR` loaded by a replica NMOS `MQNxR` (2 µm / 0.5 µm, gate = the OTA's own
   diode node `da`/`db`), a PMOS mirror `MQPxS`, and a sense NMOS `MQNxS` (1.6 µm / 0.5 µm,
   gate = the OTA output `oa`/`ob`). The stage output `sa`/`sb` is an **active-high stillness
   flag**: high until the OTA output has risen above its diode node by the amount at which
   the 1.6 µm sense device passes the replica's current. `STILL = sa AND sb` (the existing
   `nand2_lv` + `inv_lv`).

Why this answers the mechanism: the stage's trip is a property of the **same OTA's own diode node**
and a width ratio of two same-length devices (1.6 : 2), not of a minimum inverter in another
sizing family. Trip and rest point now move together with process, supply and temperature, so the
quiet state keeps its distance from the trip. The threshold is set by the ratio (1.6 µm against
2 µm), which is a sizing choice with a stated sensitivity, not a trim on a 0.1 µm width.

How a quiet 0.600 V is recognised and motion is still detected: with equal OTA inputs the sense
device carries less current than the replica branch, so `sa`/`sb` sit at a high level. A VCTRL step
moves `vsa` against the low-passed `vsb` (the low-pass has τ ≈ 10 ns); the OTA output moves off
its diode node, the sense device takes over the replica's current and the flag falls.

## What the evidence shows (simulated, never measured; reduced-set corners tt / ss / ff)

All three runs are batch-fleet jobs, ngspice 47, deck = the committed
`design/netlist/lock_detector.spice` plus the bench body, the bench's own passive sections
(`cornerRES res_typ`, `cornerCAP cap_typ`) added beside each corner's MOS section as in the #189
probe. The reduced set is a diagnostic set and is never a recorded spec grade (`sim/corners.json`).

| evidence | location | result |
|---|---|---|
| Quiet-input DC sweep, 0–1.32 V at 5 mV (job `klt-sim-e0f3decc1a82`) | `sim/lock-detector-smoke/results/20261124T025009Z-dcprobe/` | `STILL` is high over the **whole** 0–1.32 V sweep at tt, ss and ff (minimum 1.2 V / 1.0796 V / 1.32 V, i.e. the rail less 0.4 mV at ss, at VCTRL = 0.05 V). At the smoke band 0.585 / 0.600 / 0.615 V `STILL` = rail at all three corners. The window no longer has an upper edge below 0.85 V at any corner; the margin to the old tt edge (0.6125 V) is not applicable. |
| VCTRL step test, ±3, ±5, ±8 mV, 200 ps edge, 20 fF `STILL` load (job `klt-sim-9a2a88a9b045`) | `sim/lock-detector-smoke/results/20261124T024845Z-stepprobe/` | At tt, ss and ff `STILL` **holds for +3 / −3 mV steps and drops for +5 / −5 mV steps**, then recovers inside 100 ns. At ff the ±5 mV minimum is 1.4–10.7 mV (not 0 V), which is a drop to under 1 % of the 1.32 V rail. The previous topology's tt step test held 4 mV up / 5 mV down and dropped at 5 mV up / 8 mV down. |
| Two-unit smoke transient ss + tt control, existing probe request (job `klt-sim-4e6f46403325`) | `sim/lock-detector-smoke/results/20261124T023824Z-probe/` | `LOCK` rises at **356.95 ns** at ss (353.08 ns at tt), falls at **521.42 ns** (521.10 ns) after the +240 ps error begins at 520 ns, and reacquires at **711.95 ns** (710.08 ns). Zero `LOCK` crossings before 353 ns at either corner, i.e. through the 60–220 ns ripple phase and the 220–353 ns settling. |
| Existing tt smoke bench (job `klt-sim-2bc256fbc022`) | `sim/lock-detector-smoke/results/20261124T023824Z-smoke/` | All five existing smoke gates pass: `t_rise1` 353.1 ns (gate 284–412), `t_fall1` 521.1 ns (gate 520–648), `t_rise2` 710.1 ns (gate 644–772), `lock_max_before_220n` 41 µV, `t_edge_lock` 86 ps. |

`still` at ss is not flat during the ripple (it pulses high for about 0.7 ns once per 20 ns cycle, 16 crossings
in 60–220 ns, against 32 at tt) and settles high at 225.55 ns (tt 222.88 ns), after the ripple ends at 220 ns.
`good` follows it, the counter stays cleared, the first `to` rises at 356.53 ns at ss (352.81 ns at tt) and the
one-shot sets the latch at 356.65 ns. The failure of the #145 probe is gone: its `to`/`pt`/`lock` chain, which
that probe could not exercise at ss, now executes at ss as well.

## Operating range this evidence supports

- Quiet VCTRL from 0 to the 0.85 V ceiling the committed documentation states, at tt, ss and ff, with
  the sensor flagging steps of about ±5 mV and holding below ±3 mV, at those three corner points only.
- **Above about 0.85 V the PMOS input pairs turn off and `STILL` stays high** (DC sweep: high at 1.0 V and 1.315 V
  at all three corners). The sensor then cannot flag movement. This is the same validity limit as before
  (the previous sensor also left its window above ~1.09 V); it is stated here because `STILL` high
  is not "VCTRL is quiet" outside the validity range.
- No other supply, temperature or process point, no mismatch and no Monte Carlo (#41).

## Cost and what is not shown

- **Supply current** at VCTRL = 0.600 V rises from 128 / 65 / 194 µA (tt / ss / ff, #189) to
  **217 / 123 / 364 µA**: the two replica branches (`MQNxR`/`MQPxR`) and their mirrors are always on. The
  sizing is **not optimised for power**; the replica NMOS (2 µm, gate ≈ 0.5 V) pulls its diode node to
  0.23–0.30 V, so the mirror devices run at a large overdrive. Power is not in the budget yet (`design/NOTES.md`).
- **Mismatch is not simulated.** The threshold is now a ratio of two devices and the OTA input pair is no longer
  trimmed, so the threshold's spread follows the sense/replica pair and the OTA pair mismatch. Whether it
  stays inside the 3–5 mV window at the 45-corner grade, or under Monte Carlo, is #41's question.
  The step test brackets the threshold only at 3 mV (held) and 5 mV (dropped); it is somewhere in
  between at each corner, not located.
- The ±5 mV step test is on the instantaneous follower input against the low-pass. A slow VCTRL drift
  below the low-pass corner is attenuated and may not flag; this is the previous limitation, unchanged.
- The tt smoke gates are unchanged. `t_fall1` is 1.1 ns above its lower gate edge, as it was in the previous tt
  record (both 5.211e-7 s), so that gate's margin is thin independent of this change.

## Alternatives considered

- **Re-trim the width** (3.3–4.0 µm for the mirror-diode device). Exploratory, single-corner, local
  ngspice runs in a scratch directory, not committed evidence: the quiet OTA output moved by about 0.2 V
  across that 0.7 µm range, and the step threshold diverged by corner — at 3.75 µm ss flagged at 10 mV
  while tt and ff did not flag at 10 mV. A width retune moves the failure, it does not make the corners
  agree. Rejected.
- **Skew the inverter**: still reads the OTA output against a trip that does not track the OTA's own rest point.
- **Clocked or switched-capacitor offset cancellation**: changes the four-pin interface and adds a clock to
  a block that has none; revisit only if #41's Monte Carlo grade requires it.
- **Shift the smoke stimulus below 0.47 V, relax row 12's VCTRL clause, or bypass `vmov_cmp`**: out of scope
  or prohibited (no harness change, no spec relaxation).

## Follow-ups

- #41: grade the threshold over the full PVT grid and Monte Carlo; the power increase belongs in the same pass.
- A DC `.op` current report for the OTA tails is still blocked by the OSDI current-vector gap filed as
  2AMLogic/klayout-tools#6997; the block supply current is recorded instead.
