"""Guard: one env-knob namespace per bench (issue #120).

    python3 -m unittest discover -s sim/harness/tests \
        -p 'test_bench_env_namespaces.py' -v

CI runs this suite (.github/workflows/tests.yml: `python3 -I -m unittest
discover -s sim/harness/tests`); `pytest` is not importable under `-I`, so
the unittest invocation above is the one to run by hand.

Scans every sim/<bench>/run.sh plus every shell helper under sim/harness/
(discovered by glob, recursively, tests/ excluded) for environment-knob
reads -- ${NAME:-default} including a guarded knob nested inside a default,
${NAME}, and $NAME -- and asserts that no knob in the collision families
(*_RESULTS_DIR, *_CAPACITY_WAIT_S, and the swept-axis knobs *_VC, *_B_SCALE,
*_MC_*) is read from more than one shell file. A shared helper counts
as one reader: bench-run.sh's BENCH_RESULTS_DIR and smoke-run.sh's
UNITSMOKE_RESULTS_DIR are invocation-scoped, the ratified pattern of
sim/harness/bench-run.sh.

Issue #137 hardened the guard itself, in this file only:

- Helpers are globbed instead of named, so a helper added under
  sim/harness/ that reads a guarded knob is scanned. Removing any helper
  fails the floor test; renaming bench-run.sh or smoke-run.sh fails the
  anchor test. Renaming a helper that reads no guarded knob keeps coverage
  under the glob and is deliberately not a failure.
- A knob read only inside another knob's ``:-`` default is counted: the
  braced match stops after the name, so finditer walks into the default's
  body. Fixture tests pin the single-nesting case the previous regex
  swallowed (a two-knob fixture passes unfixed -- use one).
- The positive coverage claim is structural, not a hand-edited knob dict:
  every guarded knob found must have exactly one reader, and every scanned
  file whose text $-mentions a guarded knob must have those mentions
  parsed. The mentions scan is a deliberately cruder superset of KNOB_READ,
  so a parser that stops matching fails loudly instead of vacuously. A
  shape KNOB_READ misses but the mentions scan still sees (e.g.
  ``${KNOB%pattern}``) fails the suite as that mismatch, rather than
  passing silently; a shape neither sees (e.g. ``$((KNOB))``, ``${!KNOB}``
  -- no runner or helper uses either today) would need both taught.

Issue #142 added the discoverability half of that contract: a knob that
exists and works but is written nowhere is undiscoverable -- the pre-#143
noise-method run.sh read NOISE_METHOD_RESULTS_DIR with no `# Env:` header
line at all (issue #134), the same gap that hid the SS_ collision. The
suite now asserts every guarded knob a scanned file reads -- reads coming
from knob_readers(), so a prose mention carrying no `$` is never a
reader -- is named somewhere in that file's `# Env:` block, continuation
lines included, at any indent. env_block() extracts the block: the
`# Env:` line plus the comment lines after it, ending at the first
non-comment line or at a comment that opens a new `# Word:` label
section, so a knob named only under a following `# Exit:` heading does
not count. Fixture tests pin each way the check could silently stop
working: documentation on a continuation line alone, prose-only mentions,
no block at all, a block silent on the knob, and the label boundary.

Before #120 the DS_ prefix was read by two delay benches: exporting DS_VC to
drive one silently replaced the other's swept axis (including delay-sizing's
fine sweep), and DS_RESULTS_DIR redirected both output directories; SS_
similarly pointed both single-unit smoke benches at one results directory.
This test is the guard that keeps those namespaces apart. (The SS_ collision
stayed invisible for so long because neither smoke runner documented the knob
in an `# Env:` header line; the shared helper added by #121 now carries one.)
"""

import os
import re
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
HARNESS = os.path.dirname(HERE)
SIM = os.path.dirname(HARNESS)

# Removing any scanned helper must fail the suite (issue #137): six exist
# today. Raise when a helper lands; lower only when one is removed on
# purpose -- a floor that must be edited to lose coverage is safe.
HELPER_FLOOR = 6
# Parser-death backstop, well under the guarded knobs read today (24): a
# bench removal can legitimately lower the count, so this stays coarse.
KNOB_FLOOR = 10


# Knob families whose sharing breaks recorded evidence: the output directory
# and the fleet capacity wait redirect or block runs, the swept axes (Vc
# grid, B-device scale, Monte Carlo set) change what a bench measures.
def is_guarded_knob(name):
    return (name.endswith(("_RESULTS_DIR", "_CAPACITY_WAIT_S", "_VC", "_B_SCALE"))
            or "_MC_" in name)


