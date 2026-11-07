# delay-sizing record

SIMULATED results, never measured. Reduced corner set (`sim/corners.json` reduced_set), NOT the 45-corner grade. Delay = single-event T0->Tk first edge at 50 % of Vdd (rising input = `dr`, falling input = `df`), ideal control sources (VBN=Vc, VBP=Vdd-Vc), 20 fF ideal load on every tap buffer, the delay-sanity method. Current = mean supply current over 6..10 ns (integer clock periods, line toggling). Tool versions: klt klt 0.9.2.dev247+g6c8de4e4f36a ; B scale 4 ; mode full

## a_1GHz_ff (variant a; T/8 = 125 ps; status error, 5/9 pass; backend batch; job klt-sim-ea6596953fef)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.30 | no edge / no value | - | - | - | - | 48 |
| 0.40 | no edge / no value | - | - | - | - | 49 |
| 0.50 | no edge / no value | - | - | - | - | 55 |
| 0.60 | no edge / no value | - | - | - | - | 412 |
| 0.70 | 833.3 / 844.6 | 104.9 | 72.9..158.2 | 72.9..112.7 | 123.7..158.2 | 500 |
| 0.80 | 533.8 / 536.9 | 66.9 | 53.8..90.7 | 53.8..71.7 | 73.4..90.7 | 498 |
| 0.90 | 409.1 / 410.6 | 51.2 | 44.3..63.8 | 44.3..54.5 | 54.1..63.8 | 499 |
| 1.00 | 350.8 / 352.2 | 43.9 | 39.1..52.1 | 39.1..46.2 | 45.9..52.1 | 499 |
| 1.08 | 324.4 / 325.8 | 40.6 | 36.5..47.3 | 36.5..42.5 | 42.3..47.3 | 499 |

Usable Vc window (>=100 mV from both rails, edge present): 0.70..1.08 V; dead zone: no edge at Vc <= 0.60 V. Mean step 40.6..104.9 ps; individual step min/max over the window 36.5..158.2 ps; T/8 **NOT covered**. Fastest mean step (any Vc) 40.6 ps.

## a_1GHz_ss (variant a; T/8 = 125 ps; status error, 5/9 pass; backend batch; job klt-sim-21fc137d3972)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.30 | no edge / no value | - | - | - | - | 38 |
| 0.40 | no edge / no value | - | - | - | - | 39 |
| 0.50 | no edge / no value | - | - | - | - | 41 |
| 0.60 | no edge / no value | - | - | - | - | 98 |
| 0.70 | 1359.2 / 1277.0 | 164.8 | 129.1..230.8 | 129.1..197.7 | 161.0..230.8 | 387 |
| 0.80 | 959.9 / 952.8 | 119.5 | 111.3..144.2 | 116.7..144.2 | 111.3..142.1 | 392 |
| 0.90 | 797.3 / 795.5 | 99.5 | 90.3..120.1 | 102.0..120.1 | 90.3..109.3 | 394 |
| 1.00 | 717.4 / 716.9 | 89.6 | 80.4..107.8 | 93.7..107.8 | 80.4..94.8 | 394 |
| 1.08 | 678.8 / 678.6 | 84.8 | 75.7..101.8 | 89.4..101.8 | 75.7..88.3 | 395 |

Usable Vc window (>=100 mV from both rails, edge present): 0.70..0.90 V; dead zone: no edge at Vc <= 0.60 V. Mean step 99.5..164.8 ps; individual step min/max over the window 90.3..230.8 ps; T/8 **covered**. Fastest mean step (any Vc) 84.8 ps.

## a_1GHz_tt (variant a; T/8 = 125 ps; status error, 5/9 pass; backend batch; job klt-sim-9c32c2bb55ee)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.30 | no edge / no value | - | - | - | - | 43 |
| 0.40 | no edge / no value | - | - | - | - | 43 |
| 0.50 | no edge / no value | - | - | - | - | 47 |
| 0.60 | no edge / no value | - | - | - | - | 147 |
| 0.70 | 1097.0 / 1091.8 | 136.8 | 103.7..201.2 | 103.7..154.3 | 150.7..201.2 | 441 |
| 0.80 | 714.3 / 713.3 | 89.2 | 78.4..116.0 | 78.4..100.4 | 91.4..116.0 | 443 |
| 0.90 | 562.6 / 562.0 | 70.3 | 65.3..84.2 | 65.3..78.4 | 69.9..84.2 | 444 |
| 1.00 | 492.2 / 492.1 | 61.5 | 58.3..70.8 | 58.3..67.8 | 60.8..70.8 | 444 |
| 1.08 | 459.8 / 459.9 | 57.5 | 54.8..65.1 | 54.8..62.8 | 56.9..65.1 | 445 |

