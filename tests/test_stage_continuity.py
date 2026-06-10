#!/usr/bin/env python3
"""Tests for Stage Continuity helper scripts."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from stage_continuity_capsule_check import check  # noqa: E402
from stage_recall_policy import decide  # noqa: E402


class StageContinuityTests(unittest.TestCase):
    def test_high_risk_deliverable_reaches_targeted_capsule(self) -> None:
        decision = decide("Create a stakeholder-facing decision memo from the previous project brief")

        self.assertGreaterEqual(decision.tier, 3)
        self.assertEqual(decision.recommended_action, "targeted_continuity_capsule")

    def test_source_summary_without_design_is_light_recall(self) -> None:
        decision = decide("Summarise this article without changing the method plan")

        self.assertLessEqual(decision.tier, 1)

    def test_capsule_checker_passes_complete_capsule(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "checkpoint.md"
            target.write_text(
                """
Stage Continuity Capsule:
- Current task/stage: method planning
- Trigger: method plan from previous brief
- Stage graph nodes used: `proposal-or-brief`
- Source-of-record files checked: `RESEARCH_PROJECT_BRIEF_TEMPLATE.md`; `research-wiki/TASK_STATE.md`
- Inherited decisions: `research-wiki/TASK_STATE.md` records current task state
- Later files that may supersede earlier ones: none
- Supersession needs confirmation: none
- Open confirmations / hard stops: requirement source remains `TO CONFIRM`
- What may change: planning language
- What must not change without confirmation: project scope and requirement status
- Next action boundary: prepare planning note, not formal delivery
""",
                encoding="utf-8",
            )

            status, issues, rows = check(target, "methodology-or-method-plan", False)

        self.assertEqual(status, "PASS")
        self.assertEqual(issues, [])
        self.assertTrue(rows)

    def test_capsule_checker_blocks_missing_source_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "checkpoint.md"
            target.write_text(
                """
Stage Continuity Capsule:
- Current task/stage: method planning
- Trigger: method plan from previous brief
- Inherited decisions: `proposal-or-brief`
- Open confirmations / hard stops: none
- What may change: wording
- What must not change without confirmation: scope
- Next action boundary: planning only
""",
                encoding="utf-8",
            )

            status, issues, _ = check(target, "methodology-or-method-plan", False)

        self.assertEqual(status, "BLOCK")
        self.assertTrue(any("source-of-record" in issue.lower() for issue in issues))


if __name__ == "__main__":
    unittest.main()
