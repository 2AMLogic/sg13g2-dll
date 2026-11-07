#!/usr/bin/env python3
"""Device-area estimate (sum of W*L*ng*m over every X device) of the delay line
for each variant deck. A schematic-level estimate, NOT layout area (no
spacing, wells, routing or guard rings).  usage: area.py DECK [DECK...]"""
import re, sys

def parse(path):
    subs, cur = {}, None
    insts = {}
    for ln in open(path, encoding="utf-8"):
        t = ln.split()
        if not t or ln.startswith("*"): continue
        if t[0] == ".subckt": cur = t[1]; subs[cur] = 0.0; insts[cur] = []; continue
        if t[0] == ".ends": cur = None; continue
        if cur is None: continue
        if re.match(r"XM", t[0]):
            kv = dict(x.split("=") for x in t if "=" in x)
            w = float(kv["w"].rstrip("u")); l = float(kv["l"].rstrip("u"))
            subs[cur] += w * l * float(kv.get("ng", 1)) * float(kv.get("m", 1))
        elif t[0].startswith("X"):
            insts[cur].append(t[-1])
    def tot(n):
        return subs[n] + sum(tot(c) for c in insts[n] if c in subs)
    return tot("delay_line"), tot("delay_cell"), tot("tap_buffer")

for p in sys.argv[1:]:
    line, cell, tap = parse(p)
    print(f"{p}: delay_line {line:.2f} um^2 (cell {cell:.3f} x9 incl. dummy + tap_buffer {tap:.3f} x9)")
