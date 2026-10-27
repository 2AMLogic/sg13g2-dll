v {xschem version=3.4.8RC file_version=1.3
cp_dumpbuf -- source-follower dump buffer: VDUMP tracks VOUT one Vgs below
}
G {}
K {}
V {}
S {}
E {}
C {sg13g2_pr/sg13_lv_nmos.sym} 0 0 0 0 {name=M1 model=sg13_lv_nmos w=2u l=0.25u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 20 -30 0 0 {name=l1 lab=VDD}
C {lab_pin.sym} -20 0 0 0 {name=l2 lab=VOUT}
C {lab_pin.sym} 20 30 0 0 {name=l3 lab=VDUMP}
C {lab_pin.sym} 20 0 0 0 {name=l4 lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 300 0 0 0 {name=M2 model=sg13_lv_nmos w=1u l=0.5u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 320 -30 0 0 {name=l5 lab=VDUMP}
C {lab_pin.sym} 280 0 0 0 {name=l6 lab=IBIAS}
C {lab_pin.sym} 320 30 0 0 {name=l7 lab=VSS}
C {lab_pin.sym} 320 0 0 0 {name=l8 lab=VSS}
C {ipin.sym} -400 -300 0 0 {name=p1 lab=VOUT}
C {ipin.sym} -400 -260 0 0 {name=p2 lab=IBIAS}
C {opin.sym} -400 -220 0 0 {name=p3 lab=VDUMP}
C {iopin.sym} -400 -180 0 0 {name=p4 lab=VDD}
C {iopin.sym} -400 -140 0 0 {name=p5 lab=VSS}
