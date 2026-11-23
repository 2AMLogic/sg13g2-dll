# 0017 — `win_det`'s TAPH sampler moves to a local `dffr_fast`; the shared `dffr_lv`, the sampling instants and the window stay

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
the `dffr_lv` topology with the same port list and the same cell edges, and
two changes, each answering one measured failure mode:

1. **The D=0 (TAPH-fall) master path is scaled 2x.** The path that lost the
   ss race is `D -> XID -> XRM -> XQMB -> XQM` (+ master-loop regen) racing
   the cut-off `CK -> XIC -> ckb-side`: exactly its stages are scaled — `XID`
   `inv_lv` -> `inv2x_lv`, `XRM`/`XQM` `nand2_lv` -> `nand2x_lv`, `XQMB`
   `nand3_lv` -> the new `nand3x_lv` (P 2 µm / N 3 µm, beside the issue #113
   2x family). The clock-facing gates (`XIC`, `XSM`'s ckb input) and the
   slave gates keep `dffr_lv`'s sizes, so hold stays structural (the ckb
   series devices cut `D` off; widening the D side cannot leak an opaque
   latch) and CLRB behaviour is unchanged.
2. **The slave is clocked through one `inv_lv` pair (`XD1`/`XD2` -> `ckd`).**
   The master's cut-off instant — `ckb` via `XIC`, which is what defines the
   sampled value — is untouched; the pair only delays when the slave copies
   the held master state, letting a race the master wins late resolve before
   `b_up` moves. Without it (measured, intermediate sizing): the scaled path
   settled capture-low at the 100 ps lead but `b_up` double-crossed — 0.92 V
   peak, propagating to `over` (0.62 V peak) and pulsing `set` every REF cycle
   at ss in the full supervisor (144 crossings; the reset latch did not flip,
   5 RST crossings). With the pair, `b_up` peaks at 8.7 mV, `over` stays at
   0.5 mV, and `set` crosses exactly once per stimulus event.

### Why the over-delay window (0005 part 3) is preserved

The window `OVER = b_up & a_up & ~a_dn` true for d in (1.5 T, 2 T) is defined
by the three sampling instants: `a_up`/`b_up` on the REF rise, `a_dn` on the
REF fall (`refb`). The remedy moves none of them. The master cut-off (what
freezes the sampled value) is `XIC`'s ckb edge on the shared REF net — `a_up`
and `b_up` see the same net, so no differential skew exists between them by
construction; `a_dn`'s `refb` path is untouched; the slave-clock pair changes
when the already-frozen sample appears at `b_up`, not what was sampled. The
1.8 T over-delay fault response is re-measured on the full supervisor at both
corners (evidence below). The cost is latency: `b_up`'s CK-to-Q grows by two
`inv_lv` delays and the master-loop resizing, shifting the tt over-delay
assert by +68 ps and its release by +34 ps against the #145 tt control — all
inside the committed smoke-gate windows, which pass unchanged.

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
   ss requirement by ≥ 20 ps at the sweep's 10 ps resolution instead of
   failing it by ≤ 10 ps. tt moves from (60, 80] to (40, 60] ps. At the
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

- Area/load: one `dffr_fast` (12 leaf instances against `dffr_lv`'s 10, wider
  D-path gates) for `XBUP` only. The TAPH pin load grows by the `XID` 2x +
  `nand3x_lv`-scaled input (~2.5 µm of gate width); the REF net inside
  `win_det` gains the two `inv_lv` clock-pair pins. In the smoke bench both
  are driven by ideal sources; the tap-buffer drive strength for the real
  line is re-graded with #41.
- **Not established**: mismatch spread (no Monte Carlo run — the bracket is a
  nominal-corner bracket); hold-time behaviour of `b_up` (TAPH rising through
  the REF edge — the direction the window needs at d near 2 T); the ff
  reduced-set corner and full PVT (#41); the closed loop (`sim/false-lock`
  bench); the (2 T, 3.5 T) coverage gap (unchanged by this record); that the
  a_up/a_dn samplers (unchanged cells) meet their own margins at ss.
- This record changes no `spec/` row and no gate limits; the smoke request
  `sim/supervisor-smoke/requests/sup.request.json` is untouched (its gates
  pass un-re-derived).
