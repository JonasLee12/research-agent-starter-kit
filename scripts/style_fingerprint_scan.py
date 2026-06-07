#!/usr/bin/env python3
"""Scan academic prose for mechanical binary negative-contrast overuse.

This is a style-density scanner, not an AI detector.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class PatternSpec:
    category: str
    language: str
    pattern: re.Pattern[str]


@dataclass(frozen=True)
class Finding:
    category: str
    language: str
    line: int
    match: str
    context: str


ENGLISH_PATTERNS: list[PatternSpec] = [
    PatternSpec("rather than", "en", re.compile(r"\brather than\b", re.I)),
    PatternSpec("not just ... but", "en", re.compile(r"\bnot\s+just\b.{0,160}?\bbut\b", re.I)),
    PatternSpec("not only ... but", "en", re.compile(r"\bnot\s+only\b.{0,180}?\bbut\b", re.I)),
    PatternSpec("it's not ... it's", "en", re.compile(r"\bit'?s\s+not\b.{0,180}?\bit'?s\b", re.I)),
    PatternSpec("isn't about ... it's about", "en", re.compile(r"\bisn'?t\s+about\b.{0,180}?\bit'?s\s+about\b", re.I)),
    PatternSpec("not ... but rather", "en", re.compile(r"\bnot\b.{0,160}?\bbut\s+rather\b", re.I)),
    PatternSpec("not ... but", "en", re.compile(r"\bnot\b.{0,140}?\bbut\b", re.I)),
    PatternSpec("as opposed to", "en", re.compile(r"\bas\s+opposed\s+to\b", re.I)),
    PatternSpec("instead of ... it", "en", re.compile(r"\binstead\s+of\b.{0,160}?\bit\b", re.I)),
]


CHINESE_PATTERNS: list[PatternSpec] = [
    PatternSpec("并不是……而是", "zh", re.compile(r"并不是[^。！？；;\n]{0,80}?而是")),
    PatternSpec("并非……而是", "zh", re.compile(r"并非[^。！？；;\n]{0,80}?而是")),
    PatternSpec("不是……而是", "zh", re.compile(r"不是[^。！？；;\n]{0,80}?而是")),
    PatternSpec("不是……而不是", "zh", re.compile(r"不是[^。！？；;\n]{0,80}?而不是")),
    PatternSpec("而不是", "zh", re.compile(r"而不是")),
    PatternSpec("而非", "zh", re.compile(r"而非")),
    PatternSpec("不仅……而是", "zh", re.compile(r"不仅[^。！？；;\n]{0,80}?而是")),
    PatternSpec("与其说……不如说", "zh", re.compile(r"与其说[^。！？；;\n]{0,80}?不如说")),
    PatternSpec("不在于……而在于", "zh", re.compile(r"不在于[^。！？；;\n]{0,80}?而在于")),
]


def resolve(path_text: str) -> Path:
    path = Path(path_text).expanduser()
    return path if path.is_absolute() else ROOT / path


def selected_patterns(lang: str) -> list[PatternSpec]:
    if lang == "en":
        return ENGLISH_PATTERNS
    if lang == "zh":
        return CHINESE_PATTERNS
    return ENGLISH_PATTERNS + CHINESE_PATTERNS


def estimate_words(text: str, lang: str) -> float:
    english_words = re.findall(r"[A-Za-z]+(?:[-'][A-Za-z]+)?|\d+", text)
    chinese_chars = re.findall(r"[\u4e00-\u9fff]", text)
    if lang == "en":
        return max(1.0, float(len(english_words)))
    if lang == "zh":
        return max(1.0, len(chinese_chars) / 1.6)
    return max(1.0, float(len(english_words)) + (len(chinese_chars) / 1.6))


def line_context(line: str, start: int, end: int, width: int = 90) -> str:
    left = max(0, start - width)
    right = min(len(line), end + width)
    prefix = "..." if left > 0 else ""
    suffix = "..." if right < len(line) else ""
    return f"{prefix}{line[left:right].strip()}{suffix}"


def scan(text: str, lang: str) -> list[Finding]:
    patterns = selected_patterns(lang)
    findings: list[Finding] = []
    in_fence = False
    in_yaml_frontmatter = False
    frontmatter_checked = False
    in_reference_section = False
    lines = text.splitlines()
    for line_no, line in enumerate(lines, 1):
        stripped = line.strip()
        if line_no == 1 and stripped == "---":
            in_yaml_frontmatter = True
            frontmatter_checked = True
            continue
        if in_yaml_frontmatter:
            if stripped == "---":
                in_yaml_frontmatter = False
            continue
        if not frontmatter_checked and stripped:
            frontmatter_checked = True
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        reference_heading = re.match(r"^(?:#{1,6}\s+)?(references|bibliography|reference list|works cited|参考文献)\s*$", stripped, flags=re.I)
        next_is_setext = line_no < len(lines) and re.match(r"^\s*[=-]{3,}\s*$", lines[line_no] or "")
        if reference_heading or (stripped.lower() in {"references", "bibliography", "reference list", "works cited", "参考文献"} and next_is_setext):
            in_reference_section = True
            continue
        if in_reference_section:
            continue
        if stripped.startswith(">"):
            continue
        occupied_spans: list[tuple[int, int]] = []
        for spec in patterns:
            for match in spec.pattern.finditer(line):
                span = match.span()
                if any(not (span[1] <= used[0] or span[0] >= used[1]) for used in occupied_spans):
                    continue
                occupied_spans.append(span)
                findings.append(
                    Finding(
                        category=spec.category,
                        language=spec.language,
                        line=line_no,
                        match=match.group(0).strip(),
                        context=line_context(line, match.start(), match.end()),
                    )
                )
    return findings


def grouped_counts(findings: list[Finding]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in findings:
        key = f"{item.language}:{item.category}"
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))


def status_for(
    findings: list[Finding],
    words: float,
    threshold: float,
    review_threshold: float,
    max_hits: int,
    max_category_hits: int,
) -> tuple[str, list[str]]:
    density = len(findings) / words * 1000.0
    counts = grouped_counts(findings)
    fail_reasons: list[str] = []
    if density > threshold:
        fail_reasons.append(f"density {density:.2f} exceeds threshold {threshold:.2f}")
    if len(findings) > max_hits:
        fail_reasons.append(f"total hits {len(findings)} exceed max hits {max_hits}")
    repeated = [f"{category}={count}" for category, count in counts.items() if count > max_category_hits]
    if repeated:
        fail_reasons.append(f"category repetition exceeds max {max_category_hits}: {', '.join(repeated)}")
    if fail_reasons:
        return "FAIL", fail_reasons

    review_reasons: list[str] = []
    if density > review_threshold:
        review_reasons.append(f"density {density:.2f} exceeds review threshold {review_threshold:.2f}")
    review_limit = max(2, max_category_hits // 2)
    review_repeated = [f"{category}={count}" for category, count in counts.items() if count > review_limit]
    if review_repeated:
        review_reasons.append(f"category repetition needs review: {', '.join(review_repeated)}")
    if review_reasons:
        return "REVIEW", review_reasons
    return "PASS", []


def render_report(
    path: Path,
    text: str,
    lang: str,
    threshold: float,
    review_threshold: float,
    max_hits: int,
    max_category_hits: int,
    findings: list[Finding],
) -> str:
    words = estimate_words(text, lang)
    density = len(findings) / words * 1000.0
    status, reasons = status_for(findings, words, threshold, review_threshold, max_hits, max_category_hits)
    lines = [
        "# Style Fingerprint Scan",
        "",
        f"Target: `{path}`",
        f"Language mode: `{lang}`",
        f"Estimated words: `{words:.1f}`",
        f"Total negative-contrast hits: `{len(findings)}`",
        f"Density per 1000 words: `{density:.2f}`",
        f"Threshold: `{threshold:.2f}`",
        f"Review threshold: `{review_threshold:.2f}`",
        f"Max total hits: `{max_hits}`",
        f"Max hits per category: `{max_category_hits}`",
        f"Status: `{status}`",
        "",
        "## Status Reasons",
        "",
    ]
    if reasons:
        for reason in reasons:
            lines.append(f"- {reason}")
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "## Hits By Category",
            "",
        ]
    )
    counts = grouped_counts(findings)
    if counts:
        for category, count in counts.items():
            lines.append(f"- `{category}`: {count}")
    else:
        lines.append("- None")
    lines.extend(["", "## Findings", ""])
    if findings:
        lines.extend(["| Line | Language | Category | Match | Context |", "|---:|---|---|---|---|"])
        for item in findings:
            match = item.match.replace("|", "\\|")
            context = item.context.replace("|", "\\|")
            lines.append(f"| {item.line} | {item.language} | {item.category} | {match} | {context} |")
    else:
        lines.append("- No binary negative-contrast constructions found.")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This scanner detects repeated binary negative-contrast constructions. It is not an AI detector and should not be used to make authorship claims. A small number of genuine scope distinctions can be academically legitimate.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan text for binary negative-contrast style fingerprints.")
    parser.add_argument("file", help="Path to a .md, .txt, or extracted .docx text file.")
    parser.add_argument("--threshold", type=float, default=3.0, help="Maximum allowed hits per 1000 estimated words.")
    parser.add_argument("--review-threshold", type=float, default=1.5, help="Density level that should be reviewed but does not hard fail.")
    parser.add_argument("--max-hits", type=int, default=12, help="Maximum total hits before hard fail, regardless of document length.")
    parser.add_argument("--max-category-hits", type=int, default=6, help="Maximum repeated hits for one pattern category before hard fail.")
    parser.add_argument("--lang", choices=["auto", "en", "zh", "both"], default="auto")
    parser.add_argument("--strict", action="store_true", help="Exit 1 when hard-fail thresholds are exceeded.")
    args = parser.parse_args()

    target = resolve(args.file)
    if not target.exists():
        print(f"Missing file: {target}", file=sys.stderr)
        return 2
    if not target.is_file():
        print(f"Target is not a file: {target}", file=sys.stderr)
        return 2

    lang = "both" if args.lang == "auto" else args.lang
    text = target.read_text(encoding="utf-8", errors="replace")
    findings = scan(text, lang)
    report = render_report(target, text, lang, args.threshold, args.review_threshold, args.max_hits, args.max_category_hits, findings)
    print(report)

    status, _ = status_for(
        findings,
        estimate_words(text, lang),
        args.threshold,
        args.review_threshold,
        args.max_hits,
        args.max_category_hits,
    )
    failed = status == "FAIL"
    if args.strict and failed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
