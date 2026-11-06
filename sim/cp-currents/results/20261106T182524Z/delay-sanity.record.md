# delay-sanity record

SIMULATED results, never measured. Reduced corner set (`sim/corners.json` reduced_set: tt/1.2 V/27 C, ss/1.08 V/125 C, ff/1.32 V/-40 C); NOT the 45-corner grade. Delay = single-event T0->Tk, first rising edge, 50 % of Vdd, ideal control sources (VBN=Vc, VBP=Vdd-Vc), 20 fF ideal load on every tap buffer.

## 500MHz: T/8 = 250.0 ps, total delay target span 1.667..2.500 ns (decision 0004 +/-20 %)

### corner ss (status error, 6/9 pass; backend {'resolved': 'batch', 'source': 'env', 'requested': 'batch'}; job klt-sim-bcbf3bafc512)

| Vc (V) | d8 total (ps) | mean step (ps) | min..max tap spacing (ps) |
|---|---|---|---|
| 0.30 | no edge / no value | - | - |
| 0.40 | no edge / no value | - | - |
| 0.50 | no edge / no value | - | - |
| 0.60 | 4277.3 | 534.7 | 517.5..652.4 |
| 0.70 | 2342.2 | 292.8 | 284.0..347.5 |
| 0.80 | 1678.7 | 209.8 | 205.0..239.8 |
| 0.90 | 1407.6 | 176.0 | 172.8..195.9 |
| 1.00 | 1272.1 | 159.0 | 156.6..174.6 |
| 1.08 | 1205.9 | 150.7 | 148.7..164.5 |

Mean tap step over Vc >=100 mV from both rails: 176.0..534.7 ps; T/8 250.0 ps **covered**; total d8 1.408..4.277 ns vs 0004 span 1.667..2.500 ns **spans**.

### corner tt (status error, 6/9 pass; backend {'resolved': 'batch', 'source': 'env', 'requested': 'batch'}; job klt-sim-7d87bf65a822)

| Vc (V) | d8 total (ps) | mean step (ps) | min..max tap spacing (ps) |
|---|---|---|---|
| 0.30 | no edge / no value | - | - |
| 0.40 | no edge / no value | - | - |
| 0.50 | no edge / no value | - | - |
| 0.60 | 3731.5 | 466.4 | 452.5..563.4 |
| 0.70 | 1863.8 | 233.0 | 226.2..278.0 |
| 0.80 | 1237.5 | 154.7 | 150.7..178.8 |
| 0.90 | 987.9 | 123.5 | 121.0..138.4 |
| 1.00 | 870.2 | 108.8 | 107.0..119.8 |
| 1.08 | 815.3 | 101.9 | 100.4..111.3 |

Mean tap step over Vc >=100 mV from both rails: 101.9..466.4 ps; T/8 250.0 ps **covered**; total d8 0.815..3.731 ns vs 0004 span 1.667..2.500 ns **spans**.

### corner ff (status error, 6/9 pass; backend {'resolved': 'batch', 'source': 'env', 'requested': 'batch'}; job klt-sim-bd91eb96e666)

| Vc (V) | d8 total (ps) | mean step (ps) | min..max tap spacing (ps) |
|---|---|---|---|
| 0.30 | no edge / no value | - | - |
| 0.40 | no edge / no value | - | - |
| 0.50 | no edge / no value | - | - |
| 0.60 | 2834.0 | 354.3 | 345.7..414.2 |
| 0.70 | 1407.6 | 175.9 | 171.4..206.8 |
| 0.80 | 916.1 | 114.5 | 111.8..131.0 |
| 0.90 | 712.2 | 89.0 | 87.3..99.1 |
| 1.00 | 615.7 | 77.0 | 75.7..84.0 |
| 1.08 | 571.4 | 71.4 | 70.4..77.3 |

Mean tap step over Vc >=100 mV from both rails: 71.4..354.3 ps; T/8 250.0 ps **covered**; total d8 0.571..2.834 ns vs 0004 span 1.667..2.500 ns **spans**.

## 1GHz: T/8 = 125.0 ps, total delay target span 0.833..1.250 ns (decision 0004 +/-20 %)

### corner ss (status error, 5/9 pass; backend {'resolved': 'batch', 'source': 'env', 'requested': 'batch'}; job klt-sim-809a08e3fb4f)

