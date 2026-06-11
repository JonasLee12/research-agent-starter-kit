<!-- Customise this file with your own project details -->

# Project Agent Preferences

Date: `TO CONFIRM`

Use this file to tell the agent how to behave in this research project. Keep private facts as placeholders until they are source-confirmed.

## Project Identity

- Project title: `PROJECT_TITLE`
- Project type/profile: `TO CONFIRM`
- Researcher / owner name: `TO CONFIRM`
- Email: `TO CONFIRM`
- Organisation / institution / lab / client: `TO CONFIRM`
- Programme / team / journal / funder / department: `TO CONFIRM`
- Supervisor / PI / manager / collaborator / client contact: `TO CONFIRM`
- Requirement source: `TO CONFIRM`

## Source-First Rule

Before drafting or revising formal documents, extract known factual fields from source files first.

Do not invent:

- names;
- emails;
- supervisor, PI, manager, collaborator, reviewer, funder, or client details;
- dates or deadlines;
- module, journal, funder, client, institutional, ethics, or legal requirements;
- marking criteria;
- word counts;
- participant facts;
- datasets or results;
- citations;
- page numbers;
- findings.

If a field is missing, write `TO CONFIRM`.

## Word Document Deliverables

Use Word `.docx` by default for:

- proposal drafts;
- manuscript drafts;
- report drafts;
- grant or bid drafts;
- ethics, IRB, or compliance form drafts and revisions;
- participant information sheets;
- consent forms;
- recruitment emails prepared as appendices;
- supervisor/PI/client/reviewer-facing summaries;
- chapter or section drafts;
- formal review reports.

Use Markdown for:

- project memory;
- skills;
- source maps;
- checklists;
- audit logs;
- lightweight planning notes.

## Project Delivery Review Rule

Default quality target for formal research outputs: `TO CONFIRM`.

Before delivering a formal, supervisor/PI/client/reviewer-facing, or submission-facing document the agent must:

1. check `quality-gates/PROJECT_DELIVERY_REVIEW_GATE.md`;
2. check local requirement sources, such as rubric, journal author guidelines, funder rules, client brief, protocol, or format requirements;
3. use `university-guidance/RUBRIC_EVIDENCE_GATE.md` and `university-guidance/DISTINCTION_DELIVERY_REVIEW_GATE.md` only for assessed academic work where they are relevant;
4. inspect the actual document source or rendered output;
5. list pre-revision findings;
6. revise feasible weaknesses;
7. give a post-revision readiness statement;
8. state unresolved `TO CONFIRM` items.

This is an indicative readiness review, not an official mark, journal decision, funding decision, approval, or legal judgement.

## Language Output Style

Default response structure:

1. conclusion or recommended action first;
2. two to four key reasons;
3. only necessary explanation;
4. `TO CONFIRM` for unresolved choices;
5. direct statement of file paths and changes when documents are edited.

Avoid generic filler, inflated claims, and unsupported certainty.

## Academic Writing Style

Use the relevant academic style for the project. For UK postgraduate work, prefer:

- British English spelling;
- cautious claims;
- clear signposting;
- source-grounded argument;
- concise prose;
- no fake citations;
- no invented page numbers.

## Cognitive Framework Rule

For major proposal, manuscript, report, grant, methodology, literature review, rationale, discussion, recommendation, or stakeholder-facing writing, the agent must create a cognitive protocol before drafting.

Minimum protocol:

- section type;
- main claim;
- gap/problem type;
- evidence base;
- warrant;
- boundary;
- rhetorical plan;
- risks and `TO CONFIRM` items.

Use `.agents/skills/cognitive-frameworks/SKILL.md` and `scripts/cognitive_protocol_check.py` when available.

## Stage Continuity And Token-Aware Recall Rule

For long-running projects, a later-stage task must not ignore earlier source-of-record decisions.

Use `research-wiki/STAGE_GRAPH.md` and `research-wiki/STAGE_CONTINUITY_PROTOCOL.md` when a task both:

1. changes, designs, restates, translates, formalises, or produces a high-risk deliverable; and
2. has upstream dependencies in the Stage Graph or references prior decisions, accepted outputs, source maps, or checkpoints.

Use `scripts/stage_recall_policy.py --task "<TASK>"` or the runtime `recall_decision` to choose the minimum recall scope:

- Tier 0: no project recall;
- Tier 1: anchor scan;
- Tier 2: pointer lookup;
- Tier 3: targeted Stage Continuity Capsule;
- Tier 4: full upstream audit or pause.

This saves tokens; it does not weaken source-first, compliance, citation, privacy, document-quality, or delivery gates.

