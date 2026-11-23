"""make_bench.py reads the reduced-set corners through gridspec, not its own copy.

Issue #76 ratified one reader for the fast-iteration corner values; issue #109
moved the last bench that still parsed `sim/corners.json` itself onto
`gridspec.load_reduced_set`. These tests pin that: before the swap, a second
supply rail in `reduced_set.corners` was silently dropped from the request and
an emptied corner file produced a request with no corner units at all, while
`sim/pfd-fit/run.sh` still claimed the run covered "the reduced_set corners of
sim/corners.json". Nothing here simulates.
"""
import json
import os
import re
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
PFDFIT = os.path.dirname(HERE)
sys.path.insert(0, PFDFIT)
sys.path.insert(0, os.path.join(os.path.dirname(PFDFIT), "harness"))
import gridspec  # noqa: E402
import make_bench as mb  # noqa: E402

CORNERS = os.path.join(os.path.dirname(PFDFIT), "corners.json")


class CornerSource(unittest.TestCase):
    """The corner block of every generated request is gridspec's selection."""

    def test_every_request_carries_gridspecs_reduced_set(self):
        want = gridspec.load_reduced_set(CORNERS)
        requests = {rel: json.loads(text) for rel, text in mb.build().items()
                    if rel.startswith("requests/")}
        self.assertEqual(sorted(requests), [
            "requests/ctl_1g.request.json",
            "requests/pfd_1g.request.json",
            "requests/pfd_500m.request.json",
        ])
        for rel, req in requests.items():
            with self.subTest(request=rel):
                self.assertEqual(req["corners"], want)

    def test_committed_requests_match_gridspec(self):
        # The requests on disk are evidence of what ran; they must name the
        # same corners the one reader selects today.
        want = gridspec.load_reduced_set(CORNERS)
        names = sorted(os.listdir(os.path.join(PFDFIT, "requests")))
        self.assertTrue(names)
        for name in names:
            with self.subTest(request=name):
                with open(os.path.join(PFDFIT, "requests", name)) as fh:
                    self.assertEqual(json.load(fh)["corners"], want)


class CornerFileChanges(unittest.TestCase):
    """What a changed sim/corners.json does to the request.

    `mb.SIM` is the directory make_bench resolves `corners.json` against, so
    pointing it at a temporary tree exercises the real request builder against
    a corner file this repo does not commit.
    """

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        with open(CORNERS) as fh:
            self.data = json.load(fh)
        self._sim = mb.SIM
        mb.SIM = self.tmp.name

    def tearDown(self):
        mb.SIM = self._sim

    def write(self, data):
        with open(os.path.join(self.tmp.name, "corners.json"), "w") as fh:
            json.dump(data, fh)

    def test_second_supply_rail_reaches_the_request(self):
        # Pre-#109 the bench hardcoded Vdd, so an added rail was dropped and
        # the deck's own `Vdd vdd 0 1.2` stood in for it unannounced.
        self.data["reduced_set"]["corners"][0]["Vdd_io"] = 1.8
        self.write(self.data)
        units = mb.request("pfd_1g", 19, 1e-9)["corners"]["units"]
        self.assertEqual(units[0]["supply_v"], {"Vdd": 1.20, "Vdd_io": 1.8})

    def test_emptied_reduced_set_is_refused(self):
        # Pre-#109 this built {"units": []} without complaint.
        self.data["reduced_set"]["corners"] = []
        self.write(self.data)
        with self.assertRaises(gridspec.GridError):
            mb.request("pfd_1g", 19, 1e-9)

    def test_wrong_schema_is_refused(self):
        self.data["schema"] = 2
        self.write(self.data)
        with self.assertRaises(gridspec.GridError):
            mb.request("pfd_1g", 19, 1e-9)


class ControlArmGradesCommittedLatch(unittest.TestCase):
    """`pfd_sib` must track the latch the committed PFD instantiates.

    Issue #151: the SIBLING_POLARITY arm once hard-coded `srlatch_fast`'s name
    and six-pin order; when `pfd` moved to `srlatch_buf` (spec/decisions/0015)
    a stale arm would either fail `make_bench.py --check`-adjacent netlist
    loading or, worse, keep grading the retired latch. The control must grade
    the committed latch cell with the sibling's reset polarity - same cell,
    same NAND tap, one inverter more after the NAND.
    """

    def _subckt_cell(self, body, inst):
        line = next(l for l in body.splitlines() if l.startswith(inst))
        return line.split()[-1], line.split()[1:-1]

    def test_control_instantiates_the_pfd_latch_with_matching_pin_count(self):
        with open(os.path.join(PFDFIT, "..", "..", "design", "netlist",
                               "pfd.spice")) as fh:
            pfd_netlist = fh.read()
        # the committed pfd's latch cells and their pin count
        cell, nets = self._subckt_cell(pfd_netlist, "XLU")
        sub = next(l for l in pfd_netlist.splitlines()
                   if l.lower().startswith(".subckt " + cell + " "))
        self.assertEqual(cell, "srlatch_buf")  # 0015/issue #151 rewire
        n_pins = len(sub.split()) - 2
        # the control arm instantiates the same cell on the same pin count
        sib_cell, sib_nets = self._subckt_cell(mb.SIBLING_POLARITY, "XLU")
        self.assertEqual(sib_cell, cell)
        self.assertEqual(len(sib_nets), n_pins)
        # and differs from pfd only in the reset polarity: two inverters after
        # the NAND instead of one, same NAND tap
        self.assertIn("XNR up_qn dn_qn reset_raw VDD VSS", mb.SIBLING_POLARITY)
        self.assertEqual(len([l for l in mb.SIBLING_POLARITY.splitlines()
                               if l.startswith("XI")]), 2)
        self.assertIn("XNR up_qn dn_qn reset_n0 VDD VSS", pfd_netlist)
        self.assertNotIn("srlatch_fast", mb.SIBLING_POLARITY)


