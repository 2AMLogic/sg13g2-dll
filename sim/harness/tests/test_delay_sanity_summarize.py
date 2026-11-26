"""delay-sanity headings use the shared evidence.corners_of() formatter.

`sim/delay-sanity/summarize.py` used to carry a private per-axis corner
reducer that rendered a multi-corner envelope as unpaired ranges (a
cross-product of process, Vdd and temperature the run never used) and raised
on a missing envelope. It now routes through `evidence.corners_of()`, as every
other `sim/` summarizer does. These tests run `summarize.py` on a scratch copy
of the committed `20261105T080322Z` envelopes (append-only evidence: the
committed tree is never written) and pin the `### corner` headings.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.dirname(os.path.dirname(HERE))
SUMMARIZE = os.path.join(SIM, "delay-sanity", "summarize.py")
CORPUS = os.path.join(SIM, "delay-sanity", "results", "20261105T080322Z")
sys.path.insert(0, os.path.join(SIM, "harness"))

import evidence  # noqa: E402


def _headings(record):
    return re.findall(r"^### corner (\w+) \((.*?); status", record, re.M)


class DelaySanityCornerHeadings(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        for f in os.listdir(CORPUS):
            if f.endswith(".envelope.json"):
                shutil.copy(os.path.join(CORPUS, f), self.tmp)

    def _run(self):
        subprocess.run([sys.executable, "-I", SUMMARIZE, self.tmp],
                       capture_output=True, text=True)  # exit 1 on a graded gap is expected
        with open(os.path.join(self.tmp, "record.md")) as fh:
            return fh.read()

    def test_headings_match_shared_formatter(self):
        heads = _headings(self._run())
        self.assertEqual(len(heads), 6)
        env = json.load(open(os.path.join(self.tmp, "1GHz_ss.envelope.json")))
        self.assertIn(("ss", evidence.corners_of(env)), heads)
        self.assertIn(("ss", "mos_ss/1.08 V/125 C"), heads)

    def test_multi_corner_envelope_is_paired_not_cross_product(self):
        p = os.path.join(self.tmp, "1GHz_tt.envelope.json")
        env = json.load(open(p))
        base = env["corners"][0]
        mixed = []
        for proc, vdd, t in (("mos_tt", 1.2, 27), ("mos_ss", 1.08, 125), ("mos_ff", 1.32, -40)):
            cr = json.loads(json.dumps(base))
            cr.update(process=proc, temperature_c=t)
            cr["supply_v"]["Vdd"] = vdd
            mixed.append(cr)
        env["corners"] = mixed
        json.dump(env, open(p, "w"))
        text = dict(_headings(self._run()))["tt"]
        self.assertEqual(text, "mos_tt/1.2 V/27 C, mos_ss/1.08 V/125 C, mos_ff/1.32 V/-40 C")
        self.assertNotIn("..", text)


if __name__ == "__main__":
    unittest.main()
