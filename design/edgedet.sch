v {xschem version=3.4.8RC file_version=1.3
edgedet -- rising-edge pulse generator: X AND NOT(X delayed by 3 inverters, 0.16u channels for the issue #136 window)
}
G {}
K {}
V {}
S {}
E {}
C {sg13g2_pr/sg13_lv_pmos.sym} 0 0 0 0 {name=MPD1 model=sg13_lv_pmos w=1u l=0.16u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 20 30 0 0 {name=l1 lab=d1}
C {lab_pin.sym} -20 0 0 0 {name=l2 lab=X}
C {lab_pin.sym} 20 -30 0 0 {name=l3 lab=VDD}
C {lab_pin.sym} 20 0 0 0 {name=l4 lab=VDD}
C {sg13g2_pr/sg13_lv_nmos.sym} 300 0 0 0 {name=MND1 model=sg13_lv_nmos w=0.5u l=0.16u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 320 -30 0 0 {name=l5 lab=d1}
C {lab_pin.sym} 280 0 0 0 {name=l6 lab=X}
C {lab_pin.sym} 320 30 0 0 {name=l7 lab=VSS}
C {lab_pin.sym} 320 0 0 0 {name=l8 lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 600 0 0 0 {name=MPD2 model=sg13_lv_pmos w=1u l=0.16u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 620 30 0 0 {name=l9 lab=d2}
C {lab_pin.sym} 580 0 0 0 {name=l10 lab=d1}
C {lab_pin.sym} 620 -30 0 0 {name=l11 lab=VDD}
C {lab_pin.sym} 620 0 0 0 {name=l12 lab=VDD}
C {sg13g2_pr/sg13_lv_nmos.sym} 900 0 0 0 {name=MND2 model=sg13_lv_nmos w=0.5u l=0.16u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 920 -30 0 0 {name=l13 lab=d2}
C {lab_pin.sym} 880 0 0 0 {name=l14 lab=d1}
C {lab_pin.sym} 920 30 0 0 {name=l15 lab=VSS}
C {lab_pin.sym} 920 0 0 0 {name=l16 lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 1200 0 0 0 {name=MPD3 model=sg13_lv_pmos w=1u l=0.16u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 1220 30 0 0 {name=l17 lab=d3}
C {lab_pin.sym} 1180 0 0 0 {name=l18 lab=d2}
C {lab_pin.sym} 1220 -30 0 0 {name=l19 lab=VDD}
C {lab_pin.sym} 1220 0 0 0 {name=l20 lab=VDD}
C {sg13g2_pr/sg13_lv_nmos.sym} 0 220 0 0 {name=MND3 model=sg13_lv_nmos w=0.5u l=0.16u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 20 190 0 0 {name=l21 lab=d3}
C {lab_pin.sym} -20 220 0 0 {name=l22 lab=d2}
C {lab_pin.sym} 20 250 0 0 {name=l23 lab=VSS}
C {lab_pin.sym} 20 220 0 0 {name=l24 lab=VSS}
C {nand2_lv.sym} 300 220 0 0 {name=XN1}
C {lab_pin.sym} 240 210 0 0 {name=l25 lab=X}
C {lab_pin.sym} 240 230 0 0 {name=l26 lab=d3}
C {lab_pin.sym} 360 220 0 0 {name=l27 lab=ntmp}
C {lab_pin.sym} 300 180 0 0 {name=l28 lab=VDD}
C {lab_pin.sym} 300 260 0 0 {name=l29 lab=VSS}
C {inv_lv.sym} 600 220 0 0 {name=XOUT}
C {lab_pin.sym} 540 220 0 0 {name=l30 lab=ntmp}
C {lab_pin.sym} 660 220 0 0 {name=l31 lab=OUT}
C {lab_pin.sym} 600 180 0 0 {name=l32 lab=VDD}
C {lab_pin.sym} 600 260 0 0 {name=l33 lab=VSS}
C {ipin.sym} -400 -300 0 0 {name=p1 lab=X}
C {opin.sym} -400 -260 0 0 {name=p2 lab=OUT}
C {iopin.sym} -400 -220 0 0 {name=p3 lab=VDD}
C {iopin.sym} -400 -180 0 0 {name=p4 lab=VSS}
