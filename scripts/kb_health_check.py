#!/usr/bin/env python3
"""Check the evidence-governed self-growing research knowledge base."""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_PATHS = [
    "research-wiki/RETRIEVAL_PROTOCOL.md",
    "knowledge-base/SOURCE_REGISTER.md",
    "knowledge-base/SOURCE_READINESS_MATRIX.md",
    "knowledge-base/self-growing/README.md",
    "knowledge-base/self-growing/raw-inbox/README.md",
    "knowledge-base/self-growing/growth-queue.md",
    "knowledge-base/self-growing/compiled-wiki/INDEX.md",
]
CONTENT_SCAN_PATHS = [
    "knowledge-base/self-growing/raw-inbox",
    "knowledge-base/self-growing/compiled-wiki",
    "knowledge-base/self-growing/growth-queue.md",
]
UNRESOLVED_MARKERS = ["TO CONFIRM", "SOURCE TO ADD", "TODO", "xxx"]
PRIVATE_MARKERS = [
    "participant name",
    "teacher email",
    "signed consent",
    "interview recording",
    "raw transcript",
    "client confidential",
    "restricted LMS",
    "api key",
]


def list_files(path: Path) -> list[Path]:
    if not path.exists():
        return []
    return [p for p in path.rglob("*") if p.is_file() and p.name != ".DS_Store"]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write a Markdown report")
    parser.add_argument("--out-dir", default="knowledge-base/self-growing/health-checks")
    args = parser.parse_args()

    missing = [p for p in REQUIRED_PATHS if not (ROOT / p).exists()]
    raw_files = [
        p for p in list_files(ROOT / "knowledge-base/self-growing/raw-inbox")
        if p.name != "README.md"
    ]
    compiled_files = [
        p for p in list_files(ROOT / "knowledge-base/self-growing/compiled-wiki")
        if p.name != "INDEX.md"
    ]

    marker_hits: list[str] = []
    private_hits: list[str] = []
    for scan in CONTENT_SCAN_PATHS:
        path = ROOT / scan
        files = list_files(path) if path.is_dir() else ([path] if path.exists() else [])
        for file_path in files:
            if file_path.name in {"README.md", "INDEX.md"}:
                continue
            if file_path.suffix.lower() not in {".md", ".txt"}:
                continue
            text = read_text(file_path)
            rel = file_path.relative_to(ROOT)
            for marker in UNRESOLVED_MARKERS:
                if marker in text:
                    marker_hits.append(f"{rel}: contains `{marker}`")
            lower = text.lower()
            for marker in PRIVATE_MARKERS:
                if marker in lower:
                    private_hits.append(f"{rel}: possible private-data phrase `{marker}`")

    status = "PASS"
    warnings: list[str] = []
    if missing:
        status = "HOLD"
    if raw_files:
        warnings.append(f"{len(raw_files)} raw inbox item(s) need triage.")
        if status == "PASS":
            status = "WARN"
    if marker_hits:
        warnings.append(f"{len(marker_hits)} unresolved marker hit(s) found.")
        if status == "PASS":
            status = "WARN"
    if private_hits:
        status = "HOLD"
        warnings.append(f"{len(private_hits)} possible private-data marker hit(s) found.")

    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_slug = dt.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    report_lines = [
        "# Self-Growing Knowledge Base Health Check",
        "",
        f"Generated: {now}",
        f"Status: {status}",
        "",
        "## Required Paths",
        "",
    ]
    if missing:
        report_lines.extend([f"- MISSING: `{p}`" for p in missing])
    else:
        report_lines.append("- All required paths found.")

    report_lines.extend([
        "",
        "## Counts",
        "",
        f"- Raw inbox items needing triage: {len(raw_files)}",
        f"- Compiled wiki pages beyond index/example: {len([p for p in compiled_files if p.name != 'EXAMPLE_ENTRY.md'])}",
        "",
        "## Raw Inbox",
        "",
    ])
    report_lines.extend([f"- `{p.relative_to(ROOT)}`" for p in raw_files] or ["- none"])

    report_lines.extend([
        "",
        "## Unresolved Marker Hits",
        "",
    ])
    report_lines.extend([f"- {hit}" for hit in marker_hits] or ["- none"])

    report_lines.extend([
        "",
        "## Private-Data Boundary Hits",
        "",
    ])
    report_lines.extend([f"- {hit}" for hit in private_hits] or ["- none"])

    report_lines.extend([
        "",
        "## Boundary Reminder",
        "",
        "- This check does not prove citation readiness or claim support.",
        "- Obsidian or another note app remains a navigation layer, not the formal source of record.",
        "- Formal writing still requires source-first, source-readiness, and the relevant project gates.",
        "",
    ])

    report = "\n".join(report_lines)
    if args.write:
        out_dir = ROOT / args.out_dir
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"KB_Self_Growth_Check_{date_slug}.md"
        out_path.write_text(report, encoding="utf-8")
        print(out_path)
    else:
        print(report)

    return 2 if status == "HOLD" else 0


if __name__ == "__main__":
    raise SystemExit(main())
