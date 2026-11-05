# Delay line: sizing note (issue #23)

Status: **provisional first-pass sizing, not simulated.** The sanity bench
(`sim/delay-sanity/`) is written but has not produced a result; see
"Evidence status". Nothing here is a measured or simulated number.

## Structure

| Cell | What | Devices (all `sg13_lv_*`, L = 0.13 µm) |
|---|---|---|
| `delay_cell` | two current-starved inverters in series, non-inverting; one cell = one tap step | per stage: head PMOS W 1.5 µm (gate VBP), inverter PMOS W 1 µm / NMOS W 0.5 µm, tail NMOS W 0.75 µm (gate VBN) |
| `tap_buffer` | two inverters, isolates the tap load from the line | stage 1: P 0.5 µm / N 0.25 µm; stage 2: P 3 µm / N 1.5 µm |
| `delay_line` | 8 `delay_cell` in series, 9 `tap_buffer` (T0 reference + T1..T8), one dummy `delay_cell` (`XDUM`) on the last tap | - |

Pins: `delay_line IN VBP VBN T0..T8 VDD VSS`. Control is two bias pins
(VBN = Vc, VBP = Vdd - Vc in the bench); bias generation belongs to the loop
issue (#24), not here.

## Choices and reasoning

- **Single-ended**, per decision 0004 (differential/CML and mux-selected lines
  are rejected there). Family: current-starved inverter, PMOS head / NMOS tail,
  as the sibling `vco_stage`; devices and lengths are re-sized for lv, not
  copied from the hv sibling.
- **Two stages per tap.** One inverting stage per tap would alternate tap
  polarity and make T8 an inverted copy of the input; two stages keep all taps
  the same polarity so tap k is the input delayed by k x T/8 and T8 is one full
  period. The cost is that each stage must be about half a tap: ~62 ps per
  stage at 1 GHz nominal and ~52 ps at ss / 1.08 V / 125 C (the 104 ps tap of
  decision 0004). The unstarved minimum lv inverter is 40/60 ps at ss into 5 fF
  (smoke record cited in 0004), so the starved stage has little headroom at the
  fast end. **This is the first thing the bench has to falsify**; if it fails,
  the fallback is one stage per tap with the polarity handled at the PFD
  (a new decision record, not a silent change).
- **L = 0.13 µm everywhere** (minimum, fastest). Longer starving devices would
  improve control linearity and are the first knob if the range is too wide.
  Head/tail are sized wider than the inverter devices so that at Vc near the
  fast end the starving devices stop limiting the stage.
- **Tap buffer** has a small first stage so each cell output sees one small
  gate (the next cell's input plus the buffer's) rather than the tap load.
  Every cell output sees exactly one delay_cell input + one tap_buffer input,
  including cell 8 (dummy cell `XDUM` + `XB8`) and the input (cell 1 + `XB0`).
- **Dummy load** is a full `delay_cell` rather than a lumped capacitor so the
  gate load matches by construction.
- **Hand-placed array.** Schematics are plain text under `design/`; the
  regular array (cell k at x = 500k, buffer k below it) was emitted once with a
  shell loop for the 27 repeated instance lines, then committed as ordinary
  source. There is no generator in the repo and `netlist.sh` does not run one.
  Revisit only if the array proves error-prone to edit by hand.

## Export

`design/netlist.sh` runs `klt netlist --block` for each top and writes
`design/netlist/*.spice`; `design/netlist.sh --check` writes nothing and exits 3
when any committed netlist differs from a fresh export. The script, not
`klt netlist --check`, does the comparison because the raw export embeds the
absolute checkout path in `** sch_path:` comments; the script rewrites that
prefix to `design/` first. (Generic tool gap, already tracked as 2AMLogic/klayout-tools#4091.)

## Evidence status

`sim/delay-sanity/run.sh` ran on the batch fleet (runner klt 0.9.0, 2026-11-05)
over the reduced corner set (tt/1.2 V/27 C, ss/1.08 V/125 C, ff/1.32 V/-40 C),
500 MHz and 1 GHz, and wrote
`sim/delay-sanity/results/20261105T080322Z/record.md` (grading in `GRADING.md`
beside it). **Simulated, never measured**: ideal bias sources, ideal 20 fF
loads, single-event delay, no jitter figure.

- 500 MHz: the two-stage tap spans T/8 (250 ps) at all three corners.
- 1 GHz: tt and ff reach T/8 (125 ps); **ss does not**: fastest tap step is
  150.7 ps against the 104 ps decision 0004 asks for. The two-stages-per-tap
  choice is falsified at 1 GHz / ss. `spec/decisions/0010-delay-tap-one-stage-fallback.md`
  proposes one stage per tap; this cell is not resized here.
- Vc <= 0.5 V (ss at 1 GHz: <= 0.6 V) gives no output edge at every corner.
- Only the three reduced corners were run; the 45-corner grade, mismatch and
  post-layout phase spacing remain open.

# False-lock supervisor: design note (issue #53)

Status: **drawn and smoke-simulated at one corner (tt / 1.2 V / 27 °C); not
characterised across PVT, not part of any false-lock proof.** Requirements are
in `spec/decisions/0005` parts 1 and 3 and `0008` "Start-up requirement"; no spec
row or record is edited here. Every number below that a record leaves open is a
**design choice, not a spec row**.

Pins: `supervisor REF TAPN TAPH EN VCTRL REFM RST VDD VSS`. `REF` is the input
clock, `TAPN`/`TAPH` are tap N and tap N/2 of the delay line, `REFM` is the masked
REF that goes to the PFD, `RST` is observable (high while the supervisor holds
VCTRL high), `VCTRL` is the loop-filter node the pull-up acts on.

## Structure

| Cell | What |
|---|---|
| `dffr_lv` | rising-edge D flip-flop from NAND2/NAND3, active-low asynchronous clear of both latches |
| `win_det` | three samples of the taps (see below) → `OVER` |
| `rail_cmp` | resistor ladder + two OTA comparators → `NHI`, `NLO`, `NEAR` |
| `timeout_cnt` | 5-stage ripple counter of REF rises, cleared while its enable is low |
| `refmask` | `dffr_lv` clocked on falling REF, cleared by `RSTB`, gates REF |
| `supervisor` | the above + reset latch (`srlatch`) + `MRST` (PMOS, W 20 µm, pulls VCTRL to VDD) |

## Behaviour and the record clause each part implements

- **Reset state is VCTRL high (0005 part 1, 0008 polarity).** `MRST` pulls VCTRL
  to VDD while the reset latch is set. The latch is set by `EN` low (power-up and
  re-enable: `EN` must be low at power-up, the latch has no other initial
  value), by `OVER`, or by a time-out pulse. It is cleared only when `NHI`
  says VCTRL is within ~50 mV of VDD **and** nothing is setting it, so the
  PFD is never released before VCTRL has actually reached the minimum-delay
  state (the release is closed-loop on VCTRL, not a fixed delay).
- **Over-delay window detector (0005 part 3).** `OVER = b_up & a_up & ~a_dn`
  with `a_up` = TAPN sampled at REF rise, `a_dn` = TAPN sampled at REF fall,
  `b_up` = TAPH sampled at REF rise. Ideal-waveform reasoning: `OVER` is true for
  d in (1.5 T, 2 T) and false on (0, 1.5 T). It repeats with period 2 T
  (true again on (3.5 T, 4 T)); **delays in (2 T, 3.5 T) are not detected by
  this window** and rely on the rail time-out (a line pushed there has its
  control at the low rail). Near lock (d = T) every sampled tap edge sits on the
  sampling edge by construction; requiring all three samples to agree is what
  keeps one metastable sample from asserting `OVER`, but this has **not** been
  shown in a noisy transient. `OVER` is used as a level, not an edge, so a
  persistent over-delay keeps the reset asserted until the line is back under
  range.
- **Rail time-out (0005 part 3).** `NEAR` = VCTRL within ~50 mV of either rail.
  `timeout_cnt` counts REF rises while `NEAR` is true and the reset is not
  asserted; its 5th bit rises on the **16th** REF rise, which is the time-out
  (design choice: 16 REF cycles, ~16 ns at 1 GHz / 32 ns at 500 MHz, long
  compared with the ≈3 cycles the loop needs to leave a 50 mV band at the
  per-cycle step of 0008). Its rising edge (edge detector, same cell as the PFD)
  sets the reset latch once; the counter is held cleared while the reset is
  asserted, so the reset's own pull to the high rail does not re-trigger it.
  The counter is cleared asynchronously in **both** latches of each flip-flop:
  with a slave-only clear, releasing the clear while the (ripple) clock was high
  clocked the counter (seen in simulation as a spurious time-out).
- **Rail-proximity threshold (0005 part 3, 50 mV).** Implemented as a ladder
  VDD - 1u - `REFH` - 22u - `REFL` - 1u - VSS of 24 equal `rppd` resistors
  (W 0.5 µm / L 8 µm, ≈ 100 kΩ total), so `REFH = 23/24 VDD`, `REFL = 1/24 VDD`:
  50 mV at 1.2 V, **proportional to VDD** (45 mV at 1.08 V, 55 mV at 1.32 V)
  rather than a fixed 50 mV. An NMOS-input OTA (VCTRL vs `REFH`) and a
  PMOS-input OTA (VCTRL vs `REFL`) each drive two inverters. Both inputs go
  through matched source followers first: fed directly at VDD - 50 mV the NMOS
  pair sat in triode (no gain) in simulation. DC sweep at tt: `NLO` flips at
  VCTRL = 0.03-0.04 V, `NHI` at 1.16 V. The comparator offset and its spread
  over PVT/mismatch is **not characterised**; it is the first thing a corner run
  should read, because the threshold, not the 50 mV label, is what sets when
  the loop is declared stuck. Step response at tt: `NLO` follows a step to the
  low rail after ≈3 ns.
- **Start-up mask (0008).** `refmask` holds a flip-flop (D tied high, clocked on
  **falling** REF, cleared by `RSTB`) and passes `REFM = REF & en`. `en` can
  only rise on a falling REF edge, while REF is low, so `REFM` has no glitch, and
  the REF edge in progress or next to come after the release is masked: the
  first REF rise `REFM` shows is the one after the first falling edge past the
  release. The clear is tied to `RSTB`, so the mask re-applies on **every**
  supervisor reset (enable, over-delay, time-out), as 0008 requires.

## Sizing (first pass, not justified by a result)

Logic cells reuse `inv_lv`, `nand2_lv`, `edgedet`, `srlatch`; `nand3_lv` P 1 µm /
N 1.5 µm. OTAs: pair 4 µm / 1 µm (HI) and 4 µm / 0.5 µm (LO), tails 0.5-1.5 µm /
1 µm with gate at the opposite rail, mirror loads 1-2 µm / 0.5-1 µm. All
`sg13_lv_*` (0007) plus `rppd`. The OTA sizes were changed twice during the
smoke work (headroom, then settling time); they are a working point, not an
optimum.

## Evidence status and what is not established

- `sim/supervisor-smoke/` ran at tt / 1.2 V / 27 °C, 1 GHz, one unit, locally
  (the 2026-11-05 dispatch worker has ngspice 46 and loads the OSDI models;
  the earlier notes about ngspice 42 do not apply to this host). See
  `sim/supervisor-smoke/results/*/record.md`. Stimulus is two ideal delayed
  copies of REF and a resistor-capacitor stand-in for the loop, **not** the
  delay line or charge pump.
- **Not established**: any other corner, supply, temperature or frequency; the
  comparator threshold spread; metastability of the window samples near lock;
  the (2 T, 3.5 T) coverage gap; that the supervisor never fires during a normal
  lock (needs the closed loop, the `sim/false-lock` bench); the 0008 claim that
  the mask makes FB_0 meet REF_1. The smoke bench has no negative control (a run
  with the mask removed was not made), so it shows the mask behaviour occurs,
  not that the gate would catch its absence.
- The supervisor adds a pull-up on VCTRL and ≈100 kΩ ladder current (≈12 µA at
  1.2 V, always on): neither is in the power budget yet.

# Lock detector: row 12 map and design choices (issue #54)

Status: **first pass, drawn against the draft (`proposed`) spec and simulated at one
corner** (`sim/lock-detector-smoke/`, tt / 1.2 V / 27 °C, 1 GHz, ideal stimulus). It
is re-graded at ratification (#41). **Two row-12 clauses are not met**; see "Not
met / not established" before relying on the block.

`lock_detector REF TAPN VCTRL LOCK VDD VSS`. `REF` is the input clock and `TAPN` the
last tap, as for the PFD. It reuses `dffr_lv`, `nand3_lv`, `edgedet` and `srlatch`
from the PFD and supervisor work and adds `vmov_cmp`. No second PFD or charge pump.

## Row-12 clause to circuit

| Row 12 clause | Circuit element |
|---|---|
| asserted only when locked; LOCK = 1 ⇒ the predicate held within the preceding 128 cycles | `LOCK` is a latch (`srlatch`) set only by the 128th consecutive good REF cycle. A cycle is good when the delay-error window (`s1`, `s2`) and the VCTRL sensor (`STILL`) are both true. The predicate itself needs 64 good cycles, so a 128-cycle count means the predicate has held for at least the last 64 cycles when LOCK rises. |
| LOCK rises within 128 cycles after the predicate first holds | Good cycles are counted from the first good one; LOCK rises at the 128th. The predicate first holds at the 64th, so the lag is 64 cycles plus synchroniser latency. Smoke: 131 cycles after the stimulus became ideal, 67 after the predicate would first hold. |
| LOCK falls within 128 cycles after it stops holding | The first not-good sample asserts `bad`, which resets the latch and asynchronously clears the counter. Smoke: LOCK fell 1.1 ns after the error was applied. |
| senses the delay error | `s1`, `s2`: TAPN and a copy delayed by 4 inverters sampled by REF delayed by 2 inverters (`dffr_lv`). `s1 & ~s2` is true when the TAPN edge is inside a window set by gate delays, not by the PFD output. |
| senses the 5 mV control-voltage criterion | `vmov_cmp`: two matched source followers copy VCTRL, one through an R-C low-pass (5 × rppd 0.5/8 µm ≈ 21 kΩ, MIM 20 × 20 µm, τ ≈ 10 ns); two OTAs with a deliberate offset flag `|VCTRL − lowpass| ≳ 5 mV`. |
| digital output at the rail, 20 fF load | `LOCK` is driven by `inv_lv` then `inv2x_lv`; smoke rise time 86 ps into 20 fF. |

Design choices that row 12 does not fix: the count is 128 (8-bit ripple counter of
REF rises, bit 8, cleared while not good); window delays are 2 and 4 inverters; the
low-pass τ is ≈ 10 ns (10 cycles at 1 GHz, 5 at 500 MHz); the movement threshold
is a width trim of one OTA device (3.59 µm against 4 µm). The counter and the
low-pass are not scaled with frequency; at 2 GHz the window and low-pass are the
same absolute times.

## Not met / not established

- **The delay window is gate-delay limited and far wider than 2 % of T.** An
  exploratory sweep of the tap-N edge offset e (uncommitted, tt, 1 GHz, run in a
  scratch directory, so it is a pointer, not evidence) accepted roughly
  −30 ps ≲ e ≲ +100 ps (about 13 % of T, centred about +35 ps), against the
  predicate's ±20 ps. The committed bench only shows that e = 0 is accepted and
  e = +240 ps is rejected. So the clause "LOCK = 1 ⇒ the predicate held" is **not
  met**: LOCK can assert for an error the predicate rejects. A 40 ps window needs a
  delay finer than an inverter; the likely fix is a window derived from the delay
  cell itself or a calibrated offset. Not attempted here.
- **Harmonic lock is not excluded by the detector.** The window cannot tell a
  delay of T from 2 T. The false-lock exclusion is the supervisor's (0005 / #53),
  and the "never 1 in a run that fails row 8" clause is therefore **not shown**;
  it is for the false-lock bench (#28).
- **The VCTRL threshold is a trim, not a spec.** At tt a whole-cell step test
  held `STILL` for +4 mV / −5 mV steps and dropped it at +5 mV / −8 mV. Moving
  the trim device by 0.1 µm went from "never flags" to "always flags". Random
  mismatch (not simulated) is wider than that window, so the real threshold at
  other corners or on silicon is unknown. A repeatable 5 mV sensor needs offset
  cancellation. Valid only for VCTRL below roughly 0.85 V (the follower outputs
  must stay under the PMOS pair's input range); above that `STILL` is
  meaningless.
- Not simulated: other corners, supplies, temperatures or frequencies; the real
  delay line, PFD and charge pump (stimulus is ideal); noise or metastability of
  `s1`/`s2` near the window edge; the 64-cycle p-p definition of the predicate
  (the low-pass flags a drift of VCTRL as movement, which is stricter than 5 mV
  p-p over 64 cycles on a slow ramp and looser on a short spike).
- Loading: the sensor adds two follower gates on VCTRL (no DC load); power of the
  always-on OTAs is not in the budget yet.
