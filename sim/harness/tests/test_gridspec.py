"""Unit tests for sim/harness/gridspec.py and evidence.py (stdlib unittest).

    python3 -I -m unittest discover -s sim/harness/tests

Nothing here simulates; it checks request construction and envelope grading.
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
HARNESS = os.path.dirname(HERE)
sys.path.insert(0, HARNESS)

import evidence  # noqa: E402
import gridspec  # noqa: E402

BASE = {
    "engine": "ngspice",
    "netlist": "decks/x.spice",
    "models": {"pdk": "ihp-sg13g2", "lib": "libs.tech/ngspice/models/cornerMOSlv.lib"},
    "analysis": {"kind": "tran", "args": "5p 6n uic"},
    "measurements": [],
}
CORNERS = {"process": ["mos_tt", "mos_ss"], "temperature_c": [27, 85]}


class CornersFile(unittest.TestCase):
    def write(self, data):
        fd, path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        self.addCleanup(os.unlink, path)
        with open(path, "w") as fh:
            json.dump(data, fh)
        return path

    def test_committed_placeholder_is_refused(self):
        with self.assertRaises(gridspec.GridError) as cm:
            gridspec.load_corners(os.path.join(HARNESS, "..", "corners.json"))
        self.assertIn("empty", str(cm.exception))

    def test_committed_placeholder_loads_when_allowed(self):
        self.assertEqual(
            gridspec.load_corners(os.path.join(HARNESS, "..", "corners.json"), allow_empty=True), {}
        )

    def test_filled_set_passes_through(self):
        path = self.write({"schema": 1, **CORNERS, "supply_v": {"vdd": [1.08, 1.32]}})
        got = gridspec.load_corners(path)
        self.assertEqual(got["process"], ["mos_tt", "mos_ss"])
        self.assertEqual(got["supply_v"], {"vdd": [1.08, 1.32]})

    def test_bad_schema_and_ragged_supply(self):
        with self.assertRaises(gridspec.GridError):
            gridspec.load_corners(self.write({"schema": 2, **CORNERS}))
        with self.assertRaises(gridspec.GridError):
            gridspec.load_corners(
                self.write({"schema": 1, **CORNERS, "supply_v": {"a": [1], "b": [1, 2]}})
            )


class BuildRequest(unittest.TestCase):
    def test_corner_sweep_only(self):
        req = gridspec.build_request(BASE, CORNERS)
        self.assertEqual(req["corners"], CORNERS)
        self.assertNotIn("monte_carlo", req)
        self.assertNotIn("corners", BASE, "base must not be mutated")

    def test_ic_axis_rides_supply_v(self):
        req = gridspec.build_request(BASE, CORNERS, ic={"vic": [0.0, 0.6, 1.2]})
        self.assertEqual(req["corners"]["supply_v"], {"vic": [0.0, 0.6, 1.2]})
        self.assertNotIn("params", req["corners"])
        self.assertEqual(req["corners"]["process"], CORNERS["process"])

    def test_ic_crosses_corner_supply_rows(self):
        corners = {**CORNERS, "supply_v": {"vdd": [1.08, 1.32]}}
        req = gridspec.build_request(BASE, corners, ic={"vic": [0.0, 0.6, 1.2]})
        sv = req["corners"]["supply_v"]
        self.assertEqual(sv["vdd"], [1.08, 1.08, 1.08, 1.32, 1.32, 1.32])
        self.assertEqual(sv["vic"], [0.0, 0.6, 1.2, 0.0, 0.6, 1.2])
        self.assertEqual(corners["supply_v"], {"vdd": [1.08, 1.32]}, "input must not be mutated")

    def test_ic_source_clash_with_corner_supply(self):
        with self.assertRaises(gridspec.GridError):
            gridspec.build_request(BASE, {**CORNERS, "supply_v": {"vic": [1]}}, ic={"vic": [0, 1]})

    def test_ic_rows_must_be_equal_length_numbers(self):
        for bad in ({}, {"a": []}, {"a": [1], "b": [1, 2]}, {"a": ["x"]}, {"a": [True]}):
            with self.assertRaises(gridspec.GridError, msg=str(bad)):
                gridspec.ic_axis(bad)

    def test_monte_carlo_records_seed_n_vary(self):
        mc = dict(n=8, seed=20261018, vary="mismatch", seed_scope="point")
        req = gridspec.build_request(BASE, CORNERS, mc=mc)
        self.assertEqual(
            req["monte_carlo"], {"n": 8, "seed": 20261018, "vary": "mismatch", "seed_scope": "point"}
        )
        # MC is orthogonal to the corner matrix, not a replacement for it.
        self.assertEqual(req["corners"], CORNERS)

    def test_monte_carlo_validation(self):
        for kw in (
            dict(n=0, seed=1, vary="mismatch"),
            dict(n=True, seed=1, vary="mismatch"),
            dict(n=3, seed=None, vary="mismatch"),
            dict(n=3, seed=1.5, vary="mismatch"),
            dict(n=3, seed=1, vary="noise"),
            dict(n=3, seed=1, vary="both", seed_scope="nope"),
        ):
            with self.assertRaises(gridspec.GridError, msg=str(kw)):
                gridspec.monte_carlo_block(**kw)

    def test_base_may_not_own_a_grid_axis(self):
        for key in ("corners", "monte_carlo"):
            with self.assertRaises(gridspec.GridError):
                gridspec.build_request({**BASE, key: {}}, CORNERS)

    def test_build_is_deterministic(self):
        a = gridspec.build_request(BASE, CORNERS, ic={"v": [0, 1]}, mc=dict(n=2, seed=7, vary="both"))
        b = gridspec.build_request(BASE, CORNERS, ic={"v": [0, 1]}, mc=dict(n=2, seed=7, vary="both"))
        self.assertEqual(json.dumps(a), json.dumps(b))

    def test_negative_control_swaps_sections_and_keeps_seed(self):
        mc = gridspec.build_request(BASE, CORNERS, mc=dict(n=8, seed=5, vary="mismatch"))
        ctl = gridspec.negative_control(mc, ["mos_tt"])
        self.assertEqual(ctl["corners"]["process"], ["mos_tt"])
        self.assertEqual(ctl["monte_carlo"], mc["monte_carlo"])
        self.assertEqual(ctl["corners"]["temperature_c"], CORNERS["temperature_c"])
        self.assertEqual(mc["corners"]["process"], CORNERS["process"], "source request must not be mutated")
        with self.assertRaises(gridspec.GridError):
            gridspec.negative_control(mc, [])

    def test_negative_control_needs_mc(self):
        with self.assertRaises(gridspec.GridError):
            gridspec.negative_control(gridspec.build_request(BASE, CORNERS), ["mos_tt"])

    def test_rebase_netlist(self):
        req = gridspec.rebase_netlist(dict(BASE), "/a/base", "/a/out/req.json")
        self.assertEqual(req["netlist"], os.path.join("..", "base", "decks", "x.spice"))


class Cli(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, "-I", os.path.join(HARNESS, "gridspec.py"), *args],
            capture_output=True,
            text=True,
        )

    def test_unratified_corners_refused_with_exit_2(self):
        with tempfile.TemporaryDirectory() as d:
            base = os.path.join(d, "b.json")
            with open(base, "w") as fh:
                json.dump(BASE, fh)
            r = self.run_cli(base, "-o", os.path.join(d, "o.json"))
            self.assertEqual(r.returncode, 2)
            self.assertIn("empty", r.stderr)
            self.assertFalse(os.path.exists(os.path.join(d, "o.json")))

    def test_full_grid_and_control_files(self):
        with tempfile.TemporaryDirectory() as d:
            base = os.path.join(d, "b.json")
            with open(base, "w") as fh:
                json.dump(BASE, fh)
            corners = os.path.join(d, "c.json")
            with open(corners, "w") as fh:
                json.dump({"schema": 1, **CORNERS}, fh)
            out = os.path.join(d, "o.request.json")
            r = self.run_cli(
                base, "-o", out, "--corners", corners, "--mc-n", "4", "--mc-seed", "9",
                "--mc-vary", "mismatch", "--control-process", "mos_tt",
            )
            self.assertEqual(r.returncode, 0, r.stderr)
            with open(out) as fh:
                req = json.load(fh)
            with open(os.path.join(d, "o.request.control.json")) as fh:
                ctl = json.load(fh)
            self.assertEqual(req["monte_carlo"], {"n": 4, "seed": 9, "vary": "mismatch"})
            self.assertEqual(ctl["corners"]["process"], ["mos_tt"])

    def test_partial_mc_flags_are_an_error(self):
        with tempfile.TemporaryDirectory() as d:
            base = os.path.join(d, "b.json")
            with open(base, "w") as fh:
                json.dump(BASE, fh)
            r = self.run_cli(base, "-o", os.path.join(d, "o.json"), "--no-corners", "--mc-n", "4")
            self.assertEqual(r.returncode, 2)


def mc_env(sigmas, seed=7, n=4):
    return {
        "status": "pass",
        "corner_count": 4,
        "passed": 4,
        "environment": {"monte_carlo": {"seed": seed, "n": n, "vary": "mismatch"}},
        "measurements": [{"name": k, "monte_carlo": {"stddev": v}} for k, v in sigmas.items()],
        "corners": [],
    }


def corner(cid, supply, **vals):
    return {
        "corner_id": cid,
        "supply_v": supply,
        "measurements": [{"name": k, "value": v} for k, v in vals.items()],
    }


class Evidence(unittest.TestCase):
    def test_negative_control_requires_exact_zero(self):
        self.assertEqual(evidence.check_negative_control("c", mc_env({"a": 0.0, "b": 0})), [])
        bad = evidence.check_negative_control("c", mc_env({"a": 0.0, "b": 1e-15}))
        self.assertEqual(len(bad), 1)
        self.assertIn("expected exactly 0", bad[0])
        self.assertTrue(evidence.check_negative_control("c", mc_env({"a": None})))

    def test_mc_must_record_seed_and_n(self):
        env = mc_env({"a": 1.0})
        del env["environment"]["monte_carlo"]["seed"]
        self.assertTrue(any("seed" in p for p in evidence.check_mc_recorded("e", env)))

    def test_mismatch_on_run_must_show_spread(self):
        self.assertTrue(evidence.check_signal_present("e", mc_env({"a": 0.0})))
        self.assertEqual(evidence.check_signal_present("e", mc_env({"a": 0.0, "b": 2e-12})), [])

    def test_pooled_sigma_across_corners_is_not_mc_variation(self):
        env = mc_env({})
        env["measurements"] = [{"name": "m", "monte_carlo": {
            "stddev": 5e-9, "by_corner": [{"corner_id": "tt", "stddev": 0.0}, {"corner_id": "ss", "stddev": 0.0}]}}]
        self.assertEqual(evidence.check_negative_control("c", env), [])
        env["measurements"][0]["monte_carlo"]["by_corner"][1]["stddev"] = 1e-12
        self.assertEqual(len(evidence.check_negative_control("c", env)), 1)

    def test_reproducible(self):
        a = {"corners": [corner("x", None, m=1.0)]}
        self.assertEqual(evidence.check_reproducible("r", a, json.loads(json.dumps(a))), [])
        b = {"corners": [corner("x", None, m=1.0000001)]}
        self.assertTrue(evidence.check_reproducible("r", a, b))
        self.assertTrue(evidence.check_reproducible("r", a, {"corners": []}))

    def test_ic_applied(self):
        ok = {"corners": [corner("a", {"vic": 0.0}, v0=0.0), corner("b", {"vic": 1.2}, v0=1.2)]}
        self.assertEqual(evidence.check_ic_applied("i", ok, "vic", "v0"), [])
        stuck = {"corners": [corner("a", {"vic": 0.0}, v0=0.6), corner("b", {"vic": 1.2}, v0=0.6)]}
        self.assertEqual(len(evidence.check_ic_applied("i", stuck, "vic", "v0")), 2)
        one = {"corners": [corner("a", {"vic": 0.0}, v0=0.0)]}
        self.assertTrue(evidence.check_ic_applied("i", one, "vic", "v0"))

    def test_kind_and_basic_problems(self):
        self.assertEqual(evidence.kind(mc_env({"a": 1})), "mc")
        self.assertEqual(evidence.kind({"corners": [corner("a", {"vic": 1})]}, "vic"), "ic")
        self.assertEqual(evidence.kind({"corners": [corner("a", {"vic": 1})]}), "corners")
        self.assertEqual(evidence.kind({"corners": [corner("a", None)]}, "vic"), "corners")
        err = {"error": {"code": "batch_no_capacity", "message": "no capacity"}}
        self.assertIn("batch_no_capacity", evidence.basic_problems("e", err)[0])
        self.assertTrue(evidence.basic_problems("e", {"status": "fail", "corners": []}))


if __name__ == "__main__":
    unittest.main()
