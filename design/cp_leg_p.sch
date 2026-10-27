v {xschem version=3.4.8RC file_version=1.3
cp_leg_p -- PMOS current-steering leg: mirror + cascode, switch to VOUT (UPB low) or VDUMP
}
G {}
K {}
V {}
S {}
E {}
C {sg13g2_pr/sg13_lv_pmos.sym} 0 0 0 0 {name=M1 model=sg13_lv_pmos w=6u l=0.5u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 20 30 0 0 {name=l1 lab=tail}
C {lab_pin.sym} -20 0 0 0 {name=l2 lab=IBP}
C {lab_pin.sym} 20 -30 0 0 {name=l3 lab=VDD}
C {lab_pin.sym} 20 0 0 0 {name=l4 lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 300 0 0 0 {name=M2 model=sg13_lv_pmos w=6u l=0.5u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 320 30 0 0 {name=l5 lab=sw}
C {lab_pin.sym} 280 0 0 0 {name=l6 lab=ICP}
C {lab_pin.sym} 320 -30 0 0 {name=l7 lab=tail}
C {lab_pin.sym} 320 0 0 0 {name=l8 lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 600 0 0 0 {name=XSWO model=sg13_lv_pmos w=3u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 620 30 0 0 {name=l9 lab=VOUT}
C {lab_pin.sym} 580 0 0 0 {name=l10 lab=UPB}
C {lab_pin.sym} 620 -30 0 0 {name=l11 lab=sw}
C {lab_pin.sym} 620 0 0 0 {name=l12 lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 900 0 0 0 {name=XSWD model=sg13_lv_pmos w=3u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 920 30 0 0 {name=l13 lab=VDUMP}
C {lab_pin.sym} 880 0 0 0 {name=l14 lab=UP}
C {lab_pin.sym} 920 -30 0 0 {name=l15 lab=sw}
C {lab_pin.sym} 920 0 0 0 {name=l16 lab=VDD}
C {ipin.sym} -400 -300 0 0 {name=p1 lab=IBP}
C {ipin.sym} -400 -260 0 0 {name=p2 lab=ICP}
C {ipin.sym} -400 -220 0 0 {name=p3 lab=UP}
C {ipin.sym} -400 -180 0 0 {name=p4 lab=UPB}
C {opin.sym} -400 -140 0 0 {name=p5 lab=VOUT}
C {opin.sym} -400 -100 0 0 {name=p6 lab=VDUMP}
C {iopin.sym} -400 -60 0 0 {name=p7 lab=VDD}