Usable Vc window (>=100 mV from both rails, edge present): 0.70..1.08 V; dead zone: no edge at Vc <= 0.60 V. Mean step 57.5..136.8 ps; individual step min/max over the window 54.8..201.2 ps; T/8 **covered**. Fastest mean step (any Vc) 57.5 ps.

## a_500MHz_ff (variant a; T/8 = 250 ps; status error, 6/9 pass; backend batch; job klt-sim-41aa5431c24e)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.30 | no edge / no value | - | - | - | - | 24 |
| 0.40 | no edge / no value | - | - | - | - | 26 |
| 0.50 | no edge / no value | - | - | - | - | 59 |
| 0.60 | 1687.8 / 1730.2 | 213.6 | 127.2..341.4 | 127.2..218.6 | 272.2..341.4 | 257 |
| 0.70 | 833.3 / 845.8 | 104.9 | 73.1..158.2 | 73.1..112.8 | 123.8..158.2 | 250 |
| 0.80 | 533.8 / 537.0 | 66.9 | 53.8..90.7 | 53.8..71.7 | 73.4..90.7 | 249 |
| 0.90 | 409.1 / 410.6 | 51.2 | 44.3..63.8 | 44.3..54.5 | 54.1..63.8 | 249 |
| 1.00 | 350.8 / 352.2 | 43.9 | 39.1..52.1 | 39.1..46.2 | 45.9..52.1 | 250 |
| 1.08 | 324.4 / 325.8 | 40.6 | 36.5..47.3 | 36.5..42.5 | 42.3..47.3 | 250 |

Usable Vc window (>=100 mV from both rails, edge present): 0.60..1.08 V; dead zone: no edge at Vc <= 0.50 V. Mean step 40.6..213.6 ps; individual step min/max over the window 36.5..341.4 ps; T/8 **NOT covered**. Fastest mean step (any Vc) 40.6 ps.

## a_500MHz_ss (variant a; T/8 = 250 ps; status error, 6/9 pass; backend batch; job klt-sim-85ce0796839a)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.30 | no edge / no value | - | - | - | - | 19 |
| 0.40 | no edge / no value | - | - | - | - | 20 |
| 0.50 | no edge / no value | - | - | - | - | 23 |
| 0.60 | 2535.3 / 2441.4 | 311.0 | 191.4..499.2 | 191.4..368.4 | 346.2..499.2 | 195 |
| 0.70 | 1363.2 / 1365.9 | 170.6 | 148.8..230.8 | 148.8..203.5 | 173.1..230.8 | 196 |
| 0.80 | 959.8 / 959.3 | 119.9 | 112.0..144.9 | 117.4..144.9 | 112.0..142.1 | 197 |
| 0.90 | 797.3 / 797.7 | 99.7 | 90.3..120.3 | 102.2..120.3 | 90.3..109.3 | 197 |
| 1.00 | 717.4 / 718.1 | 89.7 | 80.4..108.0 | 93.8..108.0 | 80.4..94.8 | 197 |
| 1.08 | 678.8 / 679.5 | 84.9 | 75.7..101.9 | 89.5..101.9 | 75.7..88.3 | 197 |

Usable Vc window (>=100 mV from both rails, edge present): 0.60..0.90 V; dead zone: no edge at Vc <= 0.50 V. Mean step 99.7..311.0 ps; individual step min/max over the window 90.3..499.2 ps; T/8 **covered**. Fastest mean step (any Vc) 84.9 ps.

## a_500MHz_tt (variant a; T/8 = 250 ps; status error, 6/9 pass; backend batch; job klt-sim-5832ce1972f1)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.30 | no edge / no value | - | - | - | - | 21 |
| 0.40 | no edge / no value | - | - | - | - | 22 |
| 0.50 | no edge / no value | - | - | - | - | 28 |
| 0.60 | 2219.4 / 2211.8 | 276.9 | 169.8..451.9 | 169.8..309.4 | 329.9..451.9 | 222 |
| 0.70 | 1096.8 / 1104.1 | 137.6 | 105.7..201.2 | 105.7..155.3 | 152.4..201.2 | 221 |
| 0.80 | 714.3 / 713.6 | 89.2 | 78.4..116.0 | 78.4..100.5 | 91.4..116.0 | 222 |
| 0.90 | 562.6 / 562.0 | 70.3 | 65.3..84.2 | 65.3..78.4 | 69.9..84.2 | 222 |
| 1.00 | 492.2 / 492.1 | 61.5 | 58.3..70.8 | 58.3..67.8 | 60.8..70.8 | 222 |
| 1.08 | 459.9 / 459.9 | 57.5 | 54.8..65.1 | 54.8..62.8 | 56.9..65.1 | 222 |

