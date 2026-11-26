"""Guard: the DLL bench tests release their scratch directories (issue #254).

    python3 -I -m unittest discover -s sim/harness/tests -p test_dllbench_scratch.py

test_dllbench.py builds every bench into a fresh temporary directory. Those
directories came from bare tempfile.mkdtemp() calls and were never removed:
one run of the module left 53 of them in TMPDIR (472 files, about 10 MB),
and repeated local runs accumulated generated decks, requests and synthetic
grading records.

This guard runs the whole of test_dllbench against a private temporary root
and asserts the root is empty once the run is over. Every test of that module
runs, so a bare mkdtemp() added anywhere in it, helper or test, turns this
red; pinning only the sites named in the issue would not.

Nothing here simulates.
"""

import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import test_dllbench  # noqa: E402


class ScratchReleased(unittest.TestCase):
    def test_no_scratch_directory_outlives_the_module(self):
        with tempfile.TemporaryDirectory() as root:
            outer = tempfile.tempdir
            tempfile.tempdir = root
            try:
                suite = unittest.defaultTestLoader.loadTestsFromModule(test_dllbench)
                result = unittest.TestResult()
                suite.run(result)
            finally:
                tempfile.tempdir = outer
            self.assertTrue(result.wasSuccessful(), result.failures + result.errors)
            self.assertGreater(result.testsRun, 0)
            self.assertEqual(os.listdir(root), [])


if __name__ == "__main__":
    unittest.main()
