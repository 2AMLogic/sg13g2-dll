# supervisor-smoke record (ss probe, issue #145)

**PROBE, not a graded spec result.** `sim/corners.json` states the reduced set
"is never a recorded result"; this run is a single-corner diagnostic and must
not be read as the supervisor's ss grade (the 45-corner grade is #41's).
Simulated, never measured.

## Question (issue #145)

PR #141 (issue #136) shortened the shared `edgedet` one-shot from five inverter
stages to three device-level stages (`XMPD1..XMND3`, `sg13_lv_pmos w=1u l=0.16u`
/ `sg13_lv_nmos w=0.5u l=0.16u`). The supervisor consumes that one-shot
untested. At ss / 1.080 V / 125 C, does `pt` still reach the plain `srlatch` --
i.e. does RST assert via the rail time-out path at all?

## Method

- Deck `decks/probe.spice` = `design/netlist/supervisor.spice` (as committed at
  `facba8b`; envelope `netlist_identity` `sha256:32c5dae5...`, byte-identical to
  the tt re-run in `../20261115T184803Z`) + `decks/sup_body.spice`, the tt smoke
  bench's stimulus unchanged -- the stimulus is not what changed.
- Two units in one request (`requests/probe.request.json`): the **question unit**
  at ss (mos_ss; the bench's passive corner section `cornerRES res_typ` kept
  typ, per `sim/corners.json`, whose corner axes are MOS x supply x temperature
  only) and a **control unit** at the bench's own tt corner (mos_tt / 1.2 V /
  27 C), so every ss observation is read against what the identical stimulus and
  capture produce where the block is known to pass.
- Graded on crossing counts and 50 %-of-Vdd crossing times of twelve nodes --
  the stimulus (`ref`), the `win_det` window samples (`xdut.xwin.a_up`,
  `xdut.xwin.a_dn_n`, `xdut.xwin.b_up`), `over_n`, the rail-comparator outputs
  (`nhi`, `near`), the counter enable (`cnt_en`), the one-shot input and output
  (`to`, `pt`), the gated set term and the latch output (`set`, `rst`) -- **not**
  on the smoke request's tt-calibrated `.meas` windows. Crossing counting is
  corner-portable, so no tt offset was re-derived for this corner (issue #145
  finding 4 answered by construction).