Usable Vc window (>=100 mV from both rails, edge present): 0.60..1.08 V; dead zone: no edge at Vc <= 0.50 V. Mean step 57.5..276.9 ps; individual step min/max over the window 54.8..451.9 ps; T/8 **covered**. Fastest mean step (any Vc) 57.5 ps.

## b_1GHz_ff (variant b; T/8 = 125 ps; status error, 7/9 pass; backend batch; job klt-sim-2eb7c8e0f7ab)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.30 | no edge / no value | - | - | - | - | 48 |
| 0.40 | no edge / no value | - | - | - | - | 77 |
| 0.50 | 1750.0 / 1814.4 | 222.8 | 213.8..283.3 | 213.8..252.4 | 217.2..283.3 | 516 |
| 0.60 | 750.3 / 771.6 | 95.1 | 91.4..113.1 | 91.4..108.4 | 93.6..113.1 | 557 |
| 0.70 | 508.8 / 510.3 | 63.7 | 62.7..69.9 | 62.7..69.4 | 62.8..69.9 | 557 |
| 0.80 | 436.9 / 436.5 | 54.6 | 54.0..58.6 | 54.0..58.2 | 54.0..58.6 | 558 |
| 0.90 | 407.3 / 406.9 | 50.9 | 50.4..54.3 | 50.5..53.8 | 50.4..54.3 | 558 |
| 1.00 | 391.7 / 391.4 | 48.9 | 48.5..52.0 | 48.6..51.6 | 48.5..52.0 | 559 |
| 1.08 | 383.8 / 383.7 | 48.0 | 47.5..50.9 | 47.6..50.5 | 47.5..50.9 | 559 |

Usable Vc window (>=100 mV from both rails, edge present): 0.50..1.08 V; dead zone: no edge at Vc <= 0.40 V. Mean step 48.0..222.8 ps; individual step min/max over the window 47.5..283.3 ps; T/8 **covered**. Fastest mean step (any Vc) 48.0 ps.

## b_1GHz_ss (variant b; T/8 = 125 ps; status error, 6/9 pass; backend batch; job klt-sim-00610f4df74b)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.30 | no edge / no value | - | - | - | - | 38 |
| 0.40 | no edge / no value | - | - | - | - | 63 |
| 0.50 | no edge / no value | - | - | - | - | 191 |
| 0.60 | 1381.7 / 1382.0 | 172.7 | 169.0..196.9 | 169.0..196.9 | 169.4..194.3 | 438 |
| 0.70 | 1073.6 / 1070.8 | 134.0 | 132.2..145.8 | 132.5..145.8 | 132.2..145.0 | 440 |
| 0.80 | 973.1 / 971.7 | 121.5 | 120.2..130.4 | 120.4..130.4 | 120.2..130.1 | 441 |
| 0.90 | 926.6 / 926.0 | 115.8 | 114.7..123.5 | 114.7..123.5 | 114.7..123.3 | 441 |
| 1.00 | 900.4 / 900.5 | 112.6 | 111.5..119.7 | 111.5..119.7 | 111.5..119.6 | 441 |
| 1.08 | 886.7 / 887.1 | 110.9 | 109.8..117.7 | 109.8..117.7 | 109.9..117.7 | 441 |

Usable Vc window (>=100 mV from both rails, edge present): 0.60..0.90 V; dead zone: no edge at Vc <= 0.50 V. Mean step 115.8..172.7 ps; individual step min/max over the window 114.7..196.9 ps; T/8 **covered**. Fastest mean step (any Vc) 110.9 ps.

