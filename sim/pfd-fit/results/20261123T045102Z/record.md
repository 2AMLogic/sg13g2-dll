# diag_mos_tt — rest state of the run-2 `ctl_1g` control (issue #206)

One single-corner local diagnostic of decision 0011's run-2 `ctl_1g` control
deck (`srlatch_fast` latch, sibling reset polarity), run to settle the open
question issue #206 names: whether that control was "held in reset" at
tt, as [0011](../../../../spec/decisions/0011-pfd-reset-path-too-slow-at-1ghz.md)
states, or rested in the stuck-set state the current `srlatch_buf` control
shows at tt/ff (`../20261123T013250Z/`, `../20261123T012643Z/`). Not a gate
run; `grade.py` was not run on it. Results are **simulated, never measured**.

Method: the retained run-2 deck **byte-identical** — `decks/ctl_1g.spice` and
`decks/pfd.spice` are copies of `../20261115T001809Z/decks/` (sha256
`22b6165c…` / `1acbf19e…`, staged closure identical) — plus level cards on the
latch: `upb_n`/`dnb_n` (the `QB` port nodes of `srlatch_fast` inside `pfd_sib`)
min/max over 4..24 ns; `reset`, UP and DN over the rest window 4..4.9 ns;
`reset_raw` (the NAND output) and `reset_d1` at 4 ns; crossings of
`set_up`/`set_dn`/`reset`/`upb_n`/`dnb_n`/UP/DN. One corner, tt/1.200 V/27 C,
through `klt sim --backend local`, ngspice 47, klt
0.9.3.dev3714+g958c671967c4. Request, deck and envelope are beside this file.
ngspice recovered the DC operating point via dynamic gmin stepping
(`dc_homotopy_recovery`, info-level diagnostic in the envelope).

| quantity | tt/1.200V/27C |
|---|---|
| `reset` over the rest window | 8.3e-8 V |
| `reset` across 4..24 ns | −0.00022..0.00017 V |
| `reset_raw` (NAND output) at 4 ns | 1.98e-7 V |
| `reset_d1` at 4 ns | 1.200 V |
| `upb_n`, `dnb_n` across 4..24 ns | −0.0089..0.0081 V |
| UP, DN over the rest window | 1.200 V |
| UP, DN across 4..24 ns (max) | 1.243 V |
| crossings: `set_up`, `set_dn` | 38, 38 |
| crossings: `upb_n`, `dnb_n`, `reset`, UP, DN | 0 each |

**The run-2 control rests stuck set at tt, not held in reset.** Both latches
sit set (`QB` low, the lanes at VDD) with the reset chain consistent with it —
the NAND of the two high lane outputs (`XNR UP DN reset_raw`) is low, so after
its two inverters `reset` is a driven logic low,
deasserted — while the edge detectors fire on every input edge. A set pulse
cannot change a latch that is already set and nothing ever resets it, so no
lane pulse is released: UP and DN never cross VDD/2, the width-0 observation
of the committed run-2 `fit-gate.md`. This is the same dead rest state the
`srlatch_buf` control shows at tt and ff (`../20261123T012643Z/`); the
"hold the latch reset against the edgedet set pulse" mechanism 0011 names for
run 2 at tt is therefore refuted — the conclusion (C1 failure, no usable phase
response) is unchanged. Corrected by decision
[0016](../../../../spec/decisions/0016-ctl-1g-rest-states.md).

Not probed: run 2's control at ss and ff (the open question was tt only, the
corner 0011's claim names); a physical power-up state, mismatch, and any
non-reduced corner remain open as for every run of this bench.
