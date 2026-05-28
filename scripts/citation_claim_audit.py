#!/usr/bin/env python3
"""Create a claim-by-claim citation support audit queue for Markdown drafts."""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path

from citation_style_check import (
    extract_in_text_citations,
    extract_reference_entries,
    reference_section,
    body_section,
)


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "audit-reports"
SOURCE_DIR = ROOT / "knowledge-base" / "sources"
SOURCE_MATRIX = ROOT / "knowledge-base" / "SOURCE_READINESS_MATRIX.md"
CITATION_PATTERN = re.compile(r"\([^()]*\b(?:19|20)\d{2}[a-z]?[^()]*\)|\b[A-Z][A-Za-z'’.-]+(?:\s+et al\.)?\s+\((?:19|20)\d{2}[a-z]?\)")


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", text)
    return [part.strip() for part in parts if CITATION_PATTERN.search(part)]


def source_note_status(author: str, year: str) -> tuple[str, str]:
    haystacks = []
    if SOURCE_MATRIX.exists():
        haystacks.append(("knowledge-base/SOURCE_READINESS_MATRIX.md", SOURCE_MATRIX.read_text(encoding="utf-8", errors="replace")))
    if SOURCE_DIR.exists():
        for path in SOURCE_DIR.glob("*.md"):
            text = path.read_text(encoding="utf-8", errors="replace")
            if author.lower() in text.lower() and year[:4] in text:
                haystacks.append((str(path.relative_to(ROOT)), text))
    for file_name, text in haystacks:
        lower = text.lower()
        if author.lower() in lower and year[:4] in text:
            if "claim support verified" in lower:
                return "CLAIM_SUPPORT_VERIFIED", file_name
            if "full text reviewed" in lower:
                return "SOURCE_NOTE_FULL_TEXT_REVIEWED_MANUAL_SUPPORT_CHECK_REQUIRED", file_name
            if "targeted reviewed" in lower or "website reviewed" in lower or "abstract reviewed" in lower:
                return "SOURCE_NOTE_AVAILABLE_MANUAL_SUPPORT_CHECK_REQUIRED", file_name
            if "metadata only" in lower or "metadata verified" in lower:
                return "METADATA_ONLY_NOT_CLAIM_READY", file_name
            return "SOURCE_MENTION_FOUND_STATUS_UNCLEAR", file_name
    return "NO_LOCAL_SOURCE_NOTE_FOUND", ""


def claim_rows(path: Path) -> tuple[list[dict], set[tuple[str, str]], set[tuple[str, str]]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    refs = reference_section(text)
    ref_entries = extract_reference_entries(refs)
    sentences = split_sentences(body_section(text))
    rows = []
    for index, sentence in enumerate(sentences, start=1):
        citations, unresolved = extract_in_text_citations(sentence)
        if not citations and unresolved:
            rows.append(
                {
                    "index": index,
                    "claim": sentence,
                    "citation": "; ".join(unresolved),
                    "reference_status": "UNPARSED",
                    "source_status": "NEEDS_MANUAL_REVIEW",
                    "source_file": "",
                }
            )
            continue
        for author, year in sorted(citations):
            reference_status = "REFERENCE_ENTRY_PRESENT" if (author, year) in ref_entries or (author in refs and year in refs) else "MISSING_REFERENCE_ENTRY"
            source_status, source_file = source_note_status(author, year)
            rows.append(
                {
                    "index": index,
                    "claim": sentence,
                    "citation": f"{author} ({year})",
                    "reference_status": reference_status,
                    "source_status": source_status,
                    "source_file": source_file,
                }
            )
    return rows, {tuple(row["citation"].replace(")", "").split(" (")) for row in rows if " (" in row["citation"]}, ref_entries


def render(path: Path, rows: list[dict]) -> str:
    source_attention = [
        row
        for row in rows
        if row["reference_status"] != "REFERENCE_ENTRY_PRESENT"
        or row["source_status"] != "CLAIM_SUPPORT_VERIFIED"
    ]
    lines = [
        "# Citation Claim Support Audit",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"File: `{path}`",
        "",
        "## Summary",
        "",
        f"- Claims with citations: {len({row['index'] for row in rows})}",
        f"- Citation-claim rows: {len(rows)}",
        f"- Rows requiring manual claim-support verification: {len(source_attention)}",
        "",
        "## Claim Rows",
        "",
        "| # | Citation | Reference status | Source-readiness status | Source file | Claim sentence |",
        "|---:|---|---|---|---|---|",
    ]
    for row in rows:
        claim = row["claim"].replace("|", "\\|")
        source_file = row["source_file"] or "-"
        lines.append(
            f"| {row['index']} | {row['citation']} | {row['reference_status']} | {row['source_status']} | `{source_file}` | {claim} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This tool creates a claim-support audit queue. It does not automatically prove that a source supports a claim. A human or agent must inspect the relevant source sections before marking any row as verified.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit citation-claim support readiness for Markdown drafts.")
    parser.add_argument("file")
    parser.add_argument("--output-dir", default=str(OUT_DIR))
    parser.add_argument("--fail-on-attention", action="store_true")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.is_absolute():
        path = ROOT / path
    rows, _, _ = claim_rows(path)
    out_dir = Path(args.output_dir)
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"Citation_Claim_Support_Audit_{path.stem}_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.md"
    out.write_text(render(path, rows), encoding="utf-8")
    attention = [
        row
        for row in rows
        if row["reference_status"] != "REFERENCE_ENTRY_PRESENT"
        or row["source_status"] != "CLAIM_SUPPORT_VERIFIED"
    ]
    print(f"Report: {out}")
    print(f"Rows requiring manual claim-support verification: {len(attention)}")
    return 1 if args.fail_on_attention and attention else 0


if __name__ == "__main__":
    raise SystemExit(main())
