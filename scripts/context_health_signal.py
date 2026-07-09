#!/usr/bin/env python3
"""Record lightweight context-health signals for long-running agent sessions.

This script records observable session-health signals. It cannot see the full
model context window unless the host tool exposes it, so token counts,
compression events, and model labels are often manual or environment-derived.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "research-wiki" / "CONTEXT_HEALTH_SIGNAL_LOG.jsonl"
RUNTIME_DIR = ROOT / "research-wiki" / "runtime-receipts"


def rel(path: Path | None) -> str | None:
    if path is None:
        return None
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def model_label() -> tuple[str, str]:
    for key in ("CODEX_MODEL", "OPENAI_MODEL", "MODEL", "GPT_MODEL"):
        value = os.environ.get(key)
        if value:
            return value, f"env:{key}"
    return "unknown", "not_exposed_to_runtime"


def token_scale(total: int | None) -> str:
    if total is None:
        return "unknown"
    if total < 20_000:
        return "low"
    if total < 80_000:
        return "medium"
    return "high"


def latest_runtime_receipt() -> Path | None:
    receipts = sorted(RUNTIME_DIR.glob("runtime_preflight_*.json"), key=lambda path: path.stat().st_mtime)
    return receipts[-1] if receipts else None


def find_runtime_receipt(run_id: str) -> Path | None:
    for path in sorted(RUNTIME_DIR.glob("runtime_preflight_*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if data.get("run_id") == run_id:
            return path
    return None


def load_runtime(path: Path | None) -> tuple[dict, Path | None]:
    if path is None:
        return {}, None
    return json.loads(path.read_text(encoding="utf-8")), path


def append_entry(entry: dict) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def command_record(args: argparse.Namespace) -> int:
    runtime_path = Path(args.runtime_receipt) if args.runtime_receipt else None
    if args.latest_runtime:
        runtime_path = latest_runtime_receipt()
    if runtime_path is None and args.run_id:
        runtime_path = find_runtime_receipt(args.run_id)
    runtime, runtime_path = load_runtime(runtime_path)

    model, model_source = model_label()
    if args.model:
        model, model_source = args.model, "manual"

    approx_total = args.approx_total_tokens
    if approx_total is None and args.approx_input_tokens is not None:
        approx_total = args.approx_input_tokens + (args.approx_output_tokens or 0)

    recall = runtime.get("recall_decision") or {}
    required_files = runtime.get("required_files") or []
    entry = {
        "schema": "context_health_signal.v1",
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "source": "manual",
        "run_id": args.run_id or runtime.get("run_id") or "unknown",
        "window": args.window or runtime.get("window") or "unknown",
        "task": args.task or runtime.get("task") or "",
        "mode": args.route or runtime.get("mode") or "unknown",
        "task_types": runtime.get("task_types") or [],
        "model": model,
        "model_source": model_source,
        "turn_count": args.turn_count,
        "turn_count_source": "manual" if args.turn_count is not None else "unknown",
        "context_compressed": args.context_compressed,
        "context_compressed_source": "manual",
        "approx_input_tokens": args.approx_input_tokens,
        "approx_output_tokens": args.approx_output_tokens,
        "approx_total_tokens": approx_total,
        "token_scale": token_scale(approx_total),
        "symptom": args.symptom,
        "severity": args.severity,
        "recall_tier": recall.get("tier"),
        "recall_tier_name": recall.get("tier_name"),
        "required_file_count": len(required_files),
        "skills_count": len(runtime.get("skills") or []),
        "gates_count": len(runtime.get("gates") or []),
        "receipt_requirement_count": len(runtime.get("receipt_requirements") or []),
        "runtime_receipt_json": rel(runtime_path),
    }
    append_entry(entry)
    print(f"Recorded context health signal: {rel(LOG)}")
    return 0


def command_summary(args: argparse.Namespace) -> int:
    if not LOG.exists():
        print("No context health signal log found.")
        return 0
    entries: list[dict] = []
    for line in LOG.read_text(encoding="utf-8").splitlines():
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    recent = entries[-args.limit :]
    print(f"Signals: {len(entries)} total; showing {len(recent)} latest")
    for entry in recent:
        print(
            "\t".join(
                [
                    entry.get("timestamp", ""),
                    entry.get("window", ""),
                    str(entry.get("run_id", "")),
                    str(entry.get("mode", "")),
                    str(entry.get("context_compressed", "")),
                    str(entry.get("token_scale", "")),
                    str(entry.get("severity", "")),
                    str(entry.get("symptom", ""))[:120],
                ]
            )
        )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Record or summarize agent context-health signals.")
    sub = parser.add_subparsers(dest="command", required=True)

    record = sub.add_parser("record", help="Append one context-health signal.")
    record.add_argument("--run-id")
    record.add_argument("--window", choices=["Production", "Maintenance"])
    record.add_argument("--task")
    record.add_argument("--route", help="Observed route or mode if no runtime receipt is available.")
    record.add_argument("--runtime-receipt")
    record.add_argument("--latest-runtime", action="store_true")
    record.add_argument("--model")
    record.add_argument("--turn-count", type=int)
    record.add_argument("--approx-input-tokens", type=int)
    record.add_argument("--approx-output-tokens", type=int)
    record.add_argument("--approx-total-tokens", type=int)
    record.add_argument("--context-compressed", choices=["yes", "no", "unknown"], default="unknown")
    record.add_argument("--symptom", required=True)
    record.add_argument("--severity", choices=["info", "watch", "degraded", "blocked"], default="watch")
    record.set_defaults(func=command_record)

    summary = sub.add_parser("summary", help="Show recent signals.")
    summary.add_argument("--limit", type=int, default=20)
    summary.set_defaults(func=command_summary)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
