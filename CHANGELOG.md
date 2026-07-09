# Changelog

## Unreleased

No changes yet.

## v1.8.0 - Context Health And Skill Lifecycle - 2026-07-09

Status: context-load reliability, active-skill lifecycle, and public onboarding update.

### Added

- `.codexignore` to keep generated runtime evidence, receipts, audit reports, session logs, context-health logs, and generated Word/PDF outputs out of default agent context.
- `scripts/context_health_signal.py` and automatic runtime context-health route signals for recording compression notices, approximate context scale, model label when exposed, route type, and degradation symptoms.
- Archived skill layer under `.agents/skills/_archived/` for topic-specific or late-phase example packs that should not load as active routes by default.
- GitHub social preview asset at `docs/assets/social-preview.png`, with editable SVG source and manifest in `docs/assets/`.
- Annotated runtime routing demo image at `docs/assets/terminal-routing-demo.png`, with editable SVG source and manifest in `docs/assets/`.
- Task Cards and a copyable Source-First Intake Card: `docs/TASK_CARDS.md`, `docs/TASK_CARDS_CN.md`, and `templates/SOURCE_FIRST_INTAKE_CARD.md`.
- `research-wiki/CLAIM_LEDGER_LITE_PROTOCOL.md`, `scripts/claim_ledger_lite_check.py`, and schema coverage for lightweight formal-claim boundary ledgers.
- `research-wiki/VISIBLE_OUTPUT_QA_PROTOCOL.md`, `scripts/visible_output_qa_check.py`, and schema coverage for rendered/previewed output checks.
- `scripts/borrowed_pattern_boundary_lint.py` and schema coverage to prevent imported style/workflow patterns from becoming detector-evasion, detector-score, authorship-verdict, or humanising-as-evasion guidance.
- Beginner onboarding guides for users new to Codex and GitHub: `docs/BEGINNER_README.md` and `docs/BEGINNER_README_CN.md`.
- `scripts/codex_sqlite_log_guard.py` and schema/eval coverage for the Codex `logs_*.sqlite` / WAL growth failure mode reported by users.
- Eval cases for Claim Ledger Lite, Visible Output QA, borrowed-pattern lint, formal/citation-heavy gate routing, and citation-key minor-edit routing.
- Eval cases for read-only Codex log scans, selective log-table trigger installation, and safe old-log archiving.
- Eval coverage for source-first task intake, route boundaries, and unsafe task-card boundary language.
- Eval coverage for `.codexignore`, context-health logging, archived skills not appearing in active routes, bounded source-planning context load, and fresh-clone maintenance preflight behaviour.

### Changed

- Simplified the README and README_CN workflow diagrams to show the public control path: output-risk routing, light receipts, source packaging, skill receipts, and delivery guard.
- Changed the project license for future distributions from MIT to PolyForm Noncommercial License 1.0.0, allowing personal, educational, research, and other non-commercial use while reserving commercial use.
- Runtime routing now adds Claim Ledger Lite to formal/citation-heavy routes, adds Visible Output QA to formal visible-output routes, and keeps no-content citation-key/reference-format repairs on the minor-edit path.
- Runtime routing now keeps pure bounded source-planning routes off heavy history/log files such as task state, production register, session event log, and workflow prompt files.
- AGENTS, agent-orchestration, system overview, and adaptation docs now treat archived topic packs as restorable examples rather than active default routes.
- README and README_CN now report 62 public skill evals and link Task Cards, Chinese Task Cards, the Source-First Intake Card, and context-health guidance.
- AGENTS, AGENTS template, project preferences, relevant skills, and receipt validation now document the new claim-ledger and visible-output boundaries.
- AGENTS and AGENTS template now route Codex diagnostic SQLite log growth through a read-only-first guard before any trigger, WAL checkpoint, or archive action.
- AGENTS and AGENTS template now route unclear user goals through Task Cards and the Source-First Intake Card before work begins.

### Boundary

- The social preview and routing demo are deterministic public assets. They do not include private project content, institution-specific requirements, participant material, screenshots, local paths, credentials, or generated private reports.
- GitHub social preview upload remains a repository-settings step if no stable API-backed update path is available.
- Earlier versions or copies already received under MIT remain governed by their original license terms; this update sets the license boundary for current and future distributions.
- Claim Ledger Lite is a claim-strength and structure check only; it does not prove source support or make metadata-only sources citation-ready.
- Visible Output QA verifies the rendered or previewed surface only; it does not prove compliance, citation support, academic/professional quality, or approval readiness.
- Beginner guides are public onboarding docs and contain no private project facts.
- Codex SQLite log guard is a local mitigation for Codex diagnostic log growth. It does not patch Codex itself and must not be used on conversation state, memory, goal, session, project, or arbitrary SQLite databases.
- Task Cards are intake and routing aids only. They explicitly exclude ghostwriting, plagiarism reduction, AI-detector evasion, fake citation/source-support workflows, and paid reseller/proxy/credit-pool patterns. Task intake is planning only; it is not evidence, citation readiness, or source-section verification.
- Context-health logs are maintenance trend data only. They do not prove model routing, source support, privacy compliance, academic/professional quality, or delivery readiness.
- `.codexignore` is a context-load guard, not a privacy or publication control. Public sync still requires `scripts/privacy_check.sh` and release-surface verification.
- Archived skills remain recoverable examples. Do not route them as active skills until a concrete project phase restores them deliberately.

