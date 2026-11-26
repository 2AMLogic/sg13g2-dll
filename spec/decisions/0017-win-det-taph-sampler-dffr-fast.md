# 0017 — Use a local `dffr_fast` for the `win_det` TAPH sampler

- **Status**: proposed — becomes ratified only by the operator's approval and merge of the PR that carries this record. Agents do not approve it or mark anything ratified.
- **Date**: 2026-11-23
- **Decided by**: Builder agent, issue #195 (the remedy follow-up #145/#189/#148 named in `design/NOTES.md`)
- **Consumes**: [0005](0005-false-lock-exclusion.md) (part 3, the over-delay window); [0008](0008-false-lock-argument.md) (the start-up/first-edge mask requirement); [0015](0015-pfd-buffered-lane-output.md) (the 1 GHz target and the shared edge detector stay)
- **Related**: #148 (parent); #189/#193 (the ss setup bracket this remedy answers); #145 (the ss probe that found the failure); #196 (the lock-detector VCTRL sensor, explicitly out of scope here)

## The failure this decision answers

At ss / 1.080 V / 125 C the supervisor held RST high through the 1 GHz smoke
stimulus: the `win_det` sample `b_up` (TAPH sampled by REF, a shared
`dffr_lv`) latched the stale high at the second REF rise, `over_n` asserted
permanently, `set` was held, and the rail time-out never ran
(`sim/supervisor-smoke/results/20261115T185844Z-probe/`). The issue #189 setup
sweep bracketed the cause as a cell-speed failure: at ss the sampler captures
TAPH low only for TAPH-fall-to-REF-rise leads ≥ 110 ps, the no-fault
d = 0.8 T phase provides exactly 100 ps (50 % crossings), and the tt control
needs only (60, 80] ps
(`sim/supervisor-smoke/results/20261121T004400Z-setup/`).

## Decision

**Replace exactly one instance: `win_det.XBUP` (and only it) instantiates the
new `dffr_fast`.** The shared `dffr_lv`, every leaf it is built from, and every
other `dffr_lv` consumer — `win_det`'s own `a_up`/`a_dn`, the `timeout_cnt`
stages, `refmask`'s enable flop, the `lock_detector` samplers and counter —
are untouched, so the committed records that cite those cells stay valid. The
same locality pattern as `srlatch_fast`/`srlatch_buf` (0011/0015): a shared
cell is never resized in place for one consumer; a named variant is.

`dffr_fast` (defined in `design/tools/cells.py`, generated, not hand-drawn) is
the `dffr_lv` master/slave topology with the same ports and rising-edge
assignment. It combines two changes.

1. **The D=0 (TAPH-fall) master path is scaled 2x.** The path that lost the
   ss race is `D -> XID -> XRM -> XQMB -> XQM` (+ master-loop regen) racing
   the cut-off `CK -> XIC -> ckb-side`: exactly its stages are scaled — `XID`
   `inv_lv` -> `inv2x_lv`, `XRM`/`XQM` `nand2_lv` -> `nand2x_lv`, `XQMB`
   `nand3_lv` -> the new `nand3x_lv` (P 2 µm / N 3 µm, beside the issue #113
   2x family). `XIC`, `XSM` and the slave gates keep their original sizes.
   When `ckb` is low, the series devices in `XSM` and `XRM` isolate the
   opaque master from `D`. As in `dffr_lv`, `CLRB` clears both latches.
2. **The slave is clocked through one `inv_lv` pair (`XD1`/`XD2` -> `ckd`).**
   The pair delays slave enable on REF rise to give the master time to resolve.
   The figures reported for the intermediate sizing without the pair are
   **unverified design observations**, including the comparison in the
   [setup record](../../sim/supervisor-smoke/results/20261123T101910Z-setup/record.md).
   No intermediate deck, request or result accompanies the reported ss peaks
   of 0.92 V at `b_up` and 0.62 V at `over` at 100 ps lead, or the 144
   `set` crossings in the full supervisor. The committed
   replays below exercise both changes together. At ss and 100 ps lead,
   `b_up` peaks at 8.7 mV and `over` at 0.51 mV. In the full-supervisor probe,
   `set` crosses once per stimulus event.

### Nominal over-delay window and tested phases (0005 part 3)

The predicate `OVER = b_up & a_up & ~a_dn` gives the ideal window
d in (1.5 T, 2 T). `a_up` and `b_up` use the rising REF edge, and `a_dn`
uses the falling REF edge via `refb`. Although `XAUP` and `XBUP` share REF at
their clock pins, each has its own `XIC` inverter and local `ckb` net.
Upsizing `XBUP.XRM` raises the summed gate width on that `ckb` from 4.5 to
6.5 µm. Its `XIC` can therefore close the master at a different time from
`XAUP.XIC`.

