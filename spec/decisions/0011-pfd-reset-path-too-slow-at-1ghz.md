# 0011 — PFD fit gate fails at 1 GHz (reset pulse too wide); `pfd` stays `adopting`

- **Status**: proposed (needs a follow-up issue; the spec is not changed here)
- **Date**: 2026-11-05
- **Decided by**: Builder agent, issue #30
- **Related**: 0006 (the gate), 0008 (reset polarity, "PFD redraw"), 0007 (lv devices)

## Finding (simulated, never measured)

`sim/pfd-fit/results/20261105T125120Z/fit-gate.md` (batch fleet, ngspice 46, jobs
`klt-sim-eb16fa919cbc` / `klt-sim-c9bb349b8d7c` / `klt-sim-937e4b7536d6`; reduced corner
set; criteria C1-C3 unchanged from `sim/pfd-fit/grade.py`).

- **C1 (no dead zone above 10 ps) and C3 pass** at every corner at both frequencies:
  (wUP - wDN) tracks the input offset to within about 1 ps down to the +-5 ps points.
- **C2 (reset-pulse width 30 ps .. 0.25 T) fails at 1 GHz** in two of three corners:
  tt/1.2 V/27 C 296..300 ps and ss/1.08 V/125 C 472..478 ps against the 250 ps limit; ff/1.32 V/-40 C
  passes (197..199 ps). At 500 MHz (limit 500 ps) all three corners pass.
- The reset pulse is set by the NAND + three-inverter reset path, not by the frequency, so the
  same 300 ps (tt) is simply a larger fraction of T at 1 GHz (30 % tt, 47 % ss).
- **Control (`ctl_1g`, sibling reset polarity on the same lv cells)** fails C1 at all three corners
  ((wUP - wDN)/offset between -0.33 and +0.15, i.e. no usable phase response). The 0008 claim that
  the sibling's NAND + two-inverter reset does not work holds on these cells. This confirms the
  reading in 0008; it is not a statement about the sibling's own (hv) implementation.

## Consequence

`reuse.lock.json` `pfd` stays `adopting`. 0006 makes a gate failure a new decision record, not a
silent patch; this is it. No schematic or spec row changes here.

## Proposal (for a follow-up issue; not simulated)

Shorten the reset path so the pulse falls inside 30 ps .. 250 ps at ss/1.08 V/125 C as well. Options,
in the order I would try them: (1) size up the reset-path inverters / the NAND (keeps the three-inverter
polarity of 0008); (2) a faster NAND + one-inverter or AND-type reset, which keeps the polarity the
control showed is needed but must be re-checked against C2's 30 ps floor at ff; (3) keep the cell and ask
for a ratified relaxation of C2 for ss (the gate is fixed by 0006 and agents do not relax it). The 500 MHz
fallback target already passes unchanged. Any redraw re-runs `sim/pfd-fit/run.sh`.

## Update 2026-11-15 (issue #113): both proposed redraws ran; neither closes C2 at ss with C1 intact

- **Status of this record**: the sections above are unchanged; this section appends the simulated outcome
  of the follow-up issue. All figures below are simulated, never measured. Criteria C1-C3 are unchanged
  (`sim/pfd-fit/grade.py`); C2 was **not** relaxed.

Three gate runs now exist, all on the batch fleet, ngspice 47, reduced corner set:

1. **2026-11-05** (`results/20261105T125120Z`, the finding above): reset path NAND + 3 inverters on the
   shared `srlatch`. C1/C3 pass everywhere; C2 fails at 1 GHz tt (296..300 ps) and ss (472..478 ps).
2. **2026-11-15, option (2) + sized cells** (`results/20261115T001809Z`, jobs `klt-sim-42d4f35cd4e9` /
   `klt-sim-1934c6f376e3` / `klt-sim-0f13684829b1`): reset path NAND + 1 inverter on PFD-local
   `nand2x_lv`/`inv4x_lv` and `srlatch_fast` (the `srlatch` topology with 2x NANDs and a 2x R-inverter);
   seven loop stages shortened to five. **C1/C3 pass at every corner at both frequencies.** C2 passes at
   tt (223..226 ps), ff (150..152 ps) and at 500 MHz everywhere (limit 500 ps); **C2 still fails at
   ss/1 GHz: 352..358 ps.** This is the committed design.
