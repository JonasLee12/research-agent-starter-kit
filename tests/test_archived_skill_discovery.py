from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCHIVED_SKILLS = {
    "active-learning-design-support",
    "ai-agent-design-spec",
    "codesign-output-synthesis",
    "dissertation-figure-spec",
    "dissertation-research-wiki",
    "prototype-evaluation-audit",
    "teacher-adoption-modeling",
    "teaching-knowledge-base-plan",
    "viva-prep",
}


class ArchivedSkillDiscoveryTests(unittest.TestCase):
    def test_archived_skills_are_outside_active_discovery_root(self) -> None:
        active_root = ROOT / ".agents" / "skills"
        archive_root = ROOT / ".agents" / "archived-skills"

        archived_present = {
            skill_md.parent.name for skill_md in archive_root.glob("*/SKILL.md")
        }
        archived_below_active = {
            skill_md.parent.name
            for skill_md in active_root.glob("**/SKILL.md")
            if skill_md.parent.name in ARCHIVED_SKILLS
        }

        self.assertEqual(archived_present, ARCHIVED_SKILLS)
        self.assertEqual(archived_below_active, set())
        self.assertFalse((active_root / "_archived").exists())


if __name__ == "__main__":
    unittest.main()