## b_1GHz_tt (variant b; T/8 = 125 ps; status error, 6/9 pass; backend batch; job klt-sim-abcdb8e7ddfd)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.30 | no edge / no value | - | - | - | - | 43 |
| 0.40 | no edge / no value | - | - | - | - | 58 |
| 0.50 | no edge / no value | - | - | - | - | 222 |
| 0.60 | 1048.2 / 1059.9 | 131.8 | 127.4..153.0 | 127.4..153.0 | 129.2..152.5 | 494 |
| 0.70 | 732.4 / 727.4 | 91.2 | 89.7..100.3 | 90.2..100.3 | 89.7..98.8 | 496 |
| 0.80 | 641.0 / 636.0 | 79.8 | 78.7..85.9 | 79.3..85.9 | 78.7..84.9 | 497 |
| 0.90 | 602.5 / 598.1 | 75.0 | 74.1..80.2 | 74.6..80.2 | 74.1..79.4 | 497 |
| 1.00 | 581.8 / 577.9 | 72.5 | 71.6..77.2 | 72.0..77.2 | 71.6..76.4 | 497 |
| 1.08 | 571.3 / 567.5 | 71.2 | 70.4..75.7 | 70.8..75.7 | 70.4..75.0 | 497 |

Usable Vc window (>=100 mV from both rails, edge present): 0.60..1.08 V; dead zone: no edge at Vc <= 0.50 V. Mean step 71.2..131.8 ps; individual step min/max over the window 70.4..153.0 ps; T/8 **covered**. Fastest mean step (any Vc) 71.2 ps.

## b_500MHz_ff (variant b; T/8 = 250 ps; status error, 7/9 pass; backend batch; job klt-sim-88688a9d3470)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.30 | no edge / no value | - | - | - | - | 24 |
| 0.40 | no edge / no value | - | - | - | - | 63 |
| 0.50 | 1750.2 / 1832.5 | 223.9 | 213.9..286.1 | 213.9..252.4 | 219.8..286.1 | 285 |
| 0.60 | 750.3 / 771.6 | 95.1 | 91.4..113.1 | 91.4..108.4 | 93.6..113.1 | 278 |
| 0.70 | 508.8 / 510.4 | 63.7 | 62.7..69.9 | 62.7..69.4 | 62.8..69.9 | 279 |
| 0.80 | 436.9 / 436.5 | 54.6 | 53.9..58.6 | 54.1..58.2 | 53.9..58.6 | 279 |
| 0.90 | 407.3 / 406.9 | 50.9 | 50.4..54.3 | 50.5..53.8 | 50.4..54.3 | 279 |
| 1.00 | 391.7 / 391.5 | 48.9 | 48.5..52.0 | 48.6..51.6 | 48.5..52.0 | 279 |
| 1.08 | 383.8 / 383.7 | 48.0 | 47.5..50.9 | 47.6..50.5 | 47.5..50.9 | 279 |

Usable Vc window (>=100 mV from both rails, edge present): 0.50..1.08 V; dead zone: no edge at Vc <= 0.40 V. Mean step 48.0..223.9 ps; individual step min/max over the window 47.5..286.1 ps; T/8 **NOT covered**. Fastest mean step (any Vc) 48.0 ps.

## b_500MHz_ss (variant b; T/8 = 250 ps; status error, 7/9 pass; backend batch; job klt-sim-fb17943592b1)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.30 | no edge / no value | - | - | - | - | 20 |
| 0.40 | no edge / no value | - | - | - | - | 45 |
| 0.50 | 2659.9 / 2717.1 | 336.1 | 320.9..422.6 | 320.9..406.0 | 326.3..422.6 | 218 |
| 0.60 | 1381.7 / 1384.1 | 172.9 | 169.0..196.9 | 169.0..196.9 | 169.6..194.7 | 220 |
| 0.70 | 1073.6 / 1071.3 | 134.1 | 132.2..145.8 | 132.5..145.8 | 132.2..145.1 | 220 |
| 0.80 | 973.1 / 972.0 | 121.6 | 120.3..130.4 | 120.4..130.4 | 120.3..130.1 | 221 |
| 0.90 | 926.6 / 926.3 | 115.8 | 114.7..123.5 | 114.7..123.5 | 114.7..123.4 | 221 |
| 1.00 | 900.4 / 900.7 | 112.6 | 111.5..119.7 | 111.5..119.7 | 111.6..119.7 | 221 |
| 1.08 | 886.7 / 887.3 | 110.9 | 109.8..117.7 | 109.8..117.7 | 109.9..117.7 | 221 |

Usable Vc window (>=100 mV from both rails, edge present): 0.50..0.90 V; dead zone: no edge at Vc <= 0.40 V. Mean step 115.8..336.1 ps; individual step min/max over the window 114.7..422.6 ps; T/8 **covered**. Fastest mean step (any Vc) 110.9 ps.

