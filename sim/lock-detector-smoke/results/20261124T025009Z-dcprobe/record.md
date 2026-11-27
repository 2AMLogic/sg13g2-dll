# lock-detector-smoke record (vmov_cmp quiet-input DC sweep, revised sensor, issue #196)

**PROBE, not a graded spec result** (`sim/corners.json`: the reduced set is never a recorded result).
Simulated, never measured.

## Question

The #189 sweep (`../20261121T004307Z-dcprobe/`) put the settled `STILL = 1` window of the old sensor at
[0, 0.4774) V at ss, [0, 0.6125) V at tt and [0, 0.8523) V at ff. Where is it for the replica-referenced
sensor of decision [0017](../../../../spec/decisions/0017-vmov-cmp-replica-threshold.md), and what margin does
it leave around the smoke band 0.585–0.615 V?

## Method

- Same bench as #189: `XDUT vctrl still vdd 0 vmov_cmp` alone, `.dc Vctrl 0 1.32 0.005` (265 points), in DC the low-pass
  cap is open so `vsb = vsb0 = vsa` and the sweep is the OTA pair's common-mode input. The three reduced-set
  corners (tt 1.2 V 27 °C, ss 1.08 V 125 °C, ff 1.32 V −40 °C) with `cornerRES res_typ` + `cornerCAP cap_typ`
  beside each MOS section, as in #189. Deck = the regenerated `design/netlist/lock_detector.spice` (commit
  `a1fe9a5`) + the #189 probe body; deck identity
  `sha256:345e1e45ed73bba9a175240713f21fe8c39e9009d19885bef51ff9deb27c2abb`.
- The old outputs `oab`/`obb` no longer exist; the request records the OTA outputs, the replica nodes and the new
  active-high flags `sa`/`sb`. i(vdd) (whole-block supply current) is recorded, not the tail currents
  (2AMLogic/klayout-tools#6997).
- Submitted `--backend batch --wait-for-capacity 600`; batch job `klt-sim-e0f3decc1a82`, ngspice 47, all three
  units `pass`.
- **An earlier submission of this request** (`../20261124T023824Z-dcprobe/`, job `klt-sim-cbe007fbe062`) is kept as
  evidence: its envelope status is `error` because its `.meas ... when v(still)=v(half)` transition cards report
  "out of interval", i.e. `STILL` never crosses 50 % of the rail anywhere in 0–1.32 V at any of the three corners.
  This request replaces those cards by explicit points and min/max over the whole sweep.

## Result

| quantity | tt | ss | ff |
|---|---|---|---|
| `STILL` at 0.585 / 0.600 / 0.615 V | rail (1.200 V) | rail (1.080 V) | rail (1.320 V) |
| `STILL` at 0.05 / 0.30 / 0.85 / 1.0 / 1.315 V | rail at all five | 1.0796 V at 0.05 V, rail at the others | rail at all five |
| min / max of `STILL` over 0–1.32 V | 1.200 / 1.200 V | 1.0796 / 1.080 V | 1.320 / 1.320 V |
| operating point at 0.600 V: `oa = ob` (= diode node `da`) | 0.5090 V | 0.4721 V | 0.5222 V |
| `sa` / `sb` (stillness flags) | 0.7465 / 0.7466 V | 0.6657 / 0.6658 V | 0.8245 / 0.8249 V |
| min of `sa` over [0, 0.85] V (≈ 59 % / 56 % / 60 % of the rail) | 0.706 V | 0.601 V | 0.793 V |
| replica node `ra = rb` | 0.255 V | 0.229 V | 0.298 V |
| block supply current at 0.600 V | 217.4 µA | 122.9 µA | 363.6 µA |

- **The settled `STILL` window encloses the whole smoke band at all three corners**, and in this sweep has no
  lower or upper edge anywhere in 0–1.32 V. The #189 edges (0.4774 / 0.6125 / 0.8523 V) are gone: there is no
  edge to measure a margin to, below the 0.85 V validity ceiling. Above about 0.85 V the PMOS input pairs are
  off and `STILL` staying high there says nothing about VCTRL movement (decision 0017, operating range).
- `sa` is not rail-to-rail at DC (0.60–0.79 V against rails of 1.08–1.32 V); it is buffered into `nand2_lv` +
  `inv_lv`, which restore `STILL` to the rail at all three corners (the `STILL` rows above). The ss minimum of `sa`,
  0.601 V (about 56 % of that rail), is the closest it comes to the following `nand2_lv` input trip; that trip was
  not measured here, so no margin number is claimed. This DC margin does not bound the dynamic threshold, which is in
  `../20261124T024845Z-stepprobe/`.
- Block supply current at VCTRL = 0.600 V is 1.7 / 1.9 / 1.9 times the #189 values (128 / 65 / 194 µA): the two always-on replica
  branches are the cost of the remedy. Not optimised.

## What this does not show

The motion threshold (in a settled DC sweep the two OTA inputs are equal by construction; see the step probe),
mismatch, other supply or temperature points, and any VCTRL above the validity ceiling where the pair is off.
