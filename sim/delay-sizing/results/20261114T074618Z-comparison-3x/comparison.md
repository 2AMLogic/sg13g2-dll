# Delay-tap candidate B at 3x widening vs the committed 4x result

**SIMULATED, never measured.** Issue #114, the follow-up run that
`results/20261107T231500Z-comparison/comparison.md:77` asked for ("B's scale (3x vs 4x)
is not optimised; a 3x full-grid run should precede sizing"). Decision 0010 stays
`proposed`; no spec row, schematic, netlist or decision status changes here, and **this note
makes no recommendation between candidates A and B** — that ruling is the operator's, on #58.

Method = the `sim/delay-sanity` bench, unchanged from the 4x run: ideal control sources
(VBN = Vc, VBP = Vdd - Vc), ideal 20 fF load on every tap buffer, single-event T0->Tk first
edge at 50 % of Vdd, reduced corner set (ss/1.08 V/125 C, tt/1.2 V/27 C, ff/1.32 V/-40 C),
batch fleet. "Mean step" = (d8 rise-in + d8 fall-in) / 16. **Criterion**, as in the 4x
comparison: mean tap step reaches T/8 = 125 ps at ss/1.08 V/125 C/1 GHz with Vc at least
100 mV from both rails, i.e. Vc <= 0.98 V at ss (`summarize.py:14`, `RAIL = 0.1`, applied at
`:108` — computed by the summarizer, not hand-derived here).

Records this note quotes (append-only siblings; every number is quoted from them, none is new):

- `20261114T071858Z-full/` **3x**, A and B x ss/tt/ff x 1 GHz/500 MHz, Vc 0.3..1.08
- `20261114T073524Z-mc/` **3x**, Monte Carlo matching at ss/1 GHz, n = 32, seed 20261107
- `20261107T222553Z-full/`, `20261107T224325Z-mc/`, `20261107T221844Z-probe/` the committed **4x** records
- `area.txt` beside this file, from `area.py` run against the **new 3x** deck

**Tool versions.** Both new runs: `klt 0.9.2.dev1025+ga90545db9ea6 ; B scale 3` (each
directory's own `tool-versions.txt`), ngspice 46 on the batch fleet. The committed 4x run
used client klt `0.9.2.dev247+g6c8de4e4f36a`. The runs are therefore **not** on identical
client versions — see "Cross-checks" below for what makes them comparable anyway.

## What was simulated

B at 3x = the drawn two-stage `delay_cell` with the four starving devices (MPH1/MPH2 head
PMOS, MNT1/MNT2 tail NMOS) widened **3x** instead of 4x: 1.5 u -> 4.5 u and 0.75 u -> 2.25 u
(verified in `20261114T071858Z-full/decks/dl_b_1GHz.spice`, whose header reads
`variant b scale 3.0`). Everything else is as drawn. 8 cells + 1 dummy, tap buffers as drawn.
`design/` is untouched; the decks are derived from the committed `design/netlist/*.spice` by
`make_bench.py`.

## The answer

**Yes — 3x reaches 125 ps at ss/1.08 V/125 C/1 GHz with Vc at least 100 mV from both rails,
but with materially less margin than 4x.**

Inside the usable window (Vc <= 0.98 V), the 3x mean tap step spans **122.0..208.2 ps**, which
contains 125 ps; `20261114T071858Z-full/record.md` records `b_1GHz_ss` as T/8 **covered**. The
125-ps crossing is at **Vc ~ 0.86 V** (linear interpolation between the 0.80 V / 130.1 ps and
0.90 V / 122.0 ps grid points — the same interpolation the 4x comparison used, which reproduces
its own quoted 0.77 V for B and 0.79 V for A exactly). That point sits **0.86 V above the lower
rail and 0.22 V below the 1.08 V upper rail**, so both distances clear the 100 mV criterion.

The qualification: at 3x the fastest usable point is only just inside the criterion. **122.0 ps
at Vc = 0.90 V is 2.4 % under 125 ps**, against 7.4 % for 4x (115.8 ps at the same Vc). Only
0.117 V of control range remains between the 125-ps point and the window edge, against 0.208 V
at 4x.

## 3x vs 4x at ss/1.08 V/125 C/1 GHz (mean tap step)

From `20261114T071858Z-full/record.md` (3x) and `20261107T222553Z-full/record.md` (4x):

| Vc (V) | B 3x (ps) | B 4x (ps) | A (ps) |
|---|---|---|---|
| 0.50 | no edge | no edge | no edge |
| 0.60 | 208.2 | 172.7 | no edge |
| 0.70 | 148.6 | 134.0 | 164.8 |
| 0.80 | 130.1 | 121.5 | 119.5 |
| 0.90 | **122.0** | **115.8** | 99.5 |
| 1.00 | 117.5 | 112.6 | 89.6 |
| 1.08 | 115.1 | 110.9 | 84.8 |

Rows at Vc = 1.00 and 1.08 V are **outside** the 100 mV window at ss and are shown for
continuity only. A's column is reproduced from the 3x run itself (see "Cross-checks").

### Headroom against 125 ps, both framings

| Figure | B 3x | B 4x |
|---|---|---|
| Fastest mean step **inside** the usable window (Vc <= 0.98 V) | 122.0 ps at Vc = 0.90 V (**2.4 %** under 125 ps) | 115.8 ps at Vc = 0.90 V (**7.4 %**) |
| Fastest mean step at **any** Vc, incl. Vc = 1.08 V | 115.1 ps (**7.9 %**) | 110.9 ps (**11.3 %**) |
| Vc reaching 125 ps (interpolated) | ~0.86 V | ~0.77 V |
| Vc distance from lower / upper rail at that point | 0.86 V / 0.22 V | 0.77 V / 0.31 V |
| Control range left between the 125-ps point and the window edge | 0.117 V | 0.208 V |

The 4x comparison's headline "about 11 % headroom" is the **any-Vc** figure (110.9 ps at
Vc = 1.08 V), which is itself outside the 100 mV window it states as the criterion. Stated on
the same basis, 3x gives 7.9 %. Stated on the window-restricted basis — the one the criterion
actually implies — 4x gives 7.4 % and 3x gives 2.4 %. Both rows are tabulated above so the
comparison is not sensitive to which framing is read; the committed 4x record is not edited
(append-only).

## Usable Vc window and dead zone, 3x, all six grid points

Window = Vc at least 100 mV from both rails with an edge at every tap, from
`20261114T071858Z-full/record.md`.

| corner / f | B 3x dead zone | B 3x mean step range in window | T/8 in window? |
|---|---|---|---|
| ss / 1 GHz | Vc <= 0.50 | 122.0..208.2 (Vc 0.6..0.9) | covered |
| tt / 1 GHz | Vc <= 0.50 | 74.4..166.0 (0.6..1.08) | covered |
| ff / 1 GHz | Vc <= 0.50 | 50.4..121.8 (0.6..1.08) | NOT covered (coarse grid, see below) |
| ss / 500 MHz | Vc <= 0.40 | 122.0..445.0 (0.5..0.9) | covered |
| tt / 500 MHz | Vc <= 0.40 | 74.4..418.4 (0.5..1.08) | covered |
| ff / 500 MHz | Vc <= 0.40 | 50.4..315.1 (0.5..1.08) | covered |

At 3x the dead-zone top is Vc <= 0.50 V at 1 GHz and <= 0.40 V at 500 MHz — the same as 4x at
1 GHz, and the same at 500 MHz.

**The ff / 1 GHz "NOT covered" line is a grid artifact, not a new result, and it is not the
question this issue asks.** Every point in the 3x ff / 1 GHz window is *faster* than 125 ps
(50.4..121.8 ps), so the 0.1 V grid has stepped over the dead-zone edge where the crossing
lies — exactly the limitation the committed comparison records for its own coarse ff lines and
the reason `20261107T223944Z-fine/` exists. 4x shows the mirror-image artifact: its coarse
grid prints ff / 1 GHz covered and ff / 500 MHz NOT covered. **A 3x `fine` run was not
performed**: the acceptance criterion is ss / 1 GHz, the 3x ss window is resolved cleanly on
the coarse grid (edges at every point from 0.60 V up), and scales other than 3x and grids
beyond what the criterion needs are out of this issue's scope. **No ff claim for 3x should be
read off the table above**; if ff at 1 GHz becomes load-bearing for sizing, a 3x `fine` run is
the thing to do and has not been done.

## Per-tap step sigma (random mismatch)

`20261114T073524Z-mc/record.md` vs the committed `20261107T224325Z-mc/record.md`.

**Method, stated with the numbers:** ss/1.08 V/125 C, 1 GHz, **Vc = 1.0 V**, `mos_ss_mismatch`
process section, mismatch-only Monte Carlo (`--mc-vary mismatch`), **n = 32**, **seed
20261107**, ideal bias sources, no layout parasitics. Estimator = sample standard deviation of
the per-tap step across the 32 samples, as computed by `summarize.py`. The seed, n and Vc are
the runner's committed defaults, so the 3x run used the same seed policy as the 4x run by
construction (`run.sh:83-84`). **Vc = 1.0 V is near the fast end and is not at either
candidate's 125-ps point** — the same caveat the 4x record carries; at 3x it is also outside
the 100 mV usable window, so these sigmas are a matching comparison at a common bias point,
not a sigma at the operating point.

| | B 3x | B 4x | A (3x run) |
|---|---|---|---|
| Per-tap step sigma | 12.55..16.98 ps | 12.45..16.90 ps | 8.19..15.08 ps |
| Per-tap step sigma / mean | 10.70..14.51 % | 11.08..15.05 % | 8.77..18.86 % |
| sigma of d8 | 19.29 ps | 19.11 ps | 15.32 ps |
| Per-sample max \|step - line-mean step\| (rising input) | mean 25.08, max 45.16 ps | mean 24.82, max 44.89 ps | mean 26.10, max 49.79 ps |
| Mean step at Vc = 1.0 V, tap 1..8 | 113.6..121.1 ps | 108.7..115.4 ps | 78.1..99.1 ps |

**Negative control** (`mos_ss`, no mismatch, same seed and n), the validity check for the
column above: sigma exactly 0 across samples and identical on repeat, **True for both A and B**
in the 3x run — matching the 4x run's control. The mc run completed with no diagnostics or
errors.

**3x and 4x are not distinguishable on random mismatch.** At n = 32 a sigma estimate carries
roughly 13 % relative uncertainty, and the two scales' per-tap sigmas (12.55..16.98 vs
12.45..16.90 ps) and sigma(d8) (19.29 vs 19.11 ps) differ by far less than that. Widening the
starving devices 3x rather than 4x does not measurably change B's mismatch sigma on this bench.
As in the 4x record, sigma(d_k) does not grow as sqrt(k), so a large share of the spread is
common to the line; this bench cannot separate that, and none of this is a layout-matching
result.

