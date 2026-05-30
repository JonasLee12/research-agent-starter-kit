#!/usr/bin/env python3
"""Local retrieval over research-project notes.

Provides two dependency-free retrieval layers:
- SQLite FTS5 lexical search;
- hashed-vector cosine search over project Markdown/text files.

This is a local retrieval layer, not a neural embedding model.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import re
import sqlite3
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / ".agent-runtime" / "retrieval_index.sqlite3"

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
TOP_FILES = [
    "AGENTS.md",
    "PROJECT_AGENT_PREFERENCES.md",
    "USER_DASHBOARD.md",
    "RESEARCH_PROJECT_BRIEF.md",
    "DISSERTATION_BRIEF.md",
    "RESEARCH_PROJECT_BRIEF_TEMPLATE.md",
]
SUFFIXES = {".md", ".txt", ".jsonl"}
EXCLUDE_PARTS = {
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
}
VECTOR_DIMS = 512


@dataclass
class Doc:
    path: str
    title: str
    content: str
    vector: dict[int, float]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def should_scan(path: Path) -> bool:
    if path.suffix not in SUFFIXES:
        return False
    parts = set(path.relative_to(ROOT).parts)
    if parts & EXCLUDE_PARTS:
        return False
    if "rendered" in path.name.lower():
        return False
    return True


def iter_files() -> list[Path]:
    files = []
    for item in TOP_FILES:
        path = ROOT / item
        if path.exists() and should_scan(path):
            files.append(path)
    for directory in SCAN_DIRS:
        base = ROOT / directory
        if base.exists():
            files.extend(p for p in base.rglob("*") if p.is_file() and should_scan(p))
    return sorted(set(files))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def title_for(path: Path, text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def tokens(text: str) -> list[str]:
    return [tok.lower() for tok in re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}|[\u4e00-\u9fff]{2,}", text)]


def hashed_vector(text: str) -> dict[int, float]:
    counts = Counter(tokens(text))
    if not counts:
        return {}
    vec: dict[int, float] = {}
    for token, count in counts.items():
        digest = hashlib.blake2b(token.encode("utf-8"), digest_size=4).digest()
        bucket = int.from_bytes(digest, "big") % VECTOR_DIMS
        sign = 1 if digest[0] % 2 == 0 else -1
        vec[bucket] = vec.get(bucket, 0.0) + sign * (1.0 + math.log(count))
    norm = math.sqrt(sum(value * value for value in vec.values()))
    if norm:
        vec = {key: value / norm for key, value in vec.items()}
    return vec


def cosine(a: dict[int, float], b: dict[int, float]) -> float:
    if not a or not b:
        return 0.0
    if len(a) > len(b):
        a, b = b, a
    return sum(value * b.get(key, 0.0) for key, value in a.items())


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS docs (
            path TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            token_count INTEGER NOT NULL,
            indexed_at TEXT NOT NULL
        );
        CREATE VIRTUAL TABLE IF NOT EXISTS docs_fts USING fts5(path, title, content);
        CREATE TABLE IF NOT EXISTS doc_vectors (
            path TEXT NOT NULL,
            bucket INTEGER NOT NULL,
            value REAL NOT NULL,
            PRIMARY KEY(path, bucket)
        );
        """
    )


def rebuild(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        init_db(conn)
        conn.executescript("DELETE FROM docs; DELETE FROM docs_fts; DELETE FROM doc_vectors;")
        indexed_at = datetime.now(timezone.utc).isoformat()
        seen_paths: set[str] = set()
        for path in iter_files():
            rpath = rel(path)
            if rpath in seen_paths:
                continue
            seen_paths.add(rpath)
            text = read_text(path)
            title = title_for(path, text)
            token_count = len(tokens(text))
            vec = hashed_vector(text)
            conn.execute(
                "INSERT INTO docs(path, title, content, token_count, indexed_at) VALUES (?, ?, ?, ?, ?)",
                (rpath, title, text, token_count, indexed_at),
            )
            conn.execute(
                "INSERT INTO docs_fts(path, title, content) VALUES (?, ?, ?)",
                (rpath, title, text),
            )
            conn.executemany(
                "INSERT INTO doc_vectors(path, bucket, value) VALUES (?, ?, ?)",
                [(rpath, bucket, value) for bucket, value in vec.items()],
            )
        conn.commit()
    finally:
        conn.close()


def summary(db_path: Path) -> str:
    conn = sqlite3.connect(db_path)
    try:
        docs = conn.execute("SELECT COUNT(*) FROM docs").fetchone()[0]
        vecs = conn.execute("SELECT COUNT(*) FROM doc_vectors").fetchone()[0]
    finally:
        conn.close()
    return f"Database: {db_path}\nDocuments indexed: {docs}\nVector cells indexed: {vecs}\nVector type: hashed token vectors, {VECTOR_DIMS} dimensions"


def search(db_path: Path, query: str, limit: int) -> str:
    qvec = hashed_vector(query)
    conn = sqlite3.connect(db_path)
    try:
        docs = {}
        for path, title, content in conn.execute("SELECT path, title, content FROM docs"):
            docs[path] = Doc(path, title, content, {})
        for path, bucket, value in conn.execute("SELECT path, bucket, value FROM doc_vectors"):
            if path in docs:
                docs[path].vector[int(bucket)] = float(value)
        vector_scores = [(cosine(qvec, doc.vector), doc) for doc in docs.values()]
        vector_scores.sort(key=lambda item: item[0], reverse=True)
        safe_query = " ".join(tokens(query)) or query
        fts_rows = []
        try:
            fts_rows = conn.execute(
                """
                SELECT path, title, snippet(docs_fts, 2, '[', ']', ' ... ', 20), bm25(docs_fts) AS rank
                FROM docs_fts
                WHERE docs_fts MATCH ?
                ORDER BY rank
                LIMIT ?
                """,
                (safe_query, limit),
            ).fetchall()
        except sqlite3.OperationalError:
            fts_rows = []
    finally:
        conn.close()

    lines = [f"# Local Retrieval Search", "", f"Query: {query}", "", "## FTS5 Matches"]
    if fts_rows:
        for path, title, snippet, rank in fts_rows:
            lines.append(f"- `{path}` | {title} | rank={rank:.3f} | {snippet}")
    else:
        lines.append("- No lexical FTS match.")
    lines.extend(["", "## Hashed-Vector Matches"])
    for score, doc in vector_scores[:limit]:
        if score <= 0:
            continue
        lines.append(f"- `{doc.path}` | {doc.title} | cosine={score:.3f}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build/query local retrieval index.")
    parser.add_argument("--db", default=str(DEFAULT_DB))
    parser.add_argument("--rebuild", action="store_true")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--query")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    db_path = Path(args.db)
    if not db_path.is_absolute():
        db_path = ROOT / db_path
    if args.rebuild or not db_path.exists():
        rebuild(db_path)
    if args.query:
        print(search(db_path, args.query, args.limit))
    else:
        print(summary(db_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
