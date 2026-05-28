#!/usr/bin/env python3
"""Citation/reference consistency checks for research Markdown drafts.

This script checks surface consistency. It cannot prove that a cited source
supports a specific claim; that still needs a manual citation audit.
"""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "audit-reports"
YEAR_RE = r"(?:19|20)\d{2}[a-z]?"
PAREN_CITATION_RE = re.compile(r"\(([^()]*\b(?:19|20)\d{2}[a-z]?[^()]*)\)")
NARRATIVE_CITATION_RE = re.compile(
    r"\b([A-Z][A-Za-z'’.-]+)"
    r"(?:\s+et al\.)?"
    r"(?:,\s+(?:[a-z]{1,4}\s+)?[A-Z][A-Za-z'’.-]+)*"
    r"(?:\s+(?:and|&)\s+(?:[a-z]{1,4}\s+)?[A-Z][A-Za-z'’.-]+)?"
    r"(?:'s)?\s+\(((?:19|20)\d{2}[a-z]?)\)"
)
REF_ENTRY_RE = re.compile(r"^\s*([A-Z][A-Za-z'’.-]+),.*?\(((?:19|20)\d{2}[a-z]?)\)")
DOI_RE = re.compile(r"\b10\.\d{4,9}/\S+")
STOPWORDS = {
    "Appendix",
    "Assessment",
    "Figure",
    "For",
    "In",
    "Section",
    "See",
    "Table",
    "The",
    "This",
    "To",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def reference_section(text: str) -> str:
    match = re.search(r"^#+\s+References\b", text, flags=re.I | re.M)
    if not match:
        return ""
    tail = text[match.end() :]
    next_heading = re.search(r"^#+\s+(?!References\b).+", tail, flags=re.I | re.M)
    if next_heading:
        return tail[: next_heading.start()]
    return tail


def body_section(text: str) -> str:
    match = re.search(r"^#+\s+References\b", text, flags=re.I | re.M)
    return text[: match.start()] if match else text


def normalize_author(author: str) -> str:
    author = re.sub(r"'s\b", "", author)
    author = re.sub(r"\bet al\.?\b", "", author, flags=re.I)
    author = re.sub(r"\b(?:and|&)\b.*", "", author)
    author = re.sub(r"^[Ss]ee\s+", "", author)
    author = re.sub(r"^[Ee]\.g\.,?\s+", "", author)
    author = author.strip(" ,;.")
    match = re.search(r"[A-Z][A-Za-z'’.-]+", author)
    if not match:
        return ""
    surname = match.group(0)
    return "" if surname in STOPWORDS else surname


def extract_year(segment: str) -> str:
    match = re.search(YEAR_RE, segment)
    return match.group(0) if match else ""


def extract_in_text_citations(text: str) -> tuple[set[tuple[str, str]], list[str]]:
    citations: set[tuple[str, str]] = set()
    unresolved: list[str] = []
    body = body_section(text)

    for content in PAREN_CITATION_RE.findall(body):
        if re.search(r"\b(?:19|20)\d{2}[a-z]?\b", content) is None:
            continue
        for segment in re.split(r";", content):
            year = extract_year(segment)
            if not year:
                continue
            author_text = segment.split(year, 1)[0]
            author = normalize_author(author_text)
            if author:
                citations.add((author, year))
            elif any(char.isalpha() for char in segment):
                unresolved.append(segment.strip())

    for author, year in NARRATIVE_CITATION_RE.findall(body):
        normalized = normalize_author(author)
        if normalized:
            citations.add((normalized, year))

    return citations, sorted(set(unresolved))


def extract_reference_entries(refs: str) -> set[tuple[str, str]]:
    entries: set[tuple[str, str]] = set()
    for line in refs.splitlines():
        match = REF_ENTRY_RE.search(line)
        if match:
            author = normalize_author(match.group(1))
            year = match.group(2)
            if author and year:
                entries.add((author, year))
    return entries


def has_reference_match(citation: tuple[str, str], ref_entries: set[tuple[str, str]], refs: str) -> bool:
    author, year = citation
    return citation in ref_entries or (author in refs and year in refs)


def has_body_match(reference: tuple[str, str], in_text: set[tuple[str, str]], text: str) -> bool:
    author, year = reference
    return reference in in_text or (author in body_section(text) and year in body_section(text))


def check_file(path: Path) -> str:
    text = read(path)
    refs = reference_section(text)
    in_text, unresolved_citation_segments = extract_in_text_citations(text)
    ref_entries = extract_reference_entries(refs)
    doi_like = DOI_RE.findall(text)
    issues = []

    if not refs:
        issues.append("No `References` heading found.")
    if refs and not ref_entries:
        issues.append("References section found, but no parseable author-year reference entries were detected.")

    missing_refs = sorted(citation for citation in in_text if not has_reference_match(citation, ref_entries, refs))
    uncited_refs = sorted(reference for reference in ref_entries if not has_body_match(reference, in_text, text))
    for author, year in missing_refs:
        issues.append(f"In-text citation may lack matching reference entry: {author} ({year})")
    for author, year in uncited_refs:
        issues.append(f"Reference entry may be uncited in body: {author} ({year})")
    for segment in unresolved_citation_segments:
        issues.append(f"Could not parse possible citation segment: {segment}")
    for doi in doi_like:
        if doi.endswith(".") or doi.endswith(","):
            issues.append(f"DOI may include trailing punctuation: {doi}")
    if "et al" in refs and "et al." not in refs:
        issues.append("Possible inconsistent `et al.` punctuation in references.")

    status = "PASS" if not issues else "REVIEW NEEDED"
    lines = [
        "# Citation Consistency Check",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"File: `{path}`",
        f"Status: `{status}`",
        "",
        "## Summary",
        "",
        f"- Unique in-text author-year citations found: {len(in_text)}",
        f"- Reference entries parsed: {len(ref_entries)}",
        f"- Missing reference-entry matches: {len(missing_refs)}",
        f"- Possibly uncited reference entries: {len(uncited_refs)}",
        f"- DOI-like strings found: {len(doi_like)}",
        f"- Issues: {len(issues)}",
        "",
        "## In-Text Citations Parsed",
        "",
    ]
    if in_text:
        lines.extend(f"- {author} ({year})" for author, year in sorted(in_text))
    else:
        lines.append("- None parsed.")
    lines.extend(["", "## Reference Entries Parsed", ""])
    if ref_entries:
        lines.extend(f"- {author} ({year})" for author, year in sorted(ref_entries))
    else:
        lines.append("- None parsed.")
    lines.extend(["", "## Issues", ""])
    if issues:
        lines.extend(f"- {issue}" for issue in issues)
    else:
        lines.append("- None from this automatic consistency check.")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This automatic check only tests citation/reference consistency patterns. It does not verify whether a source exists in full text, whether metadata is correct, whether a reference follows the exact required style, or whether the cited source supports the attached claim. Use `dissertation-citation-audit` or `scripts/citation_claim_audit.py` for claim-support review.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check citation/reference consistency in Markdown files.")
    parser.add_argument("files", nargs="+")
    parser.add_argument("--output-dir", default=str(OUT_DIR))
    args = parser.parse_args()
    out_dir = Path(args.output_dir)
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    exit_code = 0
    for file_name in args.files:
        path = Path(file_name)
        if not path.is_absolute():
            path = ROOT / path
        report = check_file(path)
        out = out_dir / f"Citation_Consistency_Check_{path.stem}_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.md"
        out.write_text(report, encoding="utf-8")
        print(f"Report: {out}")
        if "- Issues: 0" not in report:
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
