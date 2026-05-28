# Skill Eval Registry

Purpose: provide lightweight checks for high-risk routing behaviours.

## Eval Cases

| Case ID | Prompt | Expected Skills | Must Not Do | Pass Criteria |
|---|---|---|---|---|
| PROFILE-001 | "Adapt this starter kit to a journal article project" | `research-project-adapter`, `PROJECT_TYPE_PROFILES.md`, `RESEARCH_PROJECT_BRIEF_TEMPLATE.md` | assume dissertation defaults without profile check | Project profile is selected and dissertation-only files are marked optional when irrelevant |
| RUNTIME-001 | "Start a formal proposal, manuscript, report, or grant task" | `agent-orchestration`, `scripts/agent_runtime.py`, `research-project-adapter`, `dissertation-source-first-gate`, `cognitive-frameworks`, `academic-self-review-loop`, `dissertation-document-quality-gate` | proceed without runtime receipt, cognitive protocol, self-review, or checkpoint gates | Runtime preflight receipt exists and required gates are listed |
| DB-001 | "Search subscription academic databases" | `dissertation-research-search-protocol`, `scripts/academic_database_connector.py` | claim subscription access without credentials | Connector status report states configured/not configured and metadata-only boundary |
| CLAIM-001 | "Check whether citations support claims" | `dissertation-citation-audit`, `scripts/citation_claim_audit.py` | treat citation consistency as support proof | Claim rows, source-readiness status and manual verification boundary are recorded |
| COG-001 | "Plan the rationale for a formal research proposal" | `cognitive-frameworks`, `research-wiki/WRITING_QUALITY_RUBRIC.md` | write a vague gap without type, warrant, or boundary | Cognitive protocol names section type, gap/problem type, claim, evidence, warrant, and boundary |
| COG-002 | "Check a cognitive protocol before drafting" | `scripts/cognitive_protocol_check.py`, `cognitive-frameworks` | pass weak warrants or missing section type silently | Strict checker flags missing allowed gap/problem type or weak warrant |
| SELF-001 | "Improve a formal paragraph before delivery" | `academic-self-review-loop`, `research-wiki/WRITING_QUALITY_RUBRIC.md` | only polish wording or give generic praise | Two-pass review records concrete weaknesses, revision actions, and second-pass judgement |
| QUAL-001 | "Assess paragraph quality without using a grade rubric" | `research-wiki/WRITING_QUALITY_RUBRIC.md`, `academic-self-review-loop` | confuse intrinsic writing quality with school, journal, funder, or client acceptance | Review uses one point per paragraph, mini-claim, progression, evidence integration, reader journey, and redundancy control |
| PIPE-001 | "Prepare a formal Word or stakeholder-facing delivery" | `research-wiki/DOCUMENT_PIPELINE.md`, `academic-self-review-loop`, `dissertation-document-quality-gate` | load every delivery rule at once or skip checkpoint records | Thinking, writing, and delivery checkpoints are recorded or marked not applicable |

## Runner

```bash
python3 scripts/run_skill_evals.py
```
