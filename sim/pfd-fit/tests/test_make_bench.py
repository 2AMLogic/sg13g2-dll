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


if __name__ == "__main__":
    unittest.main()
