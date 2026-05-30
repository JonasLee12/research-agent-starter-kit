#!/usr/bin/env python3
"""Build a local SQLite index for research-agent memory files.

This is a local, dependency-free index. It does not call external APIs and it
does not replace source files as the source of record.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / ".agent-runtime" / "agent_memory_index.sqlite3"

SCAN_DIRS = [
    "research-wiki",
    "knowledge-base",
    "compliance",
    "ethics",
    "proposal",
    "chapter-plans",
    "outputs",
    "quality-gates",
    "supervisor-notes",
    "university-guidance",
    ".agents/skills",
]

TOP_LEVEL_FILES = [
    "AGENTS.md",
    "PROJECT_AGENT_PREFERENCES.md",
    "USER_DASHBOARD.md",
    "RESEARCH_PROJECT_BRIEF.md",
    "DISSERTATION_BRIEF.md",
    "RESEARCH_PROJECT_BRIEF_TEMPLATE.md",
    "SKILL_MIGRATION.md",
]

INCLUDE_SUFFIXES = {".md", ".txt", ".jsonl"}

EXCLUDED_PARTS = {
    ".git",
    ".agent-runtime",
    "private",
    "Private",
    "raw",
    "raw-inbox",
    "audio",
    "video",
    "recordings",
    "transcripts",
    "identifiable",
    "signed-consent",
    "participant-contact",
}

MARKERS = [
    "TO CONFIRM",
    "NEEDS VERIFICATION",
    "CONFIRMED",
    "INFERENCE",
    "CONTEXTUAL SOURCE",
    "OFFICIAL ORIGINAL TEXT",
    "LOCAL SUMMARY",
    "INSUFFICIENT EVIDENCE",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def should_scan(path: Path) -> bool:
    if path.suffix not in INCLUDE_SUFFIXES:
        return False
    parts = set(path.relative_to(ROOT).parts)
    if parts & EXCLUDED_PARTS:
        return False
    if "rendered" in path.name.lower():
        return False
    return True


def iter_files() -> list[Path]:
    files: list[Path] = []
    for item in TOP_LEVEL_FILES:
        path = ROOT / item
        if path.exists() and should_scan(path):
            files.append(path)
    for directory in SCAN_DIRS:
        base = ROOT / directory
        if not base.exists():
            continue
        files.extend(path for path in base.rglob("*") if path.is_file() and should_scan(path))
    return sorted(set(files))


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def classify_kind(path: Path) -> str:
    rel_parts = path.relative_to(ROOT).parts
    if len(rel_parts) == 1:
        return "project-root"
    if rel_parts[0] == ".agents":
        return "skill"
    return rel_parts[0]


def extract_title(path: Path, text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return path.stem


def evidence_status(text: str) -> str:
    if "TO CONFIRM" in text:
        return "contains_to_confirm"
    if "NEEDS VERIFICATION" in text or "INSUFFICIENT EVIDENCE" in text:
        return "needs_verification"
    if "OFFICIAL ORIGINAL TEXT" in text:
        return "official_original_text"
    if "CONFIRMED" in text:
        return "contains_confirmed"
    return "unclassified"


def initialise(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        PRAGMA journal_mode=WAL;

        CREATE TABLE IF NOT EXISTS files (
            path TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            kind TEXT NOT NULL,
            sha256 TEXT NOT NULL,
            bytes INTEGER NOT NULL,
            mtime REAL NOT NULL,
            evidence_status TEXT NOT NULL,
            indexed_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS headings (
            file_path TEXT NOT NULL,
            level INTEGER NOT NULL,
            heading TEXT NOT NULL,
            line_no INTEGER NOT NULL,
            FOREIGN KEY(file_path) REFERENCES files(path)
        );

        CREATE TABLE IF NOT EXISTS markers (
            file_path TEXT NOT NULL,
            marker TEXT NOT NULL,
            line_no INTEGER NOT NULL,
            line_text TEXT NOT NULL,
            FOREIGN KEY(file_path) REFERENCES files(path)
        );

        CREATE TABLE IF NOT EXISTS session_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            run_id TEXT,
            window TEXT,
            event_type TEXT,
            status TEXT,
            file TEXT,
            evidence TEXT,
            risk TEXT,
            raw_json TEXT NOT NULL
        );
        """
    )


