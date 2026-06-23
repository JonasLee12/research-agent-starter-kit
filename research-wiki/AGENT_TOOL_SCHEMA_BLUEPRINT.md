# Agent Tool Schema Blueprint

Purpose: keep local workflow tools explicit and testable.

## Schema Folder

Schemas live in:

- `research-wiki/tool-schemas/`

Validate with:

```bash
python3 scripts/validate_agent_schemas.py
```

## Current Schemas

- `agent_runtime_enforcement.schema.json`
- `borrowed_pattern_boundary_lint.schema.json`
- `subscription_database_connector.schema.json`
- `citation_claim_support_audit.schema.json`
- `claim_ledger_lite_check.schema.json`
- `codex_sqlite_log_guard.schema.json`
- `session_log_integrity_check.schema.json`
- `visible_output_qa_check.schema.json`

## Rule

Do not claim a workflow is enforced unless it has a local script, schema, report output, and verification step.
