#!/usr/bin/env python3
"""Create and verify pre-delivery locks for formal research artifacts.

Lock JSON files store private absolute paths inside .agent-runtime so stale
evidence can be checked. The Markdown receipt keeps safer display labels.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCK_DIR = ROOT / ".agent-runtime" / "pre-delivery-locks"
RECEIPT_DIR = ROOT / "research-wiki" / "pre-delivery-locks"
EVENT_LOG = ROOT / "research-wiki" / "SESSION_EVENT_LOG.jsonl"


@dataclass
class DeliveryLock:
    version: int
    created_at: str
    target: str
    target_hash: str
    artifact_type: str
    status: str
    evidence: dict[str, list[str]]
    private_paths: dict[str, list[str]]
    missing: list[str]
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


def collect(paths: list[str] | None) -> list[Path]:
    output: list[Path] = []
    for item in paths or []:
        path = resolve(item)
        if path is not None:
            output.append(path)
    return output


def lock_name(target: Path) -> str:
    return hashlib.sha256(str(target.resolve()).encode("utf-8")).hexdigest()[:16]


def lock_path(target: Path) -> Path:
    return LOCK_DIR / f"{lock_name(target)}.json"


def receipt_path(target: Path) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
    return RECEIPT_DIR / f"Pre_Delivery_Lock_{target.stem.replace(' ', '_')}_{stamp}.md"


def append_event(lock: DeliveryLock, report: Path) -> None:
    EVENT_LOG.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "timestamp": lock.created_at,
        "run_id": f"pre-delivery-lock-{lock.target_hash}",
        "window": "Maintenance",
        "event_type": "pre_delivery_lock",
        "status": "completed" if lock.status == "PASS" else "failed",
        "skill": "formal-delivery-guard",
        "file": rel(report),
        "evidence": f"Pre-delivery lock {lock.status} for {lock.target}.",
        "risk": "low" if lock.status == "PASS" else "medium",
    }
    with EVENT_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def render_receipt(lock: DeliveryLock) -> str:
    lines = [
        "# Pre-Delivery Lock",
        "",
        f"Created: {lock.created_at}",
        f"Target: `{lock.target}`",
        f"Artifact type: `{lock.artifact_type}`",
        f"Status: `{lock.status}`",
        "",
        "## Evidence",
        "",
    ]
    for group, items in lock.evidence.items():
        lines.append(f"### {group}")
        lines.append("")
        if items:
            lines.extend(f"- `{item}`" for item in items)
        else:
            lines.append("- None")
        lines.append("")
    lines.extend(["## Missing", ""])
    if lock.missing:
        lines.extend(f"- `{item}`" for item in lock.missing)
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This lock verifies that required gate artifacts exist before formal delivery. It does not prove academic quality, source support, approval, acceptance, or official compliance.",
            "",
            "## Notes",
            "",
            lock.notes or "-",
            "",
        ]
    )
    return "\n".join(lines)


def required_groups(args: argparse.Namespace) -> list[str]:
    groups = ["runtime_receipt", "material_passport", "source_map", "integrity_preflight", "quality_gate"]
    if args.require_project_delivery_review:
        groups.append("project_delivery_review")
    if args.require_citation:
        groups.append("citation_report")
    if args.require_compliance:
        groups.append("compliance_tracker")
    if args.require_requirements:
        groups.append("requirement_evidence")
    if args.require_render_check:
        groups.append("render_check")
    return groups


def build_lock(args: argparse.Namespace) -> tuple[DeliveryLock, Path, Path]:
    target = resolve(args.target)
    if target is None:
        raise ValueError("Missing target path.")

    evidence_paths = {
        "runtime_receipt": collect(args.runtime_receipt),
        "material_passport": collect(args.material_passport),
        "source_map": collect(args.source_map),
        "integrity_preflight": collect(args.integrity_preflight),
        "quality_gate": collect(args.quality_gate),
        "project_delivery_review": collect(args.project_delivery_review),
        "citation_report": collect(args.citation_report),
        "compliance_tracker": collect(args.compliance_tracker),
        "requirement_evidence": collect(args.requirement_evidence),
        "render_check": collect(args.render_check),
    }

    missing: list[str] = []
    if not target.exists():
        missing.append(f"target: {rel(target)}")

    for group in required_groups(args):
        paths = evidence_paths[group]
        if not paths:
            missing.append(f"{group}: no file provided")
        for path in paths:
            if not path.exists():
                missing.append(f"{group}: {rel(path)}")

    for group, paths in evidence_paths.items():
        if group in required_groups(args):
            continue
        for path in paths:
            if not path.exists():
                missing.append(f"{group}: {rel(path)}")

    lock = DeliveryLock(
        version=1,
        created_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        target=rel(target),
        target_hash=lock_name(target),
        artifact_type=args.artifact_type,
        status="PASS" if not missing else "BLOCKED",
        evidence={group: [rel(path) for path in paths] for group, paths in evidence_paths.items()},
        private_paths={group: [str(path.resolve()) for path in paths] for group, paths in evidence_paths.items()},
        missing=missing,
        notes=args.notes or "",
    )
    return lock, lock_path(target), receipt_path(target)


def create(args: argparse.Namespace) -> int:
    lock, json_path, report_path = build_lock(args)
    LOCK_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(asdict(lock), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_path.write_text(render_receipt(lock), encoding="utf-8")
    if not args.no_event:
        append_event(lock, report_path)
    print(f"Lock: {json_path}")
    print(f"Receipt: {report_path}")
    print(f"Status: {lock.status}")
    return 0 if lock.status == "PASS" else 1


def check(args: argparse.Namespace) -> int:
    target = resolve(args.target)
    if target is None:
        print("Missing target path.")
        return 2
    path = lock_path(target)
    if not path.exists():
        print(f"Missing pre-delivery lock for {rel(target)}")
        return 1
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("private_paths", data.get("evidence", {}))
    lock = DeliveryLock(**data)
    if lock.status != "PASS":
        print(f"Pre-delivery lock is not PASS: {lock.status}")
        for item in lock.missing:
            print(f"- {item}")
        return 1

    missing: list[str] = []
    paths_for_check = lock.private_paths or lock.evidence
    for group, items in paths_for_check.items():
        for item in items:
            evidence_path = resolve(item)
            if evidence_path is not None and not evidence_path.exists():
                display = lock.evidence.get(group, [item])[0] if lock.evidence.get(group) else item
                missing.append(f"{group}: {display}")
    for group in required_groups(args):
        if not lock.evidence.get(group):
            missing.append(f"{group}: no file recorded")
    if missing:
        print("Pre-delivery lock evidence is stale or incomplete:")
        for item in missing:
            print(f"- {item}")
        return 1
    print(f"Pre-delivery lock PASS for {lock.target}")
    return 0


def add_common_requirements(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--require-project-delivery-review", action="store_true")
    parser.add_argument("--require-citation", action="store_true")
    parser.add_argument("--require-compliance", action="store_true")
    parser.add_argument("--require-requirements", action="store_true")
    parser.add_argument("--require-render-check", action="store_true")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create/check pre-delivery locks for formal research artifacts.")
    sub = parser.add_subparsers(dest="command", required=True)

    create_p = sub.add_parser("create", help="Create a pre-delivery lock after required gate artifacts exist.")
    create_p.add_argument("--target", required=True)
    create_p.add_argument("--artifact-type", default="formal-artifact")
    create_p.add_argument("--runtime-receipt", action="append")
    create_p.add_argument("--material-passport", action="append")
    create_p.add_argument("--source-map", action="append")
    create_p.add_argument("--integrity-preflight", action="append")
    create_p.add_argument("--quality-gate", action="append")
    create_p.add_argument("--project-delivery-review", action="append")
    create_p.add_argument("--citation-report", action="append")
    create_p.add_argument("--compliance-tracker", action="append")
    create_p.add_argument("--requirement-evidence", action="append")
    create_p.add_argument("--render-check", action="append")
    create_p.add_argument("--notes")
    create_p.add_argument("--no-event", action="store_true")
    add_common_requirements(create_p)

    check_p = sub.add_parser("check", help="Check an existing pre-delivery lock.")
    check_p.add_argument("--target", required=True)
    add_common_requirements(check_p)

    args = parser.parse_args()
    if args.command == "create":
        return create(args)
    if args.command == "check":
        return check(args)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
