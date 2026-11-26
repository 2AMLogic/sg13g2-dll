"""noise-method provenance is read from the envelope, not the host disk.

`sim/noise-method/summarize.py` records its OSDI and PDK provenance lines the
way every other `sim/` summarizer does (#99, #119, #125): the OSDI hashes come
from `environment.osdi_preload` of the envelope the run wrote, and the PDK tag
from `sim/pdk.json` -- never from re-hashing `$SG13G2_OSDI_DIR` on the
summarizing host. The old disk re-hash recorded host state, not what the
simulation loaded: without `SG13G2_OSDI_DIR` set it silently emitted an empty
OSDI line, and with a different on-disk tree it stamped the wrong hashes onto
an old run's record.

These tests re-run `summarize` on a scratch copy of the committed
`20261115T041503Z` corpus (append-only evidence: the committed tree itself is
never written) with `SG13G2_OSDI_DIR` scrubbed from the environment, and pin:

- the scratch record reproduces the committed `record.md` line-for-line
  (except the UTC stamp line, which carries the wall clock of the re-run, and
  the PDK line, which carries the live `sim/pdk.json` pin rather than the pin
  of the run that was committed);
- the final amplitude in the scratch record matches the staged calibration
  commands when rounding the first amplitude affects the second;
- a mutated `osdi_preload` sha256 in the envelope moves the OSDI line, the
  mutation control proving the line follows the envelope and not disk;
- a scratch `sim/` tree whose `pdk.json` pins `vX` renders its PDK line with
  `vX`, proving the line follows `pdk.json` and not a tag hardcoded in
  `summarize.py`;
- a bare `summarize.py` exits 2 with the `Usage:` text and no traceback, and
  the usage documents the real argument lists of `calibrate`/`calibrate2`.

The committed corpus is a graded FAIL (pooled sigma_t outside the 0014
tolerance), so a successful summarize of it exits 1 deterministically; the
record is still written.

Nothing here simulates.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.dirname(os.path.dirname(HERE))
NOISE_METHOD = os.path.join(SIM, "noise-method")
RESULTS = os.path.join(NOISE_METHOD, "results", "20261115T041503Z")
STAMP_LINE = 7  # 0-based index of "- Stamp: ... (UTC ...)", line 8: the re-run's wall clock
PDK_LINE = 10  # 0-based index of "- PDK: ... (sim/pdk.json)", line 11: the live sim/pdk.json pin


def run_summarize(*args, script=None):
    """Run summarize.py isolated, with SG13G2_OSDI_DIR scrubbed from the env."""
    env = {k: v for k, v in os.environ.items() if k != "SG13G2_OSDI_DIR"}
    script = script or os.path.join(NOISE_METHOD, "summarize.py")
    return subprocess.run(
        [sys.executable, "-I", script, *args],
        capture_output=True,
        text=True,
        env=env,
    )


def scratch_copy(parent=None):
    """Temp copy of the committed corpus under its own basename (the Stamp line
    names the directory); the committed tree is never written. `parent` places
    it under that directory instead of its own temp root."""
    root = parent or tempfile.mkdtemp()
    scratch = os.path.join(root, os.path.basename(RESULTS))
    shutil.copytree(RESULTS, scratch)
    return root, scratch


def pinned_tree(tag):
    """Temp `sim/` tree whose `pdk.json` pins `tag`, around a scratch copy of
    the corpus: a copy of `summarize.py` (it reads `pdk.json` from next to its
    own directory) and a symlink to `harness` (it imports `../harness/evidence`)."""
    root = tempfile.mkdtemp()
    sim = os.path.join(root, "sim")
    noise_method = os.path.join(sim, "noise-method")
    results = os.path.join(noise_method, "results")
    os.makedirs(results)
    script = os.path.join(noise_method, "summarize.py")
    shutil.copy(os.path.join(NOISE_METHOD, "summarize.py"), script)
    os.symlink(os.path.join(SIM, "harness"), os.path.join(sim, "harness"))
    with open(os.path.join(sim, "pdk.json"), "w", encoding="utf-8") as fh:
        json.dump({"release_tag": tag}, fh)
    _, scratch = scratch_copy(results)
    return root, script, scratch


def record_lines(out_dir):
    with open(os.path.join(out_dir, "record.md"), encoding="utf-8") as fh:
        return fh.read().splitlines()


class RecordReproduction(unittest.TestCase):
    def test_summarize_reproduces_committed_record_without_osdi_dir(self):
        root, scratch = scratch_copy()
        self.addCleanup(shutil.rmtree, root, True)
        proc = run_summarize("summarize", scratch)
        self.assertEqual(proc.returncode, 1, proc.stderr)  # the corpus is a graded FAIL
        committed = record_lines(RESULTS)
        produced = record_lines(scratch)
        self.assertEqual(len(produced), len(committed))
        self.assertTrue(
            committed[STAMP_LINE].startswith("- Stamp: 20261115T041503Z (UTC "),
            f"line {STAMP_LINE + 1} of the committed record is not the stamp: {committed[STAMP_LINE]!r}",
        )
        self.assertRegex(
            committed[PDK_LINE],
            r"^- PDK: IHP-Open-PDK \S+ \(sim/pdk\.json\)$",
            f"line {PDK_LINE + 1} of the committed record is not the PDK line: {committed[PDK_LINE]!r}",
        )
        for i, (want, got) in enumerate(zip(committed, produced)):
            if i in (STAMP_LINE, PDK_LINE):
                continue
            self.assertEqual(got, want, f"record.md line {i + 1} differs")

    def test_final_amplitude_matches_staged_deck_calibration(self):
        root, scratch = scratch_copy()
        self.addCleanup(shutil.rmtree, root, True)
        probe_path = os.path.join(scratch, "sigma-probe.envelope.json")
        with open(probe_path, encoding="utf-8") as fh:
            probe = json.load(fh)
        readings = probe["corners"][0]["measurements"]
        vmrms = next(reading for reading in readings if reading["name"] == "vmrms")
        vmrms["value"] = 6.78455e-6
        with open(probe_path, "w", encoding="utf-8") as fh:
            json.dump(probe, fh)

        first = run_summarize("calibrate", scratch, "sigma-probe", "1e-9")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout.strip(), "1.015447e-06")
        final = run_summarize("calibrate2", scratch, first.stdout.strip())
        self.assertEqual(final.returncode, 0, final.stderr)
        self.assertEqual(final.stdout.strip(), "1.046149e-06")

        report = run_summarize("summarize", scratch)
        self.assertEqual(report.returncode, 1, report.stderr)  # graded jitter failure
        line = next(
            line
            for line in record_lines(scratch)
            if line.startswith("- Final amplitude:")
        )
        self.assertEqual(line.rsplit(" = ", 1)[-1], f"{final.stdout.strip()} A")


class EnvelopeProvenance(unittest.TestCase):
    def test_osdi_line_follows_the_envelope_not_disk(self):
        root, scratch = scratch_copy()
        self.addCleanup(shutil.rmtree, root, True)
        env_path = os.path.join(scratch, "sigma-s1.envelope.json")
        with open(env_path, encoding="utf-8") as fh:
            env = json.load(fh)
        for entry in env["environment"]["osdi_preload"]:
            entry["sha256"] = "0123456789abcdef" + "0" * 48
        with open(env_path, "w", encoding="utf-8") as fh:
            json.dump(env, fh)
        proc = run_summarize("summarize", scratch)
        self.assertEqual(proc.returncode, 1, proc.stderr)
        osdi_lines = [l for l in record_lines(scratch) if l.startswith("- OSDI")]
        self.assertEqual(len(osdi_lines), 1)
        self.assertIn("0123456789abcdef", osdi_lines[0])


class PdkProvenance(unittest.TestCase):
    def test_pdk_line_follows_pdk_json_not_a_hardcoded_tag(self):
        root, script, scratch = pinned_tree("vX")
        self.addCleanup(shutil.rmtree, root, True)
        proc = run_summarize("summarize", scratch, script=script)
        self.assertEqual(proc.returncode, 1, proc.stderr)
        pdk_lines = [l for l in record_lines(scratch) if l.startswith("- PDK")]
        self.assertEqual(pdk_lines, ["- PDK: IHP-Open-PDK vX (sim/pdk.json)"])


class CliGuard(unittest.TestCase):
    def test_no_arguments_exits_2_with_usage_and_no_traceback(self):
        proc = run_summarize()
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertIn("Usage:", proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)

    def test_usage_documents_the_real_argument_lists(self):
        proc = run_summarize()
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertIn("calibrate OUT TAG IA", proc.stderr)
        self.assertIn("calibrate2 OUT IA_1", proc.stderr)


if __name__ == "__main__":
    unittest.main()