## Device area (schematic estimate)

Sum of W x L x ng x m over the line's devices (9 cells including the dummy + 9 tap buffers),
from the decks. **A schematic estimate, not layout area** — no spacing, wells, routing or guard
rings. From `area.txt` beside this file, run against the **new 3x** deck:

| variant | device area | vs drawn (14.92 um^2) |
|---|---|---|
| drawn `delay_cell` | 14.92 um^2 | - |
| A | 10.53 um^2 | -29 % |
| **B 3x** | **25.45 um^2** | **+71 %** |
| B 4x | 30.71 um^2 | +106 % |

3x costs **5.26 um^2 less than 4x** (-17.1 %), i.e. +71 % over drawn instead of +106 %. Per
cell: 2.145 um^2 at 3x against 2.730 um^2 at 4x and 0.975 um^2 drawn.

## Supply current

Mean I(Vdd) over 6..10 ns (an integer number of clock periods, line toggling); includes the
toggling 20 fF tap loads and tap buffers, excludes the ideal bias sources, so it is **not** a
bias-generator budget. At ss/1 GHz, B 3x draws 441 uA at Vc = 1.08 V and 441 uA at Vc = 0.80 V;
at 500 MHz (ss, Vc = 1.08 V) 221 uA. These are the same figures the 4x run recorded (441 uA and
221 uA). Most of it is load switching (9 x 20 fF x 1.08 V x 1 GHz is about 195 uA), so the
starving-device scale does not move the line's current at this bias.

