#!/usr/bin/env python3
"""Run lightweight static checks against the research-agent skill eval registry.

This is not a full behavioural eval. It verifies that eval cases are present,
referenced project skills exist, and required local gate files are available.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
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
        if token.endswith((".md", ".txt", ".json", ".yml", ".yaml")):
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
    missing.extend(check_behavioral_case(case.case_id))
    return ("PASS" if not missing else "WARN", missing)


def run_local_script(args: list[str]) -> tuple[int, str]:
    proc = subprocess.run(
        ["python3", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    return proc.returncode, "\n".join(item for item in [proc.stdout.strip(), proc.stderr.strip()] if item)


def eval_fixture_path(case_id: str, suffix: str = ".md") -> Path:
    out_dir = ROOT / ".agent-runtime" / "eval-evidence"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / f"{case_id.lower()}_fixture{suffix}"


def receipt_infer_window(explicit_window: str | None, task_type: str, stage: str, task_id: str) -> str:
    script = ROOT / "scripts" / "skill_execution_receipt.py"
    spec = importlib.util.spec_from_file_location("skill_execution_receipt_eval", script)
    if spec is None or spec.loader is None:
        return "IMPORT_FAILED"
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.infer_window(explicit_window, task_type, stage, task_id)


def runtime_json(task: str) -> tuple[int, dict | None, str]:
    code, output = run_local_script(["scripts/agent_runtime.py", task, "--window", "Production"])
    if code != 0:
        return code, None, output
    try:
        return code, json.loads(output), output
    except json.JSONDecodeError:
        return code, None, output


def check_behavioral_case(case_id: str) -> list[str]:
    if case_id == "RUNTIME-005":
        code, data, output = runtime_json("Fix the citation format and typos only in this report")
        if code != 0:
            return [f"runtime-minor-edit-exit:{code}:{output[:120]}"]
        if data is None:
            return ["runtime-minor-edit-json"]
        task_types = set(data.get("task_types", []))
        receipts = set(data.get("receipt_requirements", []))
        problems = []
        if "minor_edit" not in task_types:
            problems.append(f"runtime-minor-edit-type:{','.join(sorted(task_types))}")
        if "formal_research_output" in task_types:
            problems.append("runtime-minor-edit-formal")
        forbidden = {"academic-integrity-preflight@thinking", "academic-self-review-loop@writing", "style-fingerprint-gate@writing"}
        overlap = sorted(forbidden & receipts)
        if overlap:
            problems.append(f"runtime-minor-edit-overstrict:{','.join(overlap)}")
        return problems
    if case_id == "RUNTIME-006":
        code, data, output = runtime_json("Write two formal methodology paragraphs synthesising the methodology literature")
        if code != 0:
            return [f"runtime-formal-methodology-exit:{code}:{output[:120]}"]
        if data is None:
            return ["runtime-formal-methodology-json"]
        task_types = set(data.get("task_types", []))
        receipts = set(data.get("receipt_requirements", []))
        required = {
            "academic-integrity-preflight@thinking",
            "cognitive-frameworks@thinking",
            "academic-self-review-loop@writing",
            "style-fingerprint-gate@writing",
            "dissertation-document-quality-gate@writing",
        }
        problems = []
        if "formal_research_output" not in task_types:
            problems.append(f"runtime-formal-methodology-type:{','.join(sorted(task_types))}")
        if "bounded_source_planning" in task_types:
            problems.append("runtime-formal-methodology-bounded")
        missing = sorted(required - receipts)
        if missing:
            problems.append(f"runtime-formal-methodology-receipts:{','.join(missing)}")
        return problems
    if case_id == "RUNTIME-007":
        code, data, output = runtime_json("Run methodology literature search and rematch sources")
        if code != 0:
            return [f"runtime-bounded-source-exit:{code}:{output[:120]}"]
        if data is None:
            return ["runtime-bounded-source-json"]
        task_types = set(data.get("task_types", []))
        receipts = set(data.get("receipt_requirements", []))
        forbidden = {
            "academic-integrity-preflight@thinking",
            "academic-self-review-loop@writing",
            "style-fingerprint-gate@writing",
            "uk-academic-writing-style@writing",
            "dissertation-document-quality-gate@writing",
        }
        problems = []
        if "bounded_source_planning" not in task_types:
            problems.append(f"runtime-bounded-source-type:{','.join(sorted(task_types))}")
        if "formal_research_output" in task_types:
            problems.append("runtime-bounded-source-formal")
        overlap = sorted(forbidden & receipts)
        if overlap:
            problems.append(f"runtime-bounded-source-overstrict:{','.join(overlap)}")
        return problems
    if case_id == "RUNTIME-008":
        code, data, output = runtime_json("整理 Methodology 的文献并写两段总结")
        if code != 0:
            return [f"runtime-ambiguous-formal-exit:{code}:{output[:120]}"]
        if data is None:
            return ["runtime-ambiguous-formal-json"]
        task_types = set(data.get("task_types", []))
        receipts = set(data.get("receipt_requirements", []))
        required = {"academic-integrity-preflight@thinking", "academic-self-review-loop@writing", "style-fingerprint-gate@writing"}
        problems = []
        if "formal_research_output" not in task_types:
            problems.append(f"runtime-ambiguous-formal-type:{','.join(sorted(task_types))}")
        if "bounded_source_planning" in task_types:
            problems.append("runtime-ambiguous-formal-bounded")
        missing = sorted(required - receipts)
        if missing:
            problems.append(f"runtime-ambiguous-formal-receipts:{','.join(missing)}")
        return problems
    if case_id == "RUNTIME-009":
        code, data, output = runtime_json("Check whether Palinkas 2015 has a usable sampling source section")
        if code != 0:
            return [f"runtime-bounded-lookup-exit:{code}:{output[:120]}"]
        if data is None:
            return ["runtime-bounded-lookup-json"]
        task_types = set(data.get("task_types", []))
        receipts = set(data.get("receipt_requirements", []))
        forbidden = {"academic-integrity-preflight@thinking", "academic-self-review-loop@writing", "style-fingerprint-gate@writing"}
        problems = []
        if "bounded_research_lookup" not in task_types:
            problems.append(f"runtime-bounded-lookup-type:{','.join(sorted(task_types))}")
        if "formal_research_output" in task_types:
            problems.append("runtime-bounded-lookup-formal")
        overlap = sorted(forbidden & receipts)
        if overlap:
            problems.append(f"runtime-bounded-lookup-overstrict:{','.join(overlap)}")
        return problems
    if case_id == "RUNTIME-010":
        code, data, output = runtime_json("Fix typos only in the submission-ready report")
        if code != 0:
            return [f"runtime-minor-protected-exit:{code}:{output[:120]}"]
        if data is None:
            return ["runtime-minor-protected-json"]
        task_types = set(data.get("task_types", []))
        receipts = set(data.get("receipt_requirements", []))
        required = {"academic-integrity-preflight@thinking", "academic-self-review-loop@writing"}
        problems = []
        if "formal_research_output" not in task_types:
            problems.append(f"runtime-minor-protected-type:{','.join(sorted(task_types))}")
        if "minor_edit" in task_types:
            problems.append("runtime-minor-protected-stayed-light")
        missing = sorted(required - receipts)
        if missing:
            problems.append(f"runtime-minor-protected-receipts:{','.join(missing)}")
        return problems
    if case_id == "RECEIPT-003":
        problems = []
        bounded = receipt_infer_window(None, "bounded_source_planning", "research", "eval-bounded-source")
        maintenance = receipt_infer_window(None, "system_maintenance", "maintenance", "eval-maintenance-sync")
        explicit = receipt_infer_window("Production", "system_maintenance", "maintenance", "eval-explicit-production")
        if bounded != "Production":
            problems.append(f"receipt-window-bounded:{bounded}")
        if maintenance != "Maintenance":
            problems.append(f"receipt-window-maintenance:{maintenance}")
        if explicit != "Production":
            problems.append(f"receipt-window-explicit:{explicit}")
        return problems
    if case_id == "LOG-001":
        log = eval_fixture_path(case_id, "_session_log.jsonl")
        runtime_dir = eval_fixture_path(case_id, "_runtime").with_suffix("")
        runtime_dir.mkdir(parents=True, exist_ok=True)
        runtime_receipt = runtime_dir / "runtime_preflight_log_001.json"
        runtime_receipt.write_text(
            json.dumps({"run_id": "eval-log-001", "window": "Maintenance"}, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        events = [
            {
                "timestamp": "2026-06-11T00:00:00+00:00",
                "run_id": "eval-log-001",
                "window": "Maintenance",
                "event_type": "session_start",
                "status": "completed",
                "skill": "agent-runtime-enforcement",
                "file": "scripts/agent_runtime.py",
                "evidence": "Eval fixture session started.",
                "risk": "low",
            },
            {
                "timestamp": "2026-06-11T00:00:01+00:00",
                "run_id": "eval-log-001",
                "window": "Maintenance",
                "event_type": "session_end",
                "status": "completed",
                "skill": "agent-runtime-enforcement",
                "file": "scripts/agent_runtime.py",
                "evidence": "Eval fixture session ended.",
                "risk": "low",
            },
        ]
        log.write_text("\n".join(json.dumps(item, ensure_ascii=False) for item in events) + "\n", encoding="utf-8")
        code, output = run_local_script(
            [
                "scripts/session_log_integrity_check.py",
                "--log",
                str(log),
                "--runtime-dir",
                str(runtime_dir),
                "--strict",
                "--no-report",
            ]
        )
        if code != 0:
            return [f"session-log-integrity-exit:{code}:{output[:120]}"]
        return [] if "Blocking issues: 0" in output else ["session-log-integrity-blocking-issues"]
    if case_id == "LOG-002":
        log = eval_fixture_path(case_id, "_illegal_window.jsonl")
        event = {
            "timestamp": "2026-06-11T00:00:00+00:00",
            "run_id": "eval-log-002",
            "window": "Unknown",
            "event_type": "gate_completed",
            "status": "completed",
            "skill": "agent-runtime-enforcement",
            "file": "scripts/agent_runtime.py",
            "evidence": "Eval fixture illegal window.",
            "risk": "low",
        }
        log.write_text(json.dumps(event, ensure_ascii=False) + "\n", encoding="utf-8")
        code, output = run_local_script(["scripts/session_log_integrity_check.py", "--log", str(log), "--strict", "--no-report"])
        return [] if code == 1 and "Blocking issues: 1" in output else [f"session-log-illegal-window:{code}:{output[:120]}"]
    if case_id == "LOG-003":
        log = eval_fixture_path(case_id, "_window_mismatch.jsonl")
        runtime_dir = eval_fixture_path(case_id, "_runtime").with_suffix("")
        runtime_dir.mkdir(parents=True, exist_ok=True)
        (runtime_dir / "runtime_preflight_log_003.json").write_text(
            json.dumps({"run_id": "eval-log-003", "window": "Production"}, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        event = {
            "timestamp": "2026-06-11T00:00:00+00:00",
            "run_id": "eval-log-003",
            "window": "Maintenance",
            "event_type": "gate_completed",
            "status": "completed",
            "skill": "agent-runtime-enforcement",
            "file": "scripts/agent_runtime.py",
            "evidence": "Eval fixture window mismatch.",
            "risk": "low",
        }
        log.write_text(json.dumps(event, ensure_ascii=False) + "\n", encoding="utf-8")
        code, output = run_local_script(
            [
                "scripts/session_log_integrity_check.py",
                "--log",
                str(log),
                "--runtime-dir",
                str(runtime_dir),
                "--strict",
                "--no-report",
            ]
        )
        return [] if code == 1 and "Blocking issues: 1" in output else [f"session-log-window-mismatch:{code}:{output[:120]}"]
    return []


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
