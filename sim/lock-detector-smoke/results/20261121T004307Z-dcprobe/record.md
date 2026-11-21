# lock-detector-smoke record (vmov_cmp DC probe, issue #189)

**PROBE, not a graded spec result.** `sim/corners.json` states the reduced set
"is never a recorded result"; this run is a diagnostic of one cell and must not
be read as the lock detector's corner grade (#41's). Simulated, never measured.

## Question (issue #189, the diagnostic slice of #148)

The issue #145 ss probe measured that `vmov_cmp` never asserts `still` at
ss / 1.080 V / 125 C on the committed 1 GHz smoke stimulus (flat at ~0 V for
800 ns, where the tt control settles high). Is that a dynamic failure (ripple,
low-pass settling) or a DC bias failure — and does the sensor have a valid
quiet operating point anywhere at each reduced-set corner?

## Method

- Deck `decks/vmov_dc.spice` = `design/netlist/lock_detector.spice` (committed
  export at `ce8db57`, envelope `netlist_identity`
  `sha256:e47a1e19b488181922ef6d4b69fceb061e2c82b680450f580bd5315bbbd9aa04`)
  + a probe body that instantiates `XDUT vctrl still vdd 0 vmov_cmp` alone.
- Analysis `.dc Vctrl 0 1.32 0.005` (265 points; 0.585 / 0.600 / 0.615 / 0.850
  are on-grid). In DC the low-pass cap (`XCL`) is open, so `vsb = vsb0 = vsa`
  by construction: the swept quantity is the OTA pair's **common-mode input**
  and `STILL(VCTRL)` is the sensor's **settled quiet window** — exactly the
  state a locked, quiet loop presents. Operating points are read with
  `FIND ... AT=` at the smoke stimulus's quiet input 0.600 V, the ripple band
  edges 0.585 / 0.615 V, and the documented ~0.85 V validity ceiling
  (`design/NOTES.md` "Lock detector").
