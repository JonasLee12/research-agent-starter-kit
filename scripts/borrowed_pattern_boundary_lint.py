#!/usr/bin/env python3
"""Lint borrowed external skill-pattern language for unsafe imports.

This protects a research-agent system when ideas are borrowed from public
workflow or style projects. It allows boundary language such as "do not promise detector scores",
but blocks positive instructions that promise detector evasion, authorship
verdicts, or style manipulation as an AI-detection tactic.

The default target list focuses on active rule/skill files; README, CHANGELOG,
and overview docs are excluded because they often mention refused patterns as
descriptive release notes rather than executable agent instructions.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "audit-reports" / "borrowed-pattern-boundary"

DEFAULT_TARGETS = [
    "AGENTS.md",
    "PROJECT_AGENT_PREFERENCES.md",
    ".agents/skills/uk-academic-writing-style/SKILL.md",
    ".agents/skills/authorial-voice-integrity/SKILL.md",
    ".agents/skills/style-memory-and-revision-gate/SKILL.md",
    ".agents/skills/academic-integrity-preflight/SKILL.md",
    "research-wiki/AI_WRITING_AUTHORIAL_VOICE_POLICY.md",
    "research-wiki/CLAIM_LEDGER_LITE_PROTOCOL.md",
    "research-wiki/VISIBLE_OUTPUT_QA_PROTOCOL.md",
]

PROHIBITED_PATTERNS: list[tuple[str, str]] = [
    (
        r"\b(pass|bypass|beat|evade|avoid)\b.{0,50}\b(ai|aigc|detector|detection|turnitin|gptzero)\b",
        "detector-evasion promise",
    ),
    (
        r"\b(ai|aigc|detector|detection|turnitin|gptzero)\b.{0,50}\b(pass|bypass|beat|evade|avoid)\b",
        "detector-evasion promise",
    ),
    (
        r"\b(detector[- ]score|detection[- ]score|ai[- ]rate|aigc[- ]rate)\b.{0,50}\b(improve|lower|reduce|optimise|optimize|target|guarantee)\b",
        "detector-score optimisation promise",
    ),
    (
        r"\b(improve|lower|reduce|optimise|optimize|target|guarantee)\b.{0,50}\b(detector[- ]score|detection[- ]score|ai[- ]rate|aigc[- ]rate)\b",
        "detector-score optimisation promise",
    ),
    (
        r"\b(authorship|ai-generated)\b.{0,30}\b(verdict|judgement|judgment|guarantee|guaranteed)\b",
        "authorship-verdict promise",
    ),
    (
        r"\b(humanise|humanize|make human|make it human|undetectable)\b.{0,60}\b(detector|detection|ai|aigc)\b",
        "humanising-as-evasion tactic",
    ),
    (
        r"(绕过|规避|骗过).{0,24}(检测|AI|AIGC|Turnitin|GPTZero)",
        "detector-evasion promise",
    ),
    (
        r"(降低|减少|优化).{0,18}(AI率|AIGC率|检测率)",
        "detector-score optimisation promise",
    ),
]

BOUNDARY_CUES = [
    "do not",
    "don't",
    "must not",
    "cannot",
    "not ",
    "never",
    "refuse",
    "block",
    "blocked",
    "boundary",
    "handles requests framed as",
    "requests framed as",
    "requests such as",
    "must be routed",
    "define how",
    "avoid promising",
    "no detector",
    "不要",
    "不能",
    "不得",
    "不应",
    "禁止",
    "拒绝",
    "边界",
]

BOUNDARY_SECTION_HEADINGS = {
    "avoid",
    "not allowed",
    "not allowed:",
    "trigger phrases",
    "trigger phrases:",
}


@dataclass
class Finding:
    path: str
    line: int
    category: str
    evidence: str


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def resolve(value: str) -> Path:
    path = Path(value).expanduser()
    return path if path.is_absolute() else ROOT / path


def is_boundary_line(line: str) -> bool:
    lowered = line.lower()
    return any(cue in lowered for cue in BOUNDARY_CUES)


def scan_text(path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    in_fence = False
    in_boundary_section = False
    for index, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        heading = stripped.strip("#").strip().lower()
        if heading in BOUNDARY_SECTION_HEADINGS:
            in_boundary_section = True
            continue
        if "framed as:" in line.lower() or "triggered by:" in line.lower():
            in_boundary_section = True
            continue
        if stripped.startswith("#") and heading not in BOUNDARY_SECTION_HEADINGS:
            in_boundary_section = False
        if in_fence or in_boundary_section or is_boundary_line(line):
            continue
        for pattern, category in PROHIBITED_PATTERNS:
            if re.search(pattern, line, flags=re.I):
                findings.append(Finding(rel(path), index, category, stripped[:220]))
    return findings


def scan_paths(paths: list[Path]) -> tuple[list[Finding], list[str]]:
    findings: list[Finding] = []
    missing: list[str] = []
    for path in paths:
        if not path.exists():
            missing.append(rel(path))
            continue
        if path.is_dir():
            for child in sorted(path.rglob("*.md")):
                findings.extend(scan_text(child, child.read_text(encoding="utf-8", errors="replace")))
            continue
        findings.extend(scan_text(path, path.read_text(encoding="utf-8", errors="replace")))
    return findings, missing


def render_report(paths: list[Path], findings: list[Finding], missing: list[str]) -> str:
    status = "PASS" if not findings else "BLOCK"
    lines = [
        "# Borrowed Pattern Boundary Lint",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Status: `{status}`",
        "",
        "## Targets",
        "",
    ]
    lines.extend(f"- `{rel(path)}`" for path in paths)
    lines.extend(["", "## Findings", ""])
    if findings:
        lines.extend(
            f"- `{item.path}:{item.line}` [{item.category}] {item.evidence}"
            for item in findings
        )
    else:
        lines.append("- None")
    if missing:
        lines.extend(["", "## Missing Targets", ""])
        lines.extend(f"- `{item}`" for item in missing)
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This lint detects unsafe positive instructions imported from external style/skill projects. It is not an AI detector, source check, ethics check, or academic-quality review.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint borrowed external skill-pattern language.")
    parser.add_argument("targets", nargs="*", help="Files or directories to scan. Defaults to core local style/skill policy files.")
    parser.add_argument("--no-report", action="store_true", help="Do not write a markdown report.")
    args = parser.parse_args()

    target_values = args.targets or DEFAULT_TARGETS
    paths = [resolve(value) for value in target_values]
    findings, missing = scan_paths(paths)
    report = render_report(paths, findings, missing)
    if not args.no_report:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        out = OUT_DIR / f"Borrowed_Pattern_Boundary_Lint_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.md"
        out.write_text(report, encoding="utf-8")
        print(f"Report: {out}")
    print(f"status: {'PASS' if not findings else 'BLOCK'}")
    for item in findings:
        print(f"- {item.path}:{item.line} [{item.category}] {item.evidence}")
    if missing:
        print("missing targets:")
        for item in missing:
            print(f"- {item}")
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
