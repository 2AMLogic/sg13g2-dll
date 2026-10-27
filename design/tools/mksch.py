#!/usr/bin/env python3
"""Emit xschem .sch / .sym files for the cells in design/tools/cells.py.

The committed .sch/.sym files are the design sources; this module is the
drawing aid that produced them (xschem files are coordinate text and
label-driven connectivity is repetitive to type by hand). Connectivity is
label-driven: every device terminal carries a `lab_pin`, as in the sibling
`sg13g2-pll` schematics, so a net is its name and the exported netlist is
the thing to review.

    python3 -I design/tools/mksch.py            # (re)write design/*.sch, *.sym
    python3 -I design/tools/mksch.py --check    # fail if a committed file differs

Stdlib only. `--check` guards the *drawing* against the generator; the exported
netlists are guarded separately by design/netlist.sh --check.
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(HERE)

sys.path.insert(0, HERE)

XSCHEM_HEADER = "v {xschem version=3.4.8RC file_version=1.3"

# Terminal offsets (rot 0, flip 0) of the PDK / library symbols used.
NMOS = {"D": (20, -30), "G": (-20, 0), "S": (20, 30), "B": (20, 0)}
PMOS = {"D": (20, 30), "G": (-20, 0), "S": (20, -30), "B": (20, 0)}
CAP = {"c0": (0, -30), "c1": (0, 30)}

DEVICE_SYMS = {
    "nmos": ("sg13g2_pr/sg13_lv_nmos.sym", "sg13_lv_nmos", NMOS),
    "pmos": ("sg13g2_pr/sg13_lv_pmos.sym", "sg13_lv_pmos", PMOS),
}


class Port:
    def __init__(self, name, direction, side):
        self.name, self.direction, self.side = name, direction, side


def ports(spec):
    """'REF:i:l FB:i:l UP:o:r VDD:io:t VSS:io:b' -> [Port]."""
    out = []
    for tok in spec.split():
        name, direction, side = tok.split(":")
        out.append(Port(name, direction, side))
    return out


class Symbol:
    """Geometry of a generated subcircuit symbol (pin positions + file text)."""

    def __init__(self, name, port_list, note):
        self.name, self.ports, self.note = name, port_list, note
        left = [p for p in port_list if p.side == "l"]
        right = [p for p in port_list if p.side == "r"]
        top = [p for p in port_list if p.side == "t"]
        bot = [p for p in port_list if p.side == "b"]
        rows = max(len(left), len(right), 1)
        cols = max(len(top), len(bot), 1)
        self.hw = max(60, 20 * cols + 20)
        self.hh = max(40, 10 * rows + 20)
        self.pos = {}
        for side, plist in (("l", left), ("r", right)):
            for i, p in enumerate(plist):
                y = -10 * (len(plist) - 1) + 20 * i
                self.pos[p.name] = ((-self.hw if side == "l" else self.hw), y)
        for side, plist in (("t", top), ("b", bot)):
            for i, p in enumerate(plist):
                x = -10 * (len(plist) - 1) * 2 + 40 * i if len(plist) > 1 else 0
                # keep the first top/bottom pin left of centre like the sibling
                self.pos[p.name] = (x, (-self.hh if side == "t" else self.hh))
        # pin order in the file = netlist pin order; must equal the .sch port order
        self.order = port_list

    def text(self):
        hw, hh = self.hw, self.hh
        lines = [
            XSCHEM_HEADER,
            f"* {self.name} -- generated symbol, see design/tools/mksch.py",
            "}",
            "G {}",
            'K {type=subcircuit',
            'format="@name @pinlist @symname"',
            'template="name=x1"',
            "}",
            "V {}",
            "S {}",
            "E {}",
            f"L 4 {-hw} {-hh} {hw} {-hh} {{}}",
            f"L 4 {hw} {-hh} {hw} {hh} {{}}",
            f"L 4 {-hw} {hh} {hw} {hh} {{}}",
            f"L 4 {-hw} {-hh} {-hw} {hh} {{}}",
        ]
        for p in self.order:
            x, y = self.pos[p.name]
            d = {"i": "in", "o": "out", "io": "inout"}[p.direction]
            lines.append(f"B 5 {x - 2.5:g} {y - 2.5:g} {x + 2.5:g} {y + 2.5:g} {{name={p.name} dir={d}}}")
            if p.side == "l":
                lines.append(f"T {{{p.name}}} {x + 7:g} {y - 3:g} 0 0 0.15 0.15 {{layer=7}}")
            elif p.side == "r":
                lines.append(f"T {{{p.name}}} {x - 7 - 8 * len(p.name):g} {y - 3:g} 0 0 0.15 0.15 {{layer=7}}")
            elif p.side == "t":
                lines.append(f"T {{{p.name}}} {x - 4 * len(p.name):g} {y + 6:g} 0 0 0.15 0.15 {{layer=7}}")
            else:
                lines.append(f"T {{{p.name}}} {x - 4 * len(p.name):g} {y - 18:g} 0 0 0.15 0.15 {{layer=7}}")
        lines.append(f"T {{@symname}} {-hw + 5:g} {-hh - 30:g} 0 0 0.2 0.2 {{}}")
        lines.append(f"T {{@name}} {-hw + 5:g} {-hh - 50:g} 0 0 0.2 0.2 {{}}")
        return "\n".join(lines) + "\n"


class Cell:
    """A schematic: ports, device and sub-cell instances, a title note."""

    def __init__(self, name, port_spec, note):
        self.name = name
        self.ports = ports(port_spec)
        self.note = note
        self.items = []  # (kind, ...)
        self.sym = Symbol(name, self.ports, note)

    # -- devices ---------------------------------------------------------
    def mos(self, inst, kind, w, l, **conn):
        """kind 'n'|'p'; conn: D, G, S, B net names."""
        self.items.append(("mos", inst, kind, w, l, conn))

    def cap(self, inst, w, l, c0, c1, m=1):
        self.items.append(("cap", inst, w, l, c0, c1, m))

    def sub(self, inst, cell, **conn):
        self.items.append(("sub", inst, cell, conn))

    # -- emit ------------------------------------------------------------
    def schematic(self, lib):
        lines = [XSCHEM_HEADER, f"{self.name} -- {self.note}", "}", "G {}", "K {}", "V {}", "S {}", "E {}"]
        n = [0]

        def lab(x, y, net):
            n[0] += 1
            lines.append(f"C {{lab_pin.sym}} {x} {y} 0 0 {{name=l{n[0]} lab={net}}}")

        col, row = 0, 0
        for it in self.items:
            x, y = 300 * col, 220 * row
            col += 1
            if col == 5:
                col, row = 0, row + 1
            if it[0] == "mos":
                _, inst, kind, w, l, conn = it
                sympath, model, offs = DEVICE_SYMS["nmos" if kind == "n" else "pmos"]
                lines.append(
                    f"C {{{sympath}}} {x} {y} 0 0 {{name={inst} model={model} w={w} l={l} ng=1 m=1 spiceprefix=X}}"
                )
                for term in ("D", "G", "S", "B"):
                    dx, dy = offs[term]
                    lab(x + dx, y + dy, conn[term])
            elif it[0] == "cap":
                _, inst, w, l, c0, c1, m = it
                lines.append(
                    f"C {{sg13g2_pr/cap_cmim.sym}} {x} {y} 0 0 {{name={inst} model=cap_cmim w={w} l={l} m={m} spiceprefix=X}}"
                )
                lab(x, y - 30, c0)
                lab(x, y + 30, c1)
            else:
                _, inst, cell, conn = it
                sym = lib[cell].sym
                lines.append(f"C {{{cell}.sym}} {x} {y} 0 0 {{name={inst}}}")
                for p in sym.ports:
                    dx, dy = sym.pos[p.name]
                    lab(x + dx, y + dy, conn[p.name])
        # port pins down the left edge, in port order (= .subckt pin order)
        for i, p in enumerate(self.ports):
            sym = {"i": "ipin", "o": "opin", "io": "iopin"}[p.direction]
            lines.append(f"C {{{sym}.sym}} -400 {-300 + 40 * i} 0 0 {{name=p{i + 1} lab={p.name}}}")
        return "\n".join(lines) + "\n"


def write_all(cells, check=False):
    lib = {c.name: c for c in cells}
    bad = []
    for c in cells:
        for ext, text in (("sch", c.schematic(lib)), ("sym", c.sym.text())):
            path = os.path.join(DESIGN, f"{c.name}.{ext}")
            if check:
                cur = open(path, encoding="utf-8").read() if os.path.isfile(path) else None
                if cur != text:
                    bad.append(os.path.relpath(path, os.path.dirname(DESIGN)))
            else:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(text)
    return bad


def main(argv):
    from cells import CELLS  # noqa: E402  (sys.path set above)

    check = "--check" in argv
    bad = write_all(CELLS, check=check)
    if check:
        for b in bad:
            print(f"mksch: STALE {b} differs from design/tools/cells.py", file=sys.stderr)
        print("mksch: " + ("FAIL" if bad else "ok"), file=sys.stderr)
        return 1 if bad else 0
    print(f"mksch: wrote {len(CELLS)} cells to design/", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
