# Changelog

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