- Three units in one request (`requests/vmov_dc.request.json`): the reduced
  set's tt / ss / ff points (composed by `sim/harness/gridspec.py
  --reduced-set`, the passive sections `cornerRES res_typ` + `cornerCAP
  cap_typ` added beside each MOS section exactly as the bench's own
  `requests/ld.request.json` carries them).
- Transitions are identified where each output crosses 50 % of the corner's own
  rail (`v(half)`, a behavioural node), never a per-corner literal, so the one
  request grades every corner. An errored `WHEN` card would report "no such
  transition over the range"; none occurred — every transition named below
  exists and is quoted.
- The OTA tail currents **cannot be carried by any `klt sim` measurement form
  as shipped**: an OSDI instance vector (`@m.xdut.xmta[id]`) saves but never
  prints (engine-side, ngspice 47 + PSP103 OSDI; gap filed per this repo's
  friction protocol as 2AMLogic/klayout-tools#6997, reproducer included there).
  The block's whole supply current `i(vdd)` through its VDD pin and the
  internal node voltages (`vsa`, `vsb`, `tla`, `tlb`, `oa`, `ob`, `oab`,
  `obb`) are recorded instead; the tail devices' bias is documented by their
  source nodes `tla`/`tlb`.
- Submitted through the grid/batch path (`--backend batch
  --wait-for-capacity 600`); batch job `klt-sim-ecd57d83bb12`, ngspice 47 on
  the fleet, all three corners `pass` (no diagnostics). Committed evidence:
  the envelope, the elaborated corner decks
  (`artifacts/vmov_dc/<corner>/corner.cir`), the request and this record.

## Result

**At ss the sensor has no valid quiet operating point at the smoke VCTRL: the
settled `STILL=1` window is [0, 0.477) V, and the whole smoke band
(0.585..0.615 V) sits outside it. The failure is DC bias, not dynamics.**

### Operating point at the quiet smoke input, VCTRL = 0.600 V

| quantity | tt / 1.200 V / 27 C | ss / 1.080 V / 125 C | ff / 1.320 V / -40 C |
|---|---|---|---|
| `vsa` (instantaneous copy, OTA input) | 0.1201 V | 0.1400 V | 0.1183 V |
| `vsb` (low-passed copy, OTA input) | 0.1201 V | 0.1400 V | 0.1183 V |
| `vsa` at the 0.85 V ceiling | 0.2546 V | 0.2795 V | 0.2519 V |
| OTA-A output `oa` | 0.617 V | 0.580 V | 0.632 V |
| OTA-B output `ob` | 0.617 V | 0.580 V | 0.632 V |
| `oab` (`oa` through `inv_lv`) | 0.700 V | 0.260 V | 1.209 V |
| `obb` (`ob` through `inv_lv`) | 0.700 V | 0.260 V | 1.209 V |
| tail source nodes `tla`/`tlb` | 0.856 V | 0.802 V | 0.897 V |
| block supply current `i(vdd)` | 128 µA | 65 µA | 194 µA |
| **`STILL`** | **1.200 V (asserted)** | **1 µV (dead low)** | **1.320 V (asserted)** |

Both OTA outputs sit mid-swing near their load inverter's trip at every
corner; the residual relative to that trip decides `STILL`. At ss the
common-mode leaves `oa = ob = 0.580 V` a few mV **above** the ss inverter trip
(`oab = obb = 0.26 V`, both "moved" flags active-low), so
`still_n = NAND(0.26, 0.26)` is high and `STILL` is held low — statically,
for any differential the ripple could present. At ff the same bias sits well
below the trip (`oab = obb = 1.209 V`) and `STILL` is asserted with margin.

### Settled `STILL(VCTRL)` window and transitions (50 % of the corner rail)

| corner | `STILL` at 0.585 V | at 0.600 V | at 0.615 V | at 0.850 V | falls (`still_f1`) | rises (`still_r1`) | `oab` falls / rises | `obb` falls / rises |
|---|---|---|---|---|---|---|---|---|
| tt | 1.200 V | 1.200 V | 0.008 V | 0 V | **0.6125 V** | 1.1923 V | 0.6290 / 1.1810 V | 0.6290 / 1.1811 V |
| ss | 1 µV | 1 µV | 1 µV | 1 µV | **0.4774 V** | 1.0925 V | 0.4954 / 1.0862 V | 0.4954 / 1.0862 V |
| ff | 1.320 V | 1.320 V | 1.320 V | 1.222 V | **0.8523 V** | 1.1725 V | 0.8766 / 1.1499 V | 0.8767 / 1.1497 V |

Sweep range 0..1.32 V at 5 mV resolution; every window edge is bracketed to
the 5 mV grid. `still_max` over the documented validity window [0, 0.85] V is
the rail at every corner, so a flip point exists at all three — the question
is where: at tt the quiet window's **upper edge is 0.6125 V, only 12.5 mV
above the smoke stimulus's nominal 0.600 V** (and the +15 mV ripple edge,
0.615 V, is already outside it — the committed tt transient still settles high
because the 10 ns low-pass attenuates the 50 MHz ripple before the OTAs see
it, which is a dynamic save, not a DC margin); at ss the window edge has moved
**down to 0.4774 V**, so the smoke VCTRL — and any locked VCTRL above
~0.48 V — reads "moved" forever; at ff the edge is at 0.8523 V, just above the
documented ceiling, and the band is comfortably inside.

### Attribution

The ss lock-detector failure measured by #145 is a **static common-mode
failure of the deliberate-offset trim**, the exact fragility
`design/NOTES.md` "Lock detector" documents ("the VCTRL threshold is a trim,
not a spec... random mismatch is wider than that window"): the 3.59 µm/4 µm
width trim parks the OTA outputs a few tens of mV from the load inverters'
trip at tt and ff, and the ss bias shift (slower devices, 1.08 V rail, 125 C)
pushes both outputs to the wrong side at VCTRL ≈ 0.6 V for the whole
[0.477, 1.09] V span. No ripple, settling or counter behaviour is involved:
`STILL` cannot assert at ss at the smoke operating point even in perfect
quiescence, which is what the #145 transient observed as "flat at ~0 V for
800 ns".

## What this does and does not show

- **Shows (measured)**: at tt / ss / ff, the committed `vmov_cmp`'s settled
  quiet window in VCTRL, its operating point at the smoke input, and the
  transition voltages of `STILL`, `oab` and `obb`; that the ss failure of
  issue #145 is a DC-bias window collapse (valid window [0, 0.477) V at ss),
  not a dynamic one; that even the tt margin at the nominal 0.600 V is 12.5
  mV of common-mode.
- **Does not show**: the movement **threshold** (the ±5 mV differential the
  trim is meant to enforce) — the two follower inputs cannot be separated
  without editing the committed subcircuit, and in a settled DC sweep they are
  equal by construction; any other corner, supply or temperature than the
  three reduced-set points; mismatch spread (Monte Carlo); the tail currents
  (tool gap, 2AMLogic/klayout-tools#6997 — the block total current and the
  tail node voltages are recorded instead).
- Results are simulated, never measured.
