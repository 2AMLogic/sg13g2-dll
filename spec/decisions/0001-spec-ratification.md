# 0001 — Spec ratification, device flavor and rail, lock predicate, jitter method

- **Status**: proposed — becomes ratified only by a human-reviewed merge of this record. Agents do not mark it ratified.
- **Date**: 2026-10-17
- **Decided by**: Builder agent, issue #2
- **Consumes**: README target table; [`../target-spec.md`](../target-spec.md); [`../../sim/corners.json`](../../sim/corners.json)
- **Related**: 0004 (topology), 0005 (false lock), 0006 (reuse); #4, #5, #6

## Decisions

| # | Question | Decision |
|---|---|---|
| 1 | Spec rows | Ratify `target-spec.md`; README target/fallback/stretch carried over unchanged |
| 2 | Device flavor and rail | **3.3 V thick-oxide CMOS (`sg13_hv_nmos`/`sg13_hv_pmos`) throughout**; nominal 3.30 V, tolerance ±10 % (2.97–3.63 V); **no SiGe HBT** |
| 3 | Power row | ≤ 5 mW at worst corner, consistent with the rail above |
| 4 | "Locked" | Predicate defined in the spec: ≤ 1 % T tap-N error on 64 consecutive cycles, Vctrl ripple < 5 mV pp |
| 5 | False lock | Testable criterion in the spec: exactly one period of delay, from named start states, all corners, all five frequencies |
| 6 | Jitter | Transient-noise method, run length, seeds and estimator stated in the spec |
| 7 | Corner set | Full 5 MOS × 3 supply × 3 temperature = 45 corners in `sim/corners.json`; no narrowing for any pass/fail row |

## Device flavor and rail (decision 2)

Chosen: 3.3 V thick-oxide. Rejected: 1.2 V thin-oxide (`sg13_lv_*`) for the
clock path, and a 1.2 V/3.3 V mix.

Reason: the PFD and charge pump this block adopts (0006) are already drawn
on `sg13_hv_*` in `2AMLogic/sg13g2-pll` (its `spec/decision-records/DR-002-supply-device-flavor.md` Decision 0 at `83e59fe`). A mixed rail would need
level shifters in the clock path, which add matched-load asymmetry to a block
whose accuracy is a matching property. One rail keeps the delay line and
its loads a regular array.

HBT role: none. No current mirror, reference, or buffer uses a bipolar in this
block; revisit only with extracted `sg13g2-hbt-characterization` data showing
an advantage on a stated row.

**Unverified risk, stated so it is not buried:** thick-oxide devices are slower
than thin-oxide ones, and no simulation has yet shown that an hv delay cell
spans the range the 1 GHz target needs. This is exactly why 0004 makes the
500 MHz fallback the first thing proven. **Revisit trigger:** if 0004's
topology cannot give 8 evenly spaced taps over the lock range at 1 GHz with
margin at mos_ss/2.97 V/125 °C, a new record reconsiders a 1.2 V clock path; it
does not relax the 1 GHz row quietly. 2 GHz must not drive the rail choice.

## Locked predicate (decision 4)

What is compared: the tap-N rising edge against the input rising edge plus one
period. Tolerance: 1 % of T. Held for: 64 consecutive cycles, with Vctrl pp
ripple under 5 mV. The 1 % is half the 2 % static-phase-error row, so a locked
loop has margin to the row; lock time (row 7) is the time to the first
success that persists to 2 µs.

## Corner set (decision 7)

All 45 corners are used for every pass/fail row. Narrowing below MOS ×
±10 % supply × −40…125 °C is applied to exactly one row: **jitter (row 6)**
runs at 3 corners (tt/3.30 V/27 °C, ss/2.97 V/125 °C, ff/3.63 V/−40 °C),
because transient noise at ≥ 2000 cycles × ≥ 8 seeds is the one analysis whose
cost makes 45 corners impractical. The three bracket the process, supply
and temperature extremes of a delay-line delay. The narrowing is recorded
next to every jitter number. The `reduced_set` in `corners.json` is for
iteration only and is never a recorded result. The sf/fs skew corners stay in
the full set because mismatched NMOS/PMOS strength moves rising versus falling
edge delay, which is the pulse-width asymmetry a delay line cares about.

## Jitter method (decision 6)

See "Jitter method" in the spec. In short: ngspice cannot do periodic noise,
so the number is from transient noise over ≥ 2000 locked cycles, ≥ 8 seeds,
rms time-interval error versus an ideal grid minus the same on the input.
Supply-induced jitter is not covered by it; the proxy is a recorded supply-step
sensitivity.

## Open question: `klt` placement and extraction of a matched array

See 0006 "klt capability". Answered from the tool's documented capability;
the actual symmetric-matched-array behavior is unverified.

## Ratification

This record is `proposed`. A reviewer merging this PR ratifies it. No agent
may relax a row after that without a new decision record.
