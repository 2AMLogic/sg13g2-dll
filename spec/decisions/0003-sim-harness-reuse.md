# 0003 — Sim grid harness: adopt or keep

- **Status**: recorded; decides no spec number. Corner values stay with issue #2.
- **Date**: 2026-10-18 (against `origin/main` at `6c72aa8`)
- **Origin**: this repo's issue #4.

## Question

Does the PVT / start-state / Monte Carlo harness take the mechanics of
`2AMLogic/sg13g2-bandgap` `sim/harness/` and `2AMLogic/sky130-pll`
`sim/harness/` as stamped copies, or keep a thin harness of its own?

## Decision

**Keep thin, no stamped copies.** Recorded in `reuse.lock.json` under
`not_adopted`.

| Source | What it carries | Disposition | Reason |
|---|---|---|---|
| `sg13g2-bandgap` `klt_corner_bundle.py` | One bundle `.lib` per corner label, because SG13G2 splits corners over three per-family libraries | **Not needed yet** | The only models this repo loads so far are the MOS libraries (`cornerMOSlv.lib`), and `klt sim` now takes `corners.process[].sections[]` with a per-section `lib`. Revisit when #2 fixes a corner set that needs HBT and resistor sections together; if the bundle is still needed then, adopt it from the master. |
| `sg13g2-bandgap` `klt_sim_evidence.py`, `merge_batch_shards.py` | Evidence adapter, shard merge | **Not adopted** | `klt sim` writes the envelope and merges its own batch jobs. `sim/harness/evidence.py` only grades an envelope (about 150 lines) and is specific to the three modes here. |
| `sky130-pll` `montecarlo.py`, `checkpoint.py`, `corners.py`, `executor.py` | Hand-rolled trial matrix, resume and executor | **Not adopted** | They predate native `klt sim` support for `monte_carlo` (seed, `n`, `vary`, `seed_scope`), `--resume` and the batch backend, and they are sky130-specific (`MC_MM_SWITCH`). Copying them would add a second runner beside `klt sim`. |

Fit was judged from file names and the docstrings of the two files read, not
from a full read of every file; treat it as a reasoned call, not an audit.

## What the harness is instead

`sim/harness/gridspec.py` builds a `klt sim` request from one base request plus
`sim/corners.json`, an optional start-state axis (`corners.supply_v`) and
`monte_carlo`. It runs nothing itself, so every grid is a `klt sim` request and
goes to the batch fleet. The negative control is the same Monte Carlo request on
the non-mismatch model sections (SG13G2 draws mismatch from ngspice's RNG inside
the `*_mismatch` sections, so `monte_carlo.vary` alone does not pin it).

## Tool gaps

- `klt sim` has no `.ic` / `uic` request axis. The start-state axis is a
  voltage source swept through `corners.supply_v`, with a deck that ties a
  node to it through a switch, which puts the burden on every testbench.
- The batch fleet runner image refused `corners.params` on 2026-10-18
  (`params_unsupported_worker`: 3 reports for 15 dispatched points), although
  the client documents the axis. That is why the start-state axis does not use
  it.

Filed upstream per the friction protocol: `2AMLogic/klayout-tools#3881` (no
`.ic`/`uic` axis) and a confirming comment on `2AMLogic/klayout-tools#3878`
(runner image lag for `corners.params`).
