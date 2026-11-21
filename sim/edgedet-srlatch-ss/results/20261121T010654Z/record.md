# esrl record (issue #189)

**DIAGNOSTIC BENCH, not a graded spec result.** `sim/corners.json` states the reduced
set "is never a recorded result"; this bench answers one question (#148 acceptance
criterion 3, the follow-up the issue #145 ss probes left open): **can the three-stage
`edgedet` one-shot set the plain `srlatch` at ss when its input is driven directly?**
Simulated, never measured.

## Method

- Deck `decks/esrl.spice` = `design/netlist/lock_detector.spice` (the committed export,
  the same `edgedet`/`srlatch` subcircuits the lock detector and supervisor instantiate)
  + `decks/esrl_body.spice`: the latch is reset to a known Q = 0 (active-high R held
  0..~3 ns, then released), and `to` is driven by one ideal rising edge (30 ps slew, the
  smoke decks' own edge rate) at 5 ns -- bypassing the counter that stalls at ss,
  exactly the substitution #148 names. `lockq` drives the lock detector's own
  output-chain load (`inv_lv` + `inv2x_lv` + the row-12 20 fF on LOCK).
- Two units in one request (`requests/esrl.request.json`, composed by
  `sim/harness/gridspec.py` from the reduced set): the **question unit** at ss and a
  **tt control** on the identical deck, the #145 probe convention.
- All crossings graded at 50 % of the corner's own rail (the deck's `v(half)` node),
  never a per-corner literal; pulse widths are derived from the rise/fall crossing
  times (a file-scope `.meas` result is not readable by an in-control expression, so
  the subtraction is made here, from the two recorded crossings).
- The errored `.meas` crossing cards in the envelope, when present, are crossings that
  do not exist (e.g. no Q rise); `q_pre`, `pt_max`, `q_end` and `qb_end` are
  always-valued scalars and must resolve for a verdict.

## Environment

- ngspice (as run): ngspice 47; engine host: worker
- backend: batch
- batch jobs: {"esrl": {"job_id": "klt-sim-00c3d54286ad", "instance_type": "c7i.4xlarge", "ami_id": "ami-09c14f55df4958cbd", "lifecycle": "spot"}}
- corners (as recorded): mos_tt/1.2 V/27 C, mos_ss/1.08 V/125 C

## Result

| corner | Q before edge (mV) | `to` rise (ps) | pt rise (ps) | pt fall (ps) | pt width (ps) | Q rise (ps) | LOCK rise (ps) | Q end (mV) | QB end (mV) | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| mos_tt/1.200V/27C | 0.07 | 5000.0 | 5053.4 | 5167.9 | 114.5 | 5129.0 | 5238.7 | 1199.95 | 0.01 | SETS AND HOLDS (Q rose while pt was still high; Q holds after pt falls, QB complementary) |
| mos_ss/1.080V/125C | 0.00 | 5000.0 | 5082.1 | 5262.7 | 180.6 | 5201.5 | 5377.1 | 1079.91 | 0.02 | SETS AND HOLDS (Q rose while pt was still high; Q holds after pt falls, QB complementary) |

## What this does and does not show

- **Shows (measured)**: whether the committed three-stage one-shot, driven on `to`,
  generates a pt pulse at this corner, and whether that pulse sets the plain
  `srlatch` with Q held after pt falls (QB complementary) under the lock detector's
  own loads.
- **Does not show**: the one-shot inside the stalled supervisor/lock-detector loop
  (neither block delivers an edge at ss on the committed stimulus -- that is the
  upstream failure the issue #145 probes measured); any other corner, frequency or
  load; metastability.
- Results are simulated, never measured.

