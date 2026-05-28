# Skill Dependency Graph

Purpose: show the default order for high-risk research writing workflows.

## Formal Research Writing Order

```text
agent-orchestration
  -> research-project-adapter, if project type is unclear
  -> dissertation-source-first-gate
  -> cognitive-frameworks
  -> dissertation-argument-spine / dissertation-research-review, as needed
  -> academic-self-review-loop
  -> uk-academic-writing-style
  -> style-memory-and-revision-gate
  -> dissertation-document-quality-gate
  -> project delivery / render / receipt gates
```

## Stage Mapping

| Stage | Main Skills | Checkpoint |
|---|---|---|
| Thinking | `agent-orchestration`, `dissertation-source-first-gate`, `cognitive-frameworks`, argument/research review skills | `*_THINKING_CHECKPOINT.md` |
| Writing | `academic-self-review-loop`, `uk-academic-writing-style`, `style-memory-and-revision-gate`, `dissertation-document-quality-gate` | `*_WRITING_CHECKPOINT.md` |
| Delivery | project delivery gate, citation checks, document-quality, render check, receipt validation | `*_DELIVERY_CHECKPOINT.md` |

## Boundary

This graph is a workflow guide, not a hosted runtime. Use `scripts/agent_runtime.py` for deterministic preflight when local tools are available.
