# PFD fit-gate record (decision 0006)

Simulated, never measured. Criteria C1-C3 are in `sim/pfd-fit/grade.py`.

## pfd_1g

- engine: ngspice 47; backend/host: worker; remote job: klt-sim-dc27f9cf6ad5
- envelope status: pass

- `mos_tt/1.200V/27C`: **FAIL**; reset-pulse width 138..139 ps
  - C1 offset -40 ps: (wUP-wDN)/offset = 1.77
  - C1 offset -20 ps: (wUP-wDN)/offset = 1.82
  - C1 offset -10 ps: (wUP-wDN)/offset = 1.78
- `mos_ss/1.080V/125C`: **FAIL**; reset-pulse width 0..229 ps
  - C1 offset -40 ps: (wUP-wDN)/offset = 1.50
  - C1 offset 10 ps: (wUP-wDN)/offset = 0.22
  - C2 reset-pulse width 0..229 ps outside 30 ps..250 ps
- `mos_ff/1.320V/-40C`: **FAIL**; reset-pulse width 93..94 ps
  - C1 offset -40 ps: (wUP-wDN)/offset = 1.63
  - C1 offset -20 ps: (wUP-wDN)/offset = 1.89
  - C1 offset -10 ps: (wUP-wDN)/offset = 1.85
  - C1 offset 20 ps: (wUP-wDN)/offset = 1.51

| corner | offset ps | wUP ps | wDN ps | wUP-wDN ps |
|---|---|---|---|---|
| mos_tt/1.200V/27C | -160.0 | 133.3 | 333.1 | -199.7 |
| mos_tt/1.200V/27C | -80.0 | 129.7 | 248.8 | -119.1 |
| mos_tt/1.200V/27C | -40.0 | 129.8 | 200.4 | -70.6 |
| mos_tt/1.200V/27C | -20.0 | 131.9 | 168.3 | -36.4 |
| mos_tt/1.200V/27C | -10.0 | 134.1 | 151.9 | -17.8 |
| mos_tt/1.200V/27C | -5.0 | 135.8 | 145.8 | -10.0 |
| mos_tt/1.200V/27C | 0.0 | 138.5 | 142.0 | -3.6 |
| mos_tt/1.200V/27C | 5.0 | 142.7 | 139.9 | 2.8 |
| mos_tt/1.200V/27C | 10.0 | 149.1 | 138.5 | 10.6 |
| mos_tt/1.200V/27C | 20.0 | 164.8 | 137.0 | 27.8 |
| mos_tt/1.200V/27C | 40.0 | 193.0 | 135.7 | 57.3 |
| mos_tt/1.200V/27C | 80.0 | 241.5 | 136.5 | 105.0 |
| mos_tt/1.200V/27C | 160.0 | 329.8 | 138.9 | 190.9 |
| mos_ss/1.080V/125C | -160.0 | 220.9 | 429.1 | -208.2 |
| mos_ss/1.080V/125C | -80.0 | 218.6 | 336.2 | -117.6 |
| mos_ss/1.080V/125C | -40.0 | 221.6 | 281.8 | -60.1 |
| mos_ss/1.080V/125C | -20.0 | 224.1 | 251.3 | -27.2 |
| mos_ss/1.080V/125C | -10.0 | 226.0 | 240.8 | -14.8 |
| mos_ss/1.080V/125C | -5.0 | 227.3 | 237.6 | -10.3 |
| mos_ss/1.080V/125C | 0.0 | 229.1 | 235.5 | -6.4 |
| mos_ss/1.080V/125C | 5.0 | 231.6 | 234.0 | -2.4 |
| mos_ss/1.080V/125C | 10.0 | 235.2 | 233.0 | 2.2 |
| mos_ss/1.080V/125C | 20.0 | 246.2 | 231.6 | 14.6 |
| mos_ss/1.080V/125C | 40.0 | 275.4 | 230.1 | 45.3 |
| mos_ss/1.080V/125C | 80.0 | 324.6 | 228.6 | 96.0 |
| mos_ss/1.080V/125C | 160.0 | 421.2 | 231.1 | 190.1 |
| mos_ff/1.320V/-40C | -160.0 | 90.2 | 278.0 | -187.8 |
| mos_ff/1.320V/-40C | -80.0 | 90.2 | 197.0 | -106.8 |
| mos_ff/1.320V/-40C | -40.0 | 87.0 | 152.0 | -65.0 |
| mos_ff/1.320V/-40C | -20.0 | 88.1 | 126.0 | -37.9 |
| mos_ff/1.320V/-40C | -10.0 | 89.6 | 108.1 | -18.5 |
| mos_ff/1.320V/-40C | -5.0 | 91.1 | 100.4 | -9.3 |
| mos_ff/1.320V/-40C | 0.0 | 93.8 | 96.0 | -2.2 |
| mos_ff/1.320V/-40C | 5.0 | 98.6 | 93.9 | 4.7 |
| mos_ff/1.320V/-40C | 10.0 | 106.1 | 92.8 | 13.3 |
| mos_ff/1.320V/-40C | 20.0 | 122.0 | 91.8 | 30.1 |
| mos_ff/1.320V/-40C | 40.0 | 146.2 | 91.4 | 54.9 |
| mos_ff/1.320V/-40C | 80.0 | 192.9 | 93.6 | 99.3 |
| mos_ff/1.320V/-40C | 160.0 | 276.1 | 93.0 | 183.1 |

