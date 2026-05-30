#!/usr/bin/env python3
"""Run a privacy-gated Claude Code independent review for research artifacts."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "audit-reports" / "claude-reviews"
SESSION_LOG = ROOT / "research-wiki" / "SESSION_EVENT_LOG.jsonl"

SENSITIVE_PATH_PATTERNS = [
    r"raw",
    r"transcript",
    r"recording",
    r"signed",
    r"consent",
    r"participant-contact",
    r"participant_data",
    r"private",
]

SENSITIVE_TEXT_PATTERNS = [
    r"\bparticipant\b",
    r"\binterview transcript\b",
    r"\brecording\b",
    r"\bconsent\b",
    r"\bwithdrawal\b",
    r"\banonym",
    r"\bconfidential",
    r"\bdata storage\b",
    r"\bemail\b",
    r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}",
]


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return slug[:80] or "claude-review"


def relative_or_abs(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def append_event(event: dict) -> None:
    SESSION_LOG.parent.mkdir(parents=True, exist_ok=True)
    with SESSION_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def scan_sensitive(target: Path, text: str) -> list[str]:
    findings: list[str] = []
    path_text = str(target).lower()
    for pattern in SENSITIVE_PATH_PATTERNS:
        if re.search(pattern, path_text, flags=re.I):
            findings.append(f"path matches `{pattern}`")
    for pattern in SENSITIVE_TEXT_PATTERNS:
        if re.search(pattern, text, flags=re.I):
            findings.append(f"text matches `{pattern}`")
    return findings


def build_prompt(target: Path, text: str, review_question: str) -> str:
    return f"""You are an independent reviewer for a local research-agent project.

Review task:
{review_question}

Review boundaries:
- Judge only the current artifact below.
- Do not assume prior revision history.
- Do not invent citations, source support, project facts, reviewer feedback, participants, dates, or institutional requirements.
- Treat source readiness, compliance status, and requirement/rubric evidence as local-project matters that must be verified separately.
- Your feedback is advisory. It should become a revision queue, not evidence.

Return concise Markdown with:
1. Readiness judgement
2. Top findings by severity
3. Evidence, logic, privacy, or maintenance risks
4. Concrete revision queue
5. Questions to verify locally

Artifact path:
{relative_or_abs(target)}

