v {xschem version=3.4.8RC file_version=1.3
sg13g2-dll :: tap_buffer -- two inverters (non-inverting), isolates the 20 fF tap load from the delay cell
First inverter is small (low load on the delay line); second drives the load.
Identical on every tap including the T0 reference and the last-tap dummy.
}
G {}
K {}
V {}
S {}
E {}
C {sg13g2_pr/sg13_lv_pmos.sym} 0 0 0 0 {name=MP1 model=sg13_lv_pmos w=0.5u l=0.13u ng=1 m=1 spiceprefix=X}
C {sg13g2_pr/sg13_lv_nmos.sym} 0 300 0 0 {name=MN1 model=sg13_lv_nmos w=0.25u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 20 -30 0 0 {name=l1 lab=VDD}
C {lab_pin.sym} -20 0 0 0 {name=l2 lab=IN}
C {lab_pin.sym} 20 0 0 0 {name=l3 lab=VDD}
C {lab_pin.sym} 20 30 0 0 {name=l4 lab=b}
C {lab_pin.sym} 20 270 0 0 {name=l5 lab=b}
C {lab_pin.sym} -20 300 0 0 {name=l6 lab=IN}
C {lab_pin.sym} 20 300 0 0 {name=l7 lab=VSS}
C {lab_pin.sym} 20 330 0 0 {name=l8 lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 500 0 0 0 {name=MP2 model=sg13_lv_pmos w=3u l=0.13u ng=1 m=1 spiceprefix=X}
C {sg13g2_pr/sg13_lv_nmos.sym} 500 300 0 0 {name=MN2 model=sg13_lv_nmos w=1.5u l=0.13u ng=1 m=1 spiceprefix=X}
C {lab_pin.sym} 520 -30 0 0 {name=l9 lab=VDD}
C {lab_pin.sym} 480 0 0 0 {name=l10 lab=b}
C {lab_pin.sym} 520 0 0 0 {name=l11 lab=VDD}
C {lab_pin.sym} 520 30 0 0 {name=l12 lab=OUT}
C {lab_pin.sym} 520 270 0 0 {name=l13 lab=OUT}
C {lab_pin.sym} 480 300 0 0 {name=l14 lab=b}
C {lab_pin.sym} 520 300 0 0 {name=l15 lab=VSS}
C {lab_pin.sym} 520 330 0 0 {name=l16 lab=VSS}
C {ipin.sym} -350 0 0 0 {name=p1 lab=IN}
C {opin.sym} 900 0 0 0 {name=p2 lab=OUT}
C {iopin.sym} -350 -300 0 0 {name=p3 lab=VDD}
C {iopin.sym} -350 600 0 0 {name=p4 lab=VSS}
