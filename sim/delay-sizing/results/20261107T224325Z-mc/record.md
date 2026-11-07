# delay-sizing Monte Carlo matching record

SIMULATED, never measured. ss/1.08 V/125 C, 1 GHz, one Vc, mismatch-only Monte Carlo (`mos_ss_mismatch`); negative control on `mos_ss` (no mismatch) must give sigma exactly 0 and repeat identically.

## candidate A: n=32 runs, monte_carlo {"n": 32, "seed": 20261107, "vary": "mismatch", "family_mismatch": [{"family": "mosfet", "active": true, "note": "MOS per-instance mismatch is active: every selected process section is a *_mismatch section (mos_ss_mismatch), which includes the agauss() mismatch subcircuits (see docs/cli/sim.md's 'Known-good mismatch mechanisms')."}, {"family": "other", "active": null, "note": "mismatch activity for the 'other' family is not independently verified for PDK family 'sg13g2'; treat any sampled spread for it as unconfirmed."}, {"family": "capacitor", "active": null, "note": "mismatch activity for the 'capacitor' family is not independently verified for PDK family 'sg13g2'; treat any sampled spread for it as unconfirmed."}]}; job klt-sim-e60ddbd02ed4

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

## candidate B: n=32 runs, monte_carlo {"n": 32, "seed": 20261107, "vary": "mismatch", "family_mismatch": [{"family": "mosfet", "active": true, "note": "MOS per-instance mismatch is active: every selected process section is a *_mismatch section (mos_ss_mismatch), which includes the agauss() mismatch subcircuits (see docs/cli/sim.md's 'Known-good mismatch mechanisms')."}, {"family": "other", "active": null, "note": "mismatch activity for the 'other' family is not independently verified for PDK family 'sg13g2'; treat any sampled spread for it as unconfirmed."}, {"family": "capacitor", "active": null, "note": "mismatch activity for the 'capacitor' family is not independently verified for PDK family 'sg13g2'; treat any sampled spread for it as unconfirmed."}]}; job klt-sim-dcda051c57bd

| tap k | mean step (ps) | sigma step (ps) | sigma / mean (%) | mean d_k (ps) | sigma d_k (ps) |
|---|---|---|---|---|---|
| 1 | 115.4 | 16.90 | 14.65 | 115.4 | 16.90 |
| 2 | 114.1 | 12.93 | 11.33 | 229.5 | 16.10 |
| 3 | 108.7 | 12.80 | 11.77 | 338.2 | 18.37 |
| 4 | 112.4 | 12.45 | 11.08 | 450.7 | 17.58 |
| 5 | 111.3 | 16.76 | 15.05 | 562.0 | 19.19 |
| 6 | 109.7 | 16.15 | 14.72 | 671.7 | 18.49 |
| 7 | 113.3 | 15.42 | 13.61 | 785.0 | 17.41 |
| 8 | 112.4 | 12.64 | 11.24 | 897.5 | 19.11 |

Worst per-tap step sigma/mean: 15.05 %. Per-sample max |step - line-mean step| (rising input): mean 24.82 ps, max 44.89 ps (n=32). 

Negative control (`mos_ss`, same seed/n): 32 runs, sigma exactly 0 across samples: **True**; repeat run identical: **True**.

## Run status

no diagnostics / errors
