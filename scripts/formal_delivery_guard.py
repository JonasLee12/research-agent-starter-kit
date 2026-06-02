#!/usr/bin/env python3
"""Final deterministic guard before delivering formal research artifacts."""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "audit-reports" / "formal-delivery-guard"
OVERRIDE_DIR = ROOT / "audit-reports" / "delivery-overrides"


@dataclass
class GuardResult:
    name: str
    status: str
    evidence: str


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


def run_command(command: list[str]) -> tuple[int, str]:
    proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    output = "\n".join(item for item in [proc.stdout.strip(), proc.stderr.strip()] if item)
    return proc.returncode, output


def guard_lock(args: argparse.Namespace, artifact: Path) -> GuardResult:
    command = [sys.executable, "scripts/pre_delivery_lock.py", "check", "--target", str(artifact)]
    if args.require_project_delivery_review:
        command.append("--require-project-delivery-review")
    if args.require_citation:
        command.append("--require-citation")
    if args.require_compliance:
        command.append("--require-compliance")
    if args.require_requirements:
        command.append("--require-requirements")
    if args.require_render_check:
        command.append("--require-render-check")
    code, output = run_command(command)
    return GuardResult("pre_delivery_lock", "PASS" if code == 0 else "BLOCK", output)


def guard_integrity(source: Path, args: argparse.Namespace) -> GuardResult:
    command = [
        sys.executable,
        "scripts/academic_integrity_preflight.py",
        "--target",
        str(source),
        "--stage",
        "final",
        "--strict",
    ]
    if args.require_compliance:
        command.extend(["--requires-ethics", "--ethics-evidence", "compliance/PROJECT_COMPLIANCE_TRACKER.md"])
    if args.require_requirements:
        command.extend(["--requires-rubric", "--rubric-evidence", "quality-gates/PROJECT_DELIVERY_REVIEW_GATE.md"])
    if args.require_citation:
        command.append("--citation-heavy")
    code, output = run_command(command)
    return GuardResult("academic_integrity_preflight", "PASS" if code == 0 else "BLOCK", output)


def guard_citations(source: Path, fail_on_attention: bool) -> GuardResult:
    command = [
        sys.executable,
        "scripts/citation_claim_audit.py",
        str(source),
        "--output-dir",
        "audit-reports",
    ]
    if fail_on_attention:
        command.append("--fail-on-attention")
    code, output = run_command(command)
    return GuardResult("citation_claim_support_queue", "PASS" if code == 0 else "BLOCK", output)


def render_report(artifact: Path, source: Path | None, results: list[GuardResult], override_path: Path | None) -> str:
    base_status = "PASS" if all(item.status == "PASS" for item in results) else "BLOCKED"
    status = "OVERRIDE_ACKNOWLEDGED" if override_path else base_status
    lines = [
        "# Formal Delivery Guard",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"Status: `{status}`",
        f"Artifact: `{rel(artifact)}`",
        f"Source: `{rel(source) if source else '-'}`",
        f"Override record: `{rel(override_path) if override_path else '-'}`",
        "",
        "## Results",
        "",
        "| Check | Status | Evidence |",
        "|---|---|---|",
    ]
    for item in results:
        evidence = item.evidence.replace("|", "\\|").replace("\n", "<br>")
        lines.append(f"| {item.name} | {item.status} | {evidence or '-'} |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This guard blocks delivery when required gate evidence is missing or final artifact checks fail. A user-acknowledged override records a conscious exception; it does not convert unresolved evidence into verified evidence.",
            "",
        ]
    )
    return "\n".join(lines)


def render_override(artifact: Path, source: Path | None, results: list[GuardResult], reason: str) -> str:
    blocked = [item for item in results if item.status != "PASS"]
    lines = [
        "# Delivery Override",
        "",
        f"Created: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"Artifact: `{rel(artifact)}`",
        f"Source: `{rel(source) if source else '-'}`",
        "",
        "## Acknowledgement",
        "",
        "The delivery guard found unresolved issues. The user explicitly acknowledged the risk and chose to continue with an auditable exception.",
        "",
        "## Reason",
        "",
        reason.strip(),
        "",
        "## Blocked Checks",
        "",
    ]
    if blocked:
        for item in blocked:
            lines.extend([f"### {item.name}", "", f"Status: `{item.status}`", "", item.evidence or "-", ""])
    else:
        lines.append("- None")
    lines.extend(
        [
            "## Boundary",
            "",
            "This override is a traceability record, not a quality approval. Future work should resolve the blocked checks when time allows.",
            "",
        ]
    )
    return "\n".join(lines)


def write_override(artifact: Path, source: Path | None, results: list[GuardResult], reason: str) -> Path:
    OVERRIDE_DIR.mkdir(parents=True, exist_ok=True)
    out = OVERRIDE_DIR / f"DELIVERY_OVERRIDE_{datetime.now(timezone.utc).strftime('%Y-%m-%d_%H%M%S')}_{artifact.stem}.md"
    out.write_text(render_override(artifact, source, results, reason), encoding="utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Run final deterministic checks before delivering a formal research artifact.")
    parser.add_argument("--artifact", required=True, help="Formal artifact path, such as a .docx, .pdf, or final Markdown file.")
    parser.add_argument("--source", help="Markdown/text source path for final integrity and citation checks.")
    parser.add_argument("--require-project-delivery-review", action="store_true")
    parser.add_argument("--require-citation", action="store_true")
    parser.add_argument("--require-compliance", action="store_true")
    parser.add_argument("--require-requirements", action="store_true")
    parser.add_argument("--require-render-check", action="store_true")
    parser.add_argument("--fail-on-claim-attention", action="store_true")
    parser.add_argument("--skip-integrity-preflight", action="store_true")
    parser.add_argument("--acknowledge-override", action="store_true")
    parser.add_argument("--override-reason")
    args = parser.parse_args()

    artifact = resolve(args.artifact)
    source = resolve(args.source)
    if artifact is None or not artifact.exists():
        print(f"Missing artifact: {args.artifact}")
        return 1
    if args.source and (source is None or not source.exists()):
        print(f"Missing source: {args.source}")
        return 1

    results = [guard_lock(args, artifact)]
    if source is not None and not args.skip_integrity_preflight:
        results.append(guard_integrity(source, args))
    if source is not None:
        results.append(guard_citations(source, args.fail_on_claim_attention))

    blocked = not all(item.status == "PASS" for item in results)
    override_path = None
    if blocked and args.acknowledge_override:
        if not args.override_reason or not args.override_reason.strip():
            print("--override-reason is required when --acknowledge-override is used for blocked delivery.")
            return 2
        override_path = write_override(artifact, source, results, args.override_reason)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report = OUT_DIR / f"Formal_Delivery_Guard_{artifact.stem}_{datetime.now(timezone.utc).strftime('%Y-%m-%d_%H%M%S')}.md"
    report.write_text(render_report(artifact, source, results, override_path), encoding="utf-8")
    print(f"Report: {report}")
    if override_path:
        print(f"Override: {override_path}")
    for item in results:
        print(f"{item.name}: {item.status}")
    if override_path:
        print("delivery_override: ACKNOWLEDGED")
        return 0
    return 0 if not blocked else 1


if __name__ == "__main__":
    raise SystemExit(main())
