# Skill Development Guide

Skills live in `.agents/skills/<skill-name>/SKILL.md`.

Use this guide when adding or changing a skill.

## SKILL.md Structure

Each skill should include:

1. YAML frontmatter:

```yaml
---
name: skill-name
description: Use when...
---
```

2. Trigger conditions:

- when the skill should activate;
- when it should not activate;
- what user request patterns suggest this skill.

3. Workflow:

- ordered steps;
- required files or source checks;
- expected output shape.

4. Boundaries:

- what the skill does not do;
- what must be confirmed by the user;
- privacy, source, citation, or compliance limits.

## Register Eval Cases

Add at least two rows to `research-wiki/SKILL_EVAL_REGISTRY.md`:

- a positive case that should route to the skill;
- a negative or boundary case that should not over-trigger.

Then run:

```bash
python scripts/run_skill_evals.py
```

## Check Skill Conflicts

Before adding a new skill, read:

- `AGENTS.md`
- `PROJECT_AGENT_PREFERENCES.md`
- `research-wiki/SKILL_DEPENDENCY_GRAPH.md`
- nearby existing skills in `.agents/skills/`

Do not create a new skill if an existing skill can be extended cleanly.

## Priority Order

When rules conflict, use this order:

1. privacy and sensitive data protection;
2. source-first factual verification;
3. official requirement or rubric evidence;
4. high-band or delivery-readiness gates when relevant;
5. document-quality and formatting gates;
6. citation consistency and claim-support review;
7. cognitive planning and argument quality;
8. style and voice;
9. optional tools and convenience workflows.

## Local Test Checklist

After adding or editing a skill:

```bash
python scripts/run_skill_evals.py
python scripts/validate_agent_schemas.py
./scripts/privacy_check.sh
```

If the skill changes formal writing, also check:

- `research-wiki/DOCUMENT_PIPELINE.md`
- `research-wiki/WRITING_QUALITY_RUBRIC.md`
- `research-wiki/PRODUCTION_RECEIPT_VALIDATION.md`

## Common Mistakes

- duplicating an existing skill;
- adding broad advice without trigger rules;
- omitting privacy or source boundaries;
- adding examples with real project data;
- treating tool output as evidence without source review;
- changing routing without updating eval cases.