3. **2026-11-15, three-gate reset loop** (`results/20261115T003632Z`, jobs `klt-sim-dc27f9cf6ad5` /
   `klt-sim-58c1ccea779c` / `klt-sim-69be85c983ed`): an active-low-RN latch variant fed directly from
   NAND(UP,DN) (loop of three gates), probed first at ss with a single-corner local run (228.5 ps at
   offset 0). On the full grid it reached **C2's width target** at tt (138..139 ps), ff (93..94 ps) and
   ss in settled cycles (229..235 ps) — but **fails C1 at tt, ss and ff at both frequencies**
   (ratios 0.21..0.22 at +10 ps and 1.5..1.9 in the -10..-40 ps band). It is recorded as evidence, not
   adopted; `srlatch_fast`'s committed form is the variant in run 2. At ss an unsettled start-up cycle
   also produced no UP pulse at all (width 0), which alone fails C2's 30 ps floor.

One change of character in run 2's record worth naming: its `ctl_1g` control at tt produced **no UP/DN
pulse at all** (width 0, both lanes, every cycle) where the 2026-11-05 control gave ~145..153 ps pulses
failing C1 on insensitivity. The widened `srlatch_fast` NANDs hold the latch reset against the edgedet
set pulse under the sibling's active-low polarity. It is still a C1 failure (AC3's revised requirement
holds); it demonstrates a stuck-reset corner, not a dead zone, and is not a broken deck.

### Why the two criteria fight (simulated anchors, no new model)

The UP/DN pulse ends when both the lane's own set pulse has ended *and* the shared reset has propagated.
The probe record `results/20261115T081500Z` (single ss/1.08 V/125 C corner of run 2's deck, byte-identical
to that record's `decks/pfd_1g.spice`; the PFD-internal nodes `set_up`/`set_dn`/`reset` probed alongside
`ref`/`fb`/`up`/`dn` in `probe_ss.envelope.json`) anchors both chains at ss, per input edge:

- The edgedet pulse ends at **+347 ps**: set_up/set_dn fall 346.8..346.9 ps after the edge, both lanes,
  every cycle of the probe; the lane itself rises at ~+260 ps.
- The shared reset rises **+413 ps** after the edge at offset 0 — +396.4..+560.5 ps across the +-160 ps
  sweep, tracking the offset because it fires on NAND(UP,DN) — so at offset 0 it arrives ~66 ps *after*
  the set pulse has already ended.
- The pulse therefore ends on the latch's reset path, not at set release: UP/DN falls 196.7..203.2 ps
  after reset rises, in every cycle of the probe. That pins the width at reset arrival minus the lane
  rise: **352.6..357.9 ps at offset 0** — run 2's C2 figure.

This also reads run 3 without new machinery: its three-gate reset arrives before the set pulse ends, so
the pulse end moves to the latch's set-release path and the width stops tracking the offset — exactly
its committed ss record (near-constant 229..235 ps widths, the C1 ratios above). The two criteria cross
at the set-release time: C1 needs the reset to arrive after the set pulse ends (>= ~+347 ps at the
graded offsets), while C2 needs the pulse to end within 250 ps of the lane rise, i.e. the reset to
arrive by ~+310 ps (250 + ~260 lane rise - ~199 latch reset path). +347 > +310, so no reset-path sizing
closes ss, and shortening the loop trades C1 failure for C2 progress. Closing ss needs a shorter
edge-detector pulse or a different latch family — **a PFD topology change, not a reset-path redraw** —
and is out of this issue's scope.

### Consequence and paths forward (a human decides; no agent relaxes 0006)

