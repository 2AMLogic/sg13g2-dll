v {xschem version=3.4.8RC file_version=1.3
lock_detector -- lock detector: tap-N edge window and VCTRL stillness must hold 128 REF cycles; LOCK drops on the first failing sample
}
G {}
K {}
V {}
S {}
E {}
C {inv_lv.sym} 0 0 0 0 {name=XD1}
C {lab_pin.sym} -60 0 0 0 {name=l1 lab=REF}
C {lab_pin.sym} 60 0 0 0 {name=l2 lab=rd1}
C {lab_pin.sym} 0 -40 0 0 {name=l3 lab=VDD}
C {lab_pin.sym} 0 40 0 0 {name=l4 lab=VSS}
C {inv_lv.sym} 300 0 0 0 {name=XD2}
C {lab_pin.sym} 240 0 0 0 {name=l5 lab=rd1}
C {lab_pin.sym} 360 0 0 0 {name=l6 lab=refd}
C {lab_pin.sym} 300 -40 0 0 {name=l7 lab=VDD}
C {lab_pin.sym} 300 40 0 0 {name=l8 lab=VSS}
C {inv_lv.sym} 600 0 0 0 {name=XT1}
C {lab_pin.sym} 540 0 0 0 {name=l9 lab=TAPN}
C {lab_pin.sym} 660 0 0 0 {name=l10 lab=td1}
C {lab_pin.sym} 600 -40 0 0 {name=l11 lab=VDD}
C {lab_pin.sym} 600 40 0 0 {name=l12 lab=VSS}
C {inv_lv.sym} 900 0 0 0 {name=XT2}
C {lab_pin.sym} 840 0 0 0 {name=l13 lab=td1}
C {lab_pin.sym} 960 0 0 0 {name=l14 lab=td2}
C {lab_pin.sym} 900 -40 0 0 {name=l15 lab=VDD}
C {lab_pin.sym} 900 40 0 0 {name=l16 lab=VSS}
C {inv_lv.sym} 1200 0 0 0 {name=XT3}
C {lab_pin.sym} 1140 0 0 0 {name=l17 lab=td2}
C {lab_pin.sym} 1260 0 0 0 {name=l18 lab=td3}
C {lab_pin.sym} 1200 -40 0 0 {name=l19 lab=VDD}
C {lab_pin.sym} 1200 40 0 0 {name=l20 lab=VSS}
C {inv_lv.sym} 0 220 0 0 {name=XT4}
C {lab_pin.sym} -60 220 0 0 {name=l21 lab=td3}
C {lab_pin.sym} 60 220 0 0 {name=l22 lab=tapd}
C {lab_pin.sym} 0 180 0 0 {name=l23 lab=VDD}
C {lab_pin.sym} 0 260 0 0 {name=l24 lab=VSS}
C {dffr_lv.sym} 300 220 0 0 {name=XS1}
C {lab_pin.sym} 240 200 0 0 {name=l25 lab=TAPN}
C {lab_pin.sym} 240 220 0 0 {name=l26 lab=refd}
C {lab_pin.sym} 240 240 0 0 {name=l27 lab=VDD}
C {lab_pin.sym} 360 210 0 0 {name=l28 lab=s1}
C {lab_pin.sym} 360 230 0 0 {name=l29 lab=s1_n}
C {lab_pin.sym} 300 170 0 0 {name=l30 lab=VDD}
C {lab_pin.sym} 300 270 0 0 {name=l31 lab=VSS}
C {dffr_lv.sym} 600 220 0 0 {name=XS2}
C {lab_pin.sym} 540 200 0 0 {name=l32 lab=tapd}
C {lab_pin.sym} 540 220 0 0 {name=l33 lab=refd}
C {lab_pin.sym} 540 240 0 0 {name=l34 lab=VDD}
C {lab_pin.sym} 660 210 0 0 {name=l35 lab=s2}
C {lab_pin.sym} 660 230 0 0 {name=l36 lab=s2_n}
C {lab_pin.sym} 600 170 0 0 {name=l37 lab=VDD}
C {lab_pin.sym} 600 270 0 0 {name=l38 lab=VSS}
C {vmov_cmp.sym} 900 220 0 0 {name=XMOV}
C {lab_pin.sym} 840 220 0 0 {name=l39 lab=VCTRL}
C {lab_pin.sym} 960 220 0 0 {name=l40 lab=still}
C {lab_pin.sym} 900 180 0 0 {name=l41 lab=VDD}
C {lab_pin.sym} 900 260 0 0 {name=l42 lab=VSS}
C {nand3_lv.sym} 1200 220 0 0 {name=XGN}
C {lab_pin.sym} 1140 200 0 0 {name=l43 lab=s1}
C {lab_pin.sym} 1140 220 0 0 {name=l44 lab=s2_n}
C {lab_pin.sym} 1140 240 0 0 {name=l45 lab=still}
C {lab_pin.sym} 1260 220 0 0 {name=l46 lab=bad}
C {lab_pin.sym} 1200 170 0 0 {name=l47 lab=VDD}
C {lab_pin.sym} 1200 270 0 0 {name=l48 lab=VSS}
C {inv_lv.sym} 0 440 0 0 {name=XGI}
C {lab_pin.sym} -60 440 0 0 {name=l49 lab=bad}
C {lab_pin.sym} 60 440 0 0 {name=l50 lab=good}
C {lab_pin.sym} 0 400 0 0 {name=l51 lab=VDD}
C {lab_pin.sym} 0 480 0 0 {name=l52 lab=VSS}
C {dffr_lv.sym} 300 440 0 0 {name=XC1}
C {lab_pin.sym} 240 420 0 0 {name=l53 lab=qb1}
C {lab_pin.sym} 240 440 0 0 {name=l54 lab=REF}
C {lab_pin.sym} 240 460 0 0 {name=l55 lab=good}
C {lab_pin.sym} 360 430 0 0 {name=l56 lab=q1}
C {lab_pin.sym} 360 450 0 0 {name=l57 lab=qb1}
C {lab_pin.sym} 300 390 0 0 {name=l58 lab=VDD}
C {lab_pin.sym} 300 490 0 0 {name=l59 lab=VSS}
C {dffr_lv.sym} 600 440 0 0 {name=XC2}
C {lab_pin.sym} 540 420 0 0 {name=l60 lab=qb2}
C {lab_pin.sym} 540 440 0 0 {name=l61 lab=qb1}
C {lab_pin.sym} 540 460 0 0 {name=l62 lab=good}
C {lab_pin.sym} 660 430 0 0 {name=l63 lab=q2}
C {lab_pin.sym} 660 450 0 0 {name=l64 lab=qb2}
C {lab_pin.sym} 600 390 0 0 {name=l65 lab=VDD}
C {lab_pin.sym} 600 490 0 0 {name=l66 lab=VSS}
C {dffr_lv.sym} 900 440 0 0 {name=XC3}
C {lab_pin.sym} 840 420 0 0 {name=l67 lab=qb3}
C {lab_pin.sym} 840 440 0 0 {name=l68 lab=qb2}
C {lab_pin.sym} 840 460 0 0 {name=l69 lab=good}
C {lab_pin.sym} 960 430 0 0 {name=l70 lab=q3}
C {lab_pin.sym} 960 450 0 0 {name=l71 lab=qb3}
C {lab_pin.sym} 900 390 0 0 {name=l72 lab=VDD}
C {lab_pin.sym} 900 490 0 0 {name=l73 lab=VSS}
C {dffr_lv.sym} 1200 440 0 0 {name=XC4}
C {lab_pin.sym} 1140 420 0 0 {name=l74 lab=qb4}
C {lab_pin.sym} 1140 440 0 0 {name=l75 lab=qb3}
C {lab_pin.sym} 1140 460 0 0 {name=l76 lab=good}
C {lab_pin.sym} 1260 430 0 0 {name=l77 lab=q4}
C {lab_pin.sym} 1260 450 0 0 {name=l78 lab=qb4}
C {lab_pin.sym} 1200 390 0 0 {name=l79 lab=VDD}
C {lab_pin.sym} 1200 490 0 0 {name=l80 lab=VSS}
C {dffr_lv.sym} 0 660 0 0 {name=XC5}
C {lab_pin.sym} -60 640 0 0 {name=l81 lab=qb5}
C {lab_pin.sym} -60 660 0 0 {name=l82 lab=qb4}
C {lab_pin.sym} -60 680 0 0 {name=l83 lab=good}
C {lab_pin.sym} 60 650 0 0 {name=l84 lab=q5}
C {lab_pin.sym} 60 670 0 0 {name=l85 lab=qb5}
C {lab_pin.sym} 0 610 0 0 {name=l86 lab=VDD}
C {lab_pin.sym} 0 710 0 0 {name=l87 lab=VSS}
C {dffr_lv.sym} 300 660 0 0 {name=XC6}
C {lab_pin.sym} 240 640 0 0 {name=l88 lab=qb6}
C {lab_pin.sym} 240 660 0 0 {name=l89 lab=qb5}
C {lab_pin.sym} 240 680 0 0 {name=l90 lab=good}
C {lab_pin.sym} 360 650 0 0 {name=l91 lab=q6}
C {lab_pin.sym} 360 670 0 0 {name=l92 lab=qb6}
C {lab_pin.sym} 300 610 0 0 {name=l93 lab=VDD}
C {lab_pin.sym} 300 710 0 0 {name=l94 lab=VSS}
C {dffr_lv.sym} 600 660 0 0 {name=XC7}
C {lab_pin.sym} 540 640 0 0 {name=l95 lab=qb7}
C {lab_pin.sym} 540 660 0 0 {name=l96 lab=qb6}
C {lab_pin.sym} 540 680 0 0 {name=l97 lab=good}
C {lab_pin.sym} 660 650 0 0 {name=l98 lab=q7}
C {lab_pin.sym} 660 670 0 0 {name=l99 lab=qb7}
C {lab_pin.sym} 600 610 0 0 {name=l100 lab=VDD}
C {lab_pin.sym} 600 710 0 0 {name=l101 lab=VSS}
C {dffr_lv.sym} 900 660 0 0 {name=XC8}
C {lab_pin.sym} 840 640 0 0 {name=l102 lab=qb8}
C {lab_pin.sym} 840 660 0 0 {name=l103 lab=qb7}
C {lab_pin.sym} 840 680 0 0 {name=l104 lab=good}
C {lab_pin.sym} 960 650 0 0 {name=l105 lab=to}
C {lab_pin.sym} 960 670 0 0 {name=l106 lab=qb8}
C {lab_pin.sym} 900 610 0 0 {name=l107 lab=VDD}
C {lab_pin.sym} 900 710 0 0 {name=l108 lab=VSS}
C {edgedet.sym} 1200 660 0 0 {name=XET}
C {lab_pin.sym} 1140 660 0 0 {name=l109 lab=to}
C {lab_pin.sym} 1260 660 0 0 {name=l110 lab=pt}
C {lab_pin.sym} 1200 620 0 0 {name=l111 lab=VDD}
C {lab_pin.sym} 1200 700 0 0 {name=l112 lab=VSS}
C {srlatch.sym} 0 880 0 0 {name=XLAT}
C {lab_pin.sym} -60 870 0 0 {name=l113 lab=pt}
C {lab_pin.sym} -60 890 0 0 {name=l114 lab=bad}
C {lab_pin.sym} 60 870 0 0 {name=l115 lab=lockq}
C {lab_pin.sym} 60 890 0 0 {name=l116 lab=lockqb}
C {lab_pin.sym} 0 840 0 0 {name=l117 lab=VDD}
C {lab_pin.sym} 0 920 0 0 {name=l118 lab=VSS}
C {inv_lv.sym} 300 880 0 0 {name=XO1}
C {lab_pin.sym} 240 880 0 0 {name=l119 lab=lockq}
C {lab_pin.sym} 360 880 0 0 {name=l120 lab=lockn}
C {lab_pin.sym} 300 840 0 0 {name=l121 lab=VDD}
C {lab_pin.sym} 300 920 0 0 {name=l122 lab=VSS}
C {inv2x_lv.sym} 600 880 0 0 {name=XO2}
C {lab_pin.sym} 540 880 0 0 {name=l123 lab=lockn}
C {lab_pin.sym} 660 880 0 0 {name=l124 lab=LOCK}
C {lab_pin.sym} 600 840 0 0 {name=l125 lab=VDD}
C {lab_pin.sym} 600 920 0 0 {name=l126 lab=VSS}
C {ipin.sym} -400 -300 0 0 {name=p1 lab=REF}
C {ipin.sym} -400 -260 0 0 {name=p2 lab=TAPN}
C {ipin.sym} -400 -220 0 0 {name=p3 lab=VCTRL}
C {opin.sym} -400 -180 0 0 {name=p4 lab=LOCK}
C {iopin.sym} -400 -140 0 0 {name=p5 lab=VDD}
C {iopin.sym} -400 -100 0 0 {name=p6 lab=VSS}