## b_500MHz_tt (variant b; T/8 = 250 ps; status error, 7/9 pass; backend batch; job klt-sim-ebf26b1f4993)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.30 | no edge / no value | - | - | - | - | 22 |
| 0.40 | no edge / no value | - | - | - | - | 49 |
| 0.50 | 2399.7 / 2467.0 | 304.2 | 290.9..391.1 | 290.9..359.8 | 295.0..391.1 | 248 |
| 0.60 | 1048.2 / 1059.9 | 131.8 | 127.5..153.0 | 127.5..153.0 | 129.2..152.5 | 247 |
| 0.70 | 732.4 / 727.4 | 91.2 | 89.7..100.3 | 90.2..100.3 | 89.7..98.8 | 248 |
| 0.80 | 641.0 / 636.1 | 79.8 | 78.7..85.9 | 79.3..85.9 | 78.7..84.9 | 249 |
| 0.90 | 602.5 / 598.1 | 75.0 | 74.1..80.2 | 74.6..80.2 | 74.1..79.4 | 249 |
| 1.00 | 581.8 / 577.9 | 72.5 | 71.6..77.2 | 72.1..77.2 | 71.6..76.4 | 249 |
| 1.08 | 571.3 / 567.5 | 71.2 | 70.4..75.7 | 70.8..75.7 | 70.4..75.0 | 249 |

Usable Vc window (>=100 mV from both rails, edge present): 0.50..1.08 V; dead zone: no edge at Vc <= 0.40 V. Mean step 71.2..304.2 ps; individual step min/max over the window 70.4..391.1 ps; T/8 **covered**. Fastest mean step (any Vc) 71.2 ps.

## Target check (mean tap step span contains T/8, usable window)

- a_1GHz_ff: NOT covered; fastest mean step 40.6 ps; dead zone top 0.6
- a_1GHz_ss: covered; fastest mean step 84.8 ps; dead zone top 0.6
- a_1GHz_tt: covered; fastest mean step 57.5 ps; dead zone top 0.6
- a_500MHz_ff: NOT covered; fastest mean step 40.6 ps; dead zone top 0.5
- a_500MHz_ss: covered; fastest mean step 84.9 ps; dead zone top 0.5
- a_500MHz_tt: covered; fastest mean step 57.5 ps; dead zone top 0.5
- b_1GHz_ff: covered; fastest mean step 48.0 ps; dead zone top 0.4
- b_1GHz_ss: covered; fastest mean step 110.9 ps; dead zone top 0.5
- b_1GHz_tt: covered; fastest mean step 71.2 ps; dead zone top 0.5
- b_500MHz_ff: NOT covered; fastest mean step 48.0 ps; dead zone top 0.4
- b_500MHz_ss: covered; fastest mean step 110.9 ps; dead zone top 0.4
- b_500MHz_tt: covered; fastest mean step 71.2 ps; dead zone top 0.4

## Run status

