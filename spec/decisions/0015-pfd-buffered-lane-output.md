# 0015 — PFD latch output moves behind a driver (`srlatch_buf`); the latch family and the gate are unchanged

- **Status**: proposed — becomes ratified only by the operator's approval and merge of the PR that carries this record. Agents do not approve it or mark anything ratified.
- **Date**: 2026-11-16
- **Decided by**: Builder agent, issue #140 (operator ruling 2026-11-15, attended `/fleet:decide` round 20261111-r14 q106: ratify a latch-family / edge-detector topology change — new 0006-style decision record, then redesign and re-run the gate; the (relax) and (fallback) options are declined)
- **Consumes**: [0011](0011-pfd-reset-path-too-slow-at-1ghz.md) (the two-knob refutation and the measured budget); [0006](0006-pfd-cp-reuse.md) (the fit gate); [0008](0008-false-lock-argument.md) (reset polarity); [0005](0005-false-lock-exclusion.md) (false lock)
- **Related**: #136/#113 (the chain and reset-path evidence this builds on); #151 (the follow-up that performs the redesign after this record is ratified)

## Decision

Keep everything 0006 adopted of the SR-latch + edge-detector PFD family and everything 0008 fixed of
its reset polarity, and change only the latch's **output and reset-tap wiring**. The new cell
`srlatch_buf` (defined in `design/tools/cells.py` in this record's PR; generated, not hand-drawn)
is the `srlatch_fast` core — same cross-coupled device-level 4u NAND pairs, same `XIS` `inv2x_lv`
set inverter and `XIR` `inv4x_lv` reset inverter — with:

1. **the lane output moved behind a driver**: `Q = inv4x(QB)`, sized for the 4 fF bench load
   (`LOAD_F` in `sim/pfd-fit/make_bench.py`), so no storage node drives the pad load;
2. **the internal nodes exposed for the reset tap**: `QB` is the lightly loaded internal complement
   (the driver's input) and `QN` is the internal storage node; the shared reset NAND keeps its
   inputs on the storage node (`QN`), not on the buffered `UP`/`DN`, so the driver's delay does not
   re-enter the reset path.

`edgedet` is untouched; the reset-path cells (`XNR` `nand2x_lv`, `XR1` `inv4x_lv`) are untouched;
`S`/`R` are still active high and `reset` is still NAND(UP,DN) delayed by one inverter.

**Nothing in the committed PFD moves in this record's PR.** `design/pfd.sch` still instantiates
`srlatch_fast`; `design/netlist/pfd.spice` and `sim/pfd-fit/decks/` are unchanged (the candidate is
kept unwired, its only consumer being the retained probe deck of the evidence section below, which
is the point of sequencing the ruling's two steps). The redesign of `design/pfd.sch` happens in
[#151](https://github.com/2AMLogic/sg13g2-dll/issues/151) after this record is ratified.

## The fit gate this redesign must meet (unchanged)

The gate is 0006's, criteria C1–C3 in `sim/pfd-fit/grade.py`, at both 1 GHz and the 500 MHz
fallback on the reduced corner set: C1 (response), for every graded |offset| ≥ 10 ps the ratio
`(wUP − wDN)/offset` stays inside its band around 1 (no dead zone); C2 (reset), at offset 0,
`MIN_RESET_S = 30e-12 ≤ min(wUP, wDN) ≤ MAX_RESET_FRAC = 0.25` of the period (250 ps at 1 GHz);
C3 (present), every tested offset has both an UP and a DN pulse measured — no missing series.
**This record changes no criterion in `sim/pfd-fit/grade.py` and no row of `spec/target-spec.md`.** The only failing cell of
the committed design is C2 at ss/1.080 V/125 °C (362..370 ps against the 250 ps cap,
`sim/pfd-fit/results/20261115T124912Z/fit-gate.md`); C1 and C3 pass at every corner at both
frequencies.

## The budget, from the committed anchors (all simulated, never measured)

Re-derived from the committed probe envelope
`sim/pfd-fit/results/20261115T125504Z/probe_ss.envelope.json` (ss/1.080 V/125 °C, settled offset-0
cycles; crossings at Vdd/2, referenced to the input edge):

| anchor | value | source |
|---|---|---|
| `up` rises | +264.6 ps | same envelope |
| edgedet set pulse ends (`set_up` falls) | +288.7 ps | same envelope |
| reset path (`up`/`dn` → `reset` rises) | 167.2 ps | `path` = reset rise − up rise, same envelope |
| release path (`reset` rises → `up` falls) | 194.9 ps | `release` = up fall − reset rise, same envelope |
| **C2 width** = path + release | **362.1 ps** | `width` = up fall − up rise, same envelope; cap 250 ps |

Two identities, by arithmetic from these anchors:

- **What must be shed**: `path + release ≤ 250 ps` — the loop must lose **≥ 112.1 ps jointly**.
  C1's structural floor additionally needs the reset to arrive no earlier than the set-pulse end,
  i.e. `path ≥ 288.7 − 264.6 = 24.1 ps`.
- **The window is `250 − release − 24.1`**, not a fixed 31 ps: the ruling's "~31 ps" is the window
  at today's 194.9 ps release. Every picosecond taken off `release` buys a picosecond of reset-path
  window **and** a picosecond of C2 margin. Equivalently, the smallest width the committed
  structure can emit is `24.1 + 194.9 = 219.0 ps` — only 31 ps under the cap with the reset timed
  perfectly. 0011 measured the reset path alone at 167.2 ps against a 55.1 ps window ceiling (a 3x
  gap) and found the sizing space floor-bound: the release leg is the term to attack, which is what
  the decision above attacks (the 4 fF bench load leaves the storage node, and the driver's edges
  are common to both lane transitions).

## Headroom evidence: one retained single-corner ss probe of the candidate

**Record**: `sim/pfd-fit/results/20261116T012100Z/` — `requests/probe_ss.request.json`,
`decks/probe_ss.spice` (with the `decks/pfd.spice` copy it ran against),
`probe_ss.envelope.json`, `probe_ss.stderr`, and the staged `corner.cir` under `artifacts/`.

**Method** (per CLAUDE.md, every number states how it was produced): single corner
`mos_ss/1.080 V/125 °C`, `tran 5p 25n`, ngspice 47, `klt sim … --backend local` (single unit, local
run, no job id — the envelope's `environment`/`provenance` carry the engine and PDK hashes), klt
`0.9.3.dev16+gdcf18e2e0c03`, PDK `ihp-sg13g2` fetched 0.3.0. Deck stimulus byte-identical to
`sim/pfd-fit/decks/pfd_1g.spice` (same `Vrefn`/`Vfbn` PWL lines, same 4 fF `Cup`/`Cdn` bench
loads); the DUT is `pfd_buf`, defined inline in the deck, wiring the committed `edgedet`,
`nand2x_lv` and `inv4x_lv` (from the `pfd.spice` copy) around the inlined `srlatch_buf` — the
`klt netlist design/srlatch_buf.sch --block` export of the `cells.py` cell, verbatim. Crossings on
`ref`/`fb`/`up`/`dn` plus the PFD-internal `set_up`/`set_dn`/`reset` and the new latch-internal
`up_qn`/`up_qb`/`dn_qn`/`dn_qb`, all at Vdd/2. Reduction as in every record of this bench:
`width = up_fall − up_rise`, `path = reset_rise − up_rise`, `release = up_fall − reset_rise`, on
settled offset-0 cycles; cycle 0 is a warm-up cycle and is excluded from the quoted figures (it
reads 208.1 ps, ~2.9 ps wider than the settled cycles, exactly the effect the records exclude).

**Result at ss/1.080 V/125 °C, offset 0, settled cycles** (all six settled offset-0 cycles of the
run — 1, 2, 9, 16, 17, 18 — agree; both lanes match within 0.6 ps):

| quantity | candidate | committed (0011 anchors) | budget |
|---|---|---|---|
| `path` (up rise → reset rise) | **30.8 ps** | 167.2 ps | ≥ 24.1 ps floor |
| `release` (reset rise → up fall) | **174.4 ps** | 194.9 ps | — |
| **C2 width** = path + release | **205.2 ps** (205.2..205.3 across cycles) | 362.1 ps | **30..250 ps: PASS, 44.7 ps margin** |

Internal anchors of the same cycle, which is where the margin came from and why C1's ordering
still holds: the storage node `up_qn` rises **+258.9 ps** — the flip happens **29.8 ps inside** the
set pulse (set pulse ends +288.7 ps; the committed design flipped 24.1 ps inside); the reset rises
**+416.2 ps**, i.e. **127.5 ps after** the set pulse ended (C1's structural requirement); the
internal release leg (`reset` → `up_qb` rise) is **123.8 ps** — the complement node now charges
only gate inputs instead of switching the 4 µm discharge stack behind a 4 fF load — and the driver
adds **50.6 ps** on the output fall and **44.0 ps** on the output rise (crossing `up_qb` at
+341.4/+540.0 and `up` at +385.4/+590.6). The driver's rise delay shifts the lane's visible rise
late (UP rises +385.4 ps, after the set pulse has ended) and so also subtracts from the
UP-referenced path: this is why the identities of the budget section, which are anchored to the
committed design's UP timing, transfer to the internal nodes, and why C2's UP-referenced width is
the quantity the gate actually grades.

**What this probe does not establish**: C1's ratio tracking `(wUP − wDN)/offset ≈ 1` — the probe is
one corner at offset 0 only. The full-gate re-run over the reduced corner set at both frequencies
is [#151](https://github.com/2AMLogic/sg13g2-dll/issues/151)'s deliverable; this record's claim is
the narrower one, that the ss budget the redesign must hit is **reachable** with retained,
reproducible evidence.

**Retention statement**: this issue probed exactly one candidate configuration, the one decided
above, and retains it whole. No other sizing variant was probed in this issue and none is cited
from elsewhere: 0011's unretained exploratory rows are the practice this record corrects, per the
ruling's "retain the sizing-probe records this time".

## Alternatives, disposed

- **Reset-dominant discharge device on `UP`/`DN`** (a wide NMOS gated by `reset`): rejected — the
  output stays a storage node and gains a contention/glitch path against the latch's own pull-up;
  the same load the decision removes from the storage node would sit on a fighting pair.
- **DFF-based tri-state PFD** (`dffr_lv` exists): rejected — it departs from the topology 0006
  adopted, so `reuse.lock.json`'s `pfd` could no longer reach `kept` as an adopted redraw; it
  re-opens the 0005/0008 false-lock and dead-zone argument from scratch; and `dffr_lv` as committed
  (1u/1.5u NAND master-slave) has its own ss `CK→Q` and `CLRB→Q` paths that are unlikely to fit the
  budget without their own redesign.
- **Shorten `edgedet` again** (2-stage, RC one-shot): rejected — #136 already took this knob
  (5 → 3 stages, ~59.7 ps/stage measured) and it opened the window without closing the width; it
  spends the 29.8 ps flip margin and carries the blast radius below.
- **Relax C2 at ss, or accept the 500 MHz fallback**: **declined by the 2026-11-15 operator
  ruling** on #140, not re-argued here. No agent relaxes 0006.

## Consequences

- **(a) `reuse.lock.json`**: the `pfd` entry **stays `adopting`** through this record — 0006's path
  to `kept` requires the fit gate to pass, and the redesign has not run the gate yet. When
  [#151](https://github.com/2AMLogic/sg13g2-dll/issues/151)'s re-run passes, the entry becomes
  `kept` with `differs` updated to name `srlatch_buf` and this record; if the re-run fails, the
  failure is a new decision record, not a silent patch (0006). The `cp` entry's `fit_gate` note
  cites the same open gate and updates with it.
- **(b) 0005/0008 re-argued, not assumed**:
  - *Reset polarity (0008)*: unchanged in kind — `S`/`R` are still active high, `reset` is still
    NAND(UP,DN) delayed by one inverter, active high into `R`. The NAND's inputs move from the
    buffered `UP`/`DN` to the storage node `QN`, which is the same node of the same latch core the
    committed design taps, minus the pad load; the polarity and the sibling-control argument of
    0008/0011 (the sibling's active-low two-inverter reset fails C1 on these lv cells) are not
    touched by that.
  - *False lock (0005)*: 0005's argument lives in the start-up state, the supervisor's window
    detector and the lock detector — none of which this record touches. What changes on the PFD is
    a **common-mode, symmetric** delay on both lane outputs: the driver shifts `UP` and `DN` by the
    same amount, so the phase *difference* the loop consumes is preserved; the re-run's C1 ratio
    grading at ±160 ps is the check that this holds in simulation, and #148's supervisor/lock-
    detector ss failures are a separate block, tracked there.
- **(c) The `ctl_1g` control arm**: `SIBLING_POLARITY` in `sim/pfd-fit/make_bench.py` is a
  hand-written `pfd_sib` subcircuit that hard-codes `srlatch_fast`'s cell name and six-pin port
  order. In this record's PR the decks are frozen and the control keeps grading `srlatch_fast` —
  correct, since the committed PFD still uses it. #151 must resolve the arm when it rewires `pfd`:
  either keep `srlatch_fast` defined in `design/netlist/pfd.spice` for the control while `pfd`
  instantiates `srlatch_buf`, or redefine `pfd_sib` around the new latch — and regenerate the
  committed decks. If it misses this, `make_bench.py --check` (run by `run.sh`) fails, or worse the
  control silently keeps grading the old latch.
- **(d) `edgedet` blast radius**: resolved — this record does not touch `edgedet`. The chain is
  instantiated by `pfd.sch`, `supervisor.sch` and `lock_detector.sch` (a change would have needed a
  PFD-local fork or a re-verification of the other two blocks, per the #141 → #148 precedent);
  `srlatch_fast`/`srlatch_buf` are PFD-local, so this change is contained.
- **The follow-up**: the redesign of `design/pfd.sch`, the full `sim/pfd-fit/run.sh` re-run, and
  the `reuse.lock.json`/`design/NOTES.md` updates are
  [#151](https://github.com/2AMLogic/sg13g2-dll/issues/151), filed parked on #140. It also checks
  one probe-vs-gate caveat: the retained probe ran the candidate unwired (deck-inline `pfd_buf`);
  after the rewire, the in-`pfd` netlist must reproduce the probe's figures on the identical deck
  stimulus.

## What does not happen here

- No `RATIFY-KEY` verdict is posted by this record's authors: both keys must come from identities
  that did not author the PR (`ratification/ee-key/SKILL.md` § "Non-author enforcement", 0009
  decisions 3–4), and the operator's approval of the PR is the ratification.
- No criterion of `sim/pfd-fit/grade.py`, no spec row, no committed deck, and no committed
  schematic changes in this record's PR; `sim/` receives only the new append-only
  `results/20261116T012100Z/`.
