"""The committed envelope corpus pins the klt backend provenance shape.

klt 0.8.0 (the pin, scripts/klt.sh) writes ``environment.backend`` at exactly
one site, always as the provenance dict with keys ``requested``/``resolved``/
``source``. Every record writer reads the run's backend out of that field
(`evidence.backend_of` and the summarizers), so a future klt pin bump that
changes the shape is discovered by a reader breaking rather than by a test
failing: a bare-string backend crashes a summarizer mid-record, and a dict
that drops ``resolved`` silently writes "backend unrecorded" / "backend ?"
into a committed record.md for a run that really used another backend --
silently wrong provenance in an append-only evidence tree.

These tests pin the committed ``sim/**/*.envelope.json`` corpus to the shape
the pin writes: every envelope's ``environment.backend`` must be a dict
carrying a non-null ``resolved``. There are no exemptions: error-status
envelopes carry the dict too, and a future envelope that legitimately lacks
the shape should turn this red and earn its exemption with evidence -- that
is the tripwire working. The mutation controls prove the scan fails on the
two shapes a pin bump could produce, and that an empty glob fails rather
than passing vacuously.

Nothing here simulates.
"""

import json
import os
import shutil
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.dirname(os.path.dirname(HERE))


def envelope_names(root):
    """Sorted ``*.envelope.json`` paths under root, relative to root."""
    found = []
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if name.endswith(".envelope.json"):
                found.append(os.path.relpath(os.path.join(dirpath, name), root))
    return sorted(found)


def backend_shape_problem(path):
    """Return a reason string if the envelope's backend is not the pin's shape."""
    with open(path) as fh:
        envelope = json.load(fh)
    backend = (envelope.get("environment") or {}).get("backend")
    if not isinstance(backend, dict):
        return f"environment.backend is {type(backend).__name__}, not the provenance dict"
    if backend.get("resolved") is None:
        return f"environment.backend dict has no non-null 'resolved': {sorted(backend)}"
    return None


def scan_backend_shape(root):
    """Scan every envelope under root; return ``(names, violations)``.

    ``names`` is the sorted list of envelope paths found (possibly empty);
    ``violations`` maps an envelope path to the reason its backend is not the
    pinned shape.
    """
    names = envelope_names(root)
    violations = {}
    for rel in names:
        reason = backend_shape_problem(os.path.join(root, rel))
        if reason is not None:
            violations[rel] = reason
    return names, violations


class CommittedEnvelopeCorpus(unittest.TestCase):
    """``sim/**/*.envelope.json`` is append-only evidence of what ran; pin its shape."""

    def test_every_committed_envelope_carries_backend_provenance(self):
        names, violations = scan_backend_shape(SIM)
        self.assertTrue(
            names,
            "no *.envelope.json under sim/: the corpus pin would pass vacuously",
        )
        for rel in names:
            with self.subTest(envelope=rel):
                self.assertIsNone(violations.get(rel), violations.get(rel))


class MutationControls(unittest.TestCase):
    """The pin is not a tripwire unless it fails on the shapes a bump could write."""

    def _root_with_mutated_envelope(self, backend_value):
        """Copy one committed envelope into a temp tree with its backend replaced."""
        names, _ = scan_backend_shape(SIM)
        self.assertTrue(names, "need one committed envelope to mutate")
        with open(os.path.join(SIM, names[0])) as fh:
            envelope = json.load(fh)
        envelope.setdefault("environment", {})["backend"] = backend_value
        root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, root, True)
        with open(os.path.join(root, "mutated.envelope.json"), "w") as fh:
            json.dump(envelope, fh)
        return root

    def test_bare_string_backend_fails_the_scan(self):
        names, violations = scan_backend_shape(
            self._root_with_mutated_envelope("batch"))
        self.assertEqual(names, ["mutated.envelope.json"])
        self.assertEqual(sorted(violations), ["mutated.envelope.json"])
        self.assertIn("not the provenance dict", violations["mutated.envelope.json"])

    def test_backend_dict_without_resolved_fails_the_scan(self):
        names, violations = scan_backend_shape(
            self._root_with_mutated_envelope({"name": "batch"}))
        self.assertEqual(names, ["mutated.envelope.json"])
        self.assertEqual(sorted(violations), ["mutated.envelope.json"])
        self.assertIn("resolved", violations["mutated.envelope.json"])

    def test_tree_without_envelopes_fails_the_scan(self):
        root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, root, True)
        names, violations = scan_backend_shape(root)
        self.assertEqual((names, violations), ([], {}))
        with self.assertRaises(AssertionError):
            # The corpus test's guard: an empty glob must fail the pin, not
            # pass it.
            self.assertTrue(
                names,
                "no *.envelope.json under sim/: the corpus pin would pass vacuously",
            )
