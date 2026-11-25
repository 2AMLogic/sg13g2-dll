# supervisor-smoke record (win_det setup-margin probe, issue #189)

**PROBE, not a graded spec result.** `sim/corners.json` states the reduced set
"is never a recorded result"; this run is a single-cell diagnostic and must not
be read as the supervisor's ss grade (the 45-corner grade is #41's).
Simulated, never measured.

## Question (issue #189, the diagnostic slice of #148)

The issue #145 ss probe measured `win_det`'s `b_up` sample (TAPH sampled by
REF, a `dffr_lv`) mis-latching high at ss / 1.080 V / 125 C on the committed
1 GHz smoke stimulus, where the tt control captures low. The no-fault phase of
that stimulus puts the TAPH falling edge 100 ps (50 % crossings of VDD) before
the second REF rising edge. **What TAPH-fall-to-REF-rise lead does the sampler
actually need at ss, and where does the committed 100 ps lead sit against
it — a cell-speed problem, or the documented near-lock "sample sits on the
sampling edge by construction" case (which is about d = T, not this d = 0.8 T
phase)?**

## Method

- Deck `decks/sup_setup.spice` = `design/netlist/supervisor.spice` (committed
  export at `ce8db57`, envelope `netlist_identity`
  `sha256:26a845ac36143b069870996309e4c81109146a10fd7fc13ad14d0bfc9e653b9d`)
  + a probe body that instantiates the committed `win_det` itself
  (`XWIN ref tapn taph over vdd 0 win_det`) with its supervisor-internal
  loads (REF drives `XIREF` + three `dffr_lv` clock inputs; TAPH drives
  `XBUP.D`) and the `XIPO` `inv_lv` load on `over` — the smoke bench's own
  loading, by construction.
- Stimulus reproduces the no-fault phase's timing: REF is the smoke bench's
  own clock (`Vck`, 0.5 ns base delay, 30 ps edges, 1 ns period, vdd-scaled),
  TAPN the unchanged 0.8 T copy, and TAPH **one** pulse whose fall 50 % point
  sits `lead` picoseconds before the second REF rise, shaped with the same
  30 ps linear slew. The lead is swept across units through the `Vlead` DC
  source via `corners.supply_v` (an alter, supported by every runner image)
  with `sim/harness/gridspec.py` zipping it beside the corner's Vdd row —
  `corners.params` is deliberately not used (fleet runner lag,
  `sim/harness/gridspec.py` docstring).
- Two requests: `requests/supss_setup.request.json` (ss, 22 leads: -50, -20,
  0, 20..160 in 10 ps steps, then 180, 200, 240, 300, 350, 400 ps) and
  `requests/suptt_setup.request.json` (tt control, 7 leads: -50, 0, 20, 40,
  60, 80, 100 ps). Negative lead = TAPH falls **after** the sampling edge,
  which must capture high at any corner (the probe's built-in positive
  control on its own failure mode).
- Grading: `bup_end` = `v(xwin.b_up)` settled at 2.4 ns — after the same
  (second) REF rise, before the third — read against 50 % of the corner's own
  rail from the envelope. Every unit's **true** lead is derived in this record
  from the recorded 50 % crossing times `t_ref_r2 - t_taph_f` (the actual pin
  crossings), never assumed from the source parameter; all 29 units measured
  their intended lead exactly (e.g. 100.000 ps at the nominal point, matching
  the 100 ps calculated from the committed `Vth08`/`Vck` PULSE parameters).
  `t_bup_r` (first `b_up` rise) errors exactly when `b_up` never crosses 50 %
  of the rail at all, which is the case from lead = 150 ps up in the ss
  sweep; those measurement errors are pass observations, not faults. It is
  **not** the capture-low marker: at leads 110-140 ps `b_up` does cross 50 %
  (`t_bup_r` = 1.65620 / 1.65627 / 1.65723 / 1.66143 ns) and then settles
  low (`bup_end` ≈ 0.31 mV). The `requests/*.request.json` `_comment` text
  that equates the `t_bup_r` error with capture-low is superseded by this
  sentence (the committed request files are left byte-identical as evidence).
