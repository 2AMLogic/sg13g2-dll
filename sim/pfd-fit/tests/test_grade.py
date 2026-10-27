"""grade.py reduction on a synthetic ideal PFD (no simulator)."""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import grade  # noqa: E402
import make_bench as mb  # noqa: E402

T = 1e-9


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


if __name__ == "__main__":
    unittest.main()
