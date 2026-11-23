# 0016 — The sibling-polarity `ctl_1g` control has two dead rest states; 0008/0011 named one

- **Status**: proposed. **This is an evidence record: it relaxes no `spec/` row, changes no
  criterion in `sim/pfd-fit/grade.py`, touches no schematic or netlist, and its merge ratifies
  nothing.** It corrects the *mechanism* prose of two earlier records; their conclusion stands.
- **Date**: 2026-11-23
- **Decided by**: Builder agent, issue #206
- **Consumes**: [0008](0008-false-lock-argument.md) (the reset-polarity netlist reading); [0011](0011-pfd-reset-path-too-slow-at-1ghz.md) (run 2's control); [0015](0015-pfd-buffered-lane-output.md) (the committed `srlatch_buf` latch the control now runs on)
- **Related**: #201 (the instrumented control run this evidence comes from)

## What the earlier records said

Two earlier records name a single dead rest state for the sibling reset polarity. In the
unbuffered topology they describe, the reset NAND senses the UP and DN lanes directly.
The two following inverters preserve its polarity, giving `reset = NAND(UP, DN)`.

- 0008 "PFD redraw" reads the sibling netlist and predicts "the latches are held in reset and
  UP/DN would follow the edge-detector pulses" — explicitly a reading, not a simulation.
- 0011's 2026-11-15 update describes run 2's `ctl_1g` control at tt: "The widened `srlatch_fast`
  NANDs hold the latch reset against the edgedet set pulse under the sibling's active-low
  polarity … a stuck-reset corner."

The instrumented control run of issue #201 shows the polarity fails from **two** stable rest
states, one per corner, and the run-2 sentence above is now probed and refuted as mechanism
(this record, evidence section 2). The conclusion both records draw — the sibling polarity gives
no usable phase response on these cells (C1 fails), so the redraw's NAND + odd-inverter polarity
stands — is **unchanged**; both rest states fail it.

## Evidence 1: the committed-latch control, all three corners (simulated, never measured)

`sim/pfd-fit/results/20261123T013250Z/record.md` — the full 0006 gate run with the `ctl_1g`
control instrumented (batch fleet, `ctl_1g` job `klt-sim-603ea5992192`, ngspice 47, the three
`reduced_set` corners; DUT-internal probes added by #201; decks and `pfd_*` requests
byte-identical to `../20261123T001411Z/`). Method: `sim/pfd-fit/run.sh` bench — 100 ps edges,
FB-minus-REF offsets −160..+160 ps, 4 fF lane loads, `tran 5p 25n` — graded by
`sim/pfd-fit/grade.py` (exit 0; it names the state per corner from the probes). Re-derived from
the committed envelope:

| corner | `v_reset_rest` | `v_up_qn_min` | `v_up_max` | `t_up_qn` crossings | dead rest state |
|---|---|---|---|---|---|
| mos_tt/1.200V/27C | 0.000 V (1.1e-7) | 1.155 V | 1.201 V | 0 | **stuck set** |
| mos_ss/1.080V/125C | 1.080 V | −0.049 V | 0.003 V | 38 | **held in reset** |
| mos_ff/1.320V/−40C | 0.000 V (1.6e-7) | 1.270 V | 1.321 V | 0 | **stuck set** |

- **ss rests held in reset** — `reset` is asserted at rest. During the sweep, each storage
  node crosses VDD/2 38 times and `reset` crosses 26 times. UP and DN stay below 3 mV.
- **tt and ff rest stuck set** — both latches set, `reset` a driven logic low (deasserted), the
  lanes at VDD before the first REF edge; a set pulse cannot change an already-set latch and
  nothing ever resets it. `sim/pfd-fit/results/20261123T012643Z/record.md` (single-corner local
  diagnostics, tt and ff) reads the rest of the latch consistently: `up_qb`/`dn_qb` low,
  `reset_raw` (the NAND output) ~0 V, `reset_d1` at VDD.
- In **both** states the edge detectors fire on every input edge and no lane pulse is released
  at any offset: `wUP = wDN = 0` ps, C1 ratio 0.00, at all three corners.

Each simulated corner starts from its DC operating point. Physical power-up remains untested.
In the committed `srlatch_buf` design, the reset NAND senses the latch storage nodes
`up_qn` and `dn_qn`. One inverter gives `reset = AND(up_qn, dn_qn)`. With both nodes low,
reset is deasserted so an input edge can set its latch. When both nodes go high, reset
asserts and clears the latches. The buffered sibling control senses the same nodes through
a NAND and two inverters, giving `reset = NAND(up_qn, dn_qn)`. For each zero-offset cycle,
`sim/pfd-fit/grade.py` checks C2 using the smaller of the UP and DN pulse widths at the
buffered outputs.

## Evidence 2: run 2's control at tt — stuck set, not held in reset (simulated, never measured)

The open question #206 names — 0011's run-2 claim was never probed — is now settled by
`sim/pfd-fit/results/20261123T045102Z/record.md`: one single-corner local diagnostic
(`klt sim --backend local`, ngspice 47, tt/1.200V/27 C) of the **retained run-2 deck
byte-identical** (`../20261115T001809Z/decks/ctl_1g.spice` + `pfd.spice`, sha256 `22b6165c…` /
`1acbf19e…`), reading the `srlatch_fast` `QB` nodes (`upb_n`/`dnb_n`), `reset`, `reset_raw`,
`reset_d1` and the lanes: `reset` 8.3e-8 V at rest, `upb_n`/`dnb_n` −0.009..0.008 V, UP/DN at
1.200 V, zero crossings on `reset`/`upb_n`/`dnb_n`/UP/DN, edge detectors firing 38 + 38. **Run
2's control rested stuck set at tt**, the same state as the committed latch at tt/ff; the
"hold the latch reset" mechanism sentence in 0011 is refuted, while its observation (zero-width
pulses) and conclusion (C1 failure, not a broken deck) stand. Run 2 at ss and ff remains
unprobed (tt is the corner 0011's sentence names); no claim here rests on them.

## Corrections made by this record's PR (append-only; no earlier text rewritten)

- **0008** gains a dated pointer at the "PFD redraw" passage: the one-state prediction names
  one of two dead rest states; see this record.
- **0011** gains a dated pointer at the run-2 paragraph: its mechanism sentence is refuted by
  Evidence 2; the conclusion is unchanged.
- **`design/NOTES.md`** "still fails (dead zone)" is reworded to name the two rest states
  ("resting stuck set at tt/ff and held in reset at ss, no lane pulse at any offset").
- **Nothing else moves.** No `spec/` row is relaxed, no `sim/` result is edited (the new
  diagnostic is a new, append-only results directory), and the committed PFD, latch, and reset
  path are untouched.
