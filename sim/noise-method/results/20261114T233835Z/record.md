# noise-method record

SIMULATED results, never measured. Validates spec/decisions/0014 on the known case
(one minimum sg13_lv inverter, DC-biased at its switching threshold, mos_tt/1.20 V/27 C).
No DLL jitter figure is produced here (0014; row 6 stays blocked).

- Verdict: **FAIL**
- Stamp: 20261114T233835Z (UTC 2026-11-14T23:40:39Z)
- klt: 0.9.2.dev1029+g76f47afa48f1; engine: ngspice 47; backend: local
- OSDI models (sha256, first 16): `psp103.osdi` 2e4299c4683997e2…; `psp103_nqs.osdi` 839b164483205601…; `r3_cmc.osdi` 4fead17bc2e9cbfe…; `mosvar.osdi` 25e64a374ab523db…
- PDK: IHP-Open-PDK v0.3.0 (sim/pdk.json)

## Method (from 0014)

- Noise representation: thermal noise of the known case's devices as ONE white
  input-referred series voltage `trnoise` source, derived from `.noise` at the OP
  (`onoise` band integral over 1 MHz-300 GHz), placed between the input node and the
  stage. Flicker excluded (thermal-noise class, spec row 6).
- ENBW identity: `ENBW = (sigma_R^2 - sigma_v^2)/(4 k T R)`, R = 1 MOhm series,
  T = 300.15 K; no manual spectral quadrature.
- Equivalent density: `NA = sigma_v/(sqrt(2/3)*sqrt(ENBW))` (ngspice trnoise
  piecewise-linear interpolation: process rms = NA*sqrt(2/3), measured 0.818 vs 0.8165).
- Timing figure: `sigma_t = sigma_v / SR`; SR from a noiseless edge transient
  (0.1 V between the 0.65/0.55 V crossings of a falling edge).
