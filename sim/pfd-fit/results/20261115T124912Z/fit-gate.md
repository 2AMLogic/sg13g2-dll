# PFD fit-gate record (decision 0006)

Simulated, never measured. Criteria C1-C3 are in `sim/pfd-fit/grade.py`.

## pfd_1g

- engine: ngspice 47; backend/host: worker; remote job: klt-sim-3f16b4237455
- envelope status: pass

- `mos_tt/1.200V/27C`: **PASS**; reset-pulse width 229..233 ps
- `mos_ss/1.080V/125C`: **FAIL**; reset-pulse width 362..370 ps
  - C2 reset-pulse width 362..370 ps outside 30 ps..250 ps
- `mos_ff/1.320V/-40C`: **PASS**; reset-pulse width 154..157 ps

| corner | offset ps | wUP ps | wDN ps | wUP-wDN ps |
|---|---|---|---|---|
| mos_tt/1.200V/27C | -160.0 | 213.9 | 376.5 | -162.7 |
| mos_tt/1.200V/27C | -80.0 | 215.4 | 297.6 | -82.3 |
| mos_tt/1.200V/27C | -40.0 | 218.6 | 260.1 | -41.5 |
| mos_tt/1.200V/27C | -20.0 | 221.7 | 242.7 | -20.9 |
| mos_tt/1.200V/27C | -10.0 | 224.5 | 234.9 | -10.4 |
| mos_tt/1.200V/27C | -5.0 | 226.5 | 231.6 | -5.1 |
| mos_tt/1.200V/27C | 0.0 | 228.8 | 228.8 | 0.1 |
| mos_tt/1.200V/27C | 5.0 | 231.9 | 226.6 | 5.3 |
| mos_tt/1.200V/27C | 10.0 | 235.2 | 224.8 | 10.4 |
| mos_tt/1.200V/27C | 20.0 | 242.9 | 222.4 | 20.5 |
| mos_tt/1.200V/27C | 40.0 | 259.8 | 218.9 | 40.9 |
| mos_tt/1.200V/27C | 80.0 | 297.8 | 216.1 | 81.7 |
| mos_tt/1.200V/27C | 160.0 | 378.1 | 215.9 | 162.2 |
| mos_ss/1.080V/125C | -160.0 | 338.7 | 502.4 | -163.7 |
| mos_ss/1.080V/125C | -80.0 | 343.4 | 426.1 | -82.6 |
| mos_ss/1.080V/125C | -40.0 | 349.0 | 390.6 | -41.5 |
| mos_ss/1.080V/125C | -20.0 | 353.8 | 374.6 | -20.8 |
| mos_ss/1.080V/125C | -10.0 | 357.4 | 367.7 | -10.3 |
| mos_ss/1.080V/125C | -5.0 | 359.6 | 364.7 | -5.1 |
| mos_ss/1.080V/125C | 0.0 | 362.1 | 362.1 | 0.0 |
| mos_ss/1.080V/125C | 5.0 | 365.0 | 359.9 | 5.1 |
| mos_ss/1.080V/125C | 10.0 | 368.1 | 357.9 | 10.2 |
| mos_ss/1.080V/125C | 20.0 | 375.3 | 354.9 | 20.4 |
| mos_ss/1.080V/125C | 40.0 | 391.2 | 350.6 | 40.6 |
| mos_ss/1.080V/125C | 80.0 | 426.2 | 344.9 | 81.3 |
| mos_ss/1.080V/125C | 160.0 | 505.0 | 342.4 | 162.6 |
| mos_ff/1.320V/-40C | -160.0 | 144.3 | 306.4 | -162.0 |
| mos_ff/1.320V/-40C | -80.0 | 144.6 | 226.5 | -81.8 |
| mos_ff/1.320V/-40C | -40.0 | 146.4 | 187.8 | -41.5 |
| mos_ff/1.320V/-40C | -20.0 | 148.5 | 169.5 | -21.0 |
| mos_ff/1.320V/-40C | -10.0 | 150.5 | 160.9 | -10.5 |
| mos_ff/1.320V/-40C | -5.0 | 152.1 | 157.2 | -5.2 |
| mos_ff/1.320V/-40C | 0.0 | 154.4 | 154.3 | 0.1 |
| mos_ff/1.320V/-40C | 5.0 | 157.4 | 152.1 | 5.3 |
| mos_ff/1.320V/-40C | 10.0 | 161.1 | 150.7 | 10.4 |
| mos_ff/1.320V/-40C | 20.0 | 169.3 | 148.6 | 20.7 |
| mos_ff/1.320V/-40C | 40.0 | 187.2 | 146.0 | 41.2 |
| mos_ff/1.320V/-40C | 80.0 | 226.5 | 144.8 | 81.7 |
| mos_ff/1.320V/-40C | 160.0 | 307.2 | 145.2 | 162.0 |

