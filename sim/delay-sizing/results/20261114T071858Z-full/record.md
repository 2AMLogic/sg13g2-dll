# delay-sizing record

SIMULATED results, never measured. Reduced corner set (`sim/corners.json` reduced_set), NOT the 45-corner grade. Delay = single-event T0->Tk first edge at 50 % of Vdd (rising input = `dr`, falling input = `df`), ideal control sources (VBN=Vc, VBP=Vdd-Vc), 20 fF ideal load on every tap buffer, the delay-sanity method. Current = mean supply current over 6..10 ns (integer clock periods, line toggling). Tool versions: klt klt 0.9.2.dev1025+ga90545db9ea6 ; B scale 3 ; mode full

## a_1GHz_ff (variant a; T/8 = 125 ps; status error, 5/9 pass; backend batch; job klt-sim-8017f86cbd13)

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

## a_1GHz_ss (variant a; T/8 = 125 ps; status error, 5/9 pass; backend batch; job klt-sim-957a9e928c31)

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

## a_1GHz_tt (variant a; T/8 = 125 ps; status error, 5/9 pass; backend batch; job klt-sim-66ad43c20f59)

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

## a_500MHz_ff (variant a; T/8 = 250 ps; status error, 6/9 pass; backend batch; job klt-sim-d9c3f1f098c3)

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

## a_500MHz_ss (variant a; T/8 = 250 ps; status error, 6/9 pass; backend batch; job klt-sim-b835316d1f64)

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

## a_500MHz_tt (variant a; T/8 = 250 ps; status error, 6/9 pass; backend batch; job klt-sim-9593bf6ed74a)

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

## b_1GHz_ff (variant b; T/8 = 125 ps; status error, 6/9 pass; backend batch; job klt-sim-7b9b7d53c6e0)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.30 | no edge / no value | - | - | - | - | 48 |
| 0.40 | no edge / no value | - | - | - | - | 59 |
| 0.50 | no edge / no value | - | - | - | - | 226 |
| 0.60 | 956.4 / 992.4 | 121.8 | 116.3..149.8 | 116.3..140.1 | 119.7..149.8 | 557 |
| 0.70 | 593.2 / 599.2 | 74.5 | 72.7..83.7 | 72.7..82.6 | 73.5..83.7 | 557 |
| 0.80 | 481.2 / 481.1 | 60.1 | 59.3..65.2 | 59.4..64.7 | 59.3..65.2 | 558 |
| 0.90 | 437.2 / 436.6 | 54.6 | 54.0..58.5 | 54.1..58.1 | 54.0..58.5 | 558 |
| 1.00 | 414.8 / 414.3 | 51.8 | 51.3..55.3 | 51.4..54.9 | 51.3..55.3 | 558 |
| 1.08 | 403.7 / 403.3 | 50.4 | 49.9..53.7 | 50.0..53.3 | 49.9..53.7 | 558 |

Usable Vc window (>=100 mV from both rails, edge present): 0.60..1.08 V; dead zone: no edge at Vc <= 0.50 V. Mean step 50.4..121.8 ps; individual step min/max over the window 49.9..149.8 ps; T/8 **NOT covered**. Fastest mean step (any Vc) 50.4 ps.

## b_1GHz_ss (variant b; T/8 = 125 ps; status error, 6/9 pass; backend batch; job klt-sim-33384f66f50e)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.30 | no edge / no value | - | - | - | - | 38 |
| 0.40 | no edge / no value | - | - | - | - | 41 |
| 0.50 | no edge / no value | - | - | - | - | 119 |
| 0.60 | 1660.7 / 1670.0 | 208.2 | 202.0..242.3 | 202.0..242.3 | 203.7..240.7 | 437 |
| 0.70 | 1190.5 / 1187.2 | 148.6 | 146.2..163.9 | 146.6..163.9 | 146.2..162.7 | 440 |
| 0.80 | 1042.4 / 1039.8 | 130.1 | 128.5..140.7 | 128.8..140.7 | 128.5..140.1 | 441 |
| 0.90 | 976.6 / 974.8 | 122.0 | 120.6..130.8 | 120.8..130.8 | 120.6..130.4 | 441 |
| 1.00 | 940.4 / 939.2 | 117.5 | 116.3..125.5 | 116.4..125.5 | 116.3..125.2 | 441 |
| 1.08 | 921.6 / 920.8 | 115.1 | 114.0..122.8 | 114.1..122.8 | 114.0..122.5 | 441 |

Usable Vc window (>=100 mV from both rails, edge present): 0.60..0.90 V; dead zone: no edge at Vc <= 0.50 V. Mean step 122.0..208.2 ps; individual step min/max over the window 120.6..242.3 ps; T/8 **covered**. Fastest mean step (any Vc) 115.1 ps.

