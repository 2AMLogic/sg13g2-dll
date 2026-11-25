#!/usr/bin/env python3
"""Generate cp.gds -- layout of design/cp.sch (issue #190).

Cascoded current-steering charge pump: two input inverters (XIUP/XIDN),
the PMOS and NMOS steering legs (cp_leg_p/cp_leg_n), and the unity-gain
dump buffer (cp_dumpbuf) -- 24 devices in 14 matched mos_array blocks,
placed in two rows:

    row A (pfet, activ bottom y=26): IP  LPM  LPS  BPT  BPA  BQA  BCP
    row B (nfet, activ bottom y=0):  IN  LNM  LNS  BNT  BNA  BRA  BCN

    IP/LPM/LPS    leg/inv PMOS    IN/LNM/LNS   leg/inv NMOS
    BPT/BPA/BQA   buffer PMOS     BNT/BNA/BRA  buffer NMOS
    BCP           decoupling PMOS BCN          decoupling NMOS

Unit maps (mos_array unit index -> netlist device):

    IP.U0=XIUP.XMP IP.U1=XIDN.XMP     IN.U0=XIUP.XMN IN.U1=XIDN.XMN
    LPM.U0=leg_p.M1 LPM.U1=leg_p.M2   LNM.U0=leg_n.M1 LNM.U1=leg_n.M2
    LPS.U0=leg_p.XSWO LPS.U1=leg_p.XSWD
    LNS.U0=leg_n.XSWO LNS.U1=leg_n.XSWD
    BNT=MNT  BNA.U0=MNA BNA.U1=MNB     BPT=MPT
    BPA.U0=MPA BPA.U1=MPB             BQA.U0=MQA BQA.U1=MQB
    BRA.U0=MRA BRA.U1=MRB             BCN=MCN  BCP=MCP

UP/DN leg matching: each leg's mirror pair (LPM/LNM) and switch pair
(LPS/LNS) is one mos_array with a dummy column at each end (the deck's
dummy marker drops them from extraction; their pads stay floating dead
metal, disclosed in layout/README.md).

Routing model (see layout/common.py): all horizontal runs are Metal2
tracks at unique y; vertical connections are Metal1 pad stubs or channel
runs; the layers cross freely and join only at drawn Via1s. Row A is
offset -0.6 in x from row B so no row-A down-stub shares a pad column
with a row-B up-stub. Body ties: one p+ substrate island ties every nfet
body to VSS; each pfet block's well gets an n+ island tied to VDD.

Run from the repo root:

    uv run --with klayout==0.30.13 python3 layout/cp/generate.py
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from common import Cell, Part  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cp.gds")

ROW_A_Y = 26.0   # pfet row activ bottom
DX_A = -0.6      # row-A x offset from row B

# --- Metal2 track y ledger (unique per net segment) ---------------------------
# bottom band (below row B)
Y_VSS, Y_UPB_B, Y_DNB_B = -1.0, -1.8, -2.6
Y_VOUT_B, Y_VDUMP_B = -3.4, -4.2
Y_TAILN, Y_SWN, Y_TN, Y_DA_B, Y_DP_B = -5.0, -5.8, -6.6, -7.4, -8.2
# middle band (between the rows)
Y_UP, Y_DN, Y_UPB_M, Y_DNB_M = 12.0, 12.7, 13.4, 14.1
Y_IBN, Y_ICN, Y_VOUT_M, Y_VDUMP_M = 15.0, 15.7, 16.4, 17.9
Y_TAILP, Y_SWP, Y_DA_M, Y_DP_M, Y_VDD = 18.6, 19.3, 20.0, 22.6, 23.4
Y_TP, Y_DP2 = 24.1, 24.8  # tp and dp's upper branch (BQA.U0.D pad column
#   cannot share x with BRA.U0.G's stub, so BQA.U0.D joins dp higher up)
# top band (above row A)
Y_UP_T, Y_DN_T, Y_UPB_T, Y_DNB_T, Y_IBP, Y_ICP = 31.4, 32.1, 32.8, 33.5, 34.2, 35.0
Y_VOUT_T, Y_VDUMP_T, Y_DA_T = 43.7, 44.4, 45.1

# vertical channels: x, and the y span they bridge
V_UP_A, V_DN_A, V_UPB_A, V_DNB_A = 6.4, 7.2, 8.0, 8.8          # row-A gap 1
V_VOUT_A, V_VDUMP_A, V_DA_A = 53.0, 53.8, 54.6                 # row-A gap 2
V_UPB_B, V_DNB_B = 4.6, 5.4                                    # row-B gap 1
V_VOUT_B, V_VDUMP_BX = 19.4, 20.2                              # row-B gap 2
V_DA_B = 40.0                                                  # row-B gap 3
V_DP_B = 67.4                                                  # row-B gap 4


def part(name, flavor, w, l, cols, dummy):
    return Part(name, "mos_array",
                {"rows": 1, "cols": cols, "dummy": dummy, "flavor": flavor,
                 "w_um": w, "l_um": l, "topology": "array",
                 "gate_contact": True}, HERE)


c = Cell("cp")
# row B (nfet)
i_n = c.place(part("cp_in", "nfet", 0.5, 0.13, 2, 1), 0.0, 0.0)
lnm = c.place(part("cp_lnm", "nfet", 2.0, 0.5, 2, 1), 12.0, 0.0)
lns = c.place(part("cp_lns", "nfet", 1.0, 0.13, 2, 1), 26.0, 0.0)
bnt = c.place(part("cp_bnt", "nfet", 2.0, 0.5, 1, 0), 38.0, 0.0)
bna = c.place(part("cp_bna", "nfet", 8.0, 0.5, 2, 1), 44.0, 0.0)
bra = c.place(part("cp_bra", "nfet", 2.0, 1.0, 2, 1), 58.0, 0.0)
bcn = c.place(part("cp_bcn", "nfet", 4.0, 4.0, 1, 0), 72.0, 0.0)
# row A (pfet), offset DX_A
ip = c.place(part("cp_ip", "pfet", 1.0, 0.13, 2, 1), 0.0 + DX_A, ROW_A_Y)
lpm = c.place(part("cp_lpm", "pfet", 6.0, 0.5, 2, 1), 12.0 + DX_A, ROW_A_Y)
lps = c.place(part("cp_lps", "pfet", 3.0, 0.13, 2, 1), 26.0 + DX_A, ROW_A_Y)
bpt = c.place(part("cp_bpt", "pfet", 6.0, 0.5, 1, 0), 38.0 + DX_A, ROW_A_Y)
bpa = c.place(part("cp_bpa", "pfet", 6.0, 1.0, 2, 1), 44.0 + DX_A, ROW_A_Y)
bqa = c.place(part("cp_bqa", "pfet", 16.0, 0.5, 2, 1), 58.0 + DX_A, ROW_A_Y)
bcp = c.place(part("cp_bcp", "pfet", 4.0, 4.0, 1, 0), 72.0 + DX_A, ROW_A_Y)

# --- rails --------------------------------------------------------------------
c.m2("VSS", Y_VSS, 0.0, 79.2)
for pl, i in ((i_n, 0), (i_n, 1), (lnm, 0), (bnt, 0), (bra, 0), (bra, 1),
              (bcn, 0)):
    c.stub_sd_dn("VSS", pl, i, "s", Y_VSS)
c.stub_sd_dn("VSS", bcn, 0, "d", Y_VSS)
c.psub_tap(78.6, -0.5, "VSS", Y_VSS)
c.label("VSS", 30.0, Y_VSS)

c.m2("VDD", Y_VDD, -0.6, 78.0)
for pl, i in ((ip, 0), (ip, 1), (lpm, 0), (bpt, 0), (bpa, 0), (bpa, 1)):
    c.stub_sd_dn("VDD", pl, i, "s", Y_VDD)
c.stub_sd_dn("VDD", bcp, 0, "d", Y_VDD)
c.stub_sd_dn("VDD", bcp, 0, "s", Y_VDD)
for pl in (ip, lpm, lps, bqa, bcp):
    c.well_tie(pl, "VDD", Y_VDD)
c.well_tie(bpt, "VDD", Y_VDD, side="left")
c.well_tie(bpa, "VDD", Y_VDD)
c.label("VDD", 30.0, Y_VDD)

# --- inverter inputs and legs ---------------------------------------------------
# UP: IP.U0.G (top), IN.U0.G (mid), LPS.U1.G (top)
c.m2("UP", Y_UP, i_n.pad(0, "g")[0] - 0.3, V_UP_A)
c.stub_g_up("UP", i_n, 0, Y_UP)
c.vrun("UP", V_UP_A, Y_UP, Y_UP_T)
c.via("UP", V_UP_A, Y_UP)
c.via("UP", V_UP_A, Y_UP_T)
c.m2("UP", Y_UP_T, ip.pad(0, "g")[0] - 0.3, lps.pad(1, "g")[1] + 0.3)
c.stub_g_up("UP", ip, 0, Y_UP_T)
c.stub_g_up("UP", lps, 1, Y_UP_T)
c.label("UP", 16.0, Y_UP_T)

# DN: IP.U1.G (top), IN.U1.G (mid), LNS.U0.G (mid)
c.m2("DN", Y_DN, i_n.pad(1, "g")[0] - 0.3, lns.pad(0, "g")[1] + 0.3)
c.stub_g_up("DN", i_n, 1, Y_DN)
c.stub_g_up("DN", lns, 0, Y_DN)
c.vrun("DN", V_DN_A, Y_DN, Y_DN_T)
c.via("DN", V_DN_A, Y_DN)
c.via("DN", V_DN_A, Y_DN_T)
c.m2("DN", Y_DN_T, ip.pad(1, "g")[0] - 0.3, V_DN_A)
c.stub_g_up("DN", ip, 1, Y_DN_T)
c.label("DN", 16.0, Y_DN_T)

# UPB: IP.U0.D (mid), IN.U0.D (bottom), LPS.U0.G (top)
c.m2("UPB", Y_UPB_M, ip.pad(0, "d")[0] - 0.3, V_UPB_A)
c.stub_sd_dn("UPB", ip, 0, "d", Y_UPB_M)
c.vrun("UPB", V_UPB_A, Y_UPB_M, Y_UPB_T)
c.via("UPB", V_UPB_A, Y_UPB_M)
c.via("UPB", V_UPB_A, Y_UPB_T)
c.m2("UPB", Y_UPB_T, lps.pad(0, "g")[1], V_UPB_A)
c.stub_g_up("UPB", lps, 0, Y_UPB_T)
c.m2("UPB", Y_UPB_B, i_n.pad(0, "d")[0] - 0.3, V_UPB_B)
c.stub_sd_dn("UPB", i_n, 0, "d", Y_UPB_B)
c.vrun("UPB", V_UPB_B, Y_UPB_B, Y_UPB_M)
c.via("UPB", V_UPB_B, Y_UPB_B)
c.via("UPB", V_UPB_B, Y_UPB_M)
c.label("UPB", 12.0, Y_UPB_T)

# DNB: IP.U1.D (mid), IN.U1.D (bottom), LNS.U1.G (mid)
c.m2("DNB", Y_DNB_M, min(ip.pad(1, "d")[0], lns.pad(1, "g")[0]) - 0.3,
     max(ip.pad(1, "d")[0], lns.pad(1, "g")[0]) + 0.3)
c.stub_sd_dn("DNB", ip, 1, "d", Y_DNB_M)
c.stub_g_up("DNB", lns, 1, Y_DNB_M)
c.m2("DNB", Y_DNB_B, i_n.pad(1, "d")[0] - 0.3, V_DNB_B)
c.stub_sd_dn("DNB", i_n, 1, "d", Y_DNB_B)
c.vrun("DNB", V_DNB_B, Y_DNB_B, Y_DNB_M)
c.via("DNB", V_DNB_B, Y_DNB_B)
c.via("DNB", V_DNB_B, Y_DNB_M)

# --- leg internals ---------------------------------------------------------------
# tail_p: LPM.U0.D + LPM.U1.S (under LPM)
c.m2("tail_p", Y_TAILP, lpm.pad(0, "d")[0] - 0.3, lpm.pad(1, "s")[1] + 0.3)
c.stub_sd_dn("tail_p", lpm, 0, "d", Y_TAILP)
c.stub_sd_dn("tail_p", lpm, 1, "s", Y_TAILP)

# sw_p: LPM.U1.D + LPS.U0.S + LPS.U1.S
c.m2("sw_p", Y_SWP, lpm.pad(1, "d")[0] - 0.3, lps.pad(1, "s")[1] + 0.3)
c.stub_sd_dn("sw_p", lpm, 1, "d", Y_SWP)
c.stub_sd_dn("sw_p", lps, 0, "s", Y_SWP)
c.stub_sd_dn("sw_p", lps, 1, "s", Y_SWP)

# tail_n: LNM.U0.D + LNM.U1.S (under LNM)
c.m2("tail_n", Y_TAILN, lnm.pad(0, "d")[0] - 0.3, lnm.pad(1, "s")[1] + 0.3)
c.stub_sd_dn("tail_n", lnm, 0, "d", Y_TAILN)
c.stub_sd_dn("tail_n", lnm, 1, "s", Y_TAILN)

# sw_n: LNM.U1.D + LNS.U0.S + LNS.U1.S
c.m2("sw_n", Y_SWN, lnm.pad(1, "d")[0] - 0.3, lns.pad(1, "s")[1] + 0.3)
c.stub_sd_dn("sw_n", lnm, 1, "d", Y_SWN)
c.stub_sd_dn("sw_n", lns, 0, "s", Y_SWN)
c.stub_sd_dn("sw_n", lns, 1, "s", Y_SWN)

# --- VOUT pin: legs' switches, buffer inputs -------------------------------------
c.m2("VOUT", Y_VOUT_M, V_VOUT_B, max(V_VOUT_A, bna.pad(0, "g")[1]))
c.stub_sd_dn("VOUT", lps, 0, "d", Y_VOUT_M)
c.stub_g_up("VOUT", bna, 0, Y_VOUT_M)
c.m2("VOUT", Y_VOUT_B, lns.pad(0, "d")[1], V_VOUT_B)
c.stub_sd_dn("VOUT", lns, 0, "d", Y_VOUT_B)
c.vrun("VOUT", V_VOUT_B, Y_VOUT_B, Y_VOUT_M)
c.via("VOUT", V_VOUT_B, Y_VOUT_B)
c.via("VOUT", V_VOUT_B, Y_VOUT_M)
c.vrun("VOUT", V_VOUT_A, Y_VOUT_M, Y_VOUT_T)
c.via("VOUT", V_VOUT_A, Y_VOUT_M)
c.via("VOUT", V_VOUT_A, Y_VOUT_T)
c.m2("VOUT", Y_VOUT_T, V_VOUT_A, bqa.pad(0, "g")[1] + 0.3)
c.stub_g_up("VOUT", bqa, 0, Y_VOUT_T)
c.label("VOUT", 30.0, Y_VOUT_M)

# --- VDUMP (internal): legs' dump switches, buffer outputs, decoupling gates ------
c.m2("VDUMP", Y_VDUMP_M, V_VDUMP_BX, bcn.pad(0, "g")[1])
c.stub_sd_dn("VDUMP", lps, 1, "d", Y_VDUMP_M)
c.stub_sd_dn("VDUMP", bpa, 1, "d", Y_VDUMP_M)
c.stub_sd_dn("VDUMP", bqa, 1, "d", Y_VDUMP_M)
c.stub_g_up("VDUMP", bna, 1, Y_VDUMP_M)
c.stub_g_up("VDUMP", bcn, 0, Y_VDUMP_M)
c.m2("VDUMP", Y_VDUMP_B, V_VDUMP_BX, bra.pad(1, "d")[1])
c.stub_sd_dn("VDUMP", lns, 1, "d", Y_VDUMP_B)
c.stub_sd_dn("VDUMP", bna, 1, "d", Y_VDUMP_B)
c.stub_sd_dn("VDUMP", bra, 1, "d", Y_VDUMP_B)
c.vrun("VDUMP", V_VDUMP_BX, Y_VDUMP_B, Y_VDUMP_M)
c.via("VDUMP", V_VDUMP_BX, Y_VDUMP_B)
c.via("VDUMP", V_VDUMP_BX, Y_VDUMP_M)
c.vrun("VDUMP", V_VDUMP_A, Y_VDUMP_M, Y_VDUMP_T)
c.via("VDUMP", V_VDUMP_A, Y_VDUMP_M)
c.via("VDUMP", V_VDUMP_A, Y_VDUMP_T)
c.m2("VDUMP", Y_VDUMP_T, V_VDUMP_A, bcp.pad(0, "g")[1] + 0.3)
c.stub_g_up("VDUMP", bqa, 1, Y_VDUMP_T)
c.stub_g_up("VDUMP", bcp, 0, Y_VDUMP_T)

# --- bias pins ----------------------------------------------------------------------
c.m2("IBP", Y_IBP, lpm.pad(0, "g")[0] - 0.3, bpt.pad(0, "g")[1] + 0.3)
c.stub_g_up("IBP", lpm, 0, Y_IBP)
c.stub_g_up("IBP", bpt, 0, Y_IBP)
c.label("IBP", 25.0, Y_IBP)

c.m2("ICP", Y_ICP, lpm.pad(1, "g")[0] - 0.3, lpm.pad(1, "g")[1] + 0.3)
c.stub_g_up("ICP", lpm, 1, Y_ICP)
c.label("ICP", lpm.pad(1, "g")[0], Y_ICP)

c.m2("IBN", Y_IBN, lnm.pad(0, "g")[0] - 0.3, bnt.pad(0, "g")[1] + 0.3)
c.stub_g_up("IBN", lnm, 0, Y_IBN)
c.stub_g_up("IBN", bnt, 0, Y_IBN)
c.label("IBN", 25.0, Y_IBN)

c.m2("ICN", Y_ICN, lnm.pad(1, "g")[0] - 0.3, lnm.pad(1, "g")[1] + 0.3)
c.stub_g_up("ICN", lnm, 1, Y_ICN)
c.label("ICN", lnm.pad(1, "g")[0], Y_ICN)

# --- buffer internals --------------------------------------------------------------
# tn: MNT drain + MNA/MNB sources
c.m2("tn", Y_TN, bnt.pad(0, "d")[0] - 0.3, bna.pad(1, "s")[1] + 0.3)
c.stub_sd_dn("tn", bnt, 0, "d", Y_TN)
c.stub_sd_dn("tn", bna, 0, "s", Y_TN)
c.stub_sd_dn("tn", bna, 1, "s", Y_TN)

# da: MNA drain (bottom), MPA drain (mid), MPA/MPB gates (top)
c.m2("da", Y_DA_B, bna.pad(0, "d")[1], V_DA_B)
c.stub_sd_dn("da", bna, 0, "d", Y_DA_B)
c.vrun("da", V_DA_B, Y_DA_B, Y_DA_M)
c.via("da", V_DA_B, Y_DA_B)
c.via("da", V_DA_B, Y_DA_M)
c.m2("da", Y_DA_M, V_DA_B, V_DA_A)
c.stub_sd_dn("da", bpa, 0, "d", Y_DA_M)
c.vrun("da", V_DA_A, Y_DA_M, Y_DA_T)
c.via("da", V_DA_A, Y_DA_M)
c.via("da", V_DA_A, Y_DA_T)
c.m2("da", Y_DA_T, bpa.pad(0, "g")[0] - 0.3, V_DA_A)
c.stub_g_up("da", bpa, 0, Y_DA_T)
c.stub_g_up("da", bpa, 1, Y_DA_T)

# tp: MPT drain + MQA/MQB sources
c.m2("tp", Y_TP, bpt.pad(0, "d")[0] - 0.3, bqa.pad(1, "s")[1] + 0.3)
c.stub_sd_dn("tp", bpt, 0, "d", Y_TP)
c.stub_sd_dn("tp", bqa, 0, "s", Y_TP)
c.stub_sd_dn("tp", bqa, 1, "s", Y_TP)

# dp: MQA drain (upper branch), MRA drain (bottom), MRA/MRB gates (mid)
c.m2("dp", Y_DP2, bqa.pad(0, "d")[0] - 0.3, V_DP_B)
c.stub_sd_dn("dp", bqa, 0, "d", Y_DP2)
c.vrun("dp", V_DP_B, Y_DP_B, Y_DP2)
c.via("dp", V_DP_B, Y_DP2)
c.m2("dp", Y_DP_M, bra.pad(0, "g")[0] - 0.3, V_DP_B)
c.stub_g_up("dp", bra, 0, Y_DP_M)
c.stub_g_up("dp", bra, 1, Y_DP_M)
c.via("dp", V_DP_B, Y_DP_M)
c.m2("dp", Y_DP_B, bra.pad(0, "d")[0] - 0.3, V_DP_B)
c.stub_sd_dn("dp", bra, 0, "d", Y_DP_B)
c.via("dp", V_DP_B, Y_DP_B)

c.write(OUT)
print("wrote", OUT)
