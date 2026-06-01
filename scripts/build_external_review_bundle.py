#!/usr/bin/env python3
"""Build a local external-review bundle without calling any AI service."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / ".agent-runtime" / "external-review-bundles"
PROMPT_TEMPLATE = ROOT / "templates" / "prompts" / "EXTERNAL_REVIEWER_PROMPT.md"

SENSITIVE_PATH_PATTERNS = [
    r"\braw\b",
    r"transcript",
    r"recording",
    r"signed",
    r"consent",
    r"participant-contact",
    r"participant_data",
    r"\bprivate\b",
    r"secrets?",
]

SENSITIVE_TEXT_PATTERNS = [
    r"\bparticipant\b",
    r"\binterview transcript\b",
    r"\brecording\b",
    r"\bconsent\b",
    r"\bwithdrawal\b",
    r"\banonym",
    r"\bconfidential",
    r"\bdata storage\b",
    r"\bemail\b",
    r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}",
    r"api[_-]?key",
    r"token",
    r"password",
]


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return slug[:80] or "external-review"


def source_label(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return f"outside-repo:{path.name}"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def scan_sensitive(path: Path, text: str) -> list[str]:
    findings: list[str] = []
    label = source_label(path).lower()
    for pattern in SENSITIVE_PATH_PATTERNS:
        if re.search(pattern, label, flags=re.I):
            findings.append(f"path label matches `{pattern}`")
    for pattern in SENSITIVE_TEXT_PATTERNS:
        if re.search(pattern, text, flags=re.I):
            findings.append(f"text matches `{pattern}`")
    return findings


def render_prompt(artifact_path: str, artifact_text: str, review_question: str) -> str:
    template = read_text(PROMPT_TEMPLATE)
    return (
        template.replace("{{REVIEW_QUESTION}}", review_question)
        .replace("{{ARTIFACT_PATH}}", artifact_path)
        .replace("{{ARTIFACT_TEXT}}", artifact_text)
    )


def write_block_report(output_dir: Path, target: Path, findings: list[str]) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    report = output_dir / f"BLOCKED_{slugify(target.stem)}_{stamp}.md"
    lines = [
        "# External Review Bundle Blocked",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Target: `{source_label(target)}`",
        "Status: `BLOCKED`",
        "",
        "## Sensitive Findings",
        "",
        *(f"- {finding}" for finding in findings),
        "",
        "## Boundary",
        "",
        "No artifact copy or review prompt was generated. Use an anonymised artifact, or rerun only with explicit acknowledgement using `--allow-sensitive --override-reason`.",
        "",
    ]
    report.write_text("\n".join(lines), encoding="utf-8")
    return report


def build_bundle(
    target: Path,
    output_dir: Path,
    review_question: str,
    max_chars: int,
    allow_sensitive: bool = False,
    override_reason: str | None = None,
) -> tuple[str, Path, list[str]]:
    target = target.expanduser().resolve()
    output_dir = output_dir.expanduser().resolve()
    if not target.exists() or not target.is_file():
        raise FileNotFoundError(f"target file not found: {target}")
    if allow_sensitive and not override_reason:
        raise ValueError("--override-reason is required with --allow-sensitive")

    text = read_text(target)
    findings = scan_sensitive(target, text)
    if findings and not allow_sensitive:
        return "BLOCKED", write_block_report(output_dir, target, findings), findings

    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    bundle_dir = output_dir / f"{slugify(target.stem)}_{stamp}"
    bundle_dir.mkdir(parents=True, exist_ok=False)

    prompt_text = text[:max_chars]
    truncated = len(text) > max_chars
    label = source_label(target)
    artifact_hash = hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()

    artifact_path = bundle_dir / "artifact.md"
    prompt_path = bundle_dir / "EXTERNAL_REVIEW_PROMPT.md"
    manifest_path = bundle_dir / "manifest.json"
    privacy_path = bundle_dir / "privacy_scan.md"
    readme_path = bundle_dir / "README.md"

    artifact_path.write_text(text, encoding="utf-8")
    prompt_path.write_text(render_prompt(label, prompt_text, review_question), encoding="utf-8")

    privacy_status = "OVERRIDE" if findings and allow_sensitive else "PASS"
    finding_lines = [f"- {finding}" for finding in findings] if findings else ["- None"]
    privacy_lines = [
        "# Privacy Scan",
        "",
        f"Status: `{privacy_status}`",
        f"Target: `{label}`",
        "",
    ]
    if override_reason:
        privacy_lines.extend([f"Override reason: {override_reason}", ""])
    privacy_lines.extend(
        [
            "## Findings",
            "",
            *finding_lines,
            "",
            "## Boundary",
            "",
            "This scan catches common risks only. Review the artifact manually before sending it to any external model or person.",
            "",
        ]
    )
    privacy_path.write_text("\n".join(privacy_lines), encoding="utf-8")

    manifest = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "status": privacy_status,
        "source_label": label,
        "source_name": target.name,
        "artifact_sha256": artifact_hash,
        "artifact_copy": artifact_path.name,
        "review_prompt": prompt_path.name,
        "privacy_scan": privacy_path.name,
        "input_truncated_in_prompt": truncated,
        "max_chars": max_chars,
        "sensitive_findings": findings,
        "sensitive_override": allow_sensitive,
        "override_reason": override_reason or "",
        "boundary": [
            "The bundle is local and was not sent to any AI service.",
            "External reviewer feedback is advisory only.",
            "Reviewer feedback does not prove source support, citation readiness, compliance, marks, or approval.",
        ],
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    readme_path.write_text(
        "\n".join(
            [
                "# External Review Bundle",
                "",
                "This folder was generated locally. Nothing was uploaded or sent to an AI service by the bundle builder.",
                "",
                "Use `EXTERNAL_REVIEW_PROMPT.md` with a separate Codex, ChatGPT, Claude, Gemini, or human reviewer.",
                "",
                "Before pasting anything into an external tool, read `privacy_scan.md` and inspect `artifact.md` yourself.",
                "",
                "Reviewer feedback is advisory. It is not source evidence, citation verification, compliance approval, a grade, or a delivery pass.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    return "PASS", bundle_dir, findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a local external-review bundle for Codex, ChatGPT, Claude, Gemini, or human review.")
    parser.add_argument("target", help="Markdown or text artifact to review.")
    parser.add_argument("--review-question", default="Review this artifact for argument quality, evidence risks, clarity, privacy risks, and concrete revision priorities.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Folder where the local review bundle should be created.")
    parser.add_argument("--max-chars", type=int, default=45000, help="Maximum artifact characters embedded into the review prompt.")
    parser.add_argument("--allow-sensitive", action="store_true", help="Generate a bundle despite sensitive scan findings.")
    parser.add_argument("--override-reason", help="Required when --allow-sensitive is used.")
    args = parser.parse_args()

    try:
        status, path, findings = build_bundle(
            target=Path(args.target),
            output_dir=Path(args.output_dir),
            review_question=args.review_question,
            max_chars=args.max_chars,
            allow_sensitive=args.allow_sensitive,
            override_reason=args.override_reason,
        )
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 2

    print(f"Status: {status}")
    if findings:
        print("Sensitive findings:")
        for finding in findings:
            print(f"- {finding}")
    if status == "BLOCKED":
        print(f"Report: {path}")
        return 1
    print(f"Bundle: {path}")
    print("Next: read privacy_scan.md, then copy EXTERNAL_REVIEW_PROMPT.md into your chosen reviewer if safe.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
