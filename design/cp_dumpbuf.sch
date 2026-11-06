v {xschem version=3.4.8RC file_version=1.3
cp_dumpbuf -- unity-gain dump buffer: NMOS-input and PMOS-input 5-transistor OTAs in parallel on one output (complementary input range), VDUMP fed back to both inverting inputs (issue #62)
}
G {}
K {}
V {}
S {}
E {}
C {sg13g2_pr/sg13_lv_nmos.sym} 0 0 0 0 {name=MNT model=sg13_lv_nmos w=2u l=0.5u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 20 -30 0 0 {name=l1 lab=tn}
C {lab_pin.sym} -20 0 0 0 {name=l2 lab=IBIAS}
C {lab_pin.sym} 20 30 0 0 {name=l3 lab=VSS}
C {lab_pin.sym} 20 0 0 0 {name=l4 lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 300 0 0 0 {name=MNA model=sg13_lv_nmos w=8u l=0.5u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 320 -30 0 0 {name=l5 lab=da}
C {lab_pin.sym} 280 0 0 0 {name=l6 lab=VOUT}
C {lab_pin.sym} 320 30 0 0 {name=l7 lab=tn}
C {lab_pin.sym} 320 0 0 0 {name=l8 lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 600 0 0 0 {name=MNB model=sg13_lv_nmos w=8u l=0.5u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 620 -30 0 0 {name=l9 lab=VDUMP}
C {lab_pin.sym} 580 0 0 0 {name=l10 lab=VDUMP}
C {lab_pin.sym} 620 30 0 0 {name=l11 lab=tn}
C {lab_pin.sym} 620 0 0 0 {name=l12 lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 900 0 0 0 {name=MPA model=sg13_lv_pmos w=6u l=1u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 920 30 0 0 {name=l13 lab=da}
C {lab_pin.sym} 880 0 0 0 {name=l14 lab=da}
C {lab_pin.sym} 920 -30 0 0 {name=l15 lab=VDD}
C {lab_pin.sym} 920 0 0 0 {name=l16 lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 1200 0 0 0 {name=MPB model=sg13_lv_pmos w=6u l=1u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 1220 30 0 0 {name=l17 lab=VDUMP}
C {lab_pin.sym} 1180 0 0 0 {name=l18 lab=da}
C {lab_pin.sym} 1220 -30 0 0 {name=l19 lab=VDD}
C {lab_pin.sym} 1220 0 0 0 {name=l20 lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 0 220 0 0 {name=MPT model=sg13_lv_pmos w=6u l=0.5u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 20 250 0 0 {name=l21 lab=tp}
C {lab_pin.sym} -20 220 0 0 {name=l22 lab=IBIASP}
C {lab_pin.sym} 20 190 0 0 {name=l23 lab=VDD}
C {lab_pin.sym} 20 220 0 0 {name=l24 lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 300 220 0 0 {name=MQA model=sg13_lv_pmos w=16u l=0.5u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 320 250 0 0 {name=l25 lab=dp}
C {lab_pin.sym} 280 220 0 0 {name=l26 lab=VOUT}
C {lab_pin.sym} 320 190 0 0 {name=l27 lab=tp}
C {lab_pin.sym} 320 220 0 0 {name=l28 lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 600 220 0 0 {name=MQB model=sg13_lv_pmos w=16u l=0.5u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 620 250 0 0 {name=l29 lab=VDUMP}
C {lab_pin.sym} 580 220 0 0 {name=l30 lab=VDUMP}
C {lab_pin.sym} 620 190 0 0 {name=l31 lab=tp}
C {lab_pin.sym} 620 220 0 0 {name=l32 lab=VDD}
C {sg13g2_pr/sg13_lv_nmos.sym} 900 220 0 0 {name=MRA model=sg13_lv_nmos w=2u l=1u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 920 190 0 0 {name=l33 lab=dp}
C {lab_pin.sym} 880 220 0 0 {name=l34 lab=dp}
C {lab_pin.sym} 920 250 0 0 {name=l35 lab=VSS}
C {lab_pin.sym} 920 220 0 0 {name=l36 lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 1200 220 0 0 {name=MRB model=sg13_lv_nmos w=2u l=1u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 1220 190 0 0 {name=l37 lab=VDUMP}
C {lab_pin.sym} 1180 220 0 0 {name=l38 lab=dp}
C {lab_pin.sym} 1220 250 0 0 {name=l39 lab=VSS}
C {lab_pin.sym} 1220 220 0 0 {name=l40 lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 0 440 0 0 {name=MCN model=sg13_lv_nmos w=4u l=4u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 20 410 0 0 {name=l41 lab=VSS}
C {lab_pin.sym} -20 440 0 0 {name=l42 lab=VDUMP}
C {lab_pin.sym} 20 470 0 0 {name=l43 lab=VSS}
C {lab_pin.sym} 20 440 0 0 {name=l44 lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 300 440 0 0 {name=MCP model=sg13_lv_pmos w=4u l=4u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 320 470 0 0 {name=l45 lab=VDD}
C {lab_pin.sym} 280 440 0 0 {name=l46 lab=VDUMP}
C {lab_pin.sym} 320 410 0 0 {name=l47 lab=VDD}
C {lab_pin.sym} 320 440 0 0 {name=l48 lab=VDD}
C {ipin.sym} -400 -300 0 0 {name=p1 lab=VOUT}
C {ipin.sym} -400 -260 0 0 {name=p2 lab=IBIAS}
C {ipin.sym} -400 -220 0 0 {name=p3 lab=IBIASP}
C {opin.sym} -400 -180 0 0 {name=p4 lab=VDUMP}
C {iopin.sym} -400 -140 0 0 {name=p5 lab=VDD}
C {iopin.sym} -400 -100 0 0 {name=p6 lab=VSS}
