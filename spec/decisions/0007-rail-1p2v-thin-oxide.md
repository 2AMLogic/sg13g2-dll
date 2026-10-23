# 0007 — Rail moved to 1.2 V thin-oxide; consumer reconciliation; output load

- **Status**: proposed (ratified with 0001)
- **Date**: 2026-10-20
- **Decided by**: operator (rjwalters), attended `/fleet:decide` session on
  PR #8, 2026-10-20, question 4 answered **1** (reviewer's call A: 1.2 V lv
  rail; with calls C and F, then ratify). Written up by the independent review
  session that posted the review on PR #8.
- **Supersedes**: 0001 decision 2 (rail and device flavor) and the voltages in
  0001 decision 7. **Amends**: 0004 (device family), 0006 (how the PFD and
  charge pump are adopted), `sim/corners.json`, the README table.
- **Related**: 0002 (consumer requirements G1–G5), 0005

## Decisions

| # | Question | Decision |
|---|---|---|
| 1 | Rail and device flavor | **1.2 V thin-oxide CMOS (`sg13_lv_nmos` / `sg13_lv_pmos`) throughout**; nominal 1.20 V, tolerance ±10 % (**1.08 – 1.32 V**); no SiGe HBT (unchanged) |
| 2 | Corner set | 5 MOS × 3 supply × 3 temperature = 45, now `mos_tt/ss/ff/sf/fs` of `cornerMOSlv.lib` × 1.08 / 1.20 / 1.32 V × −40 / 27 / 125 °C. The 3.63 V hv corner is gone with the rail. |
| 3 | 0002 G1 | **Accepted**: the 500 MHz fallback point carries a **±20 %** lock range (400 – 600 MHz); row 2's fallback column changes from ±10 % to ±20 %. The target (1 GHz ±20 %) and stretch (±40 %) columns are unchanged. One continuous range over 500 MHz and 1 GHz is still declined (2:1 span). |
| 4 | 0002 G2 | 8 phases at target, 16 at stretch, **kept**. The consumer's 16-at-target is met only by the stretch column; declined at target. `sg13g2-aib`'s 0014 shows 16 does not close their budget either, so the next move is theirs. |
| 5 | 0002 G4 | **Accepted** — decision 1 above is that rail. |
| 6 | 0002 G5 | **Accepted**: a lock-status output is added as spec row 12 and an interface item. 0005's supervisor already needs a lock detector. |
| 7 | Output load (review call F) | Every tap drives a **fixed 20 fF capacitive load** to VSS in every graded testbench; see "Output load" below. |

## Why 1.2 V (decision 1)

The reasoning that chose 3.3 V in 0001 was reuse: the sibling PFD and charge
pump are drawn on `sg13_hv_*`. The review found three facts that outweigh it,
all from sources in the tree or the pinned PDK:

1. **Rating.** The pinned PDK rates the hv devices at "VGS ≤ 3.3 V (Maximum)
   @ 27 °C" (`SG13G2_os_process_spec.pdf` Rev. 1.2 §2.4–2.5) and the hv model
   header states "Maximum drain-source voltage: 3.3" (`cornerMOShv.lib`). The
   spec's +10 % corner (3.63 V) was above both. The lv devices are rated
   "VGS ≤ 1.65 V @ 125 °C" (§2.1–2.2) with a model maximum drain-source voltage
   of 1.5 V (`cornerMOSlv.lib`); 1.2 V + 10 % = 1.32 V is inside both.
2. **Speed.** A tap at 1 GHz is 125 ps and must reach 104 ps at the slow corner
   (0004). This repo's pdk-smoke (`sim/pdk-smoke/results/20261017T220308Z/`)
   measured minimum-size *unstarved* inverters at tphl / tplh = 87 / 178 ps
   (hv, mos_ss) against 40 / 60 ps (lv, mos_ss), 27 °C, nominal rail, 5 fF,
   100 ps edges. Current starving only adds delay. The hv path was unlikely
   to reach 1 GHz; the lv path has roughly 2–3× the headroom.
3. **Consumer.** 0002 accepted `sg13g2-aib`'s G4 (1.2 V ±10 %, thin-oxide,
   −40…125 °C) as the input to the supply row.

