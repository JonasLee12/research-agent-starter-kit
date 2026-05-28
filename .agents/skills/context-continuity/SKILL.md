---
name: context-continuity
description: Maintain compact-ready checkpoints, task state summaries, source maps, and handoff notes during long dissertation work so future turns preserve decisions, files changed, open questions, and evidence boundaries.
---

# Context Continuity

Use this skill for long, multi-step, or easily interrupted dissertation tasks, especially when work may span many turns, involve multiple files, or risk losing source-grounded decisions.

## Purpose

Keep the project recoverable after context compaction or interruption.

This skill also carries the adapted ECC context-budget, save-session, and strategic-compact ideas for this dissertation project: preserve only the decisions, evidence boundaries, changed files, and next actions that future work needs.

## Workflow

1. At the start of a long task, identify:
   - goal
   - source files
   - output files
   - confirmed facts
   - `TO CONFIRM` fields
2. During the task, update a compact checkpoint when major decisions or files change.
3. Before final response, summarize:
   - what was done
   - what files changed
   - what evidence was used
   - what remains unresolved
   - what should happen next

## Context Budget Rule

Use compact notes instead of copying long content.

Keep:

- decisions
- source paths and URLs
- created/updated file paths
- confirmed facts
- `TO CONFIRM` items
- evidence boundaries
- next action

Avoid storing:

- long copied passages
- raw participant data
- repeated reasoning already captured in a document
- obsolete options that no longer affect the next decision

## Strategic Checkpoint Triggers

Update `research-wiki/TASK_STATE.md` when:

- a new Word or proposal-facing document is created
- ethics, LMS, or supervisor requirements are captured
- a new source cluster or contextual source is added
- a project rule or skill changes
- a decision affects methodology, research questions, concept cards, data collection, or participant-facing materials
- a long task is likely to be resumed later

For substantial Production Window tasks, also update `research-wiki/PRODUCTION_RUN_REGISTER.md` with a run receipt. This lets the Maintenance Window compare the claimed skill routing, created files, gates performed, render artifacts, temporary files, and remaining risks.

Production run receipts must include:

- mode and selected skills
- reason for selected skills
- skills considered but skipped, if relevant
- subagent decision
- gates required and completed
- main outputs, helper scripts, render folders, and temporary files

## Checkpoint Template

Use this structure:

```text
## YYYY-MM-DD Short Task Name

Goal:
- ...

Files created:
- ...

Files updated:
- ...

Evidence used:
- ...

Confirmed:
- ...

Inference / boundary:
- ...

Open confirmations:
- ...

Next action:
- ...
```

For substantial Production tasks, also add a receipt to `research-wiki/PRODUCTION_RUN_REGISTER.md` using the current receipt fields. Do not rely on `TASK_STATE.md` alone for cross-window monitoring.

## Where To Write

Use:

- `research-wiki/TASK_STATE.md` for current task state
- `research-wiki/PRODUCTION_RUN_REGISTER.md` for Production Window run receipts and Maintenance audit status
- task-specific revision notes where relevant
- source maps beside formal document drafts

## Guardrails

- Do not store raw participant data in task state.
- Use source paths, not vague references.
- Mark assumptions and unresolved fields clearly.
- Keep checkpoints concise enough to survive compaction.
