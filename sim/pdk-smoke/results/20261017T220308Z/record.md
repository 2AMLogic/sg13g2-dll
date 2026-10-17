# pdk-smoke record

SIMULATED results, never measured. Device-family load check only; no design.

- Verdict: **PASS**
- sg13g2-dll commit: `da166a6fe1cac34d166d0b45003e7ccf0e41ada7` (working tree dirty under sim/)
- PDK pin: IHP-Open-PDK `v0.3.0` (`sim/pdk.json`)
- OSDI models (sha256 of the binaries the run loaded): `psp103.osdi` 2e4299c4683997e2…; `psp103_nqs.osdi` 839b164483205601…; `r3_cmc.osdi` 4fead17bc2e9cbfe…; `mosvar.osdi` 25e64a374ab523db…
- OSDI build: `sim/harness/common/build-osdi.sh` (OpenVAF-Reloaded v24.0.1mob), see `reuse.lock.json`
- ngspice (as run, on the batch fleet): ngspice 46; the dispatch worker's local ngspice 42 cannot load these OSDI v0.4 models
- klt: klt 0.7.1.dev1743+g7ee09483b748
- backend: batch fleet; jobs: {"inv_lv": {"job_id": "klt-sim-0d1720ca1e9f", "instance_type": "m7i.4xlarge", "ami_id": "ami-0e0bec04ad8e81877", "lifecycle": "spot"}, "inv_hv": {"job_id": "klt-sim-cdb42ec3af49", "instance_type": "m7i.4xlarge", "ami_id": "ami-0e0bec04ad8e81877", "lifecycle": "spot"}, "npn_op": {"job_id": "klt-sim-c6cc00df63df", "instance_type": "m7i.4xlarge", "ami_id": "ami-0e0bec04ad8e81877", "lifecycle": "spot"}}

| request | corner | status | measurements (V, s, A) |
|---|---|---|---|
| inv_lv | mos_tt/novdd/27C | pass | voh=1.2, vol=8.153e-09, tphl=3.269e-11, tplh=4.768e-11 |
| inv_lv | mos_ff/novdd/27C | pass | voh=1.2, vol=1.722e-07, tphl=2.748e-11, tplh=3.954e-11 |
| inv_lv | mos_ss/novdd/27C | pass | voh=1.2, vol=8.808e-10, tphl=4.009e-11, tplh=6.027e-11 |
| inv_hv | mos_tt/novdd/27C | pass | voh=3.3, vol=1.027e-09, tphl=7.582e-11, tplh=1.5e-10 |
| inv_hv | mos_ff/novdd/27C | pass | voh=3.3, vol=8.727e-09, tphl=6.747e-11, tplh=1.305e-10 |
| inv_hv | mos_ss/novdd/27C | pass | voh=3.3, vol=2.925e-10, tphl=8.684e-11, tplh=1.778e-10 |
| npn_op | hbt_typ/novdd/27C | pass | ic_a=0.0001399 |
