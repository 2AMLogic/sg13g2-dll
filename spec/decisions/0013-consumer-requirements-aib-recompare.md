# 0013 — Disposition of the re-compared sg13g2-aib consumer requirements (column correction)

- **Status**: proposed. **This record restates what `spec/target-spec.md`
  already says and changes nothing.** It sets no limit, no σ and no new
  operating point, and its merge is **not** a ratification of any row. The
  spec file remains a ratification candidate under
  [0009](0009-ratification-of-target-spec.md) and issue #41.
- **Date**: 2026-11-13 (written against `origin/main` at `381d989`)
- **Source**: `2AMLogic/sg13g2-aib`, `spec/dll-interface.md` rows D-1…D-12 and
  its `spec/target-spec.md` row T-21, at `70b7d23`; the consumer's own record
  of the comparison is its DR-0020.
- **Origin**: this repo's issue #72.
- **Follows** [0002](0002-consumer-requirements-aib.md) (first pass, this
  repo's issue #10) and [0007](0007-rail-1p2v-thin-oxide.md) (operator ruling
  that settled 0002's G1, G2, G4, G5). **It edits neither.**
- **No `consumes:` edge, manifest or `reuse.lock.json` change.** The consumer
  states it is not asking for one.

Every number below is either **hand arithmetic** from the two specs' tables
(marked as such) or **simulated**, quoted with its source file and its
conditions. Nothing here is measured. The consumer's own figures were **not
opened** while writing this record: they are quoted **as stated in #72**.

## The column correction

`spec/target-spec.md` row 1 and the lines 7–9 rule ("fallback and stretch
re-grade the same condition at their own value") key every column of this spec
to its own `f0`. The consumer's columns are keyed to its data rate on a
forwarded clock at half that rate (DDR), so the two sets of columns do not
line up:

| Consumer point (as stated in #72) | Its forwarded clock | Column of this spec that applies |
|---|---|---|
| target, 1 Gb/s DDR | 500 MHz | **fallback** |
| fallback, 500 Mb/s DDR | 250 MHz | **none** — below this spec's lowest point |
| stretch, 2 Gb/s DDR | 1 GHz | **target** |

The consumer's earlier table — the one 0002 compared against — quoted this
spec's **target**-column numbers next to its own target. Corrected, the
numbers that apply at the consumer's target are the **fallback** column's,
which are looser on every row. Two of the four items below change verdict as a
result, and one of them makes 0002's recorded jitter fit inapplicable at the
frequency the consumer runs at.

## Dispositions

| # | Item (as stated in #72) | Disposition |
|---|---|---|
| 1 | A 250 MHz forwarded-clock operating point (the consumer's fallback rate; unresolved from #10's G1) | **Declined — out of scope.** No 250 MHz point exists or is proposed. See item 1. |
| 2 | Row 3's fallback column must not be read as covering the consumer's target (16 steps per clock period) | **Accepted as a statement of fact, with no spec change.** Row 3 fallback is 4 phases; it does not cover it. 0007 decision 4 stands. See item 2. |
| 3 | A limit, or a stated σ, on the row 4 Monte Carlo spacing result | **Not decided here — open in #73.** A statistical limit is an operator choice (0009 EE change A). See item 3. |
| 4 | Confirm whether ≤ 5 ps rms is the row 6 limit at the 500 MHz fallback point | **Confirmed: it is.** The absolute limits do **not** track the target column. 0002's jitter fit is corrected below and does not apply at the consumer's target. See item 4. |

## 1 — the 250 MHz point is out of scope

`spec/target-spec.md` row 1 names three operating points: 1 GHz (target),
500 MHz (fallback), 2 GHz (stretch). There is no 250 MHz point anywhere in
the file (`grep -n 250 spec/target-spec.md` returns no match at `381d989`), and
none is proposed here. **Disposition: declined.** The consumer should record
its fallback rate as *not derivable from this spec* rather than as covered.

0007 decision 3 accepted ±20 % around 500 MHz (400–600 MHz), which does close
the consumer's **target** rate — acknowledged, and that is not reopened here.

Why a 250 MHz point would be a second range, not a widening (hand arithmetic
on the spans, the same reasoning 0002 G1 used to decline one continuous range
over 500 MHz and 1 GHz):

- 400–600 MHz is already a **1.5:1** span.
- The consumer's 250 MHz ±10 % is 225–275 MHz (the ±10 % is 0002's G1 row,
  line 25; #72 carries the 225–275 MHz figure).
- A single continuous range covering both would be 225–600 MHz, a **2.67:1**
  span. 0002 G1 (lines 54–57) keeps each lock range under 2:1 so that the
  delay-range limit — one period at the top of the range, below two periods at
  the bottom — excludes harmonic lock inside it; a 2.67:1 span fails that
  bound. [0005](0005-false-lock-exclusion.md) is the stricter statement of the
  same point: it expects the corner spread of the maximum delay to exceed the
  1.33× such a bound allows, so range limiting is **necessary but cannot be
  the exclusion mechanism** (0005 lines 11–18), which is instead the
  deterministic minimum-delay start-up, bounded monotonic approach, and
  over-delay supervisor of its "Mechanism chosen". Either way, a 2.67:1 span
  is outside what the existing argument covers.

So 250 MHz would have to be a **separate** range with its own range-select and
its own false-lock argument — a design decision of the kind 0002 G1 declined to
make from a consumer requirement, and larger than this record's scope. It is
not taken here and no row changes.

## 2 — row 3's fallback column is 4 phases and does not cover the consumer's target

Hand arithmetic at the consumer's target (forwarded clock 500 MHz, so
T = 2 ns and UI = T/2 = 1 ns):

| | Value | Source |
|---|---|---|
| Consumer T-21 target step | ≤ 1/8 UI = 125 ps = T/16 → **16 steps per clock period** | as stated in #72 |
| This spec at 500 MHz, row 3 fallback | **4 phases**, even over T → step T/4 = 500 ps = **0.50 UI** | `spec/target-spec.md` row 3 |

That is **4× coarser** than the consumer's target step, not the 2× that a
reading against row 3's *target* column (8 phases) would suggest. The purpose
of this item, per #72, is that **row 3's fallback column is not read as
covering the consumer's target**; this record is that statement.

**0007 decision 4 stands**: 8 phases at target, 16 at stretch; 16-at-target is
declined, met only by the stretch column, and (per 0007 decision 4) "the next
move is theirs". No phase count changes here, and nothing new is asked of the
design — #72 states the consumer is answering decision 4 on its own side (its
DR-0014 and its issue #9).

For scale, and **not** as a spec result: the delay-sizing comparison
(`sim/delay-sizing/results/20261107T231500Z-comparison/comparison.md`,
simulated, schematic, ideal bias, no extraction) records that T/8 = 250 ps is
spanned at ss, tt and ff by both candidates at 500 MHz — i.e. even an 8-tap
line at the fallback frequency gives a 250 ps step, still **2×** coarser than
the 125 ps the consumer needs. Row 3's fallback column is 4, not 8, so this
probe is more generous than the spec, and it still does not close the item.

## 3 — the row 4 Monte Carlo result has no limit; the question is open in #73

Row 4 bounds the **systematic** (corner, end-cell, load) spacing error only —
≤ 2 % T at target, ≤ 5 % at fallback — and states that Monte Carlo is "a
separate recorded result with **no limit**", with "a consumer must budget
random mismatch separately". That wording is deliberate:
[0009](0009-ratification-of-target-spec.md) EE change A records that "a
statistical limit is an operator choice and is not added here".

**This record therefore sets no limit and no σ.** The consumer's ask (a limit,
or a σ it may budget against) is an operator decision and is tracked as
**#73**, which is open and operator-held. Until it is answered, a worst-case
placement row at this pin is **unanswerable** rather than failing — the
derivable terms alone, by hand arithmetic at T = 2 ns / UI = 1 ns, are:

| Term | Value at 500 MHz | Source |
|---|---|---|
| half a step | 0.25 UI (250 ps) | row 3 fallback, 4 phases → step T/4 |
| systematic spacing error | ≤ 0.10 UI (≤ 5 % T = 100 ps) | row 4 fallback |
| random mismatch | **unbounded** | row 4: explicitly no limit |
| derivable subtotal | **≥ 0.35 UI** | 0.25 + 0.10 |

against the consumer's worst-case placement budget of ≤ 0.0625 UI (= 62.5 ps
at UI = 1 ns), as stated in #72.

