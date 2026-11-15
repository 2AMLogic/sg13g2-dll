v {xschem version=3.4.8RC file_version=1.3
srlatch_fast -- set/reset latch, cross-coupled device-level NAND2 (4u) with inverted inputs (S, R active high); PFD-local fast variant of srlatch for the reset loop (issue #113; resized in issue #136: device NANDs, 2x S-inverter, 4x R-inverter)
}
G {}
K {}
V {}
S {}
E {}
C {inv2x_lv.sym} 0 0 0 0 {name=XIS}
C {lab_pin.sym} -60 0 0 0 {name=l1 lab=S}
C {lab_pin.sym} 60 0 0 0 {name=l2 lab=SB}
C {lab_pin.sym} 0 -40 0 0 {name=l3 lab=VDD}
C {lab_pin.sym} 0 40 0 0 {name=l4 lab=VSS}
C {inv4x_lv.sym} 300 0 0 0 {name=XIR}
C {lab_pin.sym} 240 0 0 0 {name=l5 lab=R}
C {lab_pin.sym} 360 0 0 0 {name=l6 lab=RB}
C {lab_pin.sym} 300 -40 0 0 {name=l7 lab=VDD}
C {lab_pin.sym} 300 40 0 0 {name=l8 lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 600 0 0 0 {name=MPQ1 model=sg13_lv_pmos w=4u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 620 30 0 0 {name=l9 lab=Q}
C {lab_pin.sym} 580 0 0 0 {name=l10 lab=SB}
C {lab_pin.sym} 620 -30 0 0 {name=l11 lab=VDD}
C {lab_pin.sym} 620 0 0 0 {name=l12 lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 900 0 0 0 {name=MPQ2 model=sg13_lv_pmos w=4u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 920 30 0 0 {name=l13 lab=Q}
C {lab_pin.sym} 880 0 0 0 {name=l14 lab=QB}
C {lab_pin.sym} 920 -30 0 0 {name=l15 lab=VDD}
C {lab_pin.sym} 920 0 0 0 {name=l16 lab=VDD}
C {sg13g2_pr/sg13_lv_nmos.sym} 1200 0 0 0 {name=MNQ1 model=sg13_lv_nmos w=4u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 1220 -30 0 0 {name=l17 lab=Q}
C {lab_pin.sym} 1180 0 0 0 {name=l18 lab=SB}
C {lab_pin.sym} 1220 30 0 0 {name=l19 lab=midq}
C {lab_pin.sym} 1220 0 0 0 {name=l20 lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 0 220 0 0 {name=MNQ2 model=sg13_lv_nmos w=4u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 20 190 0 0 {name=l21 lab=midq}
C {lab_pin.sym} -20 220 0 0 {name=l22 lab=QB}
C {lab_pin.sym} 20 250 0 0 {name=l23 lab=VSS}
C {lab_pin.sym} 20 220 0 0 {name=l24 lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 300 220 0 0 {name=MPB1 model=sg13_lv_pmos w=4u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 320 250 0 0 {name=l25 lab=QB}
C {lab_pin.sym} 280 220 0 0 {name=l26 lab=RB}
C {lab_pin.sym} 320 190 0 0 {name=l27 lab=VDD}
C {lab_pin.sym} 320 220 0 0 {name=l28 lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 600 220 0 0 {name=MPB2 model=sg13_lv_pmos w=4u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 620 250 0 0 {name=l29 lab=QB}
C {lab_pin.sym} 580 220 0 0 {name=l30 lab=Q}
C {lab_pin.sym} 620 190 0 0 {name=l31 lab=VDD}
C {lab_pin.sym} 620 220 0 0 {name=l32 lab=VDD}
C {sg13g2_pr/sg13_lv_nmos.sym} 900 220 0 0 {name=MNB1 model=sg13_lv_nmos w=4u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 920 190 0 0 {name=l33 lab=QB}
C {lab_pin.sym} 880 220 0 0 {name=l34 lab=RB}
C {lab_pin.sym} 920 250 0 0 {name=l35 lab=midb}
C {lab_pin.sym} 920 220 0 0 {name=l36 lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 1200 220 0 0 {name=MNB2 model=sg13_lv_nmos w=4u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 1220 190 0 0 {name=l37 lab=midb}
C {lab_pin.sym} 1180 220 0 0 {name=l38 lab=Q}
C {lab_pin.sym} 1220 250 0 0 {name=l39 lab=VSS}
C {lab_pin.sym} 1220 220 0 0 {name=l40 lab=VSS}
C {ipin.sym} -400 -300 0 0 {name=p1 lab=S}
C {ipin.sym} -400 -260 0 0 {name=p2 lab=R}
C {opin.sym} -400 -220 0 0 {name=p3 lab=Q}
C {opin.sym} -400 -180 0 0 {name=p4 lab=QB}
C {iopin.sym} -400 -140 0 0 {name=p5 lab=VDD}
C {iopin.sym} -400 -100 0 0 {name=p6 lab=VSS}
