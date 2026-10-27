v {xschem version=3.4.8RC file_version=1.3
pfd -- tri-state PFD: 2x edgedet + 2x srlatch, reset = AND(UP,DN) delayed by NAND + 3 inverters
}
G {}
K {}
V {}
S {}
E {}
C {edgedet.sym} 0 0 0 0 {name=XED_UP}
C {lab_pin.sym} -60 0 0 0 {name=l1 lab=REF}
C {lab_pin.sym} 60 0 0 0 {name=l2 lab=set_up}
C {lab_pin.sym} 0 -40 0 0 {name=l3 lab=VDD}
C {lab_pin.sym} 0 40 0 0 {name=l4 lab=VSS}
C {edgedet.sym} 300 0 0 0 {name=XED_DN}
C {lab_pin.sym} 240 0 0 0 {name=l5 lab=FB}
C {lab_pin.sym} 360 0 0 0 {name=l6 lab=set_dn}
C {lab_pin.sym} 300 -40 0 0 {name=l7 lab=VDD}
C {lab_pin.sym} 300 40 0 0 {name=l8 lab=VSS}
C {srlatch.sym} 600 0 0 0 {name=XLU}
C {lab_pin.sym} 540 -10 0 0 {name=l9 lab=set_up}
C {lab_pin.sym} 540 10 0 0 {name=l10 lab=reset}
C {lab_pin.sym} 660 -10 0 0 {name=l11 lab=UP}
C {lab_pin.sym} 660 10 0 0 {name=l12 lab=upb_n}
C {lab_pin.sym} 600 -40 0 0 {name=l13 lab=VDD}
C {lab_pin.sym} 600 40 0 0 {name=l14 lab=VSS}
C {srlatch.sym} 900 0 0 0 {name=XLD}
C {lab_pin.sym} 840 -10 0 0 {name=l15 lab=set_dn}
C {lab_pin.sym} 840 10 0 0 {name=l16 lab=reset}
C {lab_pin.sym} 960 -10 0 0 {name=l17 lab=DN}
C {lab_pin.sym} 960 10 0 0 {name=l18 lab=dnb_n}
C {lab_pin.sym} 900 -40 0 0 {name=l19 lab=VDD}
C {lab_pin.sym} 900 40 0 0 {name=l20 lab=VSS}
C {nand2_lv.sym} 1200 0 0 0 {name=XNR}
C {lab_pin.sym} 1140 -10 0 0 {name=l21 lab=UP}
C {lab_pin.sym} 1140 10 0 0 {name=l22 lab=DN}
C {lab_pin.sym} 1260 0 0 0 {name=l23 lab=reset_n0}
C {lab_pin.sym} 1200 -40 0 0 {name=l24 lab=VDD}
C {lab_pin.sym} 1200 40 0 0 {name=l25 lab=VSS}
C {inv_lv.sym} 0 220 0 0 {name=XR1}
C {lab_pin.sym} -60 220 0 0 {name=l26 lab=reset_n0}
C {lab_pin.sym} 60 220 0 0 {name=l27 lab=reset_p1}
C {lab_pin.sym} 0 180 0 0 {name=l28 lab=VDD}
C {lab_pin.sym} 0 260 0 0 {name=l29 lab=VSS}
C {inv_lv.sym} 300 220 0 0 {name=XR2}
C {lab_pin.sym} 240 220 0 0 {name=l30 lab=reset_p1}
C {lab_pin.sym} 360 220 0 0 {name=l31 lab=reset_n2}
C {lab_pin.sym} 300 180 0 0 {name=l32 lab=VDD}
C {lab_pin.sym} 300 260 0 0 {name=l33 lab=VSS}
C {inv2x_lv.sym} 600 220 0 0 {name=XR3}
C {lab_pin.sym} 540 220 0 0 {name=l34 lab=reset_n2}
C {lab_pin.sym} 660 220 0 0 {name=l35 lab=reset}
C {lab_pin.sym} 600 180 0 0 {name=l36 lab=VDD}
C {lab_pin.sym} 600 260 0 0 {name=l37 lab=VSS}
C {ipin.sym} -400 -300 0 0 {name=p1 lab=REF}
C {ipin.sym} -400 -260 0 0 {name=p2 lab=FB}
C {opin.sym} -400 -220 0 0 {name=p3 lab=UP}
C {opin.sym} -400 -180 0 0 {name=p4 lab=DN}
C {iopin.sym} -400 -140 0 0 {name=p5 lab=VDD}
C {iopin.sym} -400 -100 0 0 {name=p6 lab=VSS}
