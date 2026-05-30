<!-- 
  AGENTS.example.md — Copy this to AGENTS.md and fill in your details.
  Lines marked [CUSTOMISE] need your input.
-->

# Research Project Agent Guide

Project: `PROJECT_TITLE`

This repository is a reusable research-agent starter kit. It can be adapted for dissertations, theses, journal articles, grants, fieldwork, policy reports, design research, evidence synthesis, and knowledge-base projects.

Replace placeholders with project-specific facts only after checking a source file or receiving direct user confirmation.

## Project Profile

Before serious work, choose a profile in `RESEARCH_PROJECT_BRIEF.md` using `PROJECT_TYPE_PROFILES.md`.

Default profile: `TO CONFIRM`

Examples:

- taught dissertation / thesis
- journal article / manuscript
- research proposal / grant
- qualitative fieldwork project
- quantitative or computational study
- design research / product research
- policy / practice report
- literature review / evidence synthesis
- knowledge-base / RAG project

## Project Skills

Project-level skills live in `.agents/skills/`.

Use these skills for research-project work. Some skill names still begin with `dissertation-*` for backwards compatibility; treat them as general research workflows unless the selected project profile is specifically a dissertation or thesis.

- `agent-orchestration`: route each task to the right skills and decide whether subagents are useful.
- `dissertation-source-first-gate`: check source files before drafting formal text or factual claims.
- `dissertation-document-quality-gate`: review formal outputs before delivery.
- `dissertation-learning-loop`: turn new reading and confirmed decisions into durable project memory.
- `dissertation-literature-review`: plan and synthesise literature review work.
- `dissertation-research-search-protocol`: structure literature, web, policy, LMS, and source searches.
- `cognitive-frameworks`: make section type, claim, gap/problem type, evidence, warrant, boundary, and rhetorical plan explicit before major writing.
- `academic-self-review-loop`: run a two-pass writing-quality review and revision loop before style and document-quality gates.
- `dissertation-argument-spine`: build the controlling argument and section logic.
- `dissertation-chapter-plan`: plan chapters, section jobs, and writing schedules.
- `dissertation-research-review`: review research design, questions, methods, claims, and drafts.
- `dissertation-citation-audit`: verify citations and claim support.
- `uk-academic-writing-style`: check British-English academic style when relevant.
- `style-memory-and-revision-gate`: apply user style preferences and prohibited-phrase checks.
- `context-continuity`: keep task state and handoff notes usable across long work.
- `dissertation-knowledge-ops`: maintain research-wiki, knowledge-base, Obsidian, and source registers.
- `dissertation-agent-self-debug`: diagnose false runs, stale assumptions, or shallow checking.
- `dissertation-agent-architecture-audit`: audit rule stacks, memory layers, and skill routing.
- `dissertation-workspace-surface-audit`: audit local tools, files, rendering, connectors, and missing surfaces.
- `dissertation-automation-audit`: audit scheduled checks, hooks, monitors, and automation safety.
- `dissertation-skill-stocktake`: review skills for overlap, stale rules, and trigger clarity.
- `using-superpowers`: apply a project-safe Superpowers-style skill-first workflow without overriding source-first, quality-gate, privacy, or window-separation rules.
- `brainstorming`: structure unclear research-project or agent-system ideas before drafting, implementation, or skill changes.
- `project-skill-creator-governance`: govern new or updated project skills and route SKILL.md authoring to the global `skill-creator` skill.
- `playwright-dissertation-browser`: safely route browser automation to the global `playwright` skill while preserving read-only and privacy boundaries.
- `markitdown`: guide file-to-Markdown conversion for source review, literature ingestion, Obsidian notes, or RAG-ready knowledge-base preparation.
- `research-project-adapter`: map the starter kit to the selected project profile and decide which dissertation-specific files are optional.
- `research-neural-network-figure`: plan or audit neural-network architecture figures and tool routes such as NN-SVG, PlotNeuralNet, draw_convnet, TikZ, or custom SVG.
- `research-nature-figure`: apply high-impact scientific figure-contract logic to data, conceptual, architecture, and multi-panel figures.
- `research-nature-writing`: sharpen high-impact article-style argument structure after source, compliance, citation, cognitive, and self-review gates.

