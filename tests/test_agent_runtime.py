#!/usr/bin/env python3
"""Regression tests for deterministic research-agent runtime routing."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from agent_runtime import classify  # noqa: E402


class AgentRuntimeRoutingTests(unittest.TestCase):
    def test_research_star_skill_migration_routes_as_maintenance_only(self) -> None:
        route = classify("Audit Production Window context refresh after research-* skill migration", "Maintenance")

        self.assertEqual(route.mode, "Maintenance Mode")
        self.assertEqual(route.task_types, ["system_maintenance"])
        self.assertNotIn("literature_search", route.task_types)

    def test_english_literature_search_still_routes_as_research(self) -> None:
        route = classify("search for recent literature on a research topic", "Production")

        self.assertEqual(route.mode, "Research Mode")
        self.assertIn("literature_search", route.task_types)

    def test_chinese_literature_search_still_routes_as_research(self) -> None:
        route = classify("帮我检索最新文献", "Production")

        self.assertEqual(route.mode, "Research Mode")
        self.assertIn("literature_search", route.task_types)

    def test_maintenance_research_conflict_keeps_maintenance_as_lead_route(self) -> None:
        route = classify("Audit the literature search routing for Production Window", "Maintenance")

        self.assertEqual(route.mode, "Maintenance Mode")
        self.assertEqual(route.task_types[0], "system_maintenance")
        self.assertIn("literature_search", route.task_types)

    def test_automation_prompt_update_routes_as_maintenance_only(self) -> None:
        route = classify("Update existing weekly literature automation prompt to staged gap watch", "Maintenance")

        self.assertEqual(route.mode, "Maintenance Mode")
        self.assertEqual(route.task_types, ["system_maintenance"])
        self.assertNotIn("literature_search", route.task_types)

    def test_generic_skill_word_does_not_force_maintenance(self) -> None:
        route = classify("Find literature on cognitive skill development", "Maintenance")

        self.assertEqual(route.mode, "Research Mode")
        self.assertIn("literature_search", route.task_types)
        self.assertNotIn("system_maintenance", route.task_types)


if __name__ == "__main__":
    unittest.main()
