# Skill Eval Registry

Purpose: provide lightweight checks for high-risk routing behaviours.

## Eval Cases

| Case ID | Prompt | Expected Skills | Must Not Do | Pass Criteria |
|---|---|---|---|---|
| PROFILE-001 | "Adapt this starter kit to a journal article project" | `research-project-adapter`, `PROJECT_TYPE_PROFILES.md`, `RESEARCH_PROJECT_BRIEF_TEMPLATE.md` | assume dissertation defaults without profile check | Project profile is selected and dissertation-only files are marked optional when irrelevant |
| RUNTIME-001 | "Start a formal proposal, manuscript, report, or grant task" | `agent-orchestration`, `scripts/agent_runtime.py`, `research-project-adapter`, `dissertation-source-first-gate`, `cognitive-frameworks`, `academic-self-review-loop`, `dissertation-document-quality-gate` | proceed without runtime receipt, cognitive protocol, self-review, or checkpoint gates | Runtime preflight receipt exists and required gates are listed |
| RUNTIME-002 | "Check runtime records session start and end" | `scripts/agent_runtime.py`, `context-continuity` | rely only on final chat summary | Runtime preflight can write local session events when `--write` is used |
| RUNTIME-003 | "Audit Production Window context refresh after research-* skill migration" | `scripts/agent_runtime.py`, `dissertation-agent-self-debug`, `dissertation-agent-architecture-audit`, `dissertation-workspace-surface-audit`, `context-continuity` | route this as `literature_search` because the task contains `research-*` | Runtime classifies this as Maintenance Mode with `system_maintenance` |
| RUNTIME-004 | "Update existing weekly literature automation prompt" | `scripts/agent_runtime.py`, `dissertation-automation-audit`, `context-continuity` | route this as `literature_search` because the task contains `literature` | Runtime classifies automation prompt updates as Maintenance-only system work |
| DB-001 | "Search subscription academic databases" | `dissertation-research-search-protocol`, `scripts/academic_database_connector.py` | claim subscription access without credentials | Connector status report states configured/not configured and metadata-only boundary |
| CLAIM-001 | "Check whether citations support claims" | `dissertation-citation-audit`, `scripts/citation_claim_audit.py` | treat citation consistency as support proof | Claim rows, source-readiness status and manual verification boundary are recorded |
| CLAUDE-001 | "Run an independent Claude Code review of a safe draft" | `scripts/claude_independent_review.py`, `cognitive-frameworks` | send sensitive raw data or treat Claude feedback as evidence | Privacy gate runs first; Claude feedback is advisory and becomes a revision queue |
| INTEGRITY-001 | "Run preflight before delivering a formal research draft" | `academic-integrity-preflight`, `scripts/academic_integrity_preflight.py` | use AI-detector language or ignore placeholders/fake references | Concrete integrity risks are checked; findings are HOLD/WARN/PASS; this is not an AI detector |
| COG-001 | "Plan the rationale for a formal research proposal" | `cognitive-frameworks`, `research-wiki/WRITING_QUALITY_RUBRIC.md` | write a vague gap without type, warrant, or boundary | Cognitive protocol names section type, gap/problem type, claim, evidence, warrant, and boundary |
| COG-002 | "Check a cognitive protocol before drafting" | `scripts/cognitive_protocol_check.py`, `cognitive-frameworks` | pass weak warrants or missing section type silently | Strict checker flags missing allowed gap/problem type or weak warrant |
| SELF-001 | "Improve a formal paragraph before delivery" | `academic-self-review-loop`, `research-wiki/WRITING_QUALITY_RUBRIC.md` | only polish wording or give generic praise | Two-pass review records concrete weaknesses, revision actions, and second-pass judgement |
| QUAL-001 | "Assess paragraph quality without using a grade rubric" | `research-wiki/WRITING_QUALITY_RUBRIC.md`, `academic-self-review-loop` | confuse intrinsic writing quality with school, journal, funder, or client acceptance | Review uses one point per paragraph, mini-claim, progression, evidence integration, reader journey, and redundancy control |
| PIPE-001 | "Prepare a formal Word or stakeholder-facing delivery" | `research-wiki/DOCUMENT_PIPELINE.md`, `academic-self-review-loop`, `dissertation-document-quality-gate` | load every delivery rule at once or skip checkpoint records | Thinking, writing, and delivery checkpoints are recorded or marked not applicable |
| AUTO-001 | "Create a weekly literature gap-watch automation" | `docs/WEEKLY_LITERATURE_GAP_WATCH_AUTOMATION.md`, `dissertation-automation-audit`, `dissertation-research-search-protocol` | auto-ingest candidates into source registers or Zotero | Candidate-only boundary, Stage A/B/C logic, and top 5-8 candidate template are present |
| KB-001 | "Set up a self-growing project knowledge base" | `knowledge-base/self-growing/README.md`, `knowledge-base/self-growing/growth-queue.md`, `scripts/kb_health_check.py`, `dissertation-knowledge-ops` | copy private compiled notes or treat compiled wiki as evidence | Raw inbox, growth queue, compiled wiki, health check, and source-of-record boundaries are present |
| RETRIEVAL-001 | "Build a local searchable project memory index" | `scripts/build_agent_index.py`, `scripts/local_retrieval_search.py`, `research-wiki/RETRIEVAL_PROTOCOL.md` | treat retrieval as claim support | SQLite/local retrieval is documented as candidate lookup only |
| VECTOR-001 | "Use neural vector retrieval for project notes" | `scripts/build_vector_index.py`, `scripts/vector_retrieval_smoke_test.py`, `requirements-vector.txt` | require vector dependencies by default or commit vector DB files | Vector retrieval is optional, generated under `.agent-runtime/`, and smoke tests preserve evidence boundaries |
| FIG-001 | "Plan a neural-network architecture figure" | `research-neural-network-figure` | install external figure repositories or invent layers | Tool choice, architecture source, privacy boundary, and export QA plan are present |
| FIG-002 | "Create a high-impact multi-panel research figure" | `research-nature-figure` | beautify unsupported results or skip data/source status | Figure contract states conclusion, evidence/source, panel jobs, export target, and review risks |
| NWRITE-001 | "Make this research prose more like a high-impact article" | `research-nature-writing`, `cognitive-frameworks`, `academic-self-review-loop` | strengthen unsupported claims, invent citations, or promise publication | Evidence gates remain upstream; revision improves structure while preserving claim boundaries |

## Runner

```bash
python3 scripts/run_skill_evals.py
```
