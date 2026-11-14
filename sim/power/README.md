# sim/power

Spec row 10: average supply power over the 64 locked cycles at f0, over all 45 corners; the limit (5 mW target) applies to the worst corner.

Simulated, never measured.

One request, 45 units, `pavg` in mW from `-i(Vdd)*v(vdd)`. The tt / 1.20 V / 27 C value is in the same table. **The stand-in draws no supply current, so `pavg` is 0 there and means nothing**; the bench is only useful once repointed at the item-1 netlist. `BENCH_PMAX_MW` sets the column's limit.

The harness enforces that: the limit is attached to `pavg` only when the DUT descriptor declares `supply_current: true` (`sim/standin/dut.json` declares `false`). On a DUT that draws no supply current the value is recorded with no limit and `record.md` reports row 10 **NOT GRADED on this DUT** rather than claiming a pass against a 0 mW reading. A descriptor for the item-1 netlist sets the flag `true` and gets the 5 mW limit; the spec row and its limit are unchanged either way.

## Cold start

From a fresh clone with the PDK installed (`sim/pdk.json`: IHP-Open-PDK v0.3.0; `PDK_ROOT`, OSDI built by `sim/harness/common/build-osdi.sh`):

```
sim/power/run.sh
```

It builds the grid requests through `sim/harness/gridspec.py` (via `sim/harness/dllbench.py`), submits each with `klt sim` (multi-unit requests go to the batch fleet; there is no local fallback and a failed submit fails the run), grades the envelopes, and writes `sim/power/results/<UTC stamp>/` (decks, requests, envelopes, `record.md`; append-only). `BENCH_BUILD_ONLY=1` builds and stops. Environment knobs are listed in `sim/harness/bench-run.sh`; `BENCH_F0_HZ` picks the spec column (1e9 target, 5e8 fallback, 2e9 stretch) and `BENCH_TOL` its phase tolerance (0.02 / 0.05 / 0.01).
Exit codes: 0 pass, 1 harness fault, 3 missing prerequisite, 6 harness fine but no pass verdict -- a corner fails its row, or the row is NOT GRADED on this DUT; `record.md` says which. **On the default stand-in DUT this bench exits 6**, not 0: `sim/standin/dut.json` declares `supply_current: false`, so row 10 is NOT GRADED and there is no pass to report. A DUT descriptor with `supply_current: true` is what makes 0 reachable here.

**STAND-IN.** The default DUT is the behavioural model in `sim/standin/`, not the item-1 netlist (#24). A result here is a result about that model, is "simulated", and does not satisfy T1 item 9. Repointing is a DUT descriptor (`BENCH_DUT=...`) with the port contract in `sim/standin/dut.json`, not a bench edit. No fleet run is recorded for this bench in this PR.
