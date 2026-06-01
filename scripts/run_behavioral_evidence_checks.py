#!/usr/bin/env python3
"""Behavioural evidence checks over real project outputs.

This does not call an LLM. It checks whether recent workflow evidence matches
the behaviours the agent claims to perform.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from agent_runtime import classify


ROOT = Path(__file__).resolve().parents[1]
EVENT_LOG = ROOT / "research-wiki" / "SESSION_EVENT_LOG.jsonl"
TASK_STATE = ROOT / "research-wiki" / "TASK_STATE.md"
OUT_DIR = ROOT / "research-wiki" / "skill-evals"
RUNTIME_DIR = ROOT / "research-wiki" / "runtime-receipts"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def load_events() -> list[dict]:
    events = []
    for line in read_text(EVENT_LOG).splitlines():
        if line.strip():
            events.append(json.loads(line))
    return events


def check() -> tuple[list[str], list[str]]:
    events = load_events()
    task_state = read_text(TASK_STATE)
    public_template_mode = "[Your current project phase]" in task_state
    runtime_text = read_text(ROOT / "scripts" / "agent_runtime.py")
    static_text = "\n".join(
        read_text(ROOT / path)
        for path in [
            "AGENTS.md",
            "PROJECT_AGENT_PREFERENCES.md",
            "research-wiki/HARD_RUNTIME_ENFORCEMENT.md",
            "research-wiki/EXTERNAL_RESEARCH_CONNECTOR_SPEC.md",
            "research-wiki/ZOTERO_AND_CITATION_WORKFLOW_SPEC.md",
            "research-wiki/DOCUMENT_PIPELINE.md",
            "research-wiki/WRITING_QUALITY_RUBRIC.md",
            "knowledge-base/self-growing/README.md",
            "knowledge-base/self-growing/growth-queue.md",
            "knowledge-base/self-growing/compiled-wiki/INDEX.md",
            "knowledge-base/SOURCE_READINESS_MATRIX.md",
            "docs/EXTERNAL_REVIEW_OPTIONS.md",
            "templates/prompts/EXTERNAL_REVIEWER_PROMPT.md",
            ".agents/skills/academic-self-review-loop/SKILL.md",
            ".agents/skills/academic-integrity-preflight/SKILL.md",
        ]
    )
    passed = []
    failed = []
    event_types = {event.get("event_type") for event in events}
    if {"gate_completed"} <= event_types:
        passed.append("Session log contains a runtime gate completion event.")
    elif public_template_mode and {"session_start", "gate_completed", "session_end"} <= set(
        token for token in ["session_start", "gate_completed", "session_end"] if token in runtime_text
    ):
        # Clean starter-kit copies intentionally ship without generated runtime
        # receipts. In that state, confirm the runtime can write the required
        # event types rather than requiring a fake event log.
        passed.append("Starter template mode: runtime tool contains session start, gate completion, and session end event writers.")
    else:
        failed.append("Session log lacks runtime gate completion evidence.")
    if "source-readiness" in static_text.lower() or "SOURCE_READINESS_MATRIX.md" in static_text:
        passed.append("Project files record source-readiness boundary.")
    else:
        failed.append("Project files do not record source-readiness boundary.")
    if (ROOT / "scripts" / "agent_runtime.py").exists() and any(RUNTIME_DIR.glob("runtime_preflight_*.json")):
        passed.append("Deterministic runtime preflight tool and receipt exist.")
    elif public_template_mode and (ROOT / "scripts" / "agent_runtime.py").exists() and RUNTIME_DIR.exists():
        passed.append("Starter template mode: deterministic runtime preflight tool and receipt directory exist.")
    else:
        failed.append("Runtime preflight tool or receipt is missing.")
    migration_route = classify("Audit Production Window context refresh after research-* skill migration", "Maintenance")
    if (
        migration_route.mode == "Maintenance Mode"
        and "system_maintenance" in migration_route.task_types
        and "literature_search" not in migration_route.task_types
    ):
        passed.append("Runtime routes research-* skill migration audits as Maintenance, not literature search.")
    else:
        failed.append("Runtime misroutes research-* skill migration audits; expected Maintenance-only system_maintenance.")
    english_search_route = classify("search for recent literature on a research topic", "Production")
    if english_search_route.mode == "Research Mode" and "literature_search" in english_search_route.task_types:
        passed.append("Runtime still routes an English literature-search prompt as Research after word-boundary fixes.")
    else:
        failed.append("Runtime no longer routes an English literature-search prompt as Research.")
    automation_update_route = classify("Update existing weekly literature automation prompt to staged gap watch", "Maintenance")
    if (
        automation_update_route.mode == "Maintenance Mode"
        and automation_update_route.task_types == ["system_maintenance"]
    ):
        passed.append("Runtime routes literature automation prompt updates as Maintenance-only work.")
    else:
        failed.append("Runtime misroutes literature automation prompt updates; expected Maintenance-only system_maintenance.")
    if "academic_database_connector.py" in static_text and "metadata" in static_text.lower():
        passed.append("Project files record academic database connector status and subscription boundary.")
    else:
        failed.append("Project files do not record database connector subscription boundary.")
    if "citation_claim_audit.py" in static_text and (
        "verification queue" in static_text or "claim-support audit queue" in static_text
    ):
        passed.append("Project files record citation claim-support audit boundary.")
    else:
        failed.append("Project files do not record citation claim-support audit boundary.")
    if "academic-self-review-loop" in static_text and "WRITING_QUALITY_RUBRIC.md" in static_text:
        passed.append("Project files record self-review loop and writing-quality rubric integration.")
    else:
        failed.append("Project files do not record self-review loop and writing-quality rubric integration.")
    checkpoint_terms = {"THINKING_CHECKPOINT", "WRITING_CHECKPOINT", "DELIVERY_CHECKPOINT"}
    present_checkpoint_terms = {term for term in checkpoint_terms if term in static_text}
    if checkpoint_terms <= present_checkpoint_terms:
        passed.append("Project files record three-stage document checkpoint workflow.")
    else:
        failed.append("Project files do not record three-stage document checkpoint workflow.")
    if "academic-integrity-preflight" in static_text and (ROOT / "scripts" / "academic_integrity_preflight.py").exists():
        passed.append("Project files include academic-integrity preflight skill and local checker.")
    else:
        failed.append("Project files do not include academic-integrity preflight skill and local checker.")
    if "self-growing" in static_text and "growth-queue.md" in static_text and (ROOT / "scripts" / "kb_health_check.py").exists():
        passed.append("Project files include self-growing KB structure and health-check script.")
    else:
        failed.append("Project files do not include self-growing KB structure and health-check script.")
    if (
        (ROOT / "scripts" / "build_external_review_bundle.py").exists()
        and (ROOT / "templates" / "prompts" / "EXTERNAL_REVIEWER_PROMPT.md").exists()
        and "advisory" in static_text.lower()
        and "Claude Code" in static_text
    ):
        passed.append("Project files include vendor-neutral external-review bundle workflow with advisory boundary.")
    else:
        failed.append("Project files do not record a vendor-neutral external-review fallback workflow.")
    kb_route = classify("Set up a self-growing knowledge base with local retrieval", "Production")
    if "knowledge_base_operations" in kb_route.task_types and "kb_health_check" in kb_route.gates:
        passed.append("Runtime routes self-growing knowledge-base setup to KB operations with health-check gate.")
    else:
        failed.append("Runtime does not route self-growing knowledge-base setup to KB operations.")
    return passed, failed


def main() -> int:
    parser = argparse.ArgumentParser(description="Run behavioural evidence checks.")
    parser.add_argument("--output-dir", default=str(OUT_DIR))
    args = parser.parse_args()
    out_dir = Path(args.output_dir)
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    passed, failed = check()
    failed_lines = [f"- {item}" for item in failed] if failed else ["- None"]
    report = [
        "# Behavioural Evidence Check",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Passed",
        "",
        *(f"- {item}" for item in passed),
        "",
        "## Failed",
        "",
        *failed_lines,
        "",
        "## Boundary",
        "",
        "This checks real project evidence, not model cognition. It complements, but does not replace, human review.",
    ]
    path = out_dir / f"Behavioural_Evidence_Check_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.md"
    path.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Report: {path}")
    print(f"Passed: {len(passed)}")
    print(f"Failed: {len(failed)}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
