# Public Release Audit

Status: `CLEARED FOR PUBLIC STARTER-KIT UPDATE`

Date: 2026-05-30

This file records the release checks completed before publishing the starter kit as an open-source repository.

## v1.6.0 Public Sync Audit - 2026-06-10

Scope: Stage Continuity and Token-Aware Recall improvements were generalised into the public starter kit.

Included public-safe changes:

- generic Stage Continuity protocol and Stage Graph template;
- deterministic recall-tier helper and Stage Continuity Capsule checker;
- runtime routing support for `recall_decision`;
- agent-orchestration and context-continuity skill guidance;
- README, changelog, system overview, dual-window guide, and evaluation registry updates;
- focused tests and behavioural evidence checks for high-risk stage work, user-skip instructions, layout-only repairs, and bookkeeping tasks.

Privacy and public-template boundary:

- no private research drafts, source notes, compliance files, human-subject records, local machine paths, adviser/reviewer materials, or institution-specific requirements were copied into this public update;
- Stage Graph rows are examples and templates, not project-specific source-of-record claims;
- Claude Code review was used as advisory feedback only and did not replace local privacy, validation, or release-surface checks.

Validation completed for this update:

- Python compile check for changed scripts;
- unit tests;
- skill evals;
- behavioural evidence checks;
- schema validation;
- privacy check;
- `git diff --check`.

## Public Identity

- Maintainer: `[YOUR_NAME]`
- Contact email: `your.email@university.ac.uk`
- Replace these placeholders before publishing under a real public identity.

## Completed Checks

- [x] Current working tree contains no known personal dissertation names.
- [x] Current working tree contains no local machine paths.
- [x] Current working tree contains no real institutional email addresses.
- [x] Current working tree contains no raw participant data.
- [x] Current working tree contains no real ethics forms.
- [x] Current working tree contains no assessed proposal or dissertation drafts.
- [x] Current working tree contains no copied restricted Canvas, LMS, or university rubric content.
- [x] Current working tree contains no committed credentials.
- [x] Runtime receipts and generated eval reports have been removed from the public tree.
- [x] Example templates exist for source notes, ethics tracking, and university guidance.
- [x] README, contributing guide, acknowledgements, requirements files, and MIT license are present.
- [x] v1.1.0 runtime-routing, Claude-review-wrapper, research-skill, and literature gap-watch documentation uses generic public-template language.
- [x] New `research-*` skills are generic optional layers and do not include private project facts.
- [x] Claude Code review is documented as advisory only, not as source evidence.
- [x] Weekly literature gap-watch automation is documented as candidate-only, not as automatic source ingestion.
- [x] v1.2.0 self-growing knowledge-base scaffold contains templates only, not private compiled project content.
- [x] Local retrieval/vector scripts are documented as candidate lookup tools, not evidence verification.
- [x] Academic-integrity preflight is documented as a concrete-risk checker, not an AI detector.

## Validation Commands

The final verification suite in `CODEX_GITHUB_RELEASE_TASK.md` was run successfully:

- privacy scan passed;
- required file checks passed;
- template file checks passed;
- documentation file checks passed;
- protected content directory checks passed;
- schema validation passed;
- skill evals passed.

## Git History Warning

Previous private-history commits contained personal release metadata and local workflow traces. The public release must therefore be published from a clean Git history, not by exposing the old commit graph.

Required release method:

1. create a clean repository copy;
2. remove `.git`;
3. initialise a fresh repository;
4. commit the cleaned public tree;
5. force-push the new `main` branch only after confirming the remote has no public consumers depending on old history.

## Remaining User Responsibility

Before making the repository public, confirm that:

- `[YOUR_NAME]` and `your.email@university.ac.uk` have been replaced or intentionally left as placeholders;
- the GitHub owner/repository name is acceptable for public visibility;
- any future project-specific files are kept private or anonymised.
