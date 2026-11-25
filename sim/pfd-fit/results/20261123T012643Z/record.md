# diag_mos_tt, diag_mos_ff — inside the stuck-set control (issue #201)

Two single-corner local diagnostics of the `ctl_1g` control deck
(`sim/pfd-fit/decks/ctl_1g.spice`, byte-identical to the copy in the gate run
`../20261123T013250Z/`), run after a first three-corner gate run read tt and ff
with both lanes high and `reset` low — not the "held in reset" the control was
assumed to show — to read the rest of the latch at those two corners. Not a gate
run; `grade.py` was not run on it. Results are **simulated, never measured**.

Method: the gate's `ctl_1g` request plus level cards on the latch — `up_qn`,
`dn_qn`, `up_qb`, `dn_qb` min/max over 4..24 ns; `reset`, UP and DN over the rest
window 4..4.9 ns; `reset_raw` (the NAND output) and `reset_d1` at 4 ns — one
corner per unit through `klt sim --backend local`, ngspice 47, klt
0.9.3.dev3510+gfd0e55db542e. Requests, decks and envelopes are beside this
file.

| quantity | tt/1.200V/27C | ff/1.320V/−40C |
|---|---|---|
| `reset` over the rest window | 1.07e-7 V | 1.63e-7 V |
| `reset` across 4..24 ns | −0.0002..0.0002 V | −0.0003..0.0003 V |
| `reset_raw` (NAND output) at 4 ns | 1.98e-7 V | 3.04e-7 V |
| `reset_d1` at 4 ns | 1.200 V | 1.320 V |
| `up_qn`, `dn_qn` across 4..24 ns | 1.155..1.243 V | 1.270..1.368 V |
| `up_qb`, `dn_qb` across 4..24 ns | −0.007..0.007 V | −0.010..0.009 V |
| UP, DN over the rest window | 1.200 V | 1.320 V |
| UP, DN across 4..24 ns (max) | 1.201 V | 1.321 V |
| crossings: `set_up`, `set_dn` | 38, 38 | 38, 38 |
| crossings: `up_qn`, `dn_qn`, `reset`, UP, DN | 0 each | 0 each |

Both corners sit in the same state: both latches set (`QN` high, `QB` low, the
lane at VDD) with the reset chain consistent with it — the NAND of two high
storage nodes is low, so `reset` is deasserted and nothing ever resets the
latches — while the edge detectors fire on every input edge. This is the `stuck
set` state `grade.py` names for these corners in `../20261123T013250Z/`. The
gate's own probes identify it from `reset` at rest, the storage-node minima and
the lanes, and do not read `QB`, `reset_raw` or `reset_d1`.
