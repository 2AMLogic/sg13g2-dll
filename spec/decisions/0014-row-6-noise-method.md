# 0014 — Row 6 noise method: one thermal `trnoise` equivalent per delay stage, target taken from `.noise` at the operating point, amplitude calibrated per deck, validated on a known case

- **Status**: proposed
- **Date**: 2026-11-14 (revised same day, before any validated run — see Revision)
- **Decided by**: Builder agent, issue #115
- **Related**: `spec/target-spec.md` row 6 ("Jitter method"), 0009 (spec ratification), 0008 (false-lock argument), [klayout-tools#5772](https://github.com/2AMLogic/klayout-tools/issues/5772) (seed gap), `sim/noise-method/` (the validating bench)

This record fixes what `spec/target-spec.md` row 6 deferred to it: "which devices,
what bandwidth and where the equivalents sit is fixed in a decision record,
validated on a known case, before the first jitter result is recorded". It also
settles the open question the spec states: "whether the PSP103 OSDI models
contribute noise in a transient run is not established". It produces **no DLL
jitter figure**; row 6 stays `blocked` until a DLL deck exists. It lands as
`proposed`; ratification is out of scope (issue #115).

## Revision (2026-11-14, before any validated run)

The first formulation of this record (committed earlier the same day) derived a
white equivalent **density** `NA = sigma_v/(sqrt(2/3)*sqrt(ENBW))` for a
**series-voltage** `trnoise` source at the stage input, with `ENBW` from a
series reference-resistor identity. The bench's first run falsified it: every
seeded transient measured **zero** output noise at the derived amplitude —
about 3 orders below the prediction. Probing isolated two errors, both kept
here because they are tool facts any later jitter deck will hit again:

1. **ngspice's `trnoise` amplitude is a process rms, not a spot density.**
   `trnoise(NA NT)` generates a waveform whose rms is about `NA·sqrt(2/3)`
   (linear interpolation between Gaussian breakpoints every `NT`; measured
   `0.818` against `0.8165` theory on a bare RC). Its spectral density is
   `S0 = NA²·2·NT` — measured on a bare RC (f3dB = 159 MHz, ENBW = 2.5e8 Hz)
   to 0.2 % for the voltage form (`S0/NA² = 2.008e-12` vs `2·NT = 2e-12`) —
   so at `NT = 1 ps` an `NA` of millivolts carries nanovolt-scale density.
   A density-matching formula therefore overpredicts the delivered noise by
   orders of magnitude. Worse, the delivered multiplier is not stable across
   deck contexts (measured 1×, 1.6×, 7.4× of the bare-RC law on deck
   variants of this bench), so no fixed formula can size the source.
2. **The series reference-resistor ENBW identity is biased for gate
   injection.** The resistor's noise reaches a MOS gate through the
   gate-capacitance divider, so the identity measured the transfer *from the
   resistor*, not *from a stiff source* — the quantity the series equivalent
   needed. It is dropped from the method.
3. **Subtractive rms estimators are print-limited.** ngspice prints `.meas`
   results with 6 significant digits, so `sqrt(RMS² − AVG²)` on a 0.6 V node
   is blind below ~1 mV of noise (the difference term needs 1e-6 resolution).
   The estimators read the noise off an AC-coupled monitor node instead
   (0.1 pF / 1 MOhm, high-pass 1.6 kHz, under 0.1 % load in band), where the
   RMS card carries full precision at millivolt scale.

The corrected method sizes the equivalent **by calibration on the very deck
that runs it** (no transfer model of the injection path is needed), and places
the source as a **shunt current at the output node**, which additionally turns
out to coexist with a PULSE drive (see the edge-drive section): the known case
can validate `sigma_t` **directly** on edge transients, which the first
formulation held impossible. The expected values and the `sigma_v` tolerance
are unchanged from the first formulation; they were fixed before the first run
and the first run failed against them — that failure is part of this record.

## The OSDI intrinsic-noise answer (spec's open question)

**The PSP103 OSDI models contribute no noise by themselves in an ngspice
transient; an ngspice transient contains only the noise of explicitly declared
`trnoise` / `trrandom` sources.** Two kinds of evidence, kept distinct:

- **Tool assertion.** For any ngspice transient whose netlist declares a
  `trnoise`/`trrandom` source, klt adds an
  `environment.transient_noise` block to the result envelope stating
  `"intrinsic_device_noise": false, "intrinsic_resistor_noise": false` and
  listing the declared sources. This is klt telling the caller what the
  transient contains; it is not a measurement.
- **Committed measurement.** `sim/noise-method/` runs the known case as a
  90 ns transient **without** any declared noise source: the rms on the
  AC-coupled monitor node (0.1 pF / 1 MOhm to ground, high-pass 1.6 kHz,
  loading the output by well under 0.1 % across the band) reads **exactly
  0** at mos_tt/27 °C. The same stage **with** a declared
  `trnoise` source shows a non-zero monitor rms and carries the
  `transient_noise` block above. Both runs are committed in the bench's
  results stamps.

Complementarily, the models **do** contribute noise in a `.noise` analysis
(frequency domain): the known case's output-referred density is non-zero
(725.6 nV/sqrt(Hz) at 10 MHz; 79.2 nV/sqrt(Hz) at 1 GHz). That is what makes
the derivation below possible, and it does not contradict the transient
answer: `.noise` computes device noise sums explicitly; the ngspice transient
engine does not.

## The equivalent (what row 6's jitter deck represents)

1. **Sources represented: thermal noise of the delay cell's devices, collapsed
   into one equivalent per delay stage.** No per-device equivalents: the
   `.noise` analysis already sums every device's contribution into the
   output-referred band integral the equivalent must reproduce, and the
   figure row 6 grades is the stage-to-stage timing error, not a device
   breakdown. Flicker is **excluded**: the spec's own limitation note grades
   row 6 as "simulated added jitter, thermal-noise class", and ngspice's
   transient noise underestimates 1/f.
2. **Target figure from `.noise` at the operating point.** At the locked
   operating point (the delay cell biased to its switching threshold), run
   `analysis.kind: "noise"`, `args: "v(out) <input-source> dec <pts> <f_lo> <f_hi>"`
   and take, through klt's native `measurements[].noise` form, the `onoise`
   band integral over **[1 MHz, 300 GHz]** as `sigma_v` — the total output rms
   noise the equivalent must reproduce. Deck requirements the first probes
   hit: the `.noise` input reference source must carry an AC value
   (`ac 1`), or ngspice aborts the noise analysis ("ac input not found").
3. **Bandwidth: 1 MHz to 300 GHz, fixed before any run.** Justification: the
   upper edge is set by the stage itself — the output-referred density of the
   known case falls to 82.5 pV/sqrt(Hz) at 100 GHz (-40 dB/dec, two poles), so
   the tail above 300 GHz contributes under 1e-6 of `sigma_v^2`. The lower
   edge excludes less than 1e-5 of `sigma_v^2` (plateau density 725.6
   nV/sqrt(Hz) times 1 MHz against the 6.27e-5 V² total). 1 MHz also stays
   above the flicker-corner region the method excludes. `NT = 1 ps` keeps the
   generated process white to 1/(2 NT) = 500 GHz, above the band top, so no
   folding error enters the band.
4. **Placement: one shunt current source at the delay cell's output node**,
   `Ieq <out> 0 dc=0 trnoise(IA 1p)`. There rather than in series with the
   input: the series-voltage form cannot coexist with a switching drive (the
   abort below) and its injection strength proved deck-context-dependent;
   the output node is where the DLL's tap signal lives and where the timing is
   read, the injection stays small-signal at the calibrated amplitude
   (millivolt-scale excursions on a 1.2 V rail), and one source per tap keeps
   a DLL deck (8+ cells) tractable.
5. **Amplitude by per-deck calibration, not by formula.** `trnoise`'s
   amplitude semantics (process rms; context-dependent delivered density; see
   Revision) make a fixed density formula unreliable. The method calibrates
   on the very deck that runs: one probe transient at `IA_probe = 1e-9 A`
   measures the delivered output rms `sigma_probe`; the network is linear
   (the excursions are millivolt-scale on a 1.2 V rail), so
   `IA = IA_probe · sigma_v / sigma_probe`. The seeded runs then verify the
   scaled amplitude delivers `sigma_v` (the linearity check over the ~1e3
   calibration ratio is part of the validation).
6. **Slew rate and the timing figure.** `SR` comes from a separate
   **noiseless** transient at the same operating point and corner
   (dV/dt at the crossing, measured as 0.1 V between the 0.65 V and 0.55 V
   crossings of the same edge; deterministic — edges 2 and 3 of the same run
   agree to 10 digits). The known case's expected timing spread is

   `sigma_t = sigma_v / SR`.

   This is a pointwise identity: each crossing samples the instantaneous
   output noise divided by the instantaneous slope, so it holds whether or not
   the noise is correlated from edge to edge; correlation only widens the
   estimator's confidence interval, which the tolerance below accounts for.

## The edge-drive limitation (form-specific, measured both ways)

`trnoise` combined with a non-DC independent source **aborts the ngspice
transient at the first edge when the noise source is the series-voltage
form** — klt documents it (`timestep_too_small` diagnostic, "known ngspice
limitation"), and the bench reproduces it on ngspice-47 at mos_tt/27 °C:

> ngspice aborted the transient: timestep too small at time = 2.5e-10 s
> (trouble with node "vdd#branch"); no results exist past the abort
> (engine log: doAnalyses: TRAN: Timestep too small; time = 2.5e-10,
> timestep = 1.25e-24: trouble with node "vdd#branch").

The same stage with the **shunt-current** equivalent (`Ieq out 0 dc=0
trnoise(...)`) and the same PULSE drive **runs to completion** (the bench's
edge runs do it 8 times with calibrated amplitude). So the limitation is
form-specific: a DLL jitter deck must not use series-voltage `trnoise`
equivalents anywhere in a switched circuit; the shunt-current form is the one
this record's method uses. The bench re-checks the abort every run; if it
disappears, the bench fails loudly and this record re-opens.

## The seed story (what "seeds recorded" means on this toolchain)

The spec asks for ">= 8 independent seeds per corner; seed values recorded".
On klt 0.9.2.dev1029 + ngspice-47 **no mechanism pins or reports the RNG seed
governing a `trnoise` stream**; three were probed empirically before this
record was written:

1. `monte_carlo.seed` — klt's own `environment.transient_noise.unseeded_sources_note`
   states "trnoise()/trrandom() sources are not governed by monte_carlo.seed
   (ngspice seeds them from the process id)". Confirmed: re-running an
   identical request redraws the noise.
2. `options.ngspice_options` — `seed` is not in klt's `NGSPICE_SOLVER_OPTIONS`
   allowlist, so a request cannot emit `.options seed=N`.
3. A deck-body `.options seed=N` — the card passes through the `.include`d
   body, but **ngspice-47 does not honor it for the transient-noise
   generator**: three runs with identical `.options seed=42` produced three
   different noise waveforms (point samples at fixed times). A control-block
   `rndseed` command does not exist in ngspice-47 ("no such command").

Filed as [klayout-tools#5772](https://github.com/2AMLogic/klayout-tools/issues/5772).
Consequence for row 6: **independence is real, seed values are not
recordable.** A campaign runs >= 8 sequential fresh-process `klt sim`
invocations on one host (sequential processes cannot share a pid, closing the
shared-stream caveat klt's note raises for parallel batch jobs), reports the
per-run figures, and states beside them that the streams are pid-seeded and
unreproducible. No jitter result may claim recorded seed values on this
toolchain.

## Known case: expected values and criteria, fixed before the runs

The case: one minimum-size `sg13_lv_*` inverter (w = 0.15 u, l = 0.13 u,
`Cl` = 2 fF, Vdd = 1.2 V) at **mos_tt / 1.20 V / 27 °C**, DC-biased at its
switching threshold. Derivation values below were measured before this record
was committed and are re-derived by every `sim/noise-method/run.sh`
invocation (the analyses involved are deterministic; the bench fails if a
re-derivation drifts beyond the tolerances in the last column).

| quantity | value | source | reproduction tolerance |
|---|---|---|---|
| switching threshold `vth` | 0.570258 V | `.dc` sweep, `v(out)=0.6` | ±0.1 % |
| OP output level | 0.600319 V | control transient `vavg` | ±0.1 % |
| `sigma_v` (onoise, 1 MHz–300 GHz) | 7.916701e-3 V | `.noise` band integral | ±1 % |
| inoise band integral | 4.500722e-3 V | `.noise` band integral | ±1 % |
| density, 10 MHz / 1 GHz / 100 GHz | 725.6 n / 79.2 n / 82.5 pV/sqrt(Hz) | `.noise` spot | ±1 % |
| slew rate `SR` | 3.115265e10 V/s | noiseless edge transient, 0.65→0.55 V crossings, falling edges 2 and 3 (identical) | ±1 % |
| **expected timing spread `sigma_t`** | **2.541261e-13 s (254.13 fs)** | `sigma_v / SR` | derived |
| control monitor rms (no source) | 0.0 V exactly | `RMS(v(m))`, 90 ns | must be 0 |

**Validation criteria (fixed before the runs; the first formulation's run
failed the first of them, which drove the Revision above):**

- **`sigma_v` (8 seeded runs, DC-biased deck at the calibrated `IA`):** the
  mean within **±10 %** of 7.916701e-3 V, and each individual run within
  ±10 % of the same. The basis: the delivered rms scales linearly and the
  calibration probe measures it on the same deck; residual error is the
  finite-sample estimator (~0.25 % at NT = 1 ps over an 85 ns window) plus
  stream variance; 10 % leaves two orders of margin over that while still
  catching a broken scaling or a wrong target.
- **`sigma_t` (8 seeded runs, PULSE-driven deck at the same `IA`):** per run,
  the rms of the 45 crossing-time errors against the deterministic grid;
  the **pooled** rms across the 8 runs within **±25 %** of 2.541261e-13 s,
  per-run values reported individually. The basis: the stage's ~8 ns noise
  correlation time makes edges within a run correlated (~12 independent
  windows per run, ~95 pooled), so the pooled estimator's relative standard
  deviation is ~7 %; 25 % leaves over 3× margin. Per-run scatter is expected
  and reported, not graded.
- **Seed count:** 8 independent runs per set (fresh process each, sequential
  on one host; seed values not recordable — see the seed story).
- **Run lengths:** each sigma transient 90 ns and each edge transient 95 ns
  (trnoise step `NT = 1 ps`; sigma estimator window 5–90 ns; 45 falling edges
  per edge run at a 2 ns period).
- **Estimators:** per run, `sigma = RMS(v(m))` on the AC-coupled monitor node
  (0.1 pF / 1 MOhm; high-pass 1.6 kHz; output load under 0.1 % across the
  band) from one plain `.meas tran` RMS card — no subtractive estimator, so
  ngspice's 6-digit measurement print carries full precision at the
  millivolt scale (a subtractive `sqrt(RMS² − AVG²)` on the output node is
  print-limited and blind below ~1 mV); `sigma_t = sqrt(mean((t_i -
  t_det_i)^2))` with `t_i` from plain `.meas tran WHEN v(out)=0.65` cards and
  `t_det_i = 0.2n + (i-1)·2n + dt65`, `dt65` taken from the SR derivation.
  No hand-rolled waveform arithmetic.
- The 8 run outputs of each set must additionally be pairwise distinct (two
  identical results would mean a shared noise stream — the pid caveat).

## Outcome

Filled after the run; see the appended section once
`sim/noise-method/results/` exists in the tree.
