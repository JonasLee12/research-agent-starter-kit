#!/usr/bin/env python3
"""Validate lightweight JSON schema files for agent workflow contracts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "research-wiki" / "tool-schemas"
REQUIRED_TOP_KEYS = {"name", "version", "inputs_required", "outputs_expected", "preconditions", "quality_gate"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate local agent workflow schema files.")
    parser.add_argument("--schema-dir", default=str(SCHEMA_DIR))
    args = parser.parse_args()
    schema_dir = Path(args.schema_dir)
    if not schema_dir.is_absolute():
        schema_dir = ROOT / schema_dir
    failures = []
    count = 0
    for path in sorted(schema_dir.glob("*.json")):
        count += 1
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"{path}: invalid JSON: {exc}")
            continue
        missing = REQUIRED_TOP_KEYS - set(data)
        if missing:
            failures.append(f"{path}: missing keys {', '.join(sorted(missing))}")
    print(f"Schemas checked: {count}")
    if failures:
        print("Failures:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("All schemas passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
