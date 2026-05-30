#!/usr/bin/env python3
"""Scan formal academic artifacts for concrete integrity preflight risks."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "audit-reports" / "academic-integrity-preflight"
EVENT_LOG = ROOT / "research-wiki" / "SESSION_EVENT_LOG.jsonl"


@dataclass
class Finding:
    severity: str
    category: str
    line: int
    evidence: str
    action: str


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def resolve(path_text: str) -> Path:
    path = Path(path_text).expanduser()
    return path if path.is_absolute() else ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def add_pattern_findings(lines: list[str], findings: list[Finding], patterns: list[tuple[str, str, str, str]]) -> None:
    for index, line in enumerate(lines, 1):
        for pattern, severity, category, action in patterns:
            if re.search(pattern, line, flags=re.I):
                snippet = line.strip()
                findings.append(Finding(severity, category, index, snippet[:220], action))


def scan(text: str, args: argparse.Namespace) -> list[Finding]:
    findings: list[Finding] = []
    lines = text.splitlines()
    patterns = [
        (r"\b(as an ai|as a language model|i cannot browse|i can'?t access|chatgpt|claude)\b", "HOLD", "prompt residue", "Remove chatbot meta-text before academic use."),
        (r"\b(here'?s|certainly,?|of course,?)\s+(a|the|your)\b", "WARN", "chat-style residue", "Rewrite as academic prose if this appears in the artifact body."),
        (r"\b(TO CONFIRM|SOURCE TO ADD|NEEDS VERIFICATION|citation needed|TODO|TBD|lorem ipsum)\b", "HOLD", "unresolved placeholder", "Resolve, remove, or explicitly mark as not for delivery."),
        (r"\bxxx\b|\[[^\]]*(insert|add|complete|placeholder|confirm|source)[^\]]*\]", "HOLD", "template placeholder", "Replace template placeholder or remove unused guidance."),
        (r"\b(forthcoming source|unknown author|fake citation|example citation)\b", "HOLD", "reference integrity", "Replace with verified reference or remove the claim."),
        (r"\b(AUTHOR_PLACEHOLDER|YEAR_PLACEHOLDER|CITATION_PLACEHOLDER)\b", "HOLD", "reference placeholder", "Replace placeholder citation metadata with a verified source or remove the claim."),
    ]
    add_pattern_findings(lines, findings, patterns)

    if args.requires_rubric and not args.rubric_evidence:
        findings.append(Finding("HOLD", "requirement evidence", 0, "requires-rubric set but no rubric/requirement evidence path supplied", "Check the relevant requirement evidence file and cite the source path."))
    if args.requires_ethics and not args.ethics_evidence:
        findings.append(Finding("HOLD", "ethics/compliance evidence", 0, "requires-ethics set but no ethics/compliance evidence path supplied", "Check the relevant ethics, IRB, compliance, or privacy tracker before delivery."))
    if args.citation_heavy and not args.citation_evidence:
        findings.append(Finding("HOLD", "citation evidence", 0, "citation-heavy set but no citation evidence path supplied", "Run citation consistency or claim-support audit."))

    if re.search(r"\b(75\+|deadline|word count|submission|Canvas|LMS|marking criteria|rubric|journal guideline|funder requirement|client requirement)\b", text, flags=re.I) and not args.rubric_evidence:
        findings.append(Finding("WARN", "requirement boundary", 0, "assessment/submission/requirement language appears without explicit evidence path", "Check local requirement evidence before relying on this text."))
    if re.search(r"\b(consent|withdrawal|recording|participant information|data storage|recruitment)\b", text, flags=re.I) and not args.ethics_evidence:
        findings.append(Finding("WARN", "ethics boundary", 0, "ethics-sensitive language appears without explicit ethics evidence path", "Check ethics tracker before delivery."))
    if re.search(r"\bAI[- ]use disclosure|use of AI|AI assistance\b", text, flags=re.I) and not args.rubric_evidence:
        findings.append(Finding("WARN", "AI-use disclosure boundary", 0, "AI-use/disclosure language appears without source evidence path", "Do not imply a formal disclosure rule unless locally verified."))

    return findings


def overall_status(findings: list[Finding]) -> str:
    if any(item.severity == "HOLD" for item in findings):
        return "HOLD"
    if findings:
        return "WARN"
    return "PASS"


def render(path: Path, stage: str, findings: list[Finding]) -> str:
    status = overall_status(findings)
    lines = [
        "# Academic Integrity Preflight",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"Target: `{rel(path)}`",
        f"Stage: `{stage}`",
        f"Status: `{status}`",
        "",
        "## Findings",
        "",
        "| Severity | Category | Line | Evidence | Action |",
        "|---|---|---:|---|---|",
    ]
    if findings:
        for item in findings:
            evidence = item.evidence.replace("|", "\\|")
            action = item.action.replace("|", "\\|")
            lines.append(f"| {item.severity} | {item.category} | {item.line or '-'} | {evidence} | {action} |")
    else:
        lines.append("| PASS | no finding | - | - | - |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This preflight checks concrete artifact risks. It is not an AI detector and does not prove citation support, ethics approval, or official rubric compliance.",
            "",
        ]
    )
    return "\n".join(lines)


def append_event(target: Path, report: Path, status: str) -> None:
    EVENT_LOG.parent.mkdir(parents=True, exist_ok=True)
    now_utc = datetime.now(timezone.utc)
    event = {
        "timestamp": now_utc.isoformat(timespec="seconds"),
        "run_id": f"academic-integrity-preflight-{now_utc.strftime('%Y-%m-%d_%H%M%S')}",
        "window": "Maintenance",
        "event_type": "quality_gate",
        "status": "completed" if status != "HOLD" else "failed",
        "skill": "academic-integrity-preflight",
        "file": rel(report),
        "evidence": f"Academic integrity preflight {status} for {rel(target)}.",
        "risk": "low" if status == "PASS" else "medium",
    }
    with EVENT_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run academic integrity preflight on a Markdown/text artifact.")
    parser.add_argument("--target", required=True)
    parser.add_argument("--stage", choices=["early", "final"], default="early")
    parser.add_argument("--output-dir", default=str(OUT_DIR))
    parser.add_argument("--requires-ethics", action="store_true")
    parser.add_argument("--requires-rubric", action="store_true")
    parser.add_argument("--citation-heavy", action="store_true")
    parser.add_argument("--ethics-evidence")
    parser.add_argument("--rubric-evidence")
    parser.add_argument("--citation-evidence")
    parser.add_argument("--strict", action="store_true", help="Return non-zero on HOLD.")
    args = parser.parse_args()

    target = resolve(args.target)
    if not target.exists():
        print(f"Missing target: {target}", file=sys.stderr)
        return 2
    text = read_text(target)
    findings = scan(text, args)
    status = overall_status(findings)

    out_dir = resolve(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    report_stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
    report = out_dir / f"Academic_Integrity_Preflight_{target.stem}_{report_stamp}.md"
    report.write_text(render(target, args.stage, findings), encoding="utf-8")
    append_event(target, report, status)
    print(f"Report: {report}")
    print(f"Status: {status}")
    return 1 if args.strict and status == "HOLD" else 0


if __name__ == "__main__":
    raise SystemExit(main())
