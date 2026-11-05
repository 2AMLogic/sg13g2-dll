# Grading of `record.md` against decision 0004 (issue #23)

SIMULATED, never measured. Reduced corner set: tt/1.2 V/27 C, ss/1.08 V/125 C,
ff/1.32 V/-40 C. Added after the run; `record.md` and the envelopes are the
untouched run output. Batch jobs: 500 MHz ss/tt/ff `klt-sim-bcbf3bafc512` /
`klt-sim-7d87bf65a822` / `klt-sim-bd91eb96e666`; 1 GHz ss/tt/ff
`klt-sim-809a08e3fb4f` / `klt-sim-9450a6d3d8bb` / `klt-sim-f84a6010930b`.

The fleet accepted all six requests (runner klt 0.9.x; the exit-87 blocker is
cleared). Every envelope reports status `error` only because the low-Vc points
produce no output edge (measurement "produced no value"), see condition 4.

| # | Condition | 500 MHz | 1 GHz |
|---|---|---|---|
| 1 | Mean tap step spans T/8 (250 / 125 ps) | pass, all three corners | **FAIL at ss** (best 150.7 ps at Vc = 1.08 V); pass at tt (101.9 ps) and ff (71.4 ps) |
| 2 | ss/1.08 V/125 C reaches the 104 ps tap at 1 GHz | n/a | **FAIL**: fastest ss tap step is 150.7 ps |
| 3 | ff/1.32 V/-40 C stays within the range (does not run out of delay at the slow end, and its fast end is not above the low end of the span) | pass (d8 0.571..2.834 ns vs 1.667..2.500) | pass (d8 0.571..3.688 ns vs 0.833..1.250) |
| 4 | Both rail ends of Vc exercised | exercised; Vc <= 0.5 V gives no edge at every corner (line stalls) | exercised; Vc <= 0.5 V (ss: <= 0.6 V) gives no edge |

Notes: the usable control window is narrow and steep (ss 500 MHz: 4.28 ns at
0.6 V to 1.21 ns at 1.08 V), and the "no edge" region begins at 0.5-0.6 V, so
the loop's control range would sit just above a dead zone. The tt/ff 0.6 V rows
at 1 GHz have tap spacing up to 1.4 ns, i.e. they are near stall and not a
usable operating point. Delays are single-event, ideal bias sources, ideal
20 fF loads; no jitter figure is claimed.

Conclusion: the two-stages-per-tap choice is **falsified at 1 GHz / ss**.
See `spec/decisions/0010-delay-tap-one-stage-fallback.md`.
