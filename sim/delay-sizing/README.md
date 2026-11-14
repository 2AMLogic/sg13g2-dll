# sim/delay-sizing

Delay-tap sizing comparison (issue #67, operator ruling r7-q57 on #58): candidate **A** (one inverting current-starved stage per tap, as decision 0010 proposes) against candidate **B** (two stages per tap, starving devices widened). Same method as `sim/delay-sanity` (ideal VBN = Vc, VBP = Vdd - Vc, 20 fF ideal tap loads, single-event delay). **All results are simulated, never measured; `results/` is append-only.** `design/` and `spec/` are not touched.

```
sim/delay-sizing/run.sh probe                   # scale probe + bench regression (ss, 1 GHz)
DS_B_SCALE=4 sim/delay-sizing/run.sh full       # A and B x ss/tt/ff x 1 GHz/500 MHz
DS_B_SCALE=4 sim/delay-sizing/run.sh fine       # finer Vc at ff
DS_B_SCALE=4 sim/delay-sizing/run.sh mc         # Monte Carlo matching, ss/1 GHz, n=32
```

Every grid is a `klt sim` request (multi-unit, so the batch fleet; no local fallback). `make_bench.py` derives the A/B decks from the committed `design/netlist/*.spice` (`area.py` gives the device-area estimate); `summarize.py` writes `record.md`.

Results: `results/20261107T231500Z-comparison/comparison.md` (A vs B comparison and recommendation, B at 4x) with the records it cites, and `results/20261114T074618Z-comparison-3x/comparison.md` (issue #114: B at **3x** against those 4x figures, no A-vs-B recommendation) with its own two records:
- `results/20261114T071858Z-full/` B scale 3, A and B x ss/tt/ff x 1 GHz/500 MHz
- `results/20261114T073524Z-mc/` B scale 3, Monte Carlo matching, ss/1 GHz, n=32, seed 20261107

Notes:
- `full` exits non-zero by design: Vc points in the dead zone produce no edge, as in the `delay-sanity` baseline. Those are recorded as "no edge", not dropped.
- The 3x runs have **no `fine` counterpart**, so their coarse ff lines are not superseded and no ff claim should be read off them (the ss/1 GHz question #114 asks is resolved cleanly on the coarse grid). Candidate A is scale-independent and its rows in `20261114T071858Z-full/` reproduce the 4x run's figure for figure, which is the cross-check that the two runs are comparable despite different client klt versions.
- The coarse `full` grid steps over the dead-zone edge at ff, so its "NOT covered" lines are superseded by `fine`; both are kept.
- An earlier run whose decks defined `delay_cell` twice (the committed `delay_line.spice` export embeds copies of its sub-cells) was discarded and re-run after the generator was fixed. The numbers were identical.
- The recorded runs above predate `run.sh` calling `design/netlist.sh --check` (issue #71): the gate exited 3 on every block under the host klt regardless of content, so it was skipped. When the gate was made version-independent, the only difference in all nine diffs was klt's `** klt-netlist-inputs:` header line — the committed netlists these decks read were content-current, so the recorded numbers stand.