## v1.7.0 - Bounded Routing And Session Log Integrity - 2026-06-11

Status: proportional routing and maintenance-audit reliability update.

### Added

- Bounded runtime task types for source planning, research lookup, and minor citation/typo edits.
- Light receipt sets for bounded source planning, bounded research lookup, and minor edits.
- `scripts/session_log_integrity_check.py` to check JSONL validity, legal window labels, runtime/window alignment, paired session starts/ends, and timestamp parseability.
- `research-wiki/tool-schemas/session_log_integrity_check.schema.json`.
- Runtime/eval coverage for protected-document minor edits, formal methodology paragraphs, bounded methodology literature search, ambiguous source planning plus summary prose, bounded source lookup, receipt-window inference, and session-log integrity pass/fail cases.

### Changed

- `scripts/agent_runtime.py` now keeps source planning, literature-priority sorting, lookup, and minor edit tasks on light routes unless the task asks for formal prose, Word/DOCX, stakeholder-facing or submission-facing output, or protected source-of-record edits.
- `scripts/run_skill_evals.py` now runs targeted behavioural checks for the new routing boundaries instead of only checking that referenced files exist.
- `scripts/skill_execution_receipt.py` infers `Maintenance` when no explicit window is provided and the stage/task type/task id clearly describes maintenance or public-sync work.
- `AGENTS.md`, `templates/AGENTS.example.md`, `PROJECT_AGENT_PREFERENCES.md`, `agent-orchestration`, `WINDOW_WORKFLOW_PROMPTS.md`, `README.md`, `README_CN.md`, and `docs/SYSTEM_OVERVIEW.md` now document bounded/light routes and session-log integrity checks.
- Skill eval registry now reports 48 public checks.

### Boundary

- Bounded routes do not weaken source, citation, privacy, compliance, or document-quality boundaries.
- Metadata-only sources remain metadata-only until source-section review supports an upgrade.
- Protected source-of-record edits still need their own route; a bounded source-planning task cannot silently update registers or formal source files.
- This release does not include private project content, institution-specific requirements, participant material, private local paths, credentials, runtime state, or generated private reports.

## v1.6.0 - Stage Continuity And Token-Aware Recall - 2026-06-10

Status: long-running project continuity and context-budget reliability update.

### Added

- `research-wiki/STAGE_GRAPH.md` as a generic, user-customisable pointer map for upstream source-of-record dependencies.
- `research-wiki/STAGE_CONTINUITY_PROTOCOL.md` to define Stage Continuity A+B triggers, non-triggers, user-skip override handling, Deep Reasoning Pass, and capsule requirements.
- `scripts/stage_recall_policy.py` to compute deterministic recall tiers from task intent, target files, and change type.
- `scripts/stage_continuity_capsule_check.py` to check capsule fields, concrete source paths, and confirmation boundaries.
- Stage continuity unit tests and eval cases `STAGE-001`, `STAGE-002`, and `STAGE-003`.
- Claude Code advisory review packet and review report for this public sync.

### Changed

- `scripts/agent_runtime.py` now emits a `recall_decision` for every preflight and adds Stage Continuity gates only when recall reaches Tier 3 or higher.
- `agent-orchestration` now requires opening recall, mid-task recall recomputation, and pre-delivery recall reconciliation for substantial stage-sensitive work.
- `context-continuity` now owns Stage Continuity Capsules and records what later work must inherit.
- `AGENTS.md`, `PROJECT_AGENT_PREFERENCES.md`, `README.md`, and `README_CN.md` now document the workflow: opening recall prevents blind drafting, mid-task recall prevents drift, and delivery gates prevent packaging drift as a formal artifact.
- Skill eval registry now reports 38 public checks, including three new Stage Continuity cases.

### Boundary

- Stage Graph rows are starter examples, not required private-project structure. A one-row graph is valid after customisation.
- Token-Aware Recall is a context-budget controller. It cannot override source-first, compliance, citation, privacy, document-quality, or formal delivery gates.
- Deep Reasoning Pass is an auditable decision summary, not private chain-of-thought and not a replacement for cognitive frameworks or self-review.
- User-accepted skip/override records risk; it is not a quality pass.
- This release does not include private project content, institution-specific requirements, participant material, private local paths, credentials, runtime state, or generated private reports.

