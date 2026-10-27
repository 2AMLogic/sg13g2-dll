v {xschem version=3.4.8RC file_version=1.3
cp_bias -- charge-pump bias: one long-channel PMOS sets Iref, diode stacks give mirror and cascode gates
}
G {}
K {}
V {}
S {}
E {}
C {sg13g2_pr/sg13_lv_pmos.sym} 0 0 0 0 {name=MR model=sg13_lv_pmos w=0.5u l=4u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 20 30 0 0 {name=l1 lab=ICN}
C {lab_pin.sym} -20 0 0 0 {name=l2 lab=VSS}
C {lab_pin.sym} 20 -30 0 0 {name=l3 lab=VDD}
C {lab_pin.sym} 20 0 0 0 {name=l4 lab=VDD}
C {sg13g2_pr/sg13_lv_nmos.sym} 300 0 0 0 {name=MN3 model=sg13_lv_nmos w=2u l=0.5u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 320 -30 0 0 {name=l5 lab=ICN}
C {lab_pin.sym} 280 0 0 0 {name=l6 lab=ICN}
C {lab_pin.sym} 320 30 0 0 {name=l7 lab=IBN}
C {lab_pin.sym} 320 0 0 0 {name=l8 lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 600 0 0 0 {name=MN0 model=sg13_lv_nmos w=2u l=0.5u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 620 -30 0 0 {name=l9 lab=IBN}
C {lab_pin.sym} 580 0 0 0 {name=l10 lab=IBN}
C {lab_pin.sym} 620 30 0 0 {name=l11 lab=VSS}
C {lab_pin.sym} 620 0 0 0 {name=l12 lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 900 0 0 0 {name=MP0 model=sg13_lv_pmos w=6u l=0.5u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 920 30 0 0 {name=l13 lab=IBP}
C {lab_pin.sym} 880 0 0 0 {name=l14 lab=IBP}
C {lab_pin.sym} 920 -30 0 0 {name=l15 lab=VDD}
C {lab_pin.sym} 920 0 0 0 {name=l16 lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 1200 0 0 0 {name=MP3 model=sg13_lv_pmos w=6u l=0.5u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 1220 30 0 0 {name=l17 lab=ICP}
C {lab_pin.sym} 1180 0 0 0 {name=l18 lab=ICP}
C {lab_pin.sym} 1220 -30 0 0 {name=l19 lab=IBP}
C {lab_pin.sym} 1220 0 0 0 {name=l20 lab=VDD}
C {sg13g2_pr/sg13_lv_nmos.sym} 0 220 0 0 {name=MN4 model=sg13_lv_nmos w=2u l=0.5u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 20 190 0 0 {name=l21 lab=ICP}
C {lab_pin.sym} -20 220 0 0 {name=l22 lab=IBN}
C {lab_pin.sym} 20 250 0 0 {name=l23 lab=VSS}
C {lab_pin.sym} 20 220 0 0 {name=l24 lab=VSS}
C {opin.sym} -400 -300 0 0 {name=p1 lab=IBP}
C {opin.sym} -400 -260 0 0 {name=p2 lab=ICP}
C {opin.sym} -400 -220 0 0 {name=p3 lab=IBN}
C {opin.sym} -400 -180 0 0 {name=p4 lab=ICN}
C {iopin.sym} -400 -140 0 0 {name=p5 lab=VDD}
C {iopin.sym} -400 -100 0 0 {name=p6 lab=VSS}
