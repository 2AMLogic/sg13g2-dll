# sim/phase

Spec rows 3, 4 and 5: output phases, adjacent-tap spacing and static phase error, locked, at f0, over all 45 corners (start state 1, since these rows grade the locked loop).

Simulated, never measured.

For taps 0..8 the delay from input edge j to tap edge j is measured on the 64-cycle window and averaged (`s0`..`s8`). Row 4: each of the 8 adjacent spacings `sp0`..`sp7` (tap7 to the reference tap8 included) within T/8 +- tol*T (`sperr*`). Row 5: `sterr` = |s8 - T|/T <= tol. Row 3 is structural: the DUT descriptor lists tap0..tap7 as outputs and tap8 as the reference, checked in `sim/harness/tests/test_dllbench.py`. Every tap and LOCK drive 20 fF to VSS. This is the **schematic** result; the post-layout extracted result is the graded one for row 4 and is recorded separately (other T1 items). Monte Carlo is a separate recorded result and is not in this bench.

## Cold start

From a fresh clone with the PDK installed (`sim/pdk.json`: IHP-Open-PDK v0.3.0; `PDK_ROOT`, OSDI built by `sim/harness/common/build-osdi.sh`):

```
sim/phase/run.sh
```

It builds the grid requests through `sim/harness/gridspec.py` (via `sim/harness/dllbench.py`), submits each with `klt sim` (multi-unit requests go to the batch fleet; there is no local fallback and a failed submit fails the run), grades the envelopes, and writes `sim/phase/results/<UTC stamp>/` (decks, requests, envelopes, `record.md`; append-only). `BENCH_BUILD_ONLY=1` builds and stops. Environment knobs are listed in `sim/harness/bench-run.sh`; `BENCH_F0_HZ` picks the spec column (1e9 target, 5e8 fallback, 2e9 stretch) and `BENCH_TOL` its phase tolerance (0.02 / 0.05 / 0.01).
Exit codes: 0 pass, 1 harness fault, 3 missing prerequisite, 6 harness fine but a corner fails its row.

**STAND-IN.** The default DUT is the behavioural model in `sim/standin/`, not the item-1 netlist (#24). A result here is a result about that model, is "simulated", and does not satisfy T1 item 9. Repointing is a DUT descriptor (`BENCH_DUT=...`) with the port contract in `sim/standin/dut.json`, not a bench edit. No fleet run is recorded for this bench in this PR.
