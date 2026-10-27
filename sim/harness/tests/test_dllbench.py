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

BENCHES = ("lock-range", "phase", "lock-time", "false-lock", "power")
DUT = os.path.join(SIM, "standin", "dut.json")


def jload(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


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
        j_end = dllbench.window_end(self.T)
        vals = {"perr": 0.001, "_tol": 0.02}
        for j in range(16, j_end + 1, 16):
            ok = j >= 400
            vals[f"te_{j}"] = j * self.T
            vals[f"ds_{j}"] = self.T if ok else 0.5 * self.T
        t = dllbench.lock_time(self.T, {"ref_ns": 0.0}, vals, j_end)
        self.assertAlmostEqual(t, 400 * self.T)
        vals[f"ds_{j_end - j_end % 16}"] = 0.5 * self.T  # a late slip: not settled
        self.assertIsNone(dllbench.lock_time(self.T, {"ref_ns": 0.0}, vals, j_end))


if __name__ == "__main__":
    unittest.main()
