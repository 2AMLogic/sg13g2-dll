v {xschem version=3.4.8RC file_version=1.3
win_det -- half-period window detector: OVER when tap N falls in the late half and tap N/2 has wrapped
}
G {}
K {}
V {}
S {}
E {}
C {inv_lv.sym} 0 0 0 0 {name=XIREF}
C {lab_pin.sym} -60 0 0 0 {name=l1 lab=REF}
C {lab_pin.sym} 60 0 0 0 {name=l2 lab=refb}
C {lab_pin.sym} 0 -40 0 0 {name=l3 lab=VDD}
C {lab_pin.sym} 0 40 0 0 {name=l4 lab=VSS}
C {dffr_lv.sym} 300 0 0 0 {name=XAUP}
C {lab_pin.sym} 240 -20 0 0 {name=l5 lab=TAPN}
C {lab_pin.sym} 240 0 0 0 {name=l6 lab=REF}
C {lab_pin.sym} 240 20 0 0 {name=l7 lab=VDD}
C {lab_pin.sym} 360 -10 0 0 {name=l8 lab=a_up}
C {lab_pin.sym} 360 10 0 0 {name=l9 lab=a_up_n}
C {lab_pin.sym} 300 -50 0 0 {name=l10 lab=VDD}
C {lab_pin.sym} 300 50 0 0 {name=l11 lab=VSS}
C {dffr_lv.sym} 600 0 0 0 {name=XADN}
C {lab_pin.sym} 540 -20 0 0 {name=l12 lab=TAPN}
C {lab_pin.sym} 540 0 0 0 {name=l13 lab=refb}
C {lab_pin.sym} 540 20 0 0 {name=l14 lab=VDD}
C {lab_pin.sym} 660 -10 0 0 {name=l15 lab=a_dn}
C {lab_pin.sym} 660 10 0 0 {name=l16 lab=a_dn_n}
C {lab_pin.sym} 600 -50 0 0 {name=l17 lab=VDD}
C {lab_pin.sym} 600 50 0 0 {name=l18 lab=VSS}
C {dffr_lv.sym} 900 0 0 0 {name=XBUP}
C {lab_pin.sym} 840 -20 0 0 {name=l19 lab=TAPH}
C {lab_pin.sym} 840 0 0 0 {name=l20 lab=REF}
C {lab_pin.sym} 840 20 0 0 {name=l21 lab=VDD}
C {lab_pin.sym} 960 -10 0 0 {name=l22 lab=b_up}
C {lab_pin.sym} 960 10 0 0 {name=l23 lab=b_up_n}
C {lab_pin.sym} 900 -50 0 0 {name=l24 lab=VDD}
C {lab_pin.sym} 900 50 0 0 {name=l25 lab=VSS}
C {nand3_lv.sym} 1200 0 0 0 {name=XNO}
C {lab_pin.sym} 1140 -20 0 0 {name=l26 lab=b_up}
C {lab_pin.sym} 1140 0 0 0 {name=l27 lab=a_up}
C {lab_pin.sym} 1140 20 0 0 {name=l28 lab=a_dn_n}
C {lab_pin.sym} 1260 0 0 0 {name=l29 lab=over_n}
C {lab_pin.sym} 1200 -50 0 0 {name=l30 lab=VDD}
C {lab_pin.sym} 1200 50 0 0 {name=l31 lab=VSS}
C {inv_lv.sym} 0 220 0 0 {name=XIO}
C {lab_pin.sym} -60 220 0 0 {name=l32 lab=over_n}
C {lab_pin.sym} 60 220 0 0 {name=l33 lab=OVER}
C {lab_pin.sym} 0 180 0 0 {name=l34 lab=VDD}
C {lab_pin.sym} 0 260 0 0 {name=l35 lab=VSS}
C {ipin.sym} -400 -300 0 0 {name=p1 lab=REF}
C {ipin.sym} -400 -260 0 0 {name=p2 lab=TAPN}
C {ipin.sym} -400 -220 0 0 {name=p3 lab=TAPH}
C {opin.sym} -400 -180 0 0 {name=p4 lab=OVER}
C {iopin.sym} -400 -140 0 0 {name=p5 lab=VDD}
C {iopin.sym} -400 -100 0 0 {name=p6 lab=VSS}
