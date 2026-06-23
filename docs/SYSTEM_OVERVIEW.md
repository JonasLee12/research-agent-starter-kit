# Research Agent Starter Kit System Overview

Date: 2026-06-02

Status: depersonalised public-template explanation

## 1. Core Idea

This starter kit turns a coding agent into a structured research-project assistant. It gives the agent local rules, skills, source checks, document gates, knowledge-base habits, and privacy boundaries.

The goal is controlled support for many kinds of research-project work. The agent should help organise, review, draft, and maintain project materials without inventing facts, losing context, or leaking private data.

The operating sequence is:

1. classify the task;
2. choose the smallest useful skill set, including bounded/light routes for source planning, lookup, and minor edits;
3. compute the minimum useful recall tier;
4. check stage continuity when later-stage work depends on earlier decisions;
5. check sources before formal claims;
6. constrain formal claim strength with Claim Ledger Lite when claim-support or source-readiness changes are involved;
7. package evidence status with a Material Passport before formal artifacts move forward;
8. run integrity preflight before substantive formal drafting;
9. make claims, gaps, warrants, and boundaries explicit before drafting;
10. run self-review before style polishing;
11. check authorial voice when prose risks becoming generic, detector-framed, or disclosure-unsafe;
12. scan repeated style fingerprints before formal delivery;
13. require execution receipts for selected formal-writing gates;
14. use quality gates, Visible Output QA, and formal delivery guards before formal delivery;
15. record important decisions in project memory;
16. keep production work and system maintenance separate.

## 2. What The System Is For

Use it for:

- dissertation, article, grant, fieldwork, design research, report, evidence synthesis, or knowledge-base planning;
- proposal, manuscript, chapter, protocol, report, or work-package structure;
- ethics, IRB, privacy, funder, journal, client, and participant-facing materials;
- literature-search planning;
- source register and source-readiness checks;
- interview guide, analysis plan, concept-card, or design-material planning;
- Word document workflows;
- knowledge-base and Obsidian-style note organisation;
- agent-system maintenance and false-run checks;
- GitHub-safe sharing.

Do not use it as a substitute for:

- supervisor, PI, editor, reviewer, funder, or client judgement;
- institutional ethics, IRB, legal, or governance approval;
- official module, programme, journal, funder, client, or institutional rules;
- real citation verification;
- secure participant-data management;
- guaranteed grades or assessment outcomes.

## 3. Main Architecture

