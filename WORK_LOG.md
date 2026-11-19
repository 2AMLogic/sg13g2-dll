# Work Log

Chronological record of merged PRs and closed issues. Maintained by the Guide role.

### 2026-11-19

- **PR #185**: docs: correct the schematic-authoring docs and gate mksch staleness from netlist.sh --check
- **Issue #101** (closed): Correct the contradictory design-authoring docs and run mksch.py --check from design/netlist.sh --check
- **PR #181**: chore: re-vendor build-osdi.sh and read OpenVAF pins from --print-pins
- **Issue #179** (closed): Re-vendor build-osdi.sh at the new owner hash and read pins from --print-pins

### 2026-11-18

- **PR #180**: chore: ignore klt .spiceinit scratch in sim results
- **PR #178**: chore: drop vendored T1 checklist and --tiers-doc override
- **PR #168**: ci: run signoff and unit workflows on merge-group checks_requested
- **Issue #116** (closed): Stop vendoring design-evidence-tiers.md: the pinned klayout-tools 0.8.0 wheel already ships the identical 1053 lines
- **Issue #107** (closed): Stop committing klt's .spiceinit scratch file: 429 byte-identical copies are 19% of the repo's tracked files
- **Issue #167** (closed): Merge queue: add the merge_group trigger to the required-check workflow(s)

### 2026-11-17

- **PR #162**: chore(loom): resync installed Loom to v0.19.1306

### 2026-11-16

- **PR #154**: chore(loom): resync installed Loom to v0.19.1302
- **Issue #156** (closed): WORK_PLAN's operator merge-risk-hold section under-reports: #154 held since 06:51Z was absent from a 09:50Z Guide write

### 2026-11-15

- **PR #149**: sim: re-run supervisor and lock-detector smoke on the 3-stage edgedet; record ss probe failures
- **PR #147**: test: assert every read guarded knob is named in its Env block
- **PR #141**: design: 3-stage edgedet chain + sized srlatch_fast; gate still fails ss C2, two-knob refutation measured
- **Issue #145** (closed): Shared edgedet shortened 5 -> 3 stages: supervisor and lock_detector smoke evidence is now stale and unverified
- **Issue #142** (closed): Extend test_bench_env_namespaces.py with a documentation assertion: every *_RESULTS_DIR reader carries an # Env: line
- **Issue #136** (closed): PFD fit gate: C2 is still open at ss/1 GHz after the reset-path redraw (decision 0011 follow-up)
- **PR #143**: docs: document NOISE_METHOD_RESULTS_DIR knob in noise-method runner header
- **PR #144**: test: harden the bench env-namespace guard against silent coverage loss
- **PR #139**: fix: read recorded PVT corners from the envelope in cp-currents and delay-sizing headers
- **PR #133**: test: pin the committed envelope corpus to klt's backend provenance shape
- **PR #135**: fix: give each sim bench its own env-knob namespace
- **PR #132**: ci: gate the sim harness and pfd-fit unit suites in GitHub Actions
- **Issue #134** (closed): sim/noise-method/run.sh reads NOISE_METHOD_RESULTS_DIR with no # Env: header line
- **Issue #137** (closed): test_bench_env_namespaces guard: hardcoded helper list and nested-default parser blind spots
- **Issue #119** (closed): Two record writers still hand-copy the reduced_set corner triple that #99 removed from the other three
- **Issue #130** (closed): Pin the envelope backend shape, not just backend_of's reaction to a bad one: a klt pin bump can still crash a summarizer mid-record
- **Issue #120** (closed): Give each bench its own env-knob namespace: DS_VC and DS_RESULTS_DIR are read by two benches, SS_RESULTS_DIR by two more
- **Issue #118** (closed): CI never runs sim/harness/tests: the 83 harness unit tests are executed only by hand
- **Issue #111** (closed): Row benches document exit 6 for "a corner fails its row", but a real failing corner reaches exit 1 first
- **PR #131**: fix: grade a failed corner as exit 6 and an errored corner as exit 1
- **Issue #113** (closed): Redraw the PFD reset path so the fit gate's C2 passes at 1 GHz (decision 0011)
- **PR #129**: design(pfd): redraw the reset path on PFD-local cells; ss/1GHz fit-gate C2 stays open (0011)
- **Issue #115** (closed): Write the row 6 noise-method decision record and validate it on a known case
- **PR #128**: feat: row 6 noise-method decision record (0014) and its known-case validation bench
- **Issue #125** (closed): Deduplicate evidence.backend_of and dllbench.mvals: three backend spellings, one of which raises AttributeError
- **PR #127**: refactor: deduplicate backend_of and mvals into sim/harness/evidence.py
- **Issue #121** (closed): Collapse the two single-unit smoke runners onto one shared smoke_main: 23 of 31 lines are byte-identical
- **PR #126**: refactor(sim): collapse both single-unit smoke runners onto one smoke_main
- **PR #112**: docs: roadmap as of 2026-11-13