Artifact:
```text
{text}
```
"""


def run_claude(prompt: str, model: str | None, effort: str | None, timeout_seconds: int) -> subprocess.CompletedProcess[str]:
    command = ["claude", "-p", "--tools", "", "--no-session-persistence"]
    if model:
        command.extend(["--model", model])
    if effort:
        command.extend(["--effort", effort])
    return subprocess.run(command, input=prompt, text=True, capture_output=True, cwd=ROOT, timeout=timeout_seconds)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a safe Claude Code independent review.")
    parser.add_argument("target", help="Markdown/text file to review.")
    parser.add_argument("--review-question", default="Review this artifact for argument quality, evidence risks, clarity, privacy risks, and concrete revision priorities.")
    parser.add_argument("--output", help="Optional output report path.")
    parser.add_argument("--max-chars", type=int, default=45000, help="Maximum characters sent to Claude Code.")
    parser.add_argument("--allow-sensitive", action="store_true", help="Allow review despite sensitive scan findings.")
    parser.add_argument("--override-reason", help="Required when --allow-sensitive is used.")
    parser.add_argument("--model", help="Optional Claude model alias or full model name.")
    parser.add_argument("--effort", choices=["low", "medium", "high", "xhigh", "max"], default="high")
    parser.add_argument("--timeout-seconds", type=int, default=180, help="Maximum seconds to wait for Claude Code before writing a failed review report.")
    args = parser.parse_args()

    target = Path(args.target).expanduser()
    if not target.is_absolute():
        target = (ROOT / target).resolve()
    if not target.exists():
        print(f"ERROR: target not found: {target}", file=sys.stderr)
        return 2
    if not shutil.which("claude"):
        print("ERROR: `claude` command not found on PATH.", file=sys.stderr)
        return 2
    if args.allow_sensitive and not args.override_reason:
        print("ERROR: --override-reason is required with --allow-sensitive.", file=sys.stderr)
        return 2

    text = target.read_text(encoding="utf-8", errors="replace")
    truncated = False
    if len(text) > args.max_chars:
        text = text[: args.max_chars]
        truncated = True

    sensitive_findings = scan_sensitive(target, text)
    if sensitive_findings and not args.allow_sensitive:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        report_path = REPORT_DIR / f"Claude_Review_BLOCKED_{slugify(target.stem)}_{stamp}.md"
        report = [
            "# Claude Independent Review Blocked",
            "",
            f"Generated: {datetime.now().isoformat(timespec='seconds')}",
            f"Target: `{relative_or_abs(target)}`",
            "Status: `BLOCKED`",
            "",
            "## Sensitive Findings",
            "",
        ]
        report.extend(f"- {finding}" for finding in sensitive_findings)
        report.extend(
            [
                "",
                "## Boundary",
                "",
                "Claude review was not run. Use anonymised/sanitised material or rerun only with explicit user approval and `--allow-sensitive --override-reason`.",
                "",
            ]
        )
        report_path.write_text("\n".join(report), encoding="utf-8")
        print("Status: BLOCKED")
        print(f"Report: {report_path}")
        return 1

    prompt = build_prompt(target, text, args.review_question)
    timeout_error = ""
    try:
        result = run_claude(prompt, args.model, args.effort, args.timeout_seconds)
    except subprocess.TimeoutExpired as exc:
        timeout_error = f"Claude Code timed out after {args.timeout_seconds} seconds."
        stdout = exc.stdout.decode("utf-8", errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = exc.stderr.decode("utf-8", errors="replace") if isinstance(exc.stderr, bytes) else (exc.stderr or timeout_error)
        result = subprocess.CompletedProcess(args=exc.cmd, returncode=124, stdout=stdout, stderr=stderr)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    if args.output:
        report_path = Path(args.output).expanduser()
        if not report_path.is_absolute():
            report_path = (ROOT / report_path).resolve()
    else:
        stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        report_path = REPORT_DIR / f"Claude_Independent_Review_{slugify(target.stem)}_{stamp}.md"

    status = "PASS" if result.returncode == 0 else "FAILED"
    report = [
        "# Claude Independent Review",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Target: `{relative_or_abs(target)}`",
        f"Status: `{status}`",
        f"Claude command: `claude -p --tools \"\" --no-session-persistence --effort {args.effort}`",
        f"Input truncated: `{str(truncated).lower()}`",
        "",
        "## Privacy Gate",
        "",
        f"- Sensitive findings: {len(sensitive_findings)}",
        f"- Sensitive override: {str(args.allow_sensitive).lower()}",
    ]
    if args.override_reason:
        report.append(f"- Override reason: {args.override_reason}")
    report.extend(["", "## Review Output", "", result.stdout.strip() or "(no stdout)"])
    if result.stderr.strip():
        report.extend(["", "## stderr", "", "```text", result.stderr.strip(), "```"])
    if timeout_error:
        report.extend(["", "## Timeout", "", timeout_error])
    report.extend(
        [
            "",
            "## Boundary",
            "",
            "This Claude Code review is advisory. It does not prove source support, compliance readiness, citation correctness, or rubric/requirement compliance.",
            "",
        ]
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(report), encoding="utf-8")

    append_event(
        {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "run_id": f"{datetime.now().strftime('%Y-%m-%d')}-claude-independent-review",
            "window": "Maintenance",
            "event_type": "tool_run",
            "status": "completed" if status == "PASS" else "failed",
            "skill": "cognitive-frameworks",
            "file": relative_or_abs(report_path),
            "evidence": f"Claude Code independent review wrapper ran for {relative_or_abs(target)} with status {status}.",
            "risk": "low" if status == "PASS" else "medium",
        }
    )

    print(f"Status: {status}")
    print(f"Report: {report_path}")
    return 0 if result.returncode == 0 else result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
