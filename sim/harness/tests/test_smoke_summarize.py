"""Fixture tests for sim/harness/smoke_summarize.py (stdlib unittest).

    python3 -I -m unittest discover -s sim/harness/tests

Pins the record.md text the lock-detector and supervisor smoke benches used to
produce from their own copies of this grader. Nothing here simulates.
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

HEADER = (
    "# {bench} record\n\n"
    "Typical corner (mos_tt, res_typ, 1.2 V, 27 C), 1 GHz, single unit, `klt sim --backend local`.\n"
    "Simulated, never measured. Limits are smoke gates, not spec numbers.\n\n"
)


def envelope(meas, diags=None):
    return {"corners": [{"measurements": meas, "diagnostics": diags or []}]}


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

    def test_pass(self):
        for bench, prefix in (("lock-detector-smoke", "ld"), ("supervisor-smoke", "sup")):
            rc, rec, out = self.run_case(
                bench, prefix, envelope([{"name": "t_lock", "value": 1.5e-9, "status": "pass"}]))
            self.assertEqual(rc, 0)
            self.assertEqual(rec, HEADER.format(bench=bench) +
                             "| measurement | value (s) | status |\n|---|---|---|\n"
                             "| t_lock | 1.5e-09 | pass |\n\nRESULT: PASS\n")
            self.assertEqual(out, rec)

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
        self.assertEqual(rec, HEADER.format(bench="lock-detector-smoke") +
                         "RESULT: NOT-RUN\n\nBackend/engine error (verbatim):\n\n    model load failed\n")

    def test_missing_value_is_not_run(self):
        rc, rec, _ = self.run_case(
            "lock-detector-smoke", "ld", envelope([{"name": "t", "value": None, "status": "pass"}]))
        self.assertEqual(rc, 6)
        self.assertIn("RESULT: NOT-RUN", rec)
        self.assertIn("    (no message)", rec)

    def test_missing_envelope_names_prefix_stderr(self):
        rc, rec, _ = self.run_case("supervisor-smoke", "sup", None, klt_rc=7)
        self.assertEqual(rc, 6)
        self.assertEqual(rec, HEADER.format(bench="supervisor-smoke") +
                         "RESULT: NOT-RUN\n\nBackend/engine error (verbatim):\n\n"
                         "    no envelope written (klt exit 7); see sup.stderr\n")


if __name__ == "__main__":
    unittest.main()