| Layer | Main Files | Job |
|---|---|---|
| Rule layer | `AGENTS.md`, `PROJECT_AGENT_PREFERENCES.md` | Defines how the agent should behave |
| Profile layer | `PROJECT_TYPE_PROFILES.md`, `RESEARCH_PROJECT_BRIEF_TEMPLATE.md` | Adapts the system to different project types |
| Skill layer | `.agents/skills/` | Provides task-specific workflows |
| Memory layer | `research-wiki/` | Stores project state, decisions, open questions, and handoff notes |
| Source layer | `knowledge-base/` | Stores source registers, metadata, and source notes |
| Compliance layer | `compliance/PROJECT_COMPLIANCE_TRACKER.md` | Tracks ethics, privacy, legal, funder, journal, client, IP, and AI-use requirements |
| Quality layer | `quality-gates/PROJECT_DELIVERY_REVIEW_GATE.md`, `university-guidance/` | Stores general delivery gates and optional assessed-academic requirements |
| Writing quality layer | `.agents/skills/cognitive-frameworks/`, `.agents/skills/academic-self-review-loop/`, `research-wiki/WRITING_QUALITY_RUBRIC.md` | Checks argument depth, paragraph quality, warrants, and revision quality before style polishing |
| Stage continuity layer | `research-wiki/STAGE_GRAPH.md`, `research-wiki/STAGE_CONTINUITY_PROTOCOL.md`, `scripts/stage_recall_policy.py`, `scripts/stage_continuity_capsule_check.py` | Prevents later-stage work from ignoring upstream source-of-record decisions while keeping recall token-aware |
| Claim boundary layer | `research-wiki/CLAIM_LEDGER_LITE_PROTOCOL.md`, `scripts/claim_ledger_lite_check.py` | Keeps formal claims, claim-support audits, and source-readiness changes within evidence boundaries |
| Integrity layer | `.agents/skills/academic-integrity-preflight/`, `scripts/academic_integrity_preflight.py` | Checks concrete prompt residue, placeholder, fake-reference, unsupported-claim, and disclosure-boundary risks |
| Authorial voice layer | `.agents/skills/authorial-voice-integrity/`, `research-wiki/AI_WRITING_AUTHORIAL_VOICE_POLICY.md`, `scripts/authorial_voice_scan.py` | Improves authorial judgement and project-appropriate style while blocking detector-evasion and disclosure-hiding requests |
| Borrowed-pattern boundary layer | `scripts/borrowed_pattern_boundary_lint.py` | Prevents imported public style/workflow patterns from becoming detector-evasion, detector-score, authorship-verdict, or humanising-as-evasion guidance |
| Style fingerprint layer | `.agents/skills/style-fingerprint-gate/`, `scripts/style_fingerprint_scan.py` | Scans repeated binary negative-contrast templates before formal delivery |
| Skill execution evidence layer | `scripts/skill_execution_receipt.py`, `research-wiki/SKILL_EXECUTION_RECEIPT_PROTOCOL.md` | Requires selected skills to produce evidence receipts rather than only being mentioned in chat |
| Formal delivery layer | `.agents/skills/material-passport/`, `.agents/skills/formal-delivery-guard/`, `scripts/material_passport.py`, `scripts/pre_delivery_lock.py`, `scripts/formal_delivery_guard.py`, `research-wiki/VISIBLE_OUTPUT_QA_PROTOCOL.md`, `scripts/visible_output_qa_check.py` | Packages readiness evidence, creates pre-delivery locks, checks visible surfaces, and blocks formal delivery when required evidence is missing |
| Self-growing KB layer | `knowledge-base/self-growing/`, `scripts/kb_health_check.py` | Controls raw intake, growth queue triage, compiled-wiki navigation, and KB health checks |
| Retrieval layer | `scripts/build_agent_index.py`, `scripts/local_retrieval_search.py`, `scripts/build_vector_index.py` | Provides local SQLite/FTS/hashed retrieval and optional ChromaDB neural retrieval |
| Privacy layer | `PRIVACY_CHECKLIST.md`, `PUBLIC_RELEASE_AUDIT.md`, `scripts/privacy_check.sh` | Prevents private data from being shared accidentally |
| Runtime layer | `scripts/agent_runtime.py`, `scripts/session_log_integrity_check.py`, `scripts/codex_sqlite_log_guard.py`, `research-wiki/runtime-receipts/`, `research-wiki/SESSION_EVENT_LOG.jsonl` | Makes workflow routing, light/full receipt choices, session-log integrity, and Codex diagnostic-log safety auditable |
| Connector layer | `scripts/academic_database_connector.py`, `config/academic_database_connectors.example.json` | Supports public metadata search and subscription credential checks |
| Independent review layer | `scripts/build_external_review_bundle.py`, `scripts/claude_independent_review.py` | Optional advisory review through a local bundle for Codex/ChatGPT/Claude/Gemini/human review, with Claude Code as one direct runner |
| Schema layer | `research-wiki/tool-schemas/`, `scripts/validate_agent_schemas.py` | Keeps local workflow tools explicit and testable |
| GitHub layer | README, setup docs, changelog, template settings | Supports sharing and updating the starter kit |

## 4. Two-Window Workflow

The system works best with two Codex windows.

### Production Window

Use this for project outputs:

- research focus and gap discussion;
- proposal, manuscript, report, protocol, or grant drafting;
- literature review planning;
- ethics wording;
- participant-facing documents;
- interview guide or concept-card work;
- supervisor/PI/client/reviewer-facing summaries;
- Word document delivery.

The Production Window should route every non-trivial task through `agent-orchestration` and use source-first, style, and quality gates when needed.

For substantial work, run deterministic preflight first:

```bash
python3 scripts/agent_runtime.py "YOUR TASK" --window Production --write --strict
```

### Maintenance Window

Use this for system reliability:

- skill updates;
- rule conflicts;
- false-run checks;
- privacy checks;
- GitHub updates;
- Obsidian or knowledge-base structure;
- workflow and automation audits.

The Maintenance Window should avoid formal project drafting unless the user explicitly asks to switch roles.

