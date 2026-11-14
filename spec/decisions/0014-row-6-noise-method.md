# 0014 — Row 6 noise method: one white input-referred thermal equivalent per stage, derived from `.noise` at the operating point, validated on a known case

- **Status**: proposed
- **Date**: 2026-11-14
- **Decided by**: Builder agent, issue #115
- **Related**: `spec/target-spec.md` row 6 ("Jitter method"), 0009 (spec ratification), 0008 (false-lock argument), [klayout-tools#5772](https://github.com/2AMLogic/klayout-tools/issues/5772) (seed gap), `sim/noise-method/` (the validating bench)

This record fixes what `spec/target-spec.md` row 6 deferred to it: "which devices,
what bandwidth and where the equivalents sit is fixed in a decision record,
validated on a known case, before the first jitter result is recorded". It also
settles the open question the spec states: "whether the PSP103 OSDI models
contribute noise in a transient run is not established". It produces **no DLL
jitter figure**; row 6 stays `blocked` until a DLL deck exists. It lands as
`proposed`; ratification is out of scope (issue #115).

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
- **Committed measurement.** `sim/noise-method/` runs the known case
  (one minimum `sg13_lv_*` inverter, DC-biased at its switching threshold) as
  a 90 ns transient **without** any declared noise source: the recovered
  output rms `sqrt(vrms^2 - vavg^2)` is **exactly 0** (to the printed
  precision of both `.meas` values) at mos_tt/27 °C. The same stage **with** a
  declared `trnoise` source shows a non-zero output rms and carries the
  `transient_noise` block above. Both runs are committed in the bench's
  results stamp.

Complementarily, the models **do** contribute noise in a `.noise` analysis
(frequency domain): the known case's output-referred density is non-zero
(725.6 nV/sqrt(Hz) at 10 MHz; 79.2 nV/sqrt(Hz) at 1 GHz). That is what makes
the derivation below possible, and it does not contradict the transient
answer: `.noise` computes device noise sums explicitly; the ngspice transient
engine does not.

## The equivalent (what row 6's jitter deck represents)

1. **Sources represented: thermal noise of the delay cell's devices only,
   collapsed into one white input-referred voltage equivalent per delay
   stage.** No per-device equivalents: the `.noise` analysis already sums
   every device's contribution referred to the input source, and the figure
   row 6 grades is the stage-to-stage timing error, not a device breakdown.
   A single input-referred source reproduces the integrated output noise of
   the sum exactly (the shaping is done by the stage's own transfer, see the
   ENBW derivation), which is the quantity the method needs. Flicker is
   **excluded**: the spec's own limitation note grades row 6 as "simulated
   added jitter, thermal-noise class", and ngspice's transient noise
   underestimates 1/f.
2. **Derivation from `.noise` at the operating point.** At the locked
   operating point (the delay cell DC-biased so its output sits at the
   switching threshold), run
   `analysis.kind: "noise"`, `args: "v(out) <input-source> dec <pts> <f_lo> <f_hi>"`
   and take, through klt's native `measurements[].noise` form:
   - `sigma_v = onoise` band integral over **[1 MHz, 300 GHz]** — the total
     output rms noise the method must reproduce;
   - `ENBW = (sigma_R^2 - sigma_v^2) / (4 k T R)` from a second `.noise` run
     of the **same** netlist with a 1 MOhm resistor `R` inserted in series
     between the input source and the stage. The resistor contributes a known
     flat density `sqrt(4 k T R)` shaped by exactly the stage transfer, so
     the identity is exact and needs no manual spectral quadrature
     (`sigma_R` is that run's band integral; the device-noise run's
     `sigma_v` is subtracted in quadrature; `T` = 300.15 K).
3. **Bandwidth: 1 MHz to 300 GHz, fixed before any run.** Justification:
   the upper edge is set by the stage itself — the output-referred density of
   the known case falls to 82.5 pV/sqrt(Hz) at 100 GHz (two poles,
   -40 dB/dec), so the band tail above 300 GHz contributes under 1e-6 of
   `sigma_v^2`; the stage's noise bandwidth (measured below: 20.8 GHz)
   sits far inside the band, so the integral is transfer-limited, not
   band-limited. The lower edge excludes less than 1e-5 of `sigma_v^2`
   (plateau density 725.6 nV/sqrt(Hz) times 1 MHz against the 6.27e-5 V^2
   total). 1 MHz also stays above the flicker-corner region the method
   excludes. `trnoise` time step `NT = 1 ps` keeps the generated process
   white past 1/(2 NT) = 500 GHz, above the band top, so no folding error
   enters the band.
4. **Placement: one series voltage source at the stage input**, between the
   input node and the cell, `Vn <gin> <in> dc=0 trnoise(NA NT)`. There rather
   than at each device: the equivalent is input-referred by construction (it
   is derived from `onoise` via the transfer), the stage shapes it with the
   same transfer the `.noise` analysis used (the validation checks exactly
   this), and one source per stage keeps a DLL deck (8+ cells) tractable.
5. **`NA` — the equivalent density:**

   `NA = sigma_v / ( sqrt(2/3) * sqrt(ENBW) )`

   The `sqrt(2/3)` factor: ngspice's `trnoise(NA NT)` draws Gaussian
   breakpoints every `NT` and interpolates linearly between them; the rms of
   the interpolated process is `NA * sqrt(2/3)`, not `NA` (theory
   `0.8165`; measured `0.818` on a bare RC probe at NA = 1 mV, NT = 1 ps —
   0.2 % agreement). Omitting the factor overstates the noise by 22.5 %.
6. **Slew rate and the timing figure.** `SR` comes from a separate
   **noiseless** transient at the same operating point and corner
   (dV/dt at the crossing, measured as 0.1 V between the 0.65 V and 0.55 V
   crossings of the same edge). The known case's expected timing spread is

   `sigma_t = sigma_v / SR`.

   The transient-noise path **cannot** measure edge jitter directly on this
   toolchain — see the limitation below — so `sigma_t` is a derived figure
   whose two inputs are each validated (`sigma_v` by the seeded transient
   check; `SR` by a deterministic transient, reproducible bit-for-bit).

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

## The edge-drive limitation (why a DLL jitter deck cannot be PULSE-driven)

`trnoise` combined with **any** non-DC independent source aborts the ngspice
transient at the first edge — klt documents it (`timestep_too_small`
diagnostic, "known ngspice limitation"), and the bench reproduces it on
ngspice-47 at mos_tt/27 °C:

> ngspice aborted the transient: timestep too small at time = 2.5e-10 s
> (trouble with node "vdd#branch"); no results exist past the abort
> (engine log: doAnalyses: TRAN: Timestep too small; time = 2.5e-10,
> timestep = 1.25e-24: trouble with node "vdd#branch").

The known case aborts at t = 0.25 ns — the moment its PULSE input starts to
rise. A DLL clock is PULSE-driven, so **row 6's deck cannot inject the
equivalents and drive the loop at the same time** on this toolchain; there is
no edge-producing drive (PWL/PULSE/EXP/B-source) that survives. The method
therefore lives inside the limitation:

- `sigma_v` is measured with **all-DC** sources (allowed: `trnoise` with a DC
  bias point runs clean), at the locked operating point;
- `SR` is measured noiselessly at the same operating point;
- `sigma_t = sigma_v / SR` is derived, and every DLL figure produced this way
  states so — it is not a transient-noise measurement of a switching loop.
- If a future ngspice lifts the limitation, the method re-opens: a direct
  edge-jitter validation becomes possible and should replace the derived
  figure. The bench's abort probe re-checks this every run; if the abort
  disappears, the bench fails loudly.

## Known case: fixed before the validation run

The case: one minimum-size `sg13_lv_*` inverter (w = 0.15 u, l = 0.13 u,
`Cl` = 2 fF, Vdd = 1.2 V) at **mos_tt / 1.20 V / 27 °C**, DC-biased at its
switching threshold. Derivation values below were measured before this
record was committed and are re-derived by every `sim/noise-method/run.sh`
invocation (the analyses involved are deterministic; the bench fails if a
re-derivation drifts beyond the tolerances in the last column).

| quantity | value | source | reproduction tolerance |
|---|---|---|---|
| switching threshold `vth` | 0.570258 V | `.dc` sweep, `v(out)=0.6` | ±0.1 % |
| OP output level | 0.600319 V | control transient `vavg` | ±0.1 % |
| `sigma_v` (onoise, 1 MHz–300 GHz) | 7.916701e-3 V | `.noise` band integral | ±1 % |
| inoise band integral | 4.500722e-3 V | `.noise` band integral | ±1 % |
| density, 10 MHz / 1 GHz / 100 GHz | 725.6 n / 79.2 n / 82.5 pV/sqrt(Hz) | `.noise` spot | ±1 % |
| `sigma_R` (with 1 MOhm series R) | 2.016996e-2 V | `.noise` band integral | ±1 % |
| `ENBW` | 2.076204e10 Hz (20.76 GHz) | resistor identity | ±1 % |
| gain A0 at 1 MHz (consistency) | 25.75 V/V (single-pole fit fp ≈ 19.9 MHz) | `s_1M_R / sqrt(4kTR)` | ±2 % |
| equivalent density `NA` | 6.729066e-8 V/sqrt(Hz) | `sigma_v/(sqrt(2/3)*sqrt(ENBW))` | ±2 % |
| slew rate `SR` | 3.115265e10 V/s | noiseless edge transient, 0.65→0.55 V crossings, falling edges 2 and 3 (identical) | ±1 % |
| **expected timing spread `sigma_t`** | **2.541261e-13 s (254.13 fs)** | `sigma_v / SR` | derived |
| control output rms (no source) | 0.0 V exactly | `sqrt(vrms^2 - vavg^2)`, 90 ns | must be 0 |

**Validation criteria (fixed here, before any run of the seeded set):**

- **Expected value:** the mean of the 8 seeded transient measurements of
  `sigma_v` equals 7.916701e-3 V (the `.noise` derivation) within
  **±10 %**; each individual run within ±10 % of the same. The basis: the
  predicted agreement is ~1 % (0.2 % measured process-factor agreement,
  0.25 % finite-sample estimator at NT = 1 ps over an 85 ns window,
  < 1e-5 band-edge and folding terms); 10 % leaves two orders of margin over
  the theory error while still catching a wrong factor or a broken shaping
  argument.
- **Tolerance:** ±10 % as above; the bench fails (non-zero exit) if missed,
  and `record.md` states in/out-of-tolerance next to every number.
- **Seed count:** 8 independent runs (fresh process each, sequential on one
  host; seed values not recordable — see the seed story).
- **Run length:** each seeded transient runs 90 ns (trnoise step 1 ps;
  estimator window 5 ns–90 ns, 85 000 breakpoints).
- **Estimator:** per run, `sigma = sqrt(vrms^2 - vavg^2)` from two plain
  `.meas tran` cards (`AVG` and `RMS` of `v(out)` over the window); no
  hand-rolled waveform arithmetic.
- The 8 run outputs must additionally be pairwise distinct (two identical
  (vavg, vrms) pairs would mean a shared noise stream — the pid caveat).

A transient measurement of `sigma_t` itself is **not** possible on this
toolchain (the edge-drive limitation); the validation of `sigma_t` is
transitive through `sigma_v` and `SR`.

## Outcome

Filled after the run; see the appended section once
`sim/noise-method/results/` exists in the tree.
