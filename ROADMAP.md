# Roadmap

A delay-locked loop on IHP SG13G2: a voltage-controlled delay line locked to
one period of the input clock, with evenly spaced output phases, designed and
verified through klayout-tools (`klt`), xschem and ngspice.

Status as of 2026-11-13, `main` @ `fc59cce`. Every number cited is simulated,
never measured. `WORK_PLAN.md` is the generated label-state view.

## Where it stands

Graded position: `manifests/sg13g2-dll.signoff.json` (klt 0.8.0, byte-compared
in CI by `scripts/check-signoff.sh`) reads **1 of 11 T1 items met**. Tracker: #6.

| T1 item | Grade | State on `main` |
|---|---|---|
| 1 Design sources | unmet | 24 schematics under `design/`, 9 exported netlists (`design/netlist.sh`); no `dll_top`, nothing attested (#58) |
| 2 Layout | unmet | `layout/` holds only a README (#25) |
| 3 DRC clean | unmet | needs item 2 (#26) |
| 4 LVS clean | unmet | needs items 1 and 2 (#27) |
| 5 Corner verification | unmet | not filed; needs a ratified spec (#41) |
| 6 Monte Carlo evidence | unmet | not filed; row 4 has no statistical limit (#73) |
| 7 Post-layout verification | unmet | not filed; needs items 2 and 5 |
| 8 Characterization report | unmet | not filed; needs items 5 to 7 |
| 9 Testbenches shipped | unmet | row benches exist but drive the stand-in DUT in `sim/standin/` (#28) |
| 10 Repo hygiene | **met** | `manifests/evidence/item-10-repo-hygiene.json` (PR #47) |
| 11 Power delivery | unmet | needs `dll_top` and LVS (#29) |

Spec: `spec/target-spec.md` (12 rows, 45-corner set in `sim/corners.json`) is
**proposed**. The ratification record is
[0009](spec/decisions/0009-ratification-of-target-spec.md); the review trees
are under `ratification/` (PR #42).

Sub-block evidence, all on the reduced corner set (fast iteration, not a
recorded spec result per decision 0001):

- **Delay line**: the drawn two-stage cell spans T/8 at 500 MHz but not at
  1 GHz / ss (fastest step 150.7 ps against 125 ps;
  `sim/delay-sanity/results/20261105T080322Z/`, decision 0010). Two candidates
  both reach 125 ps at ss: A, one stage per tap, and B, two stages with the
  starving devices widened 4x
  (`sim/delay-sizing/results/20261107T231500Z-comparison/comparison.md`, PR #68).
- **PFD**: fit gate C1 and C3 pass; C2 (reset pulse at most 0.25 T) fails at
  1 GHz at tt and ss (`sim/pfd-fit/results/20261105T125120Z/fit-gate.md`,
  decision 0011). `pfd` is `adopting` in `reuse.lock.json`.
- **Charge pump**: K1 to K6 pass after the `cp_bias` and `cp_dumpbuf` redraw
  (`sim/cp-currents/results/20261106T182524Z/`, PR #64, decision 0012 update).
  Charge per pulse is not graded. `cp` stays `adopting` until the PFD gate closes.
- **Lock detector and false-lock supervisor**: drawn, smoke benches pass
  (`sim/lock-detector-smoke/results/20261105T091102Z/`,
  `sim/supervisor-smoke/results/20261105T052155Z/`; PRs #57, #55).
- **Row benches** (`sim/false-lock`, `lock-time`, `phase`, `power`): built on
  `sim/harness/dllbench.py`, no committed results. `sim/jitter` has no deck:
  the spec requires a noise-method decision record first, and none exists.

## Now

Can start today. No issue carries the ready label; #94 is curated and items
2 to 4 have no issue yet.

1. **Power bench exit code** (#94). Done when `sim/power/run.sh` exits non-zero
   on a DUT where row 10 is not graded.
2. **Redraw the PFD reset path to pass C2 at 1 GHz** (no issue; decision 0011
   proposal, options 1 and 2). Done when a new `sim/pfd-fit/results/<stamp>/fit-gate.md`
   shows C1, C2 and C3 passing at tt, ss and ff at both 1 GHz and 500 MHz with
   `grade.py` criteria unchanged, and 0011 carries a dated update.
3. **Candidate B at 3x widening, full grid** (no issue; `comparison.md`
   line 77: "a 3x full-grid run should precede sizing"). Done when
   `DS_B_SCALE=3 sim/delay-sizing/run.sh full` has a committed result directory
   and a comparison note against the 4x figures. It informs the #58 ruling and
   the cell that layout would draw; it does not make the ruling.
4. **Noise-method decision record for row 6, validated on a known case** (no
   issue; `spec/target-spec.md` "Jitter method"). Done when a record under
   `spec/decisions/` fixes which devices, what bandwidth and where the source
   equivalents sit, and a committed bench reproduces a known jitter figure
   within a tolerance stated in advance. No DLL jitter number is produced here.
5. **Harness clean-ups already in review**: PRs #88 (#85), #103 (#96),
   #105 (#104) are approved; #106 (#99) has changes requested and a conflict.

## Next

- **Draw `dll_top`, export its netlist, attest item 1** (#58). Unblocked by the
  delay-tap ruling (below); better started after Now item 2 so the PFD it
  instantiates has passed its gate. Done when `klt signoff` grades item 1 `met`.
- **Repoint the row benches at the item-1 netlist and attest item 9** (#28).
  Needs #58. Done when `sim/inventory.json` lists no stand-in bench and item 9
  grades `met`.
- **Move `pfd` and `cp` from `adopting` to `kept`** in `reuse.lock.json`. Needs
  Now item 2 and a graded charge-per-pulse criterion in `sim/cp-currents`
  (decision 0012: "still not graded and still not claimed").
- **Layout, DRC, LVS, supply ERC** (#25, #26, #27, #29), in that order. Needs
  #58. #25 is to be split when it unblocks, carrying decision 0004's symmetry
  rule (identical cells, identical tap loading, dummy on the last tap) into
  its acceptance criteria.
- **File T1 items 5 to 8** once the spec is ratified (#41).

## Later

- **Post-layout re-verification of rows 4, 5 and 8** (spec row 11). Question
  first: does extraction of the regular delay-line array preserve the matching
  that phase spacing depends on? Expect tool findings here; file them upstream.
- **Statistical phase-spacing limit** (row 4). Question first: #73, and then a
  locked-loop, post-layout Monte Carlo result to set a value from.
- **First jitter result** (row 6). Question first: do the PSP103 OSDI models
  contribute noise in an ngspice transient run? Now item 4 answers it.
- **2 GHz stretch column.** Question first: does 1 GHz close at all 45 corners?

## Blocked and waiting

Waiting on an operator decision; no agent can advance these:

- **#58 delay-tap structure**: B (two widened stages per tap, the #67 result's
  recommendation) or A (one stage per tap, ratifying 0010). Holds #58 and,
  through it, #25 to #29: six of the eleven T1 items.
- **#41 spec ratification**: the two review keys and the ratifying approval
  are owed. Holds T1 items 5 to 8.
- **#73** row 4 statistical limit.
- **Proposals awaiting a ruling**: #107 (stop committing `.spiceinit` scratch
  copies), #101 (single schematic authoring path), #91 (make the row 7 and
  row 12 verdicts grade something), #74 (one envelope screen for all graders).

Upstream tool gaps worked around, none blocking an item above:
klayout-tools#3881 and #3878 (decision 0003), #4091 (`design/NOTES.md`).

## Not planned

- A 250 MHz operating point: declined in decision 0013.
- 16 phases at the target column: declined in decision 0007; stretch only.
- Frequency synthesis, a reference oscillator, and duty-cycle correction of
  the input clock (README scope, decision 0002).
- hv or HBT devices: the block is 1.2 V thin-oxide only (decision 0007).
- A second PFD or charge-pump topology (decision 0006 adopts the sibling's).
