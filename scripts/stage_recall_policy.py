#!/usr/bin/env python3
"""Compute token-aware recall tiers for long-running research projects."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STAGE_GRAPH = ROOT / "research-wiki" / "STAGE_GRAPH.md"
SCRIPT_VERSION = "stage_recall_policy.v1"
SCHEMA_VERSION = "1.0"

TIER_NAMES = {
    0: "no_project_recall",
    1: "anchor_scan",
    2: "pointer_lookup",
    3: "targeted_continuity_capsule",
    4: "full_upstream_audit",
}

RECOMMENDED_ACTIONS = {
    0: "proceed_no_project_recall",
    1: "anchor_scan",
    2: "pointer_lookup",
    3: "targeted_continuity_capsule",
    4: "full_upstream_audit_or_pause",
}

CHANGE_TYPE_FLOORS = {
    "unspecified": 0,
    "read_only_explanation": 0,
    "source_summary_no_design": 1,
    "citation_key_only": 1,
    "ordinary_typo_or_formatting": 1,
    "formal_layout_or_structure_repair": 2,
    "formal_wording_no_meaning_change": 2,
    "formal_delivery_generation": 2,
    "source_status_update": 2,
    "source_readiness_upgrade": 3,
    "design_or_method_change": 3,
    "scoped_supersession_protected_source": 4,
}

FILE_CLASS_FLOORS = {
    "bookkeeping": 0,
    "navigation_layer": 1,
    "production_receipt_record": 1,
    "source_readiness_layer": 2,
    "formal_delivery_surface": 2,
    "stage_source_of_record": 3,
    "design_or_method_plan": 3,
    "compliance_or_ethics": 3,
    "unclassified": 0,
}

BOOKKEEPING_PREFIXES = (
    ".agent-runtime/",
    "audit-reports/skill-receipts/",
    "research-wiki/runtime-receipts/",
    "research-wiki/skill-receipts/",
)

TASK_PATTERNS = [
    (4, "task_intent:scoped_supersession", r"\b(replace|supersede|obsolete|ignore|drop)\b.{0,80}\b(old|previous|prior|accepted|source|brief|proposal|protocol|guide|route)\b"),
    (3, "task_intent:skip_upstream_known_deliverable", r"\b(skip|ignore|bypass)\b.{0,80}\b(upstream|source[- ]of[- ]record|stage|previous|prior)\b"),
    (3, "task_intent:high_risk_stage_deliverable", r"\b(write|revise|draft|create|produce|design|formalise|formalize|translate|reword)\b.{0,80}\b(methodology|method plan|analysis plan|concept card|scenario|interview guide|survey|instrument|research question|stakeholder-facing|supervisor-facing|proposal|formal draft|ethics|compliance)\b"),
    (3, "task_intent:high_risk_stage_deliverable", r"\b(methodology|method plan|analysis plan|concept card|scenario|interview guide|survey|instrument|research question|stakeholder-facing|supervisor-facing|proposal|formal draft|ethics|compliance)\b.{0,80}\b(write|revise|draft|create|produce|design|formalise|formalize|translate|reword)\b"),
    (2, "task_intent:formal_layout_repair", r"\b(layout|structure|heading|table|word|docx|format)\b.{0,80}\b(repair|fix|check)\b|\b(repair|fix|check)\b.{0,80}\b(layout|structure|heading|table|word|docx|format)\b"),
    (2, "task_intent:source_status_update", r"\b(source register|source readiness|readiness matrix|claim support)\b.{0,80}\b(update|change|revise|upgrade|mark)\b"),
    (1, "task_intent:source_summary", r"\b(read|summari[sz]e|summary)\b.{0,80}\b(source|paper|article|literature|policy|report)\b"),
]

LOW_COST_FORMAL_EDIT_PATTERNS = [
    r"\bcitation[- ]key\b",
    r"\breference[- ]format(?:ting)?\b",
    r"\bcitation[- ]format(?:ting)?\b",
    r"\btypo\b",
    r"\bpunctuation\b",
]

NO_CONTENT_CHANGE_PATTERNS = [
    r"\bdo not change (?:wording|meaning|content|claims?|argument)\b",
    r"\bno (?:wording|meaning|content|claim|argument) change\b",
    r"\bwithout changing (?:wording|meaning|content|claims?|argument)\b",
    r"不(改|修改|改变).*(措辞|含义|内容|claim|论证|正文)",
    r"不动.*(正文|内容|含义|论证)",
]

EXPLICIT_REFERENCE_PATTERNS = [
    (3, "explicit_reference:source_of_record", r"\b(source[- ]of[- ]record|design lock|accepted output|current source)\b"),
    (2, "explicit_reference:prior_artifact", r"\b(previous|prior|old version|checkpoint|source map|appendix|protocol)\b"),
    (2, "explicit_reference:official_requirement", r"\b(rubric|requirement|ethics|compliance|deadline|word count|author guideline)\b"),
]


@dataclass
class StagePath:
    path: str
    stage_node: str
    stage: str


@dataclass
class PathClassification:
    path: str
    file_class: str
    floor: int
    reason: str
    protected: bool = False
    stage_node: str | None = None


@dataclass
class RecallDecision:
    schema: str
    schema_version: str
    tier: int
    tier_name: str
    floor_reasons: list[str]
    target_files: list[str]
    path_classifications: list[dict]
    change_type: str
    task: str
    inspected_paths: list[str]
    recommended_action: str
    known_limitations: list[str]


def normalize_path(value: str) -> str:
    path = Path(value).expanduser()
    if path.is_absolute():
        try:
            return str(path.resolve().relative_to(ROOT))
        except ValueError:
            return str(path)
    return str(path).replace("\\", "/").lstrip("./")


def split_markdown_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def extract_backtick_paths(text: str) -> list[str]:
    paths: list[str] = []
    seen: set[str] = set()
    for token in re.findall(r"`([^`]+)`", text):
        if "/" not in token and not token.endswith((".md", ".json", ".jsonl", ".docx", ".pdf", ".py", ".txt")):
            continue
        path = normalize_path(token)
        if path not in seen:
            paths.append(path)
            seen.add(path)
    return paths


def parse_stage_graph(stage_graph: Path = DEFAULT_STAGE_GRAPH) -> dict[str, StagePath]:
    if not stage_graph.exists():
        return {}
    text = stage_graph.read_text(encoding="utf-8", errors="replace")
    paths: dict[str, StagePath] = {}
    in_stage_nodes = False
    for line in text.splitlines():
        if line.startswith("## Stage Nodes"):
            in_stage_nodes = True
            continue
        if in_stage_nodes and line.startswith("## "):
            break
        if not in_stage_nodes or not line.startswith("|"):
            continue
        cells = split_markdown_row(line)
        if len(cells) < 4 or cells[0] in {"Stage ID", "---"} or cells[0].startswith("---"):
            continue
        stage_node = cells[0].strip("` ")
        stage = cells[1].strip()
        for path in extract_backtick_paths(cells[2]):
            paths.setdefault(path, StagePath(path=path, stage_node=stage_node, stage=stage))
    return paths


def classify_path(path_text: str, stage_paths: dict[str, StagePath]) -> PathClassification:
    path = normalize_path(path_text)
    if path in stage_paths:
        stage_node = stage_paths[path].stage_node
        if stage_node == "production-receipts":
            file_class = "production_receipt_record"
        elif stage_node == "source-readiness":
            file_class = "source_readiness_layer"
        elif stage_node == "compliance-or-ethics":
            file_class = "compliance_or_ethics"
        elif stage_node == "method-or-analysis-plan":
            file_class = "design_or_method_plan"
        else:
            file_class = "stage_source_of_record"
        return PathClassification(path, file_class, FILE_CLASS_FLOORS[file_class], "stage_graph_exact_path", True, stage_node)
    if any(path.startswith(prefix) for prefix in BOOKKEEPING_PREFIXES):
        return PathClassification(path, "bookkeeping", 0, "bookkeeping_prefix")
    if path in {"research-wiki/TASK_STATE.md", "research-wiki/PRODUCTION_RUN_REGISTER.md", "research-wiki/SESSION_EVENT_LOG.jsonl"}:
        return PathClassification(path, "production_receipt_record", 1, "production_receipt_known_path", True)
    if path.startswith("knowledge-base/") or "SOURCE_READINESS" in path or "SOURCE_REGISTER" in path:
        return PathClassification(path, "source_readiness_layer", 2, "source_readiness_path_cue", True)
    if path.startswith("compliance/") or path.startswith("ethics/") or "PRIVACY" in path:
        return PathClassification(path, "compliance_or_ethics", 3, "compliance_path_cue", True)
    if any(term in path.lower() for term in ["method", "analysis", "instrument", "interview", "concept", "design-lock"]):
        return PathClassification(path, "design_or_method_plan", 3, "method_or_design_path_cue", True)
    if path.endswith((".docx", ".pdf", ".png", ".jpg", ".jpeg")):
        return PathClassification(path, "formal_delivery_surface", 2, "formal_delivery_suffix")
    if "obsidian" in path.lower() or "compiled-wiki" in path:
        return PathClassification(path, "navigation_layer", 1, "navigation_path_cue")
    return PathClassification(path, "unclassified", 0, "no_path_cue")


def pattern_floor(text: str, patterns: list[tuple[int, str, str]]) -> tuple[int, list[str]]:
    floor = 0
    reasons: list[str] = []
    low_cost_no_content_change = any(re.search(pattern, text, flags=re.I) for pattern in LOW_COST_FORMAL_EDIT_PATTERNS) and any(
        re.search(pattern, text, flags=re.I) for pattern in NO_CONTENT_CHANGE_PATTERNS
    )
    for value, reason, pattern in patterns:
        if re.search(pattern, text, flags=re.I):
            if low_cost_no_content_change and reason == "task_intent:high_risk_stage_deliverable":
                continue
            floor = max(floor, value)
            reasons.append(reason)
    return floor, reasons


def decide(
    task: str,
    target_files: list[str] | None = None,
    change_type: str = "unspecified",
    stage_graph: Path = DEFAULT_STAGE_GRAPH,
) -> RecallDecision:
    target_files = target_files or []
    stage_paths = parse_stage_graph(stage_graph)
    classifications = [classify_path(path, stage_paths) for path in target_files]
    floors = [CHANGE_TYPE_FLOORS.get(change_type, 0)]
    reasons = [f"change_type:{change_type}"]
    task_floor, task_reasons = pattern_floor(task, TASK_PATTERNS)
    explicit_floor, explicit_reasons = pattern_floor(task, EXPLICIT_REFERENCE_PATTERNS)
    floors.extend([task_floor, explicit_floor])
    reasons.extend(task_reasons)
    reasons.extend(explicit_reasons)
    for item in classifications:
        floors.append(item.floor)
        reasons.append(f"path:{item.reason}:{item.path}")
    tier = max(floors) if floors else 0
    return RecallDecision(
        schema=SCRIPT_VERSION,
        schema_version=SCHEMA_VERSION,
        tier=tier,
        tier_name=TIER_NAMES[tier],
        floor_reasons=reasons,
        target_files=[item.path for item in classifications],
        path_classifications=[asdict(item) for item in classifications],
        change_type=change_type,
        task=task,
        inspected_paths=[normalize_path(str(stage_graph))] if stage_graph.exists() else [],
        recommended_action=RECOMMENDED_ACTIONS[tier],
        known_limitations=[
            "Task intent is regex-assisted and should be reconciled with project-specific judgement.",
            "Token-Aware Recall controls context budget only; it cannot override source, compliance, citation, document, privacy, or delivery gates.",
        ],
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute token-aware recall tier for a research-agent task.")
    parser.add_argument("--task", required=True)
    parser.add_argument("--change-type", default="unspecified", choices=sorted(CHANGE_TYPE_FLOORS))
    parser.add_argument("--target-file", action="append", default=[])
    parser.add_argument("--stage-graph", default=str(DEFAULT_STAGE_GRAPH))
    args = parser.parse_args()
    decision = decide(args.task, args.target_file, args.change_type, Path(args.stage_graph))
    print(json.dumps(asdict(decision), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