def clear_tables(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        DELETE FROM session_events;
        DELETE FROM markers;
        DELETE FROM headings;
        DELETE FROM files;
        """
    )


def index_file(conn: sqlite3.Connection, path: Path, indexed_at: str) -> None:
    text = read_text(path)
    stat = path.stat()
    file_path = rel(path)
    conn.execute(
        """
        INSERT OR REPLACE INTO files
        (path, title, kind, sha256, bytes, mtime, evidence_status, indexed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            file_path,
            extract_title(path, text),
            classify_kind(path),
            sha256_text(text),
            len(text.encode("utf-8")),
            stat.st_mtime,
            evidence_status(text),
            indexed_at,
        ),
    )

    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("#"):
            prefix = stripped.split(" ", 1)[0]
            if set(prefix) == {"#"} and 1 <= len(prefix) <= 6 and " " in stripped:
                conn.execute(
                    "INSERT INTO headings(file_path, level, heading, line_no) VALUES (?, ?, ?, ?)",
                    (file_path, len(prefix), stripped[len(prefix) :].strip(), line_no),
                )
        for marker in MARKERS:
            if marker in line:
                conn.execute(
                    "INSERT INTO markers(file_path, marker, line_no, line_text) VALUES (?, ?, ?, ?)",
                    (file_path, marker, line_no, stripped[:500]),
                )

    if path.name == "SESSION_EVENT_LOG.jsonl":
        for line in text.splitlines():
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            conn.execute(
                """
                INSERT INTO session_events
                (timestamp, run_id, window, event_type, status, file, evidence, risk, raw_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.get("timestamp"),
                    event.get("run_id"),
                    event.get("window"),
                    event.get("event_type"),
                    event.get("status"),
                    event.get("file"),
                    event.get("evidence"),
                    event.get("risk"),
                    json.dumps(event, ensure_ascii=False, sort_keys=True),
                ),
            )


def rebuild(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        initialise(conn)
        clear_tables(conn)
        indexed_at = datetime.now(timezone.utc).isoformat()
        for path in iter_files():
            index_file(conn, path, indexed_at)
        conn.commit()
    finally:
        conn.close()


def summary(db_path: Path) -> str:
    conn = sqlite3.connect(db_path)
    try:
        files = conn.execute("SELECT COUNT(*) FROM files").fetchone()[0]
        headings = conn.execute("SELECT COUNT(*) FROM headings").fetchone()[0]
        markers = conn.execute("SELECT COUNT(*) FROM markers").fetchone()[0]
        events = conn.execute("SELECT COUNT(*) FROM session_events").fetchone()[0]
        by_kind = conn.execute(
            "SELECT kind, COUNT(*) FROM files GROUP BY kind ORDER BY kind"
        ).fetchall()
    finally:
        conn.close()
    lines = [
        f"Database: {db_path}",
        f"Files indexed: {files}",
        f"Headings indexed: {headings}",
        f"Evidence markers indexed: {markers}",
        f"Session events indexed: {events}",
        "Files by kind:",
    ]
    lines.extend(f"- {kind}: {count}" for kind, count in by_kind)
    return "\n".join(lines)


def search(db_path: Path, term: str, limit: int) -> str:
    needle = f"%{term}%"
    conn = sqlite3.connect(db_path)
    try:
        rows = conn.execute(
            """
            SELECT path, title, kind, evidence_status
            FROM files
            WHERE path LIKE ? OR title LIKE ?
            ORDER BY kind, path
            LIMIT ?
            """,
            (needle, needle, limit),
        ).fetchall()
        heading_rows = conn.execute(
            """
            SELECT file_path, heading, line_no
            FROM headings
            WHERE heading LIKE ?
            ORDER BY file_path, line_no
            LIMIT ?
            """,
            (needle, limit),
        ).fetchall()
    finally:
        conn.close()
    lines = [f"Search term: {term}", "Files:"]
    if rows:
        lines.extend(f"- {path} | {title} | {kind} | {status}" for path, title, kind, status in rows)
    else:
        lines.append("- no file-title matches")
    lines.append("Headings:")
    if heading_rows:
        lines.extend(f"- {file_path}:{line_no} | {heading}" for file_path, heading, line_no in heading_rows)
    else:
        lines.append("- no heading matches")
    return "\n".join(lines)


def list_to_confirm(db_path: Path, limit: int, include_skills: bool = False) -> str:
    conn = sqlite3.connect(db_path)
    try:
        if include_skills:
            rows = conn.execute(
                """
                SELECT file_path, line_no, line_text
                FROM markers
                WHERE marker = 'TO CONFIRM'
                ORDER BY file_path, line_no
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT m.file_path, m.line_no, m.line_text
                FROM markers m
                JOIN files f ON f.path = m.file_path
                WHERE m.marker = 'TO CONFIRM'
                  AND f.kind NOT IN ('skill', 'project-root')
                ORDER BY m.file_path, m.line_no
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
    finally:
        conn.close()
    if not rows:
        return "No TO CONFIRM markers found."
    return "\n".join(f"- {file_path}:{line_no} | {line_text}" for file_path, line_no, line_text in rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build/query the local research-agent index.")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="SQLite database path.")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild the index.")
    parser.add_argument("--summary", action="store_true", help="Print index summary.")
    parser.add_argument("--search", help="Search indexed file titles and headings.")
    parser.add_argument("--list-to-confirm", action="store_true", help="List TO CONFIRM markers.")
    parser.add_argument("--include-skills", action="store_true", help="Include skill files in TO CONFIRM marker listing.")
    parser.add_argument("--limit", type=int, default=20, help="Maximum result count.")
    args = parser.parse_args()

    db_path = Path(args.db)
    if not db_path.is_absolute():
        db_path = ROOT / db_path

    if args.rebuild or not db_path.exists():
        rebuild(db_path)

    outputs: list[str] = []
    if args.summary:
        outputs.append(summary(db_path))
    if args.search:
        outputs.append(search(db_path, args.search, args.limit))
    if args.list_to_confirm:
        outputs.append(list_to_confirm(db_path, args.limit, include_skills=args.include_skills))
    if not outputs:
        outputs.append(summary(db_path))

    print("\n\n".join(outputs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
