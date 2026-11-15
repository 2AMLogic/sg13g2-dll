# PFD fit-gate record (decision 0006)

Simulated, never measured. Criteria C1-C3 are in `sim/pfd-fit/grade.py`.

## pfd_1g

- engine: ngspice 47; backend/host: worker; remote job: klt-sim-42d4f35cd4e9
- envelope status: pass

- `mos_tt/1.200V/27C`: **PASS**; reset-pulse width 223..226 ps
- `mos_ss/1.080V/125C`: **FAIL**; reset-pulse width 352..358 ps
  - C2 reset-pulse width 352..358 ps outside 30 ps..250 ps
- `mos_ff/1.320V/-40C`: **PASS**; reset-pulse width 150..152 ps

| corner | offset ps | wUP ps | wDN ps | wUP-wDN ps |
|---|---|---|---|---|
| mos_tt/1.200V/27C | -160.0 | 209.6 | 375.0 | -165.3 |
| mos_tt/1.200V/27C | -80.0 | 210.1 | 294.9 | -84.8 |
| mos_tt/1.200V/27C | -40.0 | 212.3 | 255.7 | -43.4 |
| mos_tt/1.200V/27C | -20.0 | 215.8 | 237.9 | -22.0 |
| mos_tt/1.200V/27C | -10.0 | 219.0 | 230.1 | -11.0 |
| mos_tt/1.200V/27C | -5.0 | 221.1 | 226.5 | -5.4 |
| mos_tt/1.200V/27C | 0.0 | 223.5 | 223.5 | 0.1 |
| mos_tt/1.200V/27C | 5.0 | 226.4 | 220.8 | 5.5 |
| mos_tt/1.200V/27C | 10.0 | 229.5 | 218.6 | 10.9 |
| mos_tt/1.200V/27C | 20.0 | 236.7 | 215.2 | 21.4 |
| mos_tt/1.200V/27C | 40.0 | 253.9 | 211.7 | 42.2 |
| mos_tt/1.200V/27C | 80.0 | 295.2 | 212.3 | 82.9 |
| mos_tt/1.200V/27C | 160.0 | 377.7 | 213.7 | 164.0 |
| mos_ss/1.080V/125C | -160.0 | 331.2 | 499.1 | -167.9 |
| mos_ss/1.080V/125C | -80.0 | 333.2 | 419.1 | -85.9 |
| mos_ss/1.080V/125C | -40.0 | 338.4 | 382.3 | -43.9 |
| mos_ss/1.080V/125C | -20.0 | 343.9 | 366.0 | -22.1 |
| mos_ss/1.080V/125C | -10.0 | 347.8 | 358.8 | -11.0 |
| mos_ss/1.080V/125C | -5.0 | 350.1 | 355.6 | -5.5 |
| mos_ss/1.080V/125C | 0.0 | 352.6 | 352.7 | -0.1 |
| mos_ss/1.080V/125C | 5.0 | 355.4 | 350.1 | 5.3 |
| mos_ss/1.080V/125C | 10.0 | 358.4 | 347.7 | 10.7 |
| mos_ss/1.080V/125C | 20.0 | 365.2 | 343.8 | 21.4 |
| mos_ss/1.080V/125C | 40.0 | 380.8 | 338.5 | 42.3 |
| mos_ss/1.080V/125C | 80.0 | 418.5 | 335.4 | 83.2 |
| mos_ss/1.080V/125C | 160.0 | 502.9 | 338.3 | 164.6 |
| mos_ff/1.320V/-40C | -160.0 | 141.1 | 304.9 | -163.8 |
| mos_ff/1.320V/-40C | -80.0 | 141.2 | 224.8 | -83.6 |
| mos_ff/1.320V/-40C | -40.0 | 142.0 | 185.0 | -43.0 |
| mos_ff/1.320V/-40C | -20.0 | 144.0 | 166.0 | -22.0 |
| mos_ff/1.320V/-40C | -10.0 | 146.3 | 157.4 | -11.1 |
| mos_ff/1.320V/-40C | -5.0 | 148.2 | 153.7 | -5.4 |
| mos_ff/1.320V/-40C | 0.0 | 150.5 | 150.3 | 0.2 |
| mos_ff/1.320V/-40C | 5.0 | 153.5 | 147.8 | 5.7 |
| mos_ff/1.320V/-40C | 10.0 | 156.7 | 145.7 | 11.1 |
| mos_ff/1.320V/-40C | 20.0 | 164.6 | 143.0 | 21.7 |
| mos_ff/1.320V/-40C | 40.0 | 183.9 | 141.7 | 42.2 |
| mos_ff/1.320V/-40C | 80.0 | 225.7 | 142.8 | 82.9 |
| mos_ff/1.320V/-40C | 160.0 | 306.7 | 143.3 | 163.4 |

