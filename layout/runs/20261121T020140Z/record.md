# layout run record 20261121T020140Z

- repo HEAD: ce8db57f06f34e272f27075747d6515f4510cf8c
- klt: klt 0.8.0 (scripts/klt.sh pin)
- klayout (wiring): 0.30.13 (`uv run --with klayout==0.30.13`)
- PDK: ihp-sg13g2 (fetched:0.3.0, sim/pdk.json; root resolved by klt pdk find)

Per-cell evidence: the committed drc_report.json / lvs_report.json
next to each GDS are this run's envelopes; the sha256 below binds
them to the stream that produced them.

loop_filter gds=abd1746d3f90b250d4ee0b00bd51a851cd6d547da4a9c8f86fa4c6398ad14d92 drc=clean lvs=match
cp_bias gds=455003f1c5e3d126ed3223bcb9860140848e6ad73233bc7c9bbf4faae4576821 drc=clean lvs=match
cp gds=36b1d8b55d087d54103c1090751ad2686991305def759deb7d332ec0944cbb97 drc=clean lvs=match
