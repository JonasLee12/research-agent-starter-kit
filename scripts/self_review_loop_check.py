#!/usr/bin/env python3
"""Check that an academic self-review loop is concrete enough to audit."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "audit-reports" / "self-review-loop"


@dataclass
class Check:
    name: str
    status: str
    evidence: str


REQUIRED_PATTERNS = [
    ("pass_1_present", r"\bpass\s*1\b|self-review pass 1|first-pass", "Pass 1 review is present."),
    ("pass_2_present", r"\bpass\s*2\b|self-review pass 2|second-pass|fresh judgement", "Pass 2 / fresh review is present."),
    ("paragraph_locator", r"\b(paragraph|para\.?|section|p\d+|¶)\b", "Findings identify a paragraph or section location."),
    ("severity_label", r"\b(HIGH|MEDIUM|LOW|High|Medium|Low)\b|\bseverity\b", "Findings use severity labels."),
    ("revision_action", r"\b(revision action|action|revise|rewrite|qualify|remove|split|move|merge)\b", "Findings include actionable revision steps."),
    ("evidence_or_warrant", r"\b(evidence|source boundary|warrant|claim-support|citation)\b", "Review checks evidence/warrant quality."),
    ("fresh_pass_2", r"\b(fresh judgement|remaining weakest|ready for next gate|ready for UK academic style|pass 2 judgement)\b", "Pass 2 gives a fresh judgement."),
]

GENERIC_PASS_PATTERNS = [
    r"\b(looks good|overall good|generally clear|no major issues|well written)\b",
]


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def resolve(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else ROOT / path


def run_checks(text: str) -> list[Check]:
    checks: list[Check] = []
    for name, pattern, description in REQUIRED_PATTERNS:
        match = re.search(pattern, text, flags=re.I)
        checks.append(Check(name, "PASS" if match else "BLOCK", description if match else f"Missing: {description}"))
    generic_hits = []
    for pattern in GENERIC_PASS_PATTERNS:
        generic_hits.extend(match.group(0) for match in re.finditer(pattern, text, flags=re.I))
    if generic_hits and not re.search(r"\b(HIGH|MEDIUM|LOW|severity|revision action|paragraph)\b", text, flags=re.I):
        checks.append(Check("generic_praise_without_diagnostics", "BLOCK", ", ".join(generic_hits[:5])))
    else:
        checks.append(Check("generic_praise_without_diagnostics", "PASS", "No unsupported generic praise-only review pattern found."))
    return checks


def render(path: Path, checks: list[Check]) -> str:
    status = "PASS" if all(item.status == "PASS" for item in checks) else "BLOCK"
    lines = [
        "# Self-Review Loop Check",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"Target: `{rel(path)}`",
        f"Status: `{status}`",
        "",
        "## Checks",
        "",
        "| Check | Status | Evidence |",
        "|---|---|---|",
    ]
    for item in checks:
        evidence = item.evidence.replace("|", "\\|")
        lines.append(f"| {item.name} | {item.status} | {evidence} |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This check verifies that a self-review record contains concrete diagnostics. It does not judge whether the revised prose is academically sufficient.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check academic self-review loop depth.")
    parser.add_argument("file")
    parser.add_argument("--output-dir", default=str(OUT_DIR))
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    target = resolve(args.file)
    if not target.exists():
        print(f"Missing target: {target}")
        return 2
    text = target.read_text(encoding="utf-8", errors="replace")
    checks = run_checks(text)
    status = "PASS" if all(item.status == "PASS" for item in checks) else "BLOCK"

    out_dir = resolve(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"Self_Review_Loop_Check_{target.stem}_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.md"
    out.write_text(render(target, checks), encoding="utf-8")
    print(f"Report: {out}")
    print(f"Status: {status}")
    return 1 if args.strict and status == "BLOCK" else 0


if __name__ == "__main__":
    raise SystemExit(main())
