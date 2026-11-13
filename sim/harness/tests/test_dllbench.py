"""Unit tests for sim/harness/dllbench.py and the bench inventory (no simulator).

    python3 -I -m unittest discover -s sim/harness/tests
"""

import json
import os
import re
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
HARNESS = os.path.dirname(HERE)
SIM = os.path.dirname(HARNESS)
ROOT = os.path.dirname(SIM)
sys.path.insert(0, HARNESS)

import dllbench  # noqa: E402

BENCHES = ("phase", "lock-time", "false-lock", "power")
DUT = os.path.join(SIM, "standin", "dut.json")


def jload(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def probe_of(axis):
    """The read-back measurement name axis_problems() expects for an axis."""
    return "ic_seen" if axis == "vic" else f"{axis}_seen"


def ic_corner(corner_id, st, **over):
    """One passing corner of a start-state sweep: every swept source reads back
    its own value, the first input edge sits at the state's vtclk, and the
    row-8 predicate passes. `over` overrides measurement values."""
    ic = st["ic"]
    vals = {probe_of(a): ic[a] for a in dllbench.AXES}
    vals["tclk_edge"] = max(ic["vtclk"], 0.0) * 1e-9
    vals.update({"perr": 0.005, "vcpp": 1e-6, "d8_64": 1.005e-9,
                 "rail_hi": 0.3, "rail_lo": 0.4, "lock_end": 1.0})
    vals.update(over)
    return {"corner_id": corner_id,
            "supply_v": dict(ic, Vdd=1.2),
            "measurements": [{"name": k, "value": v} for k, v in vals.items()]}


def ic_envelope(corners):
    """A synthetic all-pass envelope around `corners` (no simulator)."""
    return {"status": "pass", "corner_count": len(corners), "passed": len(corners),
            "failed": 0, "errored": 0,
            "environment": {"engine": "ngspice", "engine_version": "44", "backend": "local"},
            "corners": corners}


class Inventory(unittest.TestCase):
    def test_every_spec_row_is_mapped(self):
        rows = jload(os.path.join(SIM, "bench-rows.json"))["rows"]
        self.assertEqual(sorted(int(k) for k in rows), dllbench.spec_rows())
        self.assertEqual(len(dllbench.spec_rows()), 12)

    def test_mapped_benches_exist_and_are_listed(self):
        inv = jload(os.path.join(SIM, "inventory.json"))
        listed = set(inv["testbenches"])
        for row, ent in jload(os.path.join(SIM, "bench-rows.json"))["rows"].items():
            if ent["status"] == "not-a-bench":
                continue
            self.assertTrue(os.path.isdir(os.path.join(ROOT, ent["bench"])), row)
            self.assertIn(f"{ent['bench']}/README.md", listed, row)
            self.assertIn(f"{ent['bench']}/run.sh", listed, row)

    def test_inventory_schema_and_files(self):
        inv = jload(os.path.join(SIM, "inventory.json"))
        self.assertEqual(set(inv), {"schema_version", "kind", "t1_item", "description", "testbenches", "cold_start", "pins"})
        self.assertEqual((inv["schema_version"], inv["kind"], inv["t1_item"]), (1, "t1-attestation-inventory", 9))
        self.assertEqual(len(inv["testbenches"]), len(set(inv["testbenches"])))
        for f in inv["testbenches"]:
            self.assertFalse(".." in f.split("/"))
            self.assertTrue(os.path.isfile(os.path.join(ROOT, f)), f)
            self.assertFalse(os.path.islink(os.path.join(ROOT, f)), f)
        self.assertTrue(os.path.isfile(os.path.join(ROOT, *inv["cold_start"]["argv"][0].split("/"))))
        self.assertIn("revision", inv["pins"]["pdk"])

    def test_blocked_row_is_marked_not_attestable(self):
        row6 = jload(os.path.join(SIM, "bench-rows.json"))["rows"]["6"]
        self.assertEqual(row6["status"], "blocked")

    def test_standin_is_flagged(self):
        dut = jload(DUT)
        self.assertTrue(dut["stand_in"])
        self.assertFalse(dut["attestable"])
        with open(os.path.join(SIM, "standin", dut["netlist"]), encoding="utf-8") as fh:
            self.assertIn("STAND-IN, not the item-1 netlist", fh.read())


class Structure(unittest.TestCase):
    def test_eight_output_taps_and_a_reference(self):
        ports = jload(DUT)["ports"]
        taps = [p for p in ports if re.fullmatch(r"tap\d", p)]
        self.assertEqual(taps, [f"tap{k}" for k in range(9)])  # 8 outputs + reference tap8
        with open(os.path.join(SIM, "standin", "dll_standin.spice"), encoding="utf-8") as fh:
            subckt = next(l for l in fh if l.startswith(".subckt dll_standin"))
        self.assertEqual(subckt.split()[2:], ports)


class Build(unittest.TestCase):
    def build(self, bench, **kw):
        d = tempfile.mkdtemp()
        out = os.path.join(d, "o")
        dllbench.build(os.path.join(SIM, bench), out, DUT, kw.get("f0", 1e9), kw.get("tol", 0.02), 5.0, "/osdi")
        return out

    def test_every_bench_builds_and_checks(self):
        for b in BENCHES:
            out = self.build(b)
            self.assertEqual(dllbench.check(out), 0, b)

    def test_false_lock_grid_is_five_frequencies_nine_states_45_corners(self):
        out = self.build("false-lock")
        man = jload(os.path.join(out, "manifest.json"))
        self.assertEqual([r["tag"] for r in man["requests"]], ["f080", "f090", "f100", "f110", "f120"])
        req = jload(os.path.join(out, "requests", "f100.request.json"))
        self.assertEqual(len(req["corners"]["supply_v"]["vic"]), 3 * 9)
        self.assertEqual(len(req["corners"]["process"]) * len(req["corners"]["temperature_c"]) * 27, 405)

    def test_start_state_4_tracks_frequency(self):
        dut = jload(DUT)
        a = dllbench.state_axes("s4b_one_and_half_T", 1e-9, dut)["vic"]
        b = dllbench.state_axes("s4b_one_and_half_T", 1 / 0.8e9, dut)["vic"]
        self.assertLess(a, b)
        self.assertAlmostEqual(a, (1.5e-9 - 4.96e-10) / 1.704e-9)

    def test_tolerance_and_period_reach_the_limits(self):
        out = self.build("phase", f0=5e8, tol=0.05)
        req = jload(os.path.join(out, "requests", "f100.request.json"))
        lim = {m["name"]: m.get("limits") for m in req["measurements"]}
        self.assertEqual(lim["perr"], {"max": 0.05})
        self.assertEqual(lim["vcpp"], {"max": 5e-3})
        with open(os.path.join(out, "decks", "tb_f100.spice"), encoding="utf-8") as fh:
            self.assertIn("2 ", fh.read())  # period 2 ns

    def test_run_length_is_per_column(self):
        self.assertAlmostEqual(dllbench.run_length(1e9), 2e-6)
        self.assertAlmostEqual(dllbench.run_length(2e9), 2e-6)
        self.assertAlmostEqual(dllbench.run_length(5e8), 10e-6)
        with self.assertRaises(dllbench.BenchError):
            dllbench.run_length(7e8)

    def test_manifest_and_request_carry_the_column_run(self):
        for f0, run in ((5e8, 10e-6), (1e9, 2e-6)):
            out = self.build("lock-time", f0=f0)
            man = jload(os.path.join(out, "manifest.json"))
            self.assertAlmostEqual(man["run_s"], run)
            for r in man["requests"]:  # every frequency of the sweep uses the column's run
                req = jload(os.path.join(out, "requests", r["tag"] + ".request.json"))
                self.assertAlmostEqual(float(req["analysis"]["args"].split()[1]), run)
                self.assertEqual(r["window"]["j_end"], dllbench.window_end(r["period_s"], run))
                self.assertLessEqual((r["window"]["j_end"] + 1) * r["period_s"], run)

    def test_unknown_column_is_refused_at_build(self):
        with self.assertRaises(dllbench.BenchError):
            self.build("power", f0=7e8)

    def test_existing_output_is_refused(self):
        out = self.build("power")
        with self.assertRaises(dllbench.BenchError):
            dllbench.build(os.path.join(SIM, "power"), out, DUT, 1e9, 0.02, 5.0, "/osdi")


class Grading(unittest.TestCase):
    T = 1e-9

    def vals(self, **kw):
        v = {"perr": 0.005, "vcpp": 1e-6, "d8_64": 1.005e-9, "rail_hi": 0.3, "rail_lo": 0.4, "lock_end": 1.0}
        v.update(kw)
        return v

    def st(self):
        return {"name": "s1_min_rail", "ic": {}, "ref_ns": 0.0}

    def test_one_period_lock_passes(self):
        f = dllbench.grade_corner("predicate", self.T, self.st(), self.vals(), 0.02)
        self.assertTrue(f["row8_pass"])
        self.assertTrue(f["lock_ok"])

    def test_two_period_lock_is_a_false_lock(self):
        f = dllbench.grade_corner("predicate", self.T, self.st(), self.vals(perr=0.0, d8_64=2.0e-9), 0.02)
        # the stand-in-style 2T lock: |d - T| is large, so the predicate itself fails
        self.assertFalse(f["row8_pass"])
        self.assertEqual(f["delay_periods"], 2)

    def test_lock_asserted_while_not_locked_is_inconsistent(self):
        f = dllbench.grade_corner("predicate", self.T, self.st(), self.vals(perr=0.5, lock_end=1.0), 0.02)
        self.assertFalse(f["lock_ok"])

    def test_rail_park_fails(self):
        f = dllbench.grade_corner("predicate", self.T, self.st(), self.vals(rail_hi=0.01), 0.02)
        self.assertTrue(f["on_rail"])
        self.assertFalse(f["row8_pass"])

    def test_lock_time_needs_settled_tail(self):
        j_end = dllbench.window_end(self.T, dllbench.run_length(1e9))
        vals = {"perr": 0.001, "_tol": 0.02}
        for j in range(16, j_end + 1, 16):
            ok = j >= 400
            vals[f"te_{j}"] = j * self.T
            vals[f"ds_{j}"] = self.T if ok else 0.5 * self.T
        t = dllbench.lock_time(self.T, {"ref_ns": 0.0}, vals, j_end)
        self.assertAlmostEqual(t, 400 * self.T)
        vals[f"ds_{j_end - j_end % 16}"] = 0.5 * self.T  # a late slip: not settled
        self.assertIsNone(dllbench.lock_time(self.T, {"ref_ns": 0.0}, vals, j_end))


class HarnessArity(unittest.TestCase):
    """The start-state arity leg expects the arity the manifest declares for each
    axis, not a hard 2 -- so a bench that deliberately sweeps one start state is
    not a harness fault (issue #92)."""

    def graded(self, bench, states=None, **over):
        """Build `bench`, write one synthetic envelope per request (one corner per
        start state, `states` to restrict which), grade it, return (rc, record)."""
        out = os.path.join(tempfile.mkdtemp(), "o")
        dllbench.build(os.path.join(SIM, bench), out, DUT, 1e9, 0.02, 5.0, "/osdi")
        man = jload(os.path.join(out, "manifest.json"))
        for req in man["requests"]:
            use = [st for st in req["states"] if states is None or st["name"] in states]
            self.assertTrue(use, f"{bench} declares none of {states}")
            env = ic_envelope([ic_corner(f"tt_27_1v2_{st['name']}", st, **over) for st in use])
            with open(os.path.join(out, f"{req['tag']}.envelope.json"), "w", encoding="utf-8") as fh:
                json.dump(env, fh)
        rc = dllbench.grade(os.path.join(SIM, bench), out)
        with open(os.path.join(out, "record.md"), encoding="utf-8") as fh:
            return rc, fh.read()

    def test_single_start_state_bench_is_not_a_harness_fault(self):
        for bench in ("phase", "power"):
            rc, record = self.graded(bench)
            self.assertIn("- harness: PASS", record, bench)
            self.assertNotIn("distinct start states", record, bench)
            self.assertEqual(rc, 0, bench)

    def test_read_back_leg_still_bites_on_a_single_state_bench(self):
        # the one leg that actually proves the axis took effect: move the vic
        # read-back off its swept source value.
        rc, record = self.graded("power", ic_seen=0.9)
        self.assertIn("- harness: FAIL", record)
        self.assertIn("ic_seen=0.9 but vic=0.0", record)
        self.assertEqual(rc, 1)

    def test_nine_state_benches_keep_grading_clean(self):
        # the per-axis expectation must not turn the full nine-state grid red
        # (vic sweeps 6 distinct values at 1 GHz, the other axes 2).
        for bench in ("false-lock", "lock-time"):
            rc, record = self.graded(bench)
            self.assertIn("- harness: PASS", record, bench)
            self.assertNotIn("distinct start states", record, bench)
            self.assertEqual(rc, 0, bench)

    def test_multi_state_axis_short_of_its_declared_arity_is_a_problem(self):
        # s1_min_rail (vic 0.0) and s3_mid (vic 0.5) are 2 distinct vic values --
        # enough for the old hard floor of 2, short of the 6 the manifest declares.
        rc, record = self.graded("false-lock", states=("s1_min_rail", "s3_mid"))
        self.assertIn("- harness: FAIL", record)
        self.assertIn("vic: an initial-condition sweep needs >= 6 distinct start states, saw 2", record)
        self.assertEqual(rc, 1)

    def test_declared_arity_is_per_axis_not_the_state_count(self):
        out = os.path.join(tempfile.mkdtemp(), "o")
        dllbench.build(os.path.join(SIM, "false-lock"), out, DUT, 1e9, 0.02, 5.0, "/osdi")
        req = jload(os.path.join(out, "manifest.json"))["requests"][0]
        self.assertEqual(len(req["states"]), 9)
        declared = {a: len({st["ic"][a] for st in req["states"]}) for a in dllbench.AXES}
        self.assertEqual(declared, {"vic": 6, "vton": 2, "vtdis": 2, "vtre": 2, "vtclk": 2})


if __name__ == "__main__":
    unittest.main()
