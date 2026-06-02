# Skill Dependency Graph

Purpose: show the default order for high-risk research writing workflows.

## Formal Research Writing Order

```text
agent-orchestration
  -> research-project-adapter, if project type is unclear
  -> dissertation-source-first-gate
  -> material-passport (short scope for formal draft movement)
  -> cognitive-frameworks
  -> dissertation-argument-spine / dissertation-research-review, as needed
  -> academic-integrity-preflight
  -> academic-self-review-loop
  -> uk-academic-writing-style
  -> style-memory-and-revision-gate
  -> dissertation-document-quality-gate
  -> material-passport (full scope when reviewer/stakeholder/submission-facing)
  -> pre-delivery lock
  -> formal-delivery-guard
  -> project delivery / render / receipt gates
```

## Stage Mapping

| Stage | Main Skills | Checkpoint |
|---|---|---|
| Thinking | `agent-orchestration`, `dissertation-source-first-gate`, `material-passport`, `cognitive-frameworks`, argument/research review skills | `*_THINKING_CHECKPOINT.md` |
| Writing | `academic-integrity-preflight`, `academic-self-review-loop`, `uk-academic-writing-style`, `style-memory-and-revision-gate`, `dissertation-document-quality-gate` | `*_WRITING_CHECKPOINT.md` |
| Delivery | full `material-passport`, project delivery gate, pre-delivery lock, formal delivery guard, citation checks, document-quality, render check, receipt validation | `*_DELIVERY_CHECKPOINT.md` |

## Knowledge-Base Operations Order

```text
agent-orchestration
  -> dissertation-knowledge-ops / teaching-knowledge-base-plan
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
