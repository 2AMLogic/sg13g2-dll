# 0012 — Charge pump delivers 2-6 uA, not the assumed 20 uA; `cp` stays `adopting`

- **Status**: proposed (needs a follow-up issue; the spec is not changed here)
- **Date**: 2026-11-05
- **Decided by**: Builder agent, issue #30
- **Related**: 0006, 0008 ("Bounded step", addendum 2026-11-05), 0010 (delay line)

## Finding (simulated, never measured)

`sim/cp-currents/results/20261105T130112Z/record.md` (batch fleet, ngspice 46, reduced corner set,
VOUT held at 0.6 V by an ideal source; criteria K1-K6 in `sim/cp-currents/summarize.py`, fixed before the
run). Earlier runs `20261105T125658Z` and `20261105T125926Z` are kept as evidence of the charge-window
changes described in `sim/cp-currents/README.md`; the current figures are identical in all three.

| corner | I_up | I_dn | mismatch | idle supply current |
|---|---|---|---|---|
| tt/1.2 V/27 C | 3.51 uA | 3.65 uA | 4 % | 12.2 uA |
| ss/1.08 V/125 C | 2.09 uA | 2.12 uA | 2 % | 7.2 uA |
| ff/1.32 V/-40 C | 6.18 uA | 5.98 uA | 3 % | 20.4 uA |

- UP/DN current mismatch is small (K2 passes, including at ss/125 C) and the bounded-step ratio
  K_dl * I / C_loop is 0.002 .. 0.030 (K4 passes with large margin; K_dl from the delay-sanity record).
- **K1 fails:** I_cp is 2.1 .. 6.2 uA, not the 20 uA that 0008 "Bounded step" assumed (and not in the
  5..40 uA window at tt and ss). The assumed number is wrong by a factor of 3 .. 10.
- K3 (leakage <= 2 % of the current) fails at ss/125 C only: 44 nA against 2.1 uA.
- **K5 fails at all corners:** the dump-buffer node VDUMP is about 0.5 V below VOUT at VOUT = 0.6 V and
  goes below VSS (-0.16 V, tt) at VOUT = 0.3 V; its slope against VOUT is 1.6 rather than 0.8 .. 1.2. The
  follower (`cp_dumpbuf`) does not track VOUT in the low half of the range, so the dump legs are not
  held at VOUT while the switches are off there.
- Charge per pulse is **not established**: the DN window carries an unexplained late current spike and
  the UP charge is dominated by switching injection (see the record's note). It was not graded.

## Consequence

`reuse.lock.json` `cp` stays `adopting`. A smaller I_cp does not endanger the bounded-step constraint
(it helps it); the risk moves to speed and leakage: a 2 uA pump into about 1 pF moves VCTRL by only
2 mV per 1 ns of error, which slows lock-time (spec row on lock time, graded by #25) by the same factor.

## Proposal (for a follow-up issue; not simulated)

Raise the `cp_bias` reference current (the PMOS resistor `XMR`, 0.5 u / 4 u, sets it) and re-check K1-K5;
K4 shows about 3x headroom at ff before the 0.1 limit. Re-bias or replace the dump follower so it
tracks VOUT down to 0.3 V (K5). Both are redraws; re-run `sim/cp-currents/run.sh` after each.
