# sim/cp-currents

Charge-pump / `cp_bias` bench (issue #30): UP and DN output current per corner, idle
leakage and supply current, both-on net current, and dump-buffer (`VDUMP`) tracking of
`VOUT`, on the three `reduced_set` corners of `sim/corners.json`. One `klt sim` request
(three units), so it rides the batch fleet; there is no local fallback.

```
design/netlist.sh && sim/cp-currents/run.sh
```

`decks/cp_body.spice` is the stimulus (ideal UP/DN, `VOUT` held by an ideal source);
`run.sh` prepends the committed `cp_bias.spice` and `cp.spice` exports. The request
carries no limits: `summarize.py` grades criteria K1-K6, fixed in its docstring before the
first result, and takes K_dl from the `1GHz_{ss,tt,ff}.envelope.json` files of one *pinned*
delay-sanity run — the pin is `DELAY_RUN` in `run.sh`, overridable with `CPI_DELAY_RUN`, and
each results directory names it in `record.md` and keeps a copy of those three envelopes
under `delay-sanity/`. The pin, rather than "the newest run", is what keeps a later
delay-sanity run from silently moving the K4 verdict of a cp-currents re-run. C_loop is the
nominal 1 pF of 0008, not extracted.

Results (append-only, simulated, never measured), exit 6 on a failed criterion:

- `20261105T125658Z` first run (killed client re-attached to its remote job; the 16 ns charge
  windows hit an unexplained current sample near the window end).
- `20261105T125926Z` adds min/max current measurements over the charge windows.
- `20261105T130112Z` the charge windows shortened to 5 ns. The charge
  columns are still not a usable result (see its note); K1-K5 are identical in all three runs.

- `20261106T182524Z` after the issue #62 redraw (`cp_bias` MR 2.2u/4u, unity-gain `cp_dumpbuf`) and a
  stimulus fix (`Bup`/`Bdn` `pwl()` lists now end with an explicit `400n,0` point: ngspice extrapolates
  the last slope, which drove UP/DN to about -175 V after the charge pulses); **the record to cite**.
  K1-K6 pass at all three corners.

Outcome of the first three runs: K1 and K5 failed; the cause and the redraw are in `spec/decisions/0012-cp-bias-currents-below-bounded-step-assumption.md`.