## pfd_500m

- engine: ngspice 47; backend/host: worker; remote job: klt-sim-58c1ccea779c
- envelope status: pass

- `mos_tt/1.200V/27C`: **FAIL**; reset-pulse width 138..138 ps
  - C1 offset -40 ps: (wUP-wDN)/offset = 1.77
  - C1 offset -20 ps: (wUP-wDN)/offset = 1.81
  - C1 offset -10 ps: (wUP-wDN)/offset = 1.77
- `mos_ss/1.080V/125C`: **FAIL**; reset-pulse width 0..229 ps
  - C1 offset 10 ps: (wUP-wDN)/offset = 0.21
  - C2 reset-pulse width 0..229 ps outside 30 ps..500 ps
- `mos_ff/1.320V/-40C`: **FAIL**; reset-pulse width 93..94 ps
  - C1 offset -40 ps: (wUP-wDN)/offset = 1.63
  - C1 offset -20 ps: (wUP-wDN)/offset = 1.89
  - C1 offset -10 ps: (wUP-wDN)/offset = 1.84
  - C1 offset 20 ps: (wUP-wDN)/offset = 1.51

| corner | offset ps | wUP ps | wDN ps | wUP-wDN ps |
|---|---|---|---|---|
| mos_tt/1.200V/27C | -160.0 | 133.1 | 333.0 | -199.9 |
| mos_tt/1.200V/27C | -80.0 | 129.4 | 248.7 | -119.3 |
| mos_tt/1.200V/27C | -40.0 | 129.6 | 200.3 | -70.7 |
| mos_tt/1.200V/27C | -20.0 | 131.6 | 167.7 | -36.1 |
| mos_tt/1.200V/27C | -10.0 | 133.8 | 151.5 | -17.7 |
| mos_tt/1.200V/27C | -5.0 | 135.5 | 145.5 | -10.0 |
| mos_tt/1.200V/27C | 0.0 | 138.2 | 141.7 | -3.6 |
| mos_tt/1.200V/27C | 5.0 | 142.4 | 139.6 | 2.8 |
| mos_tt/1.200V/27C | 10.0 | 148.8 | 138.2 | 10.5 |
| mos_tt/1.200V/27C | 20.0 | 164.5 | 136.7 | 27.7 |
| mos_tt/1.200V/27C | 40.0 | 193.0 | 135.5 | 57.5 |
| mos_tt/1.200V/27C | 80.0 | 241.5 | 136.2 | 105.3 |
| mos_tt/1.200V/27C | 160.0 | 329.8 | 138.6 | 191.2 |
| mos_ss/1.080V/125C | -160.0 | 220.4 | 429.0 | -208.6 |
| mos_ss/1.080V/125C | -80.0 | 218.1 | 336.0 | -117.9 |
| mos_ss/1.080V/125C | -40.0 | 221.0 | 280.6 | -59.6 |
| mos_ss/1.080V/125C | -20.0 | 223.5 | 250.3 | -26.8 |
| mos_ss/1.080V/125C | -10.0 | 225.4 | 240.1 | -14.7 |
| mos_ss/1.080V/125C | -5.0 | 226.7 | 237.0 | -10.2 |
| mos_ss/1.080V/125C | 0.0 | 228.5 | 234.9 | -6.4 |
| mos_ss/1.080V/125C | 5.0 | 231.0 | 233.4 | -2.5 |
| mos_ss/1.080V/125C | 10.0 | 234.5 | 232.5 | 2.1 |
| mos_ss/1.080V/125C | 20.0 | 245.5 | 231.1 | 14.4 |
| mos_ss/1.080V/125C | 40.0 | 274.7 | 229.5 | 45.2 |
| mos_ss/1.080V/125C | 80.0 | 324.6 | 228.1 | 96.5 |
| mos_ss/1.080V/125C | 160.0 | 421.1 | 230.6 | 190.5 |
| mos_ff/1.320V/-40C | -160.0 | 90.0 | 277.9 | -187.9 |
| mos_ff/1.320V/-40C | -80.0 | 90.1 | 196.9 | -106.9 |
| mos_ff/1.320V/-40C | -40.0 | 86.9 | 151.9 | -65.1 |
| mos_ff/1.320V/-40C | -20.0 | 87.9 | 125.8 | -37.9 |
| mos_ff/1.320V/-40C | -10.0 | 89.4 | 107.8 | -18.4 |
| mos_ff/1.320V/-40C | -5.0 | 90.9 | 100.2 | -9.2 |
| mos_ff/1.320V/-40C | 0.0 | 93.7 | 95.9 | -2.2 |
| mos_ff/1.320V/-40C | 5.0 | 98.4 | 93.7 | 4.7 |
| mos_ff/1.320V/-40C | 10.0 | 105.9 | 92.7 | 13.2 |
| mos_ff/1.320V/-40C | 20.0 | 121.9 | 91.7 | 30.2 |
| mos_ff/1.320V/-40C | 40.0 | 146.2 | 91.3 | 55.0 |
| mos_ff/1.320V/-40C | 80.0 | 192.9 | 93.5 | 99.4 |
| mos_ff/1.320V/-40C | 160.0 | 276.1 | 92.9 | 183.3 |

