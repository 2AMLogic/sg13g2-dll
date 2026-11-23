# supervisor-smoke record

Run conditions, as the envelope recorded them: corner tt, Vdd 1.2 V, 27 C; engine ngspice 47; backend local.
Simulated, never measured. Limits are smoke gates, not spec numbers.

| measurement | value | unit | status |
|---|---|---|---|
| t_release0 | 3.549e-09 | s | pass |
| t_over | 2.593e-08 | s | pass |
| t_release_over | 5.133e-08 | s | pass |
| t_timeout | 7.855e-08 | s | pass |
| d_mask0 | 1.026e-09 | s | pass |
| d_mask_timeout | 9.508e-10 | s | pass |

RESULT: PASS

## Provenance (issue #195)

Run on branch `feature/issue-195` (this PR): `win_det.XBUP` is the new
`dffr_fast` (spec/decisions/0017 — D-path and master-loop gates scaled 2x,
slave clocked through an `inv_lv` pair), everything else in the netlist
unchanged from the `20261115T184803Z` baseline. Envelope `netlist_identity`
`sha256:5789b6699877ab8a7258142e3676d357ea05bc9792290a87ee4a08fc05cc476b`
(the staged deck = revised `design/netlist/supervisor.spice` + the unchanged
`decks/sup_body.spice`); `design/netlist.sh --check` and
`design/tools/mksch.py --check` passed immediately before the run (run.sh runs
the check itself). All six gates pass on the revised netlist with the
committed, un-re-derived limits — the two first-edge-mask gates included
(`d_mask0` 1.026 ns, `d_mask_timeout` 0.951 ns, both unchanged from the
baseline). The ss corner is covered by the probe replay in
`../20261123T101910Z-probe/` and the setup bracket in
`../20261123T101910Z-setup/`.
