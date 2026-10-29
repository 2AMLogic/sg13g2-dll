# Work Log

Chronological record of merged PRs and closed issues. Maintained by the Guide role.

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
