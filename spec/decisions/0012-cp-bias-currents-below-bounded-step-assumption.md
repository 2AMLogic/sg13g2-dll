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

## Update 2026-11-06 (issue #62): redrawn cp_bias and cp_dumpbuf, K1-K6 pass; the 2026-11-05 K5 finding was partly a bench defect

Appended; the sections above are the record of the 2026-11-05 run and are not edited.

### Bench defect found while redrawing

`sim/cp-currents/decks/cp_body.spice` drove UP and DN with `v(vdd)*pwl(time, ...)` behavioural
sources whose lists ended on a falling edge (`160.4n,0` and `180.4n,0`). ngspice extrapolates the last
segment of a `pwl()` expression, so UP fell to about -19 V at 162 ns and -175 V at 175 ns (and DN
likewise after 180 ns). That drove `VDUMP` below VSS and into mA-level supply current after the charge
pulses, and it is the most likely source of the "unexplained late current spike" in the DN window
and of the `VDUMP` collapse in the 2026-11-05 K5 result. Both lists now end with an explicit
`400n,0` point. `summarize.py` and the K1-K6 criteria are unchanged. The charge-per-pulse columns are
still not graded and still not claimed.

With the fixed bench the unmodified follower fails K5 differently (slope 0.65 .. 0.70, VDUMP 0.23 V at
VOUT = 0.6 V; local single-corner probes, not evidence), so the follower was replaced, not just re-biased.

### Changes

- `cp_bias`: `MR` (the PMOS resistor that sets Iref) 0.5u/4u -> 2.2u/4u. Iref is about 4.4x larger.
- `cp_dumpbuf`: the NMOS source follower is replaced by a unity-gain buffer: an NMOS-input and a
  PMOS-input 5-transistor OTA on one output node (complementary input range, so VOUT = 0.3 .. 0.9 V is
  covered at 1.08 .. 1.32 V supply), `VDUMP` fed back to both inverting inputs, tails from `IBN` and
  `IBP`, plus 4u/4u MOS capacitors from `VDUMP` to VSS and VDD. The cell gained an `IBIASP` pin; `cp`
  connects it to `IBP`. The cascoded current-steering legs (0006) are unchanged.

### Result (simulated, never measured)

`sim/cp-currents/results/20261106T182524Z/record.md`: batch fleet, ngspice, reduced corner set, same
criteria as above. **RESULT: PASS** (K1-K6).

| corner | I_up | I_dn | mismatch | leakage | VDUMP-VOUT at 0.3 / 0.6 / 0.9 V | dump slope | K_dl*I/C |
|---|---|---|---|---|---|---|---|
| tt/1.2 V/27 C | 9.13 uA | 11.07 uA | 19 % | 8 nA | +4 / -8 / -29 mV | 0.95 | 0.013 |
| ss/1.08 V/125 C | 5.14 uA | 6.44 uA | 22 % | 41 nA | +2 / -14 / -73 mV | 0.88 | 0.005 |
| ff/1.32 V/-40 C | 16.63 uA | 18.55 uA | 11 % | 3 nA | +8 / -2 / -14 mV | 0.96 | 0.091 |

K3 passes (41 nA against 2 % of 5.14 uA = 103 nA at ss/125 C). Margins are thin in two places and
should not be read as comfortable: ss I_up is 5.14 uA against the 5 uA floor, and ff K4 is 0.091
against the 0.1 limit (the allowed ff/ss current ratio is about 4.1; this design has 3.6). Mismatch is
near the 25 % limit at ss (22 %). Only the three reduced-set corners were run; no Monte Carlo, no
supply or temperature sweep, no layout.

### Consequence

The finding that `cp` does not fit is resolved on the schematic by this redraw. `reuse.lock.json` `cp`
stays `adopting` with `fit_gate` and `differs` updated: 0006 gives `pfd` and `cp` the same path to `kept`,
the `pfd` fit gate is still open (0011), and charge per pulse is not established. Lock time (#25 / #28)
is not graded here. The loop-gain consequence of the larger current is covered by K4 only.