## b_1GHz_tt (variant b; T/8 = 125 ps; status error, 6/9 pass; backend batch; job klt-sim-d008ef188b11)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.30 | no edge / no value | - | - | - | - | 43 |
| 0.40 | no edge / no value | - | - | - | - | 46 |
| 0.50 | no edge / no value | - | - | - | - | 123 |
| 0.60 | 1313.9 / 1341.6 | 166.0 | 159.2..199.0 | 159.2..195.1 | 162.6..199.0 | 493 |
| 0.70 | 837.0 / 834.1 | 104.4 | 102.5..117.0 | 102.7..117.0 | 102.5..115.2 | 496 |
| 0.80 | 697.2 / 691.7 | 86.8 | 85.5..94.3 | 86.1..94.3 | 85.5..93.1 | 497 |
| 0.90 | 641.3 / 636.1 | 79.8 | 78.7..85.9 | 79.3..85.9 | 78.7..84.8 | 497 |
| 1.00 | 612.2 / 607.4 | 76.2 | 75.2..81.6 | 75.8..81.6 | 75.2..80.6 | 497 |
| 1.08 | 597.6 / 593.1 | 74.4 | 73.5..79.5 | 74.0..79.5 | 73.5..78.6 | 497 |

Usable Vc window (>=100 mV from both rails, edge present): 0.60..1.08 V; dead zone: no edge at Vc <= 0.50 V. Mean step 74.4..166.0 ps; individual step min/max over the window 73.5..199.0 ps; T/8 **covered**. Fastest mean step (any Vc) 74.4 ps.

## b_500MHz_ff (variant b; T/8 = 250 ps; status error, 7/9 pass; backend batch; job klt-sim-b433ec88f70e)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.30 | no edge / no value | - | - | - | - | 24 |
| 0.40 | no edge / no value | - | - | - | - | 59 |
| 0.50 | 2459.7 / 2582.3 | 315.1 | 301.6..395.0 | 301.6..348.1 | 311.8..395.0 | 290 |
| 0.60 | 956.4 / 992.4 | 121.8 | 116.3..149.8 | 116.3..140.1 | 119.7..149.8 | 279 |
| 0.70 | 593.2 / 599.3 | 74.5 | 72.8..83.7 | 72.8..82.6 | 73.5..83.7 | 279 |
| 0.80 | 481.2 / 481.1 | 60.1 | 59.3..65.2 | 59.4..64.7 | 59.3..65.2 | 279 |
| 0.90 | 437.2 / 436.6 | 54.6 | 54.0..58.5 | 54.1..58.1 | 54.0..58.5 | 279 |
| 1.00 | 414.8 / 414.3 | 51.8 | 51.3..55.3 | 51.4..54.9 | 51.3..55.3 | 279 |
| 1.08 | 403.7 / 403.3 | 50.4 | 49.9..53.7 | 50.0..53.3 | 49.9..53.7 | 279 |

Usable Vc window (>=100 mV from both rails, edge present): 0.50..1.08 V; dead zone: no edge at Vc <= 0.40 V. Mean step 50.4..315.1 ps; individual step min/max over the window 49.9..395.0 ps; T/8 **covered**. Fastest mean step (any Vc) 50.4 ps.

## b_500MHz_ss (variant b; T/8 = 250 ps; status error, 7/9 pass; backend batch; job klt-sim-a3e11da4cbf7)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.30 | no edge / no value | - | - | - | - | 19 |
| 0.40 | no edge / no value | - | - | - | - | 30 |
| 0.50 | 3525.3 / 3594.8 | 445.0 | 425.9..571.9 | 425.9..538.8 | 430.3..571.9 | 218 |
| 0.60 | 1660.7 / 1676.3 | 208.6 | 202.1..242.3 | 202.1..242.3 | 204.4..241.7 | 219 |
| 0.70 | 1190.5 / 1188.1 | 148.7 | 146.3..163.9 | 146.6..163.9 | 146.3..162.9 | 220 |
| 0.80 | 1042.4 / 1040.2 | 130.2 | 128.5..140.7 | 128.8..140.7 | 128.5..140.2 | 221 |
| 0.90 | 976.6 / 975.1 | 122.0 | 120.7..130.8 | 120.8..130.8 | 120.7..130.5 | 221 |
| 1.00 | 940.4 / 939.5 | 117.5 | 116.3..125.5 | 116.4..125.5 | 116.3..125.2 | 221 |
| 1.08 | 921.6 / 921.0 | 115.2 | 114.1..122.8 | 114.1..122.8 | 114.1..122.6 | 221 |

Usable Vc window (>=100 mV from both rails, edge present): 0.50..0.90 V; dead zone: no edge at Vc <= 0.40 V. Mean step 122.0..445.0 ps; individual step min/max over the window 120.7..571.9 ps; T/8 **covered**. Fastest mean step (any Vc) 115.2 ps.

## b_500MHz_tt (variant b; T/8 = 250 ps; status error, 7/9 pass; backend batch; job klt-sim-b03630600395)

