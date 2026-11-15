# lock-detector-smoke record (ss probe, issue #145)

**PROBE, not a graded spec result.** `sim/corners.json` states the reduced set
"is never a recorded result"; this run is a single-corner diagnostic and must
not be read as the lock detector's ss grade (the 45-corner grade is #41's).
Simulated, never measured.

## Question (issue #145)

PR #141 (issue #136) shortened the shared `edgedet` one-shot from five inverter
stages to three device-level stages (`XMPD1..XMND3`, `sg13_lv_pmos w=1u l=0.16u`
/ `sg13_lv_nmos w=0.5u l=0.16u`). The lock detector consumes that one-shot
untested -- and it drives the plain `srlatch`'s S input **directly**
(`XLAT pt bad lockq lockqb`). At ss / 1.080 V / 125 C, does `pt` still set the
latch -- i.e. does LOCK rise at all after the stimulus goes clean?

## Method

- Deck `decks/probe.spice` = `design/netlist/lock_detector.spice` (as committed
  at `facba8b`; envelope `netlist_identity` `sha256:620133be...`, byte-identical
  to the tt re-run in `../20261115T184954Z`) + `decks/ld_body.spice`, the tt
  smoke bench's stimulus unchanged -- the stimulus is not what changed.
- Two units in one request (`requests/probe.request.json`): the **question unit**
  at ss (mos_ss; the bench's passive corner sections `cornerRES res_typ` +
  `cornerCAP cap_typ` kept typ, per `sim/corners.json`, whose corner axes are
  MOS x supply x temperature only) and a **control unit** at the bench's own tt
  corner (mos_tt / 1.2 V / 27 C), so every ss observation is read against what
  the identical stimulus and capture produce where the block is known to pass
  (LOCK sets at 351.1 ns in the committed tt record).
- Graded on crossing counts and 50 %-of-Vdd crossing times of twelve nodes --
  the stimulus (`ref`), the window sampler clock (`refd`) and samples (`s1`,
  `s2_n`), the VCTRL-movement sensor (`still`), the predicate (`good`, `bad`),
  the first counter bit (`q1`), the one-shot input and output (`to`, `pt`), the
  latch output and the block output (`lockq`, `lock`) -- **not** on the smoke
  request's tt-calibrated `.meas` windows. Crossing counting is
  corner-portable, so no tt offset was re-derived for this corner (issue #145
  finding 4 answered by construction).
- Submitted through the grid/batch path (`--backend batch
  --wait-for-capacity 600`); batch job `klt-sim-af993ac8a260`, ngspice 47 on
  the fleet.
- Per-node waveforms: `artifacts/probe/<corner>/crossings_N.raw` (full
  transient of each probed node) were produced and inspected for grading -- the
  stuck-level statements below quote them -- but are not committed: the repo
  ignores `*.raw` by policy. The committed evidence is the envelope (crossing
  counts and 50 % times per node) and the elaborated corner decks
  (`artifacts/probe/<corner>/corner.cir`).

## Result

**FAILURE -- the lock detector never sets LOCK at ss / 1.080 V / 125 C, and the
failure is upstream of the one-shot.** The VCTRL-movement sensor (`still`,
`vmov_cmp`) never asserts, so the predicate is never good, the counter is held
cleared, and the one-shot never receives an edge.

### ss unit (question corner)

| node | crossings (50 %) | behaviour |
|---|---|---|
| `ref` | 800 rises, 0.514..799.514 ns | stimulus toggles normally |
| `refd` | 800 rises, 0.650..799.649 ns | sampler clock alive (~136 ps delay at ss) |
| `s1` | 3 (60.846, 520.941, 580.847 ns) | toggles exactly at the three stimulus error transitions -- the s1 sampler works at ss |
| `s2_n` | 1 (rise 0.863 ns) | same pattern as tt (below): the s2 capture is constant by design in the steady state |
| `still` | 0, raw max 0.0058 V | **stuck low for the whole 800 ns** -- `vmov_cmp` never declares VCTRL still, not even in the quiet 220-520 ns window where tt declares it |
| `good` | 0 | stuck low (`bad` stuck high forces the inverse low) |
| `q1` | 0 | counter held cleared (`good` low clears it) |
| `to` | 0 | the counter never reaches 128 cycles |
| `pt` | 0 | raw max 0.0000 V -- dead flat |
| `bad` | 0 | stuck high (`NAND(s1, s2_n, still)` with `still`=0) |
| `lockq` | 0 | the plain `srlatch` is never set |
| `lock` | 0 | **LOCK never rises** |

