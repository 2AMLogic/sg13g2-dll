# sim/jitter

Spec row 6 (added jitter, rms, simulated). **Not attestable yet.**

`spec/target-spec.md` fixes the method class (ngspice transient noise, >= 2000 locked cycles, >= 8 seeds, worst of taps 1..8 minus the input clock) but leaves the noise-source equivalents (which devices, what bandwidth, where they sit) to a decision record validated on a known case before the first result. `spec/decisions/` holds 0001-0007 and none covers it, so no jitter deck or request is written here: inventing a method is not allowed (CLAUDE.md, "Jitter needs its method").

What exists: this README, a `run.sh` that checks for the record and refuses to run without it, and the row in `sim/bench-rows.json` / `sim/inventory.json` marked `blocked`. The three corners (tt/1.20 V/27 C, ss/1.08 V/125 C, ff/1.32 V/-40 C) are three single-corner requests, not one grid, because `corners` is a cross product.

## Cold start

```
sim/jitter/run.sh
```

Exits 4 with the reason until a decision record whose title contains "noise method" exists under `spec/decisions/`. When it does, the deck, requests (seeds recorded) and estimator land with that record's PR; every figure then states its method next to the number.