- Submitted through the grid/batch path (`--backend batch
  --wait-for-capacity 600`); batch job `klt-sim-26a6110f6647`, ngspice 47 on the
  fleet. The envelope records one engine warning on the ss unit ("Dynamic gmin
  stepping failed", a failed convergence aid); the transient completed.
- Per-node waveforms: `artifacts/probe/<corner>/crossings_N.raw` (full
  transient of each probed node) were produced and inspected for grading -- the
  stuck-level statements below quote them -- but are not committed: the repo
  ignores `*.raw` by policy. The committed evidence is the envelope (crossing
  counts and 50 % times per node) and the elaborated corner decks
  (`artifacts/probe/<corner>/corner.cir`).
- Reproducibility: the ss question unit of this request was also run once on
  its own (batch job `klt-sim-37a3f24d765e`) and returned identical crossing
  counts and times; the two corners below are from the combined two-unit run.

## Result

**FAILURE -- the supervisor does not respond at ss / 1.080 V / 125 C, and the
failure is upstream of the one-shot.** RST never releases from its power-up
assert; the rail time-out path never runs.

### ss unit (question corner)

| node | crossings (50 %) | behaviour |
|---|---|---|
| `ref` | 100 rises, 0.515..99.515 ns | stimulus toggles normally |
| `xdut.xwin.a_up` | 1 (rise 1.659 ns) | captures the second REF rise, then never moves again |
| `xdut.xwin.a_dn_n` | 0 | stays high |
| `xdut.xwin.b_up` | 1 (rise 1.656 ns), raw ends at 1.0799 V | **latches high and stays** -- at tt this node is low in the 0-25 ns no-fault window and only toggles when the stimulus fault changes (25.6, 50.7 ns) |
| `over_n` | 1 (fall 1.857 ns), raw ends at 0 V | **asserted permanently** from 1.86 ns |
| `nhi` | 0 | stuck high (RSTB low keeps the supervisor's own pull-up holding VCTRL at the rail) |
| `near` | 0 | stuck high |
| `cnt_en` | 0 | stuck low -- RSTB low disables the counter |
| `to` | 0 | the counter never reaches 16 cycles; the one-shot never receives an edge |
| `pt` | 0 | raw max 0.0066 V -- dead flat |
| `set` | 0 | stuck high (NAND of `over_n`=0, `pt_n`=1, `EN`=1) |
| `rst` | 0 | **stuck at 1.08 V from t=0 -- RST never releases, never re-asserts** |

### tt unit (control corner) -- same deck, same capture

| node | crossings (50 %) | behaviour |
|---|---|---|
| `ref` | 100 rises | identical stimulus |
| `xdut.xwin.a_up` | 1 (rise 1.608 ns) | same steady capture as ss |
| `xdut.xwin.a_dn_n` | 0 | same as ss |
| `xdut.xwin.b_up` | 2 (25.615, 50.705 ns) | low through the no-fault window, toggles exactly at the two stimulus fault changes |
| `over_n` | 2 (25.727, 50.820 ns) | `win_det` follows the injected faults only |
| `nhi` | 3 (5.171..52.530 ns) | power-up pull-up, then follows the loop-model rail |
| `near` | 4 (5.253..61.478 ns) | window comparator alive |
| `cnt_en` | 5 (3.817..61.764 ns) | counter enabled after each release |
| `to` | 1 (rise 78.294 ns) | 16-cycle time-out fires |
| `pt` | 2: 78.372 rise, 78.490 fall | **one-shot fires, 118.5 ps wide at tt on this load** |
| `set` | 5 (3.119..78.560 ns) | gated set term pulses on the one-shot |
| `rst` | 5: 3.549 fall (power-up release), 25.858 rise (over-delay), 51.292 fall, 78.552 rise (time-out assert), 78.624 fall | full expected sequence, RST releases and re-asserts |

### Attribution

At ss the `win_det` sample `b_up` (TAPH captured by REF) latches high at the
second REF rise (1.656 ns) where tt captures low: in the bench's no-fault window
TAPH falls only ~130 ps before each REF rise, which is inside the ss setup
window of `dffr_lv` but outside the tt one. With `b_up`, `a_up` and `a_dn_n` all
high, `over_n` asserts at 1.857 ns and holds, so `set` is held high and RST --
already asserted at power-up -- never releases. `RSTB` low keeps `cnt_en` low,
so the counter is disabled and the `to` -> `pt` -> `set` time-out path this
issue asks about never executes. The stuck level of every stage is confirmed by
its own waveform in `artifacts/`, and the tt control reproduces the full working
sequence on the identical stimulus, so the contrast is the corner, not the
probe. (The ~130 ps-vs-setup-window reading of *why* `b_up` mis-latches is
interpretation; the stuck levels and the tt/ss crossing contrast above are
measurement.)

## What this does and does not show

- **Shows (measured)**: at ss / 1.080 V / 125 C, with the committed 1 GHz smoke
  stimulus, the supervisor never releases RST and never runs its time-out path;
  the one-shot (`pt`) never fires. Per issue #145's outcome clause this measured
  failure is recorded here and the remedy is filed as a follow-up issue (the
  `win_det` sampling margins / `dffr_lv` behaviour at ss need their own decision
  record, which is out of scope here).
- **Does not show**: that the three-stage one-shot itself cannot flip the plain
  `srlatch` at ss -- `pt` never received an edge in this stimulus, so the
  one-shot/latch pair is unexercised at ss here. The one-shot pulse itself was
  measured at ss for the PFD's loading in
  `sim/pfd-fit/results/20261115T125504Z/probe_ss.envelope.json` (179.1 ps);
  a targeted ss bench for the supervisor's `pt` -> `srlatch` pair alone is part
  of the follow-up.
- The tt re-run of the unchanged smoke bench on the three-stage `edgedet`
  passed -- see `../20261115T184803Z/record.md` (all six smoke gates green, so
  the regression this probe found is ss-only).
