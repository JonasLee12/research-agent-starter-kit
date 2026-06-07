#!/usr/bin/env python3
"""Check that a document-quality gate record is concrete enough to audit."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "audit-reports" / "document-quality"


@dataclass
class Check:
    name: str
    status: str
    evidence: str
    weight: int = 1


FORMAL_PATTERNS = [
    ("success_criteria", r"success criteria|purpose|audience|intended audience|must-have", "Success criteria or document purpose is explicit.", 2),
    ("source_evidence_boundary", r"source-first|source map|material passport|evidence boundary|confirmed facts", "Source/evidence boundary is recorded.", 2),
    ("citation_or_source_status", r"citation|claim-support|source-readiness|reference", "Citation or source-readiness status is recorded.", 2),
    ("ethics_or_privacy_status", r"ethics|privacy|participant|not participant-facing|sensitive", "Ethics/privacy status is recorded.", 1),
    ("style_quality_status", r"style-fingerprint|authorial voice|academic register|style-memory|writing style|language quality", "Style and register checks are recorded.", 1),
    ("format_or_render_status", r"\.docx|Word|render|PDF|PNG|format|page", "Format/render status or plan is recorded.", 1),
    ("residual_risk", r"residual risk|remaining risk|unresolved|TO CONFIRM|not final|not submission-ready", "Residual risk or unresolved items are recorded.", 2),
    ("quality_judgement", r"quality judgement|status:\s*(PASS|BLOCK|WARN)|readiness|ready for", "A quality judgement is stated.", 1),
]


STANDARD_PATTERNS = [
    ("success_criteria", r"success criteria|purpose|audience|intended audience|must-have", "Purpose or success criteria is explicit.", 1),
    ("source_evidence_boundary", r"source|evidence|confirmed|boundary", "Source/evidence boundary is recorded.", 1),
    ("residual_risk", r"risk|unresolved|TO CONFIRM|next action", "Risks or next actions are recorded.", 1),
    ("quality_judgement", r"quality|status:\s*(PASS|BLOCK|WARN)|ready", "A quality judgement is stated.", 1),
]


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def resolve(path_text: str) -> Path:
    path = Path(path_text).expanduser()
    return path if path.is_absolute() else ROOT / path


def run_checks(text: str, mode: str) -> list[Check]:
    patterns = FORMAL_PATTERNS if mode == "formal" else STANDARD_PATTERNS
    checks: list[Check] = []
    for name, pattern, description, weight in patterns:
        matched = re.search(pattern, text, flags=re.I)
        checks.append(Check(name, "PASS" if matched else "BLOCK", description if matched else f"Missing: {description}", weight))

    generic_pass = re.search(r"\b(status:\s*PASS|quality\s+pass|looks good|ready)\b", text, flags=re.I)
    concrete_markers = sum(1 for item in checks if item.status == "PASS")
    if generic_pass and concrete_markers < max(3, len(checks) // 2):
        checks.append(Check("generic_quality_pass_without_evidence", "BLOCK", "Quality pass is too generic for the recorded evidence.", 2))
    else:
        checks.append(Check("generic_quality_pass_without_evidence", "PASS", "No unsupported generic quality-pass pattern found.", 1))
    return checks


def weighted_score(checks: list[Check]) -> tuple[int, int]:
    total = sum(item.weight for item in checks)
    passed = sum(item.weight for item in checks if item.status == "PASS")
    return passed, total


def render(path: Path, mode: str, checks: list[Check]) -> str:
    passed, total = weighted_score(checks)
    status = "PASS" if all(item.status == "PASS" for item in checks) else "BLOCK"
    lines = [
        "# Document Quality Check",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"Target: `{rel(path)}`",
        f"Mode: `{mode}`",
        f"Status: `{status}`",
        f"Weighted score: `{passed}/{total}`",
        "",
        "## Checks",
        "",
        "| Check | Status | Weight | Evidence |",
        "|---|---|---:|---|",
    ]
    for item in checks:
        evidence = item.evidence.replace("|", "\\|")
        lines.append(f"| {item.name} | {item.status} | {item.weight} | {evidence} |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This tool checks whether a document-quality gate record contains auditable judgement evidence. It does not prove the academic quality of the underlying document.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check document-quality gate record depth.")
    parser.add_argument("file")
    parser.add_argument("--mode", choices=["standard", "formal"], default="formal")
    parser.add_argument("--output-dir", default=str(OUT_DIR))
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    target = resolve(args.file)
    if not target.exists():
        print(f"Missing target: {target}")
        return 2
    text = target.read_text(encoding="utf-8", errors="replace")
    checks = run_checks(text, args.mode)
    status = "PASS" if all(item.status == "PASS" for item in checks) else "BLOCK"

    out_dir = resolve(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"Document_Quality_Check_{target.stem}_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.md"
    out.write_text(render(target, args.mode, checks), encoding="utf-8")
    print(f"Report: {out}")
    print(f"Status: {status}")
    return 1 if args.strict and status == "BLOCK" else 0


if __name__ == "__main__":
    raise SystemExit(main())