Global/system skills intentionally used by this template:

- `skill-creator`: use with `project-skill-creator-governance` when creating or updating `SKILL.md` files.
- `playwright`: use with `playwright-dissertation-browser` when a task needs CLI browser automation.

Domain-specific skills are included as optional examples. Rename, edit, or remove them if your research topic does not need them.

## Safety Rules

- Treat `USER_DASHBOARD.md` as the user-facing status hub if you create one.
- For non-trivial tasks, first use `agent-orchestration` to classify the task and select skills.
- For project-type setup, first read `PROJECT_TYPE_PROFILES.md` and `RESEARCH_PROJECT_BRIEF_TEMPLATE.md`.
- For substantial Production or Maintenance tasks, run deterministic runtime preflight first when local tools are available:
  - `python3 scripts/agent_runtime.py "<TASK>" --window Production --write --strict`
  - or `python3 scripts/agent_runtime.py "<TASK>" --window Maintenance --write --strict`
  If it returns `BLOCKED`, fix the missing file or gate before continuing.
- Do not invent names, emails, supervisor/PI/client details, dates, funder/journal/client/institutional requirements, rubrics, citations, participant facts, datasets, results, or findings.
- For formal drafting or editing, use `dissertation-source-first-gate`.
- For substantial proposal, manuscript, report, grant, literature review, methodology, or stakeholder-facing writing, use `cognitive-frameworks` after source-first and before drafting.
- For formal academic or professional prose, use `academic-self-review-loop` after cognitive planning and before style/document-quality gates.
- For important Word, PDF, or stakeholder-facing delivery, follow `research-wiki/DOCUMENT_PIPELINE.md` and record thinking, writing, and delivery checkpoints, or mark delivery checkpoint not applicable.
- For rubric, marking criteria, journal author guidelines, funder rules, client requirements, deadlines, word counts, or submission rules, use the strongest available project requirement source. For assessed academic work, use `university-guidance/RUBRIC_EVIDENCE_GATE.md`.
- For formal, supervisor/PI/client/reviewer-facing, or submission-facing documents, use `quality-gates/PROJECT_DELIVERY_REVIEW_GATE.md` before delivery. Use `university-guidance/DISTINCTION_DELIVERY_REVIEW_GATE.md` only when the selected profile is assessed academic work and a high-band target is relevant.
- For formal outputs, use `dissertation-document-quality-gate` before delivery.
- For academic or professional prose, use `uk-academic-writing-style` and `style-memory-and-revision-gate` when language quality matters. Adapt spelling, tone, and format to the project context.
- Keep confirmed evidence separate from interpretation.
- Mark unresolved facts as `TO CONFIRM`.
- Treat participant data, identifiable notes, recordings, transcripts, and signed consent forms as sensitive.
- Keep raw participant data outside this repository unless it is ethically approved, anonymised, and intentionally stored.
- Use `compliance/PROJECT_COMPLIANCE_TRACKER.md` before handling ethics, IRB, privacy, funder, journal, client, IP, AI-use, or data-management requirements.
- When editing official templates, preserve fixed template text unless clearly editable.
- Before GitHub sharing, run `scripts/privacy_check.sh` and complete `PRIVACY_CHECKLIST.md`.
- Use `brainstorming` before high-impact or unclear research route, method, concept-card, skill, or system design decisions when the next action is not obvious.
- Use `project-skill-creator-governance` before adding, copying, adapting, or updating project skills; use global `skill-creator` for SKILL.md authoring.
- Use `playwright-dissertation-browser` before browser automation for LMS, local previews, or browser-visible verification; do not submit, download, or modify browser content without explicit confirmation.
- Use `markitdown` before file-to-Markdown conversion; check whether MarkItDown is installed and do not install it without explicit confirmation.
- Use `scripts/academic_database_connector.py` for academic metadata searches when available. Treat all search results as `METADATA ONLY` until source sections are reviewed.
- Use `scripts/citation_style_check.py` and `scripts/citation_claim_audit.py` for citation-heavy drafts when available. Citation consistency is not proof of claim support.
- Use `scripts/claude_independent_review.py` only for optional independent review of safe, non-sensitive artifacts. Claude Code feedback is advisory; it does not replace local source, privacy, citation, compliance, or delivery gates.
- Use `research-neural-network-figure` before planning actual neural-network/model architecture visuals. Do not install or run third-party figure repositories without explicit confirmation.
- Use `research-nature-figure` before high-impact or multi-panel research figures. It is a figure-quality layer, not a source/data validity layer.
- Use `research-nature-writing` only after required evidence and integrity gates for formal prose. It can sharpen article-style logic but must not inflate claims or invent citations.
- Use `research-wiki/GENERAL_RESEARCH_SKILL_COMPATIBILITY_CONTRACT.md` before exporting local `research-*` skills into this public starter kit.
- Use `docs/WEEKLY_LITERATURE_GAP_WATCH_AUTOMATION.md` before creating or revising a weekly literature-monitoring automation. Preserve the candidate-only boundary unless the user explicitly confirms ingestion.

