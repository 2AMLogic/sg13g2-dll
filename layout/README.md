# layout — cp, cp_bias and loop_filter GDS with per-cell klt drc / klt lvs

Issue #190's deliverable: the repo's first physical layouts, one per cell
for the three cells whose schematics the pending delay-tap ruling (#58)
cannot change. Each cell directory holds a re-runnable generator and the
GDS it writes; every result below is machine-checked, not asserted.

```
layout/
  common.py                 shared flow: klt gen part runner, placement,
                            interconnect primitives, body ties, collision
                            self-check (layout/common.py's docstring states
                            the geometry conventions and their provenance)
  build.sh                  rebuild all three cells, verify each committed
                            stream reproduces byte-for-byte, refresh the
                            committed envelopes, append layout/runs/ record
  loop_filter/
    generate.py             one cap_array unit + the two pin labels
    loop_filter.gds         committed, deterministic stream
    drc_report.json         committed klt drc envelope (status: clean)
    lvs_request.json        committed klt lvs request
    lvs_report.json         committed klt lvs envelope (status: match)
  cp_bias/                  same shape, 6 devices in 3 matched blocks
  cp/                       same shape, 24 devices in 14 matched blocks
  runs/<timestamp>/record.md  append-only run records from build.sh
```

Not here: `dll_top`, `pfd`, `supervisor`, `lock_detector`, the delay line
and tap buffers — items 2/3/4 of the block manifest grade `dll_top`, which
stays with #25/#26/#27; a note listing these sub-cells is posted on #25.

## Flow

Two ingredients per cell, both committed and re-runnable:

1. **Device footprints: `klt gen`** (pinned `klt 0.8.0` via `scripts/klt.sh`,
   PDK `ihp-sg13g2` per `sim/pdk.json`). Every `sg13_lv_*` MOS is a
   `mos_array` block (matched units, dummy columns each end where the cell
   has an in-cell match, `gate_contact` so gates land on Metal1 pads); the
   loop filter's `cap_cmim` is one `cap_array` unit
   (`num=1, plate_w_um=26, plate_h_um=26`). Requests are in each
   `generate.py`; each run also drops the generator report under
   `parts/` (gitignored, regenerated).
2. **Interconnect, body ties, pin labels: `klayout.db`** (pinned
   `klayout==0.30.13`), drawn by `layout/common.py` under each
   `generate.py`'s net-by-net plan. Routing model: every horizontal run is
   a Metal2 track at a net-unique y; every vertical connection is a Metal1
   pad stub or channel run; the two layers cross freely and join only at
   drawn Via1s, so two routed nets can never short by construction, and a
   collision self-check plus `klt drc` verify it anyway. The self-check
   compares different nets in the `m1_v` ledger (vertical overlap > 0.30 µm)
   and the Metal2 track ledger; the directly drawn body-tie pads are outside
   the ledger, so DRC is their check.
   Body ties: one p+ substrate island ties every nfet body to VSS, and each
   pfet block's NWell gets an n+ island tied to VDD (the curated deck
   derives taps from the nSD/pSD implant markers), so LVS reports
   `body_verification: verified`, not just "unchecked", on all three cells.
   That `verified` rests on the **klt deck's** nSD/pSD convention, not the
   PDK's: in the pinned PDK `nSD.drawing` (7/0) is `valid=false` and IHP's
   own runset treats n+ as the default (`nactiv_con = activ - gatpoly -
   (psd | nsd_block)`), so IHP's reference cells draw no 7/0. The 7/0 on the
   n-well ties is drawn for the deck; under IHP's derivation those ties
   resolve as n+ only because pSD does not cover them.
