# delay-sizing Monte Carlo matching record

SIMULATED, never measured. ss/1.08 V/125 C, 1 GHz, one Vc, mismatch-only Monte Carlo (`mos_ss_mismatch`); negative control on `mos_ss` (no mismatch) must give sigma exactly 0 and repeat identically.

## candidate A: n=32 runs, monte_carlo {"n": 32, "seed": 20261107, "vary": "mismatch", "family_mismatch": [{"family": "mosfet", "active": true, "note": "MOS per-instance mismatch is active: every selected process section is a *_mismatch section (mos_ss_mismatch), which includes the agauss() mismatch subcircuits (see docs/cli/sim.md's 'Known-good mismatch mechanisms')."}, {"family": "other", "active": null, "note": "mismatch activity for the 'other' family is not independently verified for PDK family 'sg13g2'; treat any sampled spread for it as unconfirmed."}, {"family": "capacitor", "active": null, "note": "mismatch activity for the 'capacitor' family is not independently verified for PDK family 'sg13g2'; treat any sampled spread for it as unconfirmed."}]}; job klt-sim-a511469c1d57

| tap k | mean step (ps) | sigma step (ps) | sigma / mean (%) | mean d_k (ps) | sigma d_k (ps) |
|---|---|---|---|---|---|
| 1 | 93.3 | 8.19 | 8.77 | 93.3 | 8.19 |
| 2 | 99.1 | 14.46 | 14.59 | 192.4 | 13.53 |
| 3 | 80.0 | 15.08 | 18.86 | 272.4 | 11.52 |
| 4 | 94.4 | 12.29 | 13.03 | 366.7 | 13.77 |
| 5 | 78.1 | 12.00 | 15.36 | 444.9 | 12.53 |
| 6 | 96.0 | 12.68 | 13.21 | 540.9 | 18.06 |
| 7 | 78.3 | 13.62 | 17.40 | 619.2 | 12.25 |
| 8 | 96.2 | 11.38 | 11.82 | 715.4 | 15.32 |

Worst per-tap step sigma/mean: 18.86 %. Per-sample max |step - line-mean step| (rising input): mean 26.10 ps, max 49.79 ps (n=32). Note: for A the rising-input steps alternate fall/rise outputs, so this includes the systematic tpHL/tpLH step alternation.

Negative control (`mos_ss`, same seed/n): 32 runs, sigma exactly 0 across samples: **True**; repeat run identical: **True**.

## candidate B: n=32 runs, monte_carlo {"n": 32, "seed": 20261107, "vary": "mismatch", "family_mismatch": [{"family": "mosfet", "active": true, "note": "MOS per-instance mismatch is active: every selected process section is a *_mismatch section (mos_ss_mismatch), which includes the agauss() mismatch subcircuits (see docs/cli/sim.md's 'Known-good mismatch mechanisms')."}, {"family": "other", "active": null, "note": "mismatch activity for the 'other' family is not independently verified for PDK family 'sg13g2'; treat any sampled spread for it as unconfirmed."}, {"family": "capacitor", "active": null, "note": "mismatch activity for the 'capacitor' family is not independently verified for PDK family 'sg13g2'; treat any sampled spread for it as unconfirmed."}]}; job klt-sim-5a1c68e9772a

| tap k | mean step (ps) | sigma step (ps) | sigma / mean (%) | mean d_k (ps) | sigma d_k (ps) |
|---|---|---|---|---|---|
| 1 | 121.1 | 16.98 | 14.01 | 121.1 | 16.98 |
| 2 | 119.0 | 13.10 | 11.00 | 240.2 | 16.18 |
| 3 | 113.6 | 12.94 | 11.39 | 353.8 | 18.48 |
| 4 | 117.3 | 12.55 | 10.70 | 471.1 | 17.73 |
| 5 | 116.2 | 16.86 | 14.51 | 587.3 | 19.32 |
| 6 | 114.5 | 16.28 | 14.21 | 701.8 | 18.63 |
| 7 | 118.3 | 15.58 | 13.17 | 820.1 | 17.51 |
| 8 | 117.4 | 12.79 | 10.89 | 937.4 | 19.29 |

Worst per-tap step sigma/mean: 14.51 %. Per-sample max |step - line-mean step| (rising input): mean 25.08 ps, max 45.16 ps (n=32). 

Negative control (`mos_ss`, same seed/n): 32 runs, sigma exactly 0 across samples: **True**; repeat run identical: **True**.

## Run status

no diagnostics / errors
