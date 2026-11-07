# Delay-tap sizing comparison: A (one stage per tap) vs B (two stages, widened starving devices)

**SIMULATED, never measured.** Issue #67, operator ruling r7-q57 on #58. Decision 0010 stays `proposed`; no spec row, schematic or decision status changes here (ratification is the operator's, on #58).

Method = the `sim/delay-sanity` bench (ideal VBN = Vc, VBP = Vdd - Vc, ideal 20 fF tap loads, single-event delay at 50 % of Vdd), reduced corner set (ss/1.08 V/125 C, tt/1.2 V/27 C, ff/1.32 V/-40 C), batch fleet (ngspice 46). Client klt is 0.9.2.dev (the 0010 baseline says runner klt 0.9.0); the version used is in each directory's `tool-versions.txt`. "Mean step" = (d8 rise-in + d8 fall-in) / 16; "step min..max" = every tap step, both input edges. Every number below is quoted from the records, none is new.

Records (append-only, siblings of this file):
- `20261107T221844Z-probe/` scale probe and bench regression (ss, 1 GHz, Vc 0.8/1.0/1.08)
- `20261107T222553Z-full/` A and B x ss/tt/ff x 1 GHz/500 MHz, Vc 0.3..1.08
- `20261107T223944Z-fine/` finer Vc grid at ff
- `20261107T224325Z-mc/` Monte Carlo matching at ss/1 GHz

## Candidates as simulated

- **A**: stage 1 of the drawn `delay_cell` alone (MPH1/MP1/MN1/MNT1, as drawn) is the whole cell; 8 cells + 1 dummy; tap buffers as drawn. Decks are derived from the committed `design/netlist/*.spice` by `make_bench.py`; `design/` is untouched.
- **B**: the drawn two-stage cell with the four starving devices (MPH1/MPH2 head PMOS, MNT1/MNT2 tail NMOS) widened **4x** (1.5 u -> 6 u, 0.75 u -> 3 u); everything else as drawn. Scale chosen from the probe (ss/1 GHz, mean step at Vc = 1.0 / 1.08): 1.5x 140.0*/132.6 ps, 2x 127.5/123.8 ps, 3x 117.5/115.1 ps, 4x 112.6/110.9 ps; drawn 158.7/150.4 ps. (*see `20261107T221844Z-probe/record.md` for every probe row.) 2x does not reach 125 ps with Vc at least 100 mV from the rail (Vc <= 0.98 V); 3x does with about 6 % to spare; 4x was taken for about 11 % to spare. The scale is a probe result, not an optimum, and 3x was not run on the full grid.
- **Bench regression**: the drawn cell in the new bench at ss/1 GHz, Vc = 1.08, rising input, d8 = 1205.9 ps, identical to `sim/delay-sanity/results/20261105T080322Z/` (1205.9 ps, 150.7 ps/tap).

## Does either reach T/8 at ss/1 GHz? (mean tap step, `20261107T222553Z-full/record.md`)

| Vc (V) | drawn (probe) | A | B (4x) |
|---|---|---|---|
| 0.60 | - | no edge | 172.7 |
| 0.70 | - | 164.8 | 134.0 |
| 0.80 | 209.9 | 119.5 | 121.5 |
| 0.90 | - | 99.5 | 115.8 |
| 1.00 | 158.7 | 89.6 | 112.6 |
| 1.08 | 150.4 | 84.8 | 110.9 |

Both reach 125 ps with Vc at least 100 mV from both rails (Vc <= 0.98 V at ss): A at about Vc = 0.79 V, B at about 0.77 V (linear interpolation between the grid points). The drawn cell does not (fastest 150.4 ps). 0010's "roughly 75 ps" extrapolation for A was optimistic: A's fastest mean step is 84.8 ps (its fastest single step 75.7 ps).

### Usable Vc window and dead zone

Window = Vc at least 100 mV from both rails with an edge at every tap (coarse grid from `-full`, 0.04 V grid from `-fine` at ff).

| corner / f | A: dead zone | A: mean step range in window | B: dead zone | B: mean step range in window |
|---|---|---|---|---|
| ss / 1 GHz | Vc <= 0.60 | 99.5..164.8 (Vc 0.7..0.9) | Vc <= 0.50 | 115.8..172.7 (0.6..0.9) |
| tt / 1 GHz | Vc <= 0.60 | 57.5..136.8 (0.7..1.08) | Vc <= 0.50 | 71.2..131.8 (0.6..1.08) |
| ff / 1 GHz | Vc <= 0.60 | 94.2..151.3 (0.64..0.72, fine) | Vc <= 0.48 | 61.0..179.2 (0.52..0.72, fine) |
| ss / 500 MHz | Vc <= 0.50 | 99.7..311.0 (0.6..0.9) | Vc <= 0.40 | 115.8..336.1 (0.5..0.9) |
| tt / 500 MHz | Vc <= 0.50 | 57.5..276.9 (0.6..1.08) | Vc <= 0.40 | 71.2..304.2 (0.5..1.08) |
| ff / 500 MHz | Vc <= 0.52 | 94.2..299.5 (0.56..0.72, fine) | Vc <= 0.44 | 61.0..290.2 (0.48..0.72, fine) |

"Dead zone" is "no edge measured". At 1 GHz some of it may be pulse swallowing in the 0.5 ns half-period rather than a device that does not switch: it is the same method and the same reading as the baseline.

The coarse 0.1 V grid steps over the dead-zone edge at ff, so `-full/record.md` prints "NOT covered" for ff (A at both frequencies, B at 500 MHz). The finer grid in `-fine/` shows T/8 is reached in all four ff cases (A 1 GHz 94.2..151.3 ps contains 125; A 500 MHz 94.2..299.5 contains 250; B 61.0..179.2 and 61.0..290.2). The coarse lines are superseded by the fine records, not edited (append-only).

