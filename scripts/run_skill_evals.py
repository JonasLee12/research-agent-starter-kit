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
import shutil
import sqlite3
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

ARCHIVED_SKILLS = {
    "active-learning-design-support",
    "ai-agent-design-spec",
    "codesign-output-synthesis",
    "dissertation-figure-spec",
    "dissertation-research-wiki",
    "prototype-evaluation-audit",
    "teacher-adoption-modeling",
    "teaching-knowledge-base-plan",
    "viva-prep",
}

LIGHT_ROUTE_HEAVY_FILES = {
    "research-wiki/TASK_STATE.md",
    "research-wiki/PRODUCTION_RUN_REGISTER.md",
    "research-wiki/SESSION_EVENT_LOG.jsonl",
    "research-wiki/WINDOW_WORKFLOW_PROMPTS.md",
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
        if token.startswith(".") or "/" in token:
            if not (ROOT / token).exists():
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
    if case_id == "INTAKE-001":
        task_cards = (ROOT / "docs" / "TASK_CARDS.md").read_text(encoding="utf-8")
        task_cards_cn = (ROOT / "docs" / "TASK_CARDS_CN.md").read_text(encoding="utf-8")
        intake = (ROOT / "templates" / "SOURCE_FIRST_INTAKE_CARD.md").read_text(encoding="utf-8")
        combined = "\n".join([task_cards, task_cards_cn, intake])
        combined_lower = combined.lower()
        required_terms = [
            "source-first intake card",
            "submitted",
            "running",
            "blocked",
            "needs_confirmation",
            "completed",
            "failed",
            "cancelled",
            "bounded",
            "standard",
            "full",
            "allowed source corpus",
            "evidence and citation boundary",
            "privacy / compliance boundary",
            "do not use",
            "ghostwriting",
            "plagiarism reduction",
            "ai-detector evasion",
            "paid reseller",
            "citation-ready",
        ]
        problems = [f"intake-missing:{term}" for term in required_terms if term not in combined_lower]
        chinese_terms = ["任务卡", "降重", "降AI", "代写", "来源", "证据", "隐私", "引用就绪"]
        problems.extend(f"intake-missing:{term}" for term in chinese_terms if term not in combined)
        return problems
    if case_id == "INTAKE-002":
        files = [
            ROOT / "README.md",
            ROOT / "README_CN.md",
            ROOT / "docs" / "TASK_CARDS.md",
            ROOT / "docs" / "TASK_CARDS_CN.md",
            ROOT / "templates" / "SOURCE_FIRST_INTAKE_CARD.md",
        ]
        combined = "\n".join(path.read_text(encoding="utf-8") for path in files)
        combined_lower = combined.lower()
        required_terms = [
            "out of scope",
            "ghostwriting",
            "plagiarism reduction",
            "ai-detector evasion",
            "fake citations",
            "paid reseller",
            "proxy-user",
            "task intake is planning only",
            "not evidence",
            "citation readiness",
            "source-section verification",
            "route levels",
            "do not use for",
        ]
        problems = [f"intake-boundary-missing:{term}" for term in required_terms if term not in combined_lower]
        chinese_terms = ["不适用范围", "代写", "降重", "降 AI", "引用就绪", "不是证据", "路由层级"]
        problems.extend(f"intake-boundary-missing:{term}" for term in chinese_terms if term not in combined)
        return problems
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
        code, data, output = runtime_json("Check whether Author 2020 has a usable sampling source section")
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
    if case_id == "CODEXLOG-001":
        fixture_dir = ROOT / ".agent-runtime" / "eval-evidence" / "codexlog-001_codex"
        if fixture_dir.exists():
            shutil.rmtree(fixture_dir)
        fixture_dir.mkdir(parents=True, exist_ok=True)
        db = fixture_dir / "logs_2.sqlite"
        conn = sqlite3.connect(db)
        try:
            conn.execute("CREATE TABLE logs (id INTEGER PRIMARY KEY, level TEXT, message TEXT)")
            conn.commit()
        finally:
            conn.close()
        code, output = run_local_script(
            [
                "scripts/codex_sqlite_log_guard.py",
                "scan",
                "--root",
                str(fixture_dir),
                "--strict",
                "--no-report",
                "--max-wal-mb",
                "1",
                "--max-total-mb",
                "1",
            ]
        )
        if code != 0:
            return [f"codex-log-scan-exit:{code}:{output[:120]}"]
        return [] if "Candidates: 1" in output and "Issues: 0" in output else [f"codex-log-scan-output:{output[:120]}"]
    if case_id == "CODEXLOG-002":
        fixture_dir = ROOT / ".agent-runtime" / "eval-evidence" / "codexlog-002_codex"
        if fixture_dir.exists():
            shutil.rmtree(fixture_dir)
        fixture_dir.mkdir(parents=True, exist_ok=True)
        db = fixture_dir / "logs_2.sqlite"
        conn = sqlite3.connect(db)
        try:
            conn.execute("CREATE TABLE logs (id INTEGER PRIMARY KEY, level TEXT, message TEXT)")
            conn.commit()
        finally:
            conn.close()
        dry_code, dry_output = run_local_script(
            ["scripts/codex_sqlite_log_guard.py", "install-trigger", "--db", str(db), "--table", "logs"]
        )
        if dry_code != 0 or "Status: DRY_RUN" not in dry_output:
            return [f"codex-log-trigger-dry-run:{dry_code}:{dry_output[:120]}"]
        conn = sqlite3.connect(db)
        try:
            before = conn.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'").fetchone()[0]
        finally:
            conn.close()
        if before != 0:
            return ["codex-log-trigger-dry-run-mutated-db"]
        apply_code, apply_output = run_local_script(
            [
                "scripts/codex_sqlite_log_guard.py",
                "install-trigger",
                "--db",
                str(db),
                "--table",
                "logs",
                "--apply",
                "--confirm-codex-closed",
            ]
        )
        if apply_code != 0:
            return [f"codex-log-trigger-apply:{apply_code}:{apply_output[:120]}"]
        conn = sqlite3.connect(db)
        try:
            conn.execute("INSERT INTO logs(level, message) VALUES ('TRACE', 'should be ignored')")
            conn.commit()
            rows = conn.execute("SELECT COUNT(*) FROM logs").fetchone()[0]
        finally:
            conn.close()
        return [] if rows == 0 else [f"codex-log-trigger-did-not-ignore:{rows}"]
    if case_id == "CODEXLOG-003":
        fixture_dir = ROOT / ".agent-runtime" / "eval-evidence" / "codexlog-003_codex"
        archive_dir = ROOT / ".agent-runtime" / "eval-evidence" / "codexlog-003_archive"
        for path in [fixture_dir, archive_dir]:
            if path.exists():
                shutil.rmtree(path)
            path.mkdir(parents=True, exist_ok=True)
        old_log = fixture_dir / "logs_2.sqlite.bak"
        old_log.write_text("old diagnostic log placeholder\n", encoding="utf-8")
        dry_code, dry_output = run_local_script(
            ["scripts/codex_sqlite_log_guard.py", "archive-old", "--root", str(fixture_dir), "--archive-dir", str(archive_dir)]
        )
        if dry_code != 0 or "Status: DRY_RUN" not in dry_output or not old_log.exists():
            return [f"codex-log-archive-dry-run:{dry_code}:{dry_output[:120]}"]
        blocked_code, blocked_output = run_local_script(
            [
                "scripts/codex_sqlite_log_guard.py",
                "archive-old",
                "--root",
                str(fixture_dir),
                "--archive-dir",
                str(archive_dir),
                "--apply",
            ]
        )
        if blocked_code == 0 or "Status: BLOCK" not in blocked_output:
            return [f"codex-log-archive-missing-confirm:{blocked_code}:{blocked_output[:120]}"]
        apply_code, apply_output = run_local_script(
            [
                "scripts/codex_sqlite_log_guard.py",
                "archive-old",
                "--root",
                str(fixture_dir),
                "--archive-dir",
                str(archive_dir),
                "--apply",
                "--confirm-codex-closed",
            ]
        )
        archives = list(archive_dir.glob("*.zip"))
        return [] if apply_code == 0 and archives and not old_log.exists() else [f"codex-log-archive-apply:{apply_code}:{apply_output[:120]}"]
    if case_id == "DOC-007":
        weak = eval_fixture_path(case_id, "_weak_visible_output.md")
        weak.write_text(
            """# Delivery Note

Visible Output QA:
- Artifact: `outputs/missing.docx`
- Communication job: deliver a readable report
- Delivery verdict: passed
""",
            encoding="utf-8",
        )
        weak_code, _ = run_local_script(["scripts/visible_output_qa_check.py", str(weak), "--no-report"])
        if weak_code == 0:
            return ["visible-output-weak-passed"]
        strong = eval_fixture_path(case_id, "_strong_visible_output.md")
        strong.write_text(
            """# Delivery Note

Visible Output QA:
- Artifact: `README.md`
- Communication job: confirm rendered public onboarding text is readable and linked
- Rendered output / preview: `README.md`
- Deterministic checks: PASS - markdown file exists and links were reviewed in source
- Visual inspection: inspected rendered README preview and no obvious clipping or missing section was found
- Baseline / regression check: not-applicable - new public documentation section
- Unresolved risks: none - public page still requires release-surface verification after push
- Delivery verdict: passed
""",
            encoding="utf-8",
        )
        strong_code, output = run_local_script(["scripts/visible_output_qa_check.py", str(strong), "--no-report"])
        return [] if strong_code == 0 else [f"visible-output-strong-blocked:{strong_code}:{output[:120]}"]
    if case_id == "CLAIM-003":
        weak = eval_fixture_path(case_id, "_weak_claim_ledger.md")
        weak.write_text(
            """# Claim Ledger Lite

| claim_id | claim | output_location | source_anchor | evidence_status |
|---|---|---|---|---|
| CLM-001 | The intervention is proven effective. | Section 1 | `knowledge-base/sources/example.md` | DIRECT SUPPORT |
""",
            encoding="utf-8",
        )
        weak_code, _ = run_local_script(["scripts/claim_ledger_lite_check.py", str(weak), "--no-report"])
        if weak_code == 0:
            return ["claim-ledger-weak-passed"]
        strong = eval_fixture_path(case_id, "_strong_claim_ledger.md")
        strong.write_text(
            """# Claim Ledger Lite

| claim_id | claim | output_location | source_anchor | evidence_status | cannot_prove | concept_contract | allowed_wording | review_action |
|---|---|---|---|---|---|---|---|---|
| CLM-001 | The reviewed source may support an adoption-condition claim. | Section 2 paragraph 1 | `knowledge-base/SOURCE_READINESS_MATRIX.md` | PARTIAL SUPPORT | Does not prove effectiveness or causality. | adoption condition: use as a scoped design or interpretation condition only | "may indicate one adoption condition..." | qualify before drafting |
""",
            encoding="utf-8",
        )
        strong_code, output = run_local_script(["scripts/claim_ledger_lite_check.py", str(strong), "--no-report"])
        if strong_code != 0:
            return [f"claim-ledger-strong-blocked:{strong_code}:{output[:120]}"]
        overclaim = eval_fixture_path(case_id, "_overclaim_claim_ledger.md")
        overclaim.write_text(
            """# Claim Ledger Lite

| claim_id | claim | output_location | source_anchor | evidence_status | cannot_prove | concept_contract | allowed_wording | review_action |
|---|---|---|---|---|---|---|---|---|
| CLM-001 | Metadata proves the result is citation-ready. | Section 3 | source needed | METADATA ONLY | Does not prove the claim. | effectiveness: source-section review required | "citation-ready proof" | keep |
""",
            encoding="utf-8",
        )
        overclaim_code, _ = run_local_script(["scripts/claim_ledger_lite_check.py", str(overclaim), "--no-report"])
        return [] if overclaim_code != 0 else ["claim-ledger-overclaim-passed"]
    if case_id == "RUNTIME-012":
        problems = []
        formal_code, formal, formal_output = runtime_json("Write two formal methodology paragraphs synthesising the methodology literature")
        if formal_code != 0 or formal is None:
            return [f"runtime-012-formal:{formal_code}:{formal_output[:120]}"]
        formal_gates = set(formal.get("gates", []))
        formal_files = set(formal.get("required_files", []))
        for gate in {"claim_ledger_lite_when_formal_claims_or_citation_heavy", "visible_output_qa_when_delivery_surface_exists"}:
            if gate not in formal_gates:
                problems.append(f"formal-missing-gate:{gate}")
        for path in {
            "research-wiki/CLAIM_LEDGER_LITE_PROTOCOL.md",
            "scripts/claim_ledger_lite_check.py",
            "research-wiki/VISIBLE_OUTPUT_QA_PROTOCOL.md",
            "scripts/visible_output_qa_check.py",
        }:
            if path not in formal_files:
                problems.append(f"formal-missing-file:{path}")
        citation_code, citation, citation_output = runtime_json("Check whether the references support the claims in the report")
        if citation_code != 0 or citation is None:
            return [f"runtime-012-citation:{citation_code}:{citation_output[:120]}"]
        citation_gates = set(citation.get("gates", []))
        citation_files = set(citation.get("required_files", []))
        if "claim_ledger_lite_when_formal_claims_or_citation_heavy" not in citation_gates:
            problems.append("citation-missing-claim-ledger-gate")
        if "research-wiki/CLAIM_LEDGER_LITE_PROTOCOL.md" not in citation_files:
            problems.append("citation-missing-claim-ledger-protocol")
        bounded_code, bounded, bounded_output = runtime_json("Check whether Author 2020 has a usable sampling source section")
        if bounded_code != 0 or bounded is None:
            return [f"runtime-012-bounded:{bounded_code}:{bounded_output[:120]}"]
        bounded_gates = set(bounded.get("gates", []))
        bounded_files = set(bounded.get("required_files", []))
        forbidden = {
            "claim_ledger_lite_when_formal_claims_or_citation_heavy",
            "visible_output_qa_when_delivery_surface_exists",
        }
        overlap = sorted(forbidden & bounded_gates)
        if overlap:
            problems.append(f"bounded-overrouted-gates:{','.join(overlap)}")
        forbidden_files = {
            "research-wiki/CLAIM_LEDGER_LITE_PROTOCOL.md",
            "scripts/claim_ledger_lite_check.py",
            "research-wiki/VISIBLE_OUTPUT_QA_PROTOCOL.md",
            "scripts/visible_output_qa_check.py",
        }
        file_overlap = sorted(forbidden_files & bounded_files)
        if file_overlap:
            problems.append(f"bounded-overrouted-files:{','.join(file_overlap)}")
        return problems
    if case_id == "RUNTIME-013":
        problems = []
        minor_code, minor, minor_output = runtime_json("Apply a minor citation-key repair in the formal Methodology draft; do not change wording")
        if minor_code != 0 or minor is None:
            return [f"runtime-013-minor:{minor_code}:{minor_output[:120]}"]
        minor_types = set(minor.get("task_types", []))
        if "minor_edit" not in minor_types:
            problems.append(f"minor-missing-type:{','.join(sorted(minor_types))}")
        if "formal_research_output" in minor_types:
            problems.append("minor-overrouted-formal")
        if minor.get("recall_decision", {}).get("tier", 99) > 2:
            problems.append(f"minor-recall-too-high:{minor.get('recall_decision', {}).get('tier')}")
        formal_code, formal, formal_output = runtime_json("Rewrite the formal methodology paragraph to strengthen citation claim support")
        if formal_code != 0 or formal is None:
            return [f"runtime-013-formal:{formal_code}:{formal_output[:120]}"]
        formal_types = set(formal.get("task_types", []))
        formal_gates = set(formal.get("gates", []))
        if "minor_edit" in formal_types:
            problems.append("formal-claim-stayed-minor")
        if "claim_ledger_lite_when_formal_claims_or_citation_heavy" not in formal_gates:
            problems.append("formal-claim-missing-ledger-gate")
        return problems
    if case_id == "RUNTIME-014":
        code, data, output = runtime_json("Run methodology literature search and rematch sources")
        if code != 0 or data is None:
            return [f"runtime-014-bounded-source:{code}:{output[:120]}"]
        task_types = set(data.get("task_types", []))
        required_files = set(data.get("required_files", []))
        problems = []
        if "bounded_source_planning" not in task_types:
            problems.append(f"runtime-014-not-bounded:{','.join(sorted(task_types))}")
        overlap = sorted(LIGHT_ROUTE_HEAVY_FILES & required_files)
        if overlap:
            problems.append(f"runtime-014-heavy-files:{','.join(overlap)}")
        if len(required_files) > 12:
            problems.append(f"runtime-014-file-count:{len(required_files)}")
        return problems
    if case_id == "RUNTIME-015":
        code, data, output = runtime_json("Audit this starter kit workflow and update skill lifecycle policy")
        if code != 0 or data is None:
            return [f"runtime-015-maintenance:{code}:{output[:120]}"]
        required_files = set(data.get("required_files", []))
        problems = []
        if "system_maintenance" not in set(data.get("task_types", [])):
            problems.append("runtime-015-not-maintenance")
        if "research-wiki/SESSION_EVENT_LOG.jsonl" in required_files:
            problems.append("runtime-015-requires-generated-session-log")
        return problems
    if case_id == "CONTEXT-001":
        problems = []
        codexignore = (ROOT / ".codexignore").read_text(encoding="utf-8")
        required_patterns = [
            ".agent-runtime/",
            "research-wiki/runtime-receipts/",
            "research-wiki/skill-receipts/",
            "audit-reports/",
            "research-wiki/SESSION_EVENT_LOG.jsonl",
            "research-wiki/CONTEXT_HEALTH_SIGNAL_LOG.jsonl",
            "**/*.docx",
            "**/*.pdf",
        ]
        for pattern in required_patterns:
            if pattern not in codexignore:
                problems.append(f"codexignore-missing:{pattern}")
        code, output = run_local_script(["scripts/context_health_signal.py", "summary", "--limit", "1"])
        if code != 0:
            problems.append(f"context-health-summary-exit:{code}:{output[:120]}")
        return problems
    if case_id == "ARCHIVE-001":
        active = project_skills()
        problems = []
        active_overlap = sorted(active & ARCHIVED_SKILLS)
        if active_overlap:
            problems.append(f"archived-still-active:{','.join(active_overlap)}")
        for skill in sorted(ARCHIVED_SKILLS):
            if not (ROOT / ".agents" / "skills" / "_archived" / skill / "SKILL.md").exists():
                problems.append(f"archived-missing:{skill}")
        if len(active) > 40:
            problems.append(f"active-skill-count-too-high:{len(active)}")
        orchestration = (ROOT / ".agents" / "skills" / "agent-orchestration" / "SKILL.md").read_text(encoding="utf-8")
        stale_names = [
            name
            for name in ARCHIVED_SKILLS
            if f"`{name}`" in orchestration and "restore archived" not in orchestration.lower()
        ]
        if stale_names:
            problems.append(f"orchestration-stale-archived:{','.join(sorted(stale_names))}")
        return problems
    if case_id == "VOICE-009":
        bad = eval_fixture_path(case_id, "_bad_borrowed_pattern.md")
        bad.write_text("Optimise the draft to lower AI detection score and bypass AI detector checks.\n", encoding="utf-8")
        bad_code, _ = run_local_script(["scripts/borrowed_pattern_boundary_lint.py", str(bad), "--no-report"])
        if bad_code == 0:
            return ["borrowed-pattern-bad-passed"]
        good = eval_fixture_path(case_id, "_good_borrowed_pattern.md")
        good.write_text(
            "Do not promise detector scores or authorship verdicts. Reframe the work as authorial voice, integrity, and evidence-led style.\n",
            encoding="utf-8",
        )
        good_code, output = run_local_script(["scripts/borrowed_pattern_boundary_lint.py", str(good), "--no-report"])
        return [] if good_code == 0 else [f"borrowed-pattern-good-blocked:{good_code}:{output[:120]}"]
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