## v1.5.2 - DOCX Structure And Layout Guards - 2026-06-09

Status: formal Word delivery reliability update.

### Added

- `scripts/markdown_docx_structure_check.py` to verify that Markdown tables survive DOCX rendering as real Word tables instead of pipe-delimited paragraphs.
- `scripts/docx_layout_review_check.py` to catch deterministic DOCX layout regressions such as heading flattening, table loss, and count regressions against a previous accepted Word baseline.
- Internal helper `scripts/_docx_runtime.py` to route DOCX scripts to a Python runtime with `python-docx` when needed.
- Skill eval cases `DOC-004` and `DOC-005` for Markdown-DOCX structural parity and DOCX layout regression behaviour.
- Unit tests covering table-render failures, real Word table passes, heading bold override regressions, and formal delivery guard integration.

### Changed

- `scripts/formal_delivery_guard.py` now runs DOCX structural parity and layout review by default for `.docx` artifacts when applicable.
- DOCX skip/allow exception flags now require `--layout-decision-reason`, which is recorded in the formal delivery guard report.
- Runtime preflight now lists Markdown-DOCX structural parity, DOCX layout review, and layout self-review as required gates for formal delivery tasks.
- `AGENTS.md`, `PROJECT_AGENT_PREFERENCES.md`, `research-wiki/DOCUMENT_PIPELINE.md`, `research-wiki/PRODUCTION_RECEIPT_VALIDATION.md`, and delivery/document-quality skills now document structure/layout guards for important Word outputs.

### Boundary

- These checks do not replace human visual inspection of rendered pages or project-specific formatting requirements.
- `--allow-table-loss`, `--allow-layout-regression`, `--skip-structure-parity`, and `--skip-layout-review` require an explicit recorded delivery decision through `--layout-decision-reason`.
- This release does not include private dissertation content, participant data, institution-specific requirements, local runtime state, or generated project reports.

## v1.5.1 - Style Fingerprint And Skill Execution Receipts - 2026-06-07

Status: public writing-quality reliability and skill-execution evidence update.

### Added

- `.agents/skills/style-fingerprint-gate/` to scan repeated binary negative-contrast templates before formal delivery.
- `scripts/style_fingerprint_scan.py` to report density, total hits, repeated pattern categories, and example locations for constructions such as `rather than`, `not...but`, `不是...而是`, and `而不是`.
- `scripts/skill_execution_receipt.py` to create and check auditable skill execution receipts with task ID, skill, stage, status, evidence path, and evidence hash.
- `research-wiki/SKILL_EXECUTION_RECEIPT_PROTOCOL.md` to explain the difference between skill routing, skill execution evidence, and academic sufficiency.
- `scripts/document_quality_check.py` and `scripts/self_review_loop_check.py` to make document-quality and self-review checks more concrete.
- Unit tests for style/receipt-enabled delivery guard behaviour and authorial voice scan boundaries.

### Changed

- Runtime routing now emits task-specific `receipt_requirements` instead of relying on the agent to remember which skills should leave evidence.
- Formal writing routes now include `style-fingerprint-gate`, `style_fingerprint_scan`, and skill execution receipts.
- `scripts/formal_delivery_guard.py` can block missing required skill receipts and optional style/authorial-voice scans, with the existing auditable override path preserved.
- README, Chinese README, system overview, app/tool documentation, software requirements, AGENTS template, document pipeline, dependency graph, production receipt validation, and skill eval registry now document the receipt-based execution layer.
- Skill eval registry expanded from 28 to 33 public checks.

### Boundary

- Style fingerprint scanning is a writing-quality safeguard, not an AI detector.
- Authorial voice checks and style scans do not promise detector scores or authorship judgement.
- Skill receipts prove execution evidence exists. They do not prove the underlying evidence is academically sufficient, truthful, non-fabricated, or acted on.
- Delivery overrides remain traceability records only; they are not quality passes.
- No private research project content, institution details, participant material, screenshots, personal files, local paths, or credentials were added.

## v1.5.0 - Authorial Voice Integrity And Real Project Operating Guide - 2026-06-02

Status: public research-agent writing integrity and operating-practice update.

### Added

- `.agents/skills/authorial-voice-integrity/` to route "less AI-like", "humanise", "lower AI rate", detector, AIGC, and AI-use disclosure requests into integrity-safe authorial voice revision.
- `research-wiki/AI_WRITING_AUTHORIAL_VOICE_POLICY.md` to define what authorial voice work may and may not do.
- `scripts/authorial_voice_scan.py` to flag detector-evasion framing, disclosure hiding, prompt residue, generic AI-style phrasing, inflated vocabulary, and possible overclaiming.
- Unit tests for authorial-voice scan boundaries.
- `docs/REAL_PROJECT_OPERATING_GUIDE.md` for turning the starter kit into a working dissertation, thesis, manuscript, report, or evidence-synthesis workflow.

