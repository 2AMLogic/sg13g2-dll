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

## Grid harness (`sim/harness/`, `sim/corners.json`)

Testbenches are graded over PVT corners, start states and Monte Carlo draws by
building **one `klt sim` request** per grid; nothing here launches `ngspice`
itself, so multi-unit grids go to the batch fleet and a failed submit is an
error, never a local fallback.

- `sim/harness/gridspec.py` builds a grid request from a base request (netlist,
  models, analysis, measurements; no `corners`/`monte_carlo`) plus:
  - **corners**: `sim/corners.json` (or `--corners`). It is a schema with **no
    values** until the ratified spec (#2) fills it, and the runner refuses an
    empty set.
  - **start states**: `--ic SOURCE=v1,v2,...` (repeatable, equal lengths; one row
    per start state). `SOURCE` is a voltage source in the deck whose value is
    swept through `corners.supply_v`; the deck ties a node to it through a
    switch for the first picoseconds, then releases it (see
    `sim/harness-example/decks/inv_ic.spice`). The axis is crossed with the
    corner file's own `supply_v` rows. `corners.params` is not used because the
    fleet runner image can lag the client and refuses it
    (`params_unsupported_worker`), and `klt sim` has no `.ic`/`uic` axis (tool
    gaps, see `spec/decisions/0003-sim-harness-reuse.md`).
  - **Monte Carlo**: `--mc-n --mc-seed --mc-vary [--mc-seed-scope]`, crossed
    with the corners (`corner_count * n` runs). Seed and `n` are echoed in the
    envelope's `environment.monte_carlo`. `--control-process mos_tt` (repeatable)
    also writes the **negative control**: the same request, seed and `n` on
    the non-mismatch model sections, which must give sigma exactly 0 and
    repeat identically.
- `sim/harness/evidence.py` grades envelopes (diagnostics, recorded seed/`n`,
  start-state axis took effect, negative control, repeat identity) and writes
  `record.md`.
- Unit tests (no simulator): `python3 -I -m unittest discover -s sim/harness/tests`

### Cold start: example bench (`sim/harness-example/`)

The `pdk-smoke` inverter through all three modes (corner sweep, start-state
sweep, Monte Carlo with negative control). Corner sets there are smoke-only,
not the DLL's. Same prerequisites as the device smoke (PDK, OSDI built):

```
sim/harness-example/run.sh
```

It writes `sim/harness-example/results/<UTC stamp>/` (requests, envelopes,
`record.md`) and exits non-zero on any diagnostic, a missing seed/`n`, a
start-state axis that did not take effect, or a negative control with nonzero
sigma. `EXAMPLE_MC_SEED` / `EXAMPLE_MC_N` override the draw; the committed
result uses the defaults. Results are simulated, never measured.

The committed run is `sim/harness-example/results/20261018T022831Z/`: seed
`20261018`, `n=8` per process corner, negative control (`ctl.envelope.json`,
repeated in `ctl_repeat.envelope.json`) with sigma exactly 0 within every
corner. The pooled sigma over several corners is not zero (it contains the
corner-to-corner spread), so the checks read the per-corner block.
