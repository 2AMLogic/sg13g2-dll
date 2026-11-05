v {xschem version=3.4.8RC file_version=1.3
refmask -- masks REF until the first falling REF edge after RSTB goes high
}
G {}
K {}
V {}
S {}
E {}
C {inv_lv.sym} 0 0 0 0 {name=XIR}
C {lab_pin.sym} -60 0 0 0 {name=l1 lab=REF}
C {lab_pin.sym} 60 0 0 0 {name=l2 lab=refb}
C {lab_pin.sym} 0 -40 0 0 {name=l3 lab=VDD}
C {lab_pin.sym} 0 40 0 0 {name=l4 lab=VSS}
C {dffr_lv.sym} 300 0 0 0 {name=XEN}
C {lab_pin.sym} 240 -20 0 0 {name=l5 lab=VDD}
C {lab_pin.sym} 240 0 0 0 {name=l6 lab=refb}
C {lab_pin.sym} 240 20 0 0 {name=l7 lab=RSTB}
C {lab_pin.sym} 360 -10 0 0 {name=l8 lab=en}
C {lab_pin.sym} 360 10 0 0 {name=l9 lab=en_n}
C {lab_pin.sym} 300 -50 0 0 {name=l10 lab=VDD}
C {lab_pin.sym} 300 50 0 0 {name=l11 lab=VSS}
C {nand2_lv.sym} 600 0 0 0 {name=XAN}
C {lab_pin.sym} 540 -10 0 0 {name=l12 lab=REF}
C {lab_pin.sym} 540 10 0 0 {name=l13 lab=en}
C {lab_pin.sym} 660 0 0 0 {name=l14 lab=refm_n}
C {lab_pin.sym} 600 -40 0 0 {name=l15 lab=VDD}
C {lab_pin.sym} 600 40 0 0 {name=l16 lab=VSS}
C {inv_lv.sym} 900 0 0 0 {name=XAI}
C {lab_pin.sym} 840 0 0 0 {name=l17 lab=refm_n}
C {lab_pin.sym} 960 0 0 0 {name=l18 lab=REFM}
C {lab_pin.sym} 900 -40 0 0 {name=l19 lab=VDD}
C {lab_pin.sym} 900 40 0 0 {name=l20 lab=VSS}
C {ipin.sym} -400 -300 0 0 {name=p1 lab=REF}
C {ipin.sym} -400 -260 0 0 {name=p2 lab=RSTB}
C {opin.sym} -400 -220 0 0 {name=p3 lab=REFM}
C {iopin.sym} -400 -180 0 0 {name=p4 lab=VDD}
C {iopin.sym} -400 -140 0 0 {name=p5 lab=VSS}