| Vc (V) | d8 total (ps) | mean step (ps) | min..max tap spacing (ps) |
|---|---|---|---|
| 0.30 | no edge / no value | - | - |
| 0.40 | no edge / no value | - | - |
| 0.50 | no edge / no value | - | - |
| 0.60 | no edge / no value | - | - |
| 0.70 | 2345.2 | 293.2 | 284.4..347.6 |
| 0.80 | 1678.6 | 209.8 | 205.0..239.8 |
| 0.90 | 1407.6 | 176.0 | 172.8..195.9 |
| 1.00 | 1272.1 | 159.0 | 156.6..174.6 |
| 1.08 | 1205.9 | 150.7 | 148.7..164.5 |

Mean tap step over Vc >=100 mV from both rails: 176.0..293.2 ps; T/8 125.0 ps **NOT covered (gap)**; total d8 1.408..2.345 ns vs 0004 span 0.833..1.250 ns **does not span**.

### corner tt (status error, 5/9 pass; backend {'resolved': 'batch', 'source': 'env', 'requested': 'batch'}; job klt-sim-9450a6d3d8bb)

| Vc (V) | d8 total (ps) | mean step (ps) | min..max tap spacing (ps) |
|---|---|---|---|
| 0.30 | no edge / no value | - | - |
| 0.40 | no edge / no value | - | - |
| 0.50 | no edge / no value | - | - |
| 0.60 | 6310.1 | 788.8 | 451.9..1369.5 |
| 0.70 | 1863.6 | 232.9 | 226.2..278.0 |
| 0.80 | 1237.5 | 154.7 | 150.7..178.8 |
| 0.90 | 987.9 | 123.5 | 121.0..138.4 |
| 1.00 | 870.2 | 108.8 | 107.0..119.8 |
| 1.08 | 815.3 | 101.9 | 100.4..111.3 |

Mean tap step over Vc >=100 mV from both rails: 101.9..788.8 ps; T/8 125.0 ps **covered**; total d8 0.815..6.310 ns vs 0004 span 0.833..1.250 ns **spans**.

### corner ff (status error, 6/9 pass; backend {'resolved': 'batch', 'source': 'env', 'requested': 'batch'}; job klt-sim-f84a6010930b)

| Vc (V) | d8 total (ps) | mean step (ps) | min..max tap spacing (ps) |
|---|---|---|---|
| 0.30 | no edge / no value | - | - |
| 0.40 | no edge / no value | - | - |
| 0.50 | no edge / no value | - | - |
| 0.60 | 3687.9 | 461.0 | 336.8..1210.8 |
| 0.70 | 1407.6 | 175.9 | 171.4..206.8 |
| 0.80 | 916.1 | 114.5 | 111.8..131.0 |
| 0.90 | 712.2 | 89.0 | 87.3..99.1 |
| 1.00 | 615.7 | 77.0 | 75.7..84.0 |
| 1.08 | 571.4 | 71.4 | 70.4..77.3 |

Mean tap step over Vc >=100 mV from both rails: 71.4..461.0 ps; T/8 125.0 ps **covered**; total d8 0.571..3.688 ns vs 0004 span 0.833..1.250 ns **spans**.

## Verdict

