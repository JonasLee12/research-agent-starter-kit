#!/usr/bin/env python3
"""Create and verify machine-checkable skill execution receipts.

The receipt layer closes the gap between "a skill was selected" and "a skill
left auditable evidence". It does not judge academic quality by itself; it
verifies that required gate artifacts exist and have not silently disappeared.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = ROOT / ".agent-runtime" / "skill-receipts"
HUMAN_DIR = ROOT / "research-wiki" / "skill-receipts"
CHECK_DIR = ROOT / "audit-reports" / "skill-receipts"
EVENT_LOG = ROOT / "research-wiki" / "SESSION_EVENT_LOG.jsonl"

PASSING_STATUSES = {"PASS", "WARN", "NA"}
MAINTENANCE_WINDOW_HINTS = [
    "maintenance",
    "system_maintenance",
    "audit",
    "runtime",
    "routing",
    "skill-change",
    "skill change",
    "release",
    "github",
    "public-sync",
    "public sync",
]


@dataclass
class EvidenceRecord:
    path: str
    exists: bool
    sha256: str | None


@dataclass
class SkillReceipt:
    version: int
    created_at: str
    task_id: str
    window: str
    task_type: str
    stage: str
    skill: str
    artifact: str
    status: str
    evidence: list[EvidenceRecord]
    command: str
    notes: str


def slugify(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", text.strip()).strip("-")
    return slug[:96] or "receipt"


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def resolve(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else ROOT / path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def evidence_record(path_text: str) -> EvidenceRecord:
    path = resolve(path_text)
    exists = path.exists()
    return EvidenceRecord(path=rel(path), exists=exists, sha256=sha256(path) if exists and path.is_file() else None)


def infer_window(explicit_window: str | None, task_type: str, stage: str, task_id: str) -> str:
    if explicit_window:
        return explicit_window
    haystack = " ".join([task_type or "", stage or "", task_id or ""]).lower()
    if any(hint in haystack for hint in MAINTENANCE_WINDOW_HINTS):
        return "Maintenance"
    return "Production"


def receipt_runtime_path(receipt: SkillReceipt) -> Path:
    name = "_".join(
        [
            slugify(receipt.task_id),
            slugify(receipt.stage),
            slugify(receipt.skill),
            datetime.now().strftime("%Y%m%d%H%M%S"),
        ]
    )
    return RUNTIME_DIR / f"{name}.json"


def receipt_human_path(receipt: SkillReceipt) -> Path:
    name = "_".join(
        [
            "Skill_Receipt",
            slugify(receipt.task_id),
            slugify(receipt.stage),
            slugify(receipt.skill),
            datetime.now().strftime("%Y-%m-%d_%H%M%S"),
        ]
    )
    return HUMAN_DIR / f"{name}.md"


def append_event(receipt: SkillReceipt, event_type: str, status: str, evidence: str, risk: str = "low") -> None:
    EVENT_LOG.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "run_id": receipt.task_id,
        "window": receipt.window,
        "event_type": event_type,
        "status": status,
        "skill": receipt.skill,
        "file": "scripts/skill_execution_receipt.py",
        "evidence": evidence,
        "risk": risk,
    }
    with EVENT_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def render_receipt(receipt: SkillReceipt, runtime_path: Path) -> str:
    lines = [
        "# Skill Execution Receipt",
        "",
        f"Created: {receipt.created_at}",
        f"Task ID: `{receipt.task_id}`",
        f"Window: `{receipt.window}`",
        f"Task type: `{receipt.task_type}`",
        f"Stage: `{receipt.stage}`",
        f"Skill: `{receipt.skill}`",
        f"Artifact: `{receipt.artifact or '-'}`",
        f"Status: `{receipt.status}`",
        f"Runtime receipt: `{rel(runtime_path)}`",
        "",
        "## Evidence",
        "",
        "| Path | Exists | SHA-256 |",
        "|---|---:|---|",
    ]
    if receipt.evidence:
        for item in receipt.evidence:
            lines.append(f"| `{item.path}` | {str(item.exists).lower()} | `{item.sha256 or '-'}` |")
    else:
        lines.append("| - | false | `-` |")
    lines.extend(
        [
            "",
            "## Command",
            "",
            receipt.command or "-",
            "",
            "## Notes",
            "",
            receipt.notes or "-",
            "",
            "## Boundary",
            "",
            "This receipt proves that a required skill left auditable evidence. It does not prove that the evidence is academically sufficient unless the referenced gate report says so.",
            "",
        ]
    )
    return "\n".join(lines)


def load_receipts() -> list[tuple[Path, SkillReceipt]]:
    receipts: list[tuple[Path, SkillReceipt]] = []
    if not RUNTIME_DIR.exists():
        return receipts
    for path in sorted(RUNTIME_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            data["evidence"] = [EvidenceRecord(**item) for item in data.get("evidence", [])]
            receipts.append((path, SkillReceipt(**data)))
        except Exception:
            continue
    return receipts


def receipt_matches(receipt: SkillReceipt, task_id: str, skill: str, artifact: str | None, stage: str | None) -> bool:
    if receipt.task_id != task_id:
        return False
    if receipt.skill != skill:
        return False
    if stage and receipt.stage != stage:
        return False
    if artifact:
        artifact_rel = rel(resolve(artifact))
        if receipt.artifact and receipt.artifact != artifact_rel:
            return False
    return True


def verify_receipt(path: Path, receipt: SkillReceipt) -> list[str]:
    issues: list[str] = []
    if receipt.status not in PASSING_STATUSES:
        issues.append(f"{receipt.skill}: status is {receipt.status}")
    if not receipt.evidence:
        issues.append(f"{receipt.skill}: no evidence files recorded")
    for item in receipt.evidence:
        evidence_path = resolve(item.path)
        if not evidence_path.exists():
            issues.append(f"{receipt.skill}: missing evidence {item.path}")
            continue
        if item.sha256 and evidence_path.is_file():
            current = sha256(evidence_path)
            if current != item.sha256:
                issues.append(f"{receipt.skill}: evidence hash changed for {item.path}")
    if not path.exists():
        issues.append(f"{receipt.skill}: receipt file disappeared")
    return issues


def render_check_report(task_id: str, required_items: list[str], rows: list[tuple[str, str, str]]) -> str:
    status = "PASS" if all(row[1] == "PASS" for row in rows) else "BLOCK"
    lines = [
        "# Skill Receipt Check",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"Task ID: `{task_id}`",
        f"Status: `{status}`",
        "",
        "## Required Skills",
        "",
    ]
    lines.extend(f"- `{item}`" for item in required_items)
    lines.extend(["", "## Results", "", "| Required receipt | Status | Evidence |", "|---|---|---|"])
    for skill, row_status, evidence in rows:
        safe_evidence = evidence.replace("|", "\\|").replace("\n", "<br>")
        lines.append(f"| `{skill}` | {row_status} | {safe_evidence or '-'} |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This check verifies execution evidence for required skills. It blocks missing, stale, or non-passing receipts, but it does not replace the underlying academic gate reports.",
            "",
        ]
    )
    return "\n".join(lines)


def create(args: argparse.Namespace) -> int:
    evidence = [evidence_record(item) for item in (args.evidence or [])]
    missing = [item.path for item in evidence if not item.exists]
    if missing and not args.allow_missing_evidence:
        for item in missing:
            print(f"Missing evidence: {item}")
        return 1
    if not evidence and not args.allow_no_evidence:
        print("At least one --evidence file is required unless --allow-no-evidence is set.")
        return 1

    artifact = rel(resolve(args.artifact)) if args.artifact else ""
    window = infer_window(args.window, args.task_type, args.stage, args.task_id)
    receipt = SkillReceipt(
        version=1,
        created_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        task_id=args.task_id,
        window=window,
        task_type=args.task_type or "",
        stage=args.stage,
        skill=args.skill,
        artifact=artifact,
        status=args.status,
        evidence=evidence,
        command=args.command or "",
        notes=args.notes or "",
    )

    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    HUMAN_DIR.mkdir(parents=True, exist_ok=True)
    runtime_path = receipt_runtime_path(receipt)
    runtime_path.write_text(json.dumps(asdict(receipt), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    human_path = receipt_human_path(receipt)
    human_path.write_text(render_receipt(receipt, runtime_path), encoding="utf-8")
    append_event(
        receipt,
        "skill_receipt_created",
        "completed" if receipt.status in PASSING_STATUSES else "failed",
        f"Skill execution receipt wrote {rel(runtime_path)} and {rel(human_path)}.",
        "low" if receipt.status in PASSING_STATUSES else "medium",
    )
    print(f"Runtime receipt: {runtime_path}")
    print(f"Human receipt: {human_path}")
    print(f"Status: {receipt.status}")
    return 0 if receipt.status in PASSING_STATUSES else 1


def check(args: argparse.Namespace) -> int:
    required_items: list[tuple[str, str | None, str]] = []
    for skill in args.required_skill or []:
        required_items.append((skill, args.stage, skill if not args.stage else f"{skill}@{args.stage}"))
    for item in args.required_receipt or []:
        if "@" in item:
            skill, stage = item.split("@", 1)
        elif ":" in item:
            skill, stage = item.split(":", 1)
        else:
            skill, stage = item, None
        required_items.append((skill, stage or args.stage, item))
    receipts = load_receipts()
    rows: list[tuple[str, str, str]] = []
    for skill, stage, label in required_items:
        matching = [
            (path, receipt)
            for path, receipt in receipts
            if receipt_matches(receipt, args.task_id, skill, args.artifact, stage)
        ]
        if not matching:
            rows.append((label, "BLOCK", "No matching skill execution receipt found."))
            continue
        # Use the newest matching receipt.
        path, receipt = matching[-1]
        issues = verify_receipt(path, receipt)
        if issues:
            rows.append((label, "BLOCK", "\n".join(issues)))
        else:
            evidence = f"Receipt: `{rel(path)}`"
            if receipt.evidence:
                evidence += "\n" + "\n".join(f"- `{item.path}`" for item in receipt.evidence)
            rows.append((label, "PASS", evidence))

    CHECK_DIR.mkdir(parents=True, exist_ok=True)
    out = CHECK_DIR / f"Skill_Receipt_Check_{slugify(args.task_id)}_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.md"
    out.write_text(render_check_report(args.task_id, [item[2] for item in required_items], rows), encoding="utf-8")
    print(f"Report: {out}")
    for skill, status, evidence in rows:
        print(f"{skill}: {status} ({evidence.splitlines()[0] if evidence else '-'})")
    return 0 if all(row[1] == "PASS" for row in rows) else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Create or verify skill execution receipts.")
    sub = parser.add_subparsers(dest="command", required=True)

    create_p = sub.add_parser("create", help="Create a receipt for a completed skill gate.")
    create_p.add_argument("--task-id", required=True)
    create_p.add_argument("--skill", required=True)
    create_p.add_argument("--stage", default="unspecified")
    create_p.add_argument("--artifact", default="")
    create_p.add_argument("--status", choices=["PASS", "WARN", "BLOCK", "NA"], default="PASS")
    create_p.add_argument("--evidence", action="append")
    create_p.add_argument("--command", default="")
    create_p.add_argument("--notes", default="")
    create_p.add_argument("--window", choices=["Production", "Maintenance"], default=None)
    create_p.add_argument("--task-type", default="")
    create_p.add_argument("--allow-missing-evidence", action="store_true")
    create_p.add_argument("--allow-no-evidence", action="store_true")
    create_p.set_defaults(func=create)

    check_p = sub.add_parser("check", help="Check required skill receipts for a task.")
    check_p.add_argument("--task-id", required=True)
    check_p.add_argument("--required-skill", action="append")
    check_p.add_argument("--required-receipt", action="append", help="Required receipt as skill@stage or skill:stage.")
    check_p.add_argument("--artifact")
    check_p.add_argument("--stage")
    check_p.set_defaults(func=check)

    args = parser.parse_args()
    if args.command == "check" and not args.required_skill and not args.required_receipt:
        parser.error("check requires at least one --required-skill or --required-receipt")
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