The σ figures #72 quotes for scale —
`sim/delay-sizing/results/20261107T224325Z-mc/`, per-tap step σ of 8.2–15.1 ps
(candidate A) and 12.5–16.9 ps (candidate B) — are **simulated** and are a
**schematic sizing probe, not a spec result**, on the conditions the record
itself states: ss/1.08 V/125 °C, **1 GHz** (not 500 MHz), **Vc = 1.0 V** (near
the fast end, not at either candidate's 125 ps point), `mos_ss_mismatch`,
mismatch-only, n = 32, ideal bias, no layout parasitics. At n = 32 a σ estimate
carries about 13 % relative uncertainty. They are quoted here only to show the
order of magnitude is comparable to the consumer's whole 62.5 ps budget; **they
are not a budget, not a limit and not an answer to #73**, and row 4's graded
result is post-layout extracted, which this probe is not.

## 4 — ≤ 5 ps rms is the limit at 500 MHz; dated correction to 0002's jitter fit

**Confirmed, answering the ask in #72**: row 6's fallback value, ≤ 5 ps rms, is
the limit at the 500 MHz operating point. The absolute limits do **not** track
the target column — lines 7–9 of `spec/target-spec.md` state that "fallback and
stretch re-grade the same condition at their own value", and row 6 names three
distinct values (≤ 2 / 5 / 1 ps rms). No limit changes here.

### Dated superseding entry, 2026-11-13, correcting 0002's Jitter section

Per 0002's own rule ("if #2 has already landed when this is read, the changes
proposed above are made by a dated superseding entry, not by editing a ratified
table"), **0002 is not edited**; this entry supersedes its Jitter arithmetic.

0002 (lines 99–108) compared the consumer's ≤ 0.03 UI peak-to-peak against
**≤ 2 ps rms** and recorded a margin of 0.002 UI. That 2 ps is this spec's
**target**-column limit, which applies at a 1 GHz clock — the consumer's
*stretch*. At the consumer's **target** the applicable limit is the fallback
column's. Hand arithmetic, at the same 14 σ Gaussian conversion 0002 used and
UI = 1 ns:

| | p-p at 14 σ | as UI | Source |
|---|---|---|---|
| 0002's comparison (target-column limit, so a 1 GHz clock) | 2 ps × 14 = 28 ps | 0.028 UI *only against UI = 1 ns, which is not the UI at a 1 GHz clock — see below* | 0002 lines 102–103 |
| **This spec at the consumer's target** (fallback column, 500 MHz) | **5 ps × 14 = 70 ps** | **0.07 UI** | row 6 fallback |
| Consumer requirement (as stated in #72) | 30 ps | 0.03 UI | consumer T-21 |

So the fit 0002 discussed **does not apply at the frequency the consumer
actually runs at**: against 0.03 UI, 0.07 UI is a **2.3× gap** (0.07 / 0.03 =
2.33), not a 0.002 UI margin.

The 0.028 UI figure does not survive at the consumer's *stretch* point either,
and it is worth being explicit about why, because the error is the same column
error one column over. 0002 divided the 28 ps by UI = 1 ns, which is the UI at
the consumer's **target** (1 Gb/s DDR), while the 2 ps that produced the 28 ps
is this spec's **target**-column limit and so applies at a 1 GHz clock — the
consumer's **stretch**. That pairing exists at no consumer operating point. At
the stretch point the link runs 2 Gb/s DDR on a 1 GHz clock, so UI = T/2 =
**500 ps**, and the same 28 ps is 28 / 500 = **0.056 UI**. #72 states the
≤ 0.03 UI requirement at the consumer's target only; whether it also applies at
stretch is not stated there and is not decided here. If it does, the gap at
stretch is **1.9×** (0.056 / 0.03).

Two further mismatches, recorded as stated in #72 rather than converted away:

- **rms versus peak-to-peak.** The 14 σ factor is an assumption about the
  distribution, not an identity. Row 6's own "Jitter method" section says the
  figure is thermal-noise class, underestimates 1/f, and does not capture
  supply noise unless injected (the proxy for which is a recorded supply-step
  sensitivity in ps per mV). A single conversion factor between the two
  quantities is therefore not available on either side of the comparison.
- **Corner coverage.** Row 6 is graded at 3 corners (tt/1.20 V/27 °C,
  ss/1.08 V/125 °C, ff/1.32 V/−40 °C) because ngspice transient noise is
  expensive; the consumer's T-21 asks for its PVT-FULL, which is the same
  45-corner grid as `sim/corners.json`. **A 3-corner jitter number is not
  PVT-FULL coverage.** #72 states the consumer is recording this mismatch, not
  disputing the choice. No corner set changes here.

Row 6 has no result yet in any case: `sim/bench-rows.json` at `381d989` carries
row 6 as `status: blocked` on the noise-method decision record, so the limit
above is a **specified-only, proposed** number at no corners.

## State of the evidence, as the consumer read it

Recorded so that the consumer's comparison can say "specified only" rather than
implying results exist. Verified at `381d989`: `sim/bench-rows.json` has
`"dut": "standin"`, row 6 is `status: blocked`, and `sim/phase`,
`sim/lock-time`, `sim/false-lock`, `sim/jitter` and `sim/power` contain no
`results/` or `records/` directory. Every row of `spec/target-spec.md` is
therefore a **proposed, specified-only** number at no corners, and the file is
itself a ratification candidate with #41 open. That is a statement of where the
work is, not a defect.

## Out of scope

- Any change to a spec value, row text or column — including a note added to
  row 3. `spec/target-spec.md` is the ratification candidate under review
  (#41), and 0009 decision 5 is that no row is edited to answer a review; #72
  itself accepts "or in a record" for item 2.
- Editing 0002 or 0007. 0002's jitter arithmetic is corrected by the dated
  superseding entry above, per 0002's own rule.
- A 250 MHz operating point, a second lock range, or a range-select; a
  phase-count change.
- A Monte Carlo limit or a stated σ (#73, operator-held).
- Any schematic, sizing, simulation or layout work; a `consumes:` edge,
  manifest or `reuse.lock.json` change.
- Anything written in `2AMLogic/sg13g2-aib`.
