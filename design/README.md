# design

Schematic sources (xschem) and the SPICE netlists derived from them. All
devices are `sg13_lv_*` (1.2 V thin oxide, `spec/decisions/0007`). What has been
simulated for each block, and what the run showed, is recorded once: in
[`NOTES.md`](NOTES.md) (each block's "Evidence status") and in the append-only
`sim/<bench>/results/`; the adoption state of the PFD and charge pump is in
`reuse.lock.json`. This file keeps no second copy of it.

| Block | Schematic | Netlist | Notes |
|---|---|---|---|
| PFD | `pfd.sch` (+ `edgedet`, `srlatch`, `nand2_lv`, `inv_lv`, `inv2x_lv`) | `netlist/pfd.spice` | topology of `sg13g2-pll@83e59fe`, redrawn; reset path differs (`spec/decisions/0008`) |
| Charge pump | `cp.sch` (+ `cp_leg_p`, `cp_leg_n`, `cp_dumpbuf`) | `netlist/cp.spice` | cascoded current-steering; bias pins `IBP ICP IBN ICN` are external |
| CP bias | `cp_bias.sch` | `netlist/cp_bias.spice` | one long-channel PMOS sets Iref; diode stacks give mirror and cascode gates |
| Loop filter | `loop_filter.sch` | `netlist/loop_filter.spice` | first-order: one MIM capacitor, `VCTRL` to `VSS` |
| Delay cell | `delay_cell.sch` | `netlist/delay_cell.spice` | two current-starved inverters, non-inverting (issue #23) |
| Tap buffer | `tap_buffer.sch` | `netlist/tap_buffer.spice` | two-inverter buffer isolating each tap |
| Delay line | `delay_line.sch` | `netlist/delay_line.spice` | 8 delay cells, `T0..T8` tap buffers, dummy last-tap load |
| False-lock supervisor | `supervisor.sch` (+ `win_det`, `rail_cmp`, `timeout_cnt`, `refmask`, `dffr_lv`, `nand3_lv`) | `netlist/supervisor.spice` | `0005` parts 1 and 3, `0008` start-up mask (issue #53); sizing and design choices in [`NOTES.md`](NOTES.md) |
| Lock detector | `lock_detector.sch` (+ `vmov_cmp`, `dffr_lv`, `edgedet`, `srlatch`, `nand3_lv`) | `netlist/lock_detector.spice` | spec row 12 (issue #54); window sampling, VCTRL-movement sensor and 128-cycle filter; built against the draft spec; sizing and design choices in [`NOTES.md`](NOTES.md) |

Sizing rationale and evidence status for the delay line: [`NOTES.md`](NOTES.md).

Not yet drawn (follow-up issue of #24): `dll_top.sch`, which now has its delay line
(#23), the supervisor (#53) and the lock detector (#54).

## Regenerate and check

```
export PDK_ROOT=...                # sim/harness/env.sh finds it
design/netlist.sh                  # re-export design/netlist/*.spice (via `klt netlist`)
design/netlist.sh --check          # exit 3 if a schematic or netlist is stale
python3 -I design/tools/mksch.py   # redraw .sch/.sym from design/tools/cells.py
python3 -I design/tools/mksch.py --check
```

`design/tools/cells.py` + `mksch.py` are the drawing aid that wrote the `.sch`
and `.sym` files (label-driven connectivity, as in the sibling); edit either the
cell definition and redraw, or the `.sch` in xschem and then update the
definition, and re-export. `netlist.sh` is the one exporter for the design:
issue #23's tops are in its `BLOCKS` list.
xschem is only run through `klt netlist`.

## Interface assumptions the delay line must meet or change

- VCTRL high = **shorter** delay (NMOS-starved tail). Minimum-delay start is
  VCTRL at the high rail. See `spec/decisions/0008`.
- PFD inputs: `REF` = input clock, `FB` = tap N. DN raises delay, UP lowers it.

## Sizing

Logic: `inv_lv` P 1 µm / N 0.5 µm, L 0.13 µm (minimum); `nand2_lv` 1 µm all
devices. Edge detector: 5 inverters. Reset: NAND + 3 inverters. Charge-pump legs
L 0.5 µm; loop capacitor 26 µm × 26 µm MIM. These are the values in
`design/tools/cells.py` that `mksch.py` draws the schematics from; what each has
been graded against is in [`NOTES.md`](NOTES.md) and `sim/<bench>/results/`.
