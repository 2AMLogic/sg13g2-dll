#!/usr/bin/env python3
"""Generate the 0006 fit-gate decks and requests (decks/, requests/).

    python3 -I sim/pfd-fit/make_bench.py          # write
    python3 -I sim/pfd-fit/make_bench.py --check  # fail if the committed files differ

Bench: the PFD alone (design/netlist/pfd.spice), REF and FB driven by ideal
sources (100 ps edges, 50 % duty, amplitude = the corner's own Vdd), FB shifted
by a different offset on each cycle, UP and DN loaded by 4 fF each. Outputs are
read as threshold-crossing series (`crossings`, level VDD/2) and reduced by
grade.py. The control (`ctl_*`) also measures the DUT-internal nodes
(`control_probes`), so grade.py can state why its lanes are dead. Stdlib only.
Nothing here simulates.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(SIM, "harness"))

import gridspec  # noqa: E402

EDGE = 100e-12          # rise/fall time of REF and FB
T0 = 5e-9               # REF's first rising VDD/2 crossing
WARM, TAIL = 3, 3       # cycles at offset 0 before and after the sweep
# FB-minus-REF offsets, ps, ascending so successive cycles differ by <= 80 ps
OFFSETS_PS = [-160, -80, -40, -20, -10, -5, 0, 5, 10, 20, 40, 80, 160]
# On each of UP and DN. Derived, not estimated, since issue #151 (EE finding 1
# of PR #152): the CP input gates the node drives are design/netlist/cp.spice's
# XIUP/XIDN inv_lv input (P 1u + N 0.5u) plus the switch gate (XLEGP XXSWD
# P 3u on UP, XLEGN XXSWO N 1u on DN), all L = 0.13u. Quasi-static charge
# integration over a full 0->Vdd->0 swing of those gates (cp biased by
# cp_bias, per reduced_set corner; method and numbers retained in the issue
# #151 run records) gives C_eff = 4.37..4.97 fF across the three corners
# (UP 4.52/4.37/4.66, DN 4.71/4.45/4.97 fF at tt/ss/ff). The 4 fF model is
# kept deliberately: it is the byte-stable stimulus of the 0006 bench and of
# the retained 0015 probe (probe-vs-gate reconciliation compares identical
# decks), and the headroom analysis in the run record shows the miss enters
# the C2 width only through the driver's fall-minus-rise difference
# (~2 ps for the full +1 fF), inside the ss margin 0015 measured.
LOAD_F = 4e-15
FREQS = {"1g": 1e9, "500m": 500e6}

# The sibling's reset polarity (two inverters after the NAND, so the reset is
# the NAND output, not its complement), applied to the committed latch itself:
# since issue #151 the PFD instantiates srlatch_buf (7 pins: S R Q QB QN VDD
# VSS, spec/decisions/0015) and its reset NAND taps the QN storage nodes, so
# the control differs from the committed pfd ONLY in the reset polarity - the
# same latch, the same NAND (nand2x_lv) tap on the QN storage nodes, one
# inverter more after the NAND (XI1+XI2 instead of pfd's single XR1), on the
# cells pfd.spice defines (issue #113). This is the deliberate
# choice recorded in issue #151's run record: the control grades the new
# latch's lane-output arrangement with the opposite (sibling) reset polarity.
SIBLING_POLARITY = """\
.subckt pfd_sib REF FB UP DN VDD VSS
XED_UP REF set_up VDD VSS edgedet
XED_DN FB set_dn VDD VSS edgedet
XLU set_up reset UP up_qb up_qn VDD VSS srlatch_buf
XLD set_dn reset DN dn_qb dn_qn VDD VSS srlatch_buf
XNR up_qn dn_qn reset_raw VDD VSS nand2x_lv
XI1 reset_raw reset_d1 VDD VSS inv4x_lv
XI2 reset_d1 reset VDD VSS inv4x_lv
.ends
"""


def pwl(cross_times, period):
    """Normalised 0..1 PWL: rise centred on each crossing, 50 % duty."""
    pts = [(0.0, 0.0)]
    for tc in cross_times:
        pts += [(tc - EDGE / 2, 0.0), (tc + EDGE / 2, 1.0),
                (tc + period / 2 - EDGE / 2, 1.0), (tc + period / 2 + EDGE / 2, 0.0)]
    return "PWL(" + " ".join(f"{t * 1e9:.4f}n {v:g}" for t, v in pts) + ")"


def offsets():
    return [0] * WARM + OFFSETS_PS + [0] * TAIL


HALF_VDD = {"frac_of": "Vdd", "fraction": 0.5}
CONTROL_NODES = ("set_up", "set_dn", "reset", "up_qn", "dn_qn")
CONTROL_LEVELS = ("v_reset_rest", "v_reset_min", "v_reset_max", "v_up_max", "v_dn_max",
                  "v_up_qn_min", "v_dn_qn_min")


def xing(name, sig, edge):
    return {"name": name, "crossings": {"signal": sig, "level": HALF_VDD, "edge": edge, "max": 1000}}


def level(name, kind, sig, window):
    return {"name": name, "spice": f".meas tran {name} {kind} {sig} {window}", "unit": "V"}


def control_probes(ncyc, period):
    """DUT-internal measurements of the control arm (ctl_* requests only).

    `t_<node>` crossings of the CONTROL_NODES: the edge-detector outputs, the
    reset and the latch storage nodes the reset NAND taps, probed as the retained
    `pfd` probe decks already probed them. Plus node levels, which crossings
    cannot give (a stuck node has no crossing whether it is stuck high or low):
    `v_reset_rest` is the reset over the cycle before the first REF edge (after
    settling, before REF starts to rise); the `*_min`/`*_max` cards cover the
    whole stimulus, from one period before the first REF crossing to one period
    before the end of the analysis. grade.py reads them back by these names.
    """
    def t_ns(t):
        return f"{t * 1e9:.3f}n"
    rest = f"from={t_ns(T0 - period)} to={t_ns(T0 - EDGE)}"
    sweep = f"from={t_ns(T0 - period)} to={t_ns(T0 + ncyc * period)}"
    return [xing(f"t_{n}", f"v(xdut.{n})", "either") for n in CONTROL_NODES] + [
        level("v_reset_rest", "min", "v(xdut.reset)", rest),
        level("v_reset_min", "min", "v(xdut.reset)", sweep),
        level("v_reset_max", "max", "v(xdut.reset)", sweep),
        level("v_up_max", "max", "v(up)", sweep),
        level("v_dn_max", "max", "v(dn)", sweep),
        level("v_up_qn_min", "min", "v(xdut.up_qn)", sweep),
        level("v_dn_qn_min", "min", "v(xdut.dn_qn)", sweep)]


def deck(tag, freq, sibling=False):
    period = 1.0 / freq
    offs = offsets()
    ref = [T0 + k * period for k in range(len(offs))]
    fb = [t + o * 1e-12 for t, o in zip(ref, offs)]
    dut = "pfd_sib" if sibling else "pfd"
    lines = [
        f"* sg13g2-dll sim/pfd-fit: 0006 PFD fit gate, {freq / 1e6:g} MHz{' (CONTROL: sibling reset polarity)' if sibling else ''}.",
        "* Generated by sim/pfd-fit/make_bench.py. klt sim netlist body: no .lib/.temp/analysis/.end.",
        "* pfd.spice is design/netlist/pfd.spice, copied next to this deck by run.sh.",
        "* FB-minus-REF offset per cycle (ps), cycle 0 first: " + " ".join(str(o) for o in offs),
        "Vdd vdd 0 1.2",
        '.include "pfd.spice"',
    ]
    if sibling:
        lines.append(SIBLING_POLARITY.rstrip())
    lines += [
        f"Vrefn refn 0 {pwl(ref, period)}",
        f"Vfbn fbn 0 {pwl(fb, period)}",
        "Bref ref 0 V = v(vdd)*v(refn)",
        "Bfb fb 0 V = v(vdd)*v(fbn)",
        f"Xdut ref fb up dn vdd 0 {dut}",
        f"Cup up 0 {LOAD_F:g}",
        f"Cdn dn 0 {LOAD_F:g}",
    ]
    return "\n".join(lines) + "\n", len(offs), period


def request(tag, ncyc, period):
    tstop = T0 + (ncyc + 1) * period
    measurements = [
        xing("t_ref", "v(ref)", "rise"), xing("t_fb", "v(fb)", "rise"),
        xing("t_up", "v(up)", "either"), xing("t_dn", "v(dn)", "either"),
    ]
    if tag.startswith("ctl_"):
        measurements += control_probes(ncyc, period)
    return {
        "_comment": [
            f"sg13g2-dll 0006 PFD fit gate ({tag}). Generated by sim/pfd-fit/make_bench.py.",
            "Corners: the three-corner reduced_set of sim/corners.json (spec/decisions/0001: fast iteration only).",
            "Results are simulated, never measured. @OSDI_DIR@ is substituted by run.sh.",
        ],
        "engine": "ngspice",
        "netlist": f"../decks/{tag}.spice",
        "netlist_source": "schematic",
        "models": {"pdk": "ihp-sg13g2", "lib": "libs.tech/ngspice/models/cornerMOSlv.lib"},
        "corners": gridspec.load_reduced_set(os.path.join(SIM, "corners.json")),
        "analysis": {"kind": "tran", "args": f"5p {tstop * 1e9:.3f}n"},
        "measurements": measurements,
        "options": {
            "osdi_preload": ["@OSDI_DIR@/psp103.osdi", "@OSDI_DIR@/psp103_nqs.osdi",
                             "@OSDI_DIR@/r3_cmc.osdi", "@OSDI_DIR@/mosvar.osdi"],
            "stage_model_inputs": True,
            "keep_artifacts": True,
        },
    }


def build():
    out = {}
    for fname, freq in FREQS.items():
        for tag, sib in ((f"pfd_{fname}", False),) + (((f"ctl_{fname}", True),) if fname == "1g" else ()):
            text, n, period = deck(tag, freq, sib)
            out[f"decks/{tag}.spice"] = text
            out[f"requests/{tag}.request.json"] = json.dumps(request(tag, n, period), indent=2) + "\n"
    return out


def main(argv):
    files = build()
    bad = []
    for rel, text in files.items():
        path = os.path.join(HERE, rel)
        if "--check" in argv:
            if not os.path.isfile(path) or open(path).read() != text:
                bad.append(rel)
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, "w").write(text)
    if "--check" in argv:
        for b in bad:
            print(f"make_bench: STALE sim/pfd-fit/{b}", file=sys.stderr)
        return 1 if bad else 0
    print(f"make_bench: wrote {len(files)} files", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
