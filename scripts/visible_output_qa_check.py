#!/usr/bin/env python3
"""Validate Visible Output QA notes for research-agent deliverables."""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "audit-reports" / "visible-output-qa"

REQUIRED_FIELDS = {
    "artifact",
    "communication job",
    "rendered output / preview",
    "deterministic checks",
    "visual inspection",
    "baseline / regression check",
    "unresolved risks",
    "delivery verdict",
}

ACCEPTED_VERDICTS = {
    "passed",
    "delta-accepted",
    "risk-accepted-by-user",
    "draft-not-rendered",
    "blocked",
}


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def normalise(label: str) -> str:
    return re.sub(r"\s+", " ", label.strip().lower())


def extract_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    current = False
    current_label: str | None = None
    for line in text.splitlines():
        marker = line.strip().strip("#").strip().rstrip(":").lower()
        if marker == "visible output qa":
            current = True
            current_label = None
            continue
        if current and line.startswith("## ") and marker != "visible output qa":
            current = False
            current_label = None
            continue
        if not current:
            continue
        match = re.match(r"^\s*-\s+([^:]+):\s*(.*)$", line)
        if match:
            current_label = normalise(match.group(1))
            fields[current_label] = match.group(2).strip()
            continue
        if current_label and line.strip():
            fields[current_label] = f"{fields[current_label]} {line.strip()}".strip()
    return fields


def extract_paths(value: str) -> list[str]:
    paths: list[str] = []
    for match in re.finditer(r"`([^`]+)`", value):
        token = match.group(1).strip()
        if "/" in token or token.endswith((".md", ".docx", ".pdf", ".png", ".jpg", ".jpeg", ".svg", ".html")):
            paths.append(token)
    bare = r"(?<!`)([A-Za-z0-9_.-]+/[A-Za-z0-9_./ -]+\.(?:md|docx|pdf|png|jpe?g|svg|html))(?!`)"
    paths.extend(match.group(1).strip() for match in re.finditer(bare, value))
    output: list[str] = []
    seen: set[str] = set()
    for path in paths:
        if path not in seen:
            output.append(path)
            seen.add(path)
    return output


def none_with_reason(value: str) -> bool:
    lowered = value.lower()
    return ("not-applicable" in lowered or "not applicable" in lowered or "none" in lowered or "draft-not-rendered" in lowered) and len(lowered) > 14


def empty(value: str) -> bool:
    return value.strip().lower() in {"", "-", "none", "n/a", "na", "to confirm"}


def check(path: Path, allow_no_render: bool) -> tuple[str, list[str], list[tuple[str, bool]]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    fields = extract_fields(text)
    issues: list[str] = []
    path_rows: list[tuple[str, bool]] = []
    if not fields:
        issues.append("missing `Visible Output QA` section")
    missing = sorted(REQUIRED_FIELDS - set(fields))
    if missing:
        issues.append("missing field(s): " + ", ".join(missing))
    for field in sorted(REQUIRED_FIELDS & set(fields)):
        if empty(fields[field]):
            issues.append(f"empty field: {field}")

    render_value = fields.get("rendered output / preview", "")
    render_paths = extract_paths(render_value)
    if not render_paths and not allow_no_render and not none_with_reason(render_value):
        issues.append("rendered output / preview needs concrete path evidence, or explicit draft/not-applicable reason")
    for path_text in render_paths + extract_paths(fields.get("artifact", "")):
        resolved = Path(path_text)
        if not resolved.is_absolute():
            resolved = ROOT / resolved
        exists = resolved.exists()
        path_rows.append((path_text, exists))
        if not exists:
            issues.append(f"referenced path does not exist: {path_text}")

    deterministic = fields.get("deterministic checks", "").lower()
    if "pass" not in deterministic and "n/a" not in deterministic and "not-applicable" not in deterministic:
        issues.append("deterministic checks must name PASS or an explicit not-applicable reason")
    visual = fields.get("visual inspection", "").lower()
    if not any(token in visual for token in ["pass", "inspected", "checked", "not-applicable", "n/a", "draft-not-rendered"]):
        issues.append("visual inspection must state inspected/checked/PASS or an explicit not-applicable reason")
    verdict = fields.get("delivery verdict", "").lower().strip("` .")
    if verdict.startswith("not-applicable"):
        pass
    elif verdict not in ACCEPTED_VERDICTS:
        issues.append(f"delivery verdict must be one of {', '.join(sorted(ACCEPTED_VERDICTS))} or not-applicable - reason")
    if verdict == "passed" and issues:
        issues.append("delivery verdict cannot be `passed` while QA issues remain")
    if verdict == "risk-accepted-by-user":
        joined = " ".join(fields.values()).lower()
        if "user" not in joined or "accept" not in joined:
            issues.append("risk-accepted-by-user requires explicit user acceptance note")
    status = "PASS" if not issues else "BLOCK"
    return status, issues, path_rows


def render_report(target: Path, status: str, issues: list[str], path_rows: list[tuple[str, bool]]) -> str:
    lines = [
        "# Visible Output QA Check",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Target: `{rel(target)}`",
        f"Status: `{status}`",
        "",
        "## Referenced Paths",
        "",
        "| Path | Exists |",
        "|---|---:|",
    ]
    if path_rows:
        for path_text, exists in path_rows:
            lines.append(f"| `{path_text}` | {str(exists).lower()} |")
    else:
        lines.append("| - | false |")
    lines.extend(["", "## Issues", ""])
    if issues:
        lines.extend(f"- {issue}" for issue in issues)
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This check validates visible-output QA structure and path evidence. A script PASS does not prove reader-visible quality, citation support, compliance readiness, rubric/journal/client requirement compliance, academic/professional quality, or submission readiness.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Visible Output QA markdown note.")
    parser.add_argument("target", help="Markdown file containing Visible Output QA.")
    parser.add_argument("--allow-no-render", action="store_true", help="Allow no rendered output path when a draft/not-applicable reason is present.")
    parser.add_argument("--no-report", action="store_true", help="Do not write a markdown report.")
    args = parser.parse_args()

    target = Path(args.target)
    if not target.is_absolute():
        target = ROOT / target
    status, issues, path_rows = check(target, args.allow_no_render)
    report = render_report(target, status, issues, path_rows)
    if not args.no_report:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        out = OUT_DIR / f"Visible_Output_QA_Check_{target.stem}_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.md"
        out.write_text(report, encoding="utf-8")
        print(f"Report: {out}")
    print(f"status: {status}")
    for issue in issues:
        print(f"- {issue}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
