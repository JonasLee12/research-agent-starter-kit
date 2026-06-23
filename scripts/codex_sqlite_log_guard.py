#!/usr/bin/env python3
"""Guard against runaway Codex SQLite diagnostic log growth.

This script is a local safety helper for the Codex `logs_*.sqlite` / WAL growth
failure mode reported by users. It is deliberately conservative:

- scan and monitor are read-only;
- trigger installation is opt-in, table-specific, and dry-run by default;
- WAL checkpointing and log archiving require explicit `--apply`;
- write actions require `--confirm-codex-closed` unless the user explicitly
  overrides the safety check.

The tool targets Codex diagnostic log databases only. It must not be used on
project state, conversation history, memory, goal, or arbitrary SQLite files.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sqlite3
import subprocess
import time
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT_DIR = ROOT / "audit-reports" / "codex-sqlite-log-guard"
DEFAULT_ARCHIVE_DIR = Path.home() / "CodexLogGuardArchives"
LOG_DB_RE = re.compile(r"^logs(?:_\d+)?\.sqlite$", re.IGNORECASE)
LOG_SIDE_RE = re.compile(r"^logs(?:_\d+)?\.sqlite(?:-wal|-shm)?(?:\.(?:bak|old|backup))?$", re.IGNORECASE)
GUARD_TRIGGER_PREFIX = "codex_log_guard_block_"


@dataclass
class Candidate:
    db_path: Path
    db_bytes: int
    wal_bytes: int
    shm_bytes: int
    is_codex_path: bool

    @property
    def total_bytes(self) -> int:
        return self.db_bytes + self.wal_bytes + self.shm_bytes

    @property
    def wal_path(self) -> Path:
        return Path(f"{self.db_path}-wal")

    @property
    def shm_path(self) -> Path:
        return Path(f"{self.db_path}-shm")


def bytes_to_mb(value: int) -> float:
    return value / (1024 * 1024)


def compact_path(path: Path) -> str:
    try:
        return "~/" + str(path.resolve().relative_to(Path.home().resolve()))
    except ValueError:
        try:
            return str(path.resolve().relative_to(ROOT))
        except ValueError:
            return str(path)


def resolve_path(value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = ROOT / path
    return path


def file_size(path: Path) -> int:
    try:
        return path.stat().st_size
    except FileNotFoundError:
        return 0


def common_codex_roots() -> list[Path]:
    roots = [
        Path.home() / ".codex",
        Path.home() / ".codex-work",
        Path.home() / ".codex-personal",
        Path.home() / "Library" / "Application Support" / "Codex",
        Path.home() / "Library" / "Application Support" / "OpenAI" / "Codex",
    ]
    for env_name in ("APPDATA", "LOCALAPPDATA", "XDG_CONFIG_HOME"):
        value = os.environ.get(env_name)
        if value:
            base = Path(value).expanduser()
            roots.extend([base / "Codex", base / "OpenAI" / "Codex", base / "codex"])
    return sorted({path for path in roots if path.exists()})


def path_looks_like_codex(path: Path) -> bool:
    lowered = [part.lower() for part in path.parts]
    return any("codex" in part for part in lowered)


def candidate_from_db(path: Path) -> Candidate:
    return Candidate(
        db_path=path,
        db_bytes=file_size(path),
        wal_bytes=file_size(Path(f"{path}-wal")),
        shm_bytes=file_size(Path(f"{path}-shm")),
        is_codex_path=path_looks_like_codex(path),
    )


def find_candidates(roots: list[Path], dbs: list[Path], include_non_codex: bool) -> list[Candidate]:
    paths: set[Path] = set()
    for db in dbs:
        paths.add(db)
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("logs*.sqlite"):
            if path.is_file() and LOG_DB_RE.match(path.name):
                paths.add(path)
    candidates = [candidate_from_db(path) for path in sorted(paths)]
    if include_non_codex:
        return candidates
    return [candidate for candidate in candidates if candidate.is_codex_path]


def sqlite_readonly(db_path: Path) -> sqlite3.Connection:
    uri = db_path.resolve().as_uri() + "?mode=ro"
    return sqlite3.connect(uri, uri=True)


def list_tables(db_path: Path) -> list[str]:
    conn = sqlite_readonly(db_path)
    try:
        return [str(row[0]) for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    finally:
        conn.close()


def list_guard_triggers(db_path: Path) -> list[str]:
    conn = sqlite_readonly(db_path)
    try:
        rows = conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='trigger' AND name LIKE ?
            ORDER BY name
            """,
            (f"{GUARD_TRIGGER_PREFIX}%",),
        ).fetchall()
    finally:
        conn.close()
    return [str(row[0]) for row in rows]


def quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def trigger_name(table: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_]+", "_", table).strip("_") or "logs"
    return f"{GUARD_TRIGGER_PREFIX}{safe}_insert"