class ControlProbes(unittest.TestCase):
    """`ctl_1g` must show WHY its lanes are dead (issue #201).

    Before this the control measured only the four ports, so a deck that never
    elaborated, a stimulus that never reached the DUT and the documented
    stuck-reset all read `t_up = t_dn = 0`. The control request now carries the
    DUT-internal crossings the retained `pfd` probe deck already used plus the
    level probes grade.py needs to tell reset-asserted from reset-never-asserted;
    the `pfd_*` arms are unchanged.
    """

    PERIOD = 1e-9

    def measurements(self, tag="ctl_1g"):
        return {m["name"]: m for m in mb.request(tag, 19, self.PERIOD)["measurements"]}

    def test_control_request_probes_the_dut_internals(self):
        ms = self.measurements()
        half = {"frac_of": "Vdd", "fraction": 0.5}
        self.assertEqual([n for n, m in ms.items() if "crossings" in m][4:],
                         [f"t_{n}" for n in mb.CONTROL_NODES])
        self.assertEqual([n for n, m in ms.items() if "spice" in m], list(mb.CONTROL_LEVELS))
        for node in mb.CONTROL_NODES:
            with self.subTest(node=node):
                x = ms[f"t_{node}"]["crossings"]
                self.assertEqual((x["signal"], x["edge"], x["level"]), (f"v(xdut.{node})", "either", half))
        self.assertEqual(ms["v_reset_rest"]["spice"],
                         ".meas tran v_reset_rest min v(xdut.reset) from=4.000n to=4.900n")
        self.assertEqual(ms["v_reset_min"]["spice"],
                         ".meas tran v_reset_min min v(xdut.reset) from=4.000n to=24.000n")
        self.assertEqual(ms["v_reset_max"]["spice"],
                         ".meas tran v_reset_max max v(xdut.reset) from=4.000n to=24.000n")
        self.assertEqual(ms["v_up_max"]["spice"], ".meas tran v_up_max max v(up) from=4.000n to=24.000n")
        self.assertEqual(ms["v_dn_max"]["spice"], ".meas tran v_dn_max max v(dn) from=4.000n to=24.000n")
        self.assertEqual(ms["v_up_qn_min"]["spice"],
                         ".meas tran v_up_qn_min min v(xdut.up_qn) from=4.000n to=24.000n")
        self.assertEqual(ms["v_dn_qn_min"]["spice"],
                         ".meas tran v_dn_qn_min min v(xdut.dn_qn) from=4.000n to=24.000n")

    def test_every_probed_node_is_a_net_of_the_control_arm(self):
        nets = {tok for line in mb.SIBLING_POLARITY.splitlines() if line.startswith("X")
                for tok in line.split()[1:-1]}
        for node in mb.CONTROL_NODES:
            with self.subTest(node=node):
                self.assertIn(node, nets)

    def test_pfd_arms_measure_the_ports_only(self):
        for tag, period in (("pfd_1g", 1e-9), ("pfd_500m", 2e-9)):
            with self.subTest(tag=tag):
                ms = mb.request(tag, 19, period)["measurements"]
                self.assertEqual([m["name"] for m in ms], ["t_ref", "t_fb", "t_up", "t_dn"])
                self.assertTrue(all("crossings" in m for m in ms))

    def test_probe_windows_bracket_the_stimulus_inside_the_analysis(self):
        req = mb.request("ctl_1g", 19, self.PERIOD)
        tstop = float(req["analysis"]["args"].split()[1][:-1]) * 1e-9
        window = lambda name: [float(x) * 1e-9 for x in
                               re.findall(r"(?:from|to)=([\d.]+)n", self.measurements()[name]["spice"])]
        rest, sweep = window("v_reset_rest"), window("v_reset_min")
        offs = mb.offsets()
        first_edge = mb.T0 - mb.EDGE / 2
        last_edge = mb.T0 + (len(offs) - 1) * self.PERIOD + max(mb.OFFSETS_PS) * 1e-12 + self.PERIOD / 2 + mb.EDGE / 2
        self.assertLess(rest[0], rest[1])
        self.assertLess(rest[1], first_edge)
        self.assertLessEqual(sweep[0], first_edge)
        self.assertLess(last_edge, sweep[1])
        self.assertLessEqual(sweep[1], tstop)


if __name__ == "__main__":
    unittest.main()
