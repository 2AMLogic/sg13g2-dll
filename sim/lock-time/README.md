# sim/lock-time

Spec row 7: lock time from the later of enable assertion and the first input edge (the re-enable time for the re-enable state), at f0, over all 45 corners and every row-8 start state (the grader takes the worst).

Simulated, never measured.

One request, 405 units. Besides the predicate set, every 16th input cycle is sampled (`te_j` edge time, `ds_j` tap-8 delay, `ls_j` LOCK). The lock time is the first sampled time from which every later sample satisfies the predicate and the final 64-cycle predicate holds; **resolution is 16 cycles (16 ns at 1 GHz)**, and each sample is a single-cycle test of the predicate's delay condition (the 64-consecutive-cycle and 5 mV conditions are applied to the final window only), so the reported time is an estimate of the spec's lock time, not the exact predicate. The limit (1 us target, 5 us fallback) is applied by whoever reads `record.md`; the bench reports the maximum and counts corners with no lock time. The run is 3.2 us so that the state with the latest enable still has 2 us.

## Cold start

From a fresh clone with the PDK installed (`sim/pdk.json`: IHP-Open-PDK v0.3.0; `PDK_ROOT`, OSDI built by `sim/harness/common/build-osdi.sh`):

```
sim/lock-time/run.sh
```

It builds the grid requests through `sim/harness/gridspec.py` (via `sim/harness/dllbench.py`), submits each with `klt sim` (multi-unit requests go to the batch fleet; there is no local fallback and a failed submit fails the run), grades the envelopes, and writes `sim/lock-time/results/<UTC stamp>/` (decks, requests, envelopes, `record.md`; append-only). `BENCH_BUILD_ONLY=1` builds and stops. Environment knobs are listed in `sim/harness/bench-run.sh`; `BENCH_F0_HZ` picks the spec column (1e9 target, 5e8 fallback, 2e9 stretch) and `BENCH_TOL` its phase tolerance (0.02 / 0.05 / 0.01).
Exit codes: 0 pass, 1 harness fault, 3 missing prerequisite, 6 harness fine but a corner fails its row.

**STAND-IN.** The default DUT is the behavioural model in `sim/standin/`, not the item-1 netlist (#24). A result here is a result about that model, is "simulated", and does not satisfy T1 item 9. Repointing is a DUT descriptor (`BENCH_DUT=...`) with the port contract in `sim/standin/dut.json`, not a bench edit. No fleet run is recorded for this bench in this PR.