ERRORS:
- a_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df3' produced no value
- a_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr4' produced no value
- a_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df4' produced no value
- a_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr5' produced no value
- a_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df5' produced no value
- a_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr6' produced no value
- a_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df6' produced no value
- a_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr7' produced no value
- a_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df7' produced no value
- a_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr8' produced no value
- a_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df8' produced no value
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
- a_1GHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'df3' produced no value
- a_1GHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'dr4' produced no value
- a_1GHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'df4' produced no value
- a_1GHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'dr5' produced no value
- a_1GHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'df5' produced no value
- a_1GHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'dr6' produced no value
- a_1GHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'df6' produced no value
- a_1GHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'dr7' produced no value
- a_1GHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'df7' produced no value
- a_1GHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'dr8' produced no value
- a_1GHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'df8' produced no value
- a_1GHz_ff mos_ff/VC=0.600_Vdd=1.320V/-40C: [measurement] measurement 'dr7' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.600_Vdd=1.320V/-40C: [measurement] measurement 'df7' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.600_Vdd=1.320V/-40C: [measurement] measurement 'dr8' produced no value -- ngspice reported: out of interval
- a_1GHz_ff mos_ff/VC=0.600_Vdd=1.320V/-40C: [measurement] measurement 'df8' produced no value -- ngspice reported: out of interval
- a_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- a_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- a_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- a_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- a_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df3' produced no value
- a_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr4' produced no value
- a_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df4' produced no value
- a_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr5' produced no value
- a_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df5' produced no value
- a_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr6' produced no value
- a_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df6' produced no value
- a_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr7' produced no value
- a_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df7' produced no value
- a_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr8' produced no value
- a_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df8' produced no value
- a_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- a_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- a_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- a_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- a_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df3' produced no value
- a_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr4' produced no value
- a_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df4' produced no value
- a_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr5' produced no value
- a_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df5' produced no value
- a_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr6' produced no value
- a_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df6' produced no value
- a_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr7' produced no value
- a_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df7' produced no value
- a_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr8' produced no value
- a_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df8' produced no value
- a_1GHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- a_1GHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- a_1GHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- a_1GHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- a_1GHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_1GHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'df3' produced no value
- a_1GHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'dr4' produced no value
- a_1GHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'df4' produced no value
- a_1GHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'dr5' produced no value
- a_1GHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'df5' produced no value
- a_1GHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'dr6' produced no value
- a_1GHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'df6' produced no value
- a_1GHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'dr7' produced no value
- a_1GHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'df7' produced no value
- a_1GHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'dr8' produced no value
- a_1GHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'df8' produced no value
- a_1GHz_ss mos_ss/VC=0.600_Vdd=1.080V/125C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- a_1GHz_ss mos_ss/VC=0.600_Vdd=1.080V/125C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- a_1GHz_ss mos_ss/VC=0.600_Vdd=1.080V/125C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_1GHz_ss mos_ss/VC=0.600_Vdd=1.080V/125C: [measurement] measurement 'df3' produced no value -- ngspice reported: out of interval
- a_1GHz_ss mos_ss/VC=0.600_Vdd=1.080V/125C: [measurement] measurement 'dr4' produced no value -- ngspice reported: out of interval
- a_1GHz_ss mos_ss/VC=0.600_Vdd=1.080V/125C: [measurement] measurement 'df4' produced no value
- a_1GHz_ss mos_ss/VC=0.600_Vdd=1.080V/125C: [measurement] measurement 'dr5' produced no value
- a_1GHz_ss mos_ss/VC=0.600_Vdd=1.080V/125C: [measurement] measurement 'df5' produced no value
- a_1GHz_ss mos_ss/VC=0.600_Vdd=1.080V/125C: [measurement] measurement 'dr6' produced no value
- a_1GHz_ss mos_ss/VC=0.600_Vdd=1.080V/125C: [measurement] measurement 'df6' produced no value
- a_1GHz_ss mos_ss/VC=0.600_Vdd=1.080V/125C: [measurement] measurement 'dr7' produced no value
- a_1GHz_ss mos_ss/VC=0.600_Vdd=1.080V/125C: [measurement] measurement 'df7' produced no value
- a_1GHz_ss mos_ss/VC=0.600_Vdd=1.080V/125C: [measurement] measurement 'dr8' produced no value
- a_1GHz_ss mos_ss/VC=0.600_Vdd=1.080V/125C: [measurement] measurement 'df8' produced no value
- a_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- a_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- a_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- a_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- a_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df3' produced no value
- a_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr4' produced no value
- a_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df4' produced no value
- a_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr5' produced no value
- a_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df5' produced no value
- a_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr6' produced no value
- a_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df6' produced no value
- a_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr7' produced no value
- a_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df7' produced no value
- a_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr8' produced no value
- a_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df8' produced no value
- a_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- a_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- a_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- a_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- a_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df3' produced no value
- a_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr4' produced no value
- a_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df4' produced no value
- a_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr5' produced no value
- a_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df5' produced no value
- a_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr6' produced no value
- a_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df6' produced no value
- a_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr7' produced no value
- a_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df7' produced no value
- a_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr8' produced no value
- a_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df8' produced no value
- a_1GHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- a_1GHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- a_1GHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- a_1GHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- a_1GHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_1GHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'df3' produced no value
- a_1GHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'dr4' produced no value
- a_1GHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'df4' produced no value
- a_1GHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'dr5' produced no value
- a_1GHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'df5' produced no value
- a_1GHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'dr6' produced no value
- a_1GHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'df6' produced no value
- a_1GHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'dr7' produced no value
- a_1GHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'df7' produced no value
- a_1GHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'dr8' produced no value
- a_1GHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'df8' produced no value
- a_1GHz_tt mos_tt/VC=0.600_Vdd=1.200V/27C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_1GHz_tt mos_tt/VC=0.600_Vdd=1.200V/27C: [measurement] measurement 'df3' produced no value -- ngspice reported: out of interval
- a_1GHz_tt mos_tt/VC=0.600_Vdd=1.200V/27C: [measurement] measurement 'dr4' produced no value -- ngspice reported: out of interval
- a_1GHz_tt mos_tt/VC=0.600_Vdd=1.200V/27C: [measurement] measurement 'df4' produced no value -- ngspice reported: out of interval
- a_1GHz_tt mos_tt/VC=0.600_Vdd=1.200V/27C: [measurement] measurement 'dr5' produced no value -- ngspice reported: out of interval
- a_1GHz_tt mos_tt/VC=0.600_Vdd=1.200V/27C: [measurement] measurement 'df5' produced no value
- a_1GHz_tt mos_tt/VC=0.600_Vdd=1.200V/27C: [measurement] measurement 'dr6' produced no value
- a_1GHz_tt mos_tt/VC=0.600_Vdd=1.200V/27C: [measurement] measurement 'df6' produced no value
- a_1GHz_tt mos_tt/VC=0.600_Vdd=1.200V/27C: [measurement] measurement 'dr7' produced no value
- a_1GHz_tt mos_tt/VC=0.600_Vdd=1.200V/27C: [measurement] measurement 'df7' produced no value
- a_1GHz_tt mos_tt/VC=0.600_Vdd=1.200V/27C: [measurement] measurement 'dr8' produced no value
- a_1GHz_tt mos_tt/VC=0.600_Vdd=1.200V/27C: [measurement] measurement 'df8' produced no value
- a_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df3' produced no value
- a_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr4' produced no value
- a_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df4' produced no value
- a_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr5' produced no value
- a_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df5' produced no value
- a_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr6' produced no value
- a_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df6' produced no value
- a_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr7' produced no value
- a_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df7' produced no value
- a_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr8' produced no value
- a_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df8' produced no value
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
- a_500MHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'df3' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'dr4' produced no value -- ngspice reported: out of interval
- a_500MHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'df4' produced no value
- a_500MHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'dr5' produced no value
- a_500MHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'df5' produced no value
- a_500MHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'dr6' produced no value
- a_500MHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'df6' produced no value
- a_500MHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'dr7' produced no value
- a_500MHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'df7' produced no value
- a_500MHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'dr8' produced no value
- a_500MHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'df8' produced no value
- a_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- a_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- a_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- a_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- a_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df3' produced no value
- a_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr4' produced no value
- a_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df4' produced no value
- a_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr5' produced no value
- a_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df5' produced no value
- a_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr6' produced no value
- a_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df6' produced no value
- a_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr7' produced no value
- a_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df7' produced no value
- a_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr8' produced no value
- a_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df8' produced no value
- a_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- a_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- a_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- a_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- a_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df3' produced no value
- a_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr4' produced no value
- a_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df4' produced no value
- a_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr5' produced no value
- a_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df5' produced no value
- a_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr6' produced no value
- a_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df6' produced no value
- a_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr7' produced no value
- a_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df7' produced no value
- a_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr8' produced no value
- a_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df8' produced no value
- a_500MHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- a_500MHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- a_500MHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- a_500MHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- a_500MHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_500MHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'df3' produced no value
- a_500MHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'dr4' produced no value
- a_500MHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'df4' produced no value
- a_500MHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'dr5' produced no value
- a_500MHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'df5' produced no value
- a_500MHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'dr6' produced no value
- a_500MHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'df6' produced no value
- a_500MHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'dr7' produced no value
- a_500MHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'df7' produced no value
- a_500MHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'dr8' produced no value
- a_500MHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'df8' produced no value
- a_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- a_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- a_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- a_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- a_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df3' produced no value
- a_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr4' produced no value
- a_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df4' produced no value
- a_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr5' produced no value
- a_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df5' produced no value
- a_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr6' produced no value
- a_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df6' produced no value
- a_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr7' produced no value
- a_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df7' produced no value
- a_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr8' produced no value
- a_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df8' produced no value
- a_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- a_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- a_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- a_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- a_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df3' produced no value
- a_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr4' produced no value
- a_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df4' produced no value
- a_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr5' produced no value
- a_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df5' produced no value
- a_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr6' produced no value
- a_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df6' produced no value
- a_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr7' produced no value
- a_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df7' produced no value
- a_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr8' produced no value
- a_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df8' produced no value
- a_500MHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- a_500MHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- a_500MHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- a_500MHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- a_500MHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- a_500MHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'df3' produced no value
- a_500MHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'dr4' produced no value
- a_500MHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'df4' produced no value
- a_500MHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'dr5' produced no value
- a_500MHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'df5' produced no value
- a_500MHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'dr6' produced no value
- a_500MHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'df6' produced no value
- a_500MHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'dr7' produced no value
- a_500MHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'df7' produced no value
- a_500MHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'dr8' produced no value
- a_500MHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'df8' produced no value
- b_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- b_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- b_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- b_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- b_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- b_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df3' produced no value
- b_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr4' produced no value
- b_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df4' produced no value
- b_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr5' produced no value
- b_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df5' produced no value
- b_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr6' produced no value
- b_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df6' produced no value
- b_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr7' produced no value
- b_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df7' produced no value
- b_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr8' produced no value
- b_1GHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df8' produced no value
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
- b_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- b_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- b_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- b_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- b_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- b_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df3' produced no value
- b_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr4' produced no value
- b_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df4' produced no value
- b_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr5' produced no value
- b_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df5' produced no value
- b_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr6' produced no value
- b_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df6' produced no value
- b_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr7' produced no value
- b_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df7' produced no value
- b_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr8' produced no value
- b_1GHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df8' produced no value
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df3' produced no value -- ngspice reported: out of interval
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr4' produced no value -- ngspice reported: out of interval
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df4' produced no value
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr5' produced no value
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df5' produced no value
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr6' produced no value
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df6' produced no value
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr7' produced no value
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df7' produced no value
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr8' produced no value
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df8' produced no value
- b_1GHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'df5' produced no value -- ngspice reported: out of interval
- b_1GHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'df6' produced no value -- ngspice reported: out of interval
- b_1GHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'df7' produced no value -- ngspice reported: out of interval
- b_1GHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'df8' produced no value -- ngspice reported: out of interval
- b_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- b_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- b_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- b_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- b_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- b_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df3' produced no value
- b_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr4' produced no value
- b_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df4' produced no value
- b_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr5' produced no value
- b_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df5' produced no value
- b_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr6' produced no value
- b_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df6' produced no value
- b_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr7' produced no value
- b_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df7' produced no value
- b_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr8' produced no value
- b_1GHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df8' produced no value
- b_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- b_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- b_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- b_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- b_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- b_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df3' produced no value
- b_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr4' produced no value
- b_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df4' produced no value
- b_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr5' produced no value
- b_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df5' produced no value
- b_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr6' produced no value
- b_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df6' produced no value
- b_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr7' produced no value
- b_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df7' produced no value
- b_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr8' produced no value
- b_1GHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df8' produced no value
- b_1GHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'df6' produced no value -- ngspice reported: out of interval
- b_1GHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'df7' produced no value -- ngspice reported: out of interval
- b_1GHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'df8' produced no value -- ngspice reported: out of interval
- b_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- b_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- b_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- b_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- b_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- b_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df3' produced no value
- b_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr4' produced no value
- b_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df4' produced no value
- b_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr5' produced no value
- b_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df5' produced no value
- b_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr6' produced no value
- b_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df6' produced no value
- b_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr7' produced no value
- b_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df7' produced no value
- b_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'dr8' produced no value
- b_500MHz_ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'df8' produced no value
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
- b_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- b_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- b_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- b_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- b_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- b_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df3' produced no value
- b_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr4' produced no value
- b_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df4' produced no value
- b_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr5' produced no value
- b_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df5' produced no value
- b_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr6' produced no value
- b_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df6' produced no value
- b_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr7' produced no value
- b_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df7' produced no value
- b_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'dr8' produced no value
- b_500MHz_ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'df8' produced no value
- b_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- b_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- b_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- b_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df3' produced no value -- ngspice reported: out of interval
- b_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr4' produced no value -- ngspice reported: out of interval
- b_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df4' produced no value
- b_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr5' produced no value
- b_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df5' produced no value
- b_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr6' produced no value
- b_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df6' produced no value
- b_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr7' produced no value
- b_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df7' produced no value
- b_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr8' produced no value
- b_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df8' produced no value
- b_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- b_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- b_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- b_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- b_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- b_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df3' produced no value
- b_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr4' produced no value
- b_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df4' produced no value
- b_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr5' produced no value
- b_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df5' produced no value
- b_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr6' produced no value
- b_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df6' produced no value
- b_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr7' produced no value
- b_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df7' produced no value
- b_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'dr8' produced no value
- b_500MHz_tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'df8' produced no value
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df3' produced no value -- ngspice reported: out of interval
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr4' produced no value -- ngspice reported: out of interval
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df4' produced no value
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr5' produced no value
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df5' produced no value
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr6' produced no value
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df6' produced no value
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr7' produced no value
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df7' produced no value
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr8' produced no value
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df8' produced no value
