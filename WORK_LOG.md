# Work Log

Chronological record of merged PRs and closed issues. Maintained by the Guide role.

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
