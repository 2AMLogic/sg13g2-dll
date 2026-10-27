# design

xschem sources and the derived SPICE for the DLL's delay line (issue #23).
Sizing rationale and evidence status: [`NOTES.md`](NOTES.md).

```
design/
  xschemrc              project-local xschem config (PDK + this directory)
  export.sh             klt netlist driver: regenerate, or --check for staleness
  netlist/*.spice       committed exports (derived; do not edit by hand)
  delay_cell.sch/.sym   two current-starved inverters, non-inverting
  tap_buffer.sch/.sym   two-inverter tap buffer
  delay_line.sch/.sym   8 delay cells, T0..T8 tap buffers, dummy last-tap load
```

```
design/export.sh          # rewrite design/netlist/*.spice
design/export.sh --check  # exit 3 if a netlist is stale
```

The PFD, charge pump, loop filter, lock detector and `dll_top` are issue #24.
