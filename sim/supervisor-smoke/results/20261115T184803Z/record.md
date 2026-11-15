# supervisor-smoke record

Run conditions, as the envelope recorded them: corner tt, Vdd 1.2 V, 27 C; engine ngspice 47; backend local.
Simulated, never measured. Limits are smoke gates, not spec numbers.

| measurement | value | unit | status |
|---|---|---|---|
| t_release0 | 3.549e-09 | s | pass |
| t_over | 2.586e-08 | s | pass |
| t_release_over | 5.129e-08 | s | pass |
| t_timeout | 7.855e-08 | s | pass |
| d_mask0 | 1.026e-09 | s | pass |
| d_mask_timeout | 9.508e-10 | s | pass |

RESULT: PASS

## Provenance (issue #145)

Run against repo commit `facba8b` (origin/main at the #141 merge; branch
`feature/issue-145`, content-identical for all design inputs). The netlisted
`supervisor.spice` carries the **three-stage device-level `edgedet`**
(`XMPD1..XMND3`, `sg13_lv_pmos w=1u l=0.16u` / `sg13_lv_nmos w=0.5u l=0.16u`,
`design/netlist/supervisor.spice:166-171`), not the five-inverter chain
(`XD1..XD5 inv_lv`) the predecessor records `20261105T052155Z` and
`20261114T092421Z` were produced with. Envelope `netlist_identity`
`sha256:32c5dae5...`; `design/netlist.sh --check` passed immediately before the
run. This record replaces the stale evidence issue #145 was filed about; the ss
corner is covered separately by the probe in `../20261115T185844Z-probe/`.
