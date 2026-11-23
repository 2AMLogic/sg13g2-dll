#!/usr/bin/env python3
"""Derived-region check the curated klt deck cannot make (issue #190 review).

The deck skips Activ with neither implant drawn, so the nwell.*.pactiv.*
rules pass vacuously on a stream with no pSD. Assert instead that every
Activ inside an NWell is either covered by pSD (a pfet S/D) or is an n-well
tie island (covered by nSD): (Activ AND NWell) - pSD - nSD must be empty.
Prints the measured areas; exits non-zero on any uncovered pactiv.
"""
import sys

import klayout.db as kdb

ACTIV, NWELL, NSD, PSD = (1, 0), (31, 0), (7, 0), (14, 0)

rc = 0
for gds in sys.argv[1:]:
    ly = kdb.Layout()
    ly.read(gds)
    top = ly.top_cell()

    def reg(layer):
        return kdb.Region(top.begin_shapes_rec(ly.layer(*layer))).merged()

    pact = reg(ACTIV) & reg(NWELL)
    covered = pact & reg(PSD)
    tie = pact & reg(NSD)
    bad = pact - reg(PSD) - reg(NSD)
    a = lambda r: r.area() * ly.dbu ** 2
    print(f"  pactiv {a(pact):.3f} um2: pSD-covered {a(covered):.3f}, "
          f"nSD tie {a(tie):.3f}, uncovered {a(bad):.3f}")
    if not bad.is_empty():
        print(f"FAIL: {gds}: {bad.count()} pactiv shape(s) with no pSD "
              f"(pfet S/D would be n+ as drawn)", file=sys.stderr)
        rc = 1
sys.exit(rc)
