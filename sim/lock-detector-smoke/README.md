# sim/lock-detector-smoke

Smoke bench for the lock detector (`design/lock_detector.sch`, issue #54). One
typical-corner transient (mos_tt + res_typ + cap_typ, 1.2 V, 27 °C, 1 GHz), **one
unit**. It runs through the shared single-unit runner
`sim/harness/smoke-run.sh`, which is where the backend policy for one unit --
why it runs locally and why it is never widened into a corner or Monte Carlo
grid here -- is defined.

The stimulus is ideal (`decks/ld_body.spice`): TAPN is REF delayed by T plus an
error e, VCTRL an ideal source, LOCK loaded with 20 fF. Timeline:

| ns | e | VCTRL | expected |
|---|---|---|---|
| 0-60 | +240 ps | quiet | LOCK stays 0 |
| 60-220 | 0 | ±15 mV, 50 MHz | LOCK stays 0 |
| 220-520 | 0 | quiet | LOCK rises within 192 cycles of 220 ns (64-cycle predicate + 128 lag) |
| 520-580 | +240 ps (60 cycles) | quiet | LOCK falls within 128 cycles |
| 580-800 | 0 | quiet | LOCK rises again |

```
design/netlist.sh && sim/lock-detector-smoke/run.sh
```

Writes `results/<UTC stamp>/` (decks, request, envelope, `record.md`; append-only).
Exit 0 pass, 3 missing prerequisite, 6 a gate failed or the run is NOT-RUN (the
record then quotes the backend/engine error verbatim). Takes several minutes.

Limits are smoke gates derived from row 12, not spec numbers; the `td=` values in
`requests/ld.request.json` follow the timeline above. In the committed record the
`lock_max_before_220n` row is in volts although the column header says seconds
(the shared summariser has one unit column). Results are simulated, never
measured.

What it does **not** show: the width of the delay window (e = 0 accepted and
e = +240 ps rejected only; see `design/NOTES.md` "Not met / not established"),
rejection of a harmonic lock, the 5 mV threshold, or any other corner or frequency.
No negative control (e.g. window forced open) was run.
