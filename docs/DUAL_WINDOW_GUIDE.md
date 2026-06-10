# Dual Window Guide

Use two working windows when the project becomes complex:

- **Production Window**: creates research outputs.
- **Maintenance Window**: maintains the agent system.

The two windows do not share chat history. They share state through local files.

## Production Window

Use the Production Window for:

- proposal, thesis, dissertation, manuscript, report, or grant writing;
- literature review and methodology drafting;
- ethics, compliance, or participant-facing drafts;
- source synthesis and citation-heavy work;
- supervisor, reviewer, client, or stakeholder-facing outputs.

Production work should update:

- `research-wiki/TASK_STATE.md`
- `research-wiki/PRODUCTION_RUN_REGISTER.md`
- source registers or output files when relevant

Before formal writing, the Production Window should use source-first, cognitive planning, self-review, style, citation, and document-quality gates.

For later-stage outputs that depend on earlier project decisions, the Production Window should also use Stage Continuity:

- compute or consume the runtime `recall_decision`;
- read `research-wiki/STAGE_GRAPH.md` when Stage Continuity A+B is triggered;
- write a short Stage Continuity Capsule before drafting or revising the artifact;
- recompute recall when the task changes from discussion to formal output, from layout to content, or from reading to design/method/analysis work;
- before delivery, check that the final artifact still matches the inherited upstream decisions.

This is meant to stop a new window from treating a long project as if it started in the current chat. It is not a full-history reread by default; `scripts/stage_recall_policy.py` chooses the smallest useful recall tier.

## Maintenance Window

Use the Maintenance Window for:

- skill edits and workflow changes;
- bug fixing and false-run checks;
- GitHub release preparation;
- privacy and public-release audits;
- validation script maintenance;
- knowledge-base structure changes;
- automation and connector audits.

Maintenance work should protect the system and avoid formal research drafting unless the user explicitly asks.

## Shared State

The windows share state through files, not chat memory:

- `AGENTS.md`
- `PROJECT_AGENT_PREFERENCES.md`
- `research-wiki/TASK_STATE.md`
- `research-wiki/PRODUCTION_RUN_REGISTER.md`
- `research-wiki/WINDOW_WORKFLOW_PROMPTS.md`
- source registers and project notes

If one window changes workflow rules, it should update `TASK_STATE.md` so the other window can refresh context.

If one window creates or changes a stage-level decision, it should also update the Stage Graph or a related continuity capsule so later work can inherit that decision without rereading the whole project.

## Startup Prompt Pattern

At the start of a new window, ask the agent to read:

```text
AGENTS.md
PROJECT_AGENT_PREFERENCES.md
research-wiki/TASK_STATE.md
research-wiki/WINDOW_WORKFLOW_PROMPTS.md
.agents/skills/
```

Then ask it to report:

1. current project phase;
2. active tasks;
3. open confirmations;
4. which skills and gates apply to the requested task.
5. whether the task triggers Stage Continuity and which recall tier applies.

## Why The Separation Matters

Without window separation, maintenance concerns can contaminate formal writing context. The agent may spend attention on scripts, releases, or debugging instead of evidence, argument quality, and document delivery.

The dual-window model keeps:

- Production focused on research output;
- Maintenance focused on system reliability;
- shared memory explicit and auditable.
