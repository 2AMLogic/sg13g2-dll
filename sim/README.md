# sim

Simulation tree for the DLL canary. All results here are **simulated, never
measured**; `sim/*/results/` is append-only evidence.

## PDK pin and OSDI device models

- `sim/pdk.json` pins the IHP-Open-PDK release (v0.3.0) and records the
  `PDK_ROOT/ihp-sg13g2` layout and ngspice versions.
- SG13G2's MOS devices are PSP103.6 Verilog-A models; ngspice loads them only
  as OSDI binaries. `sim/harness/common/build-osdi.sh` builds them from the
  PDK's own Verilog-A. It is a **vendored** copy of `2AMLogic/sg13g2-bandgap`
  `sim/tools/build-osdi.sh` at the commit in `reuse.lock.json`
  (`sg13g2-bandgap` is the master; do not edit it here).
- No `.osdi` binary is committed (platform-specific).
- `sim/check-pins.sh` re-hashes the vendored script against `reuse.lock.json`
  and checks `sim/pdk.json` against the installed tree. `--lock-only` skips
  the PDK half (no PDK needed).

```
export PDK_ROOT=/path/containing/ihp-sg13g2   # see sim/harness/env.sh for the search path
sim/harness/common/build-osdi.sh --check      # models present and loadable?
sim/harness/common/build-osdi.sh              # build them if not
```

The OSDI binaries `build-osdi.sh` produces target OSDI v0.4 and need
ngspice >= 44. A host with an older ngspice (the dispatch worker has 42)
cannot run them locally (`osdi_abi_mismatch`); the smoke runs on the batch
fleet instead.

## Device smoke (`sim/pdk-smoke/`)

One command, from a fresh clone with the PDK installed and OSDI built:

```
sim/pdk-smoke/run.sh
```

It runs a minimum-size inverter transient for `sg13_lv_*` (1.2 V) and
`sg13_hv_*` (3.3 V) at `mos_tt`/`mos_ff`/`mos_ss`, and one `npn13G2` DC
operating point, all through `klt sim` (multi-corner requests go to the batch
fleet; there is no local fallback). It writes
`sim/pdk-smoke/results/<UTC stamp>/` (requests, envelopes, `record.md`) and
exits non-zero if the OSDI models are missing (exit 3, before any simulation),
if the batch submit fails, or if any corner reports a diagnostic or does not
pass. Set `SMOKE_CAPACITY_WAIT_S` to bound the wait for fleet capacity. The
limits in the requests are sanity gates, not spec numbers.

`record.md` names the repo commit, PDK pin, OSDI binary hashes, ngspice
version and batch jobs of the run.
