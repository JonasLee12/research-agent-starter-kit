#!/usr/bin/env python3
"""Deterministic runtime guard for research-agent tasks.

This is a local enforcement wrapper. It cannot force a chat model to obey rules
unless the workflow calls it, but it can make required routing, gates, and
missing evidence machine-checkable.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVENT_LOG = ROOT / "research-wiki" / "SESSION_EVENT_LOG.jsonl"
OUT_DIR = ROOT / "research-wiki" / "runtime-receipts"


BASE_FILES = [
    "AGENTS.md",
    "PROJECT_AGENT_PREFERENCES.md",
    "PROJECT_TYPE_PROFILES.md",
    "RESEARCH_PROJECT_BRIEF_TEMPLATE.md",
    "DISSERTATION_BRIEF_TEMPLATE.md",
    "research-wiki/TASK_STATE.md",
    "research-wiki/WINDOW_WORKFLOW_PROMPTS.md",
]

TASK_RULES: list[dict] = [
    {
        "name": "formal_research_output",
        "patterns": [
            r"\bproposal\b",
            r"manuscript",
            r"article",
            r"grant",
            r"report",
            r"protocol",
            r"正式文档",
            r"Word",
            r"draft",
            r"supervisor",
            r"PI",
            r"client",
            r"reviewer",
            r"导师",
        ],
        "mode": "Drafting Mode",
        "skills": [
            "agent-orchestration",
            "dissertation-source-first-gate",
            "research-project-adapter",
            "cognitive-frameworks",
            "dissertation-argument-spine",
            "dissertation-research-review",
            "academic-self-review-loop",
            "uk-academic-writing-style",
            "style-memory-and-revision-gate",
            "dissertation-document-quality-gate",
            "context-continuity",
        ],
        "gates": [
            "source_first_gate",
            "requirement_or_rubric_evidence_gate_when_relevant",
            "cognitive_protocol_check",
            "academic_self_review_loop",
            "writing_quality_rubric",
            "thinking_checkpoint",
            "writing_checkpoint",
            "delivery_checkpoint_when_delivering_docx",
            "project_delivery_review_gate",
            "citation_consistency_check",
            "claim_support_audit_when_citation_heavy",
            "document_quality_gate",
            "task_state_update",
        ],
        "required_files": [
            "knowledge-base/SOURCE_READINESS_MATRIX.md",
            "compliance/PROJECT_COMPLIANCE_TRACKER.md",
            "quality-gates/PROJECT_DELIVERY_REVIEW_GATE.md",
            "research-wiki/DOCUMENT_PIPELINE.md",
            "research-wiki/WRITING_QUALITY_RUBRIC.md",
            ".agents/skills/cognitive-frameworks/SKILL.md",
            ".agents/skills/academic-self-review-loop/SKILL.md",
            "scripts/cognitive_protocol_check.py",
        ],
    },
    {
        "name": "literature_search",
        "patterns": [r"literature", r"文献", r"database", r"数据库", r"\bsearch\b", r"检索"],
        "mode": "Research Mode",
        "skills": [
            "agent-orchestration",
            "research-project-adapter",
            "dissertation-research-search-protocol",
            "dissertation-learning-loop",
            "dissertation-literature-review",
            "cognitive-frameworks",
            "dissertation-citation-audit",
            "context-continuity",
        ],
        "gates": [
            "research_search_protocol",
            "metadata_only_boundary",
            "source_readiness_update",
            "cognitive_protocol_when_synthesising",
            "learning_loop_update",
        ],
        "required_files": [
            "research-wiki/EXTERNAL_RESEARCH_CONNECTOR_SPEC.md",
            "knowledge-base/SOURCE_REGISTER.md",
            "knowledge-base/SOURCE_READINESS_MATRIX.md",
        ],
    },
    {
        "name": "citation_claim_support",
        "patterns": [r"citation", r"引用", r"claim", r"支持", r"reference", r"参考文献"],
        "mode": "Review Mode",
        "skills": [
            "agent-orchestration",
            "dissertation-citation-audit",
            "dissertation-source-first-gate",
            "context-continuity",
        ],
        "gates": [
            "citation_consistency_check",
            "claim_support_audit",
            "source_readiness_boundary",
        ],
        "required_files": [
            "knowledge-base/SOURCE_READINESS_MATRIX.md",
            "knowledge-base/SOURCE_REGISTER.md",
            "research-wiki/ZOTERO_AND_CITATION_WORKFLOW_SPEC.md",
        ],
    },
    {
        "name": "requirements_or_rubric",
        "patterns": [
            r"75\+",
            r"(?:assessment|marking|grading|grade|school|university|module|journal|funder|grant|client|submission)\s+rubric",
            r"rubric\s+(?:criteria|band|grade|mark|requirement|evidence|source)",
            r"评分",
            r"marking",
            r"Canvas",
            r"deadline",
            r"word count",
            r"journal",
            r"funder",
            r"grant rule",
            r"client requirement",
            r"submission rule",
            r"author guideline",
        ],
        "mode": "Review Mode",
        "skills": [
            "agent-orchestration",
            "research-project-adapter",
            "dissertation-source-first-gate",
            "dissertation-research-search-protocol",
            "dissertation-research-review",
            "dissertation-document-quality-gate",
        ],
        "gates": [
            "requirement_evidence_gate",
            "source_level_label",
            "no_official_wording_or_requirement_overclaim",
        ],
        "required_files": [
            "compliance/PROJECT_COMPLIANCE_TRACKER.md",
            "quality-gates/PROJECT_DELIVERY_REVIEW_GATE.md",
            "university-guidance/RUBRIC_EVIDENCE_GATE.md",
            "university-guidance/RUBRIC_OR_MARKING_CRITERIA_TEMPLATE.md",
            "university-guidance/MODULE_REQUIREMENTS_TEMPLATE.md",
        ],
    },
    {
        "name": "system_maintenance",
        "patterns": [
            r"agent",
            r"系统",
            r"bug",
            r"维护",
            r"runtime",
            r"routing",
            r"enforcement",
            r"hard",
            r"starter kit",
            r"template",
            r"generalise",
            r"generalize",
            r"adapt",
            r"profile",
            r"github",
            r"workflow",
            r"rule",
        ],
        "mode": "Maintenance Mode",
        "skills": [
            "agent-orchestration",
            "research-project-adapter",
            "dissertation-agent-self-debug",
            "dissertation-agent-architecture-audit",
            "dissertation-workspace-surface-audit",
            "context-continuity",
        ],
        "gates": [
            "architecture_audit",
            "tool_state_check",
            "task_state_update",
            "session_event_log",
        ],
        "required_files": [
            "research-wiki/PRODUCTION_RUN_REGISTER.md",
            "research-wiki/PRODUCTION_RECEIPT_VALIDATION.md",
            "research-wiki/SESSION_EVENT_LOG.jsonl",
        ],
    },
]


@dataclass
class RuntimeRoute:
    run_id: str
    timestamp: str
    window: str
    task: str
    mode: str
    task_types: list[str]
    skills: list[str]
    gates: list[str]
    required_files: list[str]
    missing_files: list[str]
    warnings: list[str]
    status: str


def slugify(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", text.strip().lower()).strip("-")
    return slug[:48] or "task"


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for item in items:
        if item not in seen:
            output.append(item)
            seen.add(item)
    return output


def classify(task: str, window: str) -> RuntimeRoute:
    matched = []
    for rule in TASK_RULES:
        if any(re.search(pattern, task, flags=re.I) for pattern in rule["patterns"]):
            matched.append(rule)
    if not matched:
        matched = [TASK_RULES[-1] if window.lower() == "maintenance" else TASK_RULES[0]]

    maintenance_hint = bool(
        re.search(r"starter kit|template|generalise|generalize|adapt|profile|github|system|maintenance|workflow|rule", task, flags=re.I)
    )
    mode = (
        "Maintenance Mode"
        if window.lower() == "maintenance" and (maintenance_hint or any(r["name"] == "system_maintenance" for r in matched))
        else matched[0]["mode"]
    )
    task_types = [rule["name"] for rule in matched]
    skills = unique([skill for rule in matched for skill in rule["skills"]])
    gates = unique([gate for rule in matched for gate in rule["gates"]])
    required_files = unique(BASE_FILES + [path for rule in matched for path in rule["required_files"]])
    missing_files = [path for path in required_files if not (ROOT / path).exists()]
    warnings = []

    if window.lower() == "maintenance" and any(rule["mode"] == "Drafting Mode" for rule in matched) and not maintenance_hint:
        warnings.append("Task looks like Production drafting but window is Maintenance; confirm window role before drafting.")
    if "requirements_or_rubric" in task_types and "quality-gates/PROJECT_DELIVERY_REVIEW_GATE.md" not in required_files:
        warnings.append("Requirement/rubric task lacks project delivery gate.")
    if "formal_research_output" in task_types and "project_delivery_review_gate" not in gates:
        warnings.append("Formal output lacks project delivery review gate.")
    if "formal_research_output" in task_types and "academic-self-review-loop" not in skills:
        warnings.append("Formal output lacks academic self-review loop.")
    if "formal_research_output" in task_types and not {
        "thinking_checkpoint",
        "writing_checkpoint",
        "delivery_checkpoint_when_delivering_docx",
    }.issubset(set(gates)):
        warnings.append("Formal output lacks staged checkpoint gates.")

    status = "PASS" if not missing_files and not any("lacks" in warning for warning in warnings) else "BLOCKED"
    timestamp = datetime.now().isoformat(timespec="seconds")
    return RuntimeRoute(
        run_id=f"{datetime.now().strftime('%Y-%m-%d')}-{slugify(task)}",
        timestamp=timestamp,
        window=window,
        task=task,
        mode=mode,
        task_types=task_types,
        skills=skills,
        gates=gates,
        required_files=required_files,
        missing_files=missing_files,
        warnings=warnings,
        status=status,
    )


def append_event(route: RuntimeRoute, event_type: str, status: str, evidence: str, risk: str = "low") -> None:
    EVENT_LOG.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "timestamp": route.timestamp,
        "run_id": route.run_id,
        "window": route.window,
        "event_type": event_type,
        "status": status,
        "skill": "agent-runtime-enforcement",
        "file": "scripts/agent_runtime.py",
        "evidence": evidence,
        "risk": risk,
    }
    with EVENT_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def markdown(route: RuntimeRoute) -> str:
    lines = [
        "# Agent Runtime Preflight",
        "",
        f"Generated: {route.timestamp}",
        f"Run ID: `{route.run_id}`",
        f"Window: `{route.window}`",
        f"Status: `{route.status}`",
        "",
        "## Task",
        "",
        route.task,
        "",
        "## Deterministic Routing",
        "",
        f"- Mode: {route.mode}",
        f"- Task types: {', '.join(route.task_types)}",
        f"- Skills: {', '.join(route.skills)}",
        f"- Gates: {', '.join(route.gates)}",
        "",
        "## Required Files",
        "",
    ]
    lines.extend(f"- `{path}`" for path in route.required_files)
    lines.extend(["", "## Missing Files", ""])
    lines.extend(f"- `{path}`" for path in route.missing_files) if route.missing_files else lines.append("- None")
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {warning}" for warning in route.warnings) if route.warnings else lines.append("- None")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a deterministic local preflight. It hard-checks routing, required gates, and required files, but it does not perform the research task itself.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_receipts(route: RuntimeRoute) -> tuple[Path, Path]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    json_path = OUT_DIR / f"runtime_preflight_{stamp}_{slugify(route.task)}.json"
    md_path = OUT_DIR / f"runtime_preflight_{stamp}_{slugify(route.task)}.md"
    json_path.write_text(json.dumps(asdict(route), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(markdown(route), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic research-agent routing preflight.")
    parser.add_argument("task", help="User task or short task description.")
    parser.add_argument("--window", choices=["Production", "Maintenance"], default="Maintenance")
    parser.add_argument("--write", action="store_true", help="Write JSON/Markdown receipts and append a session event.")
    parser.add_argument("--strict", action="store_true", help="Return non-zero when status is BLOCKED.")
    args = parser.parse_args()

    route = classify(args.task, args.window)
    print(json.dumps(asdict(route), ensure_ascii=False, indent=2))
    if args.write:
        json_path, md_path = write_receipts(route)
        append_event(
            route,
            "session_start",
            "completed" if route.status == "PASS" else "blocked",
            "Runtime preflight started a routed task session.",
            "low" if route.status == "PASS" else "medium",
        )
        append_event(
            route,
            "gate_completed",
            "completed" if route.status == "PASS" else "failed",
            f"Runtime preflight wrote {json_path.relative_to(ROOT)} and {md_path.relative_to(ROOT)}.",
            "low" if route.status == "PASS" else "medium",
        )
        append_event(
            route,
            "session_end",
            "completed" if route.status == "PASS" else "blocked",
            "Runtime preflight completed local routing and required-file checks.",
            "low" if route.status == "PASS" else "medium",
        )
        print(f"JSON receipt: {json_path}")
        print(f"Markdown receipt: {md_path}")
    return 1 if args.strict and route.status != "PASS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
