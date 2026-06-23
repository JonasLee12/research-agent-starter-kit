# Task Cards: Choose Your Workflow

Use this page when you know what you want to do but do not know which research-agent workflow to ask for.

The pattern is adapted from product-style task centers: make the task visible, collect the right inputs up front, show the likely route, and record the output status. It is not an essay-writing marketplace. The cards below preserve the source-first, integrity, citation, privacy, and delivery boundaries of this starter kit.

## Do Not Use This Kit For

Do not adapt or create task cards for:

- ghostwriting a thesis, dissertation, paper, proposal, report, or assignment;
- plagiarism reduction, "降重", or hiding copied text;
- AI-detector evasion, "降AI", "humanise to bypass detection", detector-score optimisation, or authorship-verdict manipulation;
- fabricating citations, data, participants, supervisor feedback, institutional requirements, or source support;
- rewriting reviewer/supervisor comments into final author text without source checks, user judgement, and explicit authorship boundaries;
- paid reseller, credit-pool, payment, or proxy-user workflows in this noncommercial starter kit.

## Status Labels

Use these labels for task-state files, receipt indexes, or dashboard summaries:

| Status | Meaning |
|---|---|
| `submitted` | The task has a defined intake card but no work has started. |
| `running` | The agent is actively reading, checking, drafting, rendering, or validating. |
| `blocked` | Work cannot proceed without missing evidence, user confirmation, credentials, or a failed gate fix. |
| `needs_confirmation` | The agent can continue only after the user decides a boundary, source, output type, or override. |
| `completed` | The requested output and required checks were completed. |
| `failed` | The task attempted a tool/check/action and did not complete. |
| `cancelled` | The user or maintainer deliberately stopped the task. |

## Intake First

Before using any card, fill or copy [`templates/SOURCE_FIRST_INTAKE_CARD.md`](../templates/SOURCE_FIRST_INTAKE_CARD.md). Unknown facts should stay `TO CONFIRM`; do not ask the agent to fill them from memory.

Minimum intake:

- task goal;
- target artifact;
- allowed source corpus;
- evidence/citation boundary;
- output surface;
- privacy/compliance constraints;
- expected route: bounded, standard, or full;
- status label.

## Route Levels

| Route | Use When | Do Not Use For |
|---|---|---|
| `bounded` | Source lookup, source-section verification, source planning, citation-key repair, reference-format repair, typo repair, or other no-substantive-change tasks. | Formal prose, Word/PDF delivery, stakeholder-facing output, protected source-of-record edits, citation-readiness upgrades, or method/design changes. |
| `standard` | Source-register updates, visible-surface checks, maintenance, public sync, dashboard/status updates, and structured knowledge-base work. | Ghostwriting, plagiarism reduction, detector evasion, fake source support, or source-readiness upgrades without reviewed evidence. |
| `full` | Formal prose, Word/PDF delivery, stakeholder-facing or submission-facing output, protected source-of-record edits, method/design/ethics changes, or high-risk stage continuity work. | Anything that asks the agent to bypass source checks, write unsupported final author text, hide AI use, fabricate evidence, or turn intake into citation proof. |

## Cards

### 1. Project Setup / Profile Card

Use when: adapting the starter kit to a thesis, article, report, grant, review, or other research project.

Required inputs:

- project type;
- confirmed title or working topic;
- source folders already available;
- private folders that must not be published;
- output types expected.

Likely route: `standard`

Use:

- `PROJECT_TYPE_PROFILES.md`
- `RESEARCH_PROJECT_BRIEF_TEMPLATE.md`
- `templates/AGENTS.example.md`

Output:

- adapted `AGENTS.md`;
- project brief with `TO CONFIRM` fields preserved;
- first validation run.

### 2. Literature Search / Source Discovery Card

Use when: finding candidate sources or planning search terms.

Required inputs:

- research question or topic;
- databases or web sources allowed;
- date/language limits;
- inclusion/exclusion criteria;
- where candidate notes should be stored.

Likely route: `bounded`

Required boundary:

- Search results are `METADATA ONLY` until source sections are reviewed.

Output:

- search log;
- candidate list;
- next-reading priority;
- no citation-readiness upgrade unless source sections are reviewed.

### 3. Source-Section Verification Card

Use when: checking whether a source supports a specific claim or section.

