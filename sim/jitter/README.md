# sim/jitter

Spec row 6 (added jitter, rms, simulated). **Not attestable yet.**

The noise method row 6 deferred to a decision record is now fixed:
`spec/decisions/0014-row-6-noise-method.md` (status `proposed`) fixes the
equivalents (one white input-referred thermal `trnoise` per stage, derived
from `.noise` at the operating point, band 1 MHz–300 GHz, ENBW from a series
reference-resistor identity), the seed story (8 independent pid-seeded runs;
seed values not recordable on this toolchain, `2AMLogic/klayout-tools#5772`),
and the edge-drive limitation (`trnoise` + PULSE drive aborts ngspice, so a
DLL jitter deck cannot carry the equivalents and a PULSE clock at the same
time — `sigma_v` is measured at the locked operating point and `sigma_t =
sigma_v / SR` is derived). The validating bench is `sim/noise-method/`.

What still blocks row 6: **no DLL jitter deck or request exists here.** This
directory stays a placeholder until the deck implementing 0014 against
`dll_top` is written; the row stays `blocked` in `sim/bench-rows.json`. The
three corners (tt/1.20 V/27 C, ss/1.08 V/125 C, ff/1.32 V/-40 C) are three
single-corner requests, not one grid, because `corners` is a cross product.

## Cold start

```
sim/jitter/run.sh
```

Exits 4 with the reason: the record exists (0014, proposed), the deck does
not. When the deck lands, its own PR replaces this placeholder with the
requests and estimator; every figure then states its method next to the
number (0014; CLAUDE.md, "Jitter needs its method").
