# Real Project Operating Guide

This guide explains how to turn the starter kit into a working research-project agent. It is written for dissertations, theses, manuscripts, reports, grants, and evidence-synthesis projects.

## Core Decision

Do not start by asking the agent to write a chapter.

Start by building the project operating layer:

1. project brief;
2. source register;
3. source-readiness matrix;
4. compliance or requirements tracker;
5. writing-quality and integrity gates;
6. delivery pipeline.

The system works best when the agent knows what evidence exists, what is still uncertain, and which claims are not ready to write.

## Step 1: Create The Project Brief

Use:

- `RESEARCH_PROJECT_BRIEF_TEMPLATE.md`
- `PROJECT_TYPE_PROFILES.md`
- `.agents/skills/research-project-adapter/`

Fill only source-confirmed facts. Mark everything else `TO CONFIRM`.

Minimum fields:

- project title or working title;
- project type;
- audience or assessment context;
- research question or practical problem;
- method or expected evidence type;
- formal requirements;
- known sources;
- private-data boundary.

## Step 2: Build The Source Register

Use:

- `knowledge-base/SOURCE_REGISTER.md`
- `knowledge-base/SOURCE_READINESS_MATRIX.md`
- `knowledge-base/sources/`

Each source should have a status:

- `METADATA ONLY`
- `TARGETED REVIEWED`
- `PARTLY REVIEWED`
- `CITATION READY`
- `NOT SUITABLE`

Do not treat a DOI, abstract, AI summary, search result, Zotero item, or retrieval hit as claim support. Claim support requires source-section review.

## Step 3: Set Up The Knowledge Base

Use:

- `knowledge-base/self-growing/raw-inbox/`
- `knowledge-base/self-growing/growth-queue.md`
- `knowledge-base/self-growing/compiled-wiki/`
- `docs/OBSIDIAN_SETUP.md`

Rule:

```text
Open knowledge-base/ as your Obsidian vault. Do not open the repository root.
```

Keep system files out of the Obsidian graph. The knowledge base is for research knowledge, not runtime receipts, scripts, tests, or public release files.

## Step 4: Use The Writing Pipeline

For formal prose, use this order:

1. source-first check;
2. Material Passport;
3. academic-integrity preflight;
4. cognitive protocol;
5. academic self-review loop;
6. authorial voice integrity check;
7. project style pass;
8. document-quality gate;
9. formal delivery guard if delivering Word/PDF/stakeholder-facing output.

This order matters. Style polishing should not happen before evidence, claim boundaries, and integrity risks are checked.

## Step 5: Use Authorial Voice Safely

Use:

- `.agents/skills/authorial-voice-integrity/`
- `research-wiki/AI_WRITING_AUTHORIAL_VOICE_POLICY.md`
- `scripts/authorial_voice_scan.py`

Allowed:

- remove generic AI-style phrasing;
- improve mini-claims and paragraph logic;
- improve academic or professional register;
- preserve source boundaries and uncertainty.

Not allowed:

- promise lower AI detector scores;
- optimise for detector evasion;
- hide AI-use disclosure;
- invent disclosure rules;
- polish unsupported claims until they sound safer than they are.

## Step 6: Prepare Formal Delivery

Use:

- `scripts/material_passport.py`
- `scripts/pre_delivery_lock.py`
- `scripts/formal_delivery_guard.py`
- `research-wiki/DOCUMENT_PIPELINE.md`

Formal delivery should have:

- a source map;
- a Material Passport;
- integrity-preflight evidence;
- citation or source-readiness status where needed;
- document-quality review;
- a pre-delivery lock;
- a final guard result.

If a guard blocks the artifact, it is not ready unless the user explicitly records a risk override. An override is not a quality pass.

## Step 7: Add External Review Only After Local Gates

Use:

- `docs/EXTERNAL_REVIEW_OPTIONS.md`
- `scripts/build_external_review_bundle.py`
- `scripts/claude_independent_review.py` when Claude Code is available

External review is advisory. It does not replace source reading, citation support, ethics/compliance review, or delivery guards.

## Practical First Week Setup

Day 1:

- fill the project brief;
- add known formal requirements;
- create the first source register rows.

Day 2:

- create 5-10 source notes;
- mark each source readiness status;
- add `TO CONFIRM` questions.

Day 3:

- create the argument or problem map;
- run a cognitive protocol for the first formal section.

Day 4:

- draft one short section;
- run self-review, authorial voice scan, and style pass.

Day 5:

- produce a small delivery checkpoint;
- run the formal guard only if the artifact is intended for a real reader.

## What Good Operation Looks Like

The agent should be able to answer:

- What is the project trying to do?
- Which sources are ready to cite?
- Which claims are still unsupported?
- Which requirements are official, inferred, or unconfirmed?
- What is the next writing task?
- Which gate blocks delivery?
- What changed in the latest draft and why?

If the agent cannot answer these questions from local files, the project memory is not ready for serious formal writing.