## Deliverable Preferences

- Use Word `.docx` for formal outputs when possible.
- Use Markdown for internal project memory, checklists, source maps, logs, and notes.
- Preserve original files and create revised copies unless overwrite is explicitly requested.
- Label draft status clearly: working draft, review draft, supervisor/PI/client draft, or submission/client-ready after user confirmation.

## Recommended Workflow

1. Route the task with `agent-orchestration`.
2. Run `scripts/agent_runtime.py` for substantial tasks when local tools are available.
3. Read `RESEARCH_PROJECT_BRIEF.md` if present; otherwise use `RESEARCH_PROJECT_BRIEF_TEMPLATE.md` and mark project facts `TO CONFIRM`.
4. Read `PROJECT_AGENT_PREFERENCES.md` and relevant task-state files.
5. Use source-first checks before formal writing.
6. Use `cognitive-frameworks` before major argument, gap, methodology, literature, proposal, manuscript, report, grant, or stakeholder-facing drafting.
7. Use `academic-self-review-loop` before style polishing and document-quality review for formal prose.
8. Use the learning loop after useful reading or confirmed decisions.
9. Use source-readiness checks before citation-heavy writing.
10. Use compliance checks before ethics, privacy, funder, journal, client, or data-management claims.
11. Use rubric or requirement evidence checks before grade-band, journal, funder, deadline, or word-count claims.
12. Use `research-wiki/DOCUMENT_PIPELINE.md` for important Word/PDF/stakeholder-facing delivery.
13. Use the project delivery review gate before formal document delivery.
14. Use relevant academic/professional style gates before delivering prose.
15. Use document-quality gate before delivering formal outputs.
16. Update `research-wiki/TASK_STATE.md` after substantial work.
17. Record substantial Production work in `research-wiki/PRODUCTION_RUN_REGISTER.md` if that register is enabled.
18. Use `brainstorming` for unclear, high-impact route decisions before drafting or system changes.
19. Use `project-skill-creator-governance` and global `skill-creator` before adding or changing skills.
20. Use `playwright-dissertation-browser` and global `playwright` for controlled browser automation.
21. Use `markitdown` only after checking tool availability and privacy boundaries.
22. Use `research-*` figure/writing skills only as optional quality layers after source, privacy, compliance, citation, and document gates.
23. Use `scripts/claude_independent_review.py` for optional context-naive independent review when the artifact is safe to send to Claude Code.
24. Use staged literature gap-watch automation only for candidate discovery unless the user confirms ingestion.

## Public Template Boundary

This repository should remain generic. Do not commit:

- personal dissertation drafts;
- private supervisor, PI, reviewer, client, or funder feedback;
- LMS, intranet, journal portal, funder portal, client portal, or restricted content;
- raw participant data;
- signed consent forms;
- API keys, tokens, cookies, or browser profiles.
