"""Guard: one env-knob namespace per bench (issue #120).

    python3 -I -m pytest sim/harness/tests/test_bench_env_namespaces.py -q

Parses every sim/<bench>/run.sh plus the shared helpers
sim/harness/{bench,smoke}-run.sh for environment-knob reads
(${NAME:-default}, ${NAME}, $NAME) and asserts that no knob in the collision
families -- *_RESULTS_DIR, *_CAPACITY_WAIT_S, and the swept-axis knobs *_VC,
*_B_SCALE, *_MC_* -- is read from more than one bench directory. A shared
helper counts as one reader: bench-run.sh's BENCH_RESULTS_DIR and
smoke-run.sh's UNITSMOKE_RESULTS_DIR are invocation-scoped, the ratified
pattern of sim/harness/bench-run.sh.

Before #120 the DS_ prefix was read by two delay benches: exporting DS_VC to
drive one silently replaced the other's swept axis (including delay-sizing's
fine sweep), and DS_RESULTS_DIR redirected both output directories; SS_
similarly pointed both single-unit smoke benches at one results directory.
This test is the guard that keeps those namespaces apart. (The SS_ collision
stayed invisible for so long because neither smoke runner documented the knob
in an `# Env:` header line; the shared helper added by #121 now carries one.)

Runs by hand: CI executes only scripts/check-signoff.sh until #118 lands.
"""

import os
import re
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
HARNESS = os.path.dirname(HERE)
SIM = os.path.dirname(HARNESS)

# Knob families whose sharing breaks recorded evidence: the output directory
# and the fleet capacity wait redirect or block runs, the swept axes (Vc
# grid, B-device scale, Monte Carlo set) change what a bench measures.
def is_guarded_knob(name):
    return (name.endswith(("_RESULTS_DIR", "_CAPACITY_WAIT_S", "_VC", "_B_SCALE"))
            or "_MC_" in name)


# ${NAME:-default} (default may nest ${...}), ${NAME} and $NAME; uppercase
# names only, so the runners' shell-local lowercase variables are not parsed.
KNOB_READ = re.compile(r"\$\{([A-Z][A-Z0-9_]*)(?::-[^}]*)?\}|\$([A-Z][A-Z0-9_]*)")


def bench_runners():
    """(reader id, path) for every bench run.sh and each shared helper."""
    for entry in sorted(os.listdir(SIM)):
        path = os.path.join(SIM, entry, "run.sh")
        if os.path.isfile(path):
            yield entry, path
    for helper in ("bench-run.sh", "smoke-run.sh"):
        yield "harness:" + helper[:-3], os.path.join(HARNESS, helper)


class OneNamespacePerBench(unittest.TestCase):
    def knob_readers(self):
        readers = {}
        nfiles = 0
        for reader, path in bench_runners():
            with open(path) as fh:
                text = fh.read()
            nfiles += 1
            for m in KNOB_READ.finditer(text):
                name = m.group(1) or m.group(2)
                if is_guarded_knob(name):
                    readers.setdefault(name, set()).add(reader)
        self.assertGreater(nfiles, 0, "no bench runner found under sim/")
        return readers

    def test_no_knob_is_read_from_two_benches(self):
        shared = {k: sorted(v) for k, v in self.knob_readers().items() if len(v) > 1}
        self.assertEqual(
            shared, {},
            "env knobs read from more than one bench directory: one namespace "
            "per bench (issue #120); a shared helper counts as one reader")

    def test_known_namespaces_are_seen_exactly_once(self):
        found = self.knob_readers()
        expected = {
            "DSAN_RESULTS_DIR": "delay-sanity",
            "DSAN_VC": "delay-sanity",
            "DSAN_CAPACITY_WAIT_S": "delay-sanity",
            "DSIZ_RESULTS_DIR": "delay-sizing",
            "DSIZ_VC": "delay-sizing",
            "DSIZ_CAPACITY_WAIT_S": "delay-sizing",
            "DSIZ_B_SCALE": "delay-sizing",
            "DSIZ_MC_VC": "delay-sizing",
            "DSIZ_MC_N": "delay-sizing",
            "DSIZ_MC_SEED": "delay-sizing",
            "UNITSMOKE_RESULTS_DIR": "harness:smoke-run",
            "BENCH_RESULTS_DIR": "harness:bench-run",
            "BENCH_CAPACITY_WAIT_S": "harness:bench-run",
        }
        for knob, reader in sorted(expected.items()):
            self.assertEqual(found.get(knob), {reader},
                             f"{knob} must be read only by {reader}, got "
                             f"{sorted(found.get(knob, []))}")


if __name__ == "__main__":
    unittest.main()
