# sg13g2-dll

A delay-locked loop (DLL) on
[IHP SG13G2](https://github.com/IHP-GmbH/IHP-Open-PDK), a 130 nm SiGe BiCMOS
open PDK — a voltage-controlled delay line locked to one period of an input
clock, producing evenly spaced output phases — designed by AI agents driving
[klayout-tools](https://github.com/2AMLogic/klayout-tools) and the
open-source xschem + ngspice flow.

**Status: just opened, specification phase.** Nothing is designed yet.

**Built agent-native.** Every specification, decision record, testbench, and
line of documentation here is produced by AI agents working from a ratified
spec and an append-only evidence trail — not human-authored work that agents
merely assisted with. Verification is the product: every claim traces to a
recorded result under PVT corners. Where the agents hit friction with the
open-source tooling — most often
[klayout-tools](https://github.com/2AMLogic/klayout-tools) — that friction is
filed as a public issue against the tool itself, so the fix benefits everyone
using SG13G2, not just this repo.

## Why this block, on this PDK

A DLL is the clock block that a PLL is not. It does not synthesize a new
frequency; it aligns and subdivides the one it is given. Multiphase clocks
for serializers, sampling clocks for time-interleaved converters, and
deskew all start here. To our knowledge, no open DLL with published
verification evidence exists on any open PDK, which makes it a real gap
rather than a re-run.

It is also a different control problem from the program's PLLs. A DLL's
loop is first-order and has no frequency acquisition, so it can lock to the
wrong multiple of the period, or run its delay line into a rail and stay
there. Proving that it locks to exactly one period from every start state,
at every corner, is the block's hard part — and it is a verification
problem as much as a circuit one.

Physically, phase accuracy is a layout property: the spacing between output
phases is set by how well the delay cells and their loads match. That puts
symmetric placement, matched routing, and post-layout extraction of a
regular array in front of the tools.

## Scope

- **In scope**: the voltage-controlled delay line, phase detector, charge
  pump and loop filter, start-up and false-lock prevention, and the output
  phase taps with their buffers.
- **Not in scope**: frequency synthesis, a reference oscillator, duty-cycle
  correction of the input clock (see
  `spec/decisions/0002-consumer-requirements-aib.md`), and any consumer of
  the phases. The input clock is an ideal or behavioural source at the block
  boundary.
- **Same-PDK siblings**: `sg13g2-pll` already designs a phase-frequency
  detector and a charge pump on this PDK. They are candidates to adopt, not
  to redesign; whether they fit a DLL's loop is decided in a decision record.

## Target specification (proposed — ratified by merge of [0001](spec/decisions/0001-spec-ratification.md); issue #2)

| Parameter | Target | Fallback | Stretch |
|---|---|---|---|
| Input clock | 1 GHz | 500 MHz | 2 GHz |
| Lock range | ±20% around the target input frequency | ±20% around 500 MHz | ±40% |
| Output phases | 8, evenly spaced over one period | 4 | 16 |
| Phase-spacing error | ≤ 2% of the period, worst corner | ≤ 5% | ≤ 1% |
| Static phase error (output vs input) | ≤ 2% of the period | ≤ 5% | ≤ 1% |
| Added jitter (rms, simulated) | ≤ 2 ps | ≤ 5 ps | ≤ 1 ps |
| Lock time | ≤ 1 µs from enable | ≤ 5 µs | — |
| False lock | none, from any start state, at any corner | — | — |
| Lock-status output | asserted only when locked | — | — |
| Supply / power | 1.2 V thin-oxide (±10 %), no HBT; ≤ 5 mW | ≤ 10 mW | ≤ 2 mW |
| Signoff | DRC + LVS clean, post-layout re-verified | — | — |

Row-by-row min/typ/max, grading conditions and corner sets are in
[`spec/target-spec.md`](spec/target-spec.md); the 45-corner set is in
[`sim/corners.json`](sim/corners.json).

Maturity ladder: spec ratified → loop architecture and false-lock argument
recorded → schematic simulated across PVT → layout DRC/LVS-clean →
post-layout re-verification → shuttle seat → measured silicon. **Current
position: spec proposed, awaiting ratification.**

## Repo layout

```
spec/          ratified spec + decision records
design/        schematics / netlists (xschem)
sim/           testbenches + PVT corner results (ngspice)
layout/        GDS + DRC/LVS reports (klayout-tools driven)
measurements/  silicon characterization (empty until tape-out)
```

## License

Apache License 2.0 — see [LICENSE](LICENSE).
