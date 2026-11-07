# delay-sizing record

SIMULATED results, never measured. Reduced corner set (`sim/corners.json` reduced_set), NOT the 45-corner grade. Delay = single-event T0->Tk first edge at 50 % of Vdd (rising input = `dr`, falling input = `df`), ideal control sources (VBN=Vc, VBP=Vdd-Vc), 20 fF ideal load on every tap buffer, the delay-sanity method. Current = mean supply current over 6..10 ns (integer clock periods, line toggling). Tool versions: klt klt 0.9.2.dev247+g6c8de4e4f36a ; B scale 4 ; mode fine

## a_1GHz_ff (variant a; T/8 = 125 ps; status error, 3/9 pass; backend batch; job klt-sim-7863060f53da)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.40 | no edge / no value | - | - | - | - | 49 |
| 0.44 | no edge / no value | - | - | - | - | 52 |
| 0.48 | no edge / no value | - | - | - | - | 53 |
| 0.52 | no edge / no value | - | - | - | - | 59 |
| 0.56 | no edge / no value | - | - | - | - | 136 |
| 0.60 | no edge / no value | - | - | - | - | 412 |
| 0.64 | 1226.2 / 1194.1 | 151.3 | 85.0..244.6 | 85.0..162.2 | 179.8..244.6 | 503 |
| 0.68 | 936.3 / 948.6 | 117.8 | 78.8..181.4 | 78.8..126.3 | 140.8..181.4 | 501 |
| 0.72 | 749.1 / 758.2 | 94.2 | 67.9..139.1 | 67.9..101.3 | 109.3..139.1 | 499 |

Usable Vc window (>=100 mV from both rails, edge present): 0.64..0.72 V; dead zone: no edge at Vc <= 0.60 V. Mean step 94.2..151.3 ps; individual step min/max over the window 67.9..244.6 ps; T/8 **covered**. Fastest mean step (any Vc) 94.2 ps.

## a_500MHz_ff (variant a; T/8 = 250 ps; status error, 5/9 pass; backend batch; job klt-sim-6af6cf9f0cfa)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.40 | no edge / no value | - | - | - | - | 26 |
| 0.44 | no edge / no value | - | - | - | - | 27 |
| 0.48 | no edge / no value | - | - | - | - | 35 |
| 0.52 | no edge / no value | - | - | - | - | 91 |
| 0.56 | 2504.9 / 2286.6 | 299.5 | 115.1..496.9 | 115.1..298.2 | 364.6..496.9 | 263 |
| 0.60 | 1687.8 / 1730.2 | 213.6 | 127.2..341.4 | 127.2..218.6 | 272.2..341.4 | 257 |
| 0.64 | 1223.3 / 1251.0 | 154.6 | 96.9..244.6 | 96.9..163.7 | 192.1..244.6 | 253 |
| 0.68 | 936.4 / 952.8 | 118.1 | 79.3..181.4 | 79.3..126.6 | 141.8..181.4 | 251 |
| 0.72 | 749.1 / 758.6 | 94.2 | 67.9..139.1 | 67.9..101.3 | 109.3..139.1 | 250 |

Usable Vc window (>=100 mV from both rails, edge present): 0.56..0.72 V; dead zone: no edge at Vc <= 0.52 V. Mean step 94.2..299.5 ps; individual step min/max over the window 67.9..496.9 ps; T/8 **covered**. Fastest mean step (any Vc) 94.2 ps.

## b_1GHz_ff (variant b; T/8 = 125 ps; status error, 6/9 pass; backend batch; job klt-sim-949198af1544)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.40 | no edge / no value | - | - | - | - | 77 |
| 0.44 | no edge / no value | - | - | - | - | 176 |
| 0.48 | no edge / no value | - | - | - | - | 243 |
| 0.52 | 1402.7 / 1463.9 | 179.2 | 170.8..229.7 | 170.8..205.6 | 175.3..229.7 | 563 |
| 0.56 | 981.6 / 1019.5 | 125.1 | 119.2..156.2 | 119.2..144.4 | 122.5..156.2 | 558 |
| 0.60 | 750.3 / 771.6 | 95.1 | 91.4..113.1 | 91.4..108.4 | 93.6..113.1 | 557 |
| 0.64 | 615.6 / 625.4 | 77.6 | 75.3..88.4 | 75.3..86.8 | 76.5..88.4 | 557 |
| 0.68 | 535.8 / 539.0 | 67.2 | 65.9..74.4 | 65.9..73.8 | 66.2..74.4 | 557 |
| 0.72 | 487.7 / 488.2 | 61.0 | 60.1..66.5 | 60.1..66.0 | 60.1..66.5 | 558 |

