# sim/delay-sizing

Delay-tap sizing comparison (issue #67, operator ruling r7-q57 on #58): candidate **A** (one inverting current-starved stage per tap, as decision 0010 proposes) against candidate **B** (two stages per tap, starving devices widened). Same method as `sim/delay-sanity` (ideal VBN = Vc, VBP = Vdd - Vc, 20 fF ideal tap loads, single-event delay). **All results are simulated, never measured; `results/` is append-only.** `design/` and `spec/` are not touched.

```
sim/delay-sizing/run.sh probe                   # scale probe + bench regression (ss, 1 GHz)
DS_B_SCALE=4 sim/delay-sizing/run.sh full       # A and B x ss/tt/ff x 1 GHz/500 MHz
DS_B_SCALE=4 sim/delay-sizing/run.sh fine       # finer Vc at ff
DS_B_SCALE=4 sim/delay-sizing/run.sh mc         # Monte Carlo matching, ss/1 GHz, n=32
```

Every grid is a `klt sim` request (multi-unit, so the batch fleet; no local fallback). `make_bench.py` derives the A/B decks from the committed `design/netlist/*.spice` (`area.py` gives the device-area estimate); `summarize.py` writes `record.md`.

`run.sh` does not run `design/netlist.sh --check`: host klt 0.9.2.dev writes an extra header line into every export, so the check fails on content-identical files.

Results: `results/20261107T231500Z-comparison/comparison.md` (comparison and recommendation) with the records it cites. Notes:
- `full` exits non-zero by design: Vc points in the dead zone produce no edge, as in the `delay-sanity` baseline. Those are recorded as "no edge", not dropped.
- The coarse `full` grid steps over the dead-zone edge at ff, so its "NOT covered" lines are superseded by `fine`; both are kept.
- An earlier run whose decks defined `delay_cell` twice (the committed `delay_line.spice` export embeds copies of its sub-cells) was discarded and re-run after the generator was fixed. The numbers were identical.
