"""grade.py reduction on a synthetic ideal PFD (no simulator)."""
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import grade  # noqa: E402
import make_bench as mb  # noqa: E402

T = 1e-9
RETAINED = os.path.join(os.path.dirname(HERE), "results")
PORTS = ("t_ref", "t_fb", "t_up", "t_dn")


def synth(reset_ps=80.0, gain=1.0):
    offs = mb.offsets()
    tr = [mb.T0 + k * T for k in range(len(offs))]
    tf = [t + o * 1e-12 for t, o in zip(tr, offs)]
    up, ue, dn, de = [], [], [], []
    for r, f, o in zip(tr, tf, offs):
        first = min(r, f) + 40e-12
        wu = reset_ps + gain * max(o, 0)
        wd = reset_ps + gain * max(-o, 0)
        up += [first, first + wu * 1e-12]; ue += ["rise", "fall"]
        dn += [first, first + wd * 1e-12]; de += ["rise", "fall"]
    m = lambda n, t, e: {"name": n, "crossings": {"times": t, "edges": e}}
    return {"corner_id": "c", "measurements": [
        m("t_ref", tr, ["rise"] * len(tr)), m("t_fb", tf, ["rise"] * len(tf)),
        m("t_up", up, ue), m("t_dn", dn, de)]}


def synth_control(vdd=1.08, lanes="low", edgedets=True, storage=True, reset_rest=None,
                  dips=(-20, -10, -5, 0, 5, 10, 20)):
    """A ctl_1g corner the way klt reports one: dead or live lanes plus the DUT-internal probes.

    The default is the measured stuck-reset signature: a set pulse and a QN pulse
    on every input edge, reset asserted at rest and dipping only where the two QN
    pulses overlap, lanes that never leave low.
    """
    offs = mb.offsets()
    tr = [mb.T0 + k * T for k in range(len(offs))]
    tf = [t + o * 1e-12 for t, o in zip(tr, offs)]
    m = lambda n, t, e: {"name": n, "crossings": {"times": t, "edges": e}}
    ms = [m("t_ref", tr, ["rise"] * len(tr)), m("t_fb", tf, ["rise"] * len(tf))]
    if lanes == "pulsing":
        ms += [x for x in synth()["measurements"] if x["name"] in ("t_up", "t_dn")]
    else:
        ms += [m("t_up", [], []), m("t_dn", [], [])]

    def train(name, starts, edges):
        t, e = [], []
        for s in starts:
            t += [s + edges[0][1] * 1e-12, s + edges[1][1] * 1e-12]
            e += [edges[0][0], edges[1][0]]
        return m(name, t, e)

    set_pulse, qn_pulse = (("rise", 110), ("fall", 289)), (("rise", 259), ("fall", 407))
    ms += [train("t_set_up", tr if edgedets else [], set_pulse),
           train("t_set_dn", tf if edgedets else [], set_pulse),
           train("t_up_qn", tr if storage else [], qn_pulse),
           train("t_dn_qn", tf if storage else [], qn_pulse),
           train("t_reset", [t for t, o in zip(tr, offs) if o in dips], (("fall", 445), ("rise", 520)))]
    rest = vdd if reset_rest is None else reset_rest
    lv = lambda n, v: {"name": n, "value": v, "unit": "V", "status": "pass", "margin": None}
    lane_max = {"low": 0.002, "high": vdd, "pulsing": vdd}[lanes]
    ms += [lv("v_reset_rest", rest), lv("v_reset_min", 0.15 * vdd if dips else rest),
           lv("v_reset_max", vdd), lv("v_up_max", lane_max), lv("v_dn_max", lane_max)]
    return {"corner_id": "c", "supply_v": {"Vdd": vdd}, "measurements": ms}


def unprobed():
    """The control as every run before issue #201 measured it: ports only."""
    c = synth_control()
    c["measurements"] = [x for x in c["measurements"] if x["name"] in PORTS]
    return c


class Grade(unittest.TestCase):
    def test_ideal_passes(self):
        g = grade.grade_corner(synth(), T)
        self.assertEqual(g["fails"], [])

    def test_dead_zone_fails(self):
        g = grade.grade_corner(synth(gain=0.0), T)  # pulses ignore the offset
        self.assertTrue(any(f.startswith("C1") for f in g["fails"]))

    def test_reset_too_short_and_too_long(self):
        self.assertTrue(any(f.startswith("C2") for f in grade.grade_corner(synth(reset_ps=10), T)["fails"]))
        self.assertTrue(any(f.startswith("C2") for f in grade.grade_corner(synth(reset_ps=400), T)["fails"]))

    def test_missing_series(self):
        c = synth(); c["measurements"].pop()
        self.assertIn("error", grade.grade_corner(c, T))