Maintenance routing is intentionally conservative. In the Maintenance Window, words such as audit, update, implement, workflow, template, and GitHub usually make system maintenance the lead route. This keeps rule edits, automation updates, and public-release work from being mistaken for ordinary research writing.

Production routing is intentionally proportional. Source planning, literature-priority sorting, bounded source lookup, and minor citation/typo edits should stay on light receipt routes unless the task asks for formal prose, Word/DOCX, stakeholder-facing or submission-facing output, or protected source-of-record edits.

## 5. Skill System

Skills are small local workflow files. Each skill tells the agent when to use it and what checks to perform.

Important skill groups:

| Group | Skills |
|---|---|
| Routing and profile adaptation | `agent-orchestration`, `research-project-adapter` |
| Source checking | `dissertation-source-first-gate`, `dissertation-citation-audit` |
| Writing and review | `material-passport`, `academic-integrity-preflight`, `cognitive-frameworks`, `academic-self-review-loop`, `authorial-voice-integrity`, `dissertation-argument-spine`, `dissertation-research-review`, `uk-academic-writing-style`, `style-memory-and-revision-gate` |
| Document delivery | `formal-delivery-guard`, `dissertation-document-quality-gate`, `context-continuity` |
| Literature and sources | `dissertation-research-search-protocol`, `dissertation-literature-review`, `dissertation-learning-loop`, `dissertation-knowledge-ops` |
| Ethics, compliance, and risk | `responsible-ai-agent-audit`, `dissertation-shared` |
| Qualitative research | `qualitative-theme-audit`, `codesign-output-synthesis`, `teacher-adoption-modeling` |
| AI-agent concept work | `ai-agent-design-spec`, `active-learning-design-support`, `prototype-evaluation-audit` |
| Maintenance | `dissertation-agent-self-debug`, `dissertation-agent-architecture-audit`, `dissertation-workspace-surface-audit`, `dissertation-automation-audit`, `dissertation-skill-stocktake` |
| Workflow adapters | `using-superpowers`, `brainstorming`, `project-skill-creator-governance`, `playwright-dissertation-browser`, `markitdown` |
| Research figure and article-style layers | `research-neural-network-figure`, `research-nature-figure`, `research-nature-writing` |

The `research-*` skills are optional quality layers. Use them only after local source, privacy, compliance, and writing-quality gates. They should improve figure logic or article-style flow, not inflate claims or replace evidence.

## 6. New Workflow Adapters

### `using-superpowers`

Adds Superpowers-style discipline without installing the full external package. It reminds the agent to check applicable skills, use brainstorming before unclear design, plan before risky implementation, and verify before completion.

Boundary: it does not override source-first, rubric, privacy, or document-quality rules.

### `brainstorming`

Use before unclear or high-impact research-design decisions. It helps turn a rough idea into a route, rationale, and next action.

Boundary: it should not slow down simple tasks.

### `project-skill-creator-governance`

Use before creating or changing project skills. It checks overlap, trigger clarity, safety boundaries, and whether the global `skill-creator` should be used.

Boundary: it prevents skill bloat and stale duplicated skills.

### `playwright-dissertation-browser`

Use before browser automation. It routes browser work through the global `playwright` skill while preserving read-only mode for LMS, journal, funder, client, institutional, or other private pages.

Boundary: no submitting, uploading, downloading, or modifying private sites without explicit confirmation.

### `markitdown`

Use before converting documents into Markdown for source review, notes, or knowledge-base ingestion.

Boundary: MarkItDown may not be installed. The agent must check availability and ask before installing dependencies.

## 7. Source-First Rule

Before formal drafting or factual claims, the agent must check sources.

Source-first applies to:

- names;
- emails;
- supervisors or institutional contacts;
- PIs, collaborators, reviewers, funders, or client contacts;
- dates and deadlines;
- module or programme requirements;
- journal, funder, client, legal, ethics, or institutional requirements;
- word counts;
- marking criteria;
- rubrics;
- ethics requirements;
- participant facts;
- citations, quotations, and page numbers.

If a fact is not confirmed, the agent should write `TO CONFIRM`.

## 7A. Runtime And Research Connectors

Version `v0.4.0` adds a local engineering layer.

