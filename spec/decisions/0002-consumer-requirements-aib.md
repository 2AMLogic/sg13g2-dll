# 0002 — Disposition of consumer requirements from sg13g2-aib

- **Status**: proposed, feeds the spec ratification in issue #2. Nothing here
  changes a ratified number; the README table is still a DRAFT.
- **Date**: 2026-10-17 (against `origin/main` at `df1ca95`)
- **Source**: `2AMLogic/sg13g2-aib`, `spec/dll-interface.md` (aib issue 2).
- **Origin**: this repo's issue #10.
- **No `consumes:` edge is added.** A manifest change is an operator
  decision, proposed only after G1 and G2 close.

This is a **draft-versus-draft** comparison. Every number below is hand
arithmetic from two draft tables. None of it is simulated, and none is a
finding.

## Context

The consumer forwards a clock at half the data rate (DDR): 1 Gb/s per wire is
a 500 MHz clock, 500 Mb/s is 250 MHz, 2 Gb/s is 1 GHz. UI = half a clock
period. It needs the received clock placed inside a 1 UI data eye.

## Dispositions

| # | Consumer requirement | Repo draft | Disposition | Reason |
|---|---|---|---|---|
| G1 | Lock at 500 MHz target, 250 MHz fallback, 1 GHz stretch; range ±20 % / ±10 % / ±40 % around the point in use | 1 GHz target, 500 MHz fallback, 2 GHz stretch; ±20 % around 1 GHz (800 MHz–1.2 GHz) | **Partly accepted** | See G1 below. 500 MHz ±20 % (400–600 MHz) is accepted as a requirement on the existing fallback point; a single range covering both points is declined. |
| G2 | 16 evenly spaced phases per period (fallback 8, stretch 32); worst-case placement error ≤ 0.0625 UI | 8 phases target (16 stretch); spacing error ≤ 2 % of the period | **Partly accepted** | See G2 below. 16 phases is already the repo stretch; the 0.0625 UI limit is not adoptable as stated. |
| G3 | Duty-cycle correction, ±10 % in to ±3 % out, conditional on the consumer's own simulation | Not in the stated scope | **Declined (out of scope)** | A corrector is a separate block. README Scope is updated to say so. Revisit only if the consumer's simulation shows it is needed. |
| G4 | 1.2 V ±10 % (1.08–1.32 V), thin-oxide, −40 to +125 °C | "Device flavor and rail to ratify" | **Accepted as an input to the ratified supply row** | It fills the open row in #2. The temperature span becomes the PVT corner range; every recorded result already carries corners. |
| G5 | Lock-status output | Not listed | **Accepted** | A lock detector is likely needed anyway to argue false-lock exclusion in #2. The output's definition (threshold, hold time) belongs to that argument, not to this record. |
| J | Added jitter ≤ 0.03 UI peak-to-peak (≈ 2.1 ps rms at 1 Gb/s, 14 σ) | ≤ 2 ps rms | **Accepted only with a shared definition** | See Jitter below. |

Already compatible per the consumer's table, with no disposition needed:
lock time (requirement ≤ 10 µs, draft ≤ 1 µs), false-lock prevention, and
delay range of one period.

## G1 — lock frequency and range

Arithmetic: 500 MHz ±20 % is 400–600 MHz (1.5:1). 250 MHz ±10 % is
225–275 MHz. 1 GHz ±40 % is 600 MHz–1.4 GHz. The draft's 1 GHz ±20 % is
800 MHz–1.2 GHz, which excludes 500 MHz.

Options named in the issue: (a) re-centre on 500 MHz with 1 GHz as a
stretch; (b) one block with a range-select; (c) 1 GHz only, G1 declined.

Proposed disposition: **keep 1 GHz as the target** (project rule: 1 GHz is
the target, 500 MHz the fallback). Accept that the **500 MHz fallback point
carries a ±20 % lock range (400–600 MHz)**, so the consumer's target is met
by the fallback. Decline a single continuous range spanning 500 MHz and
1 GHz: a 2:1 span is where a lock to two periods becomes possible, so it
would need a range-select (option b) and a separate false-lock argument per
range. That is a larger design decision than a consumer requirement can make
and is left to #2.

Effect on the false-lock argument: each lock range must stay under 2:1, so
the delay-range limit (one period at the highest frequency, below two periods
at the lowest) excludes harmonic lock inside it. A 1.5:1 span (400–600 MHz)
meets that; 800 MHz–1.2 GHz (1.5:1) already does.
Effect on the README table: the fallback column's lock range becomes
"±20 % around 500 MHz" if #2 adopts this; the 1 GHz row stays. Not edited
here.

## G2 — phase count and spacing

Arithmetic, with UI = T/2:

- 16 phases: step = T/16 = 1/8 UI. Half a step = T/32 = **0.0625 UI**.
  The consumer's limit (half a step plus spacing error ≤ 0.0625 UI) is
  therefore met only with **zero spacing error**. No margin.
- Repo draft spacing error of 2 % of T is 0.04 UI. At 16 phases the
  placement error would be 0.0625 + 0.04 = about 0.1025 UI, against 0.0625.
- 32 phases (consumer stretch): half a step = T/64 = 0.03125 UI, leaving
  0.03125 UI = 1.5625 % of T for spacing error. The repo stretch spacing of
  1 % of T (0.02 UI) fits.

Proposed disposition: accept 16 phases (the repo stretch) as the count the
consumer needs. Decline the 0.0625 UI limit as written, since it cannot be
met with any real spacing error at 16 phases. Ask the consumer to confirm
the definition of placement error (is half a step the right term, or is the
eye centred on a tap?) or relax the limit, before the spec adopts either
number. The definition must be cited from `spec/dll-interface.md` in
`sg13g2-aib`, not assumed.

Effect on the false-lock argument: more taps lengthen the delay line (more
cells for the same period), so the delay-range limit and the start-up state
must be argued for the 16-phase line. Effect on the README table: output
phases target and stretch values move only if #2 ratifies 16 as the target.

## G3 — duty-cycle correction

Out of scope. README Scope gains an explicit "not in scope" line. No design
work here.

## G4, G5

G4 matches the "device flavor and rail to ratify" row. The values are
carried into #2 as the candidate rail and temperature span. G5 is accepted
as an output; its definition is deferred to the false-lock argument.

## Jitter

0.03 UI peak-to-peak at 1 Gb/s (UI = 1 ns) is 30 ps; divided by the 14 σ
factor that is about 2.1 ps rms. The draft's 2 ps rms at 14 σ is 28 ps, or
0.028 UI: a margin of 0.002 UI. That fit holds only if both sides use one
definition. Per project rules a jitter number carries its method. Proposed
shared definition: transient-noise simulation, with run length, seeds and the
estimator (rms of the edge-time deviation from an ideal clock, converted at
14 σ assuming Gaussian) stated next to every number. The exact parameters
are set in #2. Until then the fit is **not claimed**.

## Sequencing and ratification path

Issue #2 is open (`loom:building`) as of this record. This record is input to
that ratification. No spec number is changed here. If #2 has already landed
when this is read, the changes proposed above are made by a dated
superseding entry, not by editing a ratified table.

The README refers to the ratification as issue #1; #2 is the ratification
issue as of this record, and that reference should be confirmed when #2
lands.

## Out of scope

Any schematic, sizing or simulation; the `consumes:` edge; designing duty-cycle
correction; reopening the false-lock method (that belongs to #2).
