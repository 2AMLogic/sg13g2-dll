# sim/supervisor-smoke

Smoke bench for the false-lock supervisor (`design/supervisor.sch`, issue #53).
One typical-corner transient (mos_tt + res_typ, 1.2 V, 27 °C, 1 GHz), **one unit**.
It runs through the shared single-unit runner `sim/harness/smoke-run.sh`, which
is where the backend policy for one unit -- why it runs locally and why it is
never widened into a corner or Monte Carlo grid here -- is defined.

It checks three behaviours of `design/NOTES.md` § "False-lock supervisor", with
ideal delayed copies of REF standing in for the delay line and an RC stand-in for
the loop (`decks/sup_body.spice`):

1. power-up: `RST` releases after `EN` rises and VCTRL reaches the high rail;
2. `RST` asserts for a delay of 1.8 T (inside (1.5 T, 2 T)) and releases when the
   delay is back to 0.8 T;
3. with the loop model pulling VCTRL to the low rail, the 16-cycle time-out asserts
   `RST`; and after the power-up and time-out releases the first REF edge is masked (`d_mask0`, `d_mask_timeout`).

```
design/netlist.sh && sim/supervisor-smoke/run.sh
```

Writes `results/<UTC stamp>/` (decks, request, envelope, `record.md`; append-only).
Exit 0 pass, 3 missing prerequisite, 6 a gate failed or the run is NOT-RUN (the
record then quotes the backend/engine error verbatim).

The `td=` values in `requests/sup.request.json` come from the first committed run
(a file-scope `.meas` cannot read another `.meas`); re-derive them if the design
or stimulus changes. Limits are smoke gates, not spec numbers. Results are
simulated, never measured. No negative control (mask removed) was run.

## Evidence currency and the ss probe (issue #145)

`results/20261115T184803Z/` is the record on the **three-stage device-level
`edgedet`** (`XMPD1..XMND3`, 0.16 µm devices, PR #141) and passes all six gates;
its provenance section states the commit and the chain. The two earlier records
(`20261105T052155Z`, `20261114T092421Z`) pre-date that chain and are superseded
for it.

The ss corner is covered by a **probe, not a graded result**:
`results/20261115T185844Z-probe/` runs the same stimulus at ss / 1.080 V / 125 °C
plus a tt control unit, graded on crossing counts (corner-portable; no `td=`
re-derivation), and **measures a failure**: RST never releases at ss (the
`win_det` TAPH sample mis-latches, `over_n` holds, the counter stays disabled,
the one-shot never fires). See that directory's `record.md` for method and
attribution, and `design/NOTES.md` § "Evidence status" for the summary.

`results/20261121T004400Z-setup/` (issue #189) is the follow-up **setup-margin
probe** of that mis-latch: the committed `win_det` with its supervisor-internal
loads, the no-fault phase's own 30 ps slew, the TAPH-fall-to-REF-rise lead
swept through `corners.supply_v` (an alter, not `corners.params`). Measured
bracket: ss captures low only for leads ≥ 110 ps and latches the stale high
through 100 ps — the no-fault phase's own lead — while the tt control needs
only (60, 80] ps: a cell-speed failure of the sampler at ss, not a
sampling-edge construction artefact. See that directory's `record.md`.
