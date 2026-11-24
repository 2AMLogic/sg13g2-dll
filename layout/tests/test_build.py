"""Regression tests for layout/build.sh report publication (PR #222).

Runs a copy of build.sh in a throwaway git checkout with stub KLT / GEN, so no
KLayout, klt or PDK is needed. Covers: exact verdict comparison, preserved
report mode, and per-invocation run summaries.
"""
import hashlib
import json
import os
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent / "build.sh"
CELLS = ("loop_filter", "cp_bias", "cp")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class BuildPublish(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        r = self.tmp
        (r / "layout").mkdir()
        shutil.copy(BUILD, r / "layout" / "build.sh")
        (r / "layout" / "check_psd.py").write_text("")
        for c in CELLS:
            (r / "layout" / c).mkdir()
            (r / "layout" / c / f"{c}.gds").write_bytes(b"gds-" + c.encode())
            for n, v in (("drc", "clean"), ("lvs", "match")):
                f = r / "layout" / c / f"{n}_report.json"
                f.write_text('{"status":"%s"}' % v)
                f.chmod(0o644)
            (r / "layout" / c / "lvs_request.json").write_text("{}")
        # Stub klt: prints $DRC_OUT / $LVS_OUT (raw), exit code $KLT_RC.
        klt = r / "klt-stub.sh"
        klt.write_text(
            '#!/usr/bin/env bash\n'
            'case "$1" in drc) printf "%s" "$DRC_OUT";; lvs) printf "%s" "$LVS_OUT";;'
            ' version) echo stub;; esac\nexit "${KLT_RC:-0}"\n')
        klt.chmod(0o755)
        git = lambda *a: subprocess.run(
            ["git", "-C", str(r), "-c", "user.name=t", "-c", "user.email=t@t", *a],
            check=True, capture_output=True)
        git("init", "-q")
        git("add", "-A")
        git("commit", "-q", "-m", "init")
        self.reports = [r / "layout" / c / f"{n}_report.json"
                        for c in CELLS for n in ("drc", "lvs")]

    def run_build(self, drc='{"status":"clean"}', lvs='{"status":"match"}', **env):
        e = dict(os.environ, KLT=str(self.tmp / "klt-stub.sh"), GEN="true",
                 DRC_OUT=drc, LVS_OUT=lvs, **env)
        return subprocess.run(["bash", str(self.tmp / "layout" / "build.sh")],
                              env=e, capture_output=True, text=True)

    def test_good_run_preserves_mode(self):
        r = self.run_build()
        self.assertEqual(r.returncode, 0, r.stderr)
        for f in self.reports:
            self.assertEqual(stat.S_IMODE(f.stat().st_mode), 0o644, f)
        self.assertEqual(list((self.tmp / "layout" / "runs").glob(".current*")), [])

    def _rejected(self, **kw):
        before = {f: sha(f) for f in self.reports}
        r = self.run_build(**kw)
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(before, {f: sha(f) for f in self.reports})
        self.assertEqual(list(self.tmp.rglob("*_report.json.*")), [])

    def test_drc_status_trailing_newline_rejected(self):
        self._rejected(drc='{"status":"clean\\n"}')

    def test_lvs_status_trailing_newline_rejected(self):
        self._rejected(lvs='{"status":"match\\n"}')

    def test_wrong_verdict_and_bad_json_rejected(self):
        self._rejected(drc='{"status":"dirty"}')
        self._rejected(lvs="not json {")

    def test_concurrent_summary_isolated(self):
        # A failing build's exit trap must not delete a sibling's summary.
        runs = self.tmp / "layout" / "runs"
        runs.mkdir(exist_ok=True)
        other = runs / ".current.sibling"
        other.write_text("keep\n")
        self.assertNotEqual(self.run_build(drc='{"status":"dirty"}').returncode, 0)
        self.assertTrue(other.exists())


if __name__ == "__main__":
    unittest.main()
