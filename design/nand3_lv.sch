v {xschem version=3.4.8RC file_version=1.3
nand3_lv -- 3-input NAND, sg13_lv
}
G {}
K {}
V {}
S {}
E {}
C {sg13g2_pr/sg13_lv_pmos.sym} 0 0 0 0 {name=MP1 model=sg13_lv_pmos w=1u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 20 30 0 0 {name=l1 lab=Y}
C {lab_pin.sym} -20 0 0 0 {name=l2 lab=A1}
C {lab_pin.sym} 20 -30 0 0 {name=l3 lab=VDD}
C {lab_pin.sym} 20 0 0 0 {name=l4 lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 300 0 0 0 {name=MP2 model=sg13_lv_pmos w=1u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 320 30 0 0 {name=l5 lab=Y}
C {lab_pin.sym} 280 0 0 0 {name=l6 lab=A2}
C {lab_pin.sym} 320 -30 0 0 {name=l7 lab=VDD}
C {lab_pin.sym} 320 0 0 0 {name=l8 lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 600 0 0 0 {name=MP3 model=sg13_lv_pmos w=1u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 620 30 0 0 {name=l9 lab=Y}
C {lab_pin.sym} 580 0 0 0 {name=l10 lab=A3}
C {lab_pin.sym} 620 -30 0 0 {name=l11 lab=VDD}
C {lab_pin.sym} 620 0 0 0 {name=l12 lab=VDD}
C {sg13g2_pr/sg13_lv_nmos.sym} 900 0 0 0 {name=MN1 model=sg13_lv_nmos w=1.5u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 920 -30 0 0 {name=l13 lab=Y}
C {lab_pin.sym} 880 0 0 0 {name=l14 lab=A1}
C {lab_pin.sym} 920 30 0 0 {name=l15 lab=m1}
C {lab_pin.sym} 920 0 0 0 {name=l16 lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 1200 0 0 0 {name=MN2 model=sg13_lv_nmos w=1.5u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 1220 -30 0 0 {name=l17 lab=m1}
C {lab_pin.sym} 1180 0 0 0 {name=l18 lab=A2}
C {lab_pin.sym} 1220 30 0 0 {name=l19 lab=m2}
C {lab_pin.sym} 1220 0 0 0 {name=l20 lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 0 220 0 0 {name=MN3 model=sg13_lv_nmos w=1.5u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 20 190 0 0 {name=l21 lab=m2}
C {lab_pin.sym} -20 220 0 0 {name=l22 lab=A3}
C {lab_pin.sym} 20 250 0 0 {name=l23 lab=VSS}
C {lab_pin.sym} 20 220 0 0 {name=l24 lab=VSS}
C {ipin.sym} -400 -300 0 0 {name=p1 lab=A1}
C {ipin.sym} -400 -260 0 0 {name=p2 lab=A2}
C {ipin.sym} -400 -220 0 0 {name=p3 lab=A3}
C {opin.sym} -400 -180 0 0 {name=p4 lab=Y}
C {iopin.sym} -400 -140 0 0 {name=p5 lab=VDD}
C {iopin.sym} -400 -100 0 0 {name=p6 lab=VSS}
