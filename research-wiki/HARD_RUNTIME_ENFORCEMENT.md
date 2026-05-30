# Hard Runtime Enforcement

Last updated: 2026-05-25

## Decision

The project now has a local deterministic runtime guard:

- `scripts/agent_runtime.py`

This is the hardest enforceable layer available inside the current Codex workspace without building a separate hosted agent platform.

## What It Enforces

For a task description and window role, it deterministically checks:

- task type;
- mode;
- required skills;
- required gates;
- required source files;
- wrong-window warnings;
- missing-file blocks.

It writes:

- JSON route receipt;
- Markdown preflight receipt;
- structured session-log events (`session_start`, `gate_completed`, `session_end`).

Receipts are stored under:

- `research-wiki/runtime-receipts/`

## How To Use

Before substantial Production or Maintenance work, run:

```bash
python3 scripts/agent_runtime.py "<TASK>" --window Production --write --strict
```

or:

```bash
python3 scripts/agent_runtime.py "<TASK>" --window Maintenance --write --strict
```

If the script returns `BLOCKED`, the task should not proceed until the missing required file or gate problem is fixed.

## Current Boundary

This creates a hard local preflight. It does not turn Codex chat itself into an unavoidable runtime.

The rule is:

- substantial tasks must have a runtime receipt;
- missing runtime receipt is a Maintenance audit bug;
- the script can block tasks when required files are missing;
- it cannot stop a user or model from ignoring the script outside this project workflow.

## Status

Current public-template status:

- Use `scripts/agent_runtime.py` before substantial Production or Maintenance work.
- Runtime receipts should be regenerated for each important task.
- Formal writing routes should include `cognitive-frameworks`, `academic-integrity-preflight`, `academic-self-review-loop`, and staged checkpoint gates.
- Knowledge-base routes should include self-growing KB privacy/source boundaries and the KB health-check gate.
- Historical receipts are examples only and should not be treated as proof that a later task was checked.