## ctl_1g

- engine: ngspice 47; backend/host: worker; remote job: klt-sim-69be85c983ed
- envelope status: pass

- `mos_tt/1.200V/27C`: **FAIL**; reset-pulse width 0..0 ps
  - C1 offset -160 ps: (wUP-wDN)/offset = -0.00
  - C1 offset -80 ps: (wUP-wDN)/offset = -0.00
  - C1 offset -40 ps: (wUP-wDN)/offset = -0.00
  - C1 offset -20 ps: (wUP-wDN)/offset = -0.00
  - C1 offset -10 ps: (wUP-wDN)/offset = -0.00
  - C1 offset 10 ps: (wUP-wDN)/offset = 0.00
  - C1 offset 20 ps: (wUP-wDN)/offset = 0.00
  - C1 offset 40 ps: (wUP-wDN)/offset = 0.00
  - C1 offset 80 ps: (wUP-wDN)/offset = 0.00
  - C1 offset 160 ps: (wUP-wDN)/offset = 0.00
  - C2 reset-pulse width 0..0 ps outside 30 ps..250 ps
- `mos_ss/1.080V/125C`: **FAIL**; reset-pulse width 0..235 ps
  - C3 cycle 1: unterminated pulse
  - C1 offset -160 ps: (wUP-wDN)/offset = -0.00
  - C1 offset -80 ps: (wUP-wDN)/offset = -0.00
  - C1 offset -40 ps: (wUP-wDN)/offset = -0.00
  - C1 offset -20 ps: (wUP-wDN)/offset = -0.00
  - C1 offset -10 ps: (wUP-wDN)/offset = -0.00
  - C1 offset 10 ps: (wUP-wDN)/offset = 0.00
  - C1 offset 20 ps: (wUP-wDN)/offset = 0.00
  - C1 offset 40 ps: (wUP-wDN)/offset = 0.00
  - C1 offset 80 ps: (wUP-wDN)/offset = 0.00
  - C1 offset 160 ps: (wUP-wDN)/offset = 0.00
  - C2 reset-pulse width 0..235 ps outside 30 ps..250 ps
- `mos_ff/1.320V/-40C`: **FAIL**; reset-pulse width 90..92 ps
  - C1 offset -160 ps: (wUP-wDN)/offset = 0.00
  - C1 offset -80 ps: (wUP-wDN)/offset = -0.00
  - C1 offset -40 ps: (wUP-wDN)/offset = -0.30
  - C1 offset -20 ps: (wUP-wDN)/offset = -5.35
  - C1 offset -10 ps: (wUP-wDN)/offset = -0.17
  - C1 offset 10 ps: (wUP-wDN)/offset = -12.07
  - C1 offset 20 ps: (wUP-wDN)/offset = -5.33
  - C1 offset 40 ps: (wUP-wDN)/offset = -0.23
  - C1 offset 80 ps: (wUP-wDN)/offset = -0.00
  - C1 offset 160 ps: (wUP-wDN)/offset = 0.02