# ${NAME... -- the braced match stops after the name, so a `:-` default that
# nests ${...} or $NAME is still walked -- and $NAME. Uppercase names only,
# so the runners' shell-local lowercase variables are not parsed.
KNOB_READ = re.compile(r"\$\{([A-Z][A-Z0-9_]*)(?=[:}])|\$([A-Z][A-Z0-9_]*)")

# Deliberately cruder superset of KNOB_READ for the completeness test: any
# $-introduced uppercase token, family-filtered afterwards. It sees a knob
# wherever KNOB_READ sees one (and more), so a file whose mentions the
# parser misses is a swallowed read, not a scan gap.
ANY_VAR = re.compile(r"\$\{?([A-Z][A-Z0-9_]*)")


def guarded_mentions(text):
    return {n for n in ANY_VAR.findall(text) if is_guarded_knob(n)}


def harness_helpers(harness=HARNESS):
    """Paths of every shell helper under sim/harness/, tests/ excluded."""
    found = []
    for root, dirs, files in os.walk(harness):
        dirs[:] = [d for d in dirs if d != "tests"]
        for name in sorted(files):
            if name.endswith(".sh"):
                found.append(os.path.join(root, name))
    return sorted(found)


def bench_runners(sim=SIM, harness=HARNESS):
    """Paths of every bench run.sh and each shared helper."""
    for entry in sorted(os.listdir(sim)):
        path = os.path.join(sim, entry, "run.sh")
        if os.path.isfile(path):
            yield path
    yield from harness_helpers(harness)


def reader_id(path, sim):
    """Use sim-relative paths with the same separators as the anchor table."""
    return os.path.relpath(path, sim).replace(os.sep, "/")


def knob_readers(sim=SIM, harness=HARNESS):
    """Guarded knob -> set of reader ids, across the given roots."""
    readers = {}
    for path in bench_runners(sim, harness):
        reader = reader_id(path, sim)
        with open(path) as fh:
            text = fh.read()
        for m in KNOB_READ.finditer(text):
            name = m.group(1) or m.group(2)
            if is_guarded_knob(name):
                readers.setdefault(name, set()).add(reader)
    return readers


def collisions(readers):
    return {k: sorted(v) for k, v in readers.items() if len(v) > 1}


# bench-run.sh and smoke-run.sh own the invocation-scoped namespaces of the
# ratified bench-run pattern (#121/#135); anchoring them pins the harness
# mechanism, so renaming either fails loudly. Benches themselves are covered
# structurally, never listed.
ANCHORED_NAMESPACES = {
    "BENCH_RESULTS_DIR": "harness/bench-run.sh",
    "BENCH_CAPACITY_WAIT_S": "harness/bench-run.sh",
    "UNITSMOKE_RESULTS_DIR": "harness/smoke-run.sh",
}


def anchored_namespace_violations(readers):
    violations = {}
    for knob, want in ANCHORED_NAMESPACES.items():
        got = readers.get(knob, set())
        if got != {want}:
            violations[knob] = sorted(got)
    return violations


# The `# Env:` header block of a scanned file: the `# Env:` line plus the
# comment lines after it, at any continuation indent, up to the first
# non-comment line or the comment that opens the next `# Word:` label
# section (bench-run.sh and smoke-run.sh follow the block with `# Exit:`).
ENV_START = re.compile(r"^#\s*Env:")
NEW_LABEL = re.compile(r"^#\s*[A-Z][A-Za-z]*:")
# Documentation tokens, not reads: upper-case names occurring anywhere in
# an `# Env:` block. KNOB_READ stays the only knob-read matcher (issue
# #142); this only decides whether a name the parser already found is
# written down.
ENV_TOKEN = re.compile(r"[A-Z][A-Z0-9_]*")


def env_block(text):
    """The `# Env:` header block, continuation lines included."""
    out, inside = [], False
    for line in text.splitlines():
        if ENV_START.match(line):
            inside = True
            out.append(line)
        elif inside:
            if line.startswith("#") and not NEW_LABEL.match(line):
                out.append(line)
            else:
                inside = False
    return "\n".join(out)


def undocumented_env_knobs(sim=SIM, harness=HARNESS):
    """Reader id -> sorted guarded knobs it reads but its `# Env:` block omits.

    Reads come from knob_readers(), so a prose mention with no `$` never
    counts as a reader (issue #142's trap 2 is unreachable by construction).
    """
    readers = knob_readers(sim, harness)
    undocumented = {}
    for path in bench_runners(sim, harness):
        reader = reader_id(path, sim)
        mine = {k for k, rs in readers.items() if reader in rs}
        if not mine:
            continue
        with open(path) as fh:
            text = fh.read()
        missing = mine - set(ENV_TOKEN.findall(env_block(text)))
        if missing:
            undocumented[reader] = sorted(missing)
    return undocumented