Usable Vc window (>=100 mV from both rails, edge present): 0.52..0.72 V; dead zone: no edge at Vc <= 0.48 V. Mean step 61.0..179.2 ps; individual step min/max over the window 60.1..229.7 ps; T/8 **covered**. Fastest mean step (any Vc) 61.0 ps.

## b_500MHz_ff (variant b; T/8 = 250 ps; status error, 7/9 pass; backend batch; job klt-sim-dc6ee1d7b148)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.40 | no edge / no value | - | - | - | - | 63 |
| 0.44 | no edge / no value | - | - | - | - | 154 |
| 0.48 | 2266.2 / 2376.7 | 290.2 | 278.3..363.7 | 278.3..317.4 | 286.8..363.7 | 289 |
| 0.52 | 1402.7 / 1465.4 | 179.3 | 170.8..229.9 | 170.8..205.6 | 175.4..229.9 | 282 |
| 0.56 | 981.6 / 1019.5 | 125.1 | 119.2..156.2 | 119.2..144.4 | 122.5..156.2 | 279 |
| 0.60 | 750.3 / 771.6 | 95.1 | 91.4..113.1 | 91.4..108.4 | 93.6..113.1 | 278 |
| 0.64 | 615.7 / 625.4 | 77.6 | 75.3..88.4 | 75.3..86.8 | 76.5..88.4 | 278 |
| 0.68 | 535.8 / 539.0 | 67.2 | 65.9..74.4 | 65.9..73.8 | 66.2..74.4 | 279 |
| 0.72 | 487.7 / 488.3 | 61.0 | 60.2..66.5 | 60.2..66.0 | 60.2..66.5 | 279 |

Usable Vc window (>=100 mV from both rails, edge present): 0.48..0.72 V; dead zone: no edge at Vc <= 0.44 V. Mean step 61.0..290.2 ps; individual step min/max over the window 60.2..363.7 ps; T/8 **covered**. Fastest mean step (any Vc) 61.0 ps.

## Target check (mean tap step span contains T/8, usable window)

- a_1GHz_ff: covered; fastest mean step 94.2 ps; dead zone top 0.6
- a_500MHz_ff: covered; fastest mean step 94.2 ps; dead zone top 0.52
- b_1GHz_ff: covered; fastest mean step 61.0 ps; dead zone top 0.48
- b_500MHz_ff: covered; fastest mean step 61.0 ps; dead zone top 0.44

## Run status

