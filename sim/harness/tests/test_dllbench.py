"""Unit tests for sim/harness/dllbench.py and the bench inventory (no simulator).

    python3 -I -m unittest discover -s sim/harness/tests
"""

import json
import os
import re
import shutil
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
        self.assertFalse(dut["supply_current"])
        # Every descriptor key must drive behaviour; `attestable` drove none
        # (attestability of item 9 is sim/inventory.json + `klt signoff`).
        self.assertNotIn("attestable", dut)
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


def powered_dut(tmpdir, **over):
    """A copy of the stand-in descriptor with keys overridden, beside a copy of
    its netlist so build() can find it."""
    dut = jload(DUT)
    dut.update(over)
    shutil.copy(os.path.join(SIM, "standin", dut["netlist"]), os.path.join(tmpdir, dut["netlist"]))
    path = os.path.join(tmpdir, "dut.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(dut, fh)
    return path


class Build(unittest.TestCase):
    def build(self, bench, **kw):
        d = tempfile.mkdtemp()
        out = os.path.join(d, "o")
        dllbench.build(os.path.join(SIM, bench), out, kw.get("dut", DUT),
                       kw.get("f0", 1e9), kw.get("tol", 0.02), 5.0, "/osdi")
        return out

    def pavg_limits(self, out, tag="f100"):
        req = jload(os.path.join(out, "requests", f"{tag}.request.json"))
        return next(m for m in req["measurements"] if m["name"] == "pavg").get("limits")

    def test_power_limit_is_withheld_when_the_dut_draws_no_supply_current(self):
        out = self.build("power")  # the stand-in: supply_current false
        self.assertIsNone(self.pavg_limits(out))
        self.assertFalse(jload(os.path.join(out, "manifest.json"))["supply_current"])

    def test_power_limit_is_attached_when_the_dut_draws_supply_current(self):
        d = tempfile.mkdtemp()
        out = self.build("power", dut=powered_dut(d, supply_current=True))
        self.assertEqual(self.pavg_limits(out), {"max": 5.0})
        self.assertTrue(jload(os.path.join(out, "manifest.json"))["supply_current"])

    def test_withholding_the_power_limit_keeps_the_structural_check_green(self):
        # check() requires every request to carry at least one limit; the
        # predicate limits (rows 2, 8, 12) are in every profile.
        self.assertEqual(dllbench.check(self.build("power")), 0)

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


class PowerVerdict(unittest.TestCase):
    """grade()'s row-10 verdict line, on a synthetic envelope (no simulator)."""

    def graded_record(self, **dut_over):
        d = tempfile.mkdtemp()
        out = os.path.join(d, "o")
        dut = powered_dut(d, **dut_over) if dut_over else DUT
        dllbench.build(os.path.join(SIM, "power"), out, dut, 1e9, 0.02, 5.0, "/osdi")
        man = jload(os.path.join(out, "manifest.json"))
        req = man["requests"][0]
        st = req["states"][0]
        meas = [{"name": "perr", "value": 0.001}, {"name": "vcpp", "value": 1e-6},
                {"name": "d8_64", "value": req["period_s"]},
                {"name": "rail_hi", "value": 0.3}, {"name": "rail_lo", "value": 0.4},
                {"name": "lock_end", "value": 1.0}, {"name": "pavg", "value": 0.0},
                {"name": "ic_seen", "value": st["ic"]["vic"]},
                {"name": "tclk_edge", "value": max(st["ic"]["vtclk"], 0.0) * 1e-9}]
        meas += [{"name": f"{a}_seen", "value": st["ic"][a]} for a in dllbench.AXES[1:]]
        env = {"status": "pass", "passed": 1, "corner_count": 1, "failed": 0, "errored": 0,
               "environment": {"engine": "ngspice", "engine_version": "44"},
               "corners": [{"corner_id": "tt_27_1v20", "status": "pass",
                            "supply_v": dict(st["ic"], Vdd=1.2), "measurements": meas}]}
        with open(os.path.join(out, f"{req['tag']}.envelope.json"), "w", encoding="utf-8") as fh:
            json.dump(env, fh)
        dllbench.grade(os.path.join(SIM, "power"), out)
        with open(os.path.join(out, "record.md"), encoding="utf-8") as fh:
            text = fh.read()
        m = re.search(r"^- rows 10 on this DUT: (.*)$", text, re.M)
        self.assertIsNotNone(m, text)
        return m.group(1)

    def test_zero_power_reading_is_not_reported_as_a_pass(self):
        verdict = self.graded_record()  # the stand-in: supply_current false
        self.assertIn("NOT GRADED", verdict)
        self.assertNotIn("corners pass", verdict)

    def test_a_dut_that_draws_supply_current_is_graded(self):
        verdict = self.graded_record(supply_current=True)
        # a corner verdict either way, never the ungraded line
        self.assertRegex(verdict, r"^(all corners pass|NOT all corners pass)")


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


if __name__ == "__main__":
    unittest.main()
