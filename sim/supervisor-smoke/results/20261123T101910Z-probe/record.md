# supervisor-smoke record (ss probe replay, issue #195)

**PROBE, not a graded spec result.** `sim/corners.json` states the reduced set
"is never a recorded result"; this run is a two-corner diagnostic and must not
be read as the supervisor's ss grade (the 45-corner grade is #41's).
Simulated, never measured.

## Question (issue #195, replay of the issue #145 two-unit probe)

With `win_det.XBUP` on the new `dffr_fast` (spec/decisions/0017), does the
full supervisor respond at ss / 1.080 V / 125 C on the committed 1 GHz smoke
stimulus — RST released in the 0.8 T no-fault phase, asserted by the 1.8 T
over-delay fault, released on return, and the 16-cycle low-rail time-out
traced through `to`, `pt`, `set` and RST — with the tt control corner
reproducing its committed working sequence on the identical stimulus?

## Method

- The issue #145 comparison request replayed verbatim
  (`requests/probe.request.json`, byte-identical to
  `../20261115T185844Z-probe/requests/probe.request.json`: same 12 probed
  nodes, same crossing grading, same `tran 10p 100n`, same two units — ss
  question corner and tt control). The deck `decks/probe.spice` is the only
  thing that changed: `design/netlist/supervisor.spice` regenerated from the
  remedy (envelope `netlist_identity`
  `sha256:5789b6699877ab8a7258142e3676d357ea05bc9792290a87ee4a08fc05cc476b`)
  + `decks/sup_body.spice`, the smoke bench's stimulus unchanged (two delayed
  copies of REF; d = 0.8 T to 25 ns, 1.8 T to 50 ns, 0.8 T with VCTRL pulled
  to the low rail after; EN low until 3 ns).
- Submitted through the grid/batch path (`--backend batch
  --wait-for-capacity 600`); batch job `klt-sim-7e0b469a052b`, ngspice 47 on
  the fleet, both units `pass`. Committed evidence: the envelope, the
  elaborated corner decks (`artifacts/probe/<corner>/corner.cir`), the request
  and this record.

## Result

**PASS at both corners. At ss the supervisor now runs the full expected
sequence — RST releases from the power-up assert, follows the injected
over-delay fault, and the low-rail time-out fires through `to` -> `pt` ->
`set` into RST — where the committed cell held RST stuck high from t = 0
(`../20261115T185844Z-probe/record.md`). The tt control reproduces its
committed sequence with the tens-of-ps shifts the faster sampler and the
slave-clock pair cost.**

### ss unit (the corner the #145 probe failed)

| node | crossings (50 %) | behaviour |
|---|---|---|
| `ref` | 100 rises, 0.515..99.515 ns | stimulus toggles normally |
| `xdut.xwin.a_up` | 1 (rise 1.661 ns) | unchanged cell, unchanged steady capture |
| `xdut.xwin.a_dn_n` | 0 | stays high, as at tt |
| `xdut.xwin.b_up` | 2 (25.773, 50.882 ns) | **low through the no-fault window** (the #145 failure: 1 rise at 1.656 ns, stuck at 1.0799 V), toggles exactly at the two stimulus fault changes — tt control: 25.682, 50.740 ns |
| `xdut.over_n` | 2 (25.952, 51.066 ns) | `win_det` follows the injected faults only |
| `nhi` | 3 (6.149, 31.114, 53.532 ns) | power-up pull-up, then follows the loop-model rail |
| `near` | 4 (6.281 .. 65.574 ns) | window comparator alive |
| `cnt_en` | 5 (4.208 .. 66.002 ns) | counter enabled after each release |
| `to` | 1 (rise 82.729 ns) | 16-cycle time-out fires (tt: 78.294 ns) |
| `pt` | 2: 82.852 rise, 83.041 fall | **one-shot fires, 189 ps wide at ss on this load** — the #145 open question (does `pt` still drive the plain `srlatch` at ss) answered on the live path |
| `set` | 5 (3.151, 26.030, 51.130, 83.003, 83.152 ns) | gated set term: EN release, over-delay, fault end, time-out assert/release — **one crossing per stimulus event, no per-cycle chatter** |
| `rst` | 5: 3.817 fall (power-up release), 26.160 rise (over-delay), 51.802 fall (release on return to 0.8 T), 83.137 rise (time-out assert), 83.257 fall (release) | **the full expected sequence** — tt control: 3.549 / 25.926 / 51.326 / 78.552 / 78.624 ns |

### tt unit (control corner) — same deck, same capture

Full working sequence as in `../20261115T185844Z-probe/` (its rst crossings
were 3.549 / 25.858 / 51.292 / 78.552 / 78.624 ns; the over-delay assert and
release shift by +68 ps / +34 ps — 25.926 vs 25.858, 51.326 vs 51.292 — from
the `dffr_fast` slave-clock pair's two `inv_lv` delays and the master-loop
resizing, and the time-out block is unchanged). All six smoke-gate timings
land inside the committed gate windows: see `../20261123T103022Z-smoke/`.

### Attribution

The #145 ss failure was upstream of the one-shot: the `win_det` TAPH sample
mis-latched high at the second REF rise, `over_n` asserted permanently and
`set` was held, so RST never released and the time-out path never ran. With
the sampler remedy the same stimulus produces the intended sequence at ss:
`b_up` captures low in the no-fault phase (the setup bracket of
`../20261123T101910Z-setup/` shows the 100 ps lead clearing the ss requirement
by ≥ 20 ps), `over_n` asserts only on the 1.8 T fault, the counter runs, and
`to` -> `pt` -> `set` -> RST executes the low-rail time-out. No transient
`set` chatter appears at either corner (the excursion that the intermediate
sizing produced is absent from the landed cell — see the decision record).

## What this does and does not show

- **Shows (measured)**: the full supervisor response at ss / 1.080 V / 125 C
  and tt / 1.2 V / 27 C on the committed stimulus, graded on the 12 probed
  nodes' crossing counts and 50 % times, with the tt control inside the same
  run; the ss time-out path exercised end-to-end (`to`, `pt`, `set`, `rst`).
- **Does not show**: mismatch spread (Monte Carlo); the ff reduced-set corner
  and any full PVT grading (#41); the closed loop (`sim/false-lock` bench —
  that the supervisor never fires during a normal lock); metastability of the
  window samples near d = T; the (2 T, 3.5 T) coverage gap. The tt smoke
  gates (including both first-edge-mask gates) are
  `../20261123T103022Z-smoke/record.md`.
- Results are simulated, never measured.
