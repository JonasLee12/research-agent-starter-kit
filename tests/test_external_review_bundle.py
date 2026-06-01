#!/usr/bin/env python3
"""Tests for the local external-review bundle builder."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_external_review_bundle import build_bundle  # noqa: E402


class ExternalReviewBundleTests(unittest.TestCase):
    def test_clean_artifact_generates_complete_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            artifact = tmp_path / "clean_argument.md"
            artifact.write_text("This draft makes one claim and asks for a reviewer to test the logic.", encoding="utf-8")

            status, bundle, findings = build_bundle(
                target=artifact,
                output_dir=tmp_path / "bundles",
                review_question="Review the argument quality.",
                max_chars=1000,
            )

            self.assertEqual(status, "PASS")
            self.assertEqual(findings, [])
            self.assertTrue((bundle / "artifact.md").exists())
            self.assertTrue((bundle / "EXTERNAL_REVIEW_PROMPT.md").exists())
            self.assertTrue((bundle / "privacy_scan.md").exists())
            manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["source_label"], "outside-repo:clean_argument.md")
            self.assertNotIn(str(tmp_path), json.dumps(manifest))

    def test_sensitive_artifact_blocks_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            artifact = tmp_path / "draft.md"
            artifact.write_text("This participant record includes consent language.", encoding="utf-8")

            status, report, findings = build_bundle(
                target=artifact,
                output_dir=tmp_path / "bundles",
                review_question="Review this.",
                max_chars=1000,
            )

            self.assertEqual(status, "BLOCKED")
            self.assertTrue(report.exists())
            self.assertTrue(findings)
            self.assertFalse((report.parent / "artifact.md").exists())

    def test_prompt_keeps_advisory_and_no_invention_boundaries(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            artifact = tmp_path / "plain.md"
            artifact.write_text("A short formal draft.", encoding="utf-8")

            status, bundle, _ = build_bundle(
                target=artifact,
                output_dir=tmp_path / "bundles",
                review_question="Review this.",
                max_chars=1000,
            )

            self.assertEqual(status, "PASS")
            prompt = (bundle / "EXTERNAL_REVIEW_PROMPT.md").read_text(encoding="utf-8")
            self.assertIn("advisory feedback", prompt)
            self.assertIn("Do not invent citations", prompt)
            self.assertIn("source support", prompt)
            self.assertIn("Questions To Verify Locally", prompt)


if __name__ == "__main__":
    unittest.main()
