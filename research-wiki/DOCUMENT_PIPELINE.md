# Document Pipeline

Purpose: reduce missed checks and context overload when creating formal research documents.

Use this pipeline for proposals, manuscripts, reports, grants, protocols, thesis/dissertation sections, reviewer/supervisor/PI/client-facing drafts, and important Word outputs.

## Core Decision

Replace one long delivery checklist with three staged checkpoints:

1. thinking checkpoint;
2. writing checkpoint;
3. delivery checkpoint.

Each stage should load only the files and skills needed for that stage. The next stage reads the checkpoint from the previous stage.

## Stage 1: Thinking Checkpoint

Output pattern:

```text
<OUTPUT_NAME>_THINKING_CHECKPOINT.md
```

Use:

- `agent-orchestration`
- `research-project-adapter` when profile is unclear
- `dissertation-source-first-gate`
- `material-passport` with `--scope short` when the artifact will move into formal drafting
- `academic-integrity-preflight` before substantive drafting when the artifact will make formal claims
- `cognitive-frameworks`
- `dissertation-argument-spine` or equivalent argument logic
- requirement/compliance source checks when relevant

Record:

```text
Thinking checkpoint:
- Project profile:
- Task mode:
- Source map:
- Material Passport:
- Academic-integrity preflight:
- Confirmed facts:
- TO CONFIRM:
- Section type:
- Main claim:
- Gap/problem type:
- Evidence base:
- Warrant:
- Boundary:
- Rhetorical plan:
- Risks:
- Next writing move:
```

Do not generate final Word output in this stage.

## Stage 2: Writing Checkpoint

Output pattern:

```text
<OUTPUT_NAME>_WRITING_CHECKPOINT.md
```

Use:

- current artifact or draft;
- thinking checkpoint;
- current Material Passport, updating it if source, compliance, citation, or `TO CONFIRM` status changed;
- `academic-integrity-preflight` again if the draft, claims, references, disclosure wording, or compliance status changed;
- `academic-self-review-loop`;
- `research-wiki/WRITING_QUALITY_RUBRIC.md`;
- `authorial-voice-integrity` and `scripts/authorial_voice_scan.py` when prose risks generic AI-style phrasing, detector framing, disclosure hiding, or inflated style;
- `uk-academic-writing-style` when academic/professional prose quality matters;
- `style-memory-and-revision-gate`;
- `dissertation-document-quality-gate` at draft level.

Record:

```text
Writing checkpoint:
- Draft source:
- Self-review pass 1 findings:
- Revision actions:
- Revised text or revision summary:
- Academic-integrity preflight status:
- Self-review pass 2 judgement:
- Writing-quality criteria improved:
- Authorial voice scan:
- Remaining weaknesses:
- Source/citation risks:
- Ready for delivery stage: yes / no / yes with TO CONFIRM
```

The revision should improve argument quality, not only wording.

## Stage 3: Delivery Checkpoint

Output pattern:

```text
<OUTPUT_NAME>_DELIVERY_CHECKPOINT.md
```

Use only when a formal, shareable, stakeholder-facing, or Word/PDF document is being delivered.

Use:

- thinking checkpoint;
- writing checkpoint;
- `material-passport` with `--scope full` for reviewer-facing, stakeholder-facing, client-facing, or submission-facing output;
- `quality-gates/PROJECT_DELIVERY_REVIEW_GATE.md`;
- relevant official requirement source or compliance tracker;
- citation/style checks when relevant;
- final `academic-integrity-preflight` when delivering formal prose;
- pre-delivery lock with `scripts/pre_delivery_lock.py`;
- final guard with `scripts/formal_delivery_guard.py`;
- Word/PDF/render checks when relevant.

Record:

```text
Delivery checkpoint:
- Delivery artifact:
- Full Material Passport:
- Requirement/compliance gate:
- Source-first gate:
- Citation or claim-support gate:
- Academic-integrity preflight:
- Project delivery review:
- Pre-delivery lock:
- Formal delivery guard:
- Document-quality gate:
- Render/layout check:
- Final status:
- Remaining TO CONFIRM:
```

If no formal document is generated, write:

```text
Delivery checkpoint: not applicable because no Word/PDF/stakeholder-facing artifact was produced.
```

## Rules

- Do not overwrite the original file unless the user explicitly asks.
- If a document is not source-ready, label it as a working draft.
- If citations are metadata-only, do not present them as claim support.
- If a requirement source is missing, mark it `TO CONFIRM`.
- If the output is for public sharing, run the privacy check first.
- Checkpoints are evidence of workflow discipline; they do not guarantee grade, publication, funding, approval, or client acceptance.
- A `HOLD` Material Passport or `BLOCK` formal delivery guard means the artifact should remain a draft unless the user explicitly records an override.
