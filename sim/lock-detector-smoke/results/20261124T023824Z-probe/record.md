# lock-detector-smoke record (ss/tt two-unit probe on the revised `vmov_cmp`, issue #196)

**PROBE, not a graded spec result.** `sim/corners.json` states the reduced set "is never a recorded
result"; this is a two-unit diagnostic and must not be read as the lock detector's corner grade (#41's).
Simulated, never measured.

## Question

Issue #145's probe (`../20261115T185846Z-probe/`) measured `vmov_cmp` stuck low at ss / 1.080 V / 125 °C for
the whole 800 ns, so `LOCK` never rose. With the replica-referenced threshold stage of decision
[0017](../../../../spec/decisions/0017-vmov-cmp-replica-threshold.md), does `LOCK` assert, release and
reacquire at ss on the identical stimulus, and does the ripple phase still keep it down?

## Method

- Request `requests/probe.request.json` is the #145 request, **byte-identical**, including its two units (ss =
  mos_ss / 1.080 V / 125 °C; tt control = mos_tt / 1.2 V / 27 °C; bench passive sections typ) and its twelve
  crossing-count measurements. Only the deck differs: `decks/probe.spice` = the regenerated
  `design/netlist/lock_detector.spice` (this branch, commit `a1fe9a5`; deck identity
  `sha256:b187849e9150dfafacd143e59c69a67b4e1a9d24b3f48563a9f6daa2043bd3ce`) + the tt smoke bench's
  stimulus body, unchanged (60–220 ns ±15 mV 50 MHz ripple on VCTRL = 0.600 V, +240 ps error 0–60 and 520–580 ns,
  `Cl` = 20 fF on `LOCK`).
- Submitted `--backend batch --wait-for-capacity 600`; batch job `klt-sim-4e6f46403325`, ngspice 47, 391 s,
  both units `pass` (a pass here means the measurements were produced; the grading is below).
- Per-node waveforms (`artifacts/probe/<corner>/crossings_N.raw`, ASCII) are produced but not committed (the
  repo ignores `*.raw`). The 50 %-of-Vdd crossing times below were extracted from them with a 20-line
  linear-interpolation script over the raw `time`/`v` pairs; the committed envelope carries the crossing
  **counts**, which agree with the raw files (e.g. `t_lock` 3, `t_still` 16 at ss and 32 at tt).

## Result (crossing times, ns; r = rise, f = fall)

| node | ss / 1.080 V / 125 °C | tt / 1.200 V / 27 °C |
|---|---|---|
| `still` (16 / 32 crossings) | pulses with the ripple, last fall 204.45, **settles high 225.55** | pulses with the ripple, last fall 212.80, **settles high 222.88** |
| `good` rise after the ripple | 226.32 | 223.39 |
| `to` rises (counter reaches 128) | 356.53, 711.53 | 352.81, 709.81 |
| `pt` pulse | 356.65 r, 356.84 f; 711.66 r, 711.84 f | 352.89 r, 353.01 f; 709.89 r, 710.01 f |
| `lockq` | 356.78 r, 521.26 f, 711.78 r | 352.97 r, 521.00 f, 709.97 r |
| **`LOCK`** | **356.95 r, 521.42 f, 711.95 r** | **353.08 r, 521.10 f, 710.08 r** |

- `LOCK` has no crossing before 353 ns at either corner: it stays 0 through the 60–220 ns ripple phase
  (the sensor's `still` pulses high for about 0.7 ns per 20 ns ripple cycle at ss, never long enough to
  complete the 128-cycle count) and through the settling that follows.
- Assertion lag from the end of the ripple (220 ns): 136.95 ns at ss, 133.08 ns at tt. Release lag from the
  +240 ps error at 520 ns: 1.42 ns at ss, 1.10 ns at tt. Reacquisition at 711.95 ns (ss) / 710.08 ns (tt), 131.95 /
  130.08 ns after the error ends at 580 ns. The tt smoke gates of `../20261124T023824Z-smoke/` (assertion window
  284–412 ns, release 520–648 ns, reacquisition 644–772 ns) contain the ss times as well, but they were
  calibrated at tt and are quoted here only as a reference, not as an ss gate.
- The #145 failure (`still` flat at about 0 V, `good` and `to` and `pt` dead for 800 ns) is gone at ss. The `to` →
  `pt` → latch path that probe could not exercise at ss executes at ss (`pt` pulse 180–190 ps wide, `lockq` sets
  within 130 ps of its rise).

## What this does not show

One ss point and one tt point; no other corner, supply or temperature; no mismatch or Monte Carlo; ideal
stimulus; the 5 mV threshold is bracketed in `../20261124T024845Z-stepprobe/`, not here. Residual
behaviour not explained here: `still` at ss has half the crossings of tt in the ripple phase (16 against 32);
it was not traced to a device or a stage.
