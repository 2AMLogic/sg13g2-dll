# sim/noise-method

Validates the row 6 noise method on a known case: `spec/decisions/0014-row-6-noise-method.md`
is the record; this bench is its validation. It produces **no DLL jitter figure**
and does not attest any spec row (row 6 stays `blocked` on `sim/jitter` until a
DLL deck exists).

The known case is one minimum-size `sg13_lv_*` inverter (w = 0.15u, l = 0.13u,
Cl = 2 fF, 1.2 V) at mos_tt/1.20 V/27 °C, DC-biased at its switching threshold.
The bench derives the noise equivalent from `.noise` analyses at that operating
point (band 1 MHz–300 GHz; ENBW from a series 1 MΩ reference-resistor identity),
measures the slew rate noiselessly, injects the derived white `trnoise`
equivalent with all-DC sources, and checks the seeded transient output rms
against the `.noise` derivation within the tolerance 0014 fixed before the run.
It also carries the two probes 0014 reports: the no-noise control (the OSDI
models contribute no transient noise by themselves) and the abort probe
(`trnoise` + PULSE drive is a documented ngspice limitation).

Single corners only; every run goes through `klt sim --backend local`.

## Cold start

```
sim/noise-method/run.sh
```

Derivation, control, abort probe, 8 seeded runs, and `record.md` in one
append-only `results/<UTC stamp>/` directory; exit 0 only on a PASS verdict.
The 8 seeded runs are pid-seeded fresh ngspice processes: seed values are not
recordable on this toolchain (0014 "The seed story", klayout-tools#5772), and
re-running redraws their noise.

## What is not here

No DLL deck, no request or result for any spec row, no jitter figure for the
DLL, its delay line or any tap. `sim/jitter/` remains the row 6 bench and
stays `blocked` (see its README).
