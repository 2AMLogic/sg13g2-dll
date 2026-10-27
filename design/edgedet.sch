v {xschem version=3.4.8RC file_version=1.3
edgedet -- rising-edge pulse generator: X AND NOT(X delayed by 5 inverters)
}
G {}
K {}
V {}
S {}
E {}
C {inv_lv.sym} 0 0 0 0 {name=XD1}
C {lab_pin.sym} -60 0 0 0 {name=l1 lab=X}
C {lab_pin.sym} 60 0 0 0 {name=l2 lab=d1}
C {lab_pin.sym} 0 -40 0 0 {name=l3 lab=VDD}
C {lab_pin.sym} 0 40 0 0 {name=l4 lab=VSS}
C {inv_lv.sym} 300 0 0 0 {name=XD2}
C {lab_pin.sym} 240 0 0 0 {name=l5 lab=d1}
C {lab_pin.sym} 360 0 0 0 {name=l6 lab=d2}
C {lab_pin.sym} 300 -40 0 0 {name=l7 lab=VDD}
C {lab_pin.sym} 300 40 0 0 {name=l8 lab=VSS}
C {inv_lv.sym} 600 0 0 0 {name=XD3}
C {lab_pin.sym} 540 0 0 0 {name=l9 lab=d2}
C {lab_pin.sym} 660 0 0 0 {name=l10 lab=d3}
C {lab_pin.sym} 600 -40 0 0 {name=l11 lab=VDD}
C {lab_pin.sym} 600 40 0 0 {name=l12 lab=VSS}
C {inv_lv.sym} 900 0 0 0 {name=XD4}
C {lab_pin.sym} 840 0 0 0 {name=l13 lab=d3}
C {lab_pin.sym} 960 0 0 0 {name=l14 lab=d4}
C {lab_pin.sym} 900 -40 0 0 {name=l15 lab=VDD}
C {lab_pin.sym} 900 40 0 0 {name=l16 lab=VSS}
C {inv_lv.sym} 1200 0 0 0 {name=XD5}
C {lab_pin.sym} 1140 0 0 0 {name=l17 lab=d4}
C {lab_pin.sym} 1260 0 0 0 {name=l18 lab=d5}
C {lab_pin.sym} 1200 -40 0 0 {name=l19 lab=VDD}
C {lab_pin.sym} 1200 40 0 0 {name=l20 lab=VSS}
C {nand2_lv.sym} 0 220 0 0 {name=XN1}
C {lab_pin.sym} -60 210 0 0 {name=l21 lab=X}
C {lab_pin.sym} -60 230 0 0 {name=l22 lab=d5}
C {lab_pin.sym} 60 220 0 0 {name=l23 lab=ntmp}
C {lab_pin.sym} 0 180 0 0 {name=l24 lab=VDD}
C {lab_pin.sym} 0 260 0 0 {name=l25 lab=VSS}
C {inv_lv.sym} 300 220 0 0 {name=XOUT}
C {lab_pin.sym} 240 220 0 0 {name=l26 lab=ntmp}
C {lab_pin.sym} 360 220 0 0 {name=l27 lab=OUT}
C {lab_pin.sym} 300 180 0 0 {name=l28 lab=VDD}
C {lab_pin.sym} 300 260 0 0 {name=l29 lab=VSS}
C {ipin.sym} -400 -300 0 0 {name=p1 lab=X}
C {opin.sym} -400 -260 0 0 {name=p2 lab=OUT}
C {iopin.sym} -400 -220 0 0 {name=p3 lab=VDD}
C {iopin.sym} -400 -180 0 0 {name=p4 lab=VSS}