- `reuse.lock.json` `pfd` stays `adopting` (0006's path to `kept` requires the fit gate to pass).
- The committed design (run 2's cell set) passes C1/C3 and C2 everywhere except ss/1 GHz; the 500 MHz
  fallback target passes the whole gate unchanged.
- Option (3) of the original proposal — a ratified ss-specific relaxation of C2 — and the topology
  change sketched above both need human ratification and a new decision record; neither is done here.


### Update 2026-11-15 (issue #136): the edge-detector chain knob, measured — the window it opens at ss is unreachable by the reset path

- **Status of this record**: appends the simulated outcome of the chain-length experiment the
  2026-11-15 curator rescope of #136 proposed. All figures are simulated, never measured.
  Criteria C1-C3 are unchanged (`sim/pfd-fit/grade.py`); C2 was **not** relaxed.

**What was built.** `design/edgedet.sch` shortened from a five-inverter to a **three-stage
device-level chain (0.16u channels, odd count preserved)**, moving the ss set-pulse end from
**+346.9 ps to +288.7 ps** (-58.2 ps; the rescope's ~+247..255 estimate extrapolated the old
chain's ~49.9 ps/stage (249.5 ps / 5), but the shorter chain measures ~59.7 ps/stage
(179.1 ps / 3, `results/20261115T125504Z`), which is why the end landed at +288.7 rather
than inside the estimated range). The shorter set pulse does not flip the committed
`srlatch_fast` at ss — XIS (`inv_lv`) crosses the NAND's NMOS threshold ~86 ps after the set
edge and Q peaks at ~0.75 V and collapses without latching (no reset ever fires) — so the cell
was redrawn with **device-level 4u NAND2 gates and a 2x S-inverter** (`XIS inv2x_lv`) and the
R-input inverter was upsized **`XIR inv2x_lv` -> `inv4x_lv`**; the reset-path cells `nand2x_lv`
(XNR) and `inv4x_lv` (XR1) are unchanged. Both `edgedet` and `srlatch_fast` instantiate raw
`sg13_lv_{pmos,nmos}` devices rather than a sized cell library part: the ss set pulse needed
per-device widths (0.16u chain devices, 4u NAND stacks) no library cell offers, and inlining
kept the flip tunable without adding new symbol cells — the cost, lost hierarchy for the later
layout matching and LVS work, is deferred with that work. With this,
the PFD produces clean, offset-tracking pulses again: the probe record
`results/20261115T125504Z` and gate record `results/20261115T124912Z` show **C1 ratios
1.00..1.05 at every corner at both frequencies** — better tracking than run 2.

**Gate result (`results/20261115T124912Z`, batch fleet, ngspice 47, jobs
`klt-sim-3f16b4237455` / `klt-sim-b447e41afeff` / `klt-sim-8f492193fe10`):**

- `pfd_1g`: tt **PASS** (229..233 ps), ff **PASS** (154..157 ps), **ss FAIL** — C2 width
  **362..370 ps** against 30..250 ps. **C1/C3 PASS at every corner** — ss is again the only
  failing criterion, exactly as in run 2.
- `pfd_500m`: **PASS** at tt, ss and ff.
- `ctl_1g`: **FAILS C1 at every corner** (tt/ff zero-width pulses as in run 2; ss 142..143 ps
  pulses with ratios -0.19..0.12). 0008's reset-polarity argument is unchanged.

**Why ss still fails — the two-knob argument, now measured on both knobs.** The chain change
does exactly what the rescope predicted: it moves C1's floor under C2's ceiling, opening a
window. With the probe/gate anchors at ss (offset-0, settled cycles): set pulse ends
**+288.7 ps**; the lane rises **+264.6 ps** (flip F = 155.0 ps, 24.1 ps inside the set pulse);
the latch release path is **194.9 ps** (UP falls 194.9 ps after the shared reset rises). C1
needs the reset to arrive at or after **+288.7 ps**; C2 caps the width at 250 ps, i.e. the
reset must arrive by **UP_rise + (250 - 194.9) = +319.7 ps**. The window
**[+288.7, +319.7] is 31 ps wide — it exists**. The reset arrives at **+431.8 ps**:
`path` (NAND(UP,DN) -> XR1 -> reset) = **167.2 ps**, and the window needs path <= **55.1 ps**.

The reset-path sizing space was then probed end to end (every variant at ss, offset 0). **Only
the committed-config row below has a retained record** (`results/20261115T125504Z`); the other
rows come from exploratory probes whose decks and envelopes were not retained, so they are
recorded here as observed trends, not reproducible evidence. The last row in particular is
flagged rather than asserted: `XIR` is a load *downstream* of `reset`, so 2x instead of 4x
should unload the net and make `path` *smaller*, yet it was observed slower than row 2 — with
no committed envelope there is no way to tell an effect from a transcription slip:

| reset-path sizing | path (ps) | note |
|---|---|---|
| XNR `nand2x_lv` 2u + XR1 `inv4x_lv` (committed cells) | 167.2 | as-built; **committed** record `results/20261115T125504Z` |
| XNR 6u + XR1 `inv4x_lv` at 8u/4u | ~149 | observed fastest; record not retained |
| XNR 6u + XR1 8u/4u + XIR 2x | ~169 | record not retained; flagged as physically surprising, unverifiable |

The refutation does not rest on the unretained rows: the committed as-built figure alone
carries it — `path` = **167.2 ps** against the **55.1 ps** window ceiling, a **3x gap**
(`results/20261115T125504Z/probe_ss.envelope.json`). The floor is structural at ss/1.08
V/125 C: `path` is two ss gate delays (the NAND discharge of `reset_n0` into XR1's input gate,
then XR1's rise into the two latch R-input inverter gates), each 35..90 ps at these loads.
The exploratory probes (records not retained, same caveat as the table) suggested the space
has no deep win: widening XNR beyond ~6u is self-defeating because its input gates sit on the
UP/DN nodes and each +2u of NAND width pushes the flip F past the set-pulse end (XNR 6u ->
F 163.7, margin 15.3 ps; 4u-6u NANDs *inside* `srlatch_fast` (6u..8u devices, and a buffered-Q
variant) all drove F to or past the set-release edge — the latch then fails to latch and the
widths stop tracking the offset, run 3's failure mode). The latch release floor is pinned by
committed evidence too: UP falls when XNQ discharges the ~5 fF UP node (including the bench's
4 fF) through a stack that must stay 4u for the flip, plus XNQB and XIR — **194.9 ps** in the
committed probe (`results/20261115T125504Z`), the release leg of the same anchors above.

So: `path` = 167.2 ps **as committed as-built** (and, taking the unretained probes at face
value, >= ~149 ps anywhere in the explored sizing space; structurally bounded below ~100 ps)
against a window ceiling of **55.1 ps** — **C1 and C2 remain jointly unsatisfiable at ss at
1 GHz within the ratified latch family and the reset-path sizing space**. The impossibility
claim spans both knobs (chain length *and* reset path): the chain result is committed
end to end, and the reset-path result stands on the committed as-built measurement, with the
sizing probes recorded as unretained corroboration. The chain change stands as a real
improvement — it is what moved the window into existence, and it widened the ff and tt
margins — but it does not close ss. Per 0006, the operator decision is filed as **issue #140** with the ranked
options (latch-family topology change / ss-specific C2 relaxation / accept the 500 MHz
fallback); C2 was **not** relaxed here, and `reuse.lock.json`'s `pfd` entry stays `adopting`.

### Update 2026-11-16 (issue #140): the ruling chose the topology change; see 0015

The 2026-11-15 operator ruling on #140 declined the C2 relaxation and the 500 MHz fallback and
directed a latch-family / edge-detector topology change. That decision record is
[0015](0015-pfd-buffered-lane-output.md) (ratifiable, with a retained ss headroom probe of its
`srlatch_buf` candidate: width 205.2 ps at ss offset 0 against the 250 ps cap,
`sim/pfd-fit/results/20261116T012100Z`); the redesign and the full-gate re-run are follow-up
#151, after 0015 is ratified. Nothing above is rewritten by it; this record stands as the
evidence the ruling built on.
