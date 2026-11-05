"""Cell definitions for design/ (PFD, charge pump, bias, loop filter, false-lock supervisor).

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

# ----------------------------------------------------- false-lock supervisor --
# Requirements: spec/decisions/0005 parts 1 and 3, 0008 "Start-up requirement".
# Design choices (time-out, thresholds, sizes) are in design/NOTES.md; none is a
# spec row.
c = add(Cell("nand3_lv", logic_ports(["A1", "A2", "A3"], ["Y"]), "3-input NAND, sg13_lv"))
c.mos("MP1", "p", "1u", L, D="Y", G="A1", S="VDD", B="VDD")
c.mos("MP2", "p", "1u", L, D="Y", G="A2", S="VDD", B="VDD")
c.mos("MP3", "p", "1u", L, D="Y", G="A3", S="VDD", B="VDD")
c.mos("MN1", "n", "1.5u", L, D="Y", G="A1", S="m1", B="VSS")
c.mos("MN2", "n", "1.5u", L, D="m1", G="A2", S="m2", B="VSS")
c.mos("MN3", "n", "1.5u", L, D="m2", G="A3", S="VSS", B="VSS")

c = add(Cell("dffr_lv", "D:i:l CK:i:l CLRB:i:l Q:o:r QB:o:r VDD:io:t VSS:io:b",
             "rising-edge D flip-flop, NAND master-slave, active-low asynchronous clear of both latches (Q=0 while CLRB low; releasing it with CK high does not clock)"))
c.sub("XIC", "inv_lv", A="CK", Y="ckb", VDD="VDD", VSS="VSS")
c.sub("XID", "inv_lv", A="D", Y="dn", VDD="VDD", VSS="VSS")
c.sub("XSM", "nand3_lv", A1="D", A2="ckb", A3="CLRB", Y="sm", VDD="VDD", VSS="VSS")
c.sub("XRM", "nand2_lv", A1="dn", A2="ckb", Y="rm", VDD="VDD", VSS="VSS")
c.sub("XQM", "nand2_lv", A1="sm", A2="qmb", Y="qm", VDD="VDD", VSS="VSS")
c.sub("XQMB", "nand3_lv", A1="rm", A2="qm", A3="CLRB", Y="qmb", VDD="VDD", VSS="VSS")
c.sub("XSS", "nand3_lv", A1="qm", A2="CK", A3="CLRB", Y="ss", VDD="VDD", VSS="VSS")
c.sub("XRS", "nand2_lv", A1="qmb", A2="CK", Y="rs", VDD="VDD", VSS="VSS")
c.sub("XQ", "nand2_lv", A1="ss", A2="QB", Y="Q", VDD="VDD", VSS="VSS")
c.sub("XQB", "nand3_lv", A1="rs", A2="Q", A3="CLRB", Y="QB", VDD="VDD", VSS="VSS")

# Half-period window detector (0005 part 3). Three samples of the two taps:
#   a_up = TAPN at REF rise, a_dn = TAPN at REF fall, b_up = TAPH at REF rise.
# OVER = b_up & a_up & ~a_dn, true for d in (1.5 T, 2 T) (mod 2 T).
c = add(Cell("win_det", "REF:i:l TAPN:i:l TAPH:i:l OVER:o:r VDD:io:t VSS:io:b",
             "half-period window detector: OVER when tap N falls in the late half and tap N/2 has wrapped"))
c.sub("XIREF", "inv_lv", A="REF", Y="refb", VDD="VDD", VSS="VSS")
c.sub("XAUP", "dffr_lv", D="TAPN", CK="REF", CLRB="VDD", Q="a_up", QB="a_up_n", VDD="VDD", VSS="VSS")
c.sub("XADN", "dffr_lv", D="TAPN", CK="refb", CLRB="VDD", Q="a_dn", QB="a_dn_n", VDD="VDD", VSS="VSS")
c.sub("XBUP", "dffr_lv", D="TAPH", CK="REF", CLRB="VDD", Q="b_up", QB="b_up_n", VDD="VDD", VSS="VSS")
c.sub("XNO", "nand3_lv", A1="b_up", A2="a_up", A3="a_dn_n", Y="over_n", VDD="VDD", VSS="VSS")
c.sub("XIO", "inv_lv", A="over_n", Y="OVER", VDD="VDD", VSS="VSS")

# Rail proximity: resistor ladder VDD - 1u - REFH - 22u - REFL - 1u - VSS (REFH =
# 23/24 VDD, REFL = 1/24 VDD: 50 mV at 1.2 V), NMOS-input OTA for the high rail,
# PMOS-input OTA for the low rail, each followed by two inverters.
c = add(Cell("rail_cmp", "VCTRL:i:l NHI:o:r NLO:o:r NEAR:o:r VDD:io:t VSS:io:b",
             "VCTRL within ~50 mV of VDD (NHI) or VSS (NLO); NEAR = NHI or NLO"))
c.res("RA", "0.5u", "8u", "VDD", "refh")
for i in range(22):
    c.res(f"RB{i + 1}", "0.5u", "8u", "refh" if i == 0 else f"lad{i}", "refl" if i == 21 else f"lad{i + 1}")
c.res("RC", "0.5u", "8u", "refl", "VSS")
# Both inputs are level-shifted away from the rail by matched source followers so
# the pair keeps headroom (a pair fed directly at VDD - 50 mV sits in triode).
# NMOS-input pair: M1 (gate VCTRL) on the mirror diode, M2 (gate REFH) on the output
c.mos("MFH1", "n", "2u", "1u", D="VDD", G="VCTRL", S="vsh", B="VSS")
c.mos("MFH2", "n", "2u", "1u", D="VDD", G="refh", S="rsh", B="VSS")
c.mos("MSH1", "n", "0.5u", "1u", D="vsh", G="VDD", S="VSS", B="VSS")
c.mos("MSH2", "n", "0.5u", "1u", D="rsh", G="VDD", S="VSS", B="VSS")
c.mos("MTH", "n", "0.5u", "1u", D="tlh", G="VDD", S="VSS", B="VSS")
c.mos("MH1", "n", "4u", "1u", D="dh", G="vsh", S="tlh", B="VSS")
c.mos("MH2", "n", "4u", "1u", D="oh", G="rsh", S="tlh", B="VSS")
c.mos("MLH1", "p", "2u", "1u", D="dh", G="dh", S="VDD", B="VDD")
c.mos("MLH2", "p", "2u", "1u", D="oh", G="dh", S="VDD", B="VDD")
c.sub("XH1", "inv_lv", A="oh", Y="ohb", VDD="VDD", VSS="VSS")
c.sub("XH2", "inv_lv", A="ohb", Y="NHI", VDD="VDD", VSS="VSS")
# PMOS-input pair: M1 (gate REFL) on the mirror diode, M2 (gate VCTRL) on the output
c.mos("MFL1", "p", "8u", L, D="VSS", G="VCTRL", S="vsl", B="VDD")
c.mos("MFL2", "p", "8u", L, D="VSS", G="refl", S="rsl", B="VDD")
c.mos("MSL1", "p", "1.5u", "1u", D="vsl", G="VSS", S="VDD", B="VDD")
c.mos("MSL2", "p", "1.5u", "1u", D="rsl", G="VSS", S="VDD", B="VDD")
c.mos("MTL", "p", "1.5u", "1u", D="tll", G="VSS", S="VDD", B="VDD")
c.mos("MPL1", "p", "4u", "0.5u", D="dl", G="rsl", S="tll", B="VDD")
c.mos("MPL2", "p", "4u", "0.5u", D="ol", G="vsl", S="tll", B="VDD")
c.mos("MLL1", "n", "1u", "0.5u", D="dl", G="dl", S="VSS", B="VSS")
c.mos("MLL2", "n", "1u", "0.5u", D="ol", G="dl", S="VSS", B="VSS")
c.sub("XL1", "inv_lv", A="ol", Y="olb", VDD="VDD", VSS="VSS")
c.sub("XL2", "inv_lv", A="olb", Y="NLO", VDD="VDD", VSS="VSS")
c.sub("XNH", "inv_lv", A="NHI", Y="nhi_n", VDD="VDD", VSS="VSS")
c.sub("XNL", "inv_lv", A="NLO", Y="nlo_n", VDD="VDD", VSS="VSS")
c.sub("XNE", "nand2_lv", A1="nhi_n", A2="nlo_n", Y="NEAR", VDD="VDD", VSS="VSS")

# 5-stage ripple counter of REF rising edges while NEAR; TO rises at the 16th.
c = add(Cell("timeout_cnt", "REF:i:l NEAR:i:l TO:o:r VDD:io:t VSS:io:b",
             "5-bit ripple counter of REF rises, cleared while NEAR is low; TO = bit 5 (16 REF cycles)"))
for i in range(1, 6):
    ck = "REF" if i == 1 else f"qb{i - 1}"
    q = "TO" if i == 5 else f"q{i}"
    c.sub(f"XC{i}", "dffr_lv", D=f"qb{i}", CK=ck, CLRB="NEAR", Q=q, QB=f"qb{i}", VDD="VDD", VSS="VSS")

# 0008: REF is enabled into the PFD by a flip-flop clocked on the falling REF edge,
# cleared by every supervisor reset.
c = add(Cell("refmask", "REF:i:l RSTB:i:l REFM:o:r VDD:io:t VSS:io:b",
             "masks REF until the first falling REF edge after RSTB goes high"))
c.sub("XIR", "inv_lv", A="REF", Y="refb", VDD="VDD", VSS="VSS")
c.sub("XEN", "dffr_lv", D="VDD", CK="refb", CLRB="RSTB", Q="en", QB="en_n", VDD="VDD", VSS="VSS")
c.sub("XAN", "nand2_lv", A1="REF", A2="en", Y="refm_n", VDD="VDD", VSS="VSS")
c.sub("XAI", "inv_lv", A="refm_n", Y="REFM", VDD="VDD", VSS="VSS")

c = add(Cell("supervisor",
             "REF:i:l TAPN:i:l TAPH:i:l EN:i:l VCTRL:io:l REFM:o:r RST:o:r VDD:io:t VSS:io:b",
             "false-lock supervisor: reset VCTRL high on EN low / over-delay / rail time-out, mask first REF edge after release"))
c.sub("XWIN", "win_det", REF="REF", TAPN="TAPN", TAPH="TAPH", OVER="over", VDD="VDD", VSS="VSS")
c.sub("XRAIL", "rail_cmp", VCTRL="VCTRL", NHI="nhi", NLO="nlo", NEAR="near", VDD="VDD", VSS="VSS")
c.sub("XCN", "nand2_lv", A1="near", A2="RSTB", Y="cnt_clr_n", VDD="VDD", VSS="VSS")
c.sub("XCI", "inv_lv", A="cnt_clr_n", Y="cnt_en", VDD="VDD", VSS="VSS")
c.sub("XCNT", "timeout_cnt", REF="REF", NEAR="cnt_en", TO="to", VDD="VDD", VSS="VSS")
c.sub("XET", "edgedet", X="to", OUT="pt", VDD="VDD", VSS="VSS")
c.sub("XIPO", "inv_lv", A="over", Y="over_n", VDD="VDD", VSS="VSS")
c.sub("XIPT", "inv_lv", A="pt", Y="pt_n", VDD="VDD", VSS="VSS")
c.sub("XSET", "nand3_lv", A1="over_n", A2="pt_n", A3="EN", Y="set", VDD="VDD", VSS="VSS")
c.sub("XISB", "inv_lv", A="set", Y="set_n", VDD="VDD", VSS="VSS")
c.sub("XRN", "nand2_lv", A1="nhi", A2="set_n", Y="clr_n", VDD="VDD", VSS="VSS")
c.sub("XRI", "inv_lv", A="clr_n", Y="clr", VDD="VDD", VSS="VSS")
c.sub("XLAT", "srlatch", S="set", R="clr", Q="RST", QB="RSTB", VDD="VDD", VSS="VSS")
c.mos("MRST", "p", "20u", L, D="VCTRL", G="RSTB", S="VDD", B="VDD")
c.sub("XMSK", "refmask", REF="REF", RSTB="RSTB", REFM="REFM", VDD="VDD", VSS="VSS")