| Tool | Job |
|---|---|
| `scripts/agent_runtime.py` | Checks task type, mode, skills, gates, and required files before substantial work |
| `scripts/stage_recall_policy.py` | Computes token-aware recall tiers from task intent, target files, and change type |
| `scripts/stage_continuity_capsule_check.py` | Checks whether a Stage Continuity Capsule names upstream files, inherited decisions, open confirmations, and boundaries |
| `scripts/session_log_integrity_check.py` | Checks JSONL session logs, legal window labels, runtime/window alignment, paired session starts/ends, and timestamp parseability |
| `scripts/codex_sqlite_log_guard.py` | Scans and monitors Codex `logs_*.sqlite` / WAL growth; optional trigger, checkpoint, and archive actions are guarded and dry-run by default |
| `scripts/claim_ledger_lite_check.py` | Checks Claim Ledger Lite tables for required fields, evidence-status boundaries, cannot-prove fields, concept contracts, and metadata-only overclaims |
| `scripts/visible_output_qa_check.py` | Checks Visible Output QA notes for artifact, communication job, rendered/preview evidence, deterministic checks, visual inspection, baseline/regression boundary, unresolved risks, and verdict |
| `scripts/borrowed_pattern_boundary_lint.py` | Lints borrowed public style/workflow pattern language for unsafe detector-evasion, detector-score, authorship-verdict, or humanising-as-evasion imports |
| `scripts/build_external_review_bundle.py` | Builds a local external-review bundle for Codex, ChatGPT, Claude, Gemini, or human review |
| `scripts/claude_independent_review.py` | Optional privacy-gated Claude Code runner for the same advisory external-review role |
| `scripts/academic_integrity_preflight.py` | Checks concrete integrity risks before formal drafting or delivery |
| `scripts/authorial_voice_scan.py` | Flags detector-evasion framing, disclosure hiding, prompt residue, generic AI-style phrasing, inflated vocabulary, and possible overclaiming |
| `scripts/style_fingerprint_scan.py` | Scans repeated binary negative-contrast templates such as `rather than`, `not...but`, `不是...而是`, and `而不是` |
| `scripts/skill_execution_receipt.py` | Creates/checks skill execution receipts with evidence hashes |
| `scripts/document_quality_check.py` | Checks whether document-quality review evidence is concrete |
| `scripts/self_review_loop_check.py` | Checks whether self-review records concrete findings, revision actions, and a fresh second-pass judgement |
| `scripts/material_passport.py` | Generates short or full readiness passports for formal research artifacts |
| `scripts/pre_delivery_lock.py` | Creates/checks local pre-delivery lock receipts |
| `scripts/formal_delivery_guard.py` | Blocks formal delivery when required lock or final checks are missing, with an auditable override path |
| `scripts/cognitive_protocol_check.py` | Checks whether a planning note has required cognitive protocol fields |
| `scripts/academic_database_connector.py` | Searches OpenAlex, Crossref, Semantic Scholar, and checks subscription-provider credentials |
| `scripts/citation_style_check.py` | Checks author-year citations against reference entries |
| `scripts/citation_claim_audit.py` | Creates a claim-by-claim source-support review queue |
| `scripts/kb_health_check.py` | Checks self-growing KB structure, raw-inbox triage, unresolved markers, and private-data boundary hits |
| `scripts/build_agent_index.py` | Builds a dependency-free SQLite index of project memory files |
| `scripts/local_retrieval_search.py` | Runs local FTS and hashed-vector retrieval over project files |
| `scripts/build_vector_index.py` | Builds optional ChromaDB neural vector index when vector dependencies are installed |
| `scripts/vector_retrieval_smoke_test.py` | Smoke-tests optional vector retrieval against known template queries |
| `scripts/run_skill_evals.py` | Checks whether high-risk skill routes point to available local skills/tools |
| `scripts/run_behavioral_evidence_checks.py` | Checks whether project files contain workflow evidence for runtime, source-readiness, self-review, and checkpoints |

Boundary:

- public metadata search is not claim evidence;
- subscription databases need lawful credentials;
- runtime preflight works only when the workflow calls it;
- token-aware recall controls context budget only and cannot override source, compliance, citation, privacy, document-quality, delivery, or stage-continuity gates;
- Stage Continuity applies only when a task both produces or changes a high-risk later-stage artifact and has a known upstream dependency;
- claim-support audit still needs source-section reading before verification.
- External reviewer feedback from Codex, ChatGPT, Claude, Gemini, or a human reviewer is advisory only and cannot replace source, privacy, citation, compliance, or delivery gates.
- Python 3 is needed for these local scripts; extra Python packages are not needed by default.
- Style fingerprint scans and authorial voice scans are writing-quality checks, not AI detectors.
- Skill execution receipts prove an evidence artifact exists. They do not prove academic sufficiency, source support, or that a revision was deep enough.

