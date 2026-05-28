# Adapting The Starter Kit To Other Research Projects

This repository can support many research themes. It is not limited to dissertations or education research.

## Recommended Adaptation Sequence

1. Read `PROJECT_TYPE_PROFILES.md`.
2. Copy `RESEARCH_PROJECT_BRIEF_TEMPLATE.md` to `RESEARCH_PROJECT_BRIEF.md`.
3. Choose one primary project profile.
4. Fill only confirmed project facts.
5. Decide which optional topic skills are relevant.
6. Run:

```bash
python3 scripts/agent_runtime.py "adapt this starter kit to my project" --window Maintenance --write --strict
```

7. Run:

```bash
./scripts/privacy_check.sh
```

## What To Keep For Most Projects

- `agent-orchestration`
- `research-project-adapter`
- `dissertation-source-first-gate`
- `dissertation-research-search-protocol`
- `dissertation-learning-loop`
- `dissertation-literature-review`
- `cognitive-frameworks`
- `academic-self-review-loop`
- `dissertation-citation-audit`
- `dissertation-document-quality-gate`
- `context-continuity`
- `style-memory-and-revision-gate`
- `dissertation-agent-self-debug`
- `dissertation-agent-architecture-audit`
- `dissertation-knowledge-ops`

These skills still have `dissertation-*` names for compatibility, but most of them are general research-project workflows.

## What To Treat As Optional

Use these only when the topic needs them:

- `active-learning-design-support`
- `ai-agent-design-spec`
- `codesign-output-synthesis`
- `prototype-evaluation-audit`
- `teacher-adoption-modeling`
- `teaching-knowledge-base-plan`
- `viva-prep`

## What To Replace Or Edit

Edit topic-specific wording in:

- `RESEARCH_PROJECT_BRIEF.md`
- `PROJECT_AGENT_PREFERENCES.md`
- `.agents/skills/uk-academic-writing-style/SKILL.md`
- `.agents/skills/dissertation-document-quality-gate/SKILL.md`
- `.agents/skills/dissertation-argument-spine/references/`
- `university-guidance/`

Replace dissertation requirements with journal, funder, client, lab, institutional, disciplinary, or project-specific requirements where relevant.

## Default Generic Files

Use these files before creating project-specific copies:

- `RESEARCH_PROJECT_BRIEF_TEMPLATE.md`
- `PROJECT_TYPE_PROFILES.md`
- `compliance/PROJECT_COMPLIANCE_TRACKER.md`
- `quality-gates/PROJECT_DELIVERY_REVIEW_GATE.md`
- `research-wiki/WRITING_QUALITY_RUBRIC.md`
- `research-wiki/DOCUMENT_PIPELINE.md`

## Naming Advice

For a public or shared version, use generic names:

- `research-agent-starter-kit`
- `my-research-agent`
- `project-research-copilot`
- `lab-research-agent-template`

Avoid names that expose:

- a real institution;
- a live project title;
- a participant group;
- a supervisor, client, or funder;
- a local machine path.

## Evidence Rule

The system can help find and organise sources, but source metadata is not evidence. A source becomes usable for claims only after the relevant sections have been reviewed and recorded in `knowledge-base/SOURCE_READINESS_MATRIX.md`.

## Writing Quality Rule

For formal project writing, keep the writing-quality layer even if you remove topic-specific skills:

1. `cognitive-frameworks` helps the agent define the claim, gap/problem type, warrant, and boundary.
2. `academic-self-review-loop` forces a draft-review-revise-review cycle.
3. `WRITING_QUALITY_RUBRIC.md` checks paragraph logic and argument progression.
4. `DOCUMENT_PIPELINE.md` splits important output into thinking, writing, and delivery checkpoints.
