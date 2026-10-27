"""Cell definitions for design/ (PFD, charge pump, bias, loop filter).

Every device is `sg13_lv_*` (1.2 V thin oxide, spec/decisions/0007). Topology of
the PFD and charge pump is the one adopted from `2AMLogic/sg13g2-pll` @
83e59fe81db0b09dbefcff35a55965bea0c2a76f (spec/decisions/0006); the cells are
redrawn, not copied, and the PFD reset polarity differs (see
spec/decisions/0008-false-lock-argument.md, "PFD redraw").

Sizes are first-pass. Rendering: design/tools/mksch.py.
"""

from mksch import Cell

L = "0.13u"  # minimum lv channel length (model valid L >= 0.13 um, W >= 0.15 um)

CELLS = []


def add(cell):
    CELLS.append(cell)
    return cell


def logic_ports(ins, outs):
    p = " ".join(f"{n}:i:l" for n in ins) + " " + " ".join(f"{n}:o:r" for n in outs)
    return p + " VDD:io:t VSS:io:b"


# ---------------------------------------------------------------- leaf logic --
c = add(Cell("inv_lv", logic_ports(["A"], ["Y"]), "unit static CMOS inverter, sg13_lv"))
c.mos("MP", "p", "1u", L, D="Y", G="A", S="VDD", B="VDD")
c.mos("MN", "n", "0.5u", L, D="Y", G="A", S="VSS", B="VSS")

c = add(Cell("inv2x_lv", logic_ports(["A"], ["Y"]), "2x inverter, sg13_lv"))
c.mos("MP", "p", "2u", L, D="Y", G="A", S="VDD", B="VDD")
c.mos("MN", "n", "1u", L, D="Y", G="A", S="VSS", B="VSS")

c = add(Cell("nand2_lv", logic_ports(["A1", "A2"], ["Y"]), "2-input NAND, sg13_lv"))
c.mos("MP1", "p", "1u", L, D="Y", G="A1", S="VDD", B="VDD")
c.mos("MP2", "p", "1u", L, D="Y", G="A2", S="VDD", B="VDD")
c.mos("MN1", "n", "1u", L, D="Y", G="A1", S="mid", B="VSS")
c.mos("MN2", "n", "1u", L, D="mid", G="A2", S="VSS", B="VSS")

# ------------------------------------------------------------------------ PFD --
c = add(Cell("edgedet", logic_ports(["X"], ["OUT"]),
             "rising-edge pulse generator: X AND NOT(X delayed by 5 inverters)"))
c.sub("XD1", "inv_lv", A="X", Y="d1", VDD="VDD", VSS="VSS")
c.sub("XD2", "inv_lv", A="d1", Y="d2", VDD="VDD", VSS="VSS")
c.sub("XD3", "inv_lv", A="d2", Y="d3", VDD="VDD", VSS="VSS")
c.sub("XD4", "inv_lv", A="d3", Y="d4", VDD="VDD", VSS="VSS")
c.sub("XD5", "inv_lv", A="d4", Y="d5", VDD="VDD", VSS="VSS")
c.sub("XN1", "nand2_lv", A1="X", A2="d5", Y="ntmp", VDD="VDD", VSS="VSS")
c.sub("XOUT", "inv_lv", A="ntmp", Y="OUT", VDD="VDD", VSS="VSS")

c = add(Cell("srlatch", logic_ports(["S", "R"], ["Q", "QB"]),
             "set/reset latch from two NAND2 with inverted inputs (S, R active high)"))
c.sub("XIS", "inv_lv", A="S", Y="SB", VDD="VDD", VSS="VSS")
c.sub("XIR", "inv_lv", A="R", Y="RB", VDD="VDD", VSS="VSS")
c.sub("XNQ", "nand2_lv", A1="SB", A2="QB", Y="Q", VDD="VDD", VSS="VSS")
c.sub("XNQB", "nand2_lv", A1="RB", A2="Q", Y="QB", VDD="VDD", VSS="VSS")

c = add(Cell("pfd", "REF:i:l FB:i:l UP:o:r DN:o:r VDD:io:t VSS:io:b",
             "tri-state PFD: 2x edgedet + 2x srlatch, reset = AND(UP,DN) delayed by NAND + 3 inverters"))
c.sub("XED_UP", "edgedet", X="REF", OUT="set_up", VDD="VDD", VSS="VSS")
c.sub("XED_DN", "edgedet", X="FB", OUT="set_dn", VDD="VDD", VSS="VSS")
c.sub("XLU", "srlatch", S="set_up", R="reset", Q="UP", QB="upb_n", VDD="VDD", VSS="VSS")
c.sub("XLD", "srlatch", S="set_dn", R="reset", Q="DN", QB="dnb_n", VDD="VDD", VSS="VSS")
c.sub("XNR", "nand2_lv", A1="UP", A2="DN", Y="reset_n0", VDD="VDD", VSS="VSS")
c.sub("XR1", "inv_lv", A="reset_n0", Y="reset_p1", VDD="VDD", VSS="VSS")
c.sub("XR2", "inv_lv", A="reset_p1", Y="reset_n2", VDD="VDD", VSS="VSS")
c.sub("XR3", "inv2x_lv", A="reset_n2", Y="reset", VDD="VDD", VSS="VSS")

