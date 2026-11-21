#!/usr/bin/env python3
"""Shared helpers for the sg13g2-dll cell layouts (issue #190).

Each cell directory under layout/ holds a generate.py that builds its GDS
from two ingredients:

1. device footprints drawn by the pinned klt generators (`mos_array` for
   every sg13_lv_* MOS, `cap_array` for the loop filter's cap_cmim) --
   re-runnable requests with matched arrays and dummy units;
2. interconnect, body ties and pin labels drawn by this module through the
   `klayout.db` Python API (the construction pattern 2AMLogic/sg13g2-bandgap
   layout/ established; the `klt gen-compose` router cannot bus multi-pin
   nets across same-row blocks, so interconnect is drawn here instead).

Geometry conventions read from the klt 0.8.0 generator reports (verified
against every (w, l) this repo uses):

- unit activ spans local y [0, w] and x [0, 0.84 + l];
- S/D Metal1 pads are 0.42 wide: S at x [0, 0.42], D at x [0.42 + l,
  0.84 + l], each spanning the full activ height;
- the gate tab rises above activ; with gate_contact the gate Metal1 pad is
  0.42 wide centred on the activ centre, at local y [w + 0.50, w + 0.92].

Layer numbers are the curated sg13g2 deck table (src/klayout_tools/decks/
sg13g2.py at the pinned klt 0.8.0), not a private map.
"""

from __future__ import annotations

import json
import os
import subprocess

import klayout.db as kdb

DBU = 0.001  # um per dbu -- klt gen output and our writes use 1 nm

# --- curated sg13g2 deck layers --------------------------------------------
ACTIV = (1, 0)
GATPOLY = (5, 0)
NWELL = (31, 0)
CONT = (6, 0)
NSD = (7, 0)      # n+ implant: well tie inside NWell
PSD = (14, 0)     # p+ implant: substrate tie outside every NWell
M1 = (8, 0)
M1_TEXT = (8, 25)
VIA1 = (19, 0)
M2 = (10, 0)
M2_TEXT = (10, 25)
M5 = (67, 0)
M5_TEXT = (67, 25)
TM1 = (126, 0)
TM1_TEXT = (126, 25)

W1 = 0.30          # default Metal1 route width   (deck min 0.16)
W1_NARROW = 0.22   # squeezed stub where two stubs share one pad window
W2 = 0.40          # Metal2 route width           (deck min 0.20)
VIA = 0.19         # Via1 fixed size              (deck via1.width.1)
CLEAR_M1 = 0.20    # Metal1-Metal1 clearance kept (deck min 0.18)
CLEAR_M2 = 0.24    # Metal2-Metal2 clearance kept (deck min 0.21)
PAD_W = 0.42       # generator S/D and gate Metal1 pad width


def U(x):
    return int(round(x / DBU))


def klt_env():
    env = dict(os.environ)
    env.setdefault("PDK", "ihp-sg13g2")
    env.setdefault("PDK_ROOT", os.path.expanduser("~/share/pdk"))
    return env


def run_klt(args):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return subprocess.run(
        [os.path.join(root, "scripts", "klt.sh")] + args,
        capture_output=True, text=True, env=klt_env(), check=True).stdout


def _parse_json(stdout):
    return json.loads(stdout[stdout.index("{"):])  # skip uvx install notices


class Part:
    """One `klt gen` device block: its report plus derived pad geometry."""

    def __init__(self, name, generator, params, cell_dir):
        self.name = name
        parts = os.path.join(cell_dir, "parts")
        os.makedirs(parts, exist_ok=True)
        self.gds = os.path.join(parts, name + ".gds")
        self.report_path = os.path.join(parts, name + ".json")
        stdout = run_klt(["gen", generator,
                          "--params", json.dumps(params),
                          "--cell-name", name,
                          "-o", self.gds,
                          "--format", "json"])
        self.report = _parse_json(stdout)
        with open(self.report_path, "w") as fh:
            json.dump(self.report, fh, indent=1, sort_keys=True)
        self.w = params.get("w_um")
        self.l = params.get("l_um")
        self.bbox = self.report["bbox_um"]
        self._ports = {p["name"]: p for p in self.report["ports"]}

    # -- unit-local geometry (unit i = i-th real unit, dummies excluded) -----
    def unit_x(self, i):
        """x of unit i's activ LEFT edge, local frame."""
        return self._ports[f"U{i}_S"]["x_um"] - PAD_W / 2

    def pad_s(self, i):
        x = self.unit_x(i)
        return (x, x + PAD_W)

    def pad_d(self, i):
        x = self.unit_x(i) + 0.84 + self.l
        return (x - PAD_W, x)

    def pad_g(self, i):
        c = self._ports[f"U{i}_G"]["x_um"]
        return (c - PAD_W / 2, c + PAD_W / 2)


