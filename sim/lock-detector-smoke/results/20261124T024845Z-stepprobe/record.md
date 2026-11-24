# lock-detector-smoke record (vmov_cmp VCTRL step probe, revised sensor, issue #196)

**PROBE, not a graded spec result** (`sim/corners.json`: the reduced set is never a recorded result).
Simulated, never measured.

## Question

The settled DC sweep (`../20261124T025009Z-dcprobe/`) cannot show the motion threshold: with the low-pass cap open both OTA
inputs are equal. Does the replica-referenced sensor of decision
[0017](../../../../spec/decisions/0017-vmov-cmp-replica-threshold.md) hold `STILL` for small VCTRL movement and drop it
near the 5 mV criterion at every reduced-set corner?

## Method

- `vmov_cmp` alone (`XDUT vctrl still vdd 0 vmov_cmp`, `STILL` loaded with 20 fF), driven by an ideal VCTRL
  source that is quiet at 0.600 V and then takes steps (200 ps edge) of +3, −3, −3, +3, +5, −5, −5, +5, +8, −8, −8, +8 mV,
  one step every 100 ns from 100 ns (the sequence returns to 0.600 V; the 10 ns low-pass recovers inside 100 ns,
  checked by `still_end_s*` below). `.tran 20p 1300n`. `STILL` is read as its minimum over the 60 ns after each step.
  Deck: `decks/vmov_step.spice` = regenerated `design/netlist/lock_detector.spice` (commit `a1fe9a5`) + the step body; deck
  identity `sha256:6827e381e6c3486c3d309772bb260600a135a61a697100f016d431fefa6ecd62`.
- tt / ss / ff reduced-set corners with the bench's passive sections (as `../20261124T025009Z-dcprobe/`). Submitted
  `--backend batch --wait-for-capacity 600`; batch job `klt-sim-9a2a88a9b045`, ngspice 47, 22 s, all three units `pass`.
- The steps are in VCTRL; the quantity the OTAs see is `vsa − vsb` (follower copy minus low-passed copy), which is the
  step times the follower gain for as long as the low-pass has not caught up. The follower gain was not measured.

## Result: minimum of `STILL` after each step (V; rail 1.20 / 1.08 / 1.32 V)

| step | tt | ss | ff |
|---|---|---|---|
| quiet, at 95 ns | 1.2 | 1.08 | 1.32 |
| +3 mV | 1.2 | 1.0799 | 1.32 |
| −3 mV | 1.2 | 1.0799 | 1.32 |
| −3 mV | 1.2 | 1.0799 | 1.32 |
| +3 mV | 1.2 | 1.0799 | 1.32 |
| **+5 mV** | **−0.0002** | **−0.0001** | **0.0014** |
| **−5 mV** | **−0.0001** | **−0.0001** | **0.0042** |
| **−5 mV** | **−0.0001** | **−0.0001** | **0.0085** |
| **+5 mV** | **−0.0002** | **−0.0001** | **0.0107** |
| +8 mV | −0.0002 | −0.0002 | −0.0001 |
| −8 mV | −0.0001 | −0.0001 | −0.0001 |
| −8 mV | −0.0001 | −0.0001 | −0.0001 |
| +8 mV | −0.0002 | −0.0002 | −0.0001 |

- At every corner `STILL` is untouched by ±3 mV steps (to within 0.1 mV at ss) and falls to under 1 % of the rail for ±5 mV steps;
  the threshold, in VCTRL, is therefore between 3 and 5 mV at each corner (not located more finely). At ff the ±5 mV
  minimum is 1.4–10.7 mV, higher than at tt/ss: ff's threshold sits closest to 5 mV, so it is the corner with the least
  margin on the 5 mV side.
- `still_end_s01..s12` (the value 95 ns after each step) is the rail at all three corners and all twelve steps: the sensor recovers
  after every trip inside the 100 ns spacing, so no step's reading is contaminated by the previous one.
- Comparison with the previous topology: its tt step test (quoted in the pre-change `design/tools/cells.py`) held
  +4 mV / −5 mV and dropped at +5 mV / −8 mV, with one corner measured. This sensor measures the same bracket at three corners and
  its tt threshold is nearer 3–5 mV on both signs.

## What this does not show

The threshold located finer than the 3 / 5 mV bracket; ripple response beyond the 50 MHz of the smoke stimulus
(that is `../20261124T023824Z-probe/`); mismatch or Monte Carlo (the previous record's "random mismatch is wider than
that window" caution applies to this sensor until #41 grades it); any corner other than the three.
