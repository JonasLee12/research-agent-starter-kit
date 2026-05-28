# Rubric Evidence Gate

Last updated: 2026-05-24

Purpose: prevent the agent from answering marking criteria, grade-band, distinction, deadline, LMS, word-count, or submission-rule questions from memory.

## Trigger

Use this gate before answering or drafting anything about:

- distinction or high-distinction targets;
- grade bands;
- marking criteria;
- rubric requirements;
- LMS requirements;
- module deadlines;
- word counts;
- proposal or dissertation submission rules;
- AI declaration or referencing requirements.

## Evidence Boundary

Local rubric or module summaries are useful planning notes, but they are not always the full official wording.

Before giving a substantive answer, identify the evidence level:

- `OFFICIAL ORIGINAL TEXT`
- `LOCAL SUMMARY`
- `INFERENCE FROM LOCAL SUMMARY`
- `EVIDENCE INSUFFICIENT`

If only a local summary exists, do not claim exact official wording for any numeric grade band. Ask for an official export, screenshot, handbook, LMS page, or supervisor/module confirmation when needed.

## Minimum Source Set

For rubric or grade-band questions, check:

- `university-guidance/RUBRIC_EVIDENCE_GATE.md`
- `university-guidance/RUBRIC_OR_MARKING_CRITERIA_TEMPLATE.md` or the project-specific rubric file
- `university-guidance/MODULE_REQUIREMENTS_TEMPLATE.md` or the project-specific module-requirements file
- `university-guidance/FORMAT_REQUIREMENTS_TEMPLATE.md` or the project-specific format file
- `research-wiki/TASK_STATE.md`

For citation-heavy or proposal-design work, also check:

- `knowledge-base/SOURCE_READINESS_MATRIX.md`
- relevant proposal/chapter source maps
- relevant document-quality or Distinction review notes

## Required Response Behaviour

Before giving advice, the agent must state:

```text
Evidence status:
- Files checked:
- Evidence level:
- What cannot be claimed:
```

## Failure Labels

Maintenance should flag these as bugs:

- `rubric source-first bug`: marking or grade-band advice was given without checking source files.
- `rubric evidence overclaim`: a local summary was treated as full official wording.
- `rubric citation gap`: rubric-based advice was given without naming source files.
