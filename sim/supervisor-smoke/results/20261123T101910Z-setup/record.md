# supervisor-smoke record (win_det setup-margin sweep replay, issue #195)

**PROBE, not a graded spec result.** `sim/corners.json` states the reduced set
"is never a recorded result"; this run is a single-cell diagnostic and must not
be read as the supervisor's ss grade (the 45-corner grade is #41's).
Simulated, never measured.

## Question (issue #195, remedy replay of the issue #189 sweep)

`win_det.XBUP` is now `dffr_fast` (spec/decisions/0017: the dffr_lv topology
with the D-path and master-loop gates scaled 2x and the slave clocked through
an `inv_lv` pair). On the committed `dffr_lv` the ss bracket was
[largest failing 100 ps, smallest passing 110 ps] and the no-fault phase's own
lead is exactly 100 ps (`../20261121T004400Z-setup/record.md`). **What is the
bracket on the remedied sampler, how much headroom does the 100 ps operating
point get, and does the capture window leave a transient half-rail excursion
on `b_up` that propagates to `over` (over_n inside supervisor)?**

## Method

- Replay of the issue #189 sweep with the revised netlist. Deck
  `decks/sup_setup.spice` = `design/netlist/supervisor.spice` regenerated from
  the remedy (envelope `netlist_identity`
  `sha256:f9909bb81b0dab0e96084eb919cb6988e6e1d9d3ed9724fb47a435524869b3f1`)
  + the issue #189 probe body byte-identical: same stimulus (REF is the smoke
  bench's own clock `Vck`, 0.5 ns base delay, 30 ps edges, 1 ns period,
  vdd-scaled; TAPN the unchanged 0.8 T copy; TAPH one pulse whose fall 50 %
  point sits `lead` before the second REF rise), same loads (the committed
  `win_det` itself; REF drives `XIREF` + the three sampler clock pins; TAPH
  drives `XBUP.D`, now the `dffr_fast` input; `over` carries the `XIPO`
  `inv_lv` load), same lead lists (ss 22 leads, tt 7), same `Vlead` alter
  sweep through `corners.supply_v`.
- Grading unchanged: `bup_end` = `v(xwin.b_up)` settled at 2.4 ns against
  50 % of the corner's own rail; every unit's true lead derived in this record
  from the recorded 50 % crossing times `t_ref_r2 - t_taph_f` (all 29 units
  measured their intended lead exactly; the table below quotes them).
  `t_bup_r` errors exactly when `b_up` never crosses 50 % at all — on the
  remedied cell that is the pass case at every capture-low lead (no excursion,
  see below), not a fault.
