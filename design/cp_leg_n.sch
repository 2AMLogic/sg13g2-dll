v {xschem version=3.4.8RC file_version=1.3
cp_leg_n -- NMOS current-steering leg: mirror + cascode, switch to VOUT (DN high) or VDUMP
}
G {}
K {}
V {}
S {}
E {}
C {sg13g2_pr/sg13_lv_nmos.sym} 0 0 0 0 {name=M1 model=sg13_lv_nmos w=2u l=0.5u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 20 -30 0 0 {name=l1 lab=tail}
C {lab_pin.sym} -20 0 0 0 {name=l2 lab=IBN}
C {lab_pin.sym} 20 30 0 0 {name=l3 lab=VSS}
C {lab_pin.sym} 20 0 0 0 {name=l4 lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 300 0 0 0 {name=M2 model=sg13_lv_nmos w=2u l=0.5u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 320 -30 0 0 {name=l5 lab=sw}
C {lab_pin.sym} 280 0 0 0 {name=l6 lab=ICN}
C {lab_pin.sym} 320 30 0 0 {name=l7 lab=tail}
C {lab_pin.sym} 320 0 0 0 {name=l8 lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 600 0 0 0 {name=XSWO model=sg13_lv_nmos w=1u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 620 -30 0 0 {name=l9 lab=VOUT}
C {lab_pin.sym} 580 0 0 0 {name=l10 lab=DN}
C {lab_pin.sym} 620 30 0 0 {name=l11 lab=sw}
C {lab_pin.sym} 620 0 0 0 {name=l12 lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 900 0 0 0 {name=XSWD model=sg13_lv_nmos w=1u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 920 -30 0 0 {name=l13 lab=VDUMP}
C {lab_pin.sym} 880 0 0 0 {name=l14 lab=DNB}
C {lab_pin.sym} 920 30 0 0 {name=l15 lab=sw}
C {lab_pin.sym} 920 0 0 0 {name=l16 lab=VSS}
C {ipin.sym} -400 -300 0 0 {name=p1 lab=IBN}
C {ipin.sym} -400 -260 0 0 {name=p2 lab=ICN}
C {ipin.sym} -400 -220 0 0 {name=p3 lab=DN}
C {ipin.sym} -400 -180 0 0 {name=p4 lab=DNB}
C {opin.sym} -400 -140 0 0 {name=p5 lab=VOUT}
C {opin.sym} -400 -100 0 0 {name=p6 lab=VDUMP}
C {iopin.sym} -400 -60 0 0 {name=p7 lab=VSS}