- Seeds: 8 independent runs, sequential fresh ngspice processes on one host;
  seed values are NOT recordable on this toolchain (pid-seeded streams; three pinning
  mechanisms probed and refused; 0014 and klayout-tools#5772). Re-running redraws noise.
- Run length: 90 ns per seeded run, trnoise step NT = 1 ps; estimator window 5-90 ns
  (85 000 breakpoints).
- Estimator: `sigma = sqrt(vrms^2 - vavg^2)` from two plain `.meas tran` cards
  (AVG and RMS of v(out)); no hand-rolled waveform arithmetic.
- Expected values and tolerances were fixed in 0014 BEFORE this run; derivation
  quantities re-derived by this stamp must agree within the 0014 reproduction tolerances.

## Derivation (this stamp; deterministic analyses)

| quantity | value | 0014 expected | agreement |
|---|---|---|---|
| switching threshold vth | 5.702580e-01 V | 5.702580e-01 | 0.00e+00 (0.1 %) |
| OP output level (control vavg) | 6.003190e-01 V | 6.003190e-01 | 0.00e+00 (0.1 %) |
| sigma_v (onoise, 1 MHz-300 GHz) | 7.916701e-03 V | 7.916701e-03 | 0.00e+00 (1 %) |
| inoise band integral | 4.500722e-03 V | 4.500722e-03 | 0.00e+00 (1 %) |
| density at 10 MHz | 7.255526e-07 V/sqrt(Hz) | 7.255500e-07 | 3.58e-06 (1 %) |
| density at 1 GHz | 7.915051e-08 V/sqrt(Hz) | 7.915100e-08 | 6.19e-06 (1 %) |
| density at 100 GHz | 8.253511e-10 V/sqrt(Hz) | 8.253500e-10 | 1.33e-06 (1 %) |
| sigma_R (1 MOhm series R) | 2.016996e-02 V | 2.016996e-02 | 0.00e+00 (1 %) |
| ENBW | 2.076204e+10 Hz | 2.076204e+10 | 1.86e-07 (1 %) |
| gain A0 at 1 MHz | 2.574722e+01 V/V | 2.574720e+01 | 9.22e-07 (2 %) |
| equivalent density NA | 6.729066e-08 V/sqrt(Hz) | 6.729066e-08 | 7.41e-08 (2 %) |
| slew rate SR (edge 2) | 3.115265e+10 V/s | 3.115265e+10 | 6.50e-08 (1 %) |
| slew rate SR (edge 3) | 3.115265e+10 V/s | 3.115265e+10 | 6.50e-08 (1 %) |
| derived sigma_t = sigma_v/SR | 2.541261e-13 s | 2.541261e-13 | 8.26e-09 (1 %) |

## Control run (AC: OSDI models contribute no noise by themselves)

- No `trnoise` source declared: recovered output rms `sqrt(vrms^2-vavg^2)` = 0.000e+00 V
  (must be 0; an ngspice transient carries only declared noise sources).
- Control envelope `environment.transient_noise`: None (absent -- klt adds the block
  only when the netlist declares trnoise/trrandom). klt's assertion in the seeded runs:
  `{"engine": "ngspice", "sources": [{"name": "vn", "kind": "trnoise"}], "intrinsic_device_noise": false, "intrinsic_resistor_noise": false}`. The assertion is the tool's; the 0 V measurement above is ours.
- In the frequency domain the models DO contribute noise: the `.noise` rows above are
  non-zero (that is what the derivation consumes).

## Seeded sigma_v runs (the validation 0014 fixed)

| run | vavg (V) | vrms (V) | sigma (V) | vs expected 7.916701e-03 |
|---|---|---|---|---|
| sigma-s1 | 6.003190000e-01 | 6.003190000e-01 | 0.000000e+00 | -100.00% |
| sigma-s2 | 6.003190000e-01 | 6.003190000e-01 | 0.000000e+00 | -100.00% |
| sigma-s3 | 6.003190000e-01 | 6.003190000e-01 | 0.000000e+00 | -100.00% |
| sigma-s4 | 6.003190000e-01 | 6.003190000e-01 | 0.000000e+00 | -100.00% |
| sigma-s5 | 6.003190000e-01 | 6.003190000e-01 | 0.000000e+00 | -100.00% |
| sigma-s6 | 6.003190000e-01 | 6.003190000e-01 | 0.000000e+00 | -100.00% |
| sigma-s7 | 6.003190000e-01 | 6.003190000e-01 | 0.000000e+00 | -100.00% |
| sigma-s8 | 6.003190000e-01 | 6.003190000e-01 | 0.000000e+00 | -100.00% |

- Mean of 8 runs: 0.000000e+00 V, -100.00% against expected
  7.916701e-03 V; tolerance ±10 % (fixed in 0014 before the run) per run and on the mean.
- Per-number method statement: every sigma above is `sqrt(vrms^2-vavg^2)` over 5-90 ns,
  90 ns transient, NT = 1 ps, 8 pid-seeded (unreproducible, unrecordable) runs.
- Derived sigma_t = sigma_v/SR = 2.541261e-13 s (expected 2.541261e-13 s);
  validated transitively (sigma_v by this check, SR deterministically). No direct
  transient sigma_t measurement exists on this toolchain (edge-drive limitation).

## Abort probe (edge-drive limitation)

- code: `timestep_too_small`; message: ngspice aborted the transient: timestep too small at time = 2e-10 s (trouble with node "vdd#branch"); no results exist past the abort, so measurements beyond it produce no value (engine log: doAnalyses: TRAN:  Timestep too small; time = 2e-10, timestep = 1.25e-24: trouble with node "vdd#branch"). The netlist uses trnoise(): combined with any control source that is not DC from t = 0 (PWL/PULSE/EXP/B-source gate, supply ramp) this is a known ngspice limitation -- see docs/cli/sim.md "Known limitation: trnoise() with non-DC control sources".

The PULSE-driven stage with the trnoise equivalent aborts at the first input edge,
reproducing 0014's limitation: a DLL jitter deck cannot drive the loop with a PULSE
clock while carrying trnoise sources on this toolchain.

## Verdict

- FAIL: sigma-s1: sigma 0.000000e+00 outside ±10 % (fixed in 0014 before the run) of 7.916701e-03
- FAIL: sigma-s2: sigma 0.000000e+00 outside ±10 % (fixed in 0014 before the run) of 7.916701e-03
- FAIL: sigma-s3: sigma 0.000000e+00 outside ±10 % (fixed in 0014 before the run) of 7.916701e-03
- FAIL: sigma-s4: sigma 0.000000e+00 outside ±10 % (fixed in 0014 before the run) of 7.916701e-03
- FAIL: sigma-s5: sigma 0.000000e+00 outside ±10 % (fixed in 0014 before the run) of 7.916701e-03
- FAIL: sigma-s6: sigma 0.000000e+00 outside ±10 % (fixed in 0014 before the run) of 7.916701e-03
- FAIL: sigma-s7: sigma 0.000000e+00 outside ±10 % (fixed in 0014 before the run) of 7.916701e-03
- FAIL: sigma-s8: sigma 0.000000e+00 outside ±10 % (fixed in 0014 before the run) of 7.916701e-03
- FAIL: two seeded runs returned identical (vavg, vrms): a shared noise stream

The bench FAILED; see the criteria above and 0014.
