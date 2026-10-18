# Harness evidence record

SIMULATED results, never measured.

## pvt.envelope.json (corners)
- status: pass; corners: 3/3 pass
- engine: ngspice 46; backend: batch
- batch job: klt-sim-78317c2ba1e8

## ic.envelope.json (ic)
- status: pass; corners: 15/15 pass
- engine: ngspice 46; backend: batch
- batch job: klt-sim-31ca5e090a11

## mc.envelope.json (mc)
- status: pass; corners: 16/16 pass
- engine: ngspice 46; backend: batch
- batch job: klt-sim-c6460b1aa0b1
- Monte Carlo: seed=20261018 n=8 vary=mismatch seed_scope=None
- sigma within one process corner: voh @ mos_tt_mismatch/novdd/27C=0.0, voh @ mos_ss_mismatch/novdd/27C=0.0, vol @ mos_tt_mismatch/novdd/27C=2.474857516468661e-09, vol @ mos_ss_mismatch/novdd/27C=7.763327636302066e-11, tphl @ mos_tt_mismatch/novdd/27C=1.3391784383798254e-12, tphl @ mos_ss_mismatch/novdd/27C=1.9725883832724516e-12, tplh @ mos_tt_mismatch/novdd/27C=1.9040260997141975e-12, tplh @ mos_ss_mismatch/novdd/27C=1.8642868176310374e-12

## ctl.envelope.json (mc)
- status: pass; corners: 16/16 pass
- engine: ngspice 46; backend: batch
- batch job: klt-sim-4c52811cf816
- Monte Carlo: seed=20261018 n=8 vary=mismatch seed_scope=None
- sigma within one process corner: voh @ mos_tt/novdd/27C=0.0, voh @ mos_ss/novdd/27C=0.0, vol @ mos_tt/novdd/27C=0.0, vol @ mos_ss/novdd/27C=0.0, tphl @ mos_tt/novdd/27C=0.0, tphl @ mos_ss/novdd/27C=0.0, tplh @ mos_tt/novdd/27C=0.0, tplh @ mos_ss/novdd/27C=0.0

## Verdict: PASS