### 2026-11-14

- **Issue #114** (closed): Run delay-tap candidate B at 3x widening over the full grid and compare with the 4x result
- **PR #124**: sim: record delay-tap candidate B at 3x widening and compare with 4x
- **Issue #109** (closed): Consolidate the second reduced-set corner reader: sim/pfd-fit/make_bench.py rebuilds corners.units inline instead of gridspec.load_reduced_set
- **PR #122**: refactor(sim): read pfd-fit corners through gridspec, not a second json reader
- **Issue #99** (closed): Remove the hardcoded run-condition literals from the sim record writers: backend, simulator version, corner and unit are printed as constants while the envelope records them
- **PR #106**: refactor(sim): read run conditions from the envelope instead of printing them as constants
- **Issue #94** (closed): Power bench run.sh would exit 0 (documented as pass) on a DUT where row 10 is NOT GRADED
- **PR #110**: fix: exit 6, not 0, when a bench row gets no verdict
- **Issue #96** (closed): Remove the hv and HBT legs of the PDK pin and device smoke: decision 0007 dropped both families, but every bench preflight still requires their model files
- **PR #103**: refactor(sim): drop the hv and HBT legs from the PDK pin and device smoke
- **Issue #85** (closed): Remove the noise-method grep gate in sim/jitter/run.sh: it matches decision 0001 and reports a record that does not exist
- **PR #88**: fix(jitter): refuse unconditionally instead of reporting a record that does not exist
- **Issue #104** (closed): Remove the markdown-table scrape in cp-currents: K4 re-parses delay-sanity record.md instead of reading its envelopes
- **PR #105**: refactor: read K_dl from the delay-sanity envelopes, pin the source run
- **Issue #92** (closed): bug: grade() always reports a harness FAIL on the single-start-state benches (phase, power), because check_ic_applied demands >= 2 start states
- **PR #100**: fix(harness): expect per-axis start-state arity from the manifest, not a hard 2
- **Issue #89** (closed): Give klt one true version statement: scripts/klt.sh pins 0.8.0 for one caller while every bench and netlist.sh use the klt on PATH
- **PR #97**: docs: scope the klt 0.8.0 pin claim to the signoff records

### 2026-11-13

- **Issue #87** (closed): Make the stand-in DUT flags do something: supply_current and attestable are read by nothing, so the power bench passes at 0 mW
- **PR #93**: fix(harness): withhold the row-10 power limit on a DUT that draws no supply current
- **Issue #95** (closed): Remove design/inventory.json: an unreferenced partial item-1 inventory that attests a pass for three of nine tops
- **PR #98**: chore: delete the unreferenced partial item-1 attestation inventory
- **Issue #81** (closed): Remove ten copies of the klt sim submit block: add sim_submit to sim/harness/preflight.sh
- **PR #84**: refactor(sim): replace ten copies of the klt sim submit block with sim_submit
- **Issue #83** (closed): Remove the stale hand-written status paragraphs in design/README.md and design/NOTES.md: they say nothing was simulated while committed results show two failed gates
- **PR #86**: docs(design): replace the stale status prose with pointers to the evidence
- **Issue #82** (closed): Remove nine copies of the klt sim submit block: one sim_submit in sim/harness/preflight.sh
- **Issue #76** (closed): Remove the six per-bench reduced-corner files: read reduced_set from sim/corners.json instead of four hand copies
- **PR #80**: refactor(sim): read reduced-set corners from sim/corners.json, not per-bench copies
- **Issue #71** (closed): Remove the netlist.sh --check skip in delay-sizing: make the staleness gate ignore the klt header line
- **PR #79**: fix: strip klt's provenance header in netlist.sh so --check grades content
- **Issue #72** (closed): Consumer requirements from sg13g2-aib, re-compared at 381d989: 250 MHz, 4-vs-16 phases at 500 MHz, unbounded MC spacing, 5 ps rms jitter
- **PR #75**: spec: record 0013 disposing the re-compared aib requirements

### 2026-11-12

- **PR #69**: Bump Repo Skills 0.25.10 -> 0.26.1

### 2026-11-07

- **Issue #67** (closed): Delay-tap sizing comparison: one stage per tap (0010) vs widened two-stage, at ss/1 GHz, before ratifying 0010 (r7-q57)
- **PR #68**: sim: compare one-stage and widened two-stage delay taps at ss/1 GHz
- **PR #66**: Bump Repo Skills 0.25.1 -> 0.25.10

