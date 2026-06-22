#!/usr/bin/env python3
"""Validate Claim Ledger Lite artifacts for research-agent outputs."""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "audit-reports" / "claim-ledger-lite"

REQUIRED_COLUMNS = {
    "claim_id",
    "claim",
    "output_location",
    "source_anchor",
    "evidence_status",
    "cannot_prove",
    "concept_contract",
    "allowed_wording",
    "review_action",
}

ALLOWED_STATUS = {
    "direct support",
    "partial support",
    "background only",
    "metadata only",
    "insufficient",
    "source needed",
    "to confirm",
}

HIGH_RISK_TERMS = (
    "implementation",
    "user-created",
    "user created",
    "researcher-created",
    "researcher created",
    "customised",
    "customized",
    "adoption condition",
    "responsible ai",
    "user agency",
    "autonomy",
    "trust",
    "workload",
    "professional identity",
    "safety",
    "effectiveness",
    "impact",
    "causal",
    "significant",
    "risk",
)


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def normalise(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.strip().strip("`").lower()).strip("_")


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def extract_table(text: str) -> tuple[list[str], list[dict[str, str]]]:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not line.strip().startswith("|"):
            continue
        header = split_table_row(line)
        if not header:
            continue
        normalised = [normalise(cell) for cell in header]
        if "claim_id" not in normalised or "evidence_status" not in normalised:
            continue
        if index + 1 >= len(lines) or not re.match(r"^\s*\|?\s*:?-{3,}", lines[index + 1]):
            continue
        rows: list[dict[str, str]] = []
        for row_line in lines[index + 2 :]:
            if not row_line.strip().startswith("|"):
                break
            cells = split_table_row(row_line)
            if len(cells) < len(normalised):
                cells.extend([""] * (len(normalised) - len(cells)))
            rows.append(dict(zip(normalised, cells[: len(normalised)])))
        return normalised, rows
    return [], []


def empty(value: str) -> bool:
    return value.strip().lower() in {"", "-", "n/a", "na", "none", "tbc", "to be confirmed"}


def has_path_or_source_needed(value: str) -> bool:
    lowered = value.lower()
    if "source needed" in lowered or "to confirm" in lowered:
        return True
    if re.search(r"`[^`]+`", value):
        return True
    return bool(re.search(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_./ -]+\.(?:md|pdf|docx|txt|jsonl?)", value))


def check(path: Path) -> tuple[str, list[str], list[dict[str, str]]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    issues: list[str] = []
    if "claim ledger lite" not in text.lower():
        issues.append("missing `Claim Ledger Lite` heading or label")
    columns, rows = extract_table(text)
    missing_columns = sorted(REQUIRED_COLUMNS - set(columns))
    if missing_columns:
        issues.append("missing column(s): " + ", ".join(missing_columns))
    if not rows:
        issues.append("no claim rows found")

    seen_ids: set[str] = set()
    for row_index, row in enumerate(rows, 1):
        claim_id = row.get("claim_id", "")
        if not re.fullmatch(r"CLM-\d{3}", claim_id.strip()):
            issues.append(f"row {row_index}: claim_id must match CLM-001 style")
        if claim_id in seen_ids:
            issues.append(f"row {row_index}: duplicate claim_id {claim_id}")
        seen_ids.add(claim_id)
        for column in REQUIRED_COLUMNS:
            value = row.get(column, "")
            if empty(value):
                issues.append(f"row {row_index}: empty `{column}`")
        status = row.get("evidence_status", "").strip().lower()
        status_clean = re.sub(r"\s+", " ", status)
        if status_clean not in ALLOWED_STATUS:
            issues.append(f"row {row_index}: invalid evidence_status `{row.get('evidence_status', '')}`")
        if "citation-ready" in " ".join(row.values()).lower():
            issues.append(f"row {row_index}: ledger must not declare citation-ready status")
        if status_clean in {"direct support", "partial support", "background only"} and not has_path_or_source_needed(row.get("source_anchor", "")):
            issues.append(f"row {row_index}: source_anchor needs a concrete path or source-needed boundary")
        combined_claim = f"{row.get('claim', '')} {row.get('allowed_wording', '')}".lower()
        concept = row.get("concept_contract", "")
        if any(term in combined_claim for term in HIGH_RISK_TERMS) and empty(concept):
            issues.append(f"row {row_index}: high-risk concept needs a concept_contract")
        if status_clean in {"metadata only", "insufficient", "source needed", "to confirm"}:
            wording = row.get("allowed_wording", "").lower()
            if not any(token in wording for token in ["may", "might", "cannot", "to confirm", "source needed", "insufficient", "metadata", "do not", "avoid"]):
                issues.append(f"row {row_index}: weak evidence needs cautious allowed_wording")
    status = "PASS" if not issues else "BLOCK"
    return status, issues, rows


def render_report(target: Path, status: str, issues: list[str], rows: list[dict[str, str]]) -> str:
    lines = [
        "# Claim Ledger Lite Check",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Target: `{rel(target)}`",
        f"Status: `{status}`",
        f"Rows checked: `{len(rows)}`",
        "",
        "## Issues",
        "",
    ]
    if issues:
        lines.extend(f"- {issue}" for issue in issues)
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This check validates claim-ledger structure and boundary fields. It does not prove source support, citation readiness, compliance readiness, rubric/journal/client requirement compliance, or document quality.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Claim Ledger Lite markdown artifact.")
    parser.add_argument("target", help="Markdown file containing Claim Ledger Lite.")
    parser.add_argument("--no-report", action="store_true", help="Do not write a markdown report.")
    args = parser.parse_args()

    target = Path(args.target)
    if not target.is_absolute():
        target = ROOT / target
    status, issues, rows = check(target)
    report = render_report(target, status, issues, rows)
    if not args.no_report:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        out = OUT_DIR / f"Claim_Ledger_Lite_Check_{target.stem}_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.md"
        out.write_text(report, encoding="utf-8")
        print(f"Report: {out}")
    print(f"status: {status}")
    for issue in issues:
        print(f"- {issue}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
