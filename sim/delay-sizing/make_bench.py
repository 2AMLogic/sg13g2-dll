#!/usr/bin/env python3
"""Build one delay-sizing bench deck + base request (issue #67). Pure text
generation; nothing simulates. Simulated, never measured.

usage: make_bench.py --variant {base,a,b} --freq {500MHz,1GHz} --vth V
                     [--b-scale S] --out DIR

  base  the drawn cell (two current-starved stages per tap) -- bench regression
        against sim/delay-sanity/results/20261105T080322Z/ (rising-edge d_k)
  a     candidate A: ONE inverting current-starved stage per tap (stage 1 of
        the drawn cell, unchanged devices); odd taps are inverted vs T0
  b     candidate B: the drawn two-stage cell with the starving devices
        (head PMOS MPH*, tail NMOS MNT*) widened by --b-scale; all else drawn

The decks are derived from the COMMITTED design/netlist/{delay_cell,
delay_line,tap_buffer}.spice by text transformation; design/ is not touched.
Writes DIR/decks/dl_<variant>_<freq>.spice and
DIR/base/<variant>_<freq>.base.request.json (@OSDI_DIR@ left for run.sh).
Measurements: dr<k> = T0 rise -> Tk first edge, df<k> = T0 fall -> Tk first
edge (edge direction at Tk follows the tap polarity), k=1..8, plus iavg (mean
supply current over 6..10 ns, an integer number of clock periods).
"""
import argparse, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
NETLIST = os.path.join(HERE, "..", "..", "design", "netlist")
FREQ = {"500MHz": ("2n", "1n"), "1GHz": ("1n", "0.5n")}
STARVE = ("XMPH1", "XMPH2", "XMNT1", "XMNT2")


def read(name):
    with open(os.path.join(NETLIST, name), encoding="utf-8") as fh:
        return fh.read()


def scale_w(line, s):
    return re.sub(r"\bw=([0-9.]+)u", lambda m: "w=%gu" % (float(m.group(1)) * s), line)


def cell_a(cell):
    """Stage 1 of the drawn cell as the whole cell (mid -> OUT)."""
    out = [".subckt delay_cell IN VBP VBN OUT VDD VSS"]
    for ln in cell.splitlines():
        if re.match(r"X(MPH1|MP1|MN1|MNT1)\b", ln):
            out.append(re.sub(r"\bmid\b", "OUT", ln))
    out.append(".ends")
    return "\n".join(out) + "\n"


def cell_b(cell, s):
    out = []
    for ln in cell.splitlines():
        if ln.split(" ")[0] in STARVE:
            ln = scale_w(ln, s)
        out.append(ln)
    return "\n".join(out) + "\n"


def strip_hdr(txt):
    return "\n".join(l for l in txt.splitlines() if not l.startswith("*")) + "\n"


def only_subckt(txt, name):
    """The committed delay_line export embeds copies of delay_cell/tap_buffer;
    keep just `.subckt <name> ... .ends` so a variant cell is defined once."""
    out, on = [], False
    for ln in txt.splitlines():
        t = ln.split()
        if t[:2] == [".subckt", name]:
            on = True
        if on:
            out.append(ln)
        if on and t[:1] == [".ends"]:
            break
    return "\n".join(out) + "\n"


def body(variant, period, half):
    loads = "\n".join("C%d t%d 0 20f" % (k, k) for k in range(9))
    return f"""* delay-sizing bench body (issue #67). Same stimulus/loads/bias as sim/delay-sanity.
* VC is the delay control: VBN = VC, VBP = Vdd - VC (ideal sources). Not a design.
Vdd vdd 0 1.2
VC vc 0 0.6
BVBP vbp 0 V=V(vdd)-V(vc)
Vck ck 0 PULSE(0 1 0.5n 30p 30p {half} {period})
Bin in 0 V=V(vdd)*V(ck)
XDL in vbp vc t0 t1 t2 t3 t4 t5 t6 t7 t8 vdd 0 delay_line
{loads}
"""


def requests(variant, vth):
    meas = []
    for k in range(1, 9):
        inv = variant == "a" and k % 2 == 1  # A: odd taps are inverted vs T0
        e_r, e_f = ("fall", "rise") if inv else ("rise", "fall")
        for nm, tedge, oedge in (("dr", "rise", e_r), ("df", "fall", e_f)):
            meas.append({"name": f"{nm}{k}", "unit": "s",
                         "spice": f".meas tran {nm}{k} trig v(t0) val={vth} {tedge}=1 targ v(t{k}) val={vth} {oedge}=1",
                         "limits": {"min": 0, "max": 6e-09}})
    meas.append({"name": "iavg", "unit": "A",
                 "spice": ".meas tran iavg avg i(Vdd) from=6n to=10n",
                 "limits": {"min": -1, "max": 1}})
    return meas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", required=True, choices=("base", "a", "b"))
    ap.add_argument("--freq", required=True, choices=sorted(FREQ))
    ap.add_argument("--vth", required=True)
    ap.add_argument("--b-scale", type=float, default=2.0)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    period, half = FREQ[a.freq]
    cell = strip_hdr(read("delay_cell.spice"))
    line = only_subckt(read("delay_line.spice"), "delay_line")
    tap = strip_hdr(read("tap_buffer.spice"))
    if a.variant == "a":
        cell = cell_a(cell)
    elif a.variant == "b":
        cell = cell_b(cell, a.b_scale)
    tag = f"{a.variant}_{a.freq}"
    os.makedirs(os.path.join(a.out, "decks"), exist_ok=True)
    os.makedirs(os.path.join(a.out, "base"), exist_ok=True)
    hdr = f"* delay-sizing deck: variant {a.variant}" + (f" scale {a.b_scale}" if a.variant == "b" else "") + \
          " -- derived from design/netlist/{delay_cell,delay_line,tap_buffer}.spice by sim/delay-sizing/make_bench.py\n"
    with open(os.path.join(a.out, "decks", f"dl_{tag}.spice"), "w") as fh:
        fh.write(hdr + cell + tap + line + body(a.variant, period, half))
    req = {
        "_comment": ["delay-sizing base request (issue #67). Limits are sanity gates, NOT spec numbers. Simulated, never measured.",
                     "@OSDI_DIR@ is substituted by run.sh."],
        "engine": "ngspice", "netlist": f"../decks/dl_{tag}.spice", "netlist_source": "schematic",
        "models": {"pdk": "ihp-sg13g2", "lib": "libs.tech/ngspice/models/cornerMOSlv.lib"},
        "analysis": {"kind": "tran", "args": "5p 10n"},
        "measurements": requests(a.variant, a.vth),
        "options": {"osdi_preload": [f"@OSDI_DIR@/{m}.osdi" for m in ("psp103", "psp103_nqs", "r3_cmc", "mosvar")],
                    "stage_model_inputs": True, "keep_artifacts": True},
    }
    with open(os.path.join(a.out, "base", f"{tag}.base.request.json"), "w") as fh:
        json.dump(req, fh, indent=2); fh.write("\n")


if __name__ == "__main__":
    sys.exit(main())
