# sg13g2-dll — agent instructions

Open-source canary block: a delay-locked loop on IHP SG13G2, a 130 nm SiGe
BiCMOS open PDK, designed and verified by AI agents. **Analog.** A new block,
not a port.

- **PDK**: IHP SG13G2 (open PDK, IHP-GmbH/IHP-Open-PDK). Open-source flow:
  xschem + ngspice for design and simulation; layout, DRC, and LVS through
  klayout-tools (`klt`).
- **Lock to one period is the point, and the risk.** A DLL loop has no
  frequency acquisition: it can lock to two periods, or drive the delay line
  to a rail and stay there. The false-lock argument — start-up state,
  delay-range limits, and how harmonic lock is excluded — is written into a
  decision record before the schematic is sized, and a testbench proves it
  from every start state at every corner. A design that locks only from a
  friendly initial condition has not locked.
- **Phase accuracy is a layout property.** Phase spacing comes from matched
  delay cells and matched loads. Draw the delay line as a symmetric array,
  extract it, and grade phase spacing post-layout. Expect the tools to be
  weakest at matched placement and extraction of a regular array, and file
  accordingly.
- **Scope discipline.** `sg13g2-pll` on this PDK already designs a
  phase-frequency detector and a charge pump. Adopt them or record why not
  (`reuse.lock.json` and a decision record) — do not size a second one by
  accident. The two blocks are not duplicates: a PLL and a DLL share
  sub-blocks, not a loop. Do not build a frequency synthesizer or a
  reference oscillator here; the input clock is a source at the boundary.
- **Jitter needs its method.** ngspice has no periodic-noise analysis. Every
  jitter number states the method that produced it (transient noise, run
  length, seeds, estimator) next to the number. A jitter figure without its
  method is not a result.
- **Friction protocol (the canary's job)**: every time klayout-tools is
  awkward, missing a capability, or wrong for what you need, file an issue at
  `2AMLogic/klayout-tools` describing the tool gap generically — that tracker
  is scoped to the tool, so keep design-specific detail out of it and describe
  the gap, not the design.
- **Verification is the product**: no claim without a testbench. PVT corners
  on every recorded result; `sim/` results are append-only evidence. A
  simulated number is never called measured.
- Spec changes go through `spec/` with a decision record; agents do not relax
  the ratified spec to make results pass.
- **1 GHz is the target.** 500 MHz is the fallback and 2 GHz a stretch. Do
  not let 2 GHz drive the architecture before 1 GHz closes.

<!-- BEGIN LOOM ORCHESTRATION -->
This repository uses [Loom](https://github.com/rjwalters/loom) for AI-powered development orchestration — see the Loom repository for the full guide (roles, labels, worktrees, configuration). When installed, Loom also writes a locally-substituted copy of that guide to `.loom/CLAUDE.md`.

Work is coordinated through `loom:` labels on issues and pull requests, and the same roles run either under `loom-daemon` or by hand in an attended session — daemon mode is optional. Create the labels once with `.loom/scripts/sync-labels.sh` (an install ships `.github/labels.yml` but does not create the labels on the forge). A pull request ready for review carries `loom:review-requested`; Judge reviews it and applies `loom:pr` (approved) or `loom:changes-requested`; Doctor fixes a `loom:changes-requested` pull request and returns it to `loom:review-requested`. Only a `loom:pr` pull request gets merged, and always via this repo's merge script (`.loom/scripts/merge-pr.sh`) — never a raw forge merge command such as `gh pr merge`. Full state machine: `.loom/docs/label-state-machine.md`.
<!-- END LOOM ORCHESTRATION -->

<!-- BEGIN REPO-SKILLS -->
This repository has [Repo Skills](https://github.com/rjwalters/repo) v0.24.7 installed —
general repository hygiene and environment commands invoked as `/repo:<command>`. Run
`/repo:help` for the command list, or see `.claude/skills/repo/SKILL.md` for the full
guide. Hygiene commands apply safe, reversible fixes by default and report each
change; run with `--ask` to review first, and `--prune` to allow irreversible
removals. Managed by `install.sh` — edit outside the markers only.
<!-- END REPO-SKILLS -->