## 7B. Weekly Literature Gap-Watch Automation

The starter kit includes a template for weekly literature monitoring in `docs/WEEKLY_LITERATURE_GAP_WATCH_AUTOMATION.md`.

Use it when a project already has a literature map and needs a small, priority-weighted candidate list.

Default boundary:

- top 5-8 candidates only;
- public metadata remains `METADATA ONLY`;
- no automatic write to source registers, source-readiness matrices, source notes, Obsidian, Zotero, or formal text;
- methodology searching stays off unless a concrete methodology gap or active methodology-writing task requires it;
- when formal drafting begins, the automation should shift from broad discovery to source-readiness upgrade queues.

## 8. Quality Gates

Formal outputs should pass the relevant gates before delivery.

| Gate | Use When |
|---|---|
| Source-first gate | Before formal writing or factual claims |
| Project delivery review gate | Before formal project outputs |
| Rubric or requirement evidence gate | Before marking criteria, journal/funder/client requirements, grade band, deadline, or word-count claims |
| Distinction delivery gate | Optional; only for assessed academic documents when a high-band target is relevant |
| Style gate | Before user-facing academic prose |
| Style fingerprint gate | Before formal delivery when repeated binary contrast templates may be present |
| Writing quality rubric | Before formal prose moves to style polishing |
| Academic self-review loop | Before formal prose moves to document-quality or delivery checks |
| Skill execution receipt gate | Before final delivery when the runtime lists required receipts |
| Material Passport | Before a formal artifact moves from planning to drafting, drafting to review, or review to delivery |
| Pre-delivery lock | Before presenting a formal Word/PDF/stakeholder-facing artifact as usable |
| Formal delivery guard | Final check before formal delivery or explicit override |
| Document-quality gate | Before formal documents, Word files, or stakeholder-facing outputs |
| Context-continuity gate | After long tasks or important decisions |

Delivery gates are indicative readiness checks. They do not promise a grade, publication, funding, approval, or client acceptance.

## 9. Knowledge Base

The system separates thinking notes from source evidence.

| Location | Use |
|---|---|
| `research-wiki/TASK_STATE.md` | Latest progress and next actions |
| `research-wiki/PROJECT_OVERVIEW.md` | Stable project facts |
| `research-wiki/OPEN_QUESTIONS.md` | Unresolved questions |
| `knowledge-base/SOURCE_REGISTER.md` | Source inventory |
| `knowledge-base/SOURCE_READINESS_MATRIX.md` | Whether sources are ready for formal use |
| `knowledge-base/sources/` | Individual source notes |
| `knowledge-base/self-growing/raw-inbox/` | Temporary intake queue for untriaged material |
| `knowledge-base/self-growing/growth-queue.md` | Triage queue for material that may become durable knowledge |
| `knowledge-base/self-growing/compiled-wiki/` | Theme-level navigation and synthesis layer linked to source-of-record files |

Obsidian can be used as a reading and navigation layer, but the source of record should remain in the project files.

Run:

```bash
python3 scripts/kb_health_check.py
python3 scripts/build_agent_index.py --rebuild --summary
python3 scripts/local_retrieval_search.py --query "source readiness"
```

Optional neural vector retrieval requires `requirements-vector.txt`:

```bash
bash scripts/run_vector_index.sh
```

Retrieval output is candidate lookup only. It does not prove citation readiness, official requirements, or claim support.

## 10. Writing Quality Layer

The starter kit separates reasoning quality from surface style.

### `cognitive-frameworks`

Use before major research writing. It forces the agent to state:

- section type;
- main claim;
- gap/problem type;
- evidence base;
- warrant;
- boundary;
- rhetorical plan.

This helps prevent vague gap statements, unsupported claims, and source lists without argument.

### `academic-self-review-loop`

Use after cognitive planning and before style polishing. It requires:

1. first-pass review;
2. top two or three concrete weaknesses;
3. revision that improves argument quality;
4. fresh second-pass judgement.

