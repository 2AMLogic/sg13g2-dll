# probe_ss — in-`pfd` reconciliation probe (issue #151)

Single-corner diagnostic, ss/1.080 V/125 °C, of the **committed**
`design/netlist/pfd.spice` `pfd` subckt after the `srlatch_buf` rewire of
spec/decisions/0015 — the probe-vs-gate caveat of issue #151: the retained
candidate probe `../20261116T012100Z/` ran the candidate **unwired**
(deck-inline `pfd_buf`); this run measures the same quantities on the wired-in
netlist. Deck stimulus byte-identical to `sim/pfd-fit/decks/pfd_1g.spice`
(same `Vrefn`/`Vfbn` PWL lines, same 4 fF `Cup`/`Cdn` bench loads); `decks/pfd.spice`
(sha256 `21842305…`) is identical to `design/netlist/pfd.spice` at this run's
commit and to the copy the gate run `../20261123T001411Z/` used.

Method: local single-unit `klt sim --backend local` (no job id — single unit),
ngspice 47, `tran 5p 25n`, crossings at VDD/2 on `ref`/`fb`/`up`/`dn` plus the
PFD-internal `set_up`/`set_dn`/`reset` and the latch-facing `up_qn`/`up_qb`/
`dn_qn`/`dn_qb`; reduction as in every record of this bench (`width = up_fall −
up_rise`, `path = reset_rise − up_rise`, `release = up_fall − reset_rise`) on
settled offset-0 cycles (warm-up cycle 0 excluded, as in 20261116T012100Z).
Simulated, never measured.

Result at ss/1.080 V/125 °C, offset 0, settled cycles (1, 2, 16, 17, 18 agree):

| quantity | unwired probe (20261116T012100Z) | this run (in-`pfd`) | delta |
|---|---|---|---|
| `path` | 30.8 ps | 30.8 ps | 0.0 ps |
| `release` | 174.4 ps | 174.4 ps | 0.0 ps |
| C2 `width` | 205.2..205.3 ps | 205.2..205.3 ps | ≤ 0.1 ps |
| `up_qn` rises (rel. ref edge) | +258.9 ps | +258.9 ps | 0.0 ps |
| flip inside set pulse | 29.8 ps | 29.8 ps | 0.0 ps |
| reset rise − set-pulse end | 127.5 ps | 127.4 ps | 0.1 ps |

**Delta zero**: wiring the cell into the exported hierarchy moves nothing — the
gate's ss offset-0 rows read the same widths. The full analysis, and this
probe's role in the gate record, are in `../20261123T001411Z/record.md`.
