#!/usr/bin/env python3
"""Run deterministic smoke tests against the local neural vector index."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from build_vector_index import COLLECTION_NAME, DEFAULT_DB_DIR, DEFAULT_MODEL, import_runtime


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "research-wiki" / "retrieval-evals"


@dataclass
class RetrievalCase:
    case_id: str
    query: str
    expected_paths: list[str]
    rationale: str


CASES = [
    RetrievalCase(
        case_id="VEC-001",
        query="source first gate citation readiness formal research writing",
        expected_paths=[
            "AGENTS.md",
            "PROJECT_AGENT_PREFERENCES.md",
            "knowledge-base/SOURCE_READINESS_MATRIX.md",
        ],
        rationale="Core source-first and citation-readiness queries should retrieve project rules or source-readiness files.",
    ),
    RetrievalCase(
        case_id="VEC-002",
        query="self growing knowledge base raw inbox growth queue compiled wiki",
        expected_paths=[
            "knowledge-base/self-growing/README.md",
            "knowledge-base/self-growing/growth-queue.md",
            "knowledge-base/self-growing/compiled-wiki/INDEX.md",
        ],
        rationale="Self-growing KB queries should retrieve the KB guide, queue, or compiled wiki index.",
    ),
    RetrievalCase(
        case_id="VEC-003",
        query="project delivery review compliance privacy stakeholder formal output",
        expected_paths=[
            "quality-gates/PROJECT_DELIVERY_REVIEW_GATE.md",
            "compliance/PROJECT_COMPLIANCE_TRACKER.md",
            "research-wiki/DOCUMENT_PIPELINE.md",
        ],
        rationale="Delivery/compliance queries should retrieve quality gate, compliance tracker, or document pipeline.",
    ),
]


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def query(collection, model, query: str, limit: int) -> list[dict]:
    embedding = model.encode([query], normalize_embeddings=True).tolist()[0]
    results = collection.query(query_embeddings=[embedding], n_results=limit, include=["documents", "metadatas", "distances"])
    rows = []
    for document, metadata, distance in zip(
        results.get("documents", [[]])[0],
        results.get("metadatas", [[]])[0],
        results.get("distances", [[]])[0],
    ):
        rows.append(
            {
                "path": metadata.get("path", ""),
                "title": metadata.get("title", ""),
                "distance": float(distance),
                "snippet": document[:220].replace("\n", " "),
            }
        )
    return rows


def run_cases(db_dir: Path, model_name: str, limit: int) -> tuple[list[dict], int]:
    chromadb, SentenceTransformer = import_runtime()
    client = chromadb.PersistentClient(path=str(db_dir))
    collection = client.get_collection(COLLECTION_NAME)
    model = SentenceTransformer(model_name)
    output = []
    failures = 0
    for case in CASES:
        rows = query(collection, model, case.query, limit)
        returned_paths = [row["path"] for row in rows]
        hit = next((path for path in returned_paths if path in case.expected_paths), "")
        status = "PASS" if hit else "FAIL"
        if status == "FAIL":
            failures += 1
        output.append(
            {
                "case_id": case.case_id,
                "query": case.query,
                "status": status,
                "hit": hit,
                "expected_paths": case.expected_paths,
                "rationale": case.rationale,
                "rows": rows,
            }
        )
    return output, failures


def render(results: list[dict], model_name: str, db_dir: Path, limit: int) -> str:
    pass_count = sum(1 for item in results if item["status"] == "PASS")
    lines = [
        "# Vector Retrieval Smoke Test",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Model: `{model_name}`",
        f"Vector DB: `{rel(db_dir)}`",
        f"Collection: `{COLLECTION_NAME}`",
        f"Top-k: `{limit}`",
        "",
        "Configuration note: the current index uses `sentence-transformers/all-MiniLM-L6-v2` by default and chunks text at approximately 1800 characters with 250-character overlap. This is a pragmatic local retrieval setup, not a benchmarked academic search engine.",
        "",
        "## Summary",
        "",
        f"- Cases: {len(results)}",
        f"- Pass: {pass_count}",
        f"- Fail: {len(results) - pass_count}",
        "",
        "## Cases",
        "",
    ]
    for item in results:
        lines.extend(
            [
                f"### {item['case_id']} - {item['status']}",
                "",
                f"Query: `{item['query']}`",
                f"Expected path hit: `{item['hit'] or '-'}`",
                f"Rationale: {item['rationale']}",
                "",
                "| Rank | Path | Distance | Snippet |",
                "|---:|---|---:|---|",
            ]
        )
        for rank, row in enumerate(item["rows"], 1):
            snippet = row["snippet"].replace("|", "\\|")
            lines.append(f"| {rank} | `{row['path']}` | {row['distance']:.4f} | {snippet} |")
        lines.append("")
    lines.extend(
        [
            "## Boundary",
            "",
            "These smoke tests only check whether known relevant files appear in top-k results for known queries. They do not measure recall, precision, citation readiness, or whether retrieved sources support a claim.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run smoke tests for the local neural vector index.")
    parser.add_argument("--db-dir", default=str(DEFAULT_DB_DIR))
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--output-dir", default=str(OUT_DIR))
    args = parser.parse_args()

    db_dir = Path(args.db_dir)
    if not db_dir.is_absolute():
        db_dir = ROOT / db_dir
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir

    results, failures = run_cases(db_dir, args.model, args.limit)
    output_dir.mkdir(parents=True, exist_ok=True)
    report = output_dir / f"Vector_Retrieval_Smoke_Test_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.md"
    report.write_text(render(results, args.model, db_dir, args.limit), encoding="utf-8")
    print(f"Report: {report}")
    print(f"Cases: {len(results)}")
    print(f"Failed: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