3. **pSD enclosure for pfets and substrate ties.** The pinned
   `klt gen mos_array` omits the sg13g2 pfet implant. The PDK derives P+
   source/drain as `(activ - gatpoly) & psd`. In `common.py`, each pfet
   block occupies its own NWell. `_draw_psd` encloses all its Activ,
   including dummies, by 0.18 µm (`pSD.c`). It grows and shrinks the
   implant by 0.155 µm to fill gaps below the 0.31 µm spacing limit
   (`pSD.b`). This produces one continuous implant per well. The NWell
   extends at least 0.40 µm beyond the pfet Activ, and the p+ substrate
   tie has its own 0.03 µm implant enclosure (`pSD.c1`).

   `build.sh` runs `layout/check_psd.py` on each written GDS. It checks
   both enclosures and the pSD clearance to nfet Activ (0.18 µm) and n+
   well ties (0.03 µm). All four checks found zero area in violation in
   both MOS cells. The implant encloses 206.920 µm² of pfet Activ across
   seven wells in `cp` and 42.808 µm² across two wells in `cp_bias`.

Rebuild everything and append a run record:

```bash
layout/build.sh --record
```

A clean-clone rebuild reproduces each committed stream's sha256
byte-for-byte (GDS timestamps are disabled at write; the per-cell sha256
values are in `runs/<latest>/record.md` and in each run record). If a
rebuild ever disagrees with the committed stream, `build.sh` exits non-zero
rather than committing drift silently.

## Reuse check (issue #190 "Before drawing")

Per the workspace reuse rule, checked before drawing, outcome recorded
here (not in `reuse.lock.json`, whose entries track *topology* reuse from
`2AMLogic/sg13g2-pll` and are unchanged by this issue — no block changes
`adopting`/`kept` status here):

