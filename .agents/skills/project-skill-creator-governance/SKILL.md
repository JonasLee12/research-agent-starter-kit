---
name: project-skill-creator-governance
description: Use before creating, copying, adapting, or updating project skills so new skills stay concise, non-overlapping, source-grounded, and compatible with the research agent rule stack; use with the system skill-creator when authoring SKILL.md files.
---

# Project Skill Creator Governance

Use this skill before creating or updating any project-level skill in `.agents/skills/`.

## Purpose

Make sure new skills improve the research-agent system instead of adding duplicated, stale, or unsafe instructions.

This project can use the global `skill-creator` skill for SKILL.md authoring. This governance skill adds dissertation-specific rules.

## Required Checks

Before adding or editing a skill:

1. Identify the user problem the skill solves.
2. Check whether an existing project skill already covers it.
3. Decide whether to:
   - create a new skill;
   - update an existing skill;
   - add a wrapper around a global skill;
   - leave it as a preference/rule instead of a skill.
4. Keep `SKILL.md` concise.
5. Do not include extra README, changelog, or install guide files inside the skill folder.
6. Add safety gates if the skill can affect formal documents, institution requirements, participant data, GitHub sharing, browser automation, or external tools.
7. Update `AGENTS.md`, `PROJECT_AGENT_PREFERENCES.md`, and `research-wiki/TASK_STATE.md` when the new skill changes routing.

## When To Use Global `skill-creator`

Use the global `skill-creator` when:

- writing a new `SKILL.md`;
- revising a skill's frontmatter;
- designing concise trigger descriptions;
- deciding whether references/scripts/assets are needed.

Do not copy the global `skill-creator` into this project unless the user explicitly asks for a frozen local copy.

## Skill Acceptance Checklist

```text
Skill check:
- Unique purpose:
- Trigger clear:
- Existing overlap checked:
- Safety boundary present:
- Source-first needed:
- Document-quality needed:
- External tool/install boundary:
- AGENTS.md updated:
- TASK_STATE.md updated:
```