Rejected again: a mixed rail (lv delay line, hv charge pump) — level shifters
in the clock path add matched-load asymmetry (0001's argument stands).

### PDK facts for the lv rail (read at IHP-Open-PDK `v0.3.0`, `sim/pdk.json`)

- `ihp-sg13g2/README.md`: "A thin gate oxide for the 1.2 V digital logic and a
  thick oxide for a 3.3 V supply voltage."
- `libs.tech/ngspice/models/cornerMOSlv.lib` header: "Maximum drain-source
  voltage: 1.5"; "Valid range for model: L = (0.13 - 10)um, W = (0.15 - 10)um";
  sections `mos_tt`, `mos_ss`, `mos_ff`, `mos_sf`, `mos_fs` (plus `*_mismatch`,
  `mos_tt_stat`), the same names as the hv library.
- `libs.doc/doc/SG13G2_os_process_spec.pdf` Rev. 1.2 §2.1 NMOS / §2.2 PMOS:
  "VGS ≤ 1,65 V @ 125°C"; temperature coefficients extracted for
  −40 °C < T < 125 °C (§1); NMOS Miller capacitance 0.32 – 0.40 fF/µm,
  junction capacitance 0.9 – 1.0 fF/µm².

## What the rail change touches, and what it does not

| Item | Change | Forced by the rail? |
|---|---|---|
| Row 9 supply | 2.97 / 3.30 / 3.63 V → 1.08 / 1.20 / 1.32 V; `sg13_hv` → `sg13_lv` | yes |
| Row 6 jitter corners | tt / 1.20 V / 27 °C; ss / 1.08 V / 125 °C; ff / 1.32 V / −40 °C | yes (voltages only) |
| Row 10 power | **limit kept at ≤ 5 / 10 / 2 mW**. Dynamic power scales with V², so the same limit is about 7.6× looser at 1.2 V; it is kept because no sizing exists to justify a tighter number. Revisit with the first power result. | no (noted, not changed) |
| Edge threshold | "VDD/2" now means 0.60 V nominal, scaled per corner | yes (wording only) |
| Locked predicate Vctrl ripple < 5 mV pp; row 8's 50 mV rail exclusion | kept; both are now a larger fraction of the control range (≈ 4 % of a 1.2 V rail for 50 mV). 0004 adds a control-voltage margin requirement so a legitimate lock cannot sit in the exclusion zone. | no (noted) |
| 0004 device family | `sg13_hv_*` → `sg13_lv_*`; model-valid L ≥ 0.13 µm, W ≥ 0.15 µm | yes |
| 0006 PFD / charge pump | still **adopt**, but as **topology redrawn on `sg13_lv_*`**, not a byte-identical stamped copy; the fit gate (1 GHz across the corner set) is unchanged. The `reuse.lock.json` entries stay `in_tree` / `adopting`; when the redrawn cells land they become `kept` with a decision record naming the sibling as the source of the topology, since a redrawn cell is not a vendored file. | yes |
| 0005 mechanism | unchanged by the rail | no |
| Lock range, phases, spacing, static error, jitter limit, lock time | unchanged | no |

## Output load (decision 7)

Every tap output drives **20 fF to VSS** in every graded testbench (rows 4, 5,
6, 10), and the tap buffer that drives it is part of the block and of the
power row. Justification, stated so it can be replaced: the consumer that
exists today (`sg13g2-aib`, `spec/dll-interface.md` D-11) takes the taps into
a phase-selection mux it owns, i.e. one lv gate input plus local wiring per
tap. At the process spec's 0.32 – 0.40 fF/µm Miller figure and a thin-oxide
gate, 20 fF is a mux input of several tens of µm of gate width plus a short
wire — a demanding load for a 1.2 V stage at 1 GHz, not a trivial one. It is
also 2 – 4× the loads used in this repo's smoke decks (5 and 10 fF), so the
smoke timings above are optimistic relative to it. When a `consumes:` edge
exists, the consumer's stated load replaces 20 fF through a new record; until
then, 20 fF is the number every result is graded against, and a bench that
uses another load is not a spec result.

## Folded in from the review at the operator's direction (calls D, E, G)

- **D (0005 part 3)**: the over-delay supervisor is a half-period **window
  detector on existing taps** (tap N against the input, tap N/2 as the
  half-period reference), not an extended delay line to 1.5 T. Recorded in
  0005.
- **E (Locked predicate)**: the predicate's tap-N tolerance becomes **2 % T**,
  equal to row 5's target, so row 5 is the graded number and not implied by
  the predicate; the stretch column grades with a 1 % predicate. Recorded in
  0001 and the spec.
- **G (jitter method)**: a method record, validated on a known case, precedes
  the first jitter result; already in the spec's row 6 text. The 2 ps limit is
  a target, unverified until that record exists.

Also clarified, no number changed: lock time is measured from the later of
enable and the first input rising edge (start state 5d); the jitter estimator
is graded on the worst tap over k = 1…8.

## Open items this record does not close

- Interface list (pins, levels, enable polarity, lock-status timing in cycles)
  — row 12 states the lock-status behaviour; the full list is the first
  schematic issue's first deliverable.
- Area target: none yet; add a row with the first layout estimate.
- Post-layout re-simulation of rows 7 and 10 (row 11 lists 4, 5, 8).
- Simulation budget for row 8 (≈ 9 start states × 5 frequencies × 45 corners).
