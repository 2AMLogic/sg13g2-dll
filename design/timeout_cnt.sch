v {xschem version=3.4.8RC file_version=1.3
timeout_cnt -- 5-bit ripple counter of REF rises, cleared while NEAR is low; TO = bit 5 (16 REF cycles)
}
G {}
K {}
V {}
S {}
E {}
C {dffr_lv.sym} 0 0 0 0 {name=XC1}
C {lab_pin.sym} -60 -20 0 0 {name=l1 lab=qb1}
C {lab_pin.sym} -60 0 0 0 {name=l2 lab=REF}
C {lab_pin.sym} -60 20 0 0 {name=l3 lab=NEAR}
C {lab_pin.sym} 60 -10 0 0 {name=l4 lab=q1}
C {lab_pin.sym} 60 10 0 0 {name=l5 lab=qb1}
C {lab_pin.sym} 0 -50 0 0 {name=l6 lab=VDD}
C {lab_pin.sym} 0 50 0 0 {name=l7 lab=VSS}
C {dffr_lv.sym} 300 0 0 0 {name=XC2}
C {lab_pin.sym} 240 -20 0 0 {name=l8 lab=qb2}
C {lab_pin.sym} 240 0 0 0 {name=l9 lab=qb1}
C {lab_pin.sym} 240 20 0 0 {name=l10 lab=NEAR}
C {lab_pin.sym} 360 -10 0 0 {name=l11 lab=q2}
C {lab_pin.sym} 360 10 0 0 {name=l12 lab=qb2}
C {lab_pin.sym} 300 -50 0 0 {name=l13 lab=VDD}
C {lab_pin.sym} 300 50 0 0 {name=l14 lab=VSS}
C {dffr_lv.sym} 600 0 0 0 {name=XC3}
C {lab_pin.sym} 540 -20 0 0 {name=l15 lab=qb3}
C {lab_pin.sym} 540 0 0 0 {name=l16 lab=qb2}
C {lab_pin.sym} 540 20 0 0 {name=l17 lab=NEAR}
C {lab_pin.sym} 660 -10 0 0 {name=l18 lab=q3}
C {lab_pin.sym} 660 10 0 0 {name=l19 lab=qb3}
C {lab_pin.sym} 600 -50 0 0 {name=l20 lab=VDD}
C {lab_pin.sym} 600 50 0 0 {name=l21 lab=VSS}
C {dffr_lv.sym} 900 0 0 0 {name=XC4}
C {lab_pin.sym} 840 -20 0 0 {name=l22 lab=qb4}
C {lab_pin.sym} 840 0 0 0 {name=l23 lab=qb3}
C {lab_pin.sym} 840 20 0 0 {name=l24 lab=NEAR}
C {lab_pin.sym} 960 -10 0 0 {name=l25 lab=q4}
C {lab_pin.sym} 960 10 0 0 {name=l26 lab=qb4}
C {lab_pin.sym} 900 -50 0 0 {name=l27 lab=VDD}
C {lab_pin.sym} 900 50 0 0 {name=l28 lab=VSS}
C {dffr_lv.sym} 1200 0 0 0 {name=XC5}
C {lab_pin.sym} 1140 -20 0 0 {name=l29 lab=qb5}
C {lab_pin.sym} 1140 0 0 0 {name=l30 lab=qb4}
C {lab_pin.sym} 1140 20 0 0 {name=l31 lab=NEAR}
C {lab_pin.sym} 1260 -10 0 0 {name=l32 lab=TO}
C {lab_pin.sym} 1260 10 0 0 {name=l33 lab=qb5}
C {lab_pin.sym} 1200 -50 0 0 {name=l34 lab=VDD}
C {lab_pin.sym} 1200 50 0 0 {name=l35 lab=VSS}
C {ipin.sym} -400 -300 0 0 {name=p1 lab=REF}
C {ipin.sym} -400 -260 0 0 {name=p2 lab=NEAR}
C {opin.sym} -400 -220 0 0 {name=p3 lab=TO}
C {iopin.sym} -400 -180 0 0 {name=p4 lab=VDD}
C {iopin.sym} -400 -140 0 0 {name=p5 lab=VSS}