def trigger_sql(table: str) -> str:
    return (
        f"CREATE TRIGGER IF NOT EXISTS {quote_identifier(trigger_name(table))}\n"
        f"BEFORE INSERT ON {quote_identifier(table)}\n"
        "BEGIN\n"
        "  SELECT RAISE(IGNORE);\n"
        "END;"
    )


def drop_trigger_sql(name: str) -> str:
    return f"DROP TRIGGER IF EXISTS {quote_identifier(name)};"


def require_safe_write(args: argparse.Namespace, db_path: Path | None = None) -> tuple[bool, str]:
    if not getattr(args, "confirm_codex_closed", False) and not getattr(args, "allow_running", False):
        return False, "write actions require --confirm-codex-closed or --allow-running"
    if db_path is not None and not path_looks_like_codex(db_path) and not getattr(args, "force", False):
        return False, "target path does not look like a Codex log path; use --force only after manual verification"
    return True, "ok"


def render_scan_report(candidates: list[Candidate], status: str, issues: list[str]) -> str:
    lines = [
        "# Codex SQLite Log Guard Scan",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"Status: `{status}`",
        "",
        "## Candidates",
        "",
        "| Database | DB MB | WAL MB | SHM MB | Total MB | Codex Path |",
        "|---|---:|---:|---:|---:|---|",
    ]
    if candidates:
        for candidate in candidates:
            lines.append(
                f"| `{compact_path(candidate.db_path)}` | "
                f"{bytes_to_mb(candidate.db_bytes):.1f} | "
                f"{bytes_to_mb(candidate.wal_bytes):.1f} | "
                f"{bytes_to_mb(candidate.shm_bytes):.1f} | "
                f"{bytes_to_mb(candidate.total_bytes):.1f} | "
                f"{'yes' if candidate.is_codex_path else 'no'} |"
            )
    else:
        lines.append("| - | 0.0 | 0.0 | 0.0 | 0.0 | - |")
    lines.extend(["", "## Issues", ""])
    if issues:
        lines.extend(f"- {issue}" for issue in issues)
    else:
        lines.append("- No threshold issues found.")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This scan is read-only. It identifies Codex diagnostic SQLite log files and sidecars. It does not modify conversation state, memories, goals, project files, or arbitrary SQLite databases.",
            "",
        ]
    )
    return "\n".join(lines)


def maybe_write_report(report: str, args: argparse.Namespace, stem: str) -> None:
    if not getattr(args, "write_report", False):
        return
    output = resolve_path(args.output) if getattr(args, "output", "") else DEFAULT_REPORT_DIR / f"{stem}_{datetime.now(timezone.utc).strftime('%Y-%m-%d_%H%M%S')}.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")
    print(f"Report: {compact_path(output)}")


def cmd_scan(args: argparse.Namespace) -> int:
    roots = [resolve_path(path) for path in args.root] if args.root else common_codex_roots()
    dbs = [resolve_path(path) for path in args.db]
    candidates = find_candidates(roots, dbs, args.include_non_codex)
    issues: list[str] = []
    for candidate in candidates:
        if bytes_to_mb(candidate.wal_bytes) > args.max_wal_mb:
            issues.append(f"WAL exceeds threshold: {compact_path(candidate.wal_path)} ({bytes_to_mb(candidate.wal_bytes):.1f} MB)")
        if bytes_to_mb(candidate.total_bytes) > args.max_total_mb:
            issues.append(f"Total log sidecars exceed threshold: {compact_path(candidate.db_path)} ({bytes_to_mb(candidate.total_bytes):.1f} MB)")
    status = "WARN" if issues else "PASS"
    report = render_scan_report(candidates, status, issues)
    if not args.no_report:
        print(report)
    maybe_write_report(report, args, "Codex_SQLite_Log_Guard_Scan")
    print(f"Status: {status}")
    print(f"Candidates: {len(candidates)}")
    print(f"Issues: {len(issues)}")
    return 1 if args.strict and issues else 0


