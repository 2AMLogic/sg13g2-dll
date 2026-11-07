# delay-sizing record (probe)

SIMULATED results, never measured. Reduced corner set (`sim/corners.json` reduced_set), NOT the 45-corner grade. Delay = single-event T0->Tk first edge at 50 % of Vdd (rising input = `dr`, falling input = `df`), ideal control sources (VBN=Vc, VBP=Vdd-Vc), 20 fF ideal load on every tap buffer, the delay-sanity method. Current = mean supply current over 6..10 ns (integer clock periods, line toggling). Tool versions: klt klt 0.9.2.dev247+g6c8de4e4f36a ; B scale 4 ; mode probe

## a_ss_1GHz (variant a; T/8 = 125 ps; status pass, 3/3 pass; backend batch; job klt-sim-bd7e5ba6587e)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.80 | 959.9 / 952.8 | 119.5 | 111.3..144.2 | 116.7..144.2 | 111.3..142.1 | 392 |
| 1.00 | 717.4 / 716.9 | 89.6 | 80.4..107.8 | 93.7..107.8 | 80.4..94.8 | 394 |
| 1.08 | 678.8 / 678.6 | 84.8 | 75.7..101.8 | 89.4..101.8 | 75.7..88.3 | 395 |

Usable Vc window (>=100 mV from both rails, edge present): 0.80..0.80 V; dead zone: none in the swept range. Mean step 119.5..119.5 ps; individual step min/max over the window 111.3..144.2 ps; T/8 **NOT covered**. Fastest mean step (any Vc) 84.8 ps.

## b1.5_ss_1GHz (variant b1.5; T/8 = 125 ps; status pass, 3/3 pass; backend batch; job klt-sim-fd71ae6e8976)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.80 | 1344.6 / 1341.3 | 167.9 | 164.9..187.0 | 165.2..187.0 | 164.9..185.5 | 439 |
| 1.00 | 1103.7 / 1099.3 | 137.7 | 135.8..149.4 | 136.3..149.4 | 135.8..148.4 | 441 |
| 1.08 | 1062.6 / 1058.5 | 132.6 | 130.8..143.3 | 131.3..143.3 | 130.8..142.4 | 441 |

Usable Vc window (>=100 mV from both rails, edge present): 0.80..0.80 V; dead zone: none in the swept range. Mean step 167.9..167.9 ps; individual step min/max over the window 164.9..187.0 ps; T/8 **NOT covered**. Fastest mean step (any Vc) 132.6 ps.

## b2_ss_1GHz (variant b2; T/8 = 125 ps; status pass, 3/3 pass; backend batch; job klt-sim-8ce37b12178e)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.80 | 1188.7 / 1184.9 | 148.4 | 146.0..162.8 | 146.5..162.8 | 146.0..161.8 | 440 |
| 1.00 | 1021.4 / 1018.3 | 127.5 | 125.9..137.3 | 126.3..137.3 | 125.9..136.6 | 441 |
| 1.08 | 991.8 / 989.1 | 123.8 | 122.4..132.9 | 122.7..132.9 | 122.4..132.3 | 441 |

Usable Vc window (>=100 mV from both rails, edge present): 0.80..0.80 V; dead zone: none in the swept range. Mean step 148.4..148.4 ps; individual step min/max over the window 146.0..162.8 ps; T/8 **NOT covered**. Fastest mean step (any Vc) 123.8 ps.

## b3_ss_1GHz (variant b3; T/8 = 125 ps; status pass, 3/3 pass; backend batch; job klt-sim-24f4013db03a)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.80 | 1042.4 / 1039.8 | 130.1 | 128.5..140.7 | 128.8..140.7 | 128.5..140.1 | 441 |
| 1.00 | 940.4 / 939.2 | 117.5 | 116.3..125.5 | 116.4..125.5 | 116.3..125.2 | 441 |
| 1.08 | 921.6 / 920.8 | 115.1 | 114.0..122.8 | 114.1..122.8 | 114.0..122.5 | 441 |

Usable Vc window (>=100 mV from both rails, edge present): 0.80..0.80 V; dead zone: none in the swept range. Mean step 130.1..130.1 ps; individual step min/max over the window 128.5..140.7 ps; T/8 **NOT covered**. Fastest mean step (any Vc) 115.1 ps.

## b4_ss_1GHz (variant b4; T/8 = 125 ps; status pass, 3/3 pass; backend batch; job klt-sim-df5c7331de46)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.80 | 973.1 / 971.7 | 121.5 | 120.2..130.4 | 120.4..130.4 | 120.2..130.1 | 441 |
| 1.00 | 900.4 / 900.5 | 112.6 | 111.5..119.7 | 111.5..119.7 | 111.5..119.6 | 441 |
| 1.08 | 886.7 / 887.1 | 110.9 | 109.8..117.7 | 109.8..117.7 | 109.9..117.7 | 441 |

Usable Vc window (>=100 mV from both rails, edge present): 0.80..0.80 V; dead zone: none in the swept range. Mean step 121.5..121.5 ps; individual step min/max over the window 120.2..130.4 ps; T/8 **NOT covered**. Fastest mean step (any Vc) 110.9 ps.

## base_ss_1GHz (variant base; T/8 = 125 ps; status pass, 3/3 pass; backend batch; job klt-sim-2aee08024cd1)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.80 | 1678.6 / 1680.3 | 209.9 | 205.0..239.8 | 205.0..239.8 | 205.6..237.7 | 438 |
| 1.00 | 1272.1 / 1266.4 | 158.7 | 156.0..174.6 | 156.6..174.6 | 156.0..173.0 | 440 |
| 1.08 | 1205.9 / 1199.9 | 150.4 | 148.0..164.5 | 148.7..164.5 | 148.0..163.0 | 440 |

Usable Vc window (>=100 mV from both rails, edge present): 0.80..0.80 V; dead zone: none in the swept range. Mean step 209.9..209.9 ps; individual step min/max over the window 205.0..239.8 ps; T/8 **NOT covered**. Fastest mean step (any Vc) 150.4 ps.

## Target check (mean tap step span contains T/8, usable window)

- a_ss_1GHz: NOT covered; fastest mean step 84.8 ps; dead zone top None
- b1.5_ss_1GHz: NOT covered; fastest mean step 132.6 ps; dead zone top None
- b2_ss_1GHz: NOT covered; fastest mean step 123.8 ps; dead zone top None
- b3_ss_1GHz: NOT covered; fastest mean step 115.1 ps; dead zone top None
- b4_ss_1GHz: NOT covered; fastest mean step 110.9 ps; dead zone top None
- base_ss_1GHz: NOT covered; fastest mean step 150.4 ps; dead zone top None

## Run status

no diagnostics / errors
