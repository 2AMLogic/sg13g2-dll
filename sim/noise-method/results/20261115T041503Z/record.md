# noise-method record

SIMULATED results, never measured. Validates spec/decisions/0014 on the known case
(one minimum sg13_lv inverter, mos_tt/1.20 V/27 C). No DLL jitter figure is produced
here (0014; row 6 stays blocked).

- Verdict: **FAIL**
- Stamp: 20261115T041503Z (UTC 2026-11-15T04:18:07Z)
- klt: 0.9.2.dev1029+g76f47afa48f1; engine: ngspice 47; backend: local
- OSDI models (sha256, first 16): `psp103.osdi` 2e4299c4683997e2…; `psp103_nqs.osdi` 839b164483205601…; `r3_cmc.osdi` 4fead17bc2e9cbfe…; `mosvar.osdi` 25e64a374ab523db…
- PDK: IHP-Open-PDK v0.3.0 (sim/pdk.json)

## Method (from 0014)

- Target figure: `sigma_v`, the `.noise` output-noise band integral over 1 MHz-300 GHz
  at the switching-threshold operating point (deterministic), measured on the
  monitored derivation deck (0014 Amendment: same circuit as these estimator decks).
- Equivalent: ONE shunt `trnoise` current source at the stage output node
  (`Ieq out 0 dc=0 trnoise(IA 1p)`), sized by per-deck calibration: a probe run at
  IA = 1e-09 A measures the delivered output rms, and one refinement run at the
  scaled amplitude corrects the residual non-linearity of the scaling; IA scales
  linearly (LTI network) to reproduce sigma_v. The sizing is measured on the same
  deck that the seeded runs use, so no transfer-function model of the injection
  path is needed.
- Timing figure: `sigma_t = sigma_v / SR`; SR from a noiseless edge transient
  (0.1 V between the 0.65/0.55 V crossings of a falling edge). Validated DIRECTLY:
  8 seeded PULSE-driven edge transients, sigma_t per run = rms(t_i - t_det_i) over
  45 falling edges against the deterministic grid; pooled rms across runs graded.