class ControlReason(unittest.TestCase):
    """The control's failure must carry a stated, measured reason (issue #201)."""

    def reason(self, corner):
        return grade.control_defects(grade.grade_corner(corner, T), corner, T)

    def test_stuck_reset_is_the_stated_reason(self):
        defects, evidence = self.reason(synth_control())
        self.assertEqual(defects, [])
        self.assertEqual(evidence["counts"], {"t_ref": 19, "t_fb": 19, "t_up": 0, "t_dn": 0, "t_set_up": 38,
                                              "t_set_dn": 38, "t_up_qn": 38, "t_dn_qn": 38, "t_reset": 26})
        self.assertEqual(evidence["dip_offsets_ps"], [-20, -10, -5, 0, 5, 10, 20])

    def test_zero_lanes_without_internal_activity_is_a_broken_arm(self):
        defects, _ = self.reason(synth_control(edgedets=False, storage=False, dips=()))
        self.assertTrue(any("edge detectors did not fire" in d for d in defects))
        self.assertTrue(any("storage node" in d for d in defects))

    def test_passing_control_is_a_bench_defect(self):
        defects, _ = self.reason(synth_control(lanes="pulsing"))
        self.assertTrue(any("control passed" in d for d in defects))
        self.assertTrue(any("lane pulses" in d for d in defects))

    def test_lanes_stuck_high_are_not_held_in_reset(self):
        defects, _ = self.reason(synth_control(lanes="high"))
        self.assertEqual(defects, ["lanes are stuck high, not held low (UP max 1.080 V, DN max 1.080 V)"])

    def test_reset_deasserted_at_rest_is_not_the_polarity_failure(self):
        defects, _ = self.reason(synth_control(reset_rest=0.0))
        self.assertEqual(len(defects), 1)
        self.assertIn("reset not asserted at rest", defects[0])

    def test_envelope_without_probes_cannot_state_a_reason(self):
        defects, evidence = self.reason(unprobed())
        self.assertEqual(len(defects), 1)
        self.assertIn("no DUT-internal probes", defects[0])
        self.assertIn("t_set_up, t_set_dn, t_reset, t_up_qn, t_dn_qn, "
                      "v_reset_rest, v_reset_min, v_reset_max, v_up_max, v_dn_max", defects[0])
        self.assertIn(None, evidence["counts"].values())

    def test_ungradable_corner_is_a_defect(self):
        c = synth_control()
        c["measurements"] = [x for x in c["measurements"] if x["name"] != "t_fb"]
        defects, _ = self.reason(c)
        self.assertEqual(len(defects), 1)
        self.assertIn("not graded", defects[0])


class ControlGate(unittest.TestCase):
    """grade.main's exit status once the control carries a stated reason."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def write(self, name, corner):
        path = os.path.join(self.tmp.name, name + ".envelope.json")
        with open(path, "w") as fh:
            json.dump({"status": "pass", "environment": {}, "corners": [corner]}, fh)
        return path
    def run_main(self, paths):
        out = os.path.join(self.tmp.name, "fit-gate.md")
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = grade.main(paths + ["--out", out])
        with open(out) as fh:
            return rc, fh.read(), err.getvalue()

    def test_stated_reason_leaves_the_verdict_to_the_pfd_arms(self):
        rc, text, err = self.run_main([self.write("pfd_1g", synth()), self.write("ctl_1g", synth_control())])
        self.assertEqual((rc, err), (0, ""))
        self.assertIn("FAILS FOR THE STATED REASON", text)
        self.assertIn("set_up 38, set_dn 38", text)
        self.assertIn("deasserted on 13 cycles at offsets -20..+20 ps", text)
        ctl = text.split("## ctl_1g")[1]
        self.assertNotIn("BENCH DEFECT", text.split("## ctl_1g")[0])
        self.assertEqual(ctl.count("FAILS FOR THE STATED REASON"), 1)

    def test_a_reset_that_never_deasserts_is_the_stated_reason_too(self):
        rc, text, err = self.run_main([self.write("pfd_1g", synth()),
                                       self.write("ctl_1g", synth_control(dips=()))])
        self.assertEqual((rc, err), (0, ""))
        self.assertIn("with 0 crossings, never deasserted", text)
        self.assertIn("FAILS FOR THE STATED REASON", text)

    def test_passing_control_fails_the_gate(self):
        rc, text, err = self.run_main([self.write("pfd_1g", synth()),
                                       self.write("ctl_1g", synth_control(lanes="pulsing"))])
        self.assertEqual(rc, 1)
        self.assertIn("BENCH DEFECT -- control c: control passed", err)
        self.assertIn("BENCH DEFECT", text.split("## ctl_1g")[1])

    def test_broken_arm_fails_the_gate(self):
        rc, _, err = self.run_main([self.write("pfd_1g", synth()),
                                    self.write("ctl_1g", synth_control(edgedets=False, storage=False, dips=()))])
        self.assertEqual(rc, 1)
        self.assertIn("edge detectors did not fire", err)

    def test_unprobed_control_fails_the_gate(self):
        rc, _, err = self.run_main([self.write("pfd_1g", synth()), self.write("ctl_1g", unprobed())])
        self.assertEqual(rc, 1)
        self.assertIn("no DUT-internal probes", err)

    def test_gate_without_a_control_envelope_fails(self):
        rc, _, err = self.run_main([self.write("pfd_1g", synth())])
        self.assertEqual(rc, 1)
        self.assertIn("no control (ctl_*) envelope", err)

    def test_retained_unprobed_control_is_no_longer_evidence(self):
        ctl = os.path.join(RETAINED, "20261123T001411Z", "ctl_1g.envelope.json")
        rc, _, err = self.run_main([self.write("pfd_1g", synth()), ctl])
        self.assertEqual(rc, 1)
        self.assertEqual(err.count("BENCH DEFECT"), 3)
        self.assertIn("no DUT-internal probes", err)


if __name__ == "__main__":
    unittest.main()
