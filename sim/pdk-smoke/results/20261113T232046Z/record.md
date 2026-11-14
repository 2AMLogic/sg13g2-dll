# pdk-smoke record

SIMULATED results, never measured.

## inv_lv.envelope.json (corners)
- status: pass; corners: 3/3 pass
- engine: ngspice 47; backend: batch
- batch job: klt-sim-aca1647e4ff4

## Provenance

- sg13g2-dll commit: `4a4c719515b3bc0a793259990738fb4bacba9674` (working tree dirty under sim/)
- PDK pin: IHP-Open-PDK `v0.3.0` (`sim/pdk.json`)
- OSDI models (sha256 of the binaries the run loaded): `psp103.osdi` 2e4299c4683997e2…; `psp103_nqs.osdi` 839b164483205601…; `r3_cmc.osdi` 4fead17bc2e9cbfe…; `mosvar.osdi` 25e64a374ab523db…
- OSDI build: `sim/harness/common/build-osdi.sh` (OpenVAF-Reloaded v24.0.1mob), see `reuse.lock.json`
- ngspice (as run, on the batch fleet): ngspice 47; the dispatch worker's local ngspice 42 cannot load these OSDI v0.4 models
- klt: klt 0.9.2.dev1016+g606e5728939d
- backend: batch fleet; jobs: {"inv_lv": {"job_id": "klt-sim-aca1647e4ff4", "instance_type": "c7i.8xlarge", "ami_id": "ami-0f6bb304291339ed0", "lifecycle": "spot"}}

| request | corner | status | measurements (V, s, A) |
|---|---|---|---|
| inv_lv | mos_tt/novdd/27C | pass | voh=1.2, vol=8.153e-09, tphl=3.269e-11, tplh=4.768e-11 |
| inv_lv | mos_ff/novdd/27C | pass | voh=1.2, vol=1.722e-07, tphl=2.748e-11, tplh=3.954e-11 |
| inv_lv | mos_ss/novdd/27C | pass | voh=1.2, vol=8.808e-10, tphl=4.009e-11, tplh=6.027e-11 |

## Verdict: PASS