- **Transient excursion on `b_up` (simulated).** The bracket above is a
  *settled-value* statement. `b_up` is not registered downstream
  (`design/netlist/supervisor.spice:45`, `XNO b_up a_up a_dn_n over_n …`),
  so a half-rail excursion on `b_up` propagates combinationally to
  `over_n`. In the ss sweep the first lead with no half-rail excursion at
  all is 150 ps; at 110-140 ps the cell captures low at the settled value
  but `b_up` has first crossed 50 % of the rail.
- Submitted through the grid/batch path (`--backend batch
  --wait-for-capacity 600`); batch jobs `klt-sim-ae3e48bc1700` (ss) and
  `klt-sim-80fcce40d3a0` (tt), ngspice 47 on the fleet. Committed evidence:
  both envelopes, the elaborated corner decks
  (`artifacts/supss_setup/`, `artifacts/suptt_setup/`), both requests and
  this record.

## Result

**The required lead is bracketed: at ss the sampler captures low only for
leads ≥ 110 ps and latches the stale high through 100 ps — the committed
no-fault phase's own lead is exactly 100 ps, so `b_up` falls on the failing
side by ≤ 10 ps. At tt the same cell needs only (60, 80] ps. The ss
mis-latch is a cell-speed problem, not the near-lock on-edge case.**

| lead (ps, from the recorded 50 % crossings) | ss `b_up` settled | tt `b_up` settled |
|---|---|---|
| -50 (TAPH falls after the edge) | high (latches stale 1) | high (latches stale 1) |
| -20 | high | not swept |
| 0 / 20 / 40 | high | high |
| 60 | high | **high (largest failing)** |
| 70 / 80 / 90 | high | 80: **low (smallest passing)** |
| 100 (the no-fault phase's own lead) | **high — the reproduced ss failure** | low |
| 110 / 120 / 130 / 140 | **low (smallest passing = 110)** | not swept |
| 150..400 | low | not swept |

(ss column: latch-high through lead = 100 ps, capture-low from 110 ps — a
10 ps-resolution bracket on the boundary; tt column: latch-high through 60 ps,
capture-low from 80 ps — a 20 ps-resolution bracket, and low again at the
nominal 100 ps, matching the committed tt record.)

- At the original phase (lead = 100 ps): **ss captures the stale high**
  (`bup_end` = 1.0801 V; `b_up` rises at 1.656 ns, byte-consistent with the
  #145 ss probe's 1.656 ns on the full supervisor) and **tt captures low**
  (`bup_end` = 0.14 mV), reproducing both committed observations on the
  isolated sampler.
- The ss unit at lead = 100 ps is the reproduced failure; the tt unit at
  lead = -50 ps is the probe's positive control (a lead that must fail at
  any corner does fail at tt too).

### Attribution

At ss the `dffr_lv` inside `win_det` needs a TAPH-fall-to-REF-rise lead
between 100 and 110 ps to sample TAPH low; the committed no-fault stimulus
(d = 0.8 T) provides exactly 100 ps (50 % crossings: TAPH falls 1.415 ns,
REF rises 1.515 ns). The margin budget of the phase is therefore consumed by
the ss setup window: a **cell-speed** failure of the sampler at the corner,
quantified here as a bracket, not a sampling-edge construction artefact. The
design note's "near lock (d = T) every sampled tap edge sits on the sampling
edge by construction" is a different, real condition (zero lead by design at
d = T); this phase (d = 0.8 T) has a designed 100 ps lead, and the
measurement shows ss eats precisely that 100 ps. The tt control on the
identical deck needs only (60, 80] ps, which is why the committed tt smoke
run captures low on the same stimulus.

## What this does and does not show

- **Shows (measured)**: the ss setup requirement of the committed `win_det`
  `b_up` sampler under the smoke bench's own slew (30 ps edges) and loads, as
  the bracket [largest failing = 100 ps, smallest passing = 110 ps]; the tt
  contrast [60, 80] ps; both committed #145 observations reproduced on the
  isolated cell at the original phase.
- **Does not show**: the other two `win_det` samplers (`a_up`, `a_dn`) — they
  were not the discriminator in #145; hold-time behaviour (TAPH rising
  through the clock edge); mismatch spread (Monte Carlo); any corner other
  than the two reduced-set points; the (1.5 T, 2 T) window logic.
- Results are simulated, never measured.
