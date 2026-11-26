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

from common import Cell, M5_TEXT, Part, TM1_TEXT  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "loop_filter.gds")

cap = Part("lf_cap", "cap_array",
           {"num": 1, "plate_w_um": 26.0, "plate_h_um": 26.0}, HERE)
ports = {p["name"]: p for p in cap.report["ports"]}

c = Cell("loop_filter")
c.place(cap, 0.0, 0.0)
# Pin labels on the plates' own pads, at the generator-reported port
# positions (the same coordinates klt gen-compose pins[] labels).
c.text(TM1_TEXT, "VCTRL", ports["C0_TOP"]["x_um"], ports["C0_TOP"]["y_um"])
c.text(M5_TEXT, "VSS", ports["C0_BOT"]["x_um"], ports["C0_BOT"]["y_um"])
c.write(OUT)
print("wrote", OUT)