- Seeds: 8 independent runs per set, sequential fresh ngspice processes on one
  host; seed values are NOT recordable on this toolchain (pid-seeded streams; three
  pinning mechanisms probed and refused; 0014 and klayout-tools#5772).
- Run length: 90 ns per sigma run and 95 ns per edge run, trnoise step NT = 1 ps;
  sigma estimator window 5-90 ns (85 000 breakpoints); 45 edges per edge run.
- Estimator: sigma = RMS(v(m)), the AC-coupled monitor node (Cm 0.1p / Rm 1Meg:
  high-pass 1.6 kHz; the monitor is part of the derivation deck too, so target and
  estimator are the same circuit -- attaching it lowers the stage's own sigma_v by a
  measured -13 %, see the 0014 Amendment),
  from a plain `.meas tran` RMS card; no subtractive estimator, so ngspice's
  6-digit measurement print carries full precision at millivolt scale;
  sigma_t per run = sqrt(mean((t_i - t_det_i)^2)), t_i from plain `.meas tran WHEN`
  cards, t_det_i = 0.2n + (i-1)*2n + dt65 with dt65 from the SR derivation.
- Expected values and tolerances were fixed in 0014 BEFORE these runs; derivation
  quantities re-derived by this stamp must agree within the 0014 tolerances.

## Derivation (this stamp; deterministic analyses)

| quantity | value | 0014 expected | agreement |
|---|---|---|---|
| switching threshold vth | 5.702580e-01 V | 5.702580e-01 | 0.00e+00 (0.1 %) |
| OP output level (control AVG v(out)) | 6.003190e-01 V | 6.003190e-01 | 0.00e+00 (0.1 %) |
| sigma_v (onoise, 1 MHz-300 GHz) | 6.889353e-03 V | 6.889353e-03 | 0.00e+00 (1 %) |
| inoise band integral | 4.527237e-03 V | 4.527237e-03 | 0.00e+00 (1 %) |
| density at 10 MHz | 5.782548e-07 V/sqrt(Hz) | 5.782500e-07 | 8.30e-06 (1 %) |
| density at 1 GHz | 7.810424e-08 V/sqrt(Hz) | 7.810400e-08 | 3.07e-06 (1 %) |
| density at 100 GHz | 8.301745e-10 V/sqrt(Hz) | 8.301700e-10 | 5.42e-06 (1 %) |
| slew rate SR (edge 2) | 3.115265e+10 V/s | 3.115265e+10 | 6.50e-08 (1 %) |
| slew rate SR (edge 3) | 3.115265e+10 V/s | 3.115265e+10 | 6.50e-08 (1 %) |
| slope at the 0.6 V crossing, 0.595-0.605 V | 3.125000e+10 V/s | - | informational |
| derived sigma_t = sigma_v/SR | 2.211482e-13 s | 2.211482e-13 | 1.42e-07 (1 %) |

## Injection calibration (this stamp)

- Probe run (IA = 1e-09 A): delivered output rms = 6.784540e-06 V.
- First amplitude: IA_1 = IA_probe * sigma_v / sigma_probe = 1.015449e-06 A.
- Two refinement runs at IA_1 = 1.015449e-06 A deliver 6.687165e-03 V mean  (-2.93% against target; per-run readings are averaged -- a single
  85 ns window carries ~5 independent correlation times of the process, so one
  reading scatters by several percent).
- Final amplitude: IA = IA_1 * sigma_v / mean(sigma_refine) = 1.046151e-06 A
  (target sigma_v = 6.889353e-03 V).
- Linear-scaling check: the seeded runs below deliver sigma_v at IA, verifying the
  proportionality end-to-end over the calibration ratio (~1e3).

## Control run (AC: OSDI models contribute no noise by themselves)

- No `trnoise` source declared: monitor RMS v(m) = 6.828e-14 V
  (must be 0; an ngspice transient carries only declared noise sources).
- Control envelope `environment.transient_noise`: None (absent -- klt adds the block
  only when the netlist declares trnoise/trrandom). klt's assertion in the seeded runs:
  `{"engine": "ngspice", "sources": [{"name": "ieq", "kind": "trnoise"}], "intrinsic_device_noise": false, "intrinsic_resistor_noise": false}`. The assertion is the tool's; the 0 V measurement above is ours.
- In the frequency domain the models DO contribute noise: the `.noise` rows above are
  non-zero (that is what the derivation consumes).

## Seeded sigma_v runs (8 runs, DC-biased deck)

| run | vmavg (V) | vmrms = sigma (V) | vs expected 6.889353e-03 |
|---|---|---|---|
| sigma-s1 | 6.345750000e-04 | 6.959080000e-03 | +1.01% |
| sigma-s2 | 3.109000000e-04 | 6.706760000e-03 | -2.65% |
| sigma-s3 | 6.484730000e-04 | 6.448560000e-03 | -6.40% |
| sigma-s4 | -1.518680000e-04 | 7.165370000e-03 | +4.01% |
| sigma-s5 | 5.275610000e-04 | 6.896890000e-03 | +0.11% |
| sigma-s6 | 4.759200000e-04 | 7.132950000e-03 | +3.54% |
| sigma-s7 | 6.606530000e-04 | 6.847730000e-03 | -0.60% |
| sigma-s8 | -3.458710000e-04 | 7.173850000e-03 | +4.13% |

- Mean of 8 runs: 6.916399e-03 V, +0.39% against expected
  6.889353e-03 V; graded statistic (tolerance ±10 % (fixed in 0014 before the run)).
  Per-run values above are reported, not graded: an 85 ns window holds ~5 independent
  correlation times of the process, so single-run rms values scatter by several
  percent (measured) whatever the method does; 0014's criteria grade the mean.
- Per-number method statement: every sigma above is RMS(v(m)) over 5-90 ns,
  90 ns transient, NT = 1 ps, 8 pid-seeded (unreproducible, unrecordable) runs
  at the calibrated IA.

## Seeded edge runs (direct sigma_t validation, 8 runs, PULSE-driven deck)

| run | mean error (s) | sigma_t (s) | vs expected 2.211482e-13 |
|---|---|---|---|
| edge-s1 | -8.2222e-14 | 1.299231e-13 | -41.25% |
| edge-s2 | -8.3333e-14 | 1.415706e-13 | -35.98% |
| edge-s3 | -6.3333e-14 | 1.266930e-13 | -42.71% |
| edge-s4 | -7.8667e-14 | 1.290822e-13 | -41.63% |
| edge-s5 | -5.3333e-14 | 1.333333e-13 | -39.71% |
| edge-s6 | -6.0000e-14 | 1.433411e-13 | -35.18% |
| edge-s7 | -7.6889e-14 | 1.248288e-13 | -43.55% |
| edge-s8 | -9.3111e-14 | 1.325896e-13 | -40.04% |

- Pooled sigma_t (weighted rms over 360 edges): 1.328167e-13 s,
  -39.94% against expected 2.211482e-13 s (= sigma_v/SR =
  6.889353e-03/3.115265e+10); tolerance ±25 % (fixed in 0014 before the run) pooled.
- Per-number method statement: crossing times are plain `.meas tran WHEN v(out)=0.65`
  cards, falling edges 2..46 of a 2 ns-period PULSE; per-run sigma_t is the rms of the
  crossing-time error against the deterministic grid; the noise correlation time (the
  stage's ~8 ns response time) makes edges within a run correlated, so per-run values
  scatter and the pooled figure across the 8 runs is the graded one.
- The edge deck carries the same shunt equivalent at the same calibrated IA with a
  PULSE drive: the shunt-current form coexists with a switching drive (the abort
  below is specific to the series-voltage form).

## Abort probe (series-voltage trnoise + PULSE drive)

- code: `timestep_too_small`; message: ngspice aborted the transient: timestep too small at time = 2e-10 s (trouble with node "vdd#branch"); no results exist past the abort, so measurements beyond it produce no value (engine log: doAnalyses: TRAN:  Timestep too small; time = 2e-10, timestep = 1.25e-24: trouble with node "vdd#branch"). The netlist uses trnoise(): combined with any control source that is not DC from t = 0 (PWL/PULSE/EXP/B-source gate, supply ramp) this is a known ngspice limitation -- see docs/cli/sim.md "Known limitation: trnoise() with non-DC control sources".

The series-voltage trnoise equivalent aborts the transient at the first input edge
(0014's limitation): that form cannot drive a DLL jitter deck. The shunt-current
form the method adopts runs clean with the same PULSE drive (edge runs above).

## Verdict

- FAIL: pooled sigma_t 1.328167e-13 s outside ±25 % (fixed in 0014 before the run) of 2.211482e-13 s

The bench FAILED; see the criteria above and 0014.
