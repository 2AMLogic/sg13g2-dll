# 0005 — Harmonic-lock exclusion mechanism

- **Status**: proposed (ratified with 0001)
- **Date**: 2026-10-17
- **Decided by**: Builder agent, issue #2
- **Related**: [`../target-spec.md`](../target-spec.md) row 8; 0004

This record states the criterion and chooses the mechanism. It does not make the
full false-lock *argument*; that precedes sizing in a later record (CLAUDE.md).

## Why delay-range limits alone do not work

For lock at one period over the row-2 range, the maximum delay at every corner
must exceed 1.25 ns (T at 0.8 f0). To exclude lock at 2T by range alone, the
maximum delay at every corner must also be below 2 × 0.833 ns = 1.667 ns.
Both hold only if the ss maximum delay is under 1.33 × the ff maximum delay.
Delay spread across process, 2.97–3.63 V, and −40…125 °C is expected to exceed
that, so range limiting is necessary but cannot be the exclusion mechanism.
This is a reasoned bound, not a simulated one.

## Mechanism chosen (three parts, all required)

1. **Deterministic start-up**: on enable (including re-enable), the control
   voltage is forced to the **minimum-delay** state before the PFD is allowed
   to act, so total delay starts below one period at every corner and
   frequency of the lock range.
2. **Monotonic approach**: with a tri-state PFD and a charge pump whose
   per-cycle step is bounded so total delay changes by well under T per input
   cycle, the delay increases from the minimum until the PFD sees
   zero error, which is the first crossing at 1 T. It cannot step past T to
   2T.
3. **Over-delay supervisor**: a half-period **window detector on existing
   taps** — tap N against the input, with tap N/2 (nominal T/2) as the
   half-period reference — that decides whether the tap-N edge falls in the
   first or second half of the input period. If the loop is found at delay
   > 1.5 T (reachable from a disturbed, mid-range or maximum preset), it
   re-asserts the part-1 reset. It also resets when the control voltage sits
   within 50 mV of a rail past a time-out. (0007 call D: the first draft
   compared "a tap at nominal 1.5 T", which would need a line 50 % longer than
   the lock range uses; the window detector needs no extra matched cells and
   keeps the array's edge cells as output taps.)

The full false-lock argument that precedes sizing must also cover PFD edge
pairing from the minimum-delay start: a tri-state PFD measures the delay d,
not T − d, so the loop polarity and the bounded step of part 2 are what make
d → T the first stable crossing rather than the minimum rail.

Part 3 is what covers start states 2, 3 and 4 of the spec's list; parts 1–2
cover state 1 and the enable cases. The supervisor adds a block not in the
README's scope list; it is part of "start-up and false-lock prevention",
which is in scope.

## Rejected

- **Range limiting alone** — argued above.
- **Start-from-friendly-condition only** — CLAUDE.md: a design that locks only
  from a friendly initial condition has not locked.
- **Frequency detector** — a DLL has no frequency acquisition by construction,
  and a frequency detector moves toward a PLL's loop.

## Consequence for the testbench

The false-lock testbench must run every start state of the spec at all 45
corners and all five frequencies and must measure the delay **in periods**,
passing only on exactly 1.
