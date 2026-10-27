v {xschem version=3.4.8RC file_version=1.3
loop_filter -- first-order loop filter: one MIM capacitor from VCTRL to VSS (decision 0006)
}
G {}
K {}
V {}
S {}
E {}
C {sg13g2_pr/cap_cmim.sym} 0 0 0 0 {name=C1 model=cap_cmim w=26u l=26u m=1 spiceprefix=X}
C {lab_pin.sym} 0 -30 0 0 {name=l1 lab=VCTRL}
C {lab_pin.sym} 0 30 0 0 {name=l2 lab=VSS}
C {iopin.sym} -400 -300 0 0 {name=p1 lab=VCTRL}
C {iopin.sym} -400 -260 0 0 {name=p2 lab=VSS}
