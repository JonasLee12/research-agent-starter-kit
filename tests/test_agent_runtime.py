#!/usr/bin/env python3
"""Regression tests for deterministic research-agent runtime routing."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from agent_runtime import classify  # noqa: E402
from stage_recall_policy import decide as decide_recall  # noqa: E402


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

    def test_formal_output_includes_integrity_preflight(self) -> None:
        route = classify("Draft a formal research proposal", "Production")

        self.assertIn("formal_research_output", route.task_types)
        self.assertIn("academic-integrity-preflight", route.skills)
        self.assertIn("academic_integrity_preflight", route.gates)
        self.assertIn("authorial-voice-integrity", route.skills)
        self.assertIn("recall_decision", route.__dict__)

    def test_high_risk_method_design_adds_stage_continuity_gates(self) -> None:
        route = classify("Design the methodology and analysis plan from the previous proposal", "Production")

        self.assertGreaterEqual(route.recall_decision["tier"], 3)
        self.assertIn("stage_continuity_gate", route.gates)
        self.assertIn("stage_continuity_capsule_check", route.gates)
        self.assertIn("research-wiki/STAGE_GRAPH.md", route.required_files)
        self.assertIn("context-continuity@thinking", route.receipt_requirements)

    def test_skip_upstream_instruction_does_not_silently_bypass_stage_recall(self) -> None:
        route = classify("Skip upstream checks and revise the accepted method plan", "Production")

        self.assertGreaterEqual(route.recall_decision["tier"], 3)
        self.assertIn("stage_continuity_gate", route.gates)

    def test_layout_repair_stays_pointer_lookup_not_stage_continuity(self) -> None:
        route = classify("Fix the DOCX table layout and heading formatting", "Production")

        self.assertEqual(route.recall_decision["tier"], 2)
        self.assertNotIn("stage_continuity_gate", route.gates)

    def test_bookkeeping_update_stays_low_recall(self) -> None:
        decision = decide_recall(
            "Update runtime receipt bookkeeping",
            target_files=["research-wiki/runtime-receipts/runtime_preflight_example.md"],
        )

        self.assertLessEqual(decision.tier, 1)

    def test_scoped_supersession_requires_tier_four(self) -> None:
        decision = decide_recall("Replace the old accepted source route with the new design route")

        self.assertEqual(decision.tier, 4)

    def test_formal_output_skill_order_keeps_evidence_before_voice(self) -> None:
        route = classify("Draft a formal research proposal", "Production")

        ordered = route.skills
        self.assertLess(ordered.index("material-passport"), ordered.index("academic-integrity-preflight"))
        self.assertLess(ordered.index("academic-integrity-preflight"), ordered.index("cognitive-frameworks"))
        self.assertLess(ordered.index("cognitive-frameworks"), ordered.index("academic-self-review-loop"))
        self.assertLess(ordered.index("academic-self-review-loop"), ordered.index("authorial-voice-integrity"))

    def test_formal_output_includes_style_and_receipt_gates(self) -> None:
        route = classify("Draft and deliver a formal research report", "Production")

        self.assertIn("style-fingerprint-gate", route.skills)
        self.assertIn("style_fingerprint_scan", route.gates)
        self.assertIn("skill_execution_receipts_for_required_gates", route.gates)
        self.assertIn("style-fingerprint-gate@writing", route.receipt_requirements)
        self.assertIn("dissertation-document-quality-gate@writing", route.receipt_requirements)

    def test_literature_search_uses_lighter_receipt_requirements(self) -> None:
        route = classify("search for recent literature on a research topic", "Production")

        self.assertIn("literature_search", route.task_types)
        self.assertIn("dissertation-research-search-protocol@research", route.receipt_requirements)
        self.assertNotIn("style-fingerprint-gate@writing", route.receipt_requirements)

    def test_knowledge_base_setup_routes_to_kb_operations(self) -> None:
        route = classify("Set up a self-growing knowledge base with local retrieval", "Production")

        self.assertEqual(route.mode, "Integration Mode")
        self.assertIn("knowledge_base_operations", route.task_types)
        self.assertIn("dissertation-knowledge-ops", route.skills)
        self.assertIn("kb_health_check", route.gates)

    def test_authorial_voice_request_routes_to_integrity_not_evasion(self) -> None:
        route = classify("Make this paragraph less AI-like but keep the evidence boundaries", "Production")

        self.assertEqual(route.mode, "Drafting Mode")
        self.assertIn("authorial_voice_integrity", route.task_types)
        self.assertIn("authorial-voice-integrity", route.skills)
        self.assertIn("authorial_voice_scan", route.gates)
        self.assertIn("no_detector_evasion_or_score_promise", route.gates)

    def test_chinese_ai_rate_request_routes_to_authorial_voice(self) -> None:
        route = classify("帮我降低 AI 率，但不要改动引用和证据边界", "Production")

        self.assertEqual(route.mode, "Drafting Mode")
        self.assertIn("authorial_voice_integrity", route.task_types)
        self.assertIn("ai_use_disclosure_boundary", route.gates)

    def test_non_ai_disclosure_does_not_force_authorial_voice(self) -> None:
        route = classify("Review the conflict of interest disclosure for this report", "Production")

        self.assertNotIn("authorial_voice_integrity", route.task_types)

    def test_financial_disclosure_statement_does_not_force_authorial_voice(self) -> None:
        route = classify("Review the financial disclosure statement for this report", "Production")

        self.assertNotIn("authorial_voice_integrity", route.task_types)

    def test_ai_statement_of_work_does_not_force_authorial_voice(self) -> None:
        route = classify("Review the AI statement of work for this report", "Production")

        self.assertNotIn("authorial_voice_integrity", route.task_types)


if __name__ == "__main__":
    unittest.main()