### Changed

- README, Chinese README, system overview, app/tool docs, AGENTS template, project preferences, orchestration, academic-integrity, UK style, style-memory, and writing-quality files now document the authorial voice boundary.
- Skill eval registry expanded from 25 to 28 public checks.

### Boundary

- This release does not add AI detector evasion, detection-score optimisation, disclosure hiding, ghostwriting concealment, or random style-noise rewriting.
- Authorial voice checks improve clarity, judgement, evidence boundaries, and project-specific style. They do not prove originality, authorship, source support, compliance approval, or detector outcomes.
- No private research project content, institution details, participant material, screenshots, personal files, local paths, or credentials were added.

## v1.4.0 - Material Passport And Formal Delivery Guard - 2026-06-02

Status: formal delivery reliability update.

### Added

- `.agents/skills/material-passport/` to package source-readiness, compliance/requirement status, citation boundaries, and unresolved confirmations before formal artifacts move forward.
- `scripts/material_passport.py` to generate short or full Material Passport reports.
- `.agents/skills/formal-delivery-guard/` for final formal-output delivery checks.
- `scripts/pre_delivery_lock.py` to create/check local pre-delivery lock receipts.
- `scripts/formal_delivery_guard.py` to block formal delivery when required evidence is missing, with an explicit auditable override path.
- Unit tests for Material Passport, pre-delivery lock, and formal delivery guard behaviour.

### Changed

- Runtime routing now includes `material-passport` and `formal-delivery-guard` for formal research outputs.
- Document pipeline now records Material Passport, pre-delivery lock, and formal delivery guard status in staged checkpoints.
- README, Chinese README, AGENTS template, software docs, and skill eval registry now document the new formal delivery workflow.
- Skill eval registry expanded from 23 to 25 public checks.

### Boundary

- Material Passport packages readiness evidence; it does not prove source support, compliance approval, acceptance, publication readiness, or official requirement compliance.
- Formal Delivery Guard can block agent-mediated delivery, but it cannot prevent manual bypass outside the workflow.
- Overrides create traceability records only; they are not quality passes.
- No private research project content, institution details, participant material, screenshots, or private local paths were added.

## v1.3.1 - Release Surface Verification And Public Sync Policy - 2026-06-02

Status: release hygiene and private/public sync boundary update.

### Added

- `.agents/skills/release-surface-verification/` to verify GitHub Releases, sidebar latest release, About/topics, rendered README/docs, and public links before claiming a public release or template update is complete.
- `PUBLIC_SYNC_POLICY.md` to define shared core files, private-only content, public-only onboarding files, sync checks, and release-boundary rules.

### Changed

- `dissertation-agent-self-debug` now distinguishes source-layer state from user-visible rendered surfaces when investigating false completion.
- `project-skill-creator-governance` now includes clearer examples for when to create a skill and when to use docs, templates, scripts, or preferences instead.
- Skill eval registry and README badges now include the release-surface verification case.

### Boundary

- This release does not add private dissertation content, supervisor details, institution-specific files, participant material, or local runtime state.
- A release is not treated as complete until both the source layer and GitHub-visible release surface are checked.

## v1.3.0 - Knowledge Base Setup And External Review Fallback - 2026-06-01

Status: public onboarding and quality-review update.

### Added

- `docs/EXTERNAL_REVIEW_OPTIONS.md` explaining local self-review, manual external-review bundles, and the optional Claude Code runner.
- `scripts/build_external_review_bundle.py` to create a local review bundle for Codex, ChatGPT, Claude, Gemini, or human review without calling an LLM, connecting to the internet, or uploading files.
- `templates/prompts/EXTERNAL_REVIEWER_PROMPT.md` as the shared vendor-neutral reviewer prompt.
- Tests for clean bundle generation, sensitive-content blocking, and advisory/no-invention prompt boundaries.
- `docs/OBSIDIAN_SETUP.md` and `templates/obsidian-vault/` from the Obsidian setup clarification.

### Changed

- Claude Code is now documented as one optional external-review runner, not the only independent-review path.
- README, Chinese README, app/tool documentation, system overview, AGENTS template, and architecture diagram now document Codex/ChatGPT/manual reviewer fallback.
- `scripts/claude_independent_review.py` now reuses the shared external-review prompt template.
- Skill eval registry now includes an external-review fallback case.
- `knowledge-base/` includes minimal Obsidian defaults and local-state ignore rules so it can be opened as a cleaner Obsidian vault.