### tt unit (control corner) -- same deck, same capture

| node | crossings (50 %) | behaviour |
|---|---|---|
| `ref` | 800 rises | identical stimulus |
| `refd` | 800 rises, 0.612..799.611 ns | alive (~100 ps delay at tt) |
| `s1` | 3 (60.736, 520.802, 580.738 ns) | same three transitions as ss -- the window samplers behave identically at both corners |
| `s2_n` | 1 (rise 0.749 ns) | same pattern as ss |
| `still` | 32 (63.075..220.904 ns) | bounces with the injected 50 MHz ripple, then **settles high at 220.9 ns** once VCTRL is quiet |
| `good` | 33 (61.212..581.205 ns) | predicate goes good as designed |
| `q1` | 551 (61.610..799.598 ns) | counter counts |
| `to` | 2 (rises 350.810, 709.811 ns) | 128th consecutive good cycle, twice |
| `pt` | 4 (350.888, 351.008, 709.889, 710.009 ns) | **one-shot fires twice, 119.9 ps wide at tt on this load** |
| `bad` | 35 (60.790..580.791 ns) | follows ripple and fault events |
| `lockq` | 3 (350.967, 520.997, 709.968 ns) | the plain `srlatch` sets while `pt` is still high (350.967 vs pt fall 351.008), falls on the injected error |
| `lock` | 3 (351.076, 521.102, 710.077 ns) | full expected sequence -- matches the committed tt record (351.1 / 521.1 / 710.1 ns) |

### Attribution

The ss failure isolates to `vmov_cmp`: `still` never asserts at ss (raw flat at
~0 V through the whole run) while the same node settles high at 220.9 ns in the
tt control on the identical stimulus. `still`=0 alone forces `bad`=1, so
`good` stays low and the counter is held cleared (`q1`, `to` flat); the
one-shot therefore never receives an edge and `lockq`/`lock` never move. The
digital window samplers (`s1`, `s2_n`) show the *same* crossing pattern at both
corners, so they are not the discriminator; the discriminator is the analog
VCTRL-movement sensor. The lock detector's set path (`pt` -> `srlatch` S) is
**unexercised** at ss -- no conclusion about it is possible from this run.

## What this does and does not show

- **Shows (measured)**: at ss / 1.080 V / 125 C, with the committed 1 GHz smoke
  stimulus, the lock detector never sets LOCK; `vmov_cmp` never declares VCTRL
  still; the one-shot (`pt`) never fires. Per issue #145's outcome clause this
  measured failure is recorded here and the remedy is filed as a follow-up
  issue (the `vmov_cmp` offset/sensor behaviour at ss needs its own decision
  record, which is out of scope here).
- **Does not show**: that the three-stage one-shot cannot flip the plain
  `srlatch` at ss -- `pt` never received an edge here, so the pair is
  unexercised at ss. The one-shot pulse itself was measured at ss for the PFD's
  loading in `sim/pfd-fit/results/20261115T125504Z/probe_ss.envelope.json`
  (179.1 ps). At tt this probe directly confirms the pair works: the 119.9 ps
  `pt` pulse sets the plain `srlatch` (`lockq` rises 350.967 ns, before `pt`
  falls at 351.008 ns).
- The tt re-run of the unchanged smoke bench on the three-stage `edgedet`
  passed -- see `../20261115T184954Z/record.md` (all five smoke gates green, so
  the regression this probe found is ss-only). The `lock_max_before_220n`
  unit-column quirk noted in the bench README (a volt value under the shared
  summariser's single unit column) appears there again and is the known
  summariser behaviour, not a new defect.
