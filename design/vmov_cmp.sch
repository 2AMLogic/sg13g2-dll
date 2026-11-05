v {xschem version=3.4.8RC file_version=1.3
vmov_cmp -- VCTRL movement sensor: STILL = 1 while |VCTRL - lowpass(VCTRL)| is below the offset-set threshold
}
G {}
K {}
V {}
S {}
E {}
C {sg13g2_pr/sg13_lv_nmos.sym} 0 0 0 0 {name=MFA model=sg13_lv_nmos w=2u l=1u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 20 -30 0 0 {name=l1 lab=VDD}
C {lab_pin.sym} -20 0 0 0 {name=l2 lab=VCTRL}
C {lab_pin.sym} 20 30 0 0 {name=l3 lab=vsa}
C {lab_pin.sym} 20 0 0 0 {name=l4 lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 300 0 0 0 {name=MSA model=sg13_lv_nmos w=0.5u l=1u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 320 -30 0 0 {name=l5 lab=vsa}
C {lab_pin.sym} 280 0 0 0 {name=l6 lab=VDD}
C {lab_pin.sym} 320 30 0 0 {name=l7 lab=VSS}
C {lab_pin.sym} 320 0 0 0 {name=l8 lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 600 0 0 0 {name=MFB model=sg13_lv_nmos w=2u l=1u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 620 -30 0 0 {name=l9 lab=VDD}
C {lab_pin.sym} 580 0 0 0 {name=l10 lab=VCTRL}
C {lab_pin.sym} 620 30 0 0 {name=l11 lab=vsb0}
C {lab_pin.sym} 620 0 0 0 {name=l12 lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 900 0 0 0 {name=MSB model=sg13_lv_nmos w=0.5u l=1u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 920 -30 0 0 {name=l13 lab=vsb0}
C {lab_pin.sym} 880 0 0 0 {name=l14 lab=VDD}
C {lab_pin.sym} 920 30 0 0 {name=l15 lab=VSS}
C {lab_pin.sym} 920 0 0 0 {name=l16 lab=VSS}
C {sg13g2_pr/rppd.sym} 1200 0 0 0 {name=RL1 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 1200 -30 0 0 {name=l17 lab=vsb0}
C {lab_pin.sym} 1200 30 0 0 {name=l18 lab=lp1}
C {sg13g2_pr/rppd.sym} 0 220 0 0 {name=RL2 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 0 190 0 0 {name=l19 lab=lp1}
C {lab_pin.sym} 0 250 0 0 {name=l20 lab=lp2}
C {sg13g2_pr/rppd.sym} 300 220 0 0 {name=RL3 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 300 190 0 0 {name=l21 lab=lp2}
C {lab_pin.sym} 300 250 0 0 {name=l22 lab=lp3}
C {sg13g2_pr/rppd.sym} 600 220 0 0 {name=RL4 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 600 190 0 0 {name=l23 lab=lp3}
C {lab_pin.sym} 600 250 0 0 {name=l24 lab=lp4}
C {sg13g2_pr/rppd.sym} 900 220 0 0 {name=RL5 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 900 190 0 0 {name=l25 lab=lp4}
C {lab_pin.sym} 900 250 0 0 {name=l26 lab=vsb}
C {sg13g2_pr/cap_cmim.sym} 1200 220 0 0 {name=CL model=cap_cmim w=20u l=20u m=1 spiceprefix=X}
C {lab_pin.sym} 1200 190 0 0 {name=l27 lab=vsb}
C {lab_pin.sym} 1200 250 0 0 {name=l28 lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 0 440 0 0 {name=MTA model=sg13_lv_pmos w=1.5u l=1u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 20 470 0 0 {name=l29 lab=tla}
C {lab_pin.sym} -20 440 0 0 {name=l30 lab=VSS}
C {lab_pin.sym} 20 410 0 0 {name=l31 lab=VDD}
C {lab_pin.sym} 20 440 0 0 {name=l32 lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 300 440 0 0 {name=MA1 model=sg13_lv_pmos w=3.59u l=1u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 320 470 0 0 {name=l33 lab=da}
C {lab_pin.sym} 280 440 0 0 {name=l34 lab=vsb}
C {lab_pin.sym} 320 410 0 0 {name=l35 lab=tla}
C {lab_pin.sym} 320 440 0 0 {name=l36 lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 600 440 0 0 {name=MA2 model=sg13_lv_pmos w=4u l=1u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 620 470 0 0 {name=l37 lab=oa}
C {lab_pin.sym} 580 440 0 0 {name=l38 lab=vsa}
C {lab_pin.sym} 620 410 0 0 {name=l39 lab=tla}
C {lab_pin.sym} 620 440 0 0 {name=l40 lab=VDD}
C {sg13g2_pr/sg13_lv_nmos.sym} 900 440 0 0 {name=MLA1 model=sg13_lv_nmos w=1u l=0.5u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 920 410 0 0 {name=l41 lab=da}
C {lab_pin.sym} 880 440 0 0 {name=l42 lab=da}
C {lab_pin.sym} 920 470 0 0 {name=l43 lab=VSS}
C {lab_pin.sym} 920 440 0 0 {name=l44 lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 1200 440 0 0 {name=MLA2 model=sg13_lv_nmos w=1u l=0.5u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 1220 410 0 0 {name=l45 lab=oa}
C {lab_pin.sym} 1180 440 0 0 {name=l46 lab=da}
C {lab_pin.sym} 1220 470 0 0 {name=l47 lab=VSS}
C {lab_pin.sym} 1220 440 0 0 {name=l48 lab=VSS}
C {inv_lv.sym} 0 660 0 0 {name=XA1}
C {lab_pin.sym} -60 660 0 0 {name=l49 lab=oa}
C {lab_pin.sym} 60 660 0 0 {name=l50 lab=oab}
C {lab_pin.sym} 0 620 0 0 {name=l51 lab=VDD}
C {lab_pin.sym} 0 700 0 0 {name=l52 lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 300 660 0 0 {name=MTB model=sg13_lv_pmos w=1.5u l=1u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 320 690 0 0 {name=l53 lab=tlb}
C {lab_pin.sym} 280 660 0 0 {name=l54 lab=VSS}
C {lab_pin.sym} 320 630 0 0 {name=l55 lab=VDD}
C {lab_pin.sym} 320 660 0 0 {name=l56 lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 600 660 0 0 {name=MB1 model=sg13_lv_pmos w=3.59u l=1u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 620 690 0 0 {name=l57 lab=db}
C {lab_pin.sym} 580 660 0 0 {name=l58 lab=vsa}
C {lab_pin.sym} 620 630 0 0 {name=l59 lab=tlb}
C {lab_pin.sym} 620 660 0 0 {name=l60 lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 900 660 0 0 {name=MB2 model=sg13_lv_pmos w=4u l=1u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 920 690 0 0 {name=l61 lab=ob}
C {lab_pin.sym} 880 660 0 0 {name=l62 lab=vsb}
C {lab_pin.sym} 920 630 0 0 {name=l63 lab=tlb}
C {lab_pin.sym} 920 660 0 0 {name=l64 lab=VDD}
C {sg13g2_pr/sg13_lv_nmos.sym} 1200 660 0 0 {name=MLB1 model=sg13_lv_nmos w=1u l=0.5u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 1220 630 0 0 {name=l65 lab=db}
C {lab_pin.sym} 1180 660 0 0 {name=l66 lab=db}
C {lab_pin.sym} 1220 690 0 0 {name=l67 lab=VSS}
C {lab_pin.sym} 1220 660 0 0 {name=l68 lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 0 880 0 0 {name=MLB2 model=sg13_lv_nmos w=1u l=0.5u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 20 850 0 0 {name=l69 lab=ob}
C {lab_pin.sym} -20 880 0 0 {name=l70 lab=db}
C {lab_pin.sym} 20 910 0 0 {name=l71 lab=VSS}
C {lab_pin.sym} 20 880 0 0 {name=l72 lab=VSS}
C {inv_lv.sym} 300 880 0 0 {name=XB1}
C {lab_pin.sym} 240 880 0 0 {name=l73 lab=ob}
C {lab_pin.sym} 360 880 0 0 {name=l74 lab=obb}
C {lab_pin.sym} 300 840 0 0 {name=l75 lab=VDD}
C {lab_pin.sym} 300 920 0 0 {name=l76 lab=VSS}
C {nand2_lv.sym} 600 880 0 0 {name=XSN}
C {lab_pin.sym} 540 870 0 0 {name=l77 lab=oab}
C {lab_pin.sym} 540 890 0 0 {name=l78 lab=obb}
C {lab_pin.sym} 660 880 0 0 {name=l79 lab=still_n}
C {lab_pin.sym} 600 840 0 0 {name=l80 lab=VDD}
C {lab_pin.sym} 600 920 0 0 {name=l81 lab=VSS}
C {inv_lv.sym} 900 880 0 0 {name=XSI}
C {lab_pin.sym} 840 880 0 0 {name=l82 lab=still_n}
C {lab_pin.sym} 960 880 0 0 {name=l83 lab=STILL}
C {lab_pin.sym} 900 840 0 0 {name=l84 lab=VDD}
C {lab_pin.sym} 900 920 0 0 {name=l85 lab=VSS}
C {ipin.sym} -400 -300 0 0 {name=p1 lab=VCTRL}
C {opin.sym} -400 -260 0 0 {name=p2 lab=STILL}
C {iopin.sym} -400 -220 0 0 {name=p3 lab=VDD}
C {iopin.sym} -400 -180 0 0 {name=p4 lab=VSS}
