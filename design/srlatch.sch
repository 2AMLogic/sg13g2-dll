v {xschem version=3.4.8RC file_version=1.3
srlatch -- set/reset latch from two NAND2 with inverted inputs (S, R active high)
}
G {}
K {}
V {}
S {}
E {}
C {inv_lv.sym} 0 0 0 0 {name=XIS}
C {lab_pin.sym} -60 0 0 0 {name=l1 lab=S}
C {lab_pin.sym} 60 0 0 0 {name=l2 lab=SB}
C {lab_pin.sym} 0 -40 0 0 {name=l3 lab=VDD}
C {lab_pin.sym} 0 40 0 0 {name=l4 lab=VSS}
C {inv_lv.sym} 300 0 0 0 {name=XIR}
C {lab_pin.sym} 240 0 0 0 {name=l5 lab=R}
C {lab_pin.sym} 360 0 0 0 {name=l6 lab=RB}
C {lab_pin.sym} 300 -40 0 0 {name=l7 lab=VDD}
C {lab_pin.sym} 300 40 0 0 {name=l8 lab=VSS}
C {nand2_lv.sym} 600 0 0 0 {name=XNQ}
C {lab_pin.sym} 540 -10 0 0 {name=l9 lab=SB}
C {lab_pin.sym} 540 10 0 0 {name=l10 lab=QB}
C {lab_pin.sym} 660 0 0 0 {name=l11 lab=Q}
C {lab_pin.sym} 600 -40 0 0 {name=l12 lab=VDD}
C {lab_pin.sym} 600 40 0 0 {name=l13 lab=VSS}
C {nand2_lv.sym} 900 0 0 0 {name=XNQB}
C {lab_pin.sym} 840 -10 0 0 {name=l14 lab=RB}
C {lab_pin.sym} 840 10 0 0 {name=l15 lab=Q}
C {lab_pin.sym} 960 0 0 0 {name=l16 lab=QB}
C {lab_pin.sym} 900 -40 0 0 {name=l17 lab=VDD}
C {lab_pin.sym} 900 40 0 0 {name=l18 lab=VSS}
C {ipin.sym} -400 -300 0 0 {name=p1 lab=S}
C {ipin.sym} -400 -260 0 0 {name=p2 lab=R}
C {opin.sym} -400 -220 0 0 {name=p3 lab=Q}
C {opin.sym} -400 -180 0 0 {name=p4 lab=QB}
C {iopin.sym} -400 -140 0 0 {name=p5 lab=VDD}
C {iopin.sym} -400 -100 0 0 {name=p6 lab=VSS}