## pfd_500m

- engine: ngspice 47; backend/host: worker; remote job: klt-sim-1934c6f376e3
- envelope status: pass

- `mos_tt/1.200V/27C`: **PASS**; reset-pulse width 224..226 ps
- `mos_ss/1.080V/125C`: **PASS**; reset-pulse width 353..358 ps
- `mos_ff/1.320V/-40C`: **PASS**; reset-pulse width 150..152 ps

| corner | offset ps | wUP ps | wDN ps | wUP-wDN ps |
|---|---|---|---|---|
| mos_tt/1.200V/27C | -160.0 | 209.6 | 374.9 | -165.3 |
| mos_tt/1.200V/27C | -80.0 | 210.1 | 294.9 | -84.8 |
| mos_tt/1.200V/27C | -40.0 | 212.3 | 255.7 | -43.4 |
| mos_tt/1.200V/27C | -20.0 | 215.9 | 238.0 | -22.1 |
| mos_tt/1.200V/27C | -10.0 | 219.2 | 230.2 | -11.1 |
| mos_tt/1.200V/27C | -5.0 | 221.3 | 226.8 | -5.4 |
| mos_tt/1.200V/27C | 0.0 | 223.8 | 223.7 | 0.1 |
| mos_tt/1.200V/27C | 5.0 | 226.6 | 221.1 | 5.6 |
| mos_tt/1.200V/27C | 10.0 | 229.8 | 218.8 | 10.9 |
| mos_tt/1.200V/27C | 20.0 | 236.9 | 215.4 | 21.5 |
| mos_tt/1.200V/27C | 40.0 | 254.0 | 211.8 | 42.3 |
| mos_tt/1.200V/27C | 80.0 | 295.2 | 212.3 | 82.9 |
| mos_tt/1.200V/27C | 160.0 | 377.7 | 213.7 | 164.0 |
| mos_ss/1.080V/125C | -160.0 | 331.3 | 499.1 | -167.8 |
| mos_ss/1.080V/125C | -80.0 | 333.3 | 419.3 | -86.0 |
| mos_ss/1.080V/125C | -40.0 | 338.6 | 382.5 | -44.0 |
| mos_ss/1.080V/125C | -20.0 | 344.3 | 366.4 | -22.2 |
| mos_ss/1.080V/125C | -10.0 | 348.3 | 359.4 | -11.0 |
| mos_ss/1.080V/125C | -5.0 | 350.7 | 356.2 | -5.5 |
| mos_ss/1.080V/125C | 0.0 | 353.3 | 353.3 | -0.1 |
| mos_ss/1.080V/125C | 5.0 | 356.1 | 350.7 | 5.4 |
| mos_ss/1.080V/125C | 10.0 | 359.1 | 348.3 | 10.7 |
| mos_ss/1.080V/125C | 20.0 | 365.8 | 344.4 | 21.4 |
| mos_ss/1.080V/125C | 40.0 | 381.2 | 338.9 | 42.4 |
| mos_ss/1.080V/125C | 80.0 | 418.8 | 335.5 | 83.3 |
| mos_ss/1.080V/125C | 160.0 | 503.0 | 338.4 | 164.6 |
| mos_ff/1.320V/-40C | -160.0 | 141.1 | 304.9 | -163.8 |
| mos_ff/1.320V/-40C | -80.0 | 141.2 | 224.8 | -83.6 |
| mos_ff/1.320V/-40C | -40.0 | 142.0 | 185.0 | -43.0 |
| mos_ff/1.320V/-40C | -20.0 | 144.0 | 166.0 | -22.0 |
| mos_ff/1.320V/-40C | -10.0 | 146.3 | 157.5 | -11.1 |
| mos_ff/1.320V/-40C | -5.0 | 148.3 | 153.7 | -5.5 |
| mos_ff/1.320V/-40C | 0.0 | 150.6 | 150.4 | 0.2 |
| mos_ff/1.320V/-40C | 5.0 | 153.6 | 147.9 | 5.7 |
| mos_ff/1.320V/-40C | 10.0 | 156.8 | 145.8 | 11.1 |
| mos_ff/1.320V/-40C | 20.0 | 164.7 | 143.0 | 21.7 |
| mos_ff/1.320V/-40C | 40.0 | 183.9 | 141.7 | 42.2 |
| mos_ff/1.320V/-40C | 80.0 | 225.7 | 142.8 | 82.9 |
| mos_ff/1.320V/-40C | 160.0 | 306.7 | 143.3 | 163.4 |

