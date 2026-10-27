# sim/lock-range

Spec rows 1 and 2: the Locked predicate (`spec/target-spec.md`) at 0.8, 0.9, 1.0, 1.1, 1.2 x f0, over all 45 corners, from every row-8 start state (the spec says so; a friendly start is not a lock).

Simulated, never measured.

Five requests (`f080`..`f120`), 9 start states x 45 corners = 405 units each (2025 total, about a minute of ngspice per unit on the stand-in). The same grid and measurements as `sim/false-lock`; that bench reads the delay in periods and LOCK, this one reads the predicate. Grading: a corner passes when the last 64 input cycles each have |tap8 delay - T| <= tol*T and the control voltage moves < 5 mV over them (`perr`, `vcpp`). `record.md` tabulates locked corners per frequency and start state.

## Cold start

From a fresh clone with the PDK installed (`sim/pdk.json`: IHP-Open-PDK v0.3.0; `PDK_ROOT`, OSDI built by `sim/harness/common/build-osdi.sh`):

```
sim/lock-range/run.sh
```

It builds the grid requests through `sim/harness/gridspec.py` (via `sim/harness/dllbench.py`), submits each with `klt sim` (multi-unit requests go to the batch fleet; there is no local fallback and a failed submit fails the run), grades the envelopes, and writes `sim/lock-range/results/<UTC stamp>/` (decks, requests, envelopes, `record.md`; append-only). `BENCH_BUILD_ONLY=1` builds and stops. Environment knobs are listed in `sim/harness/bench-run.sh`; `BENCH_F0_HZ` picks the spec column (1e9 target, 5e8 fallback, 2e9 stretch) and `BENCH_TOL` its phase tolerance (0.02 / 0.05 / 0.01).
Exit codes: 0 pass, 1 harness fault, 3 missing prerequisite, 6 harness fine but a corner fails its row.

**STAND-IN.** The default DUT is the behavioural model in `sim/standin/`, not the item-1 netlist (#24). A result here is a result about that model, is "simulated", and does not satisfy T1 item 9. Repointing is a DUT descriptor (`BENCH_DUT=...`) with the port contract in `sim/standin/dut.json`, not a bench edit. No fleet run is recorded for this bench in this PR.
