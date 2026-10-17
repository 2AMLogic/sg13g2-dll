# DR-004: Adopt `sg13g2-pll`'s PFD and charge pump; `klt` array capability

- **Status**: proposed (ratified with DR-001)
- **Date**: 2026-10-17
- **Decided by**: Builder agent, issue #2
- **Related**: `reuse.lock.json`; DR-001 (rail); DR-002

## Decision: adopt, with a fit gate

| Block | Decision |
|---|---|
| Phase-frequency detector | **Adopt** `design/pfd.sch` (tri-state, SR latches + edge detectors) from `2AMLogic/sg13g2-pll` @ `83e59fe81db0b09dbefcff35a55965bea0c2a76f` |
| Charge pump | **Adopt** `design/cp.sch` (cascoded current-steering, `cp_leg_n`/`cp_leg_p`, dump buffer) from the same commit |
| Loop filter | **Keep (do not adopt)**: the PLL's is a fixed second-order filter; the DLL's loop is first-order, a single capacitor. It is a DLL-specific part. |

Reason: both blocks are on the same PDK and the same `sg13_hv_*` rail (DR-001),
and the README says to adopt, not redesign. A PLL and a DLL share
sub-blocks, not a loop.

Source and evidence read: the file listing and the `.spice` exports'
header comments (`pfd REF FB UP DN VDD VSS`; `cp UP DN IBP ICP IBN ICN VOUT VDD VSS`) and the sibling's DR-002 Decision 0. **Not read or simulated**: the
internals' sizing and their behavior at 1 GHz. `pfd` uses a 5-stage delay-chain
edge detector as its reset-pulse generator; whether it resolves 1 GHz edges and
dead zone is unknown.

**Fit gate**: the first schematic issue simulates the stamped PFD with
1 GHz inputs across the corner set. If it does not fit, a new record states
why not and what replaces it. The CP's topology is adopted, its bias currents
are not: the DLL's first-order loop sets its own charge-per-cycle budget (DR-003
part 2).

## `klt` capability: symmetric placement and extraction of a matched array

Answered from the tool's documented capability, `klt 0.7.1.dev1755+gdce956c3c399`:

- `klt gen-compose --help`: "Supports placement.strategy ... `array` (one block repeated on a regular rows x cols grid, emitted as a single hierarchical instance)". So a regular, identical array is available for placement.
- `klt pex --help` lists "extract a parasitic-annotated netlist and re-sim the schematic testbenches against it".

Not established by these two commands, and so **unverified, to be filed**:

1. Whether `klt pex` extraction reports per-instance parasitic mismatch within the array so a tap-to-tap delay difference can be attributed. 
2. Whether array edges (the first and last cell see different neighbours) are
   detectable or can be given dummy cells by the tool.
3. Whether a **matched** routing check (equal-length, equal-parasitic nets for
   the control line) exists.

No gap is filed from this PR, since none was reproduced against the tool; the
first layout issue runs the command on a real array and files any gap,
described generically, at `2AMLogic/klayout-tools`.
