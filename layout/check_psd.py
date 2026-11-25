#!/usr/bin/env python3
"""Check the drawn pSD against the intended pfets and ties in these cells.

Identify active regions independently of pSD so an absent implant also fails.
Inside NWell, nSD marks the well ties. Outside NWell, gates cross the nfet
islands and the isolated ungated Activ is the substrate tie.
"""
import sys

import klayout.db as kdb

ACTIV, GATPOLY, NWELL, NSD, PSD = (1, 0), (5, 0), (31, 0), (7, 0), (14, 0)

rc = 0
for gds in sys.argv[1:]:
    ly = kdb.Layout()
    ly.read(gds)
    top = ly.top_cell()

    def reg(layer):
        return kdb.Region(top.begin_shapes_rec(ly.layer(*layer))).merged()

    active, well, psd = reg(ACTIV), reg(NWELL), reg(PSD)
    well_active = active & well
    well_ties = well_active & reg(NSD)
    pfets = well_active - well_ties
    outside = active - well
    nfets = outside.interacting(reg(GATPOLY))
    substrate_ties = outside - nfets

    # Independent PDK minima in um, converted using the stream's own dbu.
    enc = round(0.18 / ly.dbu)
    tie_enc = round(0.03 / ly.dbu)
    for rule, error in (
        ("pSD.c pfet enclosure", pfets.sized(enc) - psd),
        ("pSD.c1 substrate-tie enclosure", substrate_ties.sized(tie_enc) - psd),
        ("pSD.d nfet clearance", nfets.sized(enc) & psd),
        ("pSD.d1 well-tie clearance", well_ties.sized(tie_enc) & psd),
    ):
        area = error.area() * ly.dbu ** 2
        print(f"  {rule}: {area:.6f} um2 in violation")
        if not error.is_empty():
            print(f"FAIL: {gds}: {rule}", file=sys.stderr)
            rc = 1
sys.exit(rc)
