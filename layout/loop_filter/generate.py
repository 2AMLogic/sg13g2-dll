#!/usr/bin/env python3
"""Generate loop_filter.gds -- layout of design/loop_filter.sch (issue #190).

One cap_cmim (w=26u l=26u m=1, decision 0006's first-order DLL loop filter)
drawn by `klt gen cap_array` as a single MiM unit, with the two plates
labeled as the cell's pins:

- VCTRL on the top plate (C0_TOP, TopMetal1),
- VSS on the bottom plate (C0_BOT, Metal5),

the terminal order of `XC1 VCTRL VSS cap_cmim` in
design/netlist/loop_filter.spice. No routing or body tie: a two-terminal
MIM capacitor has no body, and both pins land on the plates' own pads.

Run from the repo root:

    uv run --with klayout==0.30.13 python3 layout/loop_filter/generate.py
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from common import M5_TEXT, Part, TM1_TEXT, U, kdb  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "loop_filter.gds")

cap = Part("lf_cap", "cap_array",
           {"num": 1, "plate_w_um": 26.0, "plate_h_um": 26.0}, HERE)
ports = {p["name"]: p for p in cap.report["ports"]}

ly = kdb.Layout()
ly.dbu = 0.001
top = ly.create_cell("loop_filter")

src = kdb.Layout()
src.read(cap.gds)
src.dbu = 0.001
stop = src.top_cell()
stop.flatten(-1, True)
cell = ly.create_cell("lf_cap")
for li in src.layer_indexes():
    info = src.get_info(li)
    tli = ly.layer(info)
    for s in stop.shapes(li).each():
        cell.shapes(tli).insert(s)
top.insert(kdb.CellInstArray(cell.cell_index(),
                             kdb.Trans(kdb.Trans.R0, 0, 0)))

# Pin labels on the plates' own pads, at the generator-reported port
# positions (the same coordinates klt gen-compose pins[] labels).
top.shapes(ly.layer(*TM1_TEXT)).insert(kdb.Text(
    "VCTRL", kdb.Trans(kdb.Trans.R0,
                       U(ports["C0_TOP"]["x_um"]), U(ports["C0_TOP"]["y_um"]))))
top.shapes(ly.layer(*M5_TEXT)).insert(kdb.Text(
    "VSS", kdb.Trans(kdb.Trans.R0,
                     U(ports["C0_BOT"]["x_um"]), U(ports["C0_BOT"]["y_um"]))))

opts = kdb.SaveLayoutOptions()
opts.gds2_write_timestamps = False  # byte-reproducible rebuilds
ly.write(OUT, opts)
print("wrote", OUT)
