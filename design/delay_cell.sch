v {xschem version=3.4.8RC file_version=1.3
sg13g2-dll :: delay_cell -- two current-starved inverters in series (non-inverting)
One tap step = 2 stages (decision 0004 leaves stages-per-tap to sizing; see
design/NOTES.md). Each stage: PMOS head (gate VBP) + inverter + NMOS tail
(gate VBN). sg13_lv_* devices on the 1.2 V rail (decision 0007). Same family
as sg13g2-pll vco_stage; devices and lengths re-sized, not copied.
Connectivity is label-driven (lab_pin on every device terminal).
}
G {}
K {}
V {}
S {}
E {}
C {sg13g2_pr/sg13_lv_pmos.sym} 0 -300 0 0 {name=MPH1 model=sg13_lv_pmos w=1.5u l=0.13u ng=1 m=1 spiceprefix=X}
C {sg13g2_pr/sg13_lv_pmos.sym} 0 0 0 0 {name=MP1 model=sg13_lv_pmos w=1u l=0.13u ng=1 m=1 spiceprefix=X}
C {sg13g2_pr/sg13_lv_nmos.sym} 0 300 0 0 {name=MN1 model=sg13_lv_nmos w=0.5u l=0.13u ng=1 m=1 spiceprefix=X}
C {sg13g2_pr/sg13_lv_nmos.sym} 0 600 0 0 {name=MNT1 model=sg13_lv_nmos w=0.75u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 20 -330 0 0 {name=l1 lab=VDD}
C {lab_pin.sym} -20 -300 0 0 {name=l2 lab=VBP}
C {lab_pin.sym} 20 -300 0 0 {name=l3 lab=VDD}
C {lab_pin.sym} 20 -270 0 0 {name=l4 lab=nh1}
C {lab_pin.sym} 20 -30 0 0 {name=l5 lab=nh1}
C {lab_pin.sym} -20 0 0 0 {name=l6 lab=IN}
C {lab_pin.sym} 20 0 0 0 {name=l7 lab=VDD}
C {lab_pin.sym} 20 30 0 0 {name=l8 lab=mid}
C {lab_pin.sym} 20 270 0 0 {name=l9 lab=mid}
C {lab_pin.sym} -20 300 0 0 {name=l10 lab=IN}
C {lab_pin.sym} 20 300 0 0 {name=l11 lab=VSS}
C {lab_pin.sym} 20 330 0 0 {name=l12 lab=nt1}
C {lab_pin.sym} 20 570 0 0 {name=l13 lab=nt1}
C {lab_pin.sym} -20 600 0 0 {name=l14 lab=VBN}
C {lab_pin.sym} 20 600 0 0 {name=l15 lab=VSS}
C {lab_pin.sym} 20 630 0 0 {name=l16 lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 700 -300 0 0 {name=MPH2 model=sg13_lv_pmos w=1.5u l=0.13u ng=1 m=1 spiceprefix=X}
C {sg13g2_pr/sg13_lv_pmos.sym} 700 0 0 0 {name=MP2 model=sg13_lv_pmos w=1u l=0.13u ng=1 m=1 spiceprefix=X}
C {sg13g2_pr/sg13_lv_nmos.sym} 700 300 0 0 {name=MN2 model=sg13_lv_nmos w=0.5u l=0.13u ng=1 m=1 spiceprefix=X}
C {sg13g2_pr/sg13_lv_nmos.sym} 700 600 0 0 {name=MNT2 model=sg13_lv_nmos w=0.75u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 720 -330 0 0 {name=l17 lab=VDD}
C {lab_pin.sym} 680 -300 0 0 {name=l18 lab=VBP}
C {lab_pin.sym} 720 -300 0 0 {name=l19 lab=VDD}
C {lab_pin.sym} 720 -270 0 0 {name=l20 lab=nh2}
C {lab_pin.sym} 720 -30 0 0 {name=l21 lab=nh2}
C {lab_pin.sym} 680 0 0 0 {name=l22 lab=mid}
C {lab_pin.sym} 720 0 0 0 {name=l23 lab=VDD}
C {lab_pin.sym} 720 30 0 0 {name=l24 lab=OUT}
C {lab_pin.sym} 720 270 0 0 {name=l25 lab=OUT}
C {lab_pin.sym} 680 300 0 0 {name=l26 lab=mid}
C {lab_pin.sym} 720 300 0 0 {name=l27 lab=VSS}
C {lab_pin.sym} 720 330 0 0 {name=l28 lab=nt2}
C {lab_pin.sym} 720 570 0 0 {name=l29 lab=nt2}
C {lab_pin.sym} 680 600 0 0 {name=l30 lab=VBN}
C {lab_pin.sym} 720 600 0 0 {name=l31 lab=VSS}
C {lab_pin.sym} 720 630 0 0 {name=l32 lab=VSS}
C {ipin.sym} -350 -40 0 0 {name=p1 lab=IN}
C {ipin.sym} -350 0 0 0 {name=p2 lab=VBP}
C {ipin.sym} -350 40 0 0 {name=p3 lab=VBN}
C {opin.sym} 1050 0 0 0 {name=p4 lab=OUT}
C {iopin.sym} -350 -600 0 0 {name=p5 lab=VDD}
C {iopin.sym} -350 900 0 0 {name=p6 lab=VSS}
