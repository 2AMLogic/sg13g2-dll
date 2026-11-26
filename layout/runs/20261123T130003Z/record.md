# layout run record 20261123T130003Z

- repo HEAD: 1b6ff270400ab1e5a69a396c76eb8fa9cd4039d5
- klt: klt 0.8.0 (scripts/klt.sh pin)
- klayout (wiring): 0.30.13 (`uv run --with klayout==0.30.13`)
- PDK: ihp-sg13g2 (fetched:0.3.0, sim/pdk.json; root resolved by klt pdk find)

Per-cell evidence: the committed drc_report.json / lvs_report.json
next to each GDS are this run's envelopes; the sha256 below binds
them to the stream that produced them.

loop_filter gds=abd1746d3f90b250d4ee0b00bd51a851cd6d547da4a9c8f86fa4c6398ad14d92 drc=clean lvs=match
cp_bias gds=8115c88328492713e21219e5ba782c6b8d4340321b2cae4c9b553297057027e2 drc=clean lvs=match
cp gds=a7da7bd1f7328506e377b7a2a6822492e69cc60e0a63651fa18c5ff0e0a47b5f drc=clean lvs=match
