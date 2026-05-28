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

## Why The Separation Matters

Without window separation, maintenance concerns can contaminate formal writing context. The agent may spend attention on scripts, releases, or debugging instead of evidence, argument quality, and document delivery.

The dual-window model keeps:

- Production focused on research output;
- Maintenance focused on system reliability;
- shared memory explicit and auditable.
