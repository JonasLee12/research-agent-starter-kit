#!/usr/bin/env python3
"""Check whether a research planning note contains a usable cognitive protocol.

This is a deterministic text check. It cannot judge scholarly quality by itself,
but it can catch missing gap/problem types, weak warrants, and missing section
types before formal drafting.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "audit-reports"

ALLOWED_GAP_TYPES = {
    "conceptual gap",
    "empirical/context gap",
    "methodological gap",
    "implementation/adoption boundary",
    "ethics/governance gap",
    "policy/practice gap",
    "evidence synthesis gap",
    "technical/design gap",
}

SECTION_TYPES = {
    "introduction",
    "rationale",
    "literature review",
    "methodology",
    "methods",
    "findings",
    "results",
    "discussion",
    "implications",
    "proposal",
    "grant",
    "report",
    "recommendation",
}


@dataclass
class Finding:
    status: str
    message: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def field_value(text: str, field: str) -> str:
    pattern = rf"(?im)^\s*-?\s*{re.escape(field)}\s*:\s*(.+)$"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else ""


def contains_allowed_gap(text: str) -> bool:
    lower = text.lower()
    return any(gap in lower for gap in ALLOWED_GAP_TYPES)


def contains_section_type(text: str) -> bool:
    value = field_value(text, "Section type").lower()
    return any(section in value for section in SECTION_TYPES)


def warrant_has_connection(text: str) -> bool:
    warrant = field_value(text, "Warrant")
    lower = warrant.lower()
    connection_words = [
        "because",
        "therefore",
        "so",
        "suggests",
        "supports",
        "indicates",
        "shows",
        "given",
        "within",
        "as",
        "since",
        "thereby",
        "leads to",
        "connects",
    ]
    has_evidence_language = any(word in lower for word in connection_words)
    has_claim_language = bool(re.search(r"\bclaim\b|\bargue\b|\breasonable\b|\btherefore\b|\bso\b", lower))
    return bool(warrant) and has_evidence_language and has_claim_language


def check(text: str) -> list[Finding]:
    findings: list[Finding] = []
    if "cognitive protocol" not in text.lower():
        findings.append(Finding("WARN", "No explicit `Cognitive protocol` heading found."))
    if contains_section_type(text):
        findings.append(Finding("PASS", "Section type is declared and recognisable."))
    else:
        findings.append(Finding("FAIL", "Missing or unrecognised `Section type`."))
    if contains_allowed_gap(text):
        findings.append(Finding("PASS", "Gap/problem type uses an allowed category."))
    else:
        findings.append(Finding("FAIL", "Missing allowed gap/problem type."))
    for field in ["Main claim", "Evidence base", "Warrant", "Boundary", "Rhetorical plan"]:
        if field_value(text, field):
            findings.append(Finding("PASS", f"`{field}` is present."))
        else:
            findings.append(Finding("FAIL", f"`{field}` is missing."))
    if warrant_has_connection(text):
        findings.append(Finding("PASS", "Warrant includes claim/evidence connection language."))
    else:
        findings.append(Finding("FAIL", "Warrant is missing clear claim/evidence connection language."))
    return findings


def render_report(source: Path, findings: list[Finding]) -> str:
    failed = [finding for finding in findings if finding.status == "FAIL"]
    status = "PASS" if not failed else "BLOCKED"
    lines = [
        "# Cognitive Protocol Check",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Source: `{source}`",
        f"Status: `{status}`",
        "",
        "## Findings",
        "",
    ]
    lines.extend(f"- {finding.status}: {finding.message}" for finding in findings)
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This deterministic check catches missing protocol elements. It does not prove the argument is scholarly, original, or source-supported.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a cognitive protocol note.")
    parser.add_argument("path", help="Path to Markdown/text planning note.")
    parser.add_argument("--strict", action="store_true", help="Return non-zero if any FAIL finding appears.")
    parser.add_argument("--output-dir", default=str(OUT_DIR), help="Directory for Markdown report.")
    args = parser.parse_args()

    source = Path(args.path)
    if not source.is_absolute():
        source = ROOT / source
    out_dir = Path(args.output_dir)
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    findings = check(read_text(source))
    report = render_report(source, findings)
    report_path = out_dir / f"Cognitive_Protocol_Check_{datetime.now().strftime('%Y-%m-%d_%H%M%S_%f')}.md"
    report_path.write_text(report, encoding="utf-8")
    print(report)
    print(f"Report: {report_path}")
    has_fail = any(finding.status == "FAIL" for finding in findings)
    return 1 if args.strict and has_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