Required inputs:

- source path or citation;
- claim or section to verify;
- exact pages/sections if known;
- current source-readiness status;
- allowed output location.

Likely route: `bounded`

Output:

- support status: direct support, partial support, background only, metadata only, insufficient evidence;
- cannot-prove boundary;
- wording allowed only if source support is confirmed.

### 4. Source Register / Readiness Update Card

Use when: updating a source register, readiness matrix, or bibliography tracker.

Required inputs:

- source note path;
- evidence reviewed;
- metadata fields;
- requested status change;
- reason for change.

Likely route: `standard`

Required boundary:

- Metadata, abstract, a saved PDF, or a search result does not make a source citation-ready.

Output:

- updated source register/readiness matrix;
- status evidence path;
- residual risk or `TO CONFIRM`.

### 5. Formal Draft Planning Card

Use when: preparing a formal section, report, proposal, methodology, literature review, or stakeholder-facing draft.

Required inputs:

- target section/artifact;
- allowed source corpus;
- claim-support policy;
- audience;
- output format;
- upstream decisions that must be inherited.

Likely route: `full`

Required gates:

- source-first;
- Material Passport;
- cognitive protocol;
- integrity preflight;
- Stage Continuity when triggered.

Output:

- section plan, source map, and drafting boundary;
- no final prose unless the required evidence is available.

### 6. Formal Draft Review / Revision Card

Use when: reviewing or revising existing formal prose.

Required inputs:

- draft path;
- review purpose;
- allowed change scope;
- citation/claim-support status;
- whether this is supervisor-facing, stakeholder-facing, or submission-facing.

Likely route: `full`

Required gates:

- source-first if claims change;
- academic integrity;
- self-review loop;
- authorial voice and style fingerprint checks;
- document-quality gate.

Output:

- revision queue;
- revised draft only if source and authorship boundaries are clear;
- residual risks.

### 7. Method / Instrument / Design Continuity Card

Use when: changing or producing method plans, research questions, interview guides, concept cards, analysis plans, or design decisions.

Required inputs:

- target artifact;
- upstream source-of-record files;
- decisions that must not change silently;
- ethics/compliance constraints;
- open confirmations.

Likely route: `full`

Required gates:

- Token-Aware Recall;
- Stage Continuity Capsule;
- source-first;
- responsible/ethics checks when participant-facing or fieldwork-facing.

Output:

- continuity capsule;
- design decision summary;
- next action or user confirmation request.

### 8. Word / DOCX Delivery Card

Use when: generating, revising, or delivering a Word/PDF output.

Required inputs:

- source Markdown/doc;
- target `.docx` or `.pdf`;
- previous accepted baseline if one exists;
- output audience;
- required style/template constraints.

Likely route: `full`

Required gates:

- pre-delivery lock;
- formal delivery guard;
- Markdown-DOCX structure check;
- DOCX layout review;
- Visible Output QA.

Output:

- deliverable artifact;
- delivery checkpoint;
- visible-output verdict;
- override record if any risk is accepted.

### 9. Visible Surface / Public Release Card

Use when: checking a rendered README, GitHub release, public page, figure, Obsidian view, or browser surface.

Required inputs:

- visible URL or artifact path;
- communication job;
- baseline if available;
- privacy boundary.

Likely route: `standard`

Required gates:

- Visible Output QA;
- release-surface verification for GitHub/public releases;
- privacy check before public sharing.

Output:

- source-layer status;
- rendered/visible status;
- remaining `TO VERIFY` items.

### 10. Agent Maintenance / Runtime Guard Card

Use when: checking agent failures, runaway logs, stale receipts, routing drift, automation problems, or dirty working trees.

Required inputs:

- symptom;
- affected files/tools;
- whether write actions are allowed;
- backup/rollback boundary.

Likely route: `standard`

Required gates:

- runtime/session-log integrity checks where relevant;
- Codex SQLite log guard for `logs_*.sqlite` growth;
- privacy check before public sync;
- explicit Git staging by file path, never `git add -A`.

Output:

- diagnosis;
- applied fix or audited risk;
- validation result;
- clean or classified Git status.

## Plain-Language Prompt

```text
Use the Task Cards workflow. First choose the smallest suitable card, then ask only for missing intake fields. Do not draft formal prose until source-first and integrity boundaries are clear.
```
