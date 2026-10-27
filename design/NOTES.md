# Delay line: sizing note (issue #23)

Status: **provisional first-pass sizing, not simulated.** The sanity bench
(`sim/delay-sanity/`) is written but has not produced a result; see
"Evidence status". Nothing here is a measured or simulated number.

## Structure

| Cell | What | Devices (all `sg13_lv_*`, L = 0.13 µm) |
|---|---|---|
| `delay_cell` | two current-starved inverters in series, non-inverting; one cell = one tap step | per stage: head PMOS W 1.5 µm (gate VBP), inverter PMOS W 1 µm / NMOS W 0.5 µm, tail NMOS W 0.75 µm (gate VBN) |
| `tap_buffer` | two inverters, isolates the tap load from the line | stage 1: P 0.5 µm / N 0.25 µm; stage 2: P 3 µm / N 1.5 µm |
| `delay_line` | 8 `delay_cell` in series, 9 `tap_buffer` (T0 reference + T1..T8), one dummy `delay_cell` (`XDUM`) on the last tap | - |

Pins: `delay_line IN VBP VBN T0..T8 VDD VSS`. Control is two bias pins
(VBN = Vc, VBP = Vdd - Vc in the bench); bias generation belongs to the loop
issue (#24), not here.

## Choices and reasoning

- **Single-ended**, per decision 0004 (differential/CML and mux-selected lines
  are rejected there). Family: current-starved inverter, PMOS head / NMOS tail,
  as the sibling `vco_stage`; devices and lengths are re-sized for lv, not
  copied from the hv sibling.
- **Two stages per tap.** One inverting stage per tap would alternate tap
  polarity and make T8 an inverted copy of the input; two stages keep all taps
  the same polarity so tap k is the input delayed by k x T/8 and T8 is one full
  period. The cost is that each stage must be about half a tap: ~62 ps per
  stage at 1 GHz nominal and ~52 ps at ss / 1.08 V / 125 C (the 104 ps tap of
  decision 0004). The unstarved minimum lv inverter is 40/60 ps at ss into 5 fF
  (smoke record cited in 0004), so the starved stage has little headroom at the
  fast end. **This is the first thing the bench has to falsify**; if it fails,
  the fallback is one stage per tap with the polarity handled at the PFD
  (a new decision record, not a silent change).
- **L = 0.13 µm everywhere** (minimum, fastest). Longer starving devices would
  improve control linearity and are the first knob if the range is too wide.
  Head/tail are sized wider than the inverter devices so that at Vc near the
  fast end the starving devices stop limiting the stage.
- **Tap buffer** has a small first stage so each cell output sees one small
  gate (the next cell's input plus the buffer's) rather than the tap load.
  Every cell output sees exactly one delay_cell input + one tap_buffer input,
  including cell 8 (dummy cell `XDUM` + `XB8`) and the input (cell 1 + `XB0`).
- **Dummy load** is a full `delay_cell` rather than a lumped capacitor so the
  gate load matches by construction.
- **Hand-placed array.** Schematics are plain text under `design/`; the
  regular array (cell k at x = 500k, buffer k below it) was emitted once with a
  shell loop for the 27 repeated instance lines, then committed as ordinary
  source. There is no generator in the repo and `netlist.sh` does not run one.
  Revisit only if the array proves error-prone to edit by hand.

## Export

`design/netlist.sh` runs `klt netlist --block` for each top and writes
`design/netlist/*.spice`; `design/netlist.sh --check` writes nothing and exits 3
when any committed netlist differs from a fresh export. The script, not
`klt netlist --check`, does the comparison because the raw export embeds the
absolute checkout path in `** sch_path:` comments; the script rewrites that
prefix to `design/` first. (Generic tool gap, already tracked as 2AMLogic/klayout-tools#4091.)

## Evidence status

`sim/delay-sanity/run.sh` runs the T0-to-Tk delay vs control voltage at
500 MHz and 1 GHz over the reduced corner set (tt/1.2 V/27 C, ss/1.08 V/125 C,
ff/1.32 V/-40 C from `sim/corners.json`) as `klt sim` requests and writes
`results/<stamp>/record.md`. On the dispatch worker that built this change the
batch submit failed (`InvalidAccessKeyId` on the S3 input upload) and the local
ngspice 42 cannot load the OSDI v0.4 models, so **no result is committed**. A second attempt (2026-10-27, loom-worker-1) got
past submit but every batch job failed with `the fleet runner runs klt 0.7.0 but
the submitting client is 0.8.1.dev61`; a throwaway `klayout-tools==0.7.0` client
lacks the `--wait-for-capacity` and `--report-out` flags `run.sh` uses. The
fleet runner image needs a klt bump (worker/fleet spec), after which the bench
can run unchanged. **No result is committed.** The
T/8 coverage question, the 104 ps ss corner and the rail-margin requirement of
decision 0004 stay open until the bench is run where the fleet is reachable.
