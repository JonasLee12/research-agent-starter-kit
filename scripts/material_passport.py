#!/usr/bin/env python3
"""Create a generic Material Passport for formal research artifacts."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_DIR = ROOT / "research-wiki" / "material-passports"
EVENT_LOG = ROOT / "research-wiki" / "SESSION_EVENT_LOG.jsonl"
SOURCE_READINESS = ROOT / "knowledge-base" / "SOURCE_READINESS_MATRIX.md"
COMPLIANCE_TRACKER = ROOT / "compliance" / "PROJECT_COMPLIANCE_TRACKER.md"
REQUIREMENT_EVIDENCE = ROOT / "quality-gates" / "PROJECT_DELIVERY_REVIEW_GATE.md"


@dataclass
class Passport:
    generated_at: str
    artifact: str
    scope: str
    audience: str
    purpose: str
    status: str
    evidence: dict[str, str]
    missing: list[str]
    to_confirm: list[str]
    notes: str


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return path.name


def resolve(path_text: str | None) -> Path | None:
    if not path_text:
        return None
    path = Path(path_text).expanduser()
    return path if path.is_absolute() else ROOT / path


def default_output(artifact: Path) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
    safe_stem = artifact.stem.replace(" ", "_") or "artifact"
    return DEFAULT_OUT_DIR / f"Material_Passport_{safe_stem}_{stamp}.md"


def status_for(scope: str, missing: list[str]) -> str:
    if not missing:
        return "PASS"
    return "HOLD" if scope == "full" else "WARN"


def evidence_status(label: str, path: Path | None, required: bool, missing: list[str]) -> str:
    if path and path.exists():
        return f"`{rel(path)}`"
    if required:
        missing.append(f"{label}: required evidence missing")
    return "not provided"


def append_event(passport: Passport, output: Path) -> None:
    EVENT_LOG.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "timestamp": passport.generated_at,
        "run_id": f"material-passport-{datetime.now(timezone.utc).strftime('%Y-%m-%d_%H%M%S')}",
        "window": "Maintenance",
        "event_type": "quality_gate",
        "status": "completed" if passport.status != "HOLD" else "failed",
        "skill": "material-passport",
        "file": rel(output),
        "evidence": f"Material Passport {passport.status} for {passport.artifact}.",
        "risk": "low" if passport.status == "PASS" else "medium",
    }
    with EVENT_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def render(passport: Passport) -> str:
    lines = [
        "# Material Passport",
        "",
        f"Generated: {passport.generated_at}",
        f"Artifact: `{passport.artifact}`",
        f"Scope: `{passport.scope}`",
        f"Audience: {passport.audience}",
        f"Purpose: {passport.purpose}",
        f"Status: `{passport.status}`",
        "",
        "## Evidence Package",
        "",
        "| Evidence | Path / Status |",
        "|---|---|",
    ]
    for label, value in passport.evidence.items():
        lines.append(f"| {label} | {value} |")
    lines.extend(["", "## Missing Or Blocking Evidence", ""])
    if passport.missing:
        lines.extend(f"- {item}" for item in passport.missing)
    else:
        lines.append("- None")
    lines.extend(["", "## TO CONFIRM", ""])
    if passport.to_confirm:
        lines.extend(f"- {item}" for item in passport.to_confirm)
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "## Notes",
            "",
            passport.notes or "-",
            "",
            "## Boundary",
            "",
            "This passport packages readiness evidence. It does not prove source support, compliance approval, citation correctness, acceptance, or official requirement compliance.",
            "",
        ]
    )
    return "\n".join(lines)


def build_passport(args: argparse.Namespace) -> tuple[Passport, Path]:
    artifact = resolve(args.artifact)
    if artifact is None:
        raise ValueError("Missing artifact path.")
    output = resolve(args.output) if args.output else default_output(artifact)
    assert output is not None

    missing: list[str] = []
    if not artifact.exists():
        missing.append("artifact: file does not exist yet")

    full_required = args.scope == "full"
    evidence = {
        "artifact": f"`{rel(artifact)}`" if artifact.exists() else "not found",
        "source_readiness": evidence_status("source_readiness", resolve(args.source_readiness), True, missing),
        "compliance_tracker": evidence_status("compliance_tracker", resolve(args.compliance_tracker), args.requires_compliance, missing),
        "requirement_evidence": evidence_status("requirement_evidence", resolve(args.requirement_evidence), args.requires_requirements, missing),
        "citation_report": evidence_status("citation_report", resolve(args.citation_report), args.citation_heavy, missing),
        "runtime_receipt": evidence_status("runtime_receipt", resolve(args.runtime_receipt), full_required, missing),
        "source_map": evidence_status("source_map", resolve(args.source_map), full_required, missing),
        "integrity_report": evidence_status("integrity_report", resolve(args.integrity_report), full_required, missing),
        "quality_gate": evidence_status("quality_gate", resolve(args.quality_gate), full_required, missing),
    }

    passport = Passport(
        generated_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        artifact=rel(artifact),
        scope=args.scope,
        audience=args.audience,
        purpose=args.purpose,
        status=status_for(args.scope, missing),
        evidence=evidence,
        missing=missing,
        to_confirm=args.to_confirm,
        notes=args.notes,
    )
    return passport, output


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Material Passport readiness report.")
    parser.add_argument("--artifact", required=True, help="Artifact path being planned, drafted, reviewed, or delivered.")
    parser.add_argument("--scope", choices=["short", "full"], default="short")
    parser.add_argument("--audience", default="internal draft", help="internal, reviewer-facing, stakeholder-facing, client-facing, or submission-facing.")
    parser.add_argument("--purpose", default="formal artifact readiness check")
    parser.add_argument("--output", help="Output Markdown path.")
    parser.add_argument("--source-readiness", default=str(SOURCE_READINESS))
    parser.add_argument("--compliance-tracker", default=str(COMPLIANCE_TRACKER))
    parser.add_argument("--requirement-evidence", default=str(REQUIREMENT_EVIDENCE))
    parser.add_argument("--citation-report")
    parser.add_argument("--runtime-receipt")
    parser.add_argument("--source-map")
    parser.add_argument("--integrity-report")
    parser.add_argument("--quality-gate")
    parser.add_argument("--requires-compliance", action="store_true")
    parser.add_argument("--requires-requirements", action="store_true")
    parser.add_argument("--citation-heavy", action="store_true")
    parser.add_argument("--to-confirm", action="append", default=[])
    parser.add_argument("--notes", default="")
    parser.add_argument("--no-event", action="store_true", help="Do not append SESSION_EVENT_LOG.jsonl.")
    args = parser.parse_args()

    passport, output = build_passport(args)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(passport), encoding="utf-8")
    if not args.no_event:
        append_event(passport, output)
    print(f"Report: {output}")
    print(f"Status: {passport.status}")
    return 1 if passport.status == "HOLD" else 0


if __name__ == "__main__":
    raise SystemExit(main())
