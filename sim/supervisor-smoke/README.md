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