If the user asks to skip an upstream check, first surface the omitted dependency. Proceed only if the user explicitly accepts the override risk, and record that risk rather than calling the gate a pass.

For non-obvious route decisions, create a Deep Reasoning Pass before drafting. It is a concise decision record, not a replacement for cognitive frameworks or self-review.

## Bounded Task Routing Rule

Do not treat every methodology, literature, proposal-background, or source task as formal writing.

Use light receipt sets for:

- source planning;
- reading priority sorting;
- literature/source lookup;
- citation-key, reference-format, typo, or punctuation edits.

Escalate to the full formal-writing chain only when the task asks for formal prose, paragraph/section/chapter drafting, Word/DOCX delivery, stakeholder/reviewer/client/submission-facing output, or protected source-of-record edits.

Bounded work must still preserve evidence boundaries: metadata-only sources stay metadata-only, source-readiness is not upgraded without source-section review, and protected registers are not edited without a separately routed task.

## Academic Self-Review Rule

For formal academic or professional prose, the agent must run `academic-self-review-loop` before style polishing and document-quality gates.

The loop must include:

1. first-pass review using `research-wiki/WRITING_QUALITY_RUBRIC.md`;
2. top two or three concrete weaknesses;
3. revision that improves argument quality, not only wording;
4. fresh second-pass judgement;
5. remaining source or evidence risks.

Claude Code, another model, or a human reviewer may provide optional independent review. Their feedback does not replace local self-review and must not be treated as evidence.

When Claude Code is available, use `scripts/claude_independent_review.py` for reviewable, non-sensitive artifacts. The wrapper provides a privacy gate, timeout handling, and an advisory-review boundary. It must not be used for raw participant data, private records, credentials, or restricted materials unless the user explicitly accepts the risk.

## Academic Integrity Preflight Rule

Before substantive formal drafting and again before final delivery, use `.agents/skills/academic-integrity-preflight/SKILL.md` and `scripts/academic_integrity_preflight.py` when available.

This check looks for concrete risks:

- prompt residue;
- unresolved placeholders;
- fake or unverified references;
- unsupported major claims;
- unresolved compliance or requirement claims;
- AI-use disclosure statements without source evidence.

It is not an AI detector and must not be used to promise detection outcomes.

## Authorial Voice And AI-Writing Integrity Rule

Requests such as "make this less AI-like", "humanise this", "lower AI rate", "de-AI", AIGC, AI detector, or AI-use disclosure changes must be routed to `.agents/skills/authorial-voice-integrity/SKILL.md`.

Allowed work:

- remove prompt residue and chatbot framing;
- replace generic phrasing with project-specific reasoning;
- improve mini-claims, warrants, transitions, and evidence boundaries;
- strengthen the user's or project's authorial judgement.

Not allowed:

- promise detector scores;
- bypass or game AI detection;
- add random stylistic noise;
- hide, weaken, or invent AI-use disclosure;
- make unsupported claims sound more confident.

Use `scripts/authorial_voice_scan.py` when available. It is not an AI detector.

## Three-Stage Document Pipeline Rule

For important Word, PDF, or stakeholder-facing outputs, use `research-wiki/DOCUMENT_PIPELINE.md`.

Required checkpoints:

- `*_THINKING_CHECKPOINT.md`: source map, cognitive protocol, argument logic;
- `*_WRITING_CHECKPOINT.md`: self-review loop, revision actions, writing-quality review;
- `*_DELIVERY_CHECKPOINT.md`: delivery gates, requirement/compliance checks, structural parity, layout self-review, render status.

If no formal document is generated, mark delivery checkpoint as not applicable.

For generated `.docx` files, preserve visible structure. A Word output should not silently flatten Markdown tables into pipe-delimited paragraphs, remove tables that existed in a previous accepted version, or weaken heading hierarchy. Use `scripts/markdown_docx_structure_check.py` and `scripts/docx_layout_review_check.py` directly or through `scripts/formal_delivery_guard.py`; record any deliberate layout change as an explicit risk/decision rather than a quality pass.

## Two-Track Research Output

For major thinking or planning tasks, produce two styles when useful:

- Thinking Pack: fuller reasoning, route comparison, decision points.
- Decision Brief: conclusion-first summary for supervisor, PI, client, reviewer, or quick review.

For small tasks, use the Decision Brief style in chat.

## Formatting Rule

Follow this order:

1. project-specific official guidance or client/journal/funder brief;
2. supervisor, PI, module leader, editor, funder, or client clarification;
3. institution, organisation, lab, or publisher guidance;
4. generic disciplinary formatting guidance only as fallback.

