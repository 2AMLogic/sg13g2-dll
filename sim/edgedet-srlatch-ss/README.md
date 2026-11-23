# sim/edgedet-srlatch-ss

Isolated `edgedet` + `srlatch` pair bench (issue #189): the measurement slice
of #148 that is valid under every #140 outcome. The issue #145 ss probes
measured that neither the supervisor nor the lock detector delivers an edge to
the shared three-stage one-shot at ss / 1.080 V / 125 C (the failure is
upstream: the `win_det` `b_up` sample mis-latches, `vmov_cmp` never asserts
`still`), so the one-shot/latch pair was **unexercised** at ss by that
stimulus. #148 acceptance criterion 3 asks the direct question: driven on its
input `to` by an external rising edge -- bypassing the stalled counter -- can
the three-stage one-shot still flip the plain `srlatch` at ss?

The bench uses the committed subcircuits from `design/netlist/lock_detector.spice`
verbatim (`XET to pt` / `XLAT pt bad lockq lockqb`, the lock detector's own
connection), resets the latch to a known Q = 0, releases reset, then applies
one ideal rising edge (30 ps slew) on `to`; `lockq` drives the lock detector's
own output-chain load (`inv_lv` + `inv2x_lv` + the row-12 20 fF on LOCK). One
`klt sim` request, two units: the reduced_set ss corner (the question) and tt
(the control, the #145 probe convention). Crossings are graded at 50 % of the
corner's own rail, so the same request grades both units.

```
design/netlist.sh && sim/edgedet-srlatch-ss/run.sh
```

Writes `results/<UTC stamp>/` (decks, request, envelope, `record.md`;
append-only). Exit 0 the record was written -- **the bench's verdict (latch
sets or not) is data, either way**; 3 missing prerequisite; 1 a harness fault
(missing envelope, an errored engine run, a diagnostic), named in `record.md`.

**DIAGNOSTIC bench, not a graded spec result** (`sim/corners.json`: the
reduced set is never a recorded result). Results are simulated, never
measured. The attribution this bench feeds (which documented weakness fired,
per block) is recorded on issue #148 and in `design/NOTES.md`.

The backend policy is the harness's: a multi-unit request goes to the batch
fleet (`--wait-for-capacity`), there is no local fallback, and nothing here
launches ngspice itself.
