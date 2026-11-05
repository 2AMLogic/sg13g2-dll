v {xschem version=3.4.8RC file_version=1.3
dffr_lv -- rising-edge D flip-flop, NAND master-slave, active-low asynchronous clear of both latches (Q=0 while CLRB low; releasing it with CK high does not clock)
}
G {}
K {}
V {}
S {}
E {}
C {inv_lv.sym} 0 0 0 0 {name=XIC}
C {lab_pin.sym} -60 0 0 0 {name=l1 lab=CK}
C {lab_pin.sym} 60 0 0 0 {name=l2 lab=ckb}
C {lab_pin.sym} 0 -40 0 0 {name=l3 lab=VDD}
C {lab_pin.sym} 0 40 0 0 {name=l4 lab=VSS}
C {inv_lv.sym} 300 0 0 0 {name=XID}
C {lab_pin.sym} 240 0 0 0 {name=l5 lab=D}
C {lab_pin.sym} 360 0 0 0 {name=l6 lab=dn}
C {lab_pin.sym} 300 -40 0 0 {name=l7 lab=VDD}
C {lab_pin.sym} 300 40 0 0 {name=l8 lab=VSS}
C {nand3_lv.sym} 600 0 0 0 {name=XSM}
C {lab_pin.sym} 540 -20 0 0 {name=l9 lab=D}
C {lab_pin.sym} 540 0 0 0 {name=l10 lab=ckb}
C {lab_pin.sym} 540 20 0 0 {name=l11 lab=CLRB}
C {lab_pin.sym} 660 0 0 0 {name=l12 lab=sm}
C {lab_pin.sym} 600 -50 0 0 {name=l13 lab=VDD}
C {lab_pin.sym} 600 50 0 0 {name=l14 lab=VSS}
C {nand2_lv.sym} 900 0 0 0 {name=XRM}
C {lab_pin.sym} 840 -10 0 0 {name=l15 lab=dn}
C {lab_pin.sym} 840 10 0 0 {name=l16 lab=ckb}
C {lab_pin.sym} 960 0 0 0 {name=l17 lab=rm}
C {lab_pin.sym} 900 -40 0 0 {name=l18 lab=VDD}
C {lab_pin.sym} 900 40 0 0 {name=l19 lab=VSS}
C {nand2_lv.sym} 1200 0 0 0 {name=XQM}
C {lab_pin.sym} 1140 -10 0 0 {name=l20 lab=sm}
C {lab_pin.sym} 1140 10 0 0 {name=l21 lab=qmb}
C {lab_pin.sym} 1260 0 0 0 {name=l22 lab=qm}
C {lab_pin.sym} 1200 -40 0 0 {name=l23 lab=VDD}
C {lab_pin.sym} 1200 40 0 0 {name=l24 lab=VSS}
C {nand3_lv.sym} 0 220 0 0 {name=XQMB}
C {lab_pin.sym} -60 200 0 0 {name=l25 lab=rm}
C {lab_pin.sym} -60 220 0 0 {name=l26 lab=qm}
C {lab_pin.sym} -60 240 0 0 {name=l27 lab=CLRB}
C {lab_pin.sym} 60 220 0 0 {name=l28 lab=qmb}
C {lab_pin.sym} 0 170 0 0 {name=l29 lab=VDD}
C {lab_pin.sym} 0 270 0 0 {name=l30 lab=VSS}
C {nand3_lv.sym} 300 220 0 0 {name=XSS}
C {lab_pin.sym} 240 200 0 0 {name=l31 lab=qm}
C {lab_pin.sym} 240 220 0 0 {name=l32 lab=CK}
C {lab_pin.sym} 240 240 0 0 {name=l33 lab=CLRB}
C {lab_pin.sym} 360 220 0 0 {name=l34 lab=ss}
C {lab_pin.sym} 300 170 0 0 {name=l35 lab=VDD}
C {lab_pin.sym} 300 270 0 0 {name=l36 lab=VSS}
C {nand2_lv.sym} 600 220 0 0 {name=XRS}
C {lab_pin.sym} 540 210 0 0 {name=l37 lab=qmb}
C {lab_pin.sym} 540 230 0 0 {name=l38 lab=CK}
C {lab_pin.sym} 660 220 0 0 {name=l39 lab=rs}
C {lab_pin.sym} 600 180 0 0 {name=l40 lab=VDD}
C {lab_pin.sym} 600 260 0 0 {name=l41 lab=VSS}
C {nand2_lv.sym} 900 220 0 0 {name=XQ}
C {lab_pin.sym} 840 210 0 0 {name=l42 lab=ss}
C {lab_pin.sym} 840 230 0 0 {name=l43 lab=QB}
C {lab_pin.sym} 960 220 0 0 {name=l44 lab=Q}
C {lab_pin.sym} 900 180 0 0 {name=l45 lab=VDD}
C {lab_pin.sym} 900 260 0 0 {name=l46 lab=VSS}
C {nand3_lv.sym} 1200 220 0 0 {name=XQB}
C {lab_pin.sym} 1140 200 0 0 {name=l47 lab=rs}
C {lab_pin.sym} 1140 220 0 0 {name=l48 lab=Q}
C {lab_pin.sym} 1140 240 0 0 {name=l49 lab=CLRB}
C {lab_pin.sym} 1260 220 0 0 {name=l50 lab=QB}
C {lab_pin.sym} 1200 170 0 0 {name=l51 lab=VDD}
C {lab_pin.sym} 1200 270 0 0 {name=l52 lab=VSS}
C {ipin.sym} -400 -300 0 0 {name=p1 lab=D}
C {ipin.sym} -400 -260 0 0 {name=p2 lab=CK}
C {ipin.sym} -400 -220 0 0 {name=p3 lab=CLRB}
C {opin.sym} -400 -180 0 0 {name=p4 lab=Q}
C {opin.sym} -400 -140 0 0 {name=p5 lab=QB}
C {iopin.sym} -400 -100 0 0 {name=p6 lab=VDD}
C {iopin.sym} -400 -60 0 0 {name=p7 lab=VSS}