- **Added for this replay** (issue #195 Test Plan): `bup_max` / `over_pk`, the
  peak of `v(xwin.b_up)` and `v(over)` over 1.3-2.4 ns — the transient
  excursion check. On the committed cell at its capture-low leads (110-140 ps)
  `b_up` crossed half-rail before settling low; the question here is whether
  the remedied cell's capture window leaves such an excursion and whether it
  reaches `over` (whose supervisor-internal image `over_n` gates `set`).
- Submitted through the grid/batch path (`--backend batch
  --wait-for-capacity 600`); batch jobs `klt-sim-dd632feb59ff` (ss, 22 units)
  and `klt-sim-45666f940182` (tt, 7 units), ngspice 47 on the fleet. Both
  envelopes carry klt exit 4 / unit status `error` from lead 80 ps up (ss) and
  60 ps up (tt): every one of those is the `t_bup_r` no-crossing pass
  observation above, the same envelope shape as the committed #189 sweep
  (`../20261121T004400Z-setup/supss_setup.envelope.json`, also `status=error`
  exit 4). Committed evidence: both envelopes, the elaborated corner decks
  (`artifacts/supss_setup/`, `artifacts/suptt_setup/`), all three requests and
  this record.

## Result

**The ss bracket moved from (100, 110] ps to (70, 80] ps: the largest failing
lead is 70 ps and the smallest passing lead is 80 ps, so the committed 100 ps
no-fault lead now clears the ss setup requirement by ≥ 20 ps (10 ps sweep
resolution) instead of failing it by ≤ 10 ps. The tt control moved from
(60, 80] ps to (40, 60] ps. At the 100 ps operating point both corners capture
low with no half-rail excursion at all: `b_up` peaks at 8.7 mV (ss) / 10.6 mV
(tt) against a 540 mV / 600 mV half rail, and `over` never leaves the floor
(0.51 mV / 0.68 mV peak) — no transient reaches `over_n`.**

| lead (ps, from the recorded 50 % crossings) | ss `b_up` settled | ss `bup_max` | ss `over_pk` | tt `b_up` settled | tt `bup_max` |
|---|---|---|---|---|---|
| -50 (TAPH falls after the edge) | **high** (1.0780 V — the positive control) | 1.097 V (latched) | 1.080 V (over asserts, as it must with b_up high) | high (1.1991 V) | 1.221 V |
| -20 / 0 / 20 / 40 | high | 1.097 V | 1.080 V | 40: high (largest failing) | 1.221 V |
| 60 | high (largest failing) | 1.097 V | 1.080 V | **low** (smallest passing) | 10.6 mV |
| 70 | high | 1.097 V | 1.080 V | not swept | — |
| 80 | **low** (smallest passing) | 8.7 mV | 0.51 mV | low | 10.6 mV |
| 100 (the no-fault phase's own lead) | **low — the ss failure removed** (48 µV) | 8.7 mV | 0.51 mV | low (−7 µV) | 10.6 mV |
| 110 .. 400 | low | 8.7 mV | 0.51-0.53 mV | not swept | — |

- The -50 ps control captures high at both corners: the faster D-path does not
  break the direction the sampler must not lose (TAPH still high at the edge ⇒
  b_up high).
- The excursion columns are the new evidence: on the committed cell the
  capture-low leads 110-140 ps each crossed half-rail first (`t_bup_r` fired);
  on the remedied cell `t_bup_r` errors at every capture-low lead from 80 ps
  up — `b_up` never reaches half rail during the capture window, and `over_pk`
  stays at the sub-mV floor, so nothing propagates toward `set`. (The
  intermediate sizing step of spec/decisions/0017 — the scaled D-path without
  the slave `inv_lv` pair — settled low at 100 ps but peaked at 0.92 V with a
  0.62 V `over` peak and pulsed `set` every REF cycle at ss in the full
  supervisor; that observation is why the pair is in the landed cell.)
- ss `bup_end` at the passing leads reads 48-71 µV (not sub-µV as at tt):
  the ss unit's 100 ns of fleet-run capture leaves `b_up` a hair above the
  floor. Both are far below the 0.54 V half rail; the verdict is unaffected.

### Attribution

The ss setup failure of issue #189/#145 was a cell-speed failure of the D=0
(TAPH-fall) path of the shared `dffr_lv` at the corner; scaling exactly that
path (and letting the master resolve before the slave clocks) moves the ss
requirement 30 ps clear of the 100 ps the d = 0.8 T phase provides. The
requirement and the remedy are both bracketed at the sweep's 10 ps resolution;
the no-fault lead sits at 100 ps with ≥ 20 ps of headroom below the
smallest passing lead.

## What this does and does not show

- **Shows (measured)**: the ss and tt setup brackets of the remedied sampler
  under the smoke bench's own slew (30 ps edges) and loads, from the same
  sweep, grading and true-lead derivation as the committed #189 baseline; the
  absence of a half-rail `b_up` excursion and of any `over`-net movement at
  the capture-low leads, both corners; the -50 ps positive control.
- **Does not show**: the other two `win_det` samplers (`a_up`, `a_dn` —
  unchanged cells, not re-bracketed here); hold-time behaviour (TAPH rising
  through the clock edge) — the b_up direction the over-delay window needs at
  d near 2 T; mismatch spread (Monte Carlo); any corner other than the two
  reduced-set points; that the excursion-free window survives the closed loop
  (needs the `sim/false-lock` bench). The full-supervisor response at ss is
  `../20261123T101910Z-probe/record.md`; the tt smoke gates are
  `../20261123T103022Z-smoke/record.md`.
- Results are simulated, never measured.
