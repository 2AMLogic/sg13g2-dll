v {xschem version=3.4.8RC file_version=1.3
inv2x_lv -- 2x inverter, sg13_lv
}
G {}
K {}
V {}
S {}
E {}
C {sg13g2_pr/sg13_lv_pmos.sym} 0 0 0 0 {name=MP model=sg13_lv_pmos w=2u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 20 30 0 0 {name=l1 lab=Y}
C {lab_pin.sym} -20 0 0 0 {name=l2 lab=A}
C {lab_pin.sym} 20 -30 0 0 {name=l3 lab=VDD}
C {lab_pin.sym} 20 0 0 0 {name=l4 lab=VDD}
C {sg13g2_pr/sg13_lv_nmos.sym} 300 0 0 0 {name=MN model=sg13_lv_nmos w=1u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 320 -30 0 0 {name=l5 lab=Y}
C {lab_pin.sym} 280 0 0 0 {name=l6 lab=A}
C {lab_pin.sym} 320 30 0 0 {name=l7 lab=VSS}
C {lab_pin.sym} 320 0 0 0 {name=l8 lab=VSS}
C {ipin.sym} -400 -300 0 0 {name=p1 lab=A}
C {opin.sym} -400 -260 0 0 {name=p2 lab=Y}
C {iopin.sym} -400 -220 0 0 {name=p3 lab=VDD}
C {iopin.sym} -400 -180 0 0 {name=p4 lab=VSS}