class OneNamespacePerBench(unittest.TestCase):
    """The live sim/ tree: no collision, coverage that cannot shrink silently."""

    def test_no_knob_is_read_from_two_files(self):
        shared = collisions(knob_readers())
        self.assertEqual(
            shared, {},
            "env knobs read from more than one shell file: one namespace "
            "per bench (issue #120); a shared helper counts as one reader")

    def test_known_namespaces_are_seen_exactly_once(self):
        found = knob_readers()
        self.assertTrue(found, "parser matched no guarded knob at all")
        self.assertGreaterEqual(
            len(found), KNOB_FLOOR,
            f"only {len(found)} guarded knobs matched: the parser has likely "
            f"stopped matching (issue #137)")
        for knob, readers in sorted(found.items()):
            self.assertEqual(len(readers), 1, f"{knob} read by {sorted(readers)}")

    def test_invocation_scoped_helper_namespaces_are_anchored(self):
        violations = anchored_namespace_violations(knob_readers())
        self.assertEqual(
            violations, {},
            "anchored helper namespaces moved: a scanned helper was renamed "
            "(issue #137)")

    def test_helper_discovery_meets_the_floor(self):
        helpers = harness_helpers()
        self.assertGreaterEqual(
            len(helpers), HELPER_FLOOR,
            f"only {len(helpers)} shell helpers under {HARNESS}: a scanned "
            f"helper was removed and coverage shrank silently (issue #137)")

    def test_every_file_mentioning_a_guarded_knob_is_parsed(self):
        found = knob_readers()
        for path in bench_runners():
            reader = reader_id(path, SIM)
            with open(path) as fh:
                text = fh.read()
            mentioned = guarded_mentions(text)
            if not mentioned:
                continue
            parsed = {k for k, rs in found.items() if reader in rs} & mentioned
            self.assertEqual(
                mentioned, parsed,
                f"{reader}: guarded knobs mentioned {sorted(mentioned)} but "
                f"parsed as {sorted(parsed)}: a read inside a default or a "
                f"token the regex no longer fits is being swallowed "
                f"(issue #137)")

    def test_every_read_guarded_knob_is_named_in_its_env_block(self):
        self.assertEqual(
            undocumented_env_knobs(), {},
            "a scanned runner or helper reads a guarded knob its `# Env:` "
            "header block does not name: the knob works but cannot be "
            "discovered (issue #134, guarded since #142)")