class _Placed:
    """A Part at a global origin; pads translated to the cell frame."""

    def __init__(self, part, x, y):
        self.part = part
        self.x = x
        self.y = y

    def pad(self, i, term):
        x0, x1 = getattr(self.part, "pad_" + term)(i)
        return (self.x + x0, self.x + x1)

    def activ_bottom(self):
        return self.y

    def activ_top(self):
        return self.y + self.part.w

    def gpad_top(self):
        return self.y + self.part.w + 0.92

    def bbox(self):
        b = self.part.bbox
        return (self.x + b["x0"], self.y + b["y0"],
                self.x + b["x1"], self.y + b["y1"])


def _side_window(pad, side, width):
    x0, x1 = pad
    if side == "left":
        return (x0 + 0.01, x0 + 0.01 + width)
    if side == "right":
        return (x1 - 0.01 - width, x1 - 0.01)
    c = (x0 + x1) / 2
    return (c - width / 2, c + width / 2)


class Cell:
    """One top cell: placed parts plus hand-drawn interconnect and labels."""

    def __init__(self, name):
        self.name = name
        self.ly = kdb.Layout()
        self.ly.dbu = DBU
        self.top = self.ly.create_cell(name)
        self.placed = {}
        self.m1_v = []   # (net, x0, x1, y0, y1) ledger for the self-check
        self.m2_h = []   # (net, y0, y1, x0, x1)
        self.vias = []
        self.labels = []

    # -- parts ---------------------------------------------------------------
    def place(self, part, ox, oy):
        src = kdb.Layout()
        src.read(part.gds)
        src.dbu = DBU
        stop = src.top_cell()
        stop.flatten(-1, True)
        cell = self.ly.create_cell(part.name)
        for li in src.layer_indexes():
            info = src.get_info(li)
            tli = self.ly.layer(info)
            for s in stop.shapes(li).each():
                cell.shapes(tli).insert(s)
        self.top.insert(kdb.CellInstArray(
            cell.cell_index(), kdb.Trans(kdb.Trans.R0, U(ox), U(oy))))
        p = _Placed(part, ox, oy)
        self.placed[part.name] = p
        return p

    # -- primitive drawing ----------------------------------------------------
    def rect(self, layer, x0, y0, x1, y1):
        self.top.shapes(self.ly.layer(*layer)).insert(
            kdb.Box(U(min(x0, x1)), U(min(y0, y1)), U(max(x0, x1)), U(max(y0, y1))))

    def text(self, layer, s, x, y):
        self.top.shapes(self.ly.layer(*layer)).insert(
            kdb.Text(s, kdb.Trans(kdb.Trans.R0, U(x), U(y))))

    def _m1(self, net, x0, y0, x1, y1):
        self.rect(M1, x0, y0, x1, y1)
        self.m1_v.append((net, min(x0, x1), max(x0, x1),
                          min(y0, y1), max(y0, y1)))

    def m2(self, net, y, x0, x1):
        # 0.3 extension past both declared ends: every endpoint via (vertical
        # channel or stub) must land fully inside the track, not on its edge.
        x0, x1 = min(x0, x1) - 0.3, max(x0, x1) + 0.3
        self.rect(M2, x0, y - W2 / 2, x1, y + W2 / 2)
        self.m2_h.append((net, y - W2 / 2, y + W2 / 2, x0, x1))

    def via(self, net, x, y):
        self.rect(VIA1, x - VIA / 2, y - VIA / 2, x + VIA / 2, y + VIA / 2)
        self.vias.append((net, x, y))

    def label(self, net, x, y):
        self.text(M2_TEXT, net, x, y)
        self.labels.append((net, x, y))

    # -- stubs: vertical Metal1 from a pad to a Metal2 track ------------------
    def stub_sd_dn(self, net, placed, i, term, y_track,
                   side="center", width=W1):
        """Extend an S/D pad DOWN from the activ bottom to y_track."""
        x0, x1 = _side_window(placed.pad(i, term), side, width)
        self._m1(net, x0, y_track - 0.15, x1, placed.activ_bottom() + 0.20)
        self.via(net, (x0 + x1) / 2, y_track)
        return (x0 + x1) / 2

    def stub_g_up(self, net, placed, i, y_track, side="center", width=W1):
        """Extend the gate pad UP from the gate-tab top to y_track."""
        x0, x1 = _side_window(placed.pad(i, "g"), side, width)
        self._m1(net, x0, placed.gpad_top(), x1, y_track + 0.15)
        self.via(net, (x0 + x1) / 2, y_track)
        return (x0 + x1) / 2

    def stub_d_up(self, net, placed, i, y_track):
        """D pad exits UP to the right of its own gate tab (diode ties)."""
        gx1 = placed.pad(i, "g")[1]
        dx0, dx1 = placed.pad(i, "d")
        x0 = max(gx1 + 0.22, dx0 + 0.01)
        x1 = x0 + W1_NARROW
        assert x1 <= dx1 + 1.0, (placed.part.name, i, x0, x1, dx1)
        self._m1(net, x0, placed.activ_top(), x1, y_track + 0.15)
        self.via(net, (x0 + x1) / 2, y_track)
        return (x0 + x1) / 2

    def stub_s_up(self, net, placed, i, y_track):
        """S pad exits UP to the left of its own gate tab."""
        sx0, _ = placed.pad(i, "s")
        gx0 = placed.pad(i, "g")[0]
        x0 = sx0 + 0.01
        x1 = min(x0 + W1_NARROW, gx0 - 0.20)
        self._m1(net, x0, placed.activ_top(), x1, y_track + 0.15)
        self.via(net, (x0 + x1) / 2, y_track)
        return (x0 + x1) / 2

    def vrun(self, net, x, y0, y1):
        """Free vertical Metal1 run (routing channels between blocks)."""
        self._m1(net, x - W1 / 2, y0 - 0.15, x + W1 / 2, y1 + 0.15)

    # -- body ties -------------------------------------------------------------
    def psub_tap(self, x, y_island_bottom, net, y_track):
        """p+ substrate-tie island (Activ+pSD+Cont+Metal1) dropped to a
        Metal2 track -- ties every nfet body to the named net."""
        self.rect(ACTIV, x, y_island_bottom, x + 0.6, y_island_bottom + 0.6)
        self.rect(PSD, x, y_island_bottom, x + 0.6, y_island_bottom + 0.6)
        c = 0.22
        self.rect(CONT, x + c, y_island_bottom + c,
                  x + 0.6 - c, y_island_bottom + 0.6 - c)
        self.rect(M1, x - 0.2, y_island_bottom + 0.1, x + 0.8,
                  y_island_bottom + 0.5)
        xc = x + 0.3
        self._m1(net, xc - W1 / 2, y_track - 0.15, xc + W1 / 2, y_island_bottom + 0.3)
        self.via(net, xc, y_track)
        return xc

    def well_tie(self, placed, net, y_track, side="right"):
        """n+ well tie for one placed pfet block: extend the block's NWell
        past its lower corner, put an nSD island inside the extension,
        drop to the Metal2 track. The extension overlaps the block's own
        well (one merged net), so the pfet bodies resolve to `net`."""
        bb = placed.bbox()
        ab = placed.activ_bottom()
        if side == "right":
            ext = (bb[2] - 0.25, bb[2] + 1.75)
            ix0, ix1 = bb[2] + 0.45, bb[2] + 1.05
        else:
            ext = (bb[0] - 1.75, bb[0] + 0.25)
            ix0, ix1 = bb[0] - 1.05, bb[0] - 0.45
        self.rect(NWELL, ext[0], ab - 1.15, ext[1], ab + 0.70)
        iy0, iy1 = ab - 0.90, ab - 0.30
        self.rect(ACTIV, ix0, iy0, ix1, iy1)
        self.rect(NSD, ix0, iy0, ix1, iy1)
        c = 0.22
        self.rect(CONT, ix0 + c, iy0 + c, ix1 - c, iy1 - c)
        self.rect(M1, ix0 - 0.2, iy0 + 0.1, ix1 + 0.2, iy1 - 0.1)
        xc = (ix0 + ix1) / 2
        self._m1(net, xc - W1 / 2, y_track - 0.15, xc + W1 / 2, iy0 + 0.2)
        self.via(net, xc, y_track)
        return xc

    # -- self-check + output ----------------------------------------------------
    def check(self):
        """Deterministic collision checks for the two routed layers."""
        problems = []
        for a in range(len(self.m1_v)):
            for b in range(a + 1, len(self.m1_v)):
                (na, ax0, ax1, ay0, ay1), (nb, bx0, bx1, by0, by1) = \
                    self.m1_v[a], self.m1_v[b]
                if na == nb:
                    continue
                gap_x = max(ax0, bx0) - min(ax1, bx1)
                if gap_x < CLEAR_M1 and min(ay1, by1) - max(ay0, by0) > 0.30:
                    problems.append(
                        f"M1 {na} x[{ax0:.2f},{ax1:.2f}] y[{ay0:.2f},{ay1:.2f}]"
                        f" vs {nb} x[{bx0:.2f},{bx1:.2f}] y[{by0:.2f},{by1:.2f}]"
                        f" gap {gap_x:.2f}")
        for a in range(len(self.m2_h)):
            for b in range(a + 1, len(self.m2_h)):
                (na, ay0, ay1, ax0, ax1), (nb, by0, by1, bx0, bx1) = \
                    self.m2_h[a], self.m2_h[b]
                if na == nb:
                    continue
                gap_y = max(ay0, by0) - min(ay1, by1)
                if gap_y < CLEAR_M2 and min(ax1, bx1) - max(ax0, bx0) > 0:
                    problems.append(
                        f"M2 {na} y[{ay0:.2f},{ay1:.2f}] x[{ax0:.2f},{ax1:.2f}]"
                        f" vs {nb} y[{by0:.2f},{by1:.2f}] x[{bx0:.2f},{bx1:.2f}]"
                        f" gap {gap_y:.2f}")
        if problems:
            raise AssertionError("routing collisions:\n  " + "\n  ".join(problems))

    def write(self, path):
        self.check()
        opts = kdb.SaveLayoutOptions()
        opts.gds2_write_timestamps = False  # byte-reproducible rebuilds
        self.ly.write(path, opts)
