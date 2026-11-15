"""Fixture tests for sim/harness/smoke_summarize.py (stdlib unittest).

    python3 -I -m unittest discover -s sim/harness/tests

Pins the record.md text the lock-detector and supervisor smoke benches produce.
Run conditions and measurement units must come from the envelope, so each case
states what the envelope recorded and asserts the record repeats exactly that.
Nothing here simulates.
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
HARNESS = os.path.dirname(HERE)
SCRIPT = os.path.join(HARNESS, "smoke_summarize.py")

NOTE = "Simulated, never measured. Limits are smoke gates, not spec numbers.\n\n"


def header(bench, conditions=None):
    """The record head: title, the envelope's run conditions (if any), the note."""
    return f"# {bench} record\n\n" + (f"{conditions}\n" if conditions else "") + NOTE


def envelope(meas, diags=None, environment=None, corner=None):
    """A one-corner envelope. `corner`/`environment` default to the committed
    lock-detector smoke run: tt / Vdd 1.2 V / 27 C, ngspice 46, backend local."""
    c = {"measurements": meas, "diagnostics": diags or []}
    c.update({"process": "tt", "supply_v": {"Vdd": 1.2}, "temperature_c": 27}
             if corner is None else corner)
    return {"corners": [c],
            "environment": {"engine": "ngspice", "engine_version": "46",
                            "backend": {"resolved": "local", "requested": "local"}}
            if environment is None else environment}


DEFAULT_CONDITIONS = ("Run conditions, as the envelope recorded them: "
                      "corner tt, Vdd 1.2 V, 27 C; engine ngspice 46; backend local.")


class SmokeSummarize(unittest.TestCase):
    def run_case(self, bench, prefix, env, klt_rc=0):
        with tempfile.TemporaryDirectory() as out:
            if env is not None:
                with open(os.path.join(out, f"{prefix}.envelope.json"), "w", encoding="utf-8") as f:
                    json.dump(env, f)
            p = subprocess.run([sys.executable, "-I", SCRIPT, out, str(klt_rc), bench, prefix],
                               capture_output=True, text=True)
            with open(os.path.join(out, "record.md"), encoding="utf-8") as f:
                return p.returncode, f.read(), p.stdout

    def test_pass_states_each_measurement_unit_from_the_envelope(self):
        # The lock-detector bench measures a voltage and a time in one record;
        # a fixed "value (s)" column mislabels the first (issue #99).
        for bench, prefix in (("lock-detector-smoke", "ld"), ("supervisor-smoke", "sup")):
            rc, rec, out = self.run_case(bench, prefix, envelope([
                {"name": "lock_max_before_220n", "value": 4.13e-5, "unit": "V", "status": "pass"},
                {"name": "t_lock", "value": 1.5e-9, "unit": "s", "status": "pass"}]))
            self.assertEqual(rc, 0)
            self.assertEqual(rec, header(bench, DEFAULT_CONDITIONS) +
                             "| measurement | value | unit | status |\n|---|---|---|---|\n"
                             "| lock_max_before_220n | 4.13e-05 | V | pass |\n"
                             "| t_lock | 1.5e-09 | s | pass |\n\nRESULT: PASS\n")
            self.assertEqual(out, rec)

    def test_run_conditions_follow_the_envelope_not_a_constant(self):
        # Same grader, a different corner on a different backend: the record
        # must say so rather than repeat the typical-corner/local literal.
        rc, rec, _ = self.run_case("supervisor-smoke", "sup", envelope(
            [{"name": "t", "value": 1e-9, "unit": "s", "status": "pass"}],
            corner={"process": "mos_ss", "supply_v": {"Vdd": 1.08}, "temperature_c": 125},
            environment={"engine": "ngspice", "engine_version": "42",
                         "backend": {"resolved": "batch", "requested": "batch"}}))
        self.assertEqual(rc, 0)
        self.assertTrue(rec.startswith(header("supervisor-smoke", (
            "Run conditions, as the envelope recorded them: "
            "corner mos_ss, Vdd 1.08 V, 125 C; engine ngspice 42; backend batch."))), rec)

    def test_conditions_omitted_when_the_envelope_records_none(self):
        # Nothing known about the run: say nothing, do not invent conditions.
        rc, rec, _ = self.run_case("supervisor-smoke", "sup", {"corners": [
            {"measurements": [{"name": "t", "value": 1e-9, "unit": "s", "status": "pass"}],
             "diagnostics": []}]})
        self.assertEqual(rc, 0)
        self.assertTrue(rec.startswith(header("supervisor-smoke")), rec)
        self.assertNotIn("Run conditions", rec)

    def test_unit_absent_from_the_envelope_is_not_guessed(self):
        rc, rec, _ = self.run_case(
            "supervisor-smoke", "sup", envelope([{"name": "t", "value": 1e-9, "status": "pass"}]))
        self.assertEqual(rc, 0)
        self.assertIn("| t | 1e-09 | ? | pass |", rec)

    def test_fail(self):
        rc, rec, _ = self.run_case(
            "supervisor-smoke", "sup", envelope([{"name": "t", "value": 2e-9, "status": "fail"}]))
        self.assertEqual(rc, 6)
        self.assertTrue(rec.endswith("RESULT: FAIL\n"))

    def test_error_diagnostic_is_not_run(self):
        rc, rec, _ = self.run_case(
            "lock-detector-smoke", "ld",
            envelope([{"name": "t", "value": None}],
                     [{"severity": "error", "message": "model load failed"}]))
        self.assertEqual(rc, 6)
        self.assertEqual(rec, header("lock-detector-smoke", DEFAULT_CONDITIONS) +
                         "RESULT: NOT-RUN\n\nBackend/engine error (verbatim):\n\n    model load failed\n")

    def test_missing_value_is_not_run(self):
        rc, rec, _ = self.run_case(
            "lock-detector-smoke", "ld", envelope([{"name": "t", "value": None, "status": "pass"}]))
        self.assertEqual(rc, 6)
        self.assertIn("RESULT: NOT-RUN", rec)
        self.assertIn("    (no message)", rec)

    def test_missing_envelope_names_prefix_stderr(self):
        # No envelope at all: no conditions can be read, so none are stated.
        rc, rec, _ = self.run_case("supervisor-smoke", "sup", None, klt_rc=7)
        self.assertEqual(rc, 6)
        self.assertEqual(rec, header("supervisor-smoke") +
                         "RESULT: NOT-RUN\n\nBackend/engine error (verbatim):\n\n"
                         "    no envelope written (klt exit 7); see sup.stderr\n")


if __name__ == "__main__":
    unittest.main()