class FixtureGuardTests(unittest.TestCase):
    """Negative cases on throwaway trees, so they keep biting as benches land."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.sim = os.path.join(tmp.name, "sim")
        self.harness = os.path.join(self.sim, "harness")
        self.bench = os.path.join(self.sim, "bench-a")
        os.makedirs(self.bench)
        os.makedirs(self.harness)

    def write(self, rel, text):
        path = os.path.join(self.sim, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as fh:
            fh.write(text)
        return path

    def found(self):
        return knob_readers(self.sim, self.harness)

    def test_guarded_knob_nested_singly_in_a_default_is_seen(self):
        self.write("bench-a/run.sh", 'out="${OUT:-${DSIZ_VC}}"\n')
        self.assertEqual(self.found(), {"DSIZ_VC": {"bench-a/run.sh"}})

    def test_bare_name_nested_in_a_default_is_seen(self):
        self.write("bench-a/run.sh", 'out="${OUT:-$DSIZ_VC}"\n')
        self.assertEqual(self.found(), {"DSIZ_VC": {"bench-a/run.sh"}})

    def test_double_nesting_is_seen(self):
        self.write("bench-a/run.sh", 'out="${OUT:-${A:-${DSIZ_VC}}}"\n')
        self.assertEqual(self.found(), {"DSIZ_VC": {"bench-a/run.sh"}})

    def test_nested_and_plain_reads_of_one_knob_are_one_reader(self):
        self.write("bench-a/run.sh",
                   'out="${OUT:-${DSIZ_VC}}"\ncd "$DSIZ_VC"\n')
        self.assertEqual(self.found(), {"DSIZ_VC": {"bench-a/run.sh"}})

    def test_two_knobs_in_one_default_are_both_seen(self):
        self.write("bench-a/run.sh", 'out="${OUT:-${DSIZ_VC}/${DSAN_VC}}"\n')
        self.assertEqual(
            self.found(),
            {"DSIZ_VC": {"bench-a/run.sh"}, "DSAN_VC": {"bench-a/run.sh"}})

    def test_lowercase_names_in_a_default_stay_unmatched(self):
        self.write("bench-a/run.sh", 'out="${out:-$dsiz_vc}"\n')
        self.assertEqual(self.found(), {})

    def test_helper_reading_a_benchs_knob_is_a_collision(self):
        self.write("bench-a/run.sh", 'mkdir -p "${FOO_RESULTS_DIR:-/tmp/fx}"\n')
        self.write("harness/new-helper.sh", 'cd "$FOO_RESULTS_DIR"\n')
        self.assertEqual(
            collisions(self.found()),
            {"FOO_RESULTS_DIR": ["bench-a/run.sh", "harness/new-helper.sh"]})

    def test_same_named_helpers_in_different_directories_collide(self):
        paths = ["harness/a/check.sh", "harness/b/check.sh"]
        for path in paths:
            self.write(path, '# Env: FOO_RESULTS_DIR\ncd "$FOO_RESULTS_DIR"\n')
        self.assertEqual(collisions(self.found()), {"FOO_RESULTS_DIR": paths})

    def test_helper_with_no_guarded_knob_is_not_a_reader(self):
        self.write("bench-a/run.sh", 'mkdir -p "${FOO_RESULTS_DIR:-/tmp/fx}"\n')
        self.write("harness/quiet.sh", 'cd "$SIM_DIR"\n')
        self.assertEqual(self.found(), {"FOO_RESULTS_DIR": {"bench-a/run.sh"}})

    def test_renaming_an_anchored_helper_away_fails_the_anchor(self):
        self.write("bench-a/run.sh", 'echo hi\n')
        helper = self.write("harness/bench-run.sh",
                            'mkdir -p "$BENCH_RESULTS_DIR"\n')
        self.assertIsNone(
            anchored_namespace_violations(self.found()).get("BENCH_RESULTS_DIR"))
        os.rename(helper, os.path.join(self.harness, "moved.sh"))
        self.assertEqual(
            anchored_namespace_violations(self.found()).get("BENCH_RESULTS_DIR"),
            ["harness/moved.sh"])

    def test_knob_on_an_env_continuation_line_is_documented(self):
        self.write(
            "bench-a/run.sh",
            "# Env: FOO_BACKEND (default unset)\n"
            "#                       FOO_RESULTS_DIR  default results/\n"
            "set -euo pipefail\n"
            'mkdir -p "${FOO_RESULTS_DIR:-/tmp/fx}"\n')
        self.assertEqual(undocumented_env_knobs(self.sim, self.harness), {})

    def test_prose_mention_is_not_a_reader(self):
        self.write(
            "bench-a/run.sh",
            "# Delegates to smoke-run.sh; UNITSMOKE_RESULTS_DIR is "
            "documented there.\n"
            "echo hi\n")
        self.assertEqual(knob_readers(self.sim, self.harness), {})
        self.assertEqual(undocumented_env_knobs(self.sim, self.harness), {})

    def test_read_with_no_env_block_fails(self):
        self.write(
            "bench-a/run.sh",
            "set -euo pipefail\n"
            'mkdir -p "${FOO_RESULTS_DIR:-/tmp/fx}"\n')
        self.assertEqual(undocumented_env_knobs(self.sim, self.harness),
                         {"bench-a/run.sh": ["FOO_RESULTS_DIR"]})

    def test_env_block_silent_on_the_read_knob_fails(self):
        self.write(
            "bench-a/run.sh",
            "# Env: FOO_BACKEND (default unset)\n"
            "set -euo pipefail\n"
            'mkdir -p "${FOO_RESULTS_DIR:-/tmp/fx}"\n')
        self.assertEqual(undocumented_env_knobs(self.sim, self.harness),
                         {"bench-a/run.sh": ["FOO_RESULTS_DIR"]})

    def test_knob_named_only_under_a_following_label_fails(self):
        self.write(
            "bench-a/run.sh",
            "# Env: FOO_BACKEND (default unset)\n"
            "# Exit: 0 pass, 3 missing prerequisite\n"
            "# FOO_RESULTS_DIR  default results/\n"
            "set -euo pipefail\n"
            'mkdir -p "${FOO_RESULTS_DIR:-/tmp/fx}"\n')
        self.assertEqual(undocumented_env_knobs(self.sim, self.harness),
                         {"bench-a/run.sh": ["FOO_RESULTS_DIR"]})


if __name__ == "__main__":
    unittest.main()