def cmd_monitor(args: argparse.Namespace) -> int:
    roots = [resolve_path(path) for path in args.root] if args.root else common_codex_roots()
    dbs = [resolve_path(path) for path in args.db]
    before = {candidate.db_path: candidate.total_bytes for candidate in find_candidates(roots, dbs, args.include_non_codex)}
    time.sleep(args.seconds)
    after_candidates = find_candidates(roots, dbs, args.include_non_codex)
    issues: list[str] = []
    lines = ["# Codex SQLite Log Guard Monitor", "", f"Window: {args.seconds} seconds", "", "| Database | Growth MB | MB/s |", "|---|---:|---:|"]
    for candidate in after_candidates:
        delta = candidate.total_bytes - before.get(candidate.db_path, 0)
        rate = bytes_to_mb(delta) / max(args.seconds, 1)
        lines.append(f"| `{compact_path(candidate.db_path)}` | {bytes_to_mb(delta):.2f} | {rate:.3f} |")
        if rate > args.warn_rate_mbps:
            issues.append(f"Write-rate threshold exceeded: {compact_path(candidate.db_path)} at {rate:.3f} MB/s")
    if not after_candidates:
        lines.append("| - | 0.00 | 0.000 |")
    lines.extend(["", "## Issues", ""])
    lines.extend(f"- {issue}" for issue in issues) if issues else lines.append("- No write-rate threshold issues found.")
    report = "\n".join(lines) + "\n"
    if not args.no_report:
        print(report)
    maybe_write_report(report, args, "Codex_SQLite_Log_Guard_Monitor")
    status = "WARN" if issues else "PASS"
    print(f"Status: {status}")
    print(f"Issues: {len(issues)}")
    return 1 if args.strict and issues else 0


def cmd_tables(args: argparse.Namespace) -> int:
    db_path = resolve_path(args.db)
    if not db_path.exists():
        print(f"Status: BLOCK")
        print(f"Reason: database not found: {compact_path(db_path)}")
        return 1
    try:
        tables = list_tables(db_path)
        triggers = list_guard_triggers(db_path)
    except sqlite3.DatabaseError as exc:
        print("Status: BLOCK")
        print(f"Reason: cannot inspect SQLite database: {exc}")
        return 1
    print(f"Database: {compact_path(db_path)}")
    print("Tables:")
    for table in tables:
        print(f"- {table}")
    print("Guard triggers:")
    for trigger in triggers or ["none"]:
        print(f"- {trigger}")
    return 0


def cmd_install_trigger(args: argparse.Namespace) -> int:
    db_path = resolve_path(args.db)
    if not db_path.exists():
        print("Status: BLOCK")
        print(f"Reason: database not found: {compact_path(db_path)}")
        return 1
    try:
        tables = set(list_tables(db_path))
    except sqlite3.DatabaseError as exc:
        print("Status: BLOCK")
        print(f"Reason: cannot inspect SQLite database: {exc}")
        return 1
    if args.table not in tables:
        print("Status: BLOCK")
        print(f"Reason: table {args.table!r} not found. Run the `tables` command first.")
        return 1
    sql = trigger_sql(args.table)
    if not args.apply:
        print("Status: DRY_RUN")
        print(sql)
        return 0
    ok, reason = require_safe_write(args, db_path)
    if not ok:
        print("Status: BLOCK")
        print(f"Reason: {reason}")
        return 1
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(sql)
        conn.commit()
    finally:
        conn.close()
    print("Status: PASS")
    print(f"Installed trigger: {trigger_name(args.table)}")
    print(f"Database: {compact_path(db_path)}")
    return 0


def cmd_remove_trigger(args: argparse.Namespace) -> int:
    db_path = resolve_path(args.db)
    triggers = list_guard_triggers(db_path)
    if not triggers:
        print("Status: PASS")
        print("Guard triggers: none")
        return 0
    sql = "\n".join(drop_trigger_sql(name) for name in triggers)
    if not args.apply:
        print("Status: DRY_RUN")
        print(sql)
        return 0
    ok, reason = require_safe_write(args, db_path)
    if not ok:
        print("Status: BLOCK")
        print(f"Reason: {reason}")
        return 1
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(sql)
        conn.commit()
    finally:
        conn.close()
    print("Status: PASS")
    print(f"Removed guard triggers: {len(triggers)}")
    return 0


def cmd_checkpoint(args: argparse.Namespace) -> int:
    db_path = resolve_path(args.db)
    if not args.apply:
        print("Status: DRY_RUN")
        print(f"Would run PRAGMA wal_checkpoint(TRUNCATE) on {compact_path(db_path)}")
        return 0
    ok, reason = require_safe_write(args, db_path)
    if not ok:
        print("Status: BLOCK")
        print(f"Reason: {reason}")
        return 1
    conn = sqlite3.connect(db_path)
    try:
        result = conn.execute("PRAGMA wal_checkpoint(TRUNCATE)").fetchall()
    finally:
        conn.close()
    print("Status: PASS")
    print(f"Checkpoint result: {result}")
    print(f"Database: {compact_path(db_path)}")
    return 0


def archive_members(root: Path, move_active_logs: bool) -> list[Path]:
    if not root.exists():
        return []
    members = []
    for path in root.rglob("logs*.sqlite*"):
        if not path.is_file():
            continue
        if not LOG_SIDE_RE.match(path.name):
            continue
        is_active = path.name.endswith((".sqlite", ".sqlite-wal", ".sqlite-shm")) and ".bak" not in path.name and ".old" not in path.name and ".backup" not in path.name
        if is_active and not move_active_logs:
            continue
        members.append(path)
    return sorted(members)


