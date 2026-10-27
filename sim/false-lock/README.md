# sim/false-lock

Spec rows 8 and 12: false lock and the lock-status output, from every start state at every frequency of row 2 and every corner.

Simulated, never measured.

Start states (`sim/harness/dllbench.py`, `STATES`): 1 min-delay rail, 2 max-delay rail, 3 mid-range, 4 the two presets where nominal delay is 0.5 T and 1.5 T (from the DUT's `delay_law`), 5 enable cases (power-up with no preset, enable while the clock runs, re-enable after a disable with the control voltage left, clock absent at enable and started later). They are the `--ic` axis (`vic`, `vton`, `vtdis`, `vtre`, `vtclk`, swept through `corners.supply_v`); `dllbench.py grade` reads each source back (`*_seen`, `ic_seen`, `tclk_edge`) and the run fails if an axis did not take effect.

A run passes row 8 only if the last-64-cycle predicate holds at a delay of **exactly one period** (`round(d/T) == 1`) and the control voltage stays > 50 mV from both rails. LOCK (row 12) is sampled at the end of the run and must equal that verdict; the 128-cycle rise/fall latency is graded only through `sim/lock-time` (16-cycle resolution). `record.md` counts, per request and start state, locked, exactly-one-period, row-8-pass, LOCK-consistent and multi-period corners.

On the stand-in the 0005 part-3 supervisor is not modelled, so start states 2-4 are expected to show lock at 2 T and LOCK asserted there: the bench is meant to show that, not hide it.

## Cold start

From a fresh clone with the PDK installed (`sim/pdk.json`: IHP-Open-PDK v0.3.0; `PDK_ROOT`, OSDI built by `sim/harness/common/build-osdi.sh`):

```
sim/false-lock/run.sh
```

It builds the grid requests through `sim/harness/gridspec.py` (via `sim/harness/dllbench.py`), submits each with `klt sim` (multi-unit requests go to the batch fleet; there is no local fallback and a failed submit fails the run), grades the envelopes, and writes `sim/false-lock/results/<UTC stamp>/` (decks, requests, envelopes, `record.md`; append-only). `BENCH_BUILD_ONLY=1` builds and stops. Environment knobs are listed in `sim/harness/bench-run.sh`; `BENCH_F0_HZ` picks the spec column (1e9 target, 5e8 fallback, 2e9 stretch) and `BENCH_TOL` its phase tolerance (0.02 / 0.05 / 0.01).
Exit codes: 0 pass, 1 harness fault, 3 missing prerequisite, 6 harness fine but a corner fails its row.

**STAND-IN.** The default DUT is the behavioural model in `sim/standin/`, not the item-1 netlist (#24). A result here is a result about that model, is "simulated", and does not satisfy T1 item 9. Repointing is a DUT descriptor (`BENCH_DUT=...`) with the port contract in `sim/standin/dut.json`, not a bench edit. No fleet run is recorded for this bench in this PR.