### `WRITING_QUALITY_RUBRIC.md`

This rubric checks six intrinsic writing qualities:

- one point per paragraph;
- mini-claim topic sentence;
- argument progression;
- evidence integration;
- reader journey;
- redundancy control.

It does not predict marks, publication, funding, approval, or client acceptance.

### `style-fingerprint-gate`

Use after self-review/authorial voice work and before final delivery. It scans repeated negative-contrast templates that can make formal prose sound mechanical, while preserving legitimate academic scope distinctions.

### Skill execution receipts

For substantial formal tasks, `scripts/agent_runtime.py` lists required receipts by task type. The agent should create receipts after required gates produce evidence. Missing receipts can block delivery through `scripts/formal_delivery_guard.py`.

Receipts make execution visible. They do not prove that the underlying evidence is sufficient or that the writing revision is deep enough.

## 11. Document Workflow

For important Word, PDF, or stakeholder-facing outputs, use a three-stage checkpoint workflow.

| Stage | Main Work | Output |
|---|---|---|
| Thinking | route task, check sources, build cognitive protocol and argument logic | `*_THINKING_CHECKPOINT.md` |
| Writing | draft/revise, run self-review loop, apply writing-quality, authorial voice, style fingerprint, and document-quality checks | `*_WRITING_CHECKPOINT.md` |
| Delivery | run full Material Passport, project delivery gate, pre-delivery lock, skill-receipt checks, formal delivery guard, citation checks, Word/PDF/render checks | `*_DELIVERY_CHECKPOINT.md` |

If no formal artifact is generated, the delivery checkpoint should be marked not applicable.

## 12. Privacy And GitHub Sharing

Before sharing or opening the repository:

1. remove real personal details;
2. remove private supervisor, PI, reviewer, funder, or client feedback;
3. remove LMS screenshots or restricted content;
4. remove raw data, transcripts, recordings, and signed consent forms;
5. remove credentials, tokens, cookies, `.env` files, and browser profiles;
6. run `scripts/privacy_check.sh`;
7. complete `PRIVACY_CHECKLIST.md`;
8. complete `PUBLIC_RELEASE_AUDIT.md` before public release.

## 13. Project Profiles

Start with `PROJECT_TYPE_PROFILES.md`.

The same system can support:

- taught dissertation / thesis;
- journal article / manuscript;
- research proposal / grant;
- qualitative fieldwork project;
- quantitative or computational study;
- design research / product research;
- policy / practice report;
- literature review / evidence synthesis;
- knowledge-base / RAG project.

The file names may still include `dissertation-*` for compatibility. The selected project profile controls how the workflow should be interpreted.

## 14. Recommended First Use

After cloning the template, ask the agent:

```text
Please work as my research-project agent.

Project path:
<PROJECT_ROOT>

Please read:
- AGENTS.md
- PROJECT_AGENT_PREFERENCES.md
- RESEARCH_PROJECT_BRIEF.md
- PROJECT_TYPE_PROFILES.md
- research-wiki/TASK_STATE.md
- research-wiki/WINDOW_WORKFLOW_PROMPTS.md
- .agents/skills/

Tell me:
1. what this system can do;
2. what facts are still TO CONFIRM;
3. which project facts I should fill in first.

Do not invent names, institutional, journal, funder, client, ethics, or legal requirements, dates, sources, data, findings, or citations.
```

## 15. Current Boundaries

- This is a starter kit, not a completed research project.
- It includes generic workflows and placeholders.
- It does not include official requirements for any specific institution, journal, funder, client, or discipline.
- It does not include real participant data.
- It does not require Claude Code for the default workflow.
- Users without Claude Code can use the local external-review bundle workflow with another Codex window, ChatGPT, Claude, Gemini, or a human reviewer.
- Claude Code can still be used as one optional direct runner if the user has access; it does not replace source evidence or local gates.
- It does not require credentials by default.
- It does not install external packages by default.

## 16. Good Next Steps

1. Fill `RESEARCH_PROJECT_BRIEF.md` from confirmed sources.
2. Set up `knowledge-base/SOURCE_REGISTER.md`.
3. Select a project profile.
4. Decide whether the project needs Obsidian.
5. Confirm ethics, compliance, output, and formatting rules from official sources.
6. Keep private data out of the repository.
7. Run privacy checks before sharing.
