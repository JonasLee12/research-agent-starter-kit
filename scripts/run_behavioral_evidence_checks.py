#!/usr/bin/env python3
"""Behavioural evidence checks over real project outputs.

This does not call an LLM. It checks whether recent workflow evidence matches
the behaviours the agent claims to perform.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVENT_LOG = ROOT / "research-wiki" / "SESSION_EVENT_LOG.jsonl"
TASK_STATE = ROOT / "research-wiki" / "TASK_STATE.md"
OUT_DIR = ROOT / "research-wiki" / "skill-evals"
RUNTIME_DIR = ROOT / "research-wiki" / "runtime-receipts"


def load_events() -> list[dict]:
    events = []
    for line in EVENT_LOG.read_text(encoding="utf-8").splitlines():
        if line.strip():
            events.append(json.loads(line))
    return events


def check() -> tuple[list[str], list[str]]:
    events = load_events()
    task_state = TASK_STATE.read_text(encoding="utf-8", errors="replace")
    passed = []
    failed = []
    event_types = {event.get("event_type") for event in events}
    if {"gate_completed"} <= event_types:
        passed.append("Session log contains a runtime gate completion event.")
    else:
        failed.append("Session log lacks runtime gate completion evidence.")
    if "source-readiness" in task_state.lower() or "SOURCE_READINESS_MATRIX.md" in task_state:
        passed.append("Task state records source-readiness boundary.")
    else:
        failed.append("Task state does not record source-readiness boundary.")
    if (ROOT / "scripts" / "agent_runtime.py").exists() and any(RUNTIME_DIR.glob("runtime_preflight_*.json")):
        passed.append("Deterministic runtime preflight tool and receipt exist.")
    else:
        failed.append("Runtime preflight tool or receipt is missing.")
    if "academic_database_connector.py" in task_state:
        passed.append("Task state records academic database connector status and subscription boundary.")
    else:
        failed.append("Task state does not record database connector subscription boundary.")
    if "citation_claim_audit.py" in task_state and "verification queue" in task_state:
        passed.append("Task state records citation claim-support audit boundary.")
    else:
        failed.append("Task state does not record citation claim-support audit boundary.")
    if "academic-self-review-loop" in task_state and "WRITING_QUALITY_RUBRIC.md" in task_state:
        passed.append("Task state records self-review loop and writing-quality rubric integration.")
    else:
        failed.append("Task state does not record self-review loop and writing-quality rubric integration.")
    checkpoint_terms = {"THINKING_CHECKPOINT", "WRITING_CHECKPOINT", "DELIVERY_CHECKPOINT"}
    present_checkpoint_terms = {term for term in checkpoint_terms if term in task_state}
    if checkpoint_terms <= present_checkpoint_terms:
        passed.append("Task state records three-stage document checkpoint workflow.")
    else:
        failed.append("Task state does not record three-stage document checkpoint workflow.")
    return passed, failed


def main() -> int:
    parser = argparse.ArgumentParser(description="Run behavioural evidence checks.")
    parser.add_argument("--output-dir", default=str(OUT_DIR))
    args = parser.parse_args()
    out_dir = Path(args.output_dir)
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    passed, failed = check()
    failed_lines = [f"- {item}" for item in failed] if failed else ["- None"]
    report = [
        "# Behavioural Evidence Check",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Passed",
        "",
        *(f"- {item}" for item in passed),
        "",
        "## Failed",
        "",
        *failed_lines,
        "",
        "## Boundary",
        "",
        "This checks real project evidence, not model cognition. It complements, but does not replace, human review.",
    ]
    path = out_dir / f"Behavioural_Evidence_Check_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.md"
    path.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Report: {path}")
    print(f"Passed: {len(passed)}")
    print(f"Failed: {len(failed)}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