### Boundary

- External reviewer feedback remains advisory only. It is not source evidence, claim-support proof, compliance approval, a mark, or a delivery pass.
- No automatic upload, sync script, hosted review service, or required Claude subscription was added.
- Obsidian remains a navigation layer, not the source of record.
- No private research project content, institution details, supervisor details, email addresses, participant material, screenshots, or private documents were added.

## v1.2.1 - Obsidian Vault Setup Clarification - 2026-06-01

Status: public documentation and onboarding fix.

### Added

- `docs/OBSIDIAN_SETUP.md` with clear Obsidian entry-point guidance in English and Chinese.
- `templates/obsidian-vault/` as a generic clean vault template for users who want a separate research notebook outside the repository.
- Minimal `knowledge-base/.obsidian/app.json` and `knowledge-base/.gitignore` so `knowledge-base/` can be opened as a cleaner Obsidian vault without committing local workspace, cache, plugin, raw-inbox, or attachment state.

### Changed

- README, Chinese README, app/connector usage, and software requirements now warn users to open `knowledge-base/` as the Obsidian vault and not the repository root.
- Obsidian documentation now states explicitly that Obsidian is a navigation layer, not the source of record.

### Boundary

- No automatic Obsidian sync script was added.
- The clean vault template contains only generic folder READMEs and neutral Obsidian defaults.
- No private research project content, institution details, supervisor details, email addresses, participant material, screenshots, or private documents were added.

## v1.2.0 - Self-Growing Knowledge Base And Integrity Preflight - 2026-05-30

Status: important public starter-kit update.

### Added

- `knowledge-base/self-growing/` scaffold with raw inbox, growth queue, compiled wiki index, example entry, and health-check folder.
- `scripts/kb_health_check.py` for self-growing knowledge-base structure, unresolved-marker, raw-inbox, and private-data boundary checks.
- `scripts/build_agent_index.py` for dependency-free SQLite project memory indexing.
- `scripts/local_retrieval_search.py` for local FTS and hashed-vector retrieval.
- `scripts/build_vector_index.py` and `scripts/vector_retrieval_smoke_test.py` for optional ChromaDB + sentence-transformers neural retrieval.
- `.agents/skills/academic-integrity-preflight/` and `scripts/academic_integrity_preflight.py` for concrete pre-delivery integrity checks.

### Changed

- Runtime routing now includes formal-writing integrity preflight and knowledge-base operations.
- Skill eval registry expanded from 17 to 21 public checks.
- README, Chinese README, setup guide, app/tool documentation, retrieval protocol, and system overview now document the self-growing KB and retrieval workflow.
- `scripts/run_vector_index.sh` now runs the optional vector build and smoke test when vector dependencies are installed.

### Boundary

- Self-growing KB content in the public repo is template-only. Real compiled wiki pages, growth queues, source notes, and health-check logs must stay local/private unless deliberately anonymised.
- Retrieval results are candidate lookup only and do not prove source support, citation readiness, or official requirement compliance.
- Academic-integrity preflight is not an AI detector and must not be used to promise detection outcomes.
- No private dissertation workspace content was added.

## v1.1.0 - Runtime Review And Gap Watch - 2026-05-30

Note: v1.1.0 and v1.2.0 were prepared on the same calendar date; v1.2.0 supersedes v1.1.0 with a larger knowledge-base and integrity-preflight update.

Status: important public starter-kit update.

### Added

- Runtime routing regression tests for research-skill migration and automation-prompt maintenance tasks.
- `tests/test_agent_runtime.py` for deterministic runtime unit tests.
- `scripts/claude_independent_review.py` as an optional privacy-gated Claude Code review wrapper with timeout handling.
- Generic `research-*` skills for neural-network architecture figures, high-impact research figures, and article-style academic prose.
- `research-wiki/GENERAL_RESEARCH_SKILL_COMPATIBILITY_CONTRACT.md` for exporting generic research skills safely.
- `docs/WEEKLY_LITERATURE_GAP_WATCH_AUTOMATION.md` as a staged, candidate-only weekly literature monitoring template.

### Changed

- Runtime classification now avoids misrouting `research-* skill migration` maintenance work as a literature-search task.
- Automation prompt/config updates now route as Maintenance-only work.
- Skill eval registry expanded from 9 to 17 public checks.
- README, Chinese README, system overview, app/connector usage, and software requirements now document the new runtime, Claude review, research-skill, and literature gap-watch layers.

### Boundary

- Claude Code review is advisory and does not replace source evidence, citation verification, privacy review, compliance checks, or delivery gates.
- The literature gap-watch automation is candidate discovery only. It must not automatically write to source registers, source-readiness matrices, source notes, Obsidian, Zotero, or formal research text.
- The `research-*` skills are optional quality layers. They must not inflate evidence, invent novelty claims, or override local project requirements.
- No private dissertation workspace content was added.

