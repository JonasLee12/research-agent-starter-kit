# Skill Execution Receipt Protocol

Purpose: make required skill execution auditable. A selected skill should leave concrete evidence, not only a chat statement that it was used.

## Problem Addressed

Research agents can load or mention a skill without actually applying it. This protocol separates:

- skill routing: the runtime selected a skill;
- skill execution: the skill produced an auditable artifact;
- academic sufficiency: the artifact's finding is strong enough for the research task.

Receipts prove execution evidence exists. They do not prove that the underlying evidence is academically sufficient.

## Receipt Command

Create a receipt after a required gate has produced evidence:

```bash
python3 scripts/skill_execution_receipt.py create \
  --task-id <task-id> \
  --skill <skill-name> \
  --stage <thinking|writing|delivery> \
  --artifact <target-artifact> \
  --status PASS \
  --evidence <gate-report.md> \
  --command "<command or workflow summary>"
```

Check required receipts:

```bash
python3 scripts/skill_execution_receipt.py check \
  --task-id <task-id> \
  --required-receipt dissertation-source-first-gate@thinking \
  --required-receipt cognitive-frameworks@thinking \
  --required-receipt academic-self-review-loop@writing
```

## Default Formal-Writing Receipts

For formal research output, use the task-specific receipt list from `scripts/agent_runtime.py`. A typical formal pipeline requires receipts for:

- `dissertation-source-first-gate@thinking`
- `material-passport@thinking`
- `academic-integrity-preflight@thinking`
- `cognitive-frameworks@thinking`
- `academic-self-review-loop@writing`
- `authorial-voice-integrity@writing`
- `style-fingerprint-gate@writing`
- `uk-academic-writing-style@writing`
- `style-memory-and-revision-gate@writing`
- `dissertation-document-quality-gate@writing`
- the formal delivery guard report itself should be produced at delivery stage after checking upstream receipts.

Not every task needs the full list. Literature discovery, simple file checks, or maintenance work should use a lighter task-specific list.

## Evidence Requirements

A useful receipt points to a real artifact such as:

- source-first note or source map;
- Material Passport report;
- cognitive protocol check report;
- self-review loop check report;
- style-fingerprint scan output;
- authorial voice scan output;
- citation claim-support queue;
- document-quality check report;
- pre-delivery lock or formal delivery guard report.

Do not create a PASS receipt with no evidence unless the gate is genuinely not applicable and the receipt status is `NA`.

## Delivery Guard Relationship

When `scripts/formal_delivery_guard.py` is run with `--require-skill-receipts`, it checks upstream required receipts for the task ID. Missing, stale, or non-passing receipts block delivery unless the user explicitly acknowledges an override. The guard's own report becomes delivery-stage evidence after it runs.

## Boundary

This protocol prevents false claims that a required skill ran. It does not make weak analysis strong, verify source support by itself, or replace human judgement.
