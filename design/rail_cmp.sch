v {xschem version=3.4.8RC file_version=1.3
rail_cmp -- VCTRL within ~50 mV of VDD (NHI) or VSS (NLO); NEAR = NHI or NLO
}
G {}
K {}
V {}
S {}
E {}
C {sg13g2_pr/rppd.sym} 0 0 0 0 {name=RA model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 0 -30 0 0 {name=l1 lab=VDD}
C {lab_pin.sym} 0 30 0 0 {name=l2 lab=refh}
C {sg13g2_pr/rppd.sym} 300 0 0 0 {name=RB1 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 300 -30 0 0 {name=l3 lab=refh}
C {lab_pin.sym} 300 30 0 0 {name=l4 lab=lad1}
C {sg13g2_pr/rppd.sym} 600 0 0 0 {name=RB2 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 600 -30 0 0 {name=l5 lab=lad1}
C {lab_pin.sym} 600 30 0 0 {name=l6 lab=lad2}
C {sg13g2_pr/rppd.sym} 900 0 0 0 {name=RB3 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 900 -30 0 0 {name=l7 lab=lad2}
C {lab_pin.sym} 900 30 0 0 {name=l8 lab=lad3}
C {sg13g2_pr/rppd.sym} 1200 0 0 0 {name=RB4 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 1200 -30 0 0 {name=l9 lab=lad3}
C {lab_pin.sym} 1200 30 0 0 {name=l10 lab=lad4}
C {sg13g2_pr/rppd.sym} 0 220 0 0 {name=RB5 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 0 190 0 0 {name=l11 lab=lad4}
C {lab_pin.sym} 0 250 0 0 {name=l12 lab=lad5}
C {sg13g2_pr/rppd.sym} 300 220 0 0 {name=RB6 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 300 190 0 0 {name=l13 lab=lad5}
C {lab_pin.sym} 300 250 0 0 {name=l14 lab=lad6}
C {sg13g2_pr/rppd.sym} 600 220 0 0 {name=RB7 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 600 190 0 0 {name=l15 lab=lad6}
C {lab_pin.sym} 600 250 0 0 {name=l16 lab=lad7}
C {sg13g2_pr/rppd.sym} 900 220 0 0 {name=RB8 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 900 190 0 0 {name=l17 lab=lad7}
C {lab_pin.sym} 900 250 0 0 {name=l18 lab=lad8}
C {sg13g2_pr/rppd.sym} 1200 220 0 0 {name=RB9 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 1200 190 0 0 {name=l19 lab=lad8}
C {lab_pin.sym} 1200 250 0 0 {name=l20 lab=lad9}
C {sg13g2_pr/rppd.sym} 0 440 0 0 {name=RB10 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 0 410 0 0 {name=l21 lab=lad9}
C {lab_pin.sym} 0 470 0 0 {name=l22 lab=lad10}
C {sg13g2_pr/rppd.sym} 300 440 0 0 {name=RB11 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 300 410 0 0 {name=l23 lab=lad10}
C {lab_pin.sym} 300 470 0 0 {name=l24 lab=lad11}
C {sg13g2_pr/rppd.sym} 600 440 0 0 {name=RB12 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 600 410 0 0 {name=l25 lab=lad11}
C {lab_pin.sym} 600 470 0 0 {name=l26 lab=lad12}
C {sg13g2_pr/rppd.sym} 900 440 0 0 {name=RB13 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 900 410 0 0 {name=l27 lab=lad12}
C {lab_pin.sym} 900 470 0 0 {name=l28 lab=lad13}
C {sg13g2_pr/rppd.sym} 1200 440 0 0 {name=RB14 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 1200 410 0 0 {name=l29 lab=lad13}
C {lab_pin.sym} 1200 470 0 0 {name=l30 lab=lad14}
C {sg13g2_pr/rppd.sym} 0 660 0 0 {name=RB15 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 0 630 0 0 {name=l31 lab=lad14}
C {lab_pin.sym} 0 690 0 0 {name=l32 lab=lad15}
C {sg13g2_pr/rppd.sym} 300 660 0 0 {name=RB16 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 300 630 0 0 {name=l33 lab=lad15}
C {lab_pin.sym} 300 690 0 0 {name=l34 lab=lad16}
C {sg13g2_pr/rppd.sym} 600 660 0 0 {name=RB17 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 600 630 0 0 {name=l35 lab=lad16}
C {lab_pin.sym} 600 690 0 0 {name=l36 lab=lad17}
C {sg13g2_pr/rppd.sym} 900 660 0 0 {name=RB18 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 900 630 0 0 {name=l37 lab=lad17}
C {lab_pin.sym} 900 690 0 0 {name=l38 lab=lad18}
C {sg13g2_pr/rppd.sym} 1200 660 0 0 {name=RB19 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 1200 630 0 0 {name=l39 lab=lad18}
C {lab_pin.sym} 1200 690 0 0 {name=l40 lab=lad19}
C {sg13g2_pr/rppd.sym} 0 880 0 0 {name=RB20 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 0 850 0 0 {name=l41 lab=lad19}
C {lab_pin.sym} 0 910 0 0 {name=l42 lab=lad20}
C {sg13g2_pr/rppd.sym} 300 880 0 0 {name=RB21 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 300 850 0 0 {name=l43 lab=lad20}
C {lab_pin.sym} 300 910 0 0 {name=l44 lab=lad21}
C {sg13g2_pr/rppd.sym} 600 880 0 0 {name=RB22 model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 600 850 0 0 {name=l45 lab=lad21}
C {lab_pin.sym} 600 910 0 0 {name=l46 lab=refl}
C {sg13g2_pr/rppd.sym} 900 880 0 0 {name=RC model=rppd w=0.5u l=8u body=VSS b=0 m=1 spiceprefix=X}
C {lab_pin.sym} 900 850 0 0 {name=l47 lab=refl}
C {lab_pin.sym} 900 910 0 0 {name=l48 lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 1200 880 0 0 {name=MFH1 model=sg13_lv_nmos w=2u l=1u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 1220 850 0 0 {name=l49 lab=VDD}
C {lab_pin.sym} 1180 880 0 0 {name=l50 lab=VCTRL}
C {lab_pin.sym} 1220 910 0 0 {name=l51 lab=vsh}
C {lab_pin.sym} 1220 880 0 0 {name=l52 lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 0 1100 0 0 {name=MFH2 model=sg13_lv_nmos w=2u l=1u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 20 1070 0 0 {name=l53 lab=VDD}
C {lab_pin.sym} -20 1100 0 0 {name=l54 lab=refh}
C {lab_pin.sym} 20 1130 0 0 {name=l55 lab=rsh}
C {lab_pin.sym} 20 1100 0 0 {name=l56 lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 300 1100 0 0 {name=MSH1 model=sg13_lv_nmos w=0.5u l=1u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 320 1070 0 0 {name=l57 lab=vsh}
C {lab_pin.sym} 280 1100 0 0 {name=l58 lab=VDD}
C {lab_pin.sym} 320 1130 0 0 {name=l59 lab=VSS}
C {lab_pin.sym} 320 1100 0 0 {name=l60 lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 600 1100 0 0 {name=MSH2 model=sg13_lv_nmos w=0.5u l=1u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 620 1070 0 0 {name=l61 lab=rsh}
C {lab_pin.sym} 580 1100 0 0 {name=l62 lab=VDD}
C {lab_pin.sym} 620 1130 0 0 {name=l63 lab=VSS}
C {lab_pin.sym} 620 1100 0 0 {name=l64 lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 900 1100 0 0 {name=MTH model=sg13_lv_nmos w=0.5u l=1u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 920 1070 0 0 {name=l65 lab=tlh}
C {lab_pin.sym} 880 1100 0 0 {name=l66 lab=VDD}
C {lab_pin.sym} 920 1130 0 0 {name=l67 lab=VSS}
C {lab_pin.sym} 920 1100 0 0 {name=l68 lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 1200 1100 0 0 {name=MH1 model=sg13_lv_nmos w=4u l=1u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 1220 1070 0 0 {name=l69 lab=dh}
C {lab_pin.sym} 1180 1100 0 0 {name=l70 lab=vsh}
C {lab_pin.sym} 1220 1130 0 0 {name=l71 lab=tlh}
C {lab_pin.sym} 1220 1100 0 0 {name=l72 lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 0 1320 0 0 {name=MH2 model=sg13_lv_nmos w=4u l=1u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 20 1290 0 0 {name=l73 lab=oh}
C {lab_pin.sym} -20 1320 0 0 {name=l74 lab=rsh}
C {lab_pin.sym} 20 1350 0 0 {name=l75 lab=tlh}
C {lab_pin.sym} 20 1320 0 0 {name=l76 lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 300 1320 0 0 {name=MLH1 model=sg13_lv_pmos w=2u l=1u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 320 1350 0 0 {name=l77 lab=dh}
C {lab_pin.sym} 280 1320 0 0 {name=l78 lab=dh}
C {lab_pin.sym} 320 1290 0 0 {name=l79 lab=VDD}
C {lab_pin.sym} 320 1320 0 0 {name=l80 lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 600 1320 0 0 {name=MLH2 model=sg13_lv_pmos w=2u l=1u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 620 1350 0 0 {name=l81 lab=oh}
C {lab_pin.sym} 580 1320 0 0 {name=l82 lab=dh}
C {lab_pin.sym} 620 1290 0 0 {name=l83 lab=VDD}
C {lab_pin.sym} 620 1320 0 0 {name=l84 lab=VDD}
C {inv_lv.sym} 900 1320 0 0 {name=XH1}
C {lab_pin.sym} 840 1320 0 0 {name=l85 lab=oh}
C {lab_pin.sym} 960 1320 0 0 {name=l86 lab=ohb}
C {lab_pin.sym} 900 1280 0 0 {name=l87 lab=VDD}
C {lab_pin.sym} 900 1360 0 0 {name=l88 lab=VSS}
C {inv_lv.sym} 1200 1320 0 0 {name=XH2}
C {lab_pin.sym} 1140 1320 0 0 {name=l89 lab=ohb}
C {lab_pin.sym} 1260 1320 0 0 {name=l90 lab=NHI}
C {lab_pin.sym} 1200 1280 0 0 {name=l91 lab=VDD}
C {lab_pin.sym} 1200 1360 0 0 {name=l92 lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 0 1540 0 0 {name=MFL1 model=sg13_lv_pmos w=8u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 20 1570 0 0 {name=l93 lab=VSS}
C {lab_pin.sym} -20 1540 0 0 {name=l94 lab=VCTRL}
C {lab_pin.sym} 20 1510 0 0 {name=l95 lab=vsl}
C {lab_pin.sym} 20 1540 0 0 {name=l96 lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 300 1540 0 0 {name=MFL2 model=sg13_lv_pmos w=8u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 320 1570 0 0 {name=l97 lab=VSS}
C {lab_pin.sym} 280 1540 0 0 {name=l98 lab=refl}
C {lab_pin.sym} 320 1510 0 0 {name=l99 lab=rsl}
C {lab_pin.sym} 320 1540 0 0 {name=l100 lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 600 1540 0 0 {name=MSL1 model=sg13_lv_pmos w=1.5u l=1u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 620 1570 0 0 {name=l101 lab=vsl}
C {lab_pin.sym} 580 1540 0 0 {name=l102 lab=VSS}
C {lab_pin.sym} 620 1510 0 0 {name=l103 lab=VDD}
C {lab_pin.sym} 620 1540 0 0 {name=l104 lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 900 1540 0 0 {name=MSL2 model=sg13_lv_pmos w=1.5u l=1u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 920 1570 0 0 {name=l105 lab=rsl}
C {lab_pin.sym} 880 1540 0 0 {name=l106 lab=VSS}
C {lab_pin.sym} 920 1510 0 0 {name=l107 lab=VDD}
C {lab_pin.sym} 920 1540 0 0 {name=l108 lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 1200 1540 0 0 {name=MTL model=sg13_lv_pmos w=1.5u l=1u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 1220 1570 0 0 {name=l109 lab=tll}
C {lab_pin.sym} 1180 1540 0 0 {name=l110 lab=VSS}
C {lab_pin.sym} 1220 1510 0 0 {name=l111 lab=VDD}
C {lab_pin.sym} 1220 1540 0 0 {name=l112 lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 0 1760 0 0 {name=MPL1 model=sg13_lv_pmos w=4u l=0.5u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 20 1790 0 0 {name=l113 lab=dl}
C {lab_pin.sym} -20 1760 0 0 {name=l114 lab=rsl}
C {lab_pin.sym} 20 1730 0 0 {name=l115 lab=tll}
C {lab_pin.sym} 20 1760 0 0 {name=l116 lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 300 1760 0 0 {name=MPL2 model=sg13_lv_pmos w=4u l=0.5u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 320 1790 0 0 {name=l117 lab=ol}
C {lab_pin.sym} 280 1760 0 0 {name=l118 lab=vsl}
C {lab_pin.sym} 320 1730 0 0 {name=l119 lab=tll}
C {lab_pin.sym} 320 1760 0 0 {name=l120 lab=VDD}
C {sg13g2_pr/sg13_lv_nmos.sym} 600 1760 0 0 {name=MLL1 model=sg13_lv_nmos w=1u l=0.5u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 620 1730 0 0 {name=l121 lab=dl}
C {lab_pin.sym} 580 1760 0 0 {name=l122 lab=dl}
C {lab_pin.sym} 620 1790 0 0 {name=l123 lab=VSS}
C {lab_pin.sym} 620 1760 0 0 {name=l124 lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 900 1760 0 0 {name=MLL2 model=sg13_lv_nmos w=1u l=0.5u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 920 1730 0 0 {name=l125 lab=ol}
C {lab_pin.sym} 880 1760 0 0 {name=l126 lab=dl}
C {lab_pin.sym} 920 1790 0 0 {name=l127 lab=VSS}
C {lab_pin.sym} 920 1760 0 0 {name=l128 lab=VSS}
C {inv_lv.sym} 1200 1760 0 0 {name=XL1}
C {lab_pin.sym} 1140 1760 0 0 {name=l129 lab=ol}
C {lab_pin.sym} 1260 1760 0 0 {name=l130 lab=olb}
C {lab_pin.sym} 1200 1720 0 0 {name=l131 lab=VDD}
C {lab_pin.sym} 1200 1800 0 0 {name=l132 lab=VSS}
C {inv_lv.sym} 0 1980 0 0 {name=XL2}
C {lab_pin.sym} -60 1980 0 0 {name=l133 lab=olb}
C {lab_pin.sym} 60 1980 0 0 {name=l134 lab=NLO}
C {lab_pin.sym} 0 1940 0 0 {name=l135 lab=VDD}
C {lab_pin.sym} 0 2020 0 0 {name=l136 lab=VSS}
C {inv_lv.sym} 300 1980 0 0 {name=XNH}
C {lab_pin.sym} 240 1980 0 0 {name=l137 lab=NHI}
C {lab_pin.sym} 360 1980 0 0 {name=l138 lab=nhi_n}
C {lab_pin.sym} 300 1940 0 0 {name=l139 lab=VDD}
C {lab_pin.sym} 300 2020 0 0 {name=l140 lab=VSS}
C {inv_lv.sym} 600 1980 0 0 {name=XNL}
C {lab_pin.sym} 540 1980 0 0 {name=l141 lab=NLO}
C {lab_pin.sym} 660 1980 0 0 {name=l142 lab=nlo_n}
C {lab_pin.sym} 600 1940 0 0 {name=l143 lab=VDD}
C {lab_pin.sym} 600 2020 0 0 {name=l144 lab=VSS}
C {nand2_lv.sym} 900 1980 0 0 {name=XNE}
C {lab_pin.sym} 840 1970 0 0 {name=l145 lab=nhi_n}
C {lab_pin.sym} 840 1990 0 0 {name=l146 lab=nlo_n}
C {lab_pin.sym} 960 1980 0 0 {name=l147 lab=NEAR}
C {lab_pin.sym} 900 1940 0 0 {name=l148 lab=VDD}
C {lab_pin.sym} 900 2020 0 0 {name=l149 lab=VSS}
C {ipin.sym} -400 -300 0 0 {name=p1 lab=VCTRL}
C {opin.sym} -400 -260 0 0 {name=p2 lab=NHI}
C {opin.sym} -400 -220 0 0 {name=p3 lab=NLO}
C {opin.sym} -400 -180 0 0 {name=p4 lab=NEAR}
C {iopin.sym} -400 -140 0 0 {name=p5 lab=VDD}
C {iopin.sym} -400 -100 0 0 {name=p6 lab=VSS}
