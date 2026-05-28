#!/usr/bin/env python3
"""Run lightweight static checks against the research-agent skill eval registry.

This is not a full behavioural eval. It verifies that eval cases are present,
referenced project skills exist, and required local gate files are available.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "research-wiki" / "SKILL_EVAL_REGISTRY.md"
DEFAULT_OUTPUT = ROOT / "research-wiki" / "skill-evals" / f"Skill_Eval_Run_{date.today().isoformat()}.md"

GLOBAL_OR_EXTERNAL_REFS = {
    "documents",
    "playwright",
    "skill-creator",
}

LOCAL_FILE_REFS = {
    "RUBRIC_EVIDENCE_GATE.md": "university-guidance/RUBRIC_EVIDENCE_GATE.md",
}


@dataclass
class EvalCase:
    case_id: str
    prompt: str
    expected: str
    must_not_do: str
    pass_criteria: str


def split_markdown_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def load_cases(path: Path) -> list[EvalCase]:
    cases: list[EvalCase] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = split_markdown_row(line)
        if len(cells) != 5:
            continue
        if cells[0] in {"Case ID", "---"} or cells[0].startswith("---"):
            continue
        if not re.match(r"^[A-Z]+-\d{3}$", cells[0]):
            continue
        cases.append(EvalCase(*cells))
    return cases


def project_skills() -> set[str]:
    skills: set[str] = set()
    skills_dir = ROOT / ".agents" / "skills"
    if not skills_dir.exists():
        return skills
    for skill_md in skills_dir.glob("*/SKILL.md"):
        skills.add(skill_md.parent.name)
    return skills


def referenced_tokens(text: str) -> list[str]:
    return re.findall(r"`([^`]+)`", text)


def check_case(case: EvalCase, available_skills: set[str]) -> tuple[str, list[str]]:
    missing: list[str] = []
    for token in referenced_tokens(case.expected):
        if token.endswith(".md"):
            rel_path = LOCAL_FILE_REFS.get(token, token)
            if not (ROOT / rel_path).exists():
                missing.append(token)
            continue
        if token.endswith(".py") or token.startswith("scripts/"):
            if not (ROOT / token).exists():
                missing.append(token)
            continue
        if token in GLOBAL_OR_EXTERNAL_REFS:
            continue
        if token not in available_skills:
            missing.append(token)
    return ("PASS" if not missing else "WARN", missing)


def render_report(cases: list[EvalCase], results: list[tuple[EvalCase, str, list[str]]]) -> str:
    pass_count = sum(1 for _, status, _ in results if status == "PASS")
    warn_count = len(results) - pass_count
    lines = [
        "# Skill Eval Run",
        "",
        f"Date: {date.today().isoformat()}",
        "",
        "Scope: static availability check for high-risk research-agent routing cases.",
        "",
        "Boundary: this does not prove behavioural quality. It checks whether the registry cases can be routed to existing local skills or known global tools.",
        "",
        "## Summary",
        "",
        f"- Cases checked: {len(cases)}",
        f"- Pass: {pass_count}",
        f"- Warning: {warn_count}",
        "",
        "## Results",
        "",
        "| Case ID | Status | Missing references | Pass criteria |",
        "|---|---|---|---|",
    ]
    for case, status, missing in results:
        missing_text = ", ".join(f"`{item}`" for item in missing) if missing else "-"
        lines.append(f"| {case.case_id} | {status} | {missing_text} | {case.pass_criteria} |")
    lines.extend(
        [
            "",
            "## Next Actions",
            "",
            "- Treat `WARN` as a maintenance task before relying on that workflow.",
            "- Add a new eval case after any high-risk skill or routing rule change.",
            "- Behavioural evals still require a future runner that tests real prompts against real agent outputs.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run research-agent skill eval registry checks.")
    parser.add_argument("--registry", default=str(REGISTRY), help="Path to skill eval registry.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Markdown report output path.")
    args = parser.parse_args()

    registry = Path(args.registry)
    output = Path(args.output)
    if not registry.is_absolute():
        registry = ROOT / registry
    if not output.is_absolute():
        output = ROOT / output

    cases = load_cases(registry)
    available = project_skills()
    results = [(case, *check_case(case, available)) for case in cases]

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_report(cases, results), encoding="utf-8")
    print(f"Wrote {output}")
    for case, status, missing in results:
        missing_text = ", ".join(missing) if missing else "-"
        print(f"{case.case_id}: {status} ({missing_text})")
    return 0 if all(status == "PASS" for _, status, _ in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