At ss and tt the full-supervisor probes release RST at d = 0.8 T and assert
it for the fault at d = 1.8 T. The setup sweep brackets capture for a
**falling** TAPH. The effective aperture for a **rising** TAPH near 2 T and
the physical window boundaries remain uncharacterized. Relative to the #145
tt control, RST asserts 68 ps later for the over-delay fault and releases
34 ps later. Both times fall within the committed smoke-gate limits.

### Why first-edge masking (0008) is preserved

`refmask` is untouched — its `XEN` flop is the shared `dffr_lv`, `RSTB`-cleared
and clocked on the falling REF edge, exactly as 0008 requires. Both mask gates
(`d_mask0`, `d_mask_timeout`) pass on the revised netlist at tt (evidence
below).

### What 0015 keeps

The 1 GHz target stands (the remedy is sized against the 1 GHz smoke
stimulus); the shared `edgedet` one-shot is untouched — and is now
*exercised* at ss on the live `to` -> `pt` -> `set` -> RST path, which the
#145 failure had starved of an edge (the ss one-shot width on this load:
189 ps, vs 118.5 ps at tt in #145).

## Evidence (simulated, never measured)

All from the revised `design/netlist/supervisor.spice`
(`sha256:567be887ad74152b5b9991f6b93573106e341e03bed6110ba552b5f68613a884`;
the envelopes' `netlist_identity` hashes the staged decks — the sweep deck
`sha256:f9909bb81b0dab0e96084eb919cb6988e6e1d9d3ed9724fb47a435524869b3f1`,
the probe and smoke decks
`sha256:5789b6699877ab8a7258142e3676d357ea05bc9792290a87ee4a08fc05cc476b`),
batch fleet, ngspice 47, reduced-set corners only (never a graded result; the
45-corner grade is #41's):

1. **Setup sweep replay**
   (`sim/supervisor-smoke/results/20261123T101910Z-setup/`, jobs
   `klt-sim-dd632feb59ff` ss / `klt-sim-45666f940182` tt): the ss bracket
   moves from (100, 110] ps to **(70, 80] ps** — largest failing 70 ps,
   smallest passing 80 ps — so the committed 100 ps no-fault lead clears the
   ss requirement by ≥ 20 ps with the bench's ideal 30 ps edges and loads
   (10 ps sweep resolution). tt moves from (60, 80] to (40, 60] ps. At the
   100 ps operating point: capture low at both corners with no half-rail
   excursion (`bup_max` 8.7 mV ss / 10.6 mV tt; `over_pk` 0.51 / 0.68 mV).
   The -50 ps control (TAPH falls after the edge) still captures high at both
   corners.
2. **Two-unit probe replay**
   (`sim/supervisor-smoke/results/20261123T101910Z-probe/`, job
   `klt-sim-7e0b469a052b`): the issue #145 comparison request verbatim on the
   revised deck. ss: RST runs the full expected sequence (release 3.817 ns,
   over-delay assert 26.160 ns at the 1.8 T fault, release 51.802 ns, time-out
   assert 83.137 ns, release 83.257 ns); `b_up` low through the no-fault
   window; `set` crosses exactly once per stimulus event. tt control: its
   committed sequence reproduced. Both units pass.
3. **tt smoke gates**
   (`sim/supervisor-smoke/results/20261123T103022Z-smoke/`): all six gates
   pass on the revised netlist, including `d_mask0` 1.026 ns and
   `d_mask_timeout` 0.951 ns.

## Costs and what is not established

`XBUP` grows from 10 to 12 leaf instances. The following sums count transistor
gate widths driven directly by each `XBUP` input in `design/netlist/supervisor.spice`.

| Input | `dffr_lv` | `dffr_fast` |
|---|---|---|
| TAPH (`D`) | `XID` 1.5 + `XSM` 2.5 = **4.0 µm** | `XID` 3.0 + `XSM` 2.5 = **5.5 µm** |
| REF (`CK`) | `XIC` 1.5 + `XSS` 2.5 + `XRS` 2.0 = **6.0 µm** | `XIC` 1.5 + `XD1` 1.5 = **3.0 µm** |

`XID` accounts for the entire 1.5 µm increase on TAPH. The wider `XQMB`
(`nand3x_lv`) sits inside the master. On the clock path, `ckd1` drives
`XD2`, and `ckd` drives `XSS` and `XRS`. Effective input capacitance and
slew with a real tap buffer require separate characterization. The smoke
bench drives TAPH and REF with ideal sources. The real-line tap-buffer
drive is part of #41.

- **Not established**: mismatch spread (no Monte Carlo run — the bracket is a
  nominal-corner bracket); hold-time behaviour of `b_up` (TAPH rising through
  the REF edge — the direction the window needs at d near 2 T); the ff
  reduced-set corner and full PVT (#41); the closed loop (`sim/false-lock`
  bench); the (2 T, 3.5 T) coverage gap (unchanged by this record); that the
  a_up/a_dn samplers (unchanged cells) meet their own margins at ss.
- This record changes no `spec/` row and no gate limits; the smoke request
  `sim/supervisor-smoke/requests/sup.request.json` is untouched (its gates
  pass un-re-derived).
