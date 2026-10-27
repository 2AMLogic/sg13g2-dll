v {xschem version=3.4.8RC file_version=1.3
cp -- cascoded current-steering charge pump (bias pins external, see cp_bias)
}
G {}
K {}
V {}
S {}
E {}
C {inv_lv.sym} 0 0 0 0 {name=XIUP}
C {lab_pin.sym} -60 0 0 0 {name=l1 lab=UP}
C {lab_pin.sym} 60 0 0 0 {name=l2 lab=UPB}
C {lab_pin.sym} 0 -40 0 0 {name=l3 lab=VDD}
C {lab_pin.sym} 0 40 0 0 {name=l4 lab=VSS}
C {inv_lv.sym} 300 0 0 0 {name=XIDN}
C {lab_pin.sym} 240 0 0 0 {name=l5 lab=DN}
C {lab_pin.sym} 360 0 0 0 {name=l6 lab=DNB}
C {lab_pin.sym} 300 -40 0 0 {name=l7 lab=VDD}
C {lab_pin.sym} 300 40 0 0 {name=l8 lab=VSS}
C {cp_leg_p.sym} 600 0 0 0 {name=XLEGP}
C {lab_pin.sym} 540 -30 0 0 {name=l9 lab=IBP}
C {lab_pin.sym} 540 -10 0 0 {name=l10 lab=ICP}
C {lab_pin.sym} 540 10 0 0 {name=l11 lab=UP}
C {lab_pin.sym} 540 30 0 0 {name=l12 lab=UPB}
C {lab_pin.sym} 660 -10 0 0 {name=l13 lab=VOUT}
C {lab_pin.sym} 660 10 0 0 {name=l14 lab=VDUMP}
C {lab_pin.sym} 600 -60 0 0 {name=l15 lab=VDD}
C {cp_leg_n.sym} 900 0 0 0 {name=XLEGN}
C {lab_pin.sym} 840 -30 0 0 {name=l16 lab=IBN}
C {lab_pin.sym} 840 -10 0 0 {name=l17 lab=ICN}
C {lab_pin.sym} 840 10 0 0 {name=l18 lab=DN}
C {lab_pin.sym} 840 30 0 0 {name=l19 lab=DNB}
C {lab_pin.sym} 960 -10 0 0 {name=l20 lab=VOUT}
C {lab_pin.sym} 960 10 0 0 {name=l21 lab=VDUMP}
C {lab_pin.sym} 900 60 0 0 {name=l22 lab=VSS}
C {cp_dumpbuf.sym} 1200 0 0 0 {name=XBUF}
C {lab_pin.sym} 1140 -10 0 0 {name=l23 lab=VOUT}
C {lab_pin.sym} 1140 10 0 0 {name=l24 lab=IBN}
C {lab_pin.sym} 1260 0 0 0 {name=l25 lab=VDUMP}
C {lab_pin.sym} 1200 -40 0 0 {name=l26 lab=VDD}
C {lab_pin.sym} 1200 40 0 0 {name=l27 lab=VSS}
C {ipin.sym} -400 -300 0 0 {name=p1 lab=UP}
C {ipin.sym} -400 -260 0 0 {name=p2 lab=DN}
C {ipin.sym} -400 -220 0 0 {name=p3 lab=IBP}
C {ipin.sym} -400 -180 0 0 {name=p4 lab=ICP}
C {ipin.sym} -400 -140 0 0 {name=p5 lab=IBN}
C {ipin.sym} -400 -100 0 0 {name=p6 lab=ICN}
C {opin.sym} -400 -60 0 0 {name=p7 lab=VOUT}
C {iopin.sym} -400 -20 0 0 {name=p8 lab=VDD}
C {iopin.sym} -400 20 0 0 {name=p9 lab=VSS}