## Cross-checks

- **Candidate A reproduces exactly across the two runs.** `run.sh full` re-runs A as well, and
  A is scale-independent, so its rows are a free consistency check between the 4x run (client
  klt 0.9.2.dev247) and this 3x run (dev1025). All six of the 3x run's A tags match the
  committed 4x record figure for figure: fastest mean step 84.8 ps (ss/1 GHz), 57.5 (tt/1 GHz),
  40.6 (ff/1 GHz), 84.9 (ss/500 MHz), 57.5 (tt/500 MHz), 40.6 (ff/500 MHz), with identical
  dead-zone tops and identical window step ranges (e.g. ss/1 GHz 99.5..164.8 ps). A's mc table
  is identical row for row to the committed one (per-tap sigma 8.19..15.08 ps, sigma(d8)
  15.32 ps, per-sample max mean 26.10 / max 49.79 ps). Nothing in the bench moved between the
  two runs, and the client-version difference above did not change a single number.
- **Area arithmetic.** 25.45 um^2 is `area.py`'s own output. It is independently reproduced from
  the deck geometry: four starving devices at 4.5 u x2 and 2.25 u x2, L = 0.13 u, so
  cell = 0.975 - 0.585 + 3 x 0.585 = 2.145 um^2 and line = 9 x (2.145 + 0.683) = 25.45 um^2.
  The same arithmetic reproduces the committed 1x (14.92) and 4x (30.71) figures.