## v1.0.0-public-release - 2026-05-28

Status: first public starter-kit release.

### Added

- Clean public README and matching Chinese README.
- MIT license, contribution guide, acknowledgements, requirements files, and setup documentation.
- Example templates for project rules, cognitive protocols, source notes, ethics/compliance tracking, and rubric/guidance records.
- Documentation for dual-window workflows, skill development, retrieval protocol, software/tool requirements, and app/connector boundaries.

### Changed

- Replaced private dissertation state with generic starter-kit templates.
- Removed generated runtime receipts, system audit outputs, skill eval logs, database search reports, and private release-review artifacts from the public tree.
- Generalised project memory files so the kit can be adapted to different research topics rather than one private dissertation.
- Updated validation badges to reflect the public starter kit eval suite.

### Release Boundary

- This release is a local, file-driven research-agent starter kit. It does not include private project data, credentials, subscription-database access, or hosted runtime enforcement.
- The clean public release should be published from a fresh Git history because earlier private-history commits contained personal workflow metadata.

## Planned

- Rename `dissertation-*` skill prefixes to `research-*` for better alignment with multi-project-type support. Existing `dissertation-*` names will continue to work as aliases during the transition.

## v0.7.1-public-release-review-pack - 2026-05-28

Status: final public-release review preparation.

### Added

- `PUBLIC_RELEASE_FINAL_REVIEW.md` as a consolidated bilingual release-review document.
- The document gathers the remaining public-release checks, README/README_CN consistency review, GitHub About status, skill copyright/generalisation audit, and final human confirmation box.

### Changed

- Updated `PUBLIC_RELEASE_AUDIT.md` to point to the consolidated final review document.
- Updated GitHub About topics with `ai-agent`, `academic-research`, `privacy-first`, and `knowledge-base`.

### Boundary

- Repository visibility remains private.
- This does not mark the project as public-release cleared.
- Topic-specific skills still need generalisation or explicit optional-pack treatment before public release.

## v0.7.0-readme-style-refresh - 2026-05-28

Status: public project-page presentation refresh.

### Changed

- Rebuilt the English README as a clearer public landing page with a stronger opening pitch, agent/human entry points, badges, quick start, workflow map, feature table, tool boundaries, and privacy boundary.
- Rebuilt the Chinese README to match the same structure and onboarding flow.
- Updated README current version to `v0.7.0-readme-style-refresh`.
- Made the repository page easier for beginners to scan before cloning or sharing.

### Style Reference

- This update borrows the presentation logic of public research-agent pages such as ARIS-style README layouts: immediate value proposition, workflow-first framing, agent-readable entry point, compact onboarding, and explicit boundaries.
- No ARIS wording, images, slogans, or project-specific content were copied.

### Boundary

- This update changes public-template documentation only.
- No private research workspace files were modified.
- The starter kit remains generic and can be adapted to many research project types.

## v0.6.2-github-audit-sync - 2026-05-25

Status: GitHub metadata and release-audit synchronisation.

### Changed

- Updated README current version to `v0.6.2-github-audit-sync`.
- Updated `PUBLIC_RELEASE_AUDIT.md` to record the `v0.6.1` tooling documentation refresh.
- Marked GitHub Actions privacy check as configured and passing on recent pushes.
- Replaced origin-specific public-release wording with generic private-identity wording.
- Clarified that the repository remains private until final manual content and external-licence review is complete.

### Boundary

- This update changes public-template documentation only.
- No private research workspace files were modified.
- GitHub Actions passing does not replace manual privacy, copyright, licence, or academic-integrity review.

## v0.6.1-tooling-docs - 2026-05-25

Status: software and tooling documentation correction.

### Changed

- Added Python 3 to the minimum setup because local scripts rely on `python3`.
- Expanded `docs/APP_AND_CONNECTOR_USAGE.md` with a local script tools table.
- Documented `scripts/cognitive_protocol_check.py` and `scripts/run_behavioral_evidence_checks.py` in README and Chinese README.
- Added Claude Code as an optional independent review tool, with the boundary that it is not required and cannot replace source evidence.
- Updated `SETUP_GUIDE.md` and `docs/SYSTEM_OVERVIEW.md` so new users can see which software and local scripts are actually used.

### Boundary

- No new external dependency was added.
- Extra Python packages are still not required for the default workflow.
- This is a documentation correction for the v0.6.0 writing-quality upgrade.

## v0.6.0-writing-quality-stability - 2026-05-25

Status: important writing-quality stability upgrade.

### Added

