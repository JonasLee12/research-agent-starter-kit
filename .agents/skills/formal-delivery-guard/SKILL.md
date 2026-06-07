---
name: formal-delivery-guard
description: Use before presenting a formal Word, PDF, reviewer-facing, stakeholder-facing, or submission-facing research artifact as usable; checks pre-delivery lock evidence and final integrity/citation risks, with an explicit override path for acknowledged risk.
---

# Formal Delivery Guard

Use this skill at the final delivery stage for formal research outputs.

## Purpose

Prevent a formal artifact from being handed over as ready when required gates were skipped, unresolved placeholders remain, or citation/support checks still need attention.

## Activate For

- Word or PDF outputs intended for a user, reviewer, supervisor/PI, client, funder, journal, committee, or submission portal
- formal proposal, manuscript, report, thesis/dissertation section, grant, protocol, or compliance-facing document
- any artifact whose delivery checkpoint says `ready for delivery`

## Required Sequence

1. Complete the thinking and writing checkpoints in `research-wiki/DOCUMENT_PIPELINE.md`.
2. Run `material-passport` with `--scope full` when the artifact is reviewer-facing, stakeholder-facing, or submission-facing.
3. Run final `academic-integrity-preflight` on the Markdown/text source when available.
4. Create a pre-delivery lock:

```bash
python3 scripts/pre_delivery_lock.py create --target <artifact> \
  --runtime-receipt <path> \
  --material-passport <path> \
  --source-map <path> \
  --integrity-preflight <path> \
  --quality-gate <path> \
  --require-material-passport \
  --require-integrity-preflight
```

5. Run the final guard:

```bash
python3 scripts/formal_delivery_guard.py --artifact <artifact> --source <markdown-source> \
  --require-material-passport \
  --require-integrity-preflight \
  --require-style-fingerprint \
  --require-skill-receipts \
  --task-id <task-id>
```

Add `--require-citation`, `--require-compliance`, or `--fail-on-claim-attention` when the output needs those checks.

Use `--required-receipt <skill@stage>` to provide a custom task-specific receipt list. Without custom receipt flags, the guard checks the default upstream formal-writing receipts.

## Override Rule

If the guard blocks delivery and the user explicitly accepts the risk, use:

```bash
python3 scripts/formal_delivery_guard.py --artifact <artifact> --source <markdown-source> \
  --acknowledge-override \
  --override-reason "User accepts unresolved risk because ..."
```

An override creates an audit record. It does not convert unresolved evidence into verified evidence and must not be described as a quality pass.

## Failure Behaviour

- `PASS`: required lock and final checks are present.
- `WARN`: non-blocking issue remains visible.
- `BLOCK`: required lock/evidence is missing, integrity preflight fails, style-fingerprint scan fails, required skill receipts are missing/stale/non-passing, or citation claim-support attention is configured as blocking.
- `OVERRIDE_ACKNOWLEDGED`: blocked checks exist, but the user explicitly recorded a delivery-risk exception.

## Boundaries

- This guard does not guarantee marks, acceptance, funding, publication, or official approval.
- It does not prove that source sections support claims.
- It cannot stop manual bypass outside the agent workflow.
- Do not use override flags unless the user explicitly accepts the unresolved risk.
- Pre-delivery lock JSON files in `.agent-runtime/pre-delivery-locks/` may store local absolute paths so stale evidence can be checked. That directory is ignored by Git and should not be shared publicly.