# ------------------------------------------------------------- charge pump --
c = add(Cell("cp_leg_p", "IBP:i:l ICP:i:l UP:i:l UPB:i:l VOUT:o:r VDUMP:o:r VDD:io:t",
             "PMOS current-steering leg: mirror + cascode, switch to VOUT (UPB low) or VDUMP"))
c.mos("M1", "p", "6u", "0.5u", D="tail", G="IBP", S="VDD", B="VDD")
c.mos("M2", "p", "6u", "0.5u", D="sw", G="ICP", S="tail", B="VDD")
c.mos("XSWO", "p", "3u", L, D="VOUT", G="UPB", S="sw", B="VDD")
c.mos("XSWD", "p", "3u", L, D="VDUMP", G="UP", S="sw", B="VDD")

c = add(Cell("cp_leg_n", "IBN:i:l ICN:i:l DN:i:l DNB:i:l VOUT:o:r VDUMP:o:r VSS:io:b",
             "NMOS current-steering leg: mirror + cascode, switch to VOUT (DN high) or VDUMP"))
c.mos("M1", "n", "2u", "0.5u", D="tail", G="IBN", S="VSS", B="VSS")
c.mos("M2", "n", "2u", "0.5u", D="sw", G="ICN", S="tail", B="VSS")
c.mos("XSWO", "n", "1u", L, D="VOUT", G="DN", S="sw", B="VSS")
c.mos("XSWD", "n", "1u", L, D="VDUMP", G="DNB", S="sw", B="VSS")

c = add(Cell("cp_dumpbuf", "VOUT:i:l IBIAS:i:l VDUMP:o:r VDD:io:t VSS:io:b",
             "source-follower dump buffer: VDUMP tracks VOUT one Vgs below"))
c.mos("M1", "n", "2u", "0.25u", D="VDD", G="VOUT", S="VDUMP", B="VSS")
c.mos("M2", "n", "1u", "0.5u", D="VDUMP", G="IBIAS", S="VSS", B="VSS")

c = add(Cell("cp", "UP:i:l DN:i:l IBP:i:l ICP:i:l IBN:i:l ICN:i:l VOUT:o:r VDD:io:t VSS:io:b",
             "cascoded current-steering charge pump (bias pins external, see cp_bias)"))
c.sub("XIUP", "inv_lv", A="UP", Y="UPB", VDD="VDD", VSS="VSS")
c.sub("XIDN", "inv_lv", A="DN", Y="DNB", VDD="VDD", VSS="VSS")
c.sub("XLEGP", "cp_leg_p", IBP="IBP", ICP="ICP", UP="UP", UPB="UPB", VOUT="VOUT", VDUMP="VDUMP", VDD="VDD")
c.sub("XLEGN", "cp_leg_n", IBN="IBN", ICN="ICN", DN="DN", DNB="DNB", VOUT="VOUT", VDUMP="VDUMP", VSS="VSS")
c.sub("XBUF", "cp_dumpbuf", VOUT="VOUT", IBIAS="IBN", VDUMP="VDUMP", VDD="VDD", VSS="VSS")

c = add(Cell("cp_bias", "IBP:o:r ICP:o:r IBN:o:r ICN:o:r VDD:io:t VSS:io:b",
             "charge-pump bias: one long-channel PMOS sets Iref, diode stacks give mirror and cascode gates"))
c.mos("MR", "p", "0.5u", "4u", D="ICN", G="VSS", S="VDD", B="VDD")
c.mos("MN3", "n", "2u", "0.5u", D="ICN", G="ICN", S="IBN", B="VSS")
c.mos("MN0", "n", "2u", "0.5u", D="IBN", G="IBN", S="VSS", B="VSS")
c.mos("MP0", "p", "6u", "0.5u", D="IBP", G="IBP", S="VDD", B="VDD")
c.mos("MP3", "p", "6u", "0.5u", D="ICP", G="ICP", S="IBP", B="VDD")
c.mos("MN4", "n", "2u", "0.5u", D="ICP", G="IBN", S="VSS", B="VSS")

# -------------------------------------------------------------- loop filter --
c = add(Cell("loop_filter", "VCTRL:io:t VSS:io:b",
             "first-order loop filter: one MIM capacitor from VCTRL to VSS (decision 0006)"))
c.cap("C1", "26u", "26u", "VCTRL", "VSS")