- `.agents/skills/cognitive-frameworks/` for explicit section type, claim, gap/problem type, evidence, warrant, boundary, and rhetorical planning before major writing.
- `.agents/skills/academic-self-review-loop/` for a two-pass review-revise-review loop before style and document-quality gates.
- `research-wiki/WRITING_QUALITY_RUBRIC.md` with six intrinsic writing-quality criteria.
- `scripts/cognitive_protocol_check.py` for deterministic cognitive protocol checks.
- `research-wiki/SKILL_DEPENDENCY_GRAPH.md` to show the default formal-writing skill order.

### Changed

- `research-wiki/DOCUMENT_PIPELINE.md` now uses three staged checkpoints: thinking, writing, and delivery.
- Runtime preflight now routes formal research outputs through `cognitive-frameworks`, `academic-self-review-loop`, and checkpoint gates.
- Production receipt validation now checks cognitive protocol, self-review loop, writing-quality rubric, and checkpoint records.
- Skill eval and behavioural evidence checks now include writing-quality stability cases.
- README, Chinese README, system overview, preferences, and window prompts now document the new writing-quality layer.

### Boundary

- This upgrade improves workflow discipline and writing-quality review. It does not guarantee grades, publication, funding, approval, or client acceptance.
- No private dissertation workspace content was added.
- The update is generic and suitable for many research project types.

## v0.5.1-bilingual-readme - 2026-05-25

Status: bilingual documentation update.

### Added

- `README_CN.md` as a full Chinese-language README for Chinese readers.
- `docs/APP_AND_CONNECTOR_USAGE.md` as a bilingual app/connector usage status guide.

### Changed

- `README.md` now links to `README_CN.md` at the top.
- `README.md`, `README_CN.md`, and `docs/SOFTWARE_AND_PLUGIN_REQUIREMENTS.md` now link to the app/connector usage guide.
- README current version now points to `v0.5.1-bilingual-readme`.

### Boundary

- This update changes public-facing documentation only.
- No private dissertation workspace content was added.
- The English README remains the default GitHub landing page.

## v0.5.0-general-research-projects - 2026-05-25

Status: important generalisation upgrade.

### Added

- `RESEARCH_PROJECT_BRIEF_TEMPLATE.md` as the default setup file for any research project.
- `PROJECT_TYPE_PROFILES.md` with profiles for dissertation/thesis, article, grant, fieldwork, computational study, design research, policy/practice report, evidence synthesis, and knowledge-base/RAG projects.
- `research-project-adapter` skill for mapping the starter kit to the selected project type.
- `quality-gates/PROJECT_DELIVERY_REVIEW_GATE.md` as the project-neutral delivery gate.
- `compliance/PROJECT_COMPLIANCE_TRACKER.md` for ethics, privacy, journal, funder, client, legal, IP, data-management, and AI-use requirements.
- `docs/ADAPTING_TO_OTHER_RESEARCH_PROJECTS.md`.
- `outputs/` as the generic output folder.

### Changed

- README now presents the repository as a general research-agent starter kit, not a dissertation-only template.
- `AGENTS.md`, `PROJECT_AGENT_PREFERENCES.md`, `docs/SYSTEM_OVERVIEW.md`, and window prompts now use research-project language by default.
- Runtime preflight now includes the research project brief, project profiles, compliance tracker, and general delivery gate.
- Skill evals now include a project-profile adaptation case.
- Dissertation/thesis remains a supported project type, but dissertation-specific files are optional for non-dissertation projects.

### Boundary

- Existing `dissertation-*` skill names are kept for compatibility.
- This update does not migrate or alter the user's private dissertation workspace.
- Public release still requires final privacy, external-licence, and GitHub Actions checks before changing repository visibility.

## v0.4.0-runtime-research-connectors - 2026-05-25

Status: important engineering upgrade for the public starter kit.

### Added

- `scripts/agent_runtime.py` for deterministic runtime preflight.
- `scripts/academic_database_connector.py` for public metadata search and subscription-provider credential checks.
- `scripts/citation_style_check.py` for citation/reference consistency checks.
- `scripts/citation_claim_audit.py` for claim-by-claim citation support audit queues.
- `scripts/validate_agent_schemas.py`, `scripts/run_skill_evals.py`, and `scripts/run_behavioral_evidence_checks.py`.
- `research-wiki/tool-schemas/` with workflow schemas for runtime enforcement, subscription database connectors, and citation claim-support audit.
- `research-wiki/HARD_RUNTIME_ENFORCEMENT.md`.
- Starter files for source readiness, ethics readiness, document pipeline, Production receipts, external connectors, and citation workflow boundaries.
- `config/academic_database_connectors.example.json`.

### Changed

- README now foregrounds the runtime and connector upgrade.
- `AGENTS.md` now instructs substantial tasks to use deterministic runtime preflight when local tools are available.
- Task state, system overview, and preferences now describe the new engineering layer.