- **The 3x deck is the 3x deck.** Every probe scale writes the same filename, so the
  `20261107T221844Z-probe/` B deck is scale 4.0 and would silently re-report the 4x area.
  `area.txt` here points at `20261114T071858Z-full/decks/dl_b_1GHz.spice`, whose header reads
  `variant b scale 3.0` and whose starving devices are `w=4.5u` / `w=2.25u`.

## Run status: the `full` exit code

`DS_B_SCALE=3 run.sh full` exited **1**, as the 4x run did, and **the run is valid**: all 519
diagnostics in `20261114T071858Z-full/record.md` are `measurement '...' produced no value`
(ngspice "out of interval"), and all of them are at Vc in {0.300, 0.400, 0.500, 0.600} — the
dead zone, where no edge reaches the tap. There is no other error class in the record. This is
the documented behaviour (`README.md`: "`full` exits non-zero by design: Vc points in the dead
zone produce no edge"); those points are recorded as "no edge", not dropped. Per-tag pass
counts (5/9 to 7/9) account for exactly those Vc points. `run.sh mc` exited **0** with no
diagnostics.

Both grids ran on the batch fleet (`backend batch` and a job id on every tag in the records);
no submit hit `batch_no_capacity`, and no part of either grid was run locally.

## What this note does not do

- It does **not** recommend between A and B, and does not revisit the 4x comparison's
  recommendation. Both are the operator's call on #58.
- It does **not** change decision 0010's status, any `spec/` row, `design/delay_cell.sch`, or
  any committed netlist.
- It does **not** supersede or edit any committed record. It sits beside them; `results/` is
  append-only.
- It does **not** establish an ff / 1 GHz result for 3x (see the coarse-grid note above), a
  sigma at the 125-ps operating point (the mc bias is Vc = 1.0 V), a layout area, or anything
  about extracted layout, loaded or non-ideal taps, real bias generation or jitter — none of
  which this bench simulates.