def cmd_archive_old(args: argparse.Namespace) -> int:
    root = resolve_path(args.root)
    members = archive_members(root, args.move_active_logs)
    if not members:
        print("Status: PASS")
        print("Files selected: 0")
        return 0
    archive_dir = resolve_path(args.archive_dir)
    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_path = archive_dir / f"codex_sqlite_logs_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.zip"
    if not args.apply:
        print("Status: DRY_RUN")
        print(f"Would archive {len(members)} files to {compact_path(archive_path)}")
        for member in members:
            print(f"- {compact_path(member)}")
        return 0
    ok, reason = require_safe_write(args, root)
    if not ok:
        print("Status: BLOCK")
        print(f"Reason: {reason}")
        return 1
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for member in members:
            archive.write(member, arcname=str(member.relative_to(root)))
    for member in members:
        if member.exists():
            member.unlink()
    print("Status: PASS")
    print(f"Archived files: {len(members)}")
    print(f"Archive: {compact_path(archive_path)}")
    return 0


def add_common_report_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--write-report", action="store_true", help="Write a Markdown report under audit-reports.")
    parser.add_argument("--no-report", action="store_true", help="Suppress Markdown report output.")
    parser.add_argument("--output", default="", help="Optional Markdown report output path.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when thresholds are exceeded.")


def add_write_safety_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--apply", action="store_true", help="Actually perform the write action. Default is dry-run.")
    parser.add_argument("--confirm-codex-closed", action="store_true", help="Confirm Codex is fully closed before modifying log files.")
    parser.add_argument("--allow-running", action="store_true", help="Override the closed-Codex safety requirement.")
    parser.add_argument("--force", action="store_true", help="Allow a non-Codex-looking target path after manual verification.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Guard against runaway Codex logs_*.sqlite / WAL growth.")
    sub = parser.add_subparsers(dest="command", required=True)

    scan = sub.add_parser("scan", help="Read-only scan for Codex SQLite log databases and WAL size.")
    scan.add_argument("--root", action="append", default=[], help="Codex data root to scan. Defaults to common Codex locations.")
    scan.add_argument("--db", action="append", default=[], help="Exact logs_*.sqlite database path to inspect.")
    scan.add_argument("--include-non-codex", action="store_true", help="Include matching filenames outside Codex-looking paths.")
    scan.add_argument("--max-wal-mb", type=float, default=512.0)
    scan.add_argument("--max-total-mb", type=float, default=1024.0)
    add_common_report_args(scan)
    scan.set_defaults(func=cmd_scan)

    monitor = sub.add_parser("monitor", help="Read-only growth-rate monitor over a short time window.")
    monitor.add_argument("--root", action="append", default=[], help="Codex data root to scan. Defaults to common Codex locations.")
    monitor.add_argument("--db", action="append", default=[], help="Exact logs_*.sqlite database path to monitor.")
    monitor.add_argument("--include-non-codex", action="store_true")
    monitor.add_argument("--seconds", type=int, default=10)
    monitor.add_argument("--warn-rate-mbps", type=float, default=1.0)
    add_common_report_args(monitor)
    monitor.set_defaults(func=cmd_monitor)

    tables = sub.add_parser("tables", help="List tables and installed guard triggers for one Codex log database.")
    tables.add_argument("--db", required=True)
    tables.set_defaults(func=cmd_tables)

    install = sub.add_parser("install-trigger", help="Install a table-specific trigger that ignores future log inserts.")
    install.add_argument("--db", required=True)
    install.add_argument("--table", default="logs", help="Target log table. Run `tables` first if unsure.")
    add_write_safety_args(install)
    install.set_defaults(func=cmd_install_trigger)

    remove = sub.add_parser("remove-trigger", help="Remove triggers installed by this guard.")
    remove.add_argument("--db", required=True)
    add_write_safety_args(remove)
    remove.set_defaults(func=cmd_remove_trigger)

    checkpoint = sub.add_parser("checkpoint", help="Run WAL checkpoint/truncate on a Codex log database.")
    checkpoint.add_argument("--db", required=True)
    add_write_safety_args(checkpoint)
    checkpoint.set_defaults(func=cmd_checkpoint)

    archive = sub.add_parser("archive-old", help="Zip and remove old Codex logs_*.sqlite* files under one root.")
    archive.add_argument("--root", required=True, help="Codex data root, for example ~/.codex.")
    archive.add_argument("--archive-dir", default=str(DEFAULT_ARCHIVE_DIR))
    archive.add_argument("--move-active-logs", action="store_true", help="Also archive active logs_*.sqlite, -wal, and -shm files.")
    add_write_safety_args(archive)
    archive.set_defaults(func=cmd_archive_old)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