### Boundary

- This does not include real subscription database credentials.
- Scopus, Web of Science, and EBSCO require lawful institutional/API access.
- Citation claim-support audit creates a review queue; it does not automatically prove source support.
- Runtime preflight is local enforcement, not a hosted autonomous agent platform.

## v0.3.1-public-release-foundation - 2026-05-25

Status: private repository, public-template release foundation.

### Added

- MIT `LICENSE`.
- `CONTRIBUTING.md` with privacy, academic-integrity, skill-design, and pull-request rules.

### Changed

- README now links the licence and contribution guide.
- Public release audit now records the selected licence and contribution policy.

### Boundary

- Repository visibility should stay private until GitHub Actions privacy checks pass after push.
- External workflow licence compatibility still needs final manual confirmation before a public release.

## v0.3.0-skill-adapter-refresh - 2026-05-25

Status: private repository, public-template content draft.

### Added

- `using-superpowers` project-safe adapter skill.
- `brainstorming` structured ideation skill.
- `project-skill-creator-governance` wrapper for safe project skill creation.
- `playwright-dissertation-browser` wrapper for browser automation with read-only and privacy boundaries.
- `markitdown` workflow wrapper for file-to-Markdown conversion.
- `docs/SYSTEM_OVERVIEW.md` as a depersonalised explanation of the full system.

### Changed

- Updated `AGENTS.md` with the new adapter skills and routing boundaries.
- Updated `PROJECT_AGENT_PREFERENCES.md` with Superpowers, Brainstorming, Playwright, and MarkItDown boundaries.
- Updated `agent-orchestration` to route unclear route decisions, file conversion, browser automation, and skill migration.
- Updated window prompts so Production and Maintenance know when to use the new adapters.
- Updated README current version and linked the system overview.
- Updated software requirements with optional Playwright and MarkItDown notes.
- Added public maintainer identity as [YOUR_NAME] and kept the original student identity out of release-facing files.
- Updated the privacy checker to allow the confirmed public maintainer email while still flagging other email addresses.

### Boundary

- The full external Superpowers package is not installed.
- MarkItDown is not installed by default.
- Global `skill-creator` and `playwright` are referenced through wrappers rather than copied into the template.
- The update remains generic and should not include private dissertation details.
- Public release still needs a licence and final manual review before repository visibility changes.

## v0.2.0-public-ready-template - 2026-05-24

Status: private repository, public-ready content draft.

### Changed

- Renamed the GitHub repository from `dissertation-agent-private-template` to `research-agent-starter-kit`.
- Updated the GitHub About description:
  - `A privacy-first starter kit for dissertation and research-project agents: source-first workflows, literature ops, writing gates, and GitHub-safe sharing.`
- Added repository topics:
  - `research-agent`
  - `dissertation`
  - `academic-writing`
  - `codex`
  - `literature-review`
- Marked the repository as a GitHub template repository.
- Reworked `README.md` into a beginner-friendly starter guide.
- Added clearer software and plugin requirements.
- Added a reusable Distinction/high-band delivery review gate.
- Added generic rubric and module-requirements templates.
- Reworked the privacy check script so it supports project-specific `.privacy-patterns`.
- Removed private, institution-specific, supervisor-specific, path-specific, and live-dissertation identifiers from the shareable template layer.

### Added

- `university-guidance/DISTINCTION_DELIVERY_REVIEW_GATE.md`
- `university-guidance/RUBRIC_EVIDENCE_GATE.md`
- `university-guidance/MODULE_REQUIREMENTS_TEMPLATE.md`
- `university-guidance/RUBRIC_OR_MARKING_CRITERIA_TEMPLATE.md`
- `docs/PUBLIC_RELEASE_RENAMING_GUIDE.md`
- `.privacy-patterns.example`

### Verified

- Local privacy check passed: `./scripts/privacy_check.sh`.
- Manual private-pattern scan passed for the original private dissertation identifiers.
- Git diff check passed.
- Remote GitHub repository was confirmed after rename.

### Still To Do Before Full Public Release

- Choose and add a licence.
- Complete `PUBLIC_RELEASE_AUDIT.md`.
- Run GitHub Actions privacy check after every public-release update.
- Review topic-specific example skills and decide whether to keep, generalise, or move them into examples.
- Confirm contribution policy.

## v0.1.0-private-sharing-template - 2026-05-21

Status: private sharing ready.

### Added

- Initial shareable dissertation-agent template.
- Project skills under `.agents/skills/`.
- Source-first, document-quality, style, and context-continuity rules.
- Privacy checklist and basic privacy check script.
- Beginner setup notes for friends using Codex.

### Boundary

- Designed for private repository sharing only.
- Not ready for public release at this stage.