## pfd_500m

- engine: ngspice 47; backend/host: worker; remote job: klt-sim-b447e41afeff
- envelope status: pass

- `mos_tt/1.200V/27C`: **PASS**; reset-pulse width 229..233 ps
- `mos_ss/1.080V/125C`: **PASS**; reset-pulse width 363..370 ps
- `mos_ff/1.320V/-40C`: **PASS**; reset-pulse width 154..157 ps

| corner | offset ps | wUP ps | wDN ps | wUP-wDN ps |
|---|---|---|---|---|
| mos_tt/1.200V/27C | -160.0 | 214.0 | 376.6 | -162.7 |
| mos_tt/1.200V/27C | -80.0 | 215.5 | 297.8 | -82.3 |
| mos_tt/1.200V/27C | -40.0 | 218.8 | 260.3 | -41.5 |
| mos_tt/1.200V/27C | -20.0 | 222.0 | 242.9 | -20.9 |
| mos_tt/1.200V/27C | -10.0 | 224.8 | 235.3 | -10.5 |
| mos_tt/1.200V/27C | -5.0 | 226.9 | 232.0 | -5.1 |
| mos_tt/1.200V/27C | 0.0 | 229.3 | 229.2 | 0.1 |
| mos_tt/1.200V/27C | 5.0 | 232.3 | 227.0 | 5.3 |
| mos_tt/1.200V/27C | 10.0 | 235.7 | 225.3 | 10.4 |
| mos_tt/1.200V/27C | 20.0 | 243.3 | 222.7 | 20.5 |
| mos_tt/1.200V/27C | 40.0 | 260.1 | 219.2 | 40.9 |
| mos_tt/1.200V/27C | 80.0 | 297.9 | 216.2 | 81.7 |
| mos_tt/1.200V/27C | 160.0 | 378.2 | 216.0 | 162.2 |
| mos_ss/1.080V/125C | -160.0 | 339.1 | 502.7 | -163.6 |
| mos_ss/1.080V/125C | -80.0 | 344.0 | 426.7 | -82.6 |
| mos_ss/1.080V/125C | -40.0 | 349.8 | 391.3 | -41.6 |
| mos_ss/1.080V/125C | -20.0 | 354.7 | 375.5 | -20.8 |
| mos_ss/1.080V/125C | -10.0 | 358.4 | 368.7 | -10.3 |
| mos_ss/1.080V/125C | -5.0 | 360.7 | 365.9 | -5.2 |
| mos_ss/1.080V/125C | 0.0 | 363.3 | 363.3 | 0.0 |
| mos_ss/1.080V/125C | 5.0 | 366.2 | 361.1 | 5.1 |
| mos_ss/1.080V/125C | 10.0 | 369.4 | 359.1 | 10.2 |
| mos_ss/1.080V/125C | 20.0 | 376.4 | 356.0 | 20.4 |
| mos_ss/1.080V/125C | 40.0 | 392.2 | 351.6 | 40.6 |
| mos_ss/1.080V/125C | 80.0 | 426.8 | 345.4 | 81.3 |
| mos_ss/1.080V/125C | 160.0 | 505.3 | 342.7 | 162.6 |
| mos_ff/1.320V/-40C | -160.0 | 144.4 | 306.4 | -162.0 |
| mos_ff/1.320V/-40C | -80.0 | 144.7 | 226.5 | -81.8 |
| mos_ff/1.320V/-40C | -40.0 | 146.4 | 187.9 | -41.5 |
| mos_ff/1.320V/-40C | -20.0 | 148.6 | 169.6 | -21.0 |
| mos_ff/1.320V/-40C | -10.0 | 150.6 | 161.1 | -10.5 |
| mos_ff/1.320V/-40C | -5.0 | 152.2 | 157.4 | -5.2 |
| mos_ff/1.320V/-40C | 0.0 | 154.6 | 154.5 | 0.1 |
| mos_ff/1.320V/-40C | 5.0 | 157.6 | 152.3 | 5.3 |
| mos_ff/1.320V/-40C | 10.0 | 161.3 | 150.9 | 10.4 |
| mos_ff/1.320V/-40C | 20.0 | 169.5 | 148.8 | 20.7 |
| mos_ff/1.320V/-40C | 40.0 | 187.2 | 146.0 | 41.2 |
| mos_ff/1.320V/-40C | 80.0 | 226.6 | 144.9 | 81.7 |
| mos_ff/1.320V/-40C | 160.0 | 307.2 | 145.3 | 162.0 |