**500 MHz fallback**: T/8 = 250 ps is spanned at ss, tt and ff by both A and B (ss/tt in `-full`, ff in `-fine`). **1 GHz** is spanned at ss, tt and ff by both.

## Matching

- **Systematic (nominal) step equality.** B's taps are uniform. At ss/1 GHz, Vc = 0.8 the 16 steps (8 taps x 2 edges) span 120.2..130.4 ps; at Vc = 1.0, 111.5..119.7 ps. A alternates by construction, because an inverting stage has different tpHL and tpLH. At ss/1 GHz, Vc = 0.8: 111.3..144.2 ps (rising-output steps 116.7..144.2, falling-output 111.3..142.1); at Vc = 1.0: 80.4..107.8 ps (rise-out 93.7..107.8, fall-out 80.4..94.8). At ff/1 GHz, Vc = 0.68 (fine) A's rising-output steps are 78.8..126.3 ps and falling-output 140.8..181.4 ps (mean 117.8 ps); B at its 125-ps point (Vc = 0.56) spans 119.2..156.2 ps. A's rise-in and fall-in d8 also differ, e.g. ss/1 GHz, Vc = 0.7: 1359.2 vs 1277.0 ps (82 ps, duty-cycle distortion at the line end); B's differ by about 1 ps. This is a topology property, independent of layout.
- **Random mismatch** (`20261107T224325Z-mc/`): ss/1.08 V/125 C, 1 GHz, **Vc = 1.0 V** (near the fast end, not at either candidate's 125-ps point), `mos_ss_mismatch`, mismatch-only, n = 32, seed 20261107, ideal bias, no layout parasitics. Negative control on `mos_ss` (same seed and n): sigma exactly 0 and identical on repeat, for A and B. Per-tap step sigma: A 8.2..15.1 ps (8.8..18.9 % of the mean step), B 12.5..16.9 ps (11.1..15.1 %); sigma of d8: A 15.3 ps, B 19.1 ps. At n = 32 a sigma estimate carries about 13 % relative uncertainty, so A and B are **not distinguishable on random mismatch**; if anything B's absolute sigma is slightly larger (more devices per tap). sigma(d_k) does not grow as sqrt(k) in either candidate, so a large share of the spread is common to the line; this bench cannot separate that, and it is not a layout-matching result.
- **Not simulated**: extracted layout, loaded or non-ideal taps, real bias generation (Vc -> VBP/VBN spread), jitter.

## Area and current (estimates)

- **Device area** (sum of W x L over the line's devices: 9 cells including the dummy + 9 tap buffers, from the decks; schematic estimate, **not layout area**; `area.txt`): drawn 14.92 um^2; **A 10.53 um^2 (-29 %; the delay cells alone -50 %)**; **B 30.71 um^2 (+106 %)** at 4x.
- **Supply current** (mean I(Vdd) over 6..10 ns, an integer number of clock periods; includes the toggling 20 fF tap loads and tap buffers, excludes the ideal bias sources, so it is not a bias-generator budget): ss/1 GHz at Vc = 1.08 V: A 395 uA, B 441 uA, drawn 440 uA; at Vc = 0.8 V: A 392 uA, B 441 uA. At 500 MHz (ss, Vc = 1.08): A 197 uA, B 221 uA. Most of it is load switching (9 x 20 fF x 1.08 V x 1 GHz is about 195 uA), so the candidates differ by about 10 %.

## Candidate A: tap polarity (the PFD and tap-select side must handle)

Odd stages invert; T0 is the (non-inverting) input buffer:

| tap | T0 | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 |
|---|---|---|---|---|---|---|---|---|---|
| polarity vs T0 | + | - | + | - | + | - | + | - | + |

A rising T0 edge gives a falling edge at T1, T3, T5, T7 and a rising edge at T2, T4, T6, T8 (the bench measures each tap against its own edge direction). Correction to the issue/0010 text: **T8 is not inverted** (eight inverting stages are non-inverting), so the T0 -> T8 one-period comparison keeps its polarity. Every odd tap handed to the PFD / tap-select or to the 0008 false-lock logic is an inverted copy: it must be re-inverted or compared on the opposite edge, and the rise/fall step alternation above then appears as alternating tap spacing. B has no such pattern (all taps +, uniform steps). 0008 and the PFD interface (#30) are not edited here.

## Recommendation (for the operator to ratify on #58)

- **Both meet 125 ps at ss/1.08 V/125 C/1 GHz** with Vc at least 100 mV from the rails; speed does not eliminate either. Both also span T/8 at 500 MHz at all three corners and at 1 GHz at tt and ff.
- **A** has the smallest area (-29 % vs drawn) and the most speed headroom (fastest 84.8 ps vs 125 ps; B 110.9 ps), but its steps are systematically unequal (single steps 111..144 ps around a 119.5 ps mean at ss/Vc = 0.8; 79..126 vs 141..181 ps rise/fall-output at ff), it distorts duty cycle at the line end, and it needs the tap-polarity handling in 0008/#30. Its random mismatch is no better than B's.
- **B (4x)** has uniform steps and no polarity handling, at 2x the device area (14.92 -> 30.71 um^2) and only about 11 % headroom against 125 ps at ss.
- **No candidate wins both matching and area.** Recommendation: **B**. Phase spacing is this block's accuracy product, A's unequal steps are structural (matched layout cannot remove them), and B's cost is about 16 um^2 of extra device area. **A is the alternative** if area or speed headroom proves decisive, accepting the polarity and spacing work. B's scale (3x vs 4x) is not optimised; a 3x full-grid run should precede sizing.
- Not decided here: ratification of 0010, `spec/` rows, `design/delay_cell.sch`, 0008, #30.
