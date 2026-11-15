# lock-detector-smoke record

Run conditions, as the envelope recorded them: corner tt, Vdd 1.2 V, 27 C; engine ngspice 47; backend local.
Simulated, never measured. Limits are smoke gates, not spec numbers.

| measurement | value | unit | status |
|---|---|---|---|
| lock_max_before_220n | 4.126e-05 | V | pass |
| t_rise1 | 3.511e-07 | s | pass |
| t_fall1 | 5.211e-07 | s | pass |
| t_rise2 | 7.101e-07 | s | pass |
| t_edge_lock | 8.594e-11 | s | pass |

RESULT: PASS

## Provenance (issue #145)

Run against repo commit `facba8b` (origin/main at the #141 merge; branch
`feature/issue-145`, content-identical for all design inputs). The netlisted
`lock_detector.spice` carries the **three-stage device-level `edgedet`**
(`XMPD1..XMND3`, `sg13_lv_pmos w=1u l=0.16u` / `sg13_lv_nmos w=0.5u l=0.16u`,
`design/netlist/lock_detector.spice:135-140`), not the five-inverter chain
(`XD1..XD5 inv_lv`) the predecessor records `20261105T091102Z` and
`20261114T091558Z` were produced with. Envelope `netlist_identity`
`sha256:620133be...`; `design/netlist.sh --check` passed immediately before the
run. This record replaces the stale evidence issue #145 was filed about; the ss
corner is covered separately by the probe in `../20261115T185846Z-probe/`.
