#!/usr/bin/env python3
"""Check Stage Continuity Capsule structure and source-path evidence."""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "audit-reports" / "stage-continuity"

SOURCE_FIELD_LABELS = {
    "upstream source-of-record checked",
    "source-of-record files checked",
}

REQUIRED_LABELS = {
    "current task/stage",
    "trigger",
    "inherited decisions",
    "open confirmations / hard stops",
    "what may change",
    "what must not change without confirmation",
    "next action boundary",
}

HIGH_RISK_CLASSES = {
    "proposal-or-brief",
    "methodology-or-method-plan",
    "ethics-or-compliance-material",
    "interview-guide-or-fieldwork-instrument",
    "concept-card-or-scenario-stimulus",
    "research-question-to-method-mapping",
    "analysis-plan",
    "stakeholder-facing-decision-memo",
    "chapter-or-section-formal-draft",
}

EMPTY_VALUES = {"", "-", "none", "n/a", "na", "not applicable", "to confirm", "to be confirmed"}


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def resolve(path_text: str) -> Path:
    path = Path(path_text.strip())
    return path if path.is_absolute() else ROOT / path


def extract_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    in_capsule = False
    for line in text.splitlines():
        if "Stage Continuity Capsule:" in line:
            in_capsule = True
            continue
        if in_capsule and line.startswith("## "):
            break
        match = re.match(r"^\s*-\s+([^:]+):\s*(.*)$", line)
        if match:
            fields[match.group(1).strip().lower()] = match.group(2).strip()
    return fields


def extract_paths(value: str) -> list[str]:
    output: list[str] = []
    seen: set[str] = set()
    for match in re.finditer(r"`([^`]+)`", value):
        token = match.group(1).strip()
        if "/" in token or token.endswith((".md", ".docx", ".json", ".jsonl", ".txt", ".py", ".pdf")):
            if token not in seen:
                output.append(token)
                seen.add(token)
    return output


def is_empty(value: str) -> bool:
    return value.strip().lower() in EMPTY_VALUES


def check(path: Path, deliverable_class: str, require_confirmation_boundary: bool) -> tuple[str, list[str], list[tuple[str, bool, str]]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    fields = extract_fields(text)
    issues: list[str] = []
    missing = sorted(label for label in REQUIRED_LABELS if label not in fields)
    if missing:
        issues.append(f"Missing capsule field(s): {', '.join(missing)}")
    if not any(label in fields for label in SOURCE_FIELD_LABELS):
        issues.append("Missing source-of-record path field.")

    source_values = " ".join(fields.get(label, "") for label in SOURCE_FIELD_LABELS)
    source_paths = extract_paths(source_values)
    path_rows: list[tuple[str, bool, str]] = []
    if not source_paths:
        issues.append("Source-of-record field has no concrete backtick file path.")
    for source_path in source_paths:
        resolved = resolve(source_path)
        exists = resolved.exists()
        mtime = datetime.fromtimestamp(resolved.stat().st_mtime).isoformat(timespec="seconds") if exists else "-"
        path_rows.append((source_path, exists, mtime))
        if not exists:
            issues.append(f"Source-of-record path does not exist: {source_path}")

    inherited = fields.get("inherited decisions", "")
    if inherited and "/" not in inherited and "`" not in inherited:
        issues.append("Inherited decisions should cite a stage node or source file path.")

    high_risk = deliverable_class in HIGH_RISK_CLASSES or require_confirmation_boundary
    if high_risk and is_empty(fields.get("what must not change without confirmation", "")):
        issues.append("High-risk deliverable requires a non-empty confirmation boundary.")

    status = "PASS" if not issues else "BLOCK"
    return status, issues, path_rows


def render_report(target: Path, status: str, issues: list[str], path_rows: list[tuple[str, bool, str]], deliverable_class: str) -> str:
    lines = [
        "# Stage Continuity Capsule Check",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Target: `{rel(target)}`",
        f"Deliverable class: `{deliverable_class or '-'}`",
        f"Status: `{status}`",
        "",
        "## Source Path Evidence",
        "",
        "| Path | Exists | Modified |",
        "|---|---:|---|",
    ]
    if path_rows:
        for source_path, exists, mtime in path_rows:
            lines.append(f"| `{source_path}` | {str(exists).lower()} | `{mtime}` |")
    else:
        lines.append("| - | false | `-` |")
    lines.extend(["", "## Issues", ""])
    lines.extend(f"- {issue}" for issue in issues) if issues else lines.append("- None")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This check verifies capsule structure and local source-path evidence. It does not prove research correctness, compliance readiness, source support, or delivery quality.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Stage Continuity Capsule.")
    parser.add_argument("target", help="Markdown file containing a Stage Continuity Capsule.")
    parser.add_argument("--deliverable-class", default="", help="Deliverable class from STAGE_GRAPH.md.")
    parser.add_argument("--require-confirmation-boundary", action="store_true")
    parser.add_argument("--no-report", action="store_true")
    args = parser.parse_args()

    target = Path(args.target)
    if not target.is_absolute():
        target = ROOT / target
    status, issues, path_rows = check(target, args.deliverable_class, args.require_confirmation_boundary)
    report = render_report(target, status, issues, path_rows, args.deliverable_class)
    if not args.no_report:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        out = OUT_DIR / f"Stage_Continuity_Capsule_Check_{target.stem}_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.md"
        out.write_text(report, encoding="utf-8")
        print(f"Report: {out}")
    print(f"status: {status}")
    for issue in issues:
        print(f"- {issue}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