| corner | offset ps | wUP ps | wDN ps | wUP-wDN ps |
|---|---|---|---|---|
| mos_tt/1.200V/27C | -160.0 | 0.0 | 0.0 | 0.0 |
| mos_tt/1.200V/27C | -80.0 | 0.0 | 0.0 | 0.0 |
| mos_tt/1.200V/27C | -40.0 | 0.0 | 0.0 | 0.0 |
| mos_tt/1.200V/27C | -20.0 | 0.0 | 0.0 | 0.0 |
| mos_tt/1.200V/27C | -10.0 | 0.0 | 0.0 | 0.0 |
| mos_tt/1.200V/27C | -5.0 | 0.0 | 0.0 | 0.0 |
| mos_tt/1.200V/27C | 0.0 | 0.0 | 0.0 | 0.0 |
| mos_tt/1.200V/27C | 5.0 | 0.0 | 0.0 | 0.0 |
| mos_tt/1.200V/27C | 10.0 | 0.0 | 0.0 | 0.0 |
| mos_tt/1.200V/27C | 20.0 | 0.0 | 0.0 | 0.0 |
| mos_tt/1.200V/27C | 40.0 | 0.0 | 0.0 | 0.0 |
| mos_tt/1.200V/27C | 80.0 | 0.0 | 0.0 | 0.0 |
| mos_tt/1.200V/27C | 160.0 | 0.0 | 0.0 | 0.0 |
| mos_ss/1.080V/125C | -160.0 | 0.0 | 0.0 | 0.0 |
| mos_ss/1.080V/125C | -80.0 | 0.0 | 0.0 | 0.0 |
| mos_ss/1.080V/125C | -40.0 | 0.0 | 0.0 | 0.0 |
| mos_ss/1.080V/125C | -20.0 | 0.0 | 0.0 | 0.0 |
| mos_ss/1.080V/125C | -10.0 | 0.0 | 0.0 | 0.0 |
| mos_ss/1.080V/125C | -5.0 | 0.0 | 0.0 | 0.0 |
| mos_ss/1.080V/125C | 0.0 | 0.0 | 0.0 | 0.0 |
| mos_ss/1.080V/125C | 5.0 | 0.0 | 0.0 | 0.0 |
| mos_ss/1.080V/125C | 10.0 | 0.0 | 0.0 | 0.0 |
| mos_ss/1.080V/125C | 20.0 | 0.0 | 0.0 | 0.0 |
| mos_ss/1.080V/125C | 40.0 | 0.0 | 0.0 | 0.0 |
| mos_ss/1.080V/125C | 80.0 | 0.0 | 0.0 | 0.0 |
| mos_ss/1.080V/125C | 160.0 | 0.0 | 0.0 | 0.0 |
| mos_ff/1.320V/-40C | -160.0 | 94.9 | 95.1 | -0.2 |
| mos_ff/1.320V/-40C | -80.0 | 94.5 | 94.4 | 0.1 |
| mos_ff/1.320V/-40C | -40.0 | 103.9 | 92.1 | 11.8 |
| mos_ff/1.320V/-40C | -20.0 | 198.4 | 91.3 | 107.1 |
| mos_ff/1.320V/-40C | -10.0 | 92.3 | 90.6 | 1.7 |
| mos_ff/1.320V/-40C | -5.0 | 93.3 | 92.7 | 0.5 |
| mos_ff/1.320V/-40C | 0.0 | 90.8 | 97.4 | -6.6 |
| mos_ff/1.320V/-40C | 5.0 | 89.5 | 214.9 | -125.4 |
| mos_ff/1.320V/-40C | 10.0 | 88.8 | 209.5 | -120.7 |
| mos_ff/1.320V/-40C | 20.0 | 88.0 | 194.7 | -106.7 |
| mos_ff/1.320V/-40C | 40.0 | 87.6 | 96.8 | -9.1 |
| mos_ff/1.320V/-40C | 80.0 | 94.3 | 94.5 | -0.3 |
| mos_ff/1.320V/-40C | 160.0 | 96.2 | 93.3 | 3.0 |