- `2AMLogic/sg13g2-pll` `layout/bin/` (flow, pinned at the `reuse.lock.json`
  commit `83e59fe`): **taken** — the device-footprint half of its flow
  (`klt gen mos_array`/`cap_array` per device group, exactly its
  `pll_layout.py` grouping) is what this repo runs. **Not taken**: its
  `klt gen-compose` composition is placement-only, and the router cannot
  bus multi-pin nets across same-row blocks — cross-confirmed with a
  minimal two-device sg13g2 repro on
  [klayout-tools#1962](https://github.com/2AMLogic/klayout-tools/issues/1962#issuecomment-7055580984)
  (the #199 same-facing-port limitation also applies). Interconnect is
  therefore hand-drawn, as below.
- `2AMLogic/sg13g2-bandgap` `layout/` (per-cell directory shape): **taken**
  — this directory mirrors its `layout/<cell>/{generate.py,<cell>.gds,
  drc_report.json,lvs_request.json,lvs_report.json}` convention, and its
  klayout.db construction pattern (hand-drawn interconnect + implant-marker
  body-tie islands over the curated sg13g2 deck) is the pattern
  `layout/common.py` implements. No code is copied: the bandgap draws its
  own device footprints (its issue pre-dates sg13g2 `klt gen` support);
  here the footprints come from `klt gen` and only interconnect is
  hand-drawn.

## Results (committed envelopes, re-runnable)

| cell | devices | klt drc (`--deck sg13g2`) | klt lvs vs `design/netlist/<cell>.spice` |
| --- | --- | --- | --- |
| `loop_filter` | 1 `cap_cmim` | **clean** (0 violations) | **match** — nets 2/2, devices 1/1, pins 2/2 |
| `cp_bias` | 6 (3 nfet, 3 pfet) | **clean** (0 violations) | **match** — nets 6/6, devices 6/6, pins 6/6 |
| `cp` | 24 (12 nfet, 12 pfet) | **clean** (0 violations) | **match** — nets 20/20, devices 24/24, pins 9/9 |

LVS references are the committed schematic netlists read directly
(`reference.form: "subckt-call"`, `reference.deck: "sg13g2"`, the PDK
device calls converted by klt; `cp.spice` is hierarchical, so its request
sets `options.flatten_reference: true`, disclosed by the report as
`topology.flattened`). Netlist commits the layouts were checked against:
`loop_filter.spice` at `fcb2d9b` (2026-10-27), `cp_bias.spice` and
`cp.spice` at `1c48a42` (2026-11-06). `cp` itself is still **`adopting`**
in `reuse.lock.json` (its remaining gate is charge-per-pulse grading, per `reuse.lock.json`):
if a later ruling changes a CP device size, re-run `layout/build.sh` — the
generators, not the streams, are the source of truth.

### Disclosures required by issue #190

Each cell's committed `drc_report.json` / `lvs_report.json` carry these
fields verbatim; quoted here as required. The deck is identical across all
runs: `sg13g2`, deck content hash
`sha256:1c95db40596afc5412e216009bcf0b775d1d74895b32738447eccbc76336dd15` (the
curated deck shipped in the pinned klt 0.8.0), run with the default
`curated` engine.

**DRC `coverage.layers_in_stream_without_rules`** — layers present in each
stream that no curated rule reads:

- `loop_filter`: `67/25` (Metal5 pin/label purpose), `126/25` (TopMetal1
  pin/label purpose), `129/0` (Vmim — the cap's plate via; the deck reads
  it for extraction/device recognition, and enforces its enclosure rules
  only in MIM contexts this stream's shapes satisfy)
- `cp_bias`, `cp`: `10/25` (Metal2 pin/label purpose — the pin labels),
  `99/50` (the deck's own extraction-only dummy-device marker that
  `mos_array` dummy columns carry; deliberately rule-free by design, see
  the deck's `dummy=(99,50)` comment)

**DRC `coverage.deck_scope`** (same for all three cells — section groups
the curated sg13g2 deck transcribes from IHP-Open-PDK v0.3.0):
`Act, Cnt, Gat, M1, M2, M3, M4, M5, MIM, NW, TM1, TM2, TV1, TV2, V1, V2,
V3, V4, pSD`.

**pSD rule coverage.** In klt 0.8.0, the `pSD` group checks
`psd.width.1`, `psd.space.1` and `psd.area.1`. The deck source lists
the omitted rules in two groups.

> `pSD.c`/`c1`/`d`/`d1` (enclosure/separation vs Activ/NWell/PWell) and
> `pSD.e`/`f`/`g`/`h` (abutted-tie rules).

These rules are absent from `coverage.rules_skipped` even when the stream
contains pSD. The enclosure and clearance measurements above come from the
stream check. The abutted-tie rules remain outside its scope. [Pinned deck source](https://github.com/2AMLogic/klayout-tools/blob/v0.8.0/src/klayout_tools/decks/sg13g2.py#L972-L983)

**DRC `coverage.rules_skipped`** — rules the deck did not evaluate because
their subject layers are absent from that stream:

- `cp_bias`, `cp` (identical lists; the streams draw no Metal3+ / MIM /
  TopMetal): `metal2.enclosing.via2.1`, `metal3.enclosing.via3.1`, `metal3.space.1`, `metal3.width.1`, `metal4.enclosing.via4.1`, `metal4.space.1`, `metal4.width.1`, `metal5.enclosing.mim.1`, `metal5.enclosing.topvia1.1`, `metal5.space.1`, `metal5.width.1`, `mim.enclosing.topvia1.1`, `topmetal1.enclosing.topvia1.1`, `topmetal1.enclosing.topvia2.1`, `topmetal1.space.1`, `topmetal1.width.1`, `topmetal2.enclosing.topvia2.1`, `topmetal2.space.1`, `topmetal2.width.1`, `topvia1.space.1`, `topvia1.width.1`, `topvia2.space.1`, `topvia2.width.1`, `via2.space.1`, `via2.width.1`, `via3.space.1`, `via3.width.1`, `via4.space.1`, `via4.width.1`
- `loop_filter` (a MIM-only stream: the cp list above — minus
  `metal5.enclosing.mim.1`, which its MIM stack *does* trigger — plus
  every FEOL/low-metal rule its stream lacks): additionally
  `activ.enclosing.cont.1`, `activ.space.1`, `activ.width.1`, `cont.space.1`, `cont.width.1`, `gatpoly.enclosing.cont.1`, `gatpoly.separation.activ.1`, `gatpoly.space.1`, `gatpoly.width.1`, `metal1.enclosing.via1.1`, `metal1.space.1`, `metal1.width.1`, `metal2.space.1`, `metal2.width.1`, `nwell.enclosing.nactiv.1`, `nwell.enclosing.nactiv.dig.1`, `nwell.enclosing.nactiv.hv.1`, `nwell.enclosing.pactiv.1`, `nwell.enclosing.pactiv.dig.1`, `nwell.enclosing.pactiv.hv.1`, `nwell.space.1`, `nwell.space.nactiv.1`, `nwell.space.nactiv.dig.1`, `nwell.space.nactiv.hv.1`, `nwell.space.pactiv.1`, `nwell.space.pactiv.dig.1`, `nwell.space.pactiv.hv.1`, `nwell.width.1`, `psd.area.1`, `psd.space.1`, `psd.width.1`, `via1.space.1`, `via1.width.1`

**Generator `drc_hints` (all 17 MOS part reports)**: `sd_implant_present:
false`, note "family 'sg13g2' declares no S/D implant role ('pplus') for
flavor 'pfet' -- no implant mask was drawn". The nfets are unaffected
(n+ is the default); the pfet pSD is drawn by `common.py` as described
above, not by the generator.

**LVS `power_connectivity.status`**: `unchecked` on all three cells — the
documented, expected value for a `subckt-call` reference, whose netlist
carries its own power/ground pins and nets that take part in the ordinary
compare ("this check exists to cover the signal-only `gate-level-verilog`
form"). No power connectivity is left unverified by this.

**LVS `body_verification.status`**: `verified` on all three cells — the
drawn p+/n+ body-tie islands resolve every MOS body to a named rail.

Further LVS disclosures the reports carry (all `severity: warning`, none
affect the verdict): `loop_filter` — `device.geometry_not_compared` (the
capacitor class's `A`/`P` are KLayout-secondary, so the match is topology
pairing; the drawn plate is 26×26 µm by construction) and
`device.placeholder_value` (the converted reference's `C` is the literal `0`
placeholder, excluded on both sides); `cp` — `topology.flattened`
(`flatten_reference`), plus the deck's routine "device class has no
counterpart and no devices" notes for classes the layout does not use.

### Matching structure and dead metal

`cp`'s UP/DN leg matching (the schematic-level rule issue #190 names): each
leg's mirror pair (`cp_leg_p` M1/M2, `cp_leg_n` M1/M2) is one matched
`mos_array` with a dummy column at each end, and the switch pairs
(`XXSWO`/`XXSWD`) likewise; the two legs are separate but identical blocks.
`cp_bias`'s mirror stack (MN0/MN3/MN4, MP0/MP3) is matched the same way;
`MR` (the Iref device) and the single-device buffer blocks (`MNT`, `MPT`,
`MCN`, `MCP`) have no in-cell match partner and draw no dummies. The
`mos_array` dummy columns are covered by the deck's `99/50` dummy marker,
so `klt extract` drops them as devices (`dummy_devices_dropped` in each
LVS report's underlying extraction); their unconnected S/D pads remain as
**dead metal**, which `klt extract` discloses in its `dead_metal[]` list —
known, deliberate, and invisible to both verdicts.

## Friction filed

One gap hit while standing this flow up, filed per the friction protocol
(generic tool description, cross-confirmed on the existing open tracker
issue rather than duplicating):
[klayout-tools#1962 (comment)](https://github.com/2AMLogic/klayout-tools/issues/1962#issuecomment-7055580984)
— `klt gen-compose` cannot bus multi-pin nets across same-row blocks even
with per-net routing planes and waypoints, which is why interconnect is
hand-drawn here rather than composed.

Second gap, found in review of the first version of this PR: the generator
draws no pfet S/D implant and the curated deck passes its implant-derived
rules vacuously when none is drawn, so a PMOS-less layout was DRC `clean`
and LVS `match` —
[klayout-tools#7531](https://github.com/2AMLogic/klayout-tools/issues/7531).
`layout/check_psd.py` is the interim derived-region check.

A separate deck gap allows coincident pSD and Activ edges inside NWell to
pass curated DRC with zero enclosure. A three-rectangle reproducer and an
enclosed control are documented upstream. [klayout-tools#7640](https://github.com/2AMLogic/klayout-tools/issues/7640)