| Vc (V) | d8 rise-in / fall-in (ps) | mean step (ps) | step min..max, all (ps) | rise-out min..max | fall-out min..max | I(vdd) mean (uA) |
|---|---|---|---|---|---|---|
| 0.30 | no edge / no value | - | - | - | - | 22 |
| 0.40 | no edge / no value | - | - | - | - | 35 |
| 0.50 | 3308.0 / 3385.9 | 418.4 | 402.6..536.0 | 402.6..488.6 | 406.2..536.0 | 248 |
| 0.60 | 1313.9 / 1342.0 | 166.0 | 159.2..199.1 | 159.2..195.1 | 162.6..199.1 | 247 |
| 0.70 | 837.0 / 834.1 | 104.4 | 102.5..117.0 | 102.7..117.0 | 102.5..115.2 | 248 |
| 0.80 | 697.2 / 691.7 | 86.8 | 85.5..94.3 | 86.1..94.3 | 85.5..93.1 | 248 |
| 0.90 | 641.3 / 636.1 | 79.8 | 78.7..85.9 | 79.3..85.9 | 78.7..84.8 | 249 |
| 1.00 | 612.3 / 607.4 | 76.2 | 75.3..81.6 | 75.8..81.6 | 75.3..80.6 | 249 |
| 1.08 | 597.6 / 593.1 | 74.4 | 73.5..79.5 | 74.0..79.5 | 73.5..78.6 | 249 |

Usable Vc window (>=100 mV from both rails, edge present): 0.50..1.08 V; dead zone: no edge at Vc <= 0.40 V. Mean step 74.4..418.4 ps; individual step min/max over the window 73.5..536.0 ps; T/8 **covered**. Fastest mean step (any Vc) 74.4 ps.

## Target check (mean tap step span contains T/8, usable window)

- a_1GHz_ff: NOT covered; fastest mean step 40.6 ps; dead zone top 0.6
- a_1GHz_ss: covered; fastest mean step 84.8 ps; dead zone top 0.6
- a_1GHz_tt: covered; fastest mean step 57.5 ps; dead zone top 0.6
- a_500MHz_ff: NOT covered; fastest mean step 40.6 ps; dead zone top 0.5
- a_500MHz_ss: covered; fastest mean step 84.9 ps; dead zone top 0.5
- a_500MHz_tt: covered; fastest mean step 57.5 ps; dead zone top 0.5
- b_1GHz_ff: NOT covered; fastest mean step 50.4 ps; dead zone top 0.5
- b_1GHz_ss: covered; fastest mean step 115.1 ps; dead zone top 0.5
- b_1GHz_tt: covered; fastest mean step 74.4 ps; dead zone top 0.5
- b_500MHz_ff: covered; fastest mean step 50.4 ps; dead zone top 0.4
- b_500MHz_ss: covered; fastest mean step 115.2 ps; dead zone top 0.4
- b_500MHz_tt: covered; fastest mean step 74.4 ps; dead zone top 0.4

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
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df3' produced no value
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr4' produced no value
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df4' produced no value
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr5' produced no value
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df5' produced no value
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr6' produced no value
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df6' produced no value
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr7' produced no value
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df7' produced no value
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'dr8' produced no value
- b_1GHz_ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'df8' produced no value
- b_1GHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'df5' produced no value -- ngspice reported: out of interval
- b_1GHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'df6' produced no value -- ngspice reported: out of interval
- b_1GHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'df7' produced no value -- ngspice reported: out of interval
- b_1GHz_ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'df8' produced no value -- ngspice reported: out of interval
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
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr1' produced no value -- ngspice reported: out of interval
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df3' produced no value
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr4' produced no value
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df4' produced no value
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr5' produced no value
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df5' produced no value
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr6' produced no value
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df6' produced no value
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr7' produced no value
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df7' produced no value
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr8' produced no value
- b_1GHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df8' produced no value
- b_1GHz_ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'df3' produced no value -- ngspice reported: out of interval
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
- b_1GHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'df3' produced no value -- ngspice reported: out of interval
- b_1GHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'df4' produced no value -- ngspice reported: out of interval
- b_1GHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'df5' produced no value -- ngspice reported: out of interval
- b_1GHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'df6' produced no value -- ngspice reported: out of interval
- b_1GHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'df7' produced no value -- ngspice reported: out of interval
- b_1GHz_tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'df8' produced no value
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
- b_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- b_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- b_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- b_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- b_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'df3' produced no value -- ngspice reported: out of interval
- b_500MHz_ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'dr4' produced no value
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
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df1' produced no value -- ngspice reported: out of interval
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr2' produced no value -- ngspice reported: out of interval
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df2' produced no value -- ngspice reported: out of interval
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr3' produced no value -- ngspice reported: out of interval
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df3' produced no value -- ngspice reported: out of interval
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr4' produced no value
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df4' produced no value
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr5' produced no value
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df5' produced no value
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr6' produced no value
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df6' produced no value
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr7' produced no value
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df7' produced no value
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'dr8' produced no value
- b_500MHz_tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'df8' produced no value