Mark unresolved conflicts as `TO CONFIRM`.

## Repository Sharing Rule

Before pushing or sharing:

- run `scripts/privacy_check.sh`;
- review `PRIVACY_CHECKLIST.md`;
- complete `PUBLIC_RELEASE_AUDIT.md` before public release;
- keep the repository private unless every privacy and academic-integrity check has passed.

## Runtime And Connector Rule

For substantial tasks, use deterministic runtime preflight when local tools are available:

```bash
python3 scripts/agent_runtime.py "<TASK>" --window Production --write --strict
```

or:

```bash
python3 scripts/agent_runtime.py "<TASK>" --window Maintenance --write --strict
```

Academic database searches must use metadata boundaries:

- public APIs can return metadata;
- subscription databases require lawful credentials;
- metadata is not evidence until source sections are reviewed.

Citation-heavy drafts need two checks when possible:

- citation/reference consistency;
- claim-support audit queue.

Do not describe a cited claim as verified until the relevant source section has been checked.

## Self-Growing Knowledge Base Rule

Use `knowledge-base/self-growing/` as the controlled intake and synthesis layer for project knowledge.

Default flow:

1. place untriaged material in `raw-inbox/` only after privacy review;
2. add a row to `growth-queue.md`;
3. assign evidence status and canonical destination;
4. compile only source-linked, non-sensitive synthesis into `compiled-wiki/`;
5. run `python3 scripts/kb_health_check.py --write` for local health checks.

Retrieval tools may help find files:

- `scripts/build_agent_index.py`;
- `scripts/local_retrieval_search.py`;
- `scripts/build_vector_index.py`;
- `scripts/vector_retrieval_smoke_test.py`.

Retrieval output is not evidence. Formal writing still needs source-readiness and claim-support review.

## Superpowers / Brainstorming / Tool-Skill Integration

Date: 2026-05-25

Decision:

- This template includes project-safe adapters for Superpowers-style workflows, Brainstorming, skill creation governance, Playwright browser automation, and MarkItDown-style file conversion.
- Do not install the full external Superpowers package by default.
- Do not install MarkItDown by default.
- Do not copy global `skill-creator` or global `playwright` into project skills; use project wrappers so the system can route to them without creating stale duplicates.

Included project skills:

- `using-superpowers`: use when the user asks for Superpowers-style workflow discipline or external process-skill adaptation.
- `brainstorming`: use before unclear, high-impact research route, methodology, concept-card, supervisor-question, or system-design decisions.
- `project-skill-creator-governance`: use before creating, copying, adapting, or updating project skills; pair with global `skill-creator`.
- `playwright-dissertation-browser`: use before controlled browser automation; pair with global `playwright`.
- `markitdown`: use before file-to-Markdown conversion for source review, Obsidian notes, knowledge-base ingestion, or RAG preparation.
- `research-project-adapter`: use when adapting the starter kit to a non-dissertation project profile.
- `research-neural-network-figure`: use only for actual neural-network or AI model architecture figures.
- `research-nature-figure`: use as an optional quality layer for high-impact research figures, after source/data/privacy checks.
- `research-nature-writing`: use as an optional article-style prose layer after source-first, cognitive planning, citation/readiness, and self-review gates.

Tool boundary:

- Global `skill-creator` may be available through Codex system skills.
- Global `playwright` may be available through the user skill surface.
- MarkItDown may not be installed. Check availability before use and ask before installing it.

Routing boundary:

- `agent-orchestration` remains the primary router.
- Superpowers-style rules must not override source-first, rubric evidence, document-quality, privacy, or window-separation rules.
- Brainstorming should be used when the decision is genuinely unclear; it should not slow down simple direct tasks.
- Browser automation must stay read-only for LMS/private sites unless the user explicitly confirms an action.
- File conversion must not move participant data, private LMS material, or identifiable records into public/shareable layers.
- `research-*` skills must remain optional quality layers and must not override project-specific requirements, source evidence, privacy gates, or compliance checks.

## Weekly Literature Gap-Watch Automation

Use `docs/WEEKLY_LITERATURE_GAP_WATCH_AUTOMATION.md` when setting up or reviewing recurring literature-monitoring tasks.

Default rule:

- candidate discovery only;
- top 5-8 candidates;
- public metadata remains `METADATA ONLY`;
- no automatic write to source registers, source-readiness matrices, source notes, Obsidian, Zotero, or formal research text;
- methodology track is off unless a concrete methodology-writing or methodology-gap task is active;
- Stage C shifts from broad discovery to source-readiness upgrade when formal drafting begins.