ERRORS:
- a_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df3' produced no value
- a_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr4' produced no value
- a_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df4' produced no value
- a_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr5' produced no value
- a_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df5' produced no value
- a_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr6' produced no value
- a_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df6' produced no value
- a_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr7' produced no value
- a_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df7' produced no value
- a_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr8' produced no value
- a_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df8' produced no value
- a_1GHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'df3' produced no value
- a_1GHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'dr4' produced no value
- a_1GHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'df4' produced no value
- a_1GHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'dr5' produced no value
- a_1GHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'df5' produced no value
- a_1GHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'dr6' produced no value
- a_1GHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'df6' produced no value
- a_1GHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'dr7' produced no value
- a_1GHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'df7' produced no value
- a_1GHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'dr8' produced no value
- a_1GHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'df8' produced no value
- a_1GHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'df3' produced no value
- a_1GHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'dr4' produced no value
- a_1GHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'df4' produced no value
- a_1GHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'dr5' produced no value
- a_1GHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'df5' produced no value
- a_1GHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'dr6' produced no value
- a_1GHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'df6' produced no value
- a_1GHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'dr7' produced no value
- a_1GHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'df7' produced no value
- a_1GHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'dr8' produced no value
- a_1GHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'df8' produced no value
- a_1GHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'df3' produced no value
- a_1GHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'dr4' produced no value
- a_1GHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'df4' produced no value
- a_1GHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'dr5' produced no value
- a_1GHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'df5' produced no value
- a_1GHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'dr6' produced no value
- a_1GHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'df6' produced no value
- a_1GHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'dr7' produced no value
- a_1GHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'df7' produced no value
- a_1GHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'dr8' produced no value
- a_1GHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'df8' produced no value
- a_1GHz_ff mos_ff/VC=0.560_Vdd=1.320V/-40C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.560_Vdd=1.320V/-40C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.560_Vdd=1.320V/-40C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.560_Vdd=1.320V/-40C: [measurement] measurement 'df3' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.560_Vdd=1.320V/-40C: [measurement] measurement 'dr4' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.560_Vdd=1.320V/-40C: [measurement] measurement 'df4' produced no value
- a_1GHz_ff mos_ff/VC=0.560_Vdd=1.320V/-40C: [measurement] measurement 'dr5' produced no value
- a_1GHz_ff mos_ff/VC=0.560_Vdd=1.320V/-40C: [measurement] measurement 'df5' produced no value
- a_1GHz_ff mos_ff/VC=0.560_Vdd=1.320V/-40C: [measurement] measurement 'dr6' produced no value
- a_1GHz_ff mos_ff/VC=0.560_Vdd=1.320V/-40C: [measurement] measurement 'df6' produced no value
- a_1GHz_ff mos_ff/VC=0.560_Vdd=1.320V/-40C: [measurement] measurement 'dr7' produced no value
- a_1GHz_ff mos_ff/VC=0.560_Vdd=1.320V/-40C: [measurement] measurement 'df7' produced no value
- a_1GHz_ff mos_ff/VC=0.560_Vdd=1.320V/-40C: [measurement] measurement 'dr8' produced no value
- a_1GHz_ff mos_ff/VC=0.560_Vdd=1.320V/-40C: [measurement] measurement 'df8' produced no value
- a_1GHz_ff mos_ff/VC=0.600_Vdd=1.320V/-40C: [measurement] measurement 'dr7' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.600_Vdd=1.320V/-40C: [measurement] measurement 'df7' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.600_Vdd=1.320V/-40C: [measurement] measurement 'dr8' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.600_Vdd=1.320V/-40C: [measurement] measurement 'df8' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df3' produced no value
- a_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr4' produced no value
- a_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df4' produced no value
- a_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr5' produced no value
- a_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df5' produced no value
- a_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr6' produced no value
- a_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df6' produced no value
- a_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr7' produced no value
- a_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df7' produced no value
- a_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr8' produced no value
- a_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df8' produced no value
- a_500MHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'df3' produced no value
- a_500MHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'dr4' produced no value
- a_500MHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'df4' produced no value
- a_500MHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'dr5' produced no value
- a_500MHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'df5' produced no value
- a_500MHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'dr6' produced no value
- a_500MHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'df6' produced no value
- a_500MHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'dr7' produced no value
- a_500MHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'df7' produced no value
- a_500MHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'dr8' produced no value
- a_500MHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'df8' produced no value
- a_500MHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'df3' produced no value
- a_500MHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'dr4' produced no value
- a_500MHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'df4' produced no value
- a_500MHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'dr5' produced no value
- a_500MHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'df5' produced no value
- a_500MHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'dr6' produced no value
- a_500MHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'df6' produced no value
- a_500MHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'dr7' produced no value
- a_500MHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'df7' produced no value
- a_500MHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'dr8' produced no value
- a_500MHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'df8' produced no value
- a_500MHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'df3' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'dr4' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'df4' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'dr5' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'df5' produced no value
- a_500MHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'dr6' produced no value
- a_500MHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'df6' produced no value
- a_500MHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'dr7' produced no value
- a_500MHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'df7' produced no value
- a_500MHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'dr8' produced no value
- a_500MHz_ff mos_ff/VC=0.520_Vdd=1.320V/-40C: [measurement] measurement 'df8' produced no value
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df3' produced no value -- ngspice reported: out of interval
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr4' produced no value -- ngspice reported: out of interval
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df4' produced no value -- ngspice reported: out of interval
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr5' produced no value
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df5' produced no value
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr6' produced no value
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df6' produced no value
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr7' produced no value
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df7' produced no value
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr8' produced no value
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df8' produced no value
- b_1GHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'df3' produced no value -- ngspice reported: out of interval
- b_1GHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'df4' produced no value -- ngspice reported: out of interval
- b_1GHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'df5' produced no value -- ngspice reported: out of interval
- b_1GHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'df6' produced no value -- ngspice reported: out of interval
- b_1GHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'df7' produced no value -- ngspice reported: out of interval
- b_1GHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'df8' produced no value
- b_1GHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'df6' produced no value -- ngspice reported: out of interval
- b_1GHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'df7' produced no value -- ngspice reported: out of interval
- b_1GHz_ff mos_ff/VC=0.480_Vdd=1.320V/-40C: [measurement] measurement 'df8' produced no value -- ngspice reported: out of interval
- b_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- b_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- b_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- b_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df3' produced no value -- ngspice reported: out of interval
- b_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr4' produced no value -- ngspice reported: out of interval
- b_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df4' produced no value
- b_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr5' produced no value
- b_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df5' produced no value
- b_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr6' produced no value
- b_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df6' produced no value
- b_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr7' produced no value
- b_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df7' produced no value
- b_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr8' produced no value
- b_500MHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df8' produced no value
- b_500MHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'df5' produced no value -- ngspice reported: out of interval
- b_500MHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'df6' produced no value -- ngspice reported: out of interval
- b_500MHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'df7' produced no value -- ngspice reported: out of interval
- b_500MHz_ff mos_ff/VC=0.440_Vdd=1.320V/-40C: [measurement] measurement 'df8' produced no value -- ngspice reported: out of interval
