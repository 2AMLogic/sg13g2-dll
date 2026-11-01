# Target specification

Status: **proposed — ratification candidate**. Becomes ratified only when the
operator approves and merges the ratification PR carrying
[0009](decisions/0009-ratification-of-target-spec.md) (the standard two-key
path; builds on [0001](decisions/0001-spec-ratification.md)). Target / fallback / stretch
values are carried over unchanged from the README table. `min/typ/max` is the
pass window for the **target** column; fallback and stretch re-grade the same
condition at their own value.

All rows are graded over the full corner set in `sim/corners.json` (45 corners:
5 MOS × 3 supply × 3 temperature) unless the row says otherwise. Every
simulated number is "simulated", never "measured".

## Conventions

- **T** = input clock period. **f0** = 1 GHz (target), 500 MHz (fallback), 2 GHz (stretch).
- **Input**: ideal source, 50 % duty, 100 ps rise/fall held fixed at every frequency, 0 jitter unless the jitter row says otherwise.
- **Locked** is defined once, below, and used by every row that says "locked".
- **Load**: every tap output (and the lock-status output) drives a fixed **20 fF to VSS** in every graded run ([0007](decisions/0007-rail-1p2v-thin-oxide.md) decision 7: one lv mux-input gate plus local wiring, 2–4× the smoke decks' loads). The tap buffer that drives it is part of the block. A result at another load is not a spec result; a consumer's stated load replaces 20 fF only through a new record.

## Locked (predicate)

The loop is **locked** at time t if, measured on the input edge and the
delay-line output tap *N* (the last tap, nominal delay one period), the signed
edge-to-edge time error satisfies

|t_edge(tap N) − (t_edge(in) + T)| ≤ p of T

where the tolerance p is set **per column**: 2 % in the target column, 5 % in
the fallback column, 1 % in the stretch column. Each column's p equals that
column's row 5 limit (0007 call E; the same three tolerances `dllbench.py
--tol` grades). Consequently row 5 is implied by lock at every column: a
design whose static phase error exceeds the column's row 5 limit is not locked
and fails the rows that say "locked", rather than failing row 5 alone. Row 5
is kept as the named statement of that limit, not as an independent check.

on **each of the 64 consecutive input cycles ending at t**, and the
delay-line control voltage moves by less than 5 mV peak-to-peak over those 64
cycles. Edges are the rising edges at VDD/2 crossings (0.60 V at the nominal
1.2 V rail; VDD/2 of the corner's own supply elsewhere). A graded run lasts
**2 × the column's lock-time limit**: 2 µs in the target and stretch columns,
10 µs in the fallback column. Lock time is the first time at which the
predicate holds and continues to hold to the end of the run; "not locked by
the end of the run" in row 8 uses the same length.

## Rows

| # | Parameter | Target | Fallback | Stretch | min / typ / max (target) | Grading condition | Corners |
|---|---|---|---|---|---|---|---|
| 1 | Input clock | 1 GHz | 500 MHz | 2 GHz | — / 1 GHz / — | Operating point; each row below is graded at this frequency | all 45 |
| 2 | Lock range | ±20 % around target | ±20 % around 500 MHz (0002 G1, accepted in 0007; was ±10 %) | ±40 % | locks at 0.8 f0 and 1.2 f0 and at 0.9, 1.0, 1.1 f0; the five points, at whichever f0 the column names | Locked predicate holds at each of the five frequencies, from the start states in the false-lock row | all 45 |
| 3 | Output phases | 8, even over T | 4 | 16 | 8 taps at k·T/8, k=0…7 | Count of taps; spacing graded in row 4 | n/a (structural) |
| 4 | Systematic phase-spacing error (excludes random mismatch) | ≤ 2 % T | ≤ 5 % | ≤ 1 % | every adjacent-tap spacing within T/8 ± 0.02 T | Locked, rising edges at VDD/2 into the 20 fF tap load, 64-cycle average per tap; post-layout extracted result is the graded one, schematic result is recorded separately | all 45 post-layout. Monte Carlo is a separate recorded result with **no limit**: this row bounds the systematic (corner, end-cell, load) spacing only, and a consumer must budget random mismatch separately |
| 5 | Static phase error | ≤ 2 % T | ≤ 5 % | ≤ 1 % | abs(t_tapN − t_in − T) ≤ 0.02 T | Locked, 64-cycle average, ideal input | all 45 |
| 6 | Added jitter (rms, simulated) | ≤ 2 ps | ≤ 5 ps | ≤ 1 ps | — / — / 2 ps | See "Jitter method" below | tt/1.20 V/27 °C and ss/1.08 V/125 °C and ff/1.32 V/−40 °C (3 corners; ngspice transient noise is expensive); stated next to every number |
| 7 | Lock time | ≤ 1 µs from enable | ≤ 5 µs | — | — / — / 1 µs | Time from the later of enable assertion and the first input rising edge (start state 5d starts the clock after enable) to the first Locked-predicate success that persists to the end of the column's run (2 µs target, 10 µs fallback; see "Locked"), from the worst start state of row 8 | all 45 |
| 8 | False lock | none | — | — | pass = settles to **exactly one** period of delay | See "False-lock criterion" below | all 45 |
| 9 | Supply / device flavor | 1.2 V thin-oxide (`sg13_lv_*`), no HBT ([0007](decisions/0007-rail-1p2v-thin-oxide.md), operator ruling 2026-10-20) | — | — | 1.08 / 1.20 / 1.32 V | Rail tolerance ±10 %; inside the PDK's "VGS ≤ 1.65 V @ 125 °C" rating and the lv model's 1.5 V maximum | all 45 |
| 10 | Power | ≤ 5 mW | ≤ 10 mW | ≤ 2 mW | — / — / 5 mW | Average VDD supply power over the 64 locked cycles, including bias and the tap buffers driving 20 fF each, at the target frequency; graded at every corner and the limit applies to the worst of the 45 (expected at 1.32 V / 125 °C / mos_ff, confirmed by the result, not assumed); also recorded at tt / 1.20 V / 27 °C. Limit kept across the rail change (0007); it is loose at 1.2 V and is revisited with the first result | all 45; limit applies at the worst |
| 11 | Signoff | DRC + LVS clean, post-layout re-verified | — | — | — | `klt drc`, `klt lvs`, `klt pex` re-sim of rows 4, 5, 8 | n/a |
| 12 | Lock-status output (0002 G5, accepted in 0007) | asserted only when locked | — | — | LOCK may lag the Locked predicate by up to 128 input cycles in both directions: LOCK = 1 ⇒ the predicate held at some time within the preceding 128 input cycles; LOCK rises within 128 cycles after the predicate first holds; LOCK falls within 128 cycles after it stops holding. The detector therefore senses the delay error and the 5 mV control-voltage criterion of the predicate, not the PFD output alone | Graded in every row-8 run: LOCK is never 1 in a run that fails row 8 (delay ≠ 1 T or rail park), and is 1 by lock time + 128 cycles in a run that passes; a digital output at the rail, driving the same 20 fF load as a tap | all 45, all five frequencies, all start states |

Note on row 4: at 1 GHz, 2 % of T is 20 ps; the pass window per adjacent-tap
spacing is 125 ps ± 20 ps.

Row 3: the 8 phases are the eight taps; the ninth point (T) is the lock
reference tap N, not an output. The `sg13g2-aib` consumer asks for 16 at its
own target (0002 G2); that is met only by this spec's stretch column and is
declined at target (0007 decision 4).

## False-lock criterion (row 8)

A run **passes** if, after enable, the loop settles to a state in which the
delay-line total delay equals **exactly 1 × T** (Locked predicate, with
tap N delay = T), and does not settle to any other delay. A run **fails** if
the loop satisfies the Locked predicate at delay ≈ 2T (or any other multiple),
parks the control voltage within 50 mV of either rail, or has not met the
Locked predicate by the end of the run (2 µs; 10 µs in the fallback column). "Looks locked" (zero PFD output) is not a pass; the
delay is measured as the number of input periods between an input edge and
the tap N edge it is compared with.

Start states (all crossed with the full corner set and each of the five
frequencies of row 2):

1. Control voltage preset at the minimum-delay rail.
2. Control voltage preset at the maximum-delay rail.
3. Control voltage preset at mid-range.
4. Control voltage preset at the two points where nominal delay is 0.5 T and 1.5 T (the harmonic-lock decision boundaries) of that frequency.
5. Loop enable/reset state: enabled from power-up with no preset; enable asserted while the input clock is already running; enable re-asserted after a disable with the control voltage left at its previous value; input clock absent at enable and started later.

The mechanism the circuit uses to pass is in
[0005](decisions/0005-false-lock-exclusion.md).

## Jitter method (row 6)

ngspice has no periodic-noise analysis, so the figure is **simulated, from
transient noise**, and is stated with its method every time:

- Method: ngspice transient noise, locked loop. ngspice's transient-noise facility (`trnoise` / `trrandom`) is a property of independent sources, not of device models, so device noise enters as source equivalents derived from a `.noise` analysis at the locked operating point; which devices, what bandwidth and where the equivalents sit is fixed in a decision record, validated on a known case, **before the first jitter result is recorded**. Whether the PSP103 OSDI models contribute noise in a transient run is not established. (#3 pinned the PDK and OSDI models, not a noise method.)
- Run length: ≥ 2000 input cycles after the Locked predicate first holds (discard those before).
- Seeds: ≥ 8 independent seeds per corner; seed values recorded.
- Estimator: rms of the time-interval error of tap k's rising edge versus the ideal grid t_in + (k/8)·T over all cycles, **minus** the same estimator applied to the input clock (added jitter), RMS-combined over the 8 seeds; computed for every tap k = 1…8, **graded on the worst tap**, all eight reported with the minimum and maximum seed result.
- Limits: transient noise in ngspice underestimates 1/f and does not capture supply noise unless injected; the figure is "simulated added jitter, thermal-noise class" and the proxy for supply-induced jitter is a recorded supply-step sensitivity (ps per mV of VDD). Neither is "measured".

## Not-a-row items

Input clock jitter, duty-cycle tolerance and supply noise are not rows: the
clock is an ideal source at the boundary (README scope).