### 2026-11-06

- **Issue #63** (closed): Merge sim/lock-range into sim/false-lock: identical 2025-unit fleet grid simulated twice
- **PR #65**: refactor(sim): fold lock-range bench into false-lock to drop duplicate fleet grid
- **Issue #62** (closed): Redraw cp_bias and the CP dump follower to pass K1 and K5, then re-run sim/cp-currents
- **PR #64**: feat(design): redraw cp_bias and dump buffer to pass K1-K6; fix cp bench pwl extrapolation

### 2026-11-05

- **Issue #59** (closed): Dedupe copy-pasted smoke-bench summarize.py (lock-detector / supervisor)
- **PR #61**: refactor(sim): share one smoke-bench record grader
- **Issue #30** (closed): T1 item 1 (remainder of #24): run PFD fit gate, simulate CP, lock detector and supervisor
- **PR #60**: feat(sim): PFD fit gate and CP currents simulated; both fail, decision records 0011/0012
- **Issue #54** (closed): Draw the lock detector for spec row 12 (LOCK within 128 cycles, 20 fF load) and export it
- **PR #57**: feat(design): lock detector with window sampler, VCTRL movement sensor and 128-cycle filter
- **Issue #23** (closed): T1 item 1 (design sources): current-starved delay-line schematics, tap buffers and netlist on sg13_lv
- **PR #56**: docs: record delay-line sanity bench and propose one-stage tap fallback
- **Issue #53** (closed): Draw the false-lock supervisor (0005 parts 1 and 3, 0008 first-REF-edge mask) and export it
- **PR #55**: feat: draw false-lock supervisor with start-up REF mask and smoke bench

### 2026-11-01

- **Issue #49** (closed): sim: align dllbench run length and predicate window with the revised spec (PR #42)
- **PR #52**: feat(harness): derive bench run length per column from lock-time limit
- **PR #42**: docs: install two-key ratification trees and propose spec ratification (0009)
- **PR #51**: Bump Repo Skills 0.24.7 -> 0.25.1

### 2026-10-28

- **PR #47**: docs: add README Reproduce section and cite item-10 hygiene envelope
- **Issue #45** (closed): T1 item 10 (repo hygiene): cite the existing item-10 envelope in the manifest and give the README a true status and reproduce section

### 2026-10-27

- **PR #40**: build: pin klt to released klayout-tools 0.8.0 and regenerate signoff records
- **Issue #39** (closed): Bump klayout-tools pin fc02bdf0b6aa → 0.8.0
- **PR #7**: feat(signoff): add block manifest, committed klt signoff record and CI
- **Issue #5** (closed): Signoff scaffolding: block manifest, committed klt signoff record, and CI (T1 item 10)
- **PR #35**: fix: resolve repo symbols before stock xschem ones and declare delay-line item-1 inventory
- **PR #32**: feat(design): delay_cell/tap_buffer/delay_line sources, export gate and unrun sanity bench
- **PR #33**: feat(sim): DLL row benches, behavioural stand-in and testbench inventory
- **PR #31**: feat(design): PFD, charge pump, bias and loop filter on sg13_lv with staleness-checked exporter
- **Issue #24** (closed): T1 item 1 (design sources): PFD/CP redrawn on sg13_lv, loop filter, lock detector and dll_top schematic

### 2026-10-21

- **PR #19**: Bump Repo Skills 0.24.3 -> 0.24.7

### 2026-10-20

- **PR #8**: docs(spec): propose DLL target spec, decision records and corner set
- **Issue #2** (closed): Draft and ratify the target spec

### 2026-10-19

- **PR #16**: refactor(sim): share bench preflight and grade pdk-smoke via evidence.py
- **Issue #15** (closed): Consolidate duplicated sim preflight and envelope grader under sim/

### 2026-10-18

- **PR #12**: feat(sim): add grid harness for PVT, start-state and Monte Carlo sweeps
- **Issue #4** (closed): Simulation harness skeleton: klt sim corner runner, initial-condition axis and Monte Carlo mode (T1 item 9)

### 2026-10-17

- **PR #11**: docs(spec): disposition record for sg13g2-aib consumer requirements
- **PR #10**: Consumer requirements from sg13g2-aib: lock at 500/250 MHz, 16 phases per period, DCC scope
- **PR #9**: feat(sim): pin SG13G2 PDK, vendor OSDI build, add device smoke
- **PR #1**: chore(loom): Install Loom 0.19.1181
- **Issue #10** (closed): Consumer requirements from sg13g2-aib: lock at 500/250 MHz, 16 phases per period, DCC scope
- **Issue #3** (closed): Pin the SG13G2 PDK, port the OSDI build step, and commit a device smoke simulation
