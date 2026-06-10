# Stage Continuity Protocol

Last updated: 2026-06-10

## Purpose

Use this protocol when a long-running research project moves from one stage to another. The goal is to stop an agent from producing a later-stage artifact as if earlier briefs, proposals, compliance decisions, method plans, or source-readiness decisions did not exist.

This protocol is part of `context-continuity`. It does not replace source-first checks, compliance or ethics checks, citation checks, cognitive planning, document-quality gates, or formal delivery guards.

## Trigger Predicate

The Stage Continuity Gate fires only when both A and B hold.

A. Deliverable class. The task changes, designs, restates, translates, formalises, or produces a high-risk deliverable class.

Canonical high-risk deliverable classes:

- `proposal-or-brief`
- `methodology-or-method-plan`
- `ethics-or-compliance-material`
- `interview-guide-or-fieldwork-instrument`
- `concept-card-or-scenario-stimulus`
- `research-question-to-method-mapping`
- `analysis-plan`
- `stakeholder-facing-decision-memo`
- `chapter-or-section-formal-draft`

Counter-example: fixing a typo, table border, file name, or citation format in an already scoped document does not trigger Stage Continuity unless the task also changes meaning, method, compliance status, or formal claims.

B. Upstream dependency exists. `research-wiki/STAGE_GRAPH.md` lists at least one upstream node for that deliverable class, or the task text references a prior decision, previous artifact, source-of-record file, source map, design lock, accepted output, or checkpoint.

Explicit non-triggers:

- citation-only edits;
- formatting or layout fixes;
- typo or punctuation repair;
- file moves;
- log, receipt, registry, or Git bookkeeping;
- reading or summarising a source without producing a design decision or formal claim.

## User Skip Instruction

A first user instruction such as "skip the upstream check" does not silently bypass known dependencies when A and B hold.

Required behaviour:

1. Surface the omitted dependency.
2. Ask whether the user accepts the unresolved risk.
3. If the user explicitly accepts, record an override risk in the relevant checkpoint or task state.
4. Do not call the gate a pass.

## Token-Aware Recall

Use `scripts/stage_recall_policy.py` or the runtime preflight `recall_decision` as a context-budget controller.

| Tier | Name | Trigger condition | Action |
|---:|---|---|---|
| 0 | `no_project_recall` | no project-memory signal | proceed without project recall |
| 1 | `anchor_scan` | source summary, light requirement mention, or low-risk reference | scan anchors only |
| 2 | `pointer_lookup` | formal output, source-status, layout/structure, or requirement pointer | check named pointers and relevant status files |
| 3 | `targeted_continuity_capsule` | high-risk deliverable or protected upstream source | write a Stage Continuity Capsule |
| 4 | `full_upstream_audit` | scoped supersession or request to replace/ignore protected prior sources | pause for branch decision or run a full upstream audit if explicitly requested |

Token-Aware Recall is not an authority layer. It cannot override Stage Continuity A+B, source-first, compliance, citation, document-quality, delivery, privacy, or project-specific requirement gates.

Recompute the tier when:

- a task moves from discussion to formal output;
- a layout task becomes content or structure revision;
- source reading becomes method, design, analysis-plan, or formal-claim production;
- the target file changes;
- delivery begins.

## Stage Continuity Capsule

Use a compact capsule for routine continuation. Use a fuller capsule for route changes, methods, instruments, formal prose, or stakeholder-facing decisions.

```text
Stage Continuity Capsule:
- Current task/stage:
- Trigger:
- Stage graph nodes used:
- Source-of-record files checked:
- Inherited decisions:
- Later files that may supersede earlier ones:
- Supersession needs confirmation:
- Open confirmations / hard stops:
- What may change:
- What must not change without confirmation:
- Next action boundary:
```

Rules:

- Name concrete file paths, not only labels such as "proposal" or "method notes".
- Cite a stage graph node or source path for inherited decisions.
- For high-risk deliverables, `What must not change without confirmation` must be non-empty.
- Run `scripts/stage_continuity_capsule_check.py <checkpoint.md> --deliverable-class <class>` when local tools are available.

## Deep Reasoning Pass

Use this before a non-obvious route decision, especially when there is a trade-off, irreversible commitment, or deviation from a previous direction.

This is a concise auditable decision summary. It sits before cognitive frameworks and self-review. It does not replace them.

```text
Deep Reasoning Pass:
- Decision under consideration:
- Chosen direction and concrete trade-off accepted:
- Rejected alternative, only if one was genuinely considered:
- What would change the decision:
```

Rules:

- Name the trade-off accepted, not only the benefit gained.
- Do not invent a weak alternative just to fill the template.
- Do not expose private chain-of-thought.
- If evidence is weak, lower the claim or mark `TO CONFIRM`.

## Failure Handling

- Missing source-of-record: pause and locate or confirm before drafting.
- Conflicting inherited decisions: surface the conflict; do not silently choose.
- Unclear supersession: mark `needs confirmation`; do not declare older sources irrelevant.
- Compliance or ethics uncertainty: use the project compliance tracker before writing as if approval exists.
- Citation or source-readiness uncertainty: use source-readiness files; do not upgrade metadata-only material to claim support.
- Formal delivery guard cannot compensate for a missing Stage Continuity Gate.
