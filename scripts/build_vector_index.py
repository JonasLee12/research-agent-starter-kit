#!/usr/bin/env python3
"""Build/query a local neural embedding vector index for research-project notes.

Run with the project vector environment:

    .venv-vector/bin/python scripts/build_vector_index.py --rebuild --summary

The generated Chroma database lives under `.agent-runtime/` and is not committed.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_DIR = ROOT / ".agent-runtime" / "vector_index" / "chroma"
DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
COLLECTION_NAME = "research_project_notes"

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
    ".venv-vector",
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


@dataclass
class Chunk:
    chunk_id: str
    path: str
    title: str
    text: str


def import_runtime():
    try:
        import chromadb
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise SystemExit(
            "Vector dependencies are missing. Run this script with "
            "`.venv-vector/bin/python`, after installing chromadb and sentence-transformers."
        ) from exc
    return chromadb, SentenceTransformer


def should_scan(path: Path) -> bool:
    if path.suffix not in SUFFIXES:
        return False
    try:
        parts = set(path.relative_to(ROOT).parts)
    except ValueError:
        return False
    if parts & EXCLUDE_PARTS:
        return False
    if "rendered" in path.name.lower():
        return False
    return True


def iter_files() -> list[Path]:
    files: list[Path] = []
    for item in TOP_FILES:
        path = ROOT / item
        if path.exists() and should_scan(path):
            files.append(path)
    for directory in SCAN_DIRS:
        base = ROOT / directory
        if base.exists():
            files.extend(path for path in base.rglob("*") if path.is_file() and should_scan(path))
    return sorted(set(files))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def title_for(path: Path, text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def chunk_text(path: Path, text: str, chunk_chars: int = 1800, overlap: int = 250) -> list[Chunk]:
    cleaned = clean_text(text)
    if not cleaned:
        return []
    title = title_for(path, text)
    chunks: list[Chunk] = []
    start = 0
    index = 0
    while start < len(cleaned):
        end = min(start + chunk_chars, len(cleaned))
        piece = cleaned[start:end]
        digest = hashlib.sha1(f"{rel(path)}:{index}:{piece[:80]}".encode("utf-8")).hexdigest()[:16]
        chunks.append(Chunk(f"{rel(path)}::{digest}", rel(path), title, piece))
        if end == len(cleaned):
            break
        start = max(0, end - overlap)
        index += 1
    return chunks


def load_chunks() -> list[Chunk]:
    chunks: list[Chunk] = []
    for path in iter_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        chunks.extend(chunk_text(path, text))
    return chunks


def build_index(db_dir: Path, model_name: str, batch_size: int) -> tuple[int, int]:
    chromadb, SentenceTransformer = import_runtime()
    os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")
    db_dir.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(db_dir))
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={
            "model": model_name,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "evidence_boundary": "local neural embeddings; source files remain authoritative",
        },
    )
    chunks = load_chunks()
    model = SentenceTransformer(model_name)
    for start in range(0, len(chunks), batch_size):
        batch = chunks[start : start + batch_size]
        embeddings = model.encode([chunk.text for chunk in batch], normalize_embeddings=True).tolist()
        collection.add(
            ids=[chunk.chunk_id for chunk in batch],
            documents=[chunk.text for chunk in batch],
            metadatas=[
                {
                    "path": chunk.path,
                    "title": chunk.title,
                    "chunk_index": start + offset,
                    "model": model_name,
                }
                for offset, chunk in enumerate(batch)
            ],
            embeddings=embeddings,
        )
    return len(iter_files()), len(chunks)


def query_index(db_dir: Path, model_name: str, query: str, limit: int) -> str:
    chromadb, SentenceTransformer = import_runtime()
    os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")
    client = chromadb.PersistentClient(path=str(db_dir))
    collection = client.get_collection(COLLECTION_NAME)
    model = SentenceTransformer(model_name)
    embedding = model.encode([query], normalize_embeddings=True).tolist()[0]
    results = collection.query(query_embeddings=[embedding], n_results=limit, include=["documents", "metadatas", "distances"])
    lines = ["# Neural Vector Search", "", f"Query: {query}", ""]
    ids = results.get("ids", [[]])[0]
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]
    for item_id, document, metadata, distance in zip(ids, documents, metadatas, distances):
        snippet = document[:280].replace("\n", " ")
        lines.append(f"- `{metadata.get('path')}` | {metadata.get('title')} | distance={distance:.4f} | id={item_id}")
        lines.append(f"  {snippet}...")
    return "\n".join(lines) + "\n"


def count_index(db_dir: Path) -> int:
    chromadb, _ = import_runtime()
    client = chromadb.PersistentClient(path=str(db_dir))
    collection = client.get_or_create_collection(COLLECTION_NAME)
    return collection.count()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build/query the local neural vector index.")
    parser.add_argument("--db-dir", default=str(DEFAULT_DB_DIR))
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--rebuild", action="store_true")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--query")
    parser.add_argument("--limit", type=int, default=8)
    args = parser.parse_args()

    db_dir = Path(args.db_dir)
    if not db_dir.is_absolute():
        db_dir = ROOT / db_dir

    if args.rebuild:
        files, chunks = build_index(db_dir, args.model, args.batch_size)
        print(f"Vector DB: {db_dir}")
        print(f"Model: {args.model}")
        print(f"Files scanned: {files}")
        print(f"Chunks indexed: {chunks}")
    if args.query:
        print(query_index(db_dir, args.model, args.query, args.limit))
    elif args.summary and not args.rebuild:
        print(f"Vector DB: {db_dir}")
        print(f"Collection: {COLLECTION_NAME}")
        print(f"Chunks indexed: {count_index(db_dir)}")
    elif args.summary and args.rebuild:
        print(f"Collection: {COLLECTION_NAME}")
        print(f"Chunks indexed: {count_index(db_dir)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
