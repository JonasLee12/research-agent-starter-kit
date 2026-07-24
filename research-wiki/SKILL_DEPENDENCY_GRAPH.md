# Skill Dependency Graph

Purpose: show the default order for high-risk research writing workflows.

## Formal Research Writing Order

```text
agent-orchestration
  -> research-project-adapter, if project type is unclear
  -> dissertation-source-first-gate
  -> material-passport (short scope for formal draft movement)
  -> academic-integrity-preflight
  -> cognitive-frameworks
  -> dissertation-argument-spine / dissertation-research-review, as needed
  -> academic-self-review-loop
  -> authorial-voice-integrity / authorial voice scan, for formal Document Pipeline outputs or explicit language-risk requests
  -> style-fingerprint-gate
  -> uk-academic-writing-style
  -> style-memory-and-revision-gate
  -> dissertation-document-quality-gate
  -> skill execution receipts for required upstream gates
  -> material-passport (full scope when reviewer/stakeholder/submission-facing)
  -> pre-delivery lock
  -> formal-delivery-guard
  -> project delivery / render / receipt gates
```

## Stage Mapping

| Stage | Main Skills | Checkpoint |
|---|---|---|
| Thinking | `agent-orchestration`, `dissertation-source-first-gate`, `material-passport`, `academic-integrity-preflight`, `cognitive-frameworks`, argument/research review skills | `*_THINKING_CHECKPOINT.md` |
| Writing | final integrity check if needed, `academic-self-review-loop`, `authorial-voice-integrity`, `style-fingerprint-gate`, `uk-academic-writing-style`, `style-memory-and-revision-gate`, `dissertation-document-quality-gate` | `*_WRITING_CHECKPOINT.md` |
| Delivery | upstream skill receipts, full `material-passport`, project delivery gate, pre-delivery lock, formal delivery guard, citation checks, document-quality, render check, receipt validation | `*_DELIVERY_CHECKPOINT.md` |

## Knowledge-Base Operations Order

```text
agent-orchestration
  -> dissertation-knowledge-ops
  -> source and privacy boundary check
  -> raw-inbox intake
  -> growth-queue triage
  -> compiled-wiki synthesis linked to source-of-record files
  -> kb_health_check
  -> local retrieval index or optional vector index
```

Retrieval skills and scripts must stay downstream of source/privacy boundaries. They find candidate files; they do not prove claims.

## Boundary

This graph is a workflow guide, not a hosted runtime. Use `scripts/agent_runtime.py` for deterministic preflight when local tools are available.

Archived skills under `.agents/archived-skills/` are preserved examples outside the active discovery root, not active routing nodes. Restore an archived topic pack into `.agents/skills/` only after a concrete project phase needs it and Maintenance records why the added active context is justified.
