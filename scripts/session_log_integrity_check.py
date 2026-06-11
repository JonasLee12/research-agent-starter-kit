#!/usr/bin/env python3
"""Check research-agent session event log integrity.

This checker focuses on auditability rather than substantive research quality.
It blocks malformed JSONL, illegal window labels, runtime/window mismatches,
and unclosed runtime sessions. Older schema-light events are reported as
warnings so the checker can be used on historical logs without rewriting
unrelated evidence.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG = ROOT / "research-wiki" / "SESSION_EVENT_LOG.jsonl"
DEFAULT_RUNTIME_DIR = ROOT / "research-wiki" / "runtime-receipts"
DEFAULT_REPORT_DIR = ROOT / "audit-reports" / "session-log-integrity"
LEGAL_WINDOWS = {"Production", "Maintenance"}
CORE_FIELDS = {"timestamp", "run_id", "window", "event_type", "status", "evidence", "risk"}
RECOMMENDED_FIELDS = {"skill", "file"}
SESSION_START = "session_start"
SESSION_END = "session_end"


@dataclass
class Issue:
    severity: str
    line: int
    run_id: str
    message: str


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def parse_timestamp(text: str) -> datetime:
    normalised = text.replace("Z", "+00:00")
    if len(normalised) >= 5 and normalised[-5] in {"+", "-"} and normalised[-3] != ":":
        normalised = f"{normalised[:-2]}:{normalised[-2:]}"
    value = datetime.fromisoformat(normalised)
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def load_runtime_windows(runtime_dir: Path) -> dict[str, set[str]]:
    windows: dict[str, set[str]] = {}
    if not runtime_dir.exists():
        return windows
    for path in sorted(runtime_dir.glob("runtime_preflight_*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        run_id = data.get("run_id")
        window = data.get("window")
        if run_id and window:
            windows.setdefault(run_id, set()).add(window)
    return windows


def load_events(log_path: Path) -> tuple[list[dict], list[Issue]]:
    events: list[dict] = []
    issues: list[Issue] = []
    if not log_path.exists():
        return events, [Issue("BLOCK", 0, "-", f"Log file not found: {rel(log_path)}")]
    for line_no, line in enumerate(log_path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            issues.append(Issue("BLOCK", line_no, "-", f"Invalid JSON: {exc}"))
            continue
        event["_line"] = line_no
        events.append(event)
    return events, issues


def check_events(events: list[dict], runtime_windows: dict[str, set[str]], strict_time: bool) -> list[Issue]:
    issues: list[Issue] = []
    session_counts: dict[str, list[int]] = {}
    last_by_run: dict[str, tuple[datetime, int]] = {}
    for event in events:
        line = int(event.get("_line", 0))
        run_id = str(event.get("run_id", "-"))
        missing_core = sorted(CORE_FIELDS - set(event))
        if missing_core:
            issues.append(Issue("BLOCK", line, run_id, f"Missing core fields: {', '.join(missing_core)}"))
        missing_recommended = sorted(RECOMMENDED_FIELDS - set(event))
        if missing_recommended:
            issues.append(Issue("WARN", line, run_id, f"Missing recommended fields: {', '.join(missing_recommended)}"))

        window = event.get("window")
        if window not in LEGAL_WINDOWS:
            issues.append(Issue("BLOCK", line, run_id, f"Illegal window label: {window!r}"))
        if run_id in runtime_windows and window not in runtime_windows[run_id]:
            expected = ", ".join(sorted(runtime_windows[run_id]))
            issues.append(Issue("BLOCK", line, run_id, f"Window {window!r} does not match runtime receipt window(s): {expected}"))

        timestamp_text = event.get("timestamp")
        parsed: datetime | None = None
        if timestamp_text:
            try:
                parsed = parse_timestamp(str(timestamp_text))
            except ValueError as exc:
                issues.append(Issue("BLOCK", line, run_id, f"Unparseable timestamp {timestamp_text!r}: {exc}"))
        if parsed and run_id != "-":
            previous = last_by_run.get(run_id)
            if previous and parsed < previous[0]:
                severity = "BLOCK" if strict_time else "WARN"
                issues.append(
                    Issue(
                        severity,
                        line,
                        run_id,
                        f"Timestamp moved backwards within run_id; previous line {previous[1]} is later.",
                    )
                )
            last_by_run[run_id] = (parsed, line)

        event_type = event.get("event_type")
        if event_type in {SESSION_START, SESSION_END} and run_id != "-":
            counts = session_counts.setdefault(run_id, [0, 0])
            if event_type == SESSION_START:
                counts[0] += 1
            else:
                counts[1] += 1

    for run_id, (starts, ends) in sorted(session_counts.items()):
        if starts > ends:
            issues.append(Issue("BLOCK", 0, run_id, f"Unpaired session_start: starts={starts}, ends={ends}"))
        elif ends > starts:
            issues.append(Issue("WARN", 0, run_id, f"Extra session_end without matching start in current log scope: starts={starts}, ends={ends}"))
    return issues


def render_report(log_path: Path, runtime_dir: Path, events: list[dict], issues: list[Issue]) -> str:
    block_count = sum(1 for issue in issues if issue.severity == "BLOCK")
    warn_count = sum(1 for issue in issues if issue.severity == "WARN")
    status = "BLOCK" if block_count else "PASS_WITH_WARNINGS" if warn_count else "PASS"
    lines = [
        "# Session Event Log Integrity Check",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"Status: `{status}`",
        f"Log: `{rel(log_path)}`",
        f"Runtime receipt directory: `{rel(runtime_dir)}`",
        "",
        "## Summary",
        "",
        f"- Events checked: {len(events)}",
        f"- Blocking issues: {block_count}",
        f"- Warnings: {warn_count}",
        "",
        "## Checks",
        "",
        "- JSONL parseability",
        "- Legal `window` labels",
        "- Event `window` alignment with runtime preflight receipt where a runtime receipt exists",
        "- `session_start` has a corresponding `session_end` for each run id",
        "- Timestamp parseability and per-run monotonic order",
        "",
        "## Issues",
        "",
        "| Severity | Line | Run ID | Issue |",
        "|---|---:|---|---|",
    ]
    if issues:
        for issue in issues:
            run_id = issue.run_id.replace("|", "\\|")
            message = issue.message.replace("|", "\\|")
            lines.append(f"| {issue.severity} | {issue.line or '-'} | `{run_id}` | {message} |")
    else:
        lines.append("| PASS | - | - | No issues found. |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This checker verifies event-log integrity for auditability. It does not prove that the referenced Production or Maintenance task was substantively sufficient.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check SESSION_EVENT_LOG.jsonl integrity.")
    parser.add_argument("--log", default=str(DEFAULT_LOG))
    parser.add_argument("--runtime-dir", default=str(DEFAULT_RUNTIME_DIR))
    parser.add_argument("--output", default="")
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--no-report", action="store_true")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on blocking issues.")
    parser.add_argument("--strict-time", action="store_true", help="Treat per-run timestamp regressions as blocking.")
    args = parser.parse_args()

    log_path = Path(args.log)
    runtime_dir = Path(args.runtime_dir)
    if not log_path.is_absolute():
        log_path = ROOT / log_path
    if not runtime_dir.is_absolute():
        runtime_dir = ROOT / runtime_dir

    events, parse_issues = load_events(log_path)
    issues = parse_issues + check_events(events, load_runtime_windows(runtime_dir), args.strict_time)
    block_count = sum(1 for issue in issues if issue.severity == "BLOCK")
    warn_count = sum(1 for issue in issues if issue.severity == "WARN")
    status = "BLOCK" if block_count else "PASS_WITH_WARNINGS" if warn_count else "PASS"
    report = render_report(log_path, runtime_dir, events, issues)

    if args.write_report and not args.no_report:
        output = Path(args.output) if args.output else DEFAULT_REPORT_DIR / f"Session_Log_Integrity_{datetime.now(timezone.utc).strftime('%Y-%m-%d_%H%M%S')}.md"
        if not output.is_absolute():
            output = ROOT / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report, encoding="utf-8")
        print(f"Report: {output}")
    elif not args.no_report:
        print(report)

    print(f"Status: {status}")
    print(f"Events checked: {len(events)}")
    print(f"Blocking issues: {block_count}")
    print(f"Warnings: {warn_count}")
    return 1 if args.strict and block_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
