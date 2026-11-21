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

## Evidence currency and the ss probe (issue #145)

`results/20261115T184954Z/` is the record on the **three-stage device-level
`edgedet`** (`XMPD1..XMND3`, 0.16 µm devices, PR #141) and passes all five gates;
its provenance section states the commit and the chain. The two earlier records
(`20261105T091102Z`, `20261114T091558Z`) pre-date that chain and are superseded
for it.

The ss corner is covered by a **probe, not a graded result**:
`results/20261115T185846Z-probe/` runs the same stimulus at ss / 1.080 V / 125 °C
plus a tt control unit, graded on crossing counts (corner-portable; no `td=`
re-derivation), and **measures a failure**: `vmov_cmp` never asserts `still` at
ss, so `bad` holds, the counter stays cleared, and LOCK never rises. See that
directory's `record.md` for method and attribution, and `design/NOTES.md`
"Not met / not established" for the summary.

`results/20261121T004307Z-dcprobe/` (issue #189) is the follow-up **DC probe**
of that failure: a settled `.dc` sweep of VCTRL through the standalone
`vmov_cmp` at the reduced-set corners. Measured: the `STILL=1` quiet window is
[0, 0.477) V at ss (the smoke's 0.585–0.615 V band is outside it — the failure
is static common-mode bias, not ripple or settling), [0, 0.6125) V at tt
(12.5 mV above the nominal 0.600 V) and [0, 0.8523) V at ff. See that
directory's `record.md`. The isolated one-shot/latch set path the ss probe
left unexercised is covered by `sim/edgedet-srlatch-ss/` (it works at ss).