## ctl_1g

- engine: ngspice 47; backend/host: worker; remote job: klt-sim-8f492193fe10
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
- `mos_ss/1.080V/125C`: **FAIL**; reset-pulse width 142..143 ps
  - C1 offset -160 ps: (wUP-wDN)/offset = 0.01
  - C1 offset -80 ps: (wUP-wDN)/offset = 0.01
  - C1 offset -40 ps: (wUP-wDN)/offset = 0.03
  - C1 offset -20 ps: (wUP-wDN)/offset = 0.06
  - C1 offset -10 ps: (wUP-wDN)/offset = 0.12
  - C1 offset 10 ps: (wUP-wDN)/offset = -0.19
  - C1 offset 20 ps: (wUP-wDN)/offset = -0.12
  - C1 offset 40 ps: (wUP-wDN)/offset = -0.08
  - C1 offset 80 ps: (wUP-wDN)/offset = -0.04
  - C1 offset 160 ps: (wUP-wDN)/offset = 0.01
- `mos_ff/1.320V/-40C`: **FAIL**; reset-pulse width 0..0 ps
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
| mos_ss/1.080V/125C | -160.0 | 145.1 | 145.9 | -0.8 |
| mos_ss/1.080V/125C | -80.0 | 144.7 | 145.3 | -0.6 |
| mos_ss/1.080V/125C | -40.0 | 143.5 | 144.6 | -1.2 |
| mos_ss/1.080V/125C | -20.0 | 143.4 | 144.5 | -1.2 |
| mos_ss/1.080V/125C | -10.0 | 143.3 | 144.6 | -1.2 |
| mos_ss/1.080V/125C | -5.0 | 143.3 | 144.6 | -1.3 |
| mos_ss/1.080V/125C | 0.0 | 143.2 | 144.6 | -1.5 |
| mos_ss/1.080V/125C | 5.0 | 143.1 | 144.8 | -1.7 |
| mos_ss/1.080V/125C | 10.0 | 143.0 | 144.9 | -1.9 |
| mos_ss/1.080V/125C | 20.0 | 142.8 | 145.2 | -2.4 |
| mos_ss/1.080V/125C | 40.0 | 142.8 | 146.0 | -3.3 |
| mos_ss/1.080V/125C | 80.0 | 143.8 | 146.7 | -2.8 |
| mos_ss/1.080V/125C | 160.0 | 146.2 | 144.7 | 1.5 |
| mos_ff/1.320V/-40C | -160.0 | 0.0 | 0.0 | 0.0 |
| mos_ff/1.320V/-40C | -80.0 | 0.0 | 0.0 | 0.0 |
| mos_ff/1.320V/-40C | -40.0 | 0.0 | 0.0 | 0.0 |
| mos_ff/1.320V/-40C | -20.0 | 0.0 | 0.0 | 0.0 |
| mos_ff/1.320V/-40C | -10.0 | 0.0 | 0.0 | 0.0 |
| mos_ff/1.320V/-40C | -5.0 | 0.0 | 0.0 | 0.0 |
| mos_ff/1.320V/-40C | 0.0 | 0.0 | 0.0 | 0.0 |
| mos_ff/1.320V/-40C | 5.0 | 0.0 | 0.0 | 0.0 |
| mos_ff/1.320V/-40C | 10.0 | 0.0 | 0.0 | 0.0 |
| mos_ff/1.320V/-40C | 20.0 | 0.0 | 0.0 | 0.0 |
| mos_ff/1.320V/-40C | 40.0 | 0.0 | 0.0 | 0.0 |
| mos_ff/1.320V/-40C | 80.0 | 0.0 | 0.0 | 0.0 |
| mos_ff/1.320V/-40C | 160.0 | 0.0 | 0.0 | 0.0 |