## ctl_1g

- engine: ngspice 47; backend/host: worker; remote job: klt-sim-0f13684829b1
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
- `mos_ss/1.080V/125C`: **FAIL**; reset-pulse width 222..223 ps
  - C1 offset -160 ps: (wUP-wDN)/offset = 0.01
  - C1 offset -80 ps: (wUP-wDN)/offset = -0.05
  - C1 offset -40 ps: (wUP-wDN)/offset = 0.00
  - C1 offset -20 ps: (wUP-wDN)/offset = 0.06
  - C1 offset -10 ps: (wUP-wDN)/offset = 0.18
  - C1 offset 10 ps: (wUP-wDN)/offset = -0.34
  - C1 offset 20 ps: (wUP-wDN)/offset = -0.24
  - C1 offset 40 ps: (wUP-wDN)/offset = -0.19
  - C1 offset 80 ps: (wUP-wDN)/offset = -0.15
  - C1 offset 160 ps: (wUP-wDN)/offset = -0.04
- `mos_ff/1.320V/-40C`: **FAIL**; reset-pulse width 94..95 ps
  - C1 offset -160 ps: (wUP-wDN)/offset = 0.00
  - C1 offset -80 ps: (wUP-wDN)/offset = 0.01
  - C1 offset -40 ps: (wUP-wDN)/offset = -0.05
  - C1 offset -20 ps: (wUP-wDN)/offset = -0.04
  - C1 offset -10 ps: (wUP-wDN)/offset = 0.03
  - C1 offset 10 ps: (wUP-wDN)/offset = -0.23
  - C1 offset 20 ps: (wUP-wDN)/offset = -0.19
  - C1 offset 40 ps: (wUP-wDN)/offset = -0.12
  - C1 offset 80 ps: (wUP-wDN)/offset = -0.02
  - C1 offset 160 ps: (wUP-wDN)/offset = 0.00

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
| mos_ss/1.080V/125C | -160.0 | 225.2 | 226.4 | -1.2 |
| mos_ss/1.080V/125C | -80.0 | 227.3 | 223.6 | 3.7 |
| mos_ss/1.080V/125C | -40.0 | 223.0 | 223.1 | -0.0 |
| mos_ss/1.080V/125C | -20.0 | 222.8 | 224.1 | -1.2 |
| mos_ss/1.080V/125C | -10.0 | 222.9 | 224.7 | -1.8 |
| mos_ss/1.080V/125C | -5.0 | 222.8 | 224.9 | -2.1 |
| mos_ss/1.080V/125C | 0.0 | 222.7 | 225.1 | -2.5 |
| mos_ss/1.080V/125C | 5.0 | 222.5 | 225.4 | -2.9 |
| mos_ss/1.080V/125C | 10.0 | 222.2 | 225.6 | -3.4 |
| mos_ss/1.080V/125C | 20.0 | 221.4 | 226.1 | -4.7 |
| mos_ss/1.080V/125C | 40.0 | 219.8 | 227.3 | -7.5 |
| mos_ss/1.080V/125C | 80.0 | 217.9 | 229.5 | -11.6 |
| mos_ss/1.080V/125C | 160.0 | 221.4 | 227.3 | -5.9 |
| mos_ff/1.320V/-40C | -160.0 | 95.5 | 96.0 | -0.5 |
| mos_ff/1.320V/-40C | -80.0 | 95.2 | 96.3 | -1.1 |
| mos_ff/1.320V/-40C | -40.0 | 97.0 | 95.0 | 2.0 |
| mos_ff/1.320V/-40C | -20.0 | 95.3 | 94.5 | 0.7 |
| mos_ff/1.320V/-40C | -10.0 | 94.6 | 94.9 | -0.3 |
| mos_ff/1.320V/-40C | -5.0 | 94.6 | 95.2 | -0.6 |
| mos_ff/1.320V/-40C | 0.0 | 94.4 | 95.5 | -1.1 |
| mos_ff/1.320V/-40C | 5.0 | 94.2 | 95.8 | -1.6 |
| mos_ff/1.320V/-40C | 10.0 | 93.8 | 96.1 | -2.3 |
| mos_ff/1.320V/-40C | 20.0 | 93.1 | 96.8 | -3.7 |
| mos_ff/1.320V/-40C | 40.0 | 92.3 | 97.1 | -4.8 |
| mos_ff/1.320V/-40C | 80.0 | 94.7 | 96.1 | -1.3 |
| mos_ff/1.320V/-40C | 160.0 | 95.9 | 95.7 | 0.1 |

