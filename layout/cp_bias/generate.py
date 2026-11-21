#!/usr/bin/env python3
"""Generate cp_bias.gds -- layout of design/cp_bias.sch (issue #190).

Charge-pump bias: one long-channel PMOS sets Iref, diode stacks give the
mirror and cascode gates. Six devices in three matched mos_array blocks:

    N  nfet w=2u   l=0.5u x3 (MN0, MN3, MN4)   dummies both ends
    P  pfet w=6u   l=0.5u x2 (MP0, MP3)        dummies both ends
    R  pfet w=2.2u l=4u   x1 (MR)              no dummies (no in-cell match)

Net-by-net wiring read from design/netlist/cp_bias.spice:

    XMN0  D=IBN G=IBN S=VSS     (diode)
    XMN3  D=ICN G=ICN S=IBN     (diode)
    XMN4  D=ICP G=IBN S=VSS
    XMP0  D=IBP G=IBP S=VDD     (diode)
    XMP3  D=ICP G=ICP S=IBP     (diode)
    XMR   D=ICN G=VSS  S=VDD    (Iref, l=4u)

Routing model (see layout/common.py): every horizontal run is a Metal2
track at a unique y; every vertical connection is a Metal1 stub at a pad
column or a Metal1 channel run; the two layers cross freely, joined only
by drawn Via1s. Body ties: one p+ substrate island ties all nfet bodies to
VSS; each pfet block's well gets an n+ island tied to VDD.

Run from the repo root:

    uv run --with klayout==0.30.13 python3 layout/cp_bias/generate.py
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from common import Cell, Part  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cp_bias.gds")

# --- Metal2 track y assignments (unique per net segment) --------------------
Y_VSS = -1.2    # bottom rail trunk
Y_IBN = 3.4     # above the nfet row
Y_ICN = 4.1
Y_ICP_MID = 4.8
Y_VDD = 6.6     # under the pfet row
Y_VSS_RET = 12.6   # MR gate return, above the R block
Y_IBP = 16.6    # above the P block
Y_ICP_TOP = 17.4

# vertical channel x positions (clear columns between blocks)
X_ICP_VERT = 7.2    # carries ICP between its mid and top segments
X_VSS_VERT = 19.6   # carries MR's gate down to the VSS trunk

N = Part("cpb_n", "mos_array",
         {"rows": 1, "cols": 3, "dummy": 1, "flavor": "nfet",
          "w_um": 2.0, "l_um": 0.5, "topology": "array", "gate_contact": True},
         HERE)
P = Part("cpb_p", "mos_array",
         {"rows": 1, "cols": 2, "dummy": 1, "flavor": "pfet",
          "w_um": 6.0, "l_um": 0.5, "topology": "array", "gate_contact": True},
         HERE)
R = Part("cpb_r", "mos_array",
         {"rows": 1, "cols": 1, "dummy": 0, "flavor": "pfet",
          "w_um": 2.2, "l_um": 4.0, "topology": "array", "gate_contact": True},
         HERE)

c = Cell("cp_bias")
n = c.place(N, 0.0, 0.0)     # units: 0=MN0, 1=MN3, 2=MN4
p = c.place(P, 0.0, 8.0)     # units: 0=MP0, 1=MP3
r = c.place(R, 12.0, 8.0)    # unit 0=MR

# --- VSS: nfet sources, MR gate, substrate tie ------------------------------
c.m2("VSS", Y_VSS, 0.0, X_VSS_VERT + 0.5)
c.stub_sd_dn("VSS", n, 0, "s", Y_VSS)
c.stub_sd_dn("VSS", n, 2, "s", Y_VSS)
c.stub_g_up("VSS", r, 0, Y_VSS_RET)
c.m2("VSS", Y_VSS_RET, r.pad(0, "g")[0], X_VSS_VERT)
c.vrun("VSS", X_VSS_VERT, Y_VSS, Y_VSS_RET)
c.via("VSS", X_VSS_VERT, Y_VSS)
c.via("VSS", X_VSS_VERT, Y_VSS_RET)
c.psub_tap(8.0, -1.0, "VSS", Y_VSS)
c.label("VSS", 9.8, Y_VSS)

# --- VDD: pfet sources (MP0, MR), well ties ---------------------------------
c.m2("VDD", Y_VDD, 0.0, r.bbox()[2] + 1.55)
c.stub_sd_dn("VDD", p, 0, "s", Y_VDD)
c.stub_sd_dn("VDD", r, 0, "s", Y_VDD)
c.well_tie(p, "VDD", Y_VDD)
c.well_tie(r, "VDD", Y_VDD)
c.label("VDD", 6.5, Y_VDD)

# --- IBN: MN0 diode (D+G), MN3 source, MN4 gate ------------------------------
c.m2("IBN", Y_IBN, n.pad(0, "g")[0] - 0.3, n.pad(2, "g")[1] + 0.3)
c.stub_d_up("IBN", n, 0, Y_IBN)
c.stub_g_up("IBN", n, 0, Y_IBN)
c.stub_s_up("IBN", n, 1, Y_IBN)
c.stub_g_up("IBN", n, 2, Y_IBN)
c.label("IBN", 2.4, Y_IBN)

# --- ICN: MN3 diode (D+G), MR drain ------------------------------------------
c.m2("ICN", Y_ICN, n.pad(1, "g")[0] - 0.3, r.pad(0, "d")[0] + 0.3)
c.stub_d_up("ICN", n, 1, Y_ICN)
c.stub_g_up("ICN", n, 1, Y_ICN)
c.stub_sd_dn("ICN", r, 0, "d", Y_ICN)
c.label("ICN", 9.0, Y_ICN)

# --- ICP: MN4 drain (below N), MP3 diode (D mid, G top) ----------------------
c.m2("ICP", Y_ICP_MID, p.pad(1, "d")[0] - 0.3, X_ICP_VERT)
c.stub_sd_dn("ICP", n, 2, "d", -0.4)
c.m2("ICP", -0.4, n.pad(2, "d")[0] - 0.3, X_ICP_VERT)
c.vrun("ICP", X_ICP_VERT, -0.4, Y_ICP_TOP)
c.via("ICP", X_ICP_VERT, -0.4)
c.via("ICP", X_ICP_VERT, Y_ICP_MID)
c.stub_sd_dn("ICP", p, 1, "d", Y_ICP_MID)
c.m2("ICP", Y_ICP_TOP, p.pad(1, "g")[0] - 0.3, X_ICP_VERT)
c.via("ICP", X_ICP_VERT, Y_ICP_TOP)
c.stub_g_up("ICP", p, 1, Y_ICP_TOP)
c.label("ICP", 5.6, Y_ICP_MID)

# --- IBP: MP0 diode (D+G), MP3 source ----------------------------------------
c.m2("IBP", Y_IBP, p.pad(0, "g")[0] - 0.3, p.pad(1, "s")[1] + 0.3)
c.stub_d_up("IBP", p, 0, Y_IBP)
c.stub_g_up("IBP", p, 0, Y_IBP)
c.stub_s_up("IBP", p, 1, Y_IBP)
c.label("IBP", 1.3, Y_IBP)

c.write(OUT)
print("wrote", OUT)