FAIL:
- 500MHz/ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'd1' produced no value -- ngspice reported: out of interval
- 500MHz/ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'd2' produced no value -- ngspice reported: out of interval
- 500MHz/ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'd3' produced no value -- ngspice reported: out of interval
- 500MHz/ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'd4' produced no value -- ngspice reported: out of interval
- 500MHz/ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'd5' produced no value -- ngspice reported: out of interval
- 500MHz/ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'd6' produced no value
- 500MHz/ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'd7' produced no value
- 500MHz/ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'd8' produced no value
- 500MHz/ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'd1' produced no value -- ngspice reported: out of interval
- 500MHz/ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'd2' produced no value -- ngspice reported: out of interval
- 500MHz/ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'd3' produced no value -- ngspice reported: out of interval
- 500MHz/ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'd4' produced no value -- ngspice reported: out of interval
- 500MHz/ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'd5' produced no value -- ngspice reported: out of interval
- 500MHz/ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'd6' produced no value
- 500MHz/ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'd7' produced no value
- 500MHz/ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'd8' produced no value
- 500MHz/ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'd1' produced no value -- ngspice reported: out of interval
- 500MHz/ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'd2' produced no value -- ngspice reported: out of interval
- 500MHz/ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'd3' produced no value -- ngspice reported: out of interval
- 500MHz/ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'd4' produced no value -- ngspice reported: out of interval
- 500MHz/ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'd5' produced no value -- ngspice reported: out of interval
- 500MHz/ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'd6' produced no value
- 500MHz/ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'd7' produced no value
- 500MHz/ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'd8' produced no value
- 500MHz/tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'd1' produced no value -- ngspice reported: out of interval
- 500MHz/tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'd2' produced no value -- ngspice reported: out of interval
- 500MHz/tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'd3' produced no value -- ngspice reported: out of interval
- 500MHz/tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'd4' produced no value -- ngspice reported: out of interval
- 500MHz/tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'd5' produced no value -- ngspice reported: out of interval
- 500MHz/tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'd6' produced no value
- 500MHz/tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'd7' produced no value
- 500MHz/tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'd8' produced no value
- 500MHz/tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'd1' produced no value -- ngspice reported: out of interval
- 500MHz/tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'd2' produced no value -- ngspice reported: out of interval
- 500MHz/tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'd3' produced no value -- ngspice reported: out of interval
- 500MHz/tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'd4' produced no value -- ngspice reported: out of interval
- 500MHz/tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'd5' produced no value -- ngspice reported: out of interval
- 500MHz/tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'd6' produced no value
- 500MHz/tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'd7' produced no value
- 500MHz/tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'd8' produced no value
- 500MHz/tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'd1' produced no value -- ngspice reported: out of interval
- 500MHz/tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'd2' produced no value -- ngspice reported: out of interval
- 500MHz/tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'd3' produced no value -- ngspice reported: out of interval
- 500MHz/tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'd4' produced no value -- ngspice reported: out of interval
- 500MHz/tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'd5' produced no value -- ngspice reported: out of interval
- 500MHz/tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'd6' produced no value
- 500MHz/tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'd7' produced no value
- 500MHz/tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'd8' produced no value
- 500MHz/ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'd1' produced no value -- ngspice reported: out of interval
- 500MHz/ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'd2' produced no value -- ngspice reported: out of interval
- 500MHz/ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'd3' produced no value -- ngspice reported: out of interval
- 500MHz/ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'd4' produced no value -- ngspice reported: out of interval
- 500MHz/ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'd5' produced no value -- ngspice reported: out of interval
- 500MHz/ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'd6' produced no value
- 500MHz/ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'd7' produced no value
- 500MHz/ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'd8' produced no value
- 500MHz/ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'd1' produced no value -- ngspice reported: out of interval
- 500MHz/ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'd2' produced no value -- ngspice reported: out of interval
- 500MHz/ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'd3' produced no value -- ngspice reported: out of interval
- 500MHz/ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'd4' produced no value -- ngspice reported: out of interval
- 500MHz/ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'd5' produced no value -- ngspice reported: out of interval
- 500MHz/ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'd6' produced no value
- 500MHz/ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'd7' produced no value
- 500MHz/ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'd8' produced no value
- 500MHz/ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'd2' produced no value -- ngspice reported: out of interval
- 500MHz/ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'd3' produced no value -- ngspice reported: out of interval
- 500MHz/ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'd4' produced no value -- ngspice reported: out of interval
- 500MHz/ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'd5' produced no value -- ngspice reported: out of interval
- 500MHz/ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'd6' produced no value -- ngspice reported: out of interval
- 500MHz/ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'd7' produced no value
- 500MHz/ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'd8' produced no value
- 1GHz/ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'd1' produced no value -- ngspice reported: out of interval
- 1GHz/ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'd2' produced no value -- ngspice reported: out of interval
- 1GHz/ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'd3' produced no value -- ngspice reported: out of interval
- 1GHz/ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'd4' produced no value -- ngspice reported: out of interval
- 1GHz/ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'd5' produced no value -- ngspice reported: out of interval
- 1GHz/ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'd6' produced no value
- 1GHz/ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'd7' produced no value
- 1GHz/ss mos_ss/VC=0.300_Vdd=1.080V/125C: [measurement] measurement 'd8' produced no value
- 1GHz/ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'd1' produced no value -- ngspice reported: out of interval
- 1GHz/ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'd2' produced no value -- ngspice reported: out of interval
- 1GHz/ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'd3' produced no value -- ngspice reported: out of interval
- 1GHz/ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'd4' produced no value -- ngspice reported: out of interval
- 1GHz/ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'd5' produced no value -- ngspice reported: out of interval
- 1GHz/ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'd6' produced no value
- 1GHz/ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'd7' produced no value
- 1GHz/ss mos_ss/VC=0.400_Vdd=1.080V/125C: [measurement] measurement 'd8' produced no value
- 1GHz/ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'd1' produced no value -- ngspice reported: out of interval
- 1GHz/ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'd2' produced no value -- ngspice reported: out of interval
- 1GHz/ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'd3' produced no value -- ngspice reported: out of interval
- 1GHz/ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'd4' produced no value -- ngspice reported: out of interval
- 1GHz/ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'd5' produced no value -- ngspice reported: out of interval
- 1GHz/ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'd6' produced no value
- 1GHz/ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'd7' produced no value
- 1GHz/ss mos_ss/VC=0.500_Vdd=1.080V/125C: [measurement] measurement 'd8' produced no value
- 1GHz/ss mos_ss/VC=0.600_Vdd=1.080V/125C: [measurement] measurement 'd5' produced no value -- ngspice reported: out of interval
- 1GHz/ss mos_ss/VC=0.600_Vdd=1.080V/125C: [measurement] measurement 'd6' produced no value -- ngspice reported: out of interval
- 1GHz/ss mos_ss/VC=0.600_Vdd=1.080V/125C: [measurement] measurement 'd7' produced no value -- ngspice reported: out of interval
- 1GHz/ss mos_ss/VC=0.600_Vdd=1.080V/125C: [measurement] measurement 'd8' produced no value -- ngspice reported: out of interval
- 1GHz/ss: T/8 not covered (176.0..293.2 ps)
- 1GHz/tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'd1' produced no value -- ngspice reported: out of interval
- 1GHz/tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'd2' produced no value -- ngspice reported: out of interval
- 1GHz/tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'd3' produced no value -- ngspice reported: out of interval
- 1GHz/tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'd4' produced no value -- ngspice reported: out of interval
- 1GHz/tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'd5' produced no value -- ngspice reported: out of interval
- 1GHz/tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'd6' produced no value
- 1GHz/tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'd7' produced no value
- 1GHz/tt mos_tt/VC=0.300_Vdd=1.200V/27C: [measurement] measurement 'd8' produced no value
- 1GHz/tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'd1' produced no value -- ngspice reported: out of interval
- 1GHz/tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'd2' produced no value -- ngspice reported: out of interval
- 1GHz/tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'd3' produced no value -- ngspice reported: out of interval
- 1GHz/tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'd4' produced no value -- ngspice reported: out of interval
- 1GHz/tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'd5' produced no value -- ngspice reported: out of interval
- 1GHz/tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'd6' produced no value
- 1GHz/tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'd7' produced no value
- 1GHz/tt mos_tt/VC=0.400_Vdd=1.200V/27C: [measurement] measurement 'd8' produced no value
- 1GHz/tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'd1' produced no value -- ngspice reported: out of interval
- 1GHz/tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'd2' produced no value -- ngspice reported: out of interval
- 1GHz/tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'd3' produced no value -- ngspice reported: out of interval
- 1GHz/tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'd4' produced no value -- ngspice reported: out of interval
- 1GHz/tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'd5' produced no value -- ngspice reported: out of interval
- 1GHz/tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'd6' produced no value
- 1GHz/tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'd7' produced no value
- 1GHz/tt mos_tt/VC=0.500_Vdd=1.200V/27C: [measurement] measurement 'd8' produced no value
- 1GHz/ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'd1' produced no value -- ngspice reported: out of interval
- 1GHz/ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'd2' produced no value -- ngspice reported: out of interval
- 1GHz/ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'd3' produced no value -- ngspice reported: out of interval
- 1GHz/ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'd4' produced no value -- ngspice reported: out of interval
- 1GHz/ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'd5' produced no value -- ngspice reported: out of interval
- 1GHz/ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'd6' produced no value
- 1GHz/ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'd7' produced no value
- 1GHz/ff mos_ff/VC=0.300_Vdd=1.320V/-40C: [measurement] measurement 'd8' produced no value
- 1GHz/ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'd1' produced no value -- ngspice reported: out of interval
- 1GHz/ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'd2' produced no value -- ngspice reported: out of interval
- 1GHz/ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'd3' produced no value -- ngspice reported: out of interval
- 1GHz/ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'd4' produced no value -- ngspice reported: out of interval
- 1GHz/ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'd5' produced no value -- ngspice reported: out of interval
- 1GHz/ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'd6' produced no value
- 1GHz/ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'd7' produced no value
- 1GHz/ff mos_ff/VC=0.400_Vdd=1.320V/-40C: [measurement] measurement 'd8' produced no value
- 1GHz/ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'd1' produced no value -- ngspice reported: out of interval
- 1GHz/ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'd2' produced no value -- ngspice reported: out of interval
- 1GHz/ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'd3' produced no value -- ngspice reported: out of interval
- 1GHz/ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'd4' produced no value -- ngspice reported: out of interval
- 1GHz/ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'd5' produced no value -- ngspice reported: out of interval
- 1GHz/ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'd6' produced no value
- 1GHz/ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'd7' produced no value
- 1GHz/ff mos_ff/VC=0.500_Vdd=1.320V/-40C: [measurement] measurement 'd8' produced no value
