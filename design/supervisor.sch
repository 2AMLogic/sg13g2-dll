v {xschem version=3.4.8RC file_version=1.3
supervisor -- false-lock supervisor: reset VCTRL high on EN low / over-delay / rail time-out, mask first REF edge after release
}
G {}
K {}
V {}
S {}
E {}
C {win_det.sym} 0 0 0 0 {name=XWIN}
C {lab_pin.sym} -60 -20 0 0 {name=l1 lab=REF}
C {lab_pin.sym} -60 0 0 0 {name=l2 lab=TAPN}
C {lab_pin.sym} -60 20 0 0 {name=l3 lab=TAPH}
C {lab_pin.sym} 60 0 0 0 {name=l4 lab=over}
C {lab_pin.sym} 0 -50 0 0 {name=l5 lab=VDD}
C {lab_pin.sym} 0 50 0 0 {name=l6 lab=VSS}
C {rail_cmp.sym} 300 0 0 0 {name=XRAIL}
C {lab_pin.sym} 240 0 0 0 {name=l7 lab=VCTRL}
C {lab_pin.sym} 360 -20 0 0 {name=l8 lab=nhi}
C {lab_pin.sym} 360 0 0 0 {name=l9 lab=nlo}
C {lab_pin.sym} 360 20 0 0 {name=l10 lab=near}
C {lab_pin.sym} 300 -50 0 0 {name=l11 lab=VDD}
C {lab_pin.sym} 300 50 0 0 {name=l12 lab=VSS}
C {nand2_lv.sym} 600 0 0 0 {name=XCN}
C {lab_pin.sym} 540 -10 0 0 {name=l13 lab=near}
C {lab_pin.sym} 540 10 0 0 {name=l14 lab=RSTB}
C {lab_pin.sym} 660 0 0 0 {name=l15 lab=cnt_clr_n}
C {lab_pin.sym} 600 -40 0 0 {name=l16 lab=VDD}
C {lab_pin.sym} 600 40 0 0 {name=l17 lab=VSS}
C {inv_lv.sym} 900 0 0 0 {name=XCI}
C {lab_pin.sym} 840 0 0 0 {name=l18 lab=cnt_clr_n}
C {lab_pin.sym} 960 0 0 0 {name=l19 lab=cnt_en}
C {lab_pin.sym} 900 -40 0 0 {name=l20 lab=VDD}
C {lab_pin.sym} 900 40 0 0 {name=l21 lab=VSS}
C {timeout_cnt.sym} 1200 0 0 0 {name=XCNT}
C {lab_pin.sym} 1140 -10 0 0 {name=l22 lab=REF}
C {lab_pin.sym} 1140 10 0 0 {name=l23 lab=cnt_en}
C {lab_pin.sym} 1260 0 0 0 {name=l24 lab=to}
C {lab_pin.sym} 1200 -40 0 0 {name=l25 lab=VDD}
C {lab_pin.sym} 1200 40 0 0 {name=l26 lab=VSS}
C {edgedet.sym} 0 220 0 0 {name=XET}
C {lab_pin.sym} -60 220 0 0 {name=l27 lab=to}
C {lab_pin.sym} 60 220 0 0 {name=l28 lab=pt}
C {lab_pin.sym} 0 180 0 0 {name=l29 lab=VDD}
C {lab_pin.sym} 0 260 0 0 {name=l30 lab=VSS}
C {inv_lv.sym} 300 220 0 0 {name=XIPO}
C {lab_pin.sym} 240 220 0 0 {name=l31 lab=over}
C {lab_pin.sym} 360 220 0 0 {name=l32 lab=over_n}
C {lab_pin.sym} 300 180 0 0 {name=l33 lab=VDD}
C {lab_pin.sym} 300 260 0 0 {name=l34 lab=VSS}
C {inv_lv.sym} 600 220 0 0 {name=XIPT}
C {lab_pin.sym} 540 220 0 0 {name=l35 lab=pt}
C {lab_pin.sym} 660 220 0 0 {name=l36 lab=pt_n}
C {lab_pin.sym} 600 180 0 0 {name=l37 lab=VDD}
C {lab_pin.sym} 600 260 0 0 {name=l38 lab=VSS}
C {nand3_lv.sym} 900 220 0 0 {name=XSET}
C {lab_pin.sym} 840 200 0 0 {name=l39 lab=over_n}
C {lab_pin.sym} 840 220 0 0 {name=l40 lab=pt_n}
C {lab_pin.sym} 840 240 0 0 {name=l41 lab=EN}
C {lab_pin.sym} 960 220 0 0 {name=l42 lab=set}
C {lab_pin.sym} 900 170 0 0 {name=l43 lab=VDD}
C {lab_pin.sym} 900 270 0 0 {name=l44 lab=VSS}
C {inv_lv.sym} 1200 220 0 0 {name=XISB}
C {lab_pin.sym} 1140 220 0 0 {name=l45 lab=set}
C {lab_pin.sym} 1260 220 0 0 {name=l46 lab=set_n}
C {lab_pin.sym} 1200 180 0 0 {name=l47 lab=VDD}
C {lab_pin.sym} 1200 260 0 0 {name=l48 lab=VSS}
C {nand2_lv.sym} 0 440 0 0 {name=XRN}
C {lab_pin.sym} -60 430 0 0 {name=l49 lab=nhi}
C {lab_pin.sym} -60 450 0 0 {name=l50 lab=set_n}
C {lab_pin.sym} 60 440 0 0 {name=l51 lab=clr_n}
C {lab_pin.sym} 0 400 0 0 {name=l52 lab=VDD}
C {lab_pin.sym} 0 480 0 0 {name=l53 lab=VSS}
C {inv_lv.sym} 300 440 0 0 {name=XRI}
C {lab_pin.sym} 240 440 0 0 {name=l54 lab=clr_n}
C {lab_pin.sym} 360 440 0 0 {name=l55 lab=clr}
C {lab_pin.sym} 300 400 0 0 {name=l56 lab=VDD}
C {lab_pin.sym} 300 480 0 0 {name=l57 lab=VSS}
C {srlatch.sym} 600 440 0 0 {name=XLAT}
C {lab_pin.sym} 540 430 0 0 {name=l58 lab=set}
C {lab_pin.sym} 540 450 0 0 {name=l59 lab=clr}
C {lab_pin.sym} 660 430 0 0 {name=l60 lab=RST}
C {lab_pin.sym} 660 450 0 0 {name=l61 lab=RSTB}
C {lab_pin.sym} 600 400 0 0 {name=l62 lab=VDD}
C {lab_pin.sym} 600 480 0 0 {name=l63 lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 900 440 0 0 {name=MRST model=sg13_lv_pmos w=20u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 920 470 0 0 {name=l64 lab=VCTRL}
C {lab_pin.sym} 880 440 0 0 {name=l65 lab=RSTB}
C {lab_pin.sym} 920 410 0 0 {name=l66 lab=VDD}
C {lab_pin.sym} 920 440 0 0 {name=l67 lab=VDD}
C {refmask.sym} 1200 440 0 0 {name=XMSK}
C {lab_pin.sym} 1140 430 0 0 {name=l68 lab=REF}
C {lab_pin.sym} 1140 450 0 0 {name=l69 lab=RSTB}
C {lab_pin.sym} 1260 440 0 0 {name=l70 lab=REFM}
C {lab_pin.sym} 1200 400 0 0 {name=l71 lab=VDD}
C {lab_pin.sym} 1200 480 0 0 {name=l72 lab=VSS}
C {ipin.sym} -400 -300 0 0 {name=p1 lab=REF}
C {ipin.sym} -400 -260 0 0 {name=p2 lab=TAPN}
C {ipin.sym} -400 -220 0 0 {name=p3 lab=TAPH}
C {ipin.sym} -400 -180 0 0 {name=p4 lab=EN}
C {iopin.sym} -400 -140 0 0 {name=p5 lab=VCTRL}
C {opin.sym} -400 -100 0 0 {name=p6 lab=REFM}
C {opin.sym} -400 -60 0 0 {name=p7 lab=RST}
C {iopin.sym} -400 -20 0 0 {name=p8 lab=VDD}
C {iopin.sym} -400 20 0 0 {name=p9 lab=VSS}
