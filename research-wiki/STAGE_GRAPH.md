# Research Stage Graph

Last updated: 2026-06-10

## Purpose

This file is a pointer map for long-running research projects. It tells the agent which earlier source-of-record files should be checked before later-stage tasks change related material.

The graph is not the evidence itself. It points to project files that carry the evidence.

## Customisation Rule

The rows below are optional starter examples. Replace them with your project's actual source-of-record files. A one-row graph is valid if your project has only one active dependency.

Keep paths relative to the repository root when possible.

## Authority Order

1. Latest explicit user instruction, except when it omits or conflicts with a known source-of-record dependency. In that case, surface the dependency first.
2. Current source-of-record files listed below.
3. Stage Continuity Capsule or design checkpoint created from those files.
4. Navigation notes and retrieval results.

If a listed file is missing, stale, or conflicts with the task, pause and surface the issue.

## Stage Nodes

| Stage ID | Stage | Source-of-record pointers | Must inherit for downstream work |
|---|---|---|---|
| `project-frame` | Project frame and profile | `RESEARCH_PROJECT_BRIEF_TEMPLATE.md`; `PROJECT_TYPE_PROFILES.md`; `PROJECT_AGENT_PREFERENCES.md` | project type, audience, owner-confirmed facts, source-first boundaries |
| `proposal-or-brief` | Proposal, brief, manuscript plan, or project outline | `RESEARCH_PROJECT_BRIEF_TEMPLATE.md`; `DISSERTATION_BRIEF_TEMPLATE.md`; `research-wiki/TASK_STATE.md` | research aim, scope, current questions, output status, open confirmations |
| `source-readiness` | Source and citation readiness | `knowledge-base/SOURCE_REGISTER.md`; `knowledge-base/SOURCE_READINESS_MATRIX.md` | metadata-only boundaries, reviewed-source status, claim-support limits |
| `compliance-or-ethics` | Ethics, privacy, compliance, or requirement boundary | `compliance/PROJECT_COMPLIANCE_TRACKER.md`; `PRIVACY_CHECKLIST.md`; `quality-gates/PROJECT_DELIVERY_REVIEW_GATE.md` | approval status, privacy limits, requirement-source status, unresolved checks |
| `method-or-analysis-plan` | Methods, analysis plan, instrument design, or design lock | `research-wiki/TASK_STATE.md`; `research-wiki/WRITING_QUALITY_RUBRIC.md`; `research-wiki/DOCUMENT_PIPELINE.md` | method route, analysis boundary, instrument status, document-stage boundary |
| `production-receipts` | Recent production evidence | `research-wiki/TASK_STATE.md`; `research-wiki/PRODUCTION_RUN_REGISTER.md`; `research-wiki/SESSION_EVENT_LOG.jsonl` | what was actually produced, gates run, audited risks, open next steps |

## Directed Dependencies

| Downstream task family | Must check first |
|---|---|
| Methodology, method route, analysis plan, or formal methods prose | `project-frame`, `proposal-or-brief`, `source-readiness`, `method-or-analysis-plan`, `production-receipts` |
| Interview guide, fieldwork instrument, survey, concept card, or scenario stimulus | `proposal-or-brief`, `compliance-or-ethics`, `method-or-analysis-plan`, `production-receipts` |
| Ethics, privacy, compliance, consent, recruitment, or stakeholder-facing requirement text | `project-frame`, `proposal-or-brief`, `compliance-or-ethics`, `production-receipts` |
| Literature review to method/discussion integration | `source-readiness`, `proposal-or-brief`, `method-or-analysis-plan`, `production-receipts` |
| Formal Word/PDF delivery | current source file, `research-wiki/DOCUMENT_PIPELINE.md`, prior accepted output when available, `production-receipts` |

## Deliverable Class Dependencies

Use this table for the Stage Continuity trigger.

| Deliverable class | Upstream nodes |
|---|---|
| `proposal-or-brief` | `project-frame`, `source-readiness`, `production-receipts` |
| `methodology-or-method-plan` | `project-frame`, `proposal-or-brief`, `source-readiness`, `method-or-analysis-plan`, `production-receipts` |
| `ethics-or-compliance-material` | `project-frame`, `proposal-or-brief`, `compliance-or-ethics`, `production-receipts` |
| `interview-guide-or-fieldwork-instrument` | `proposal-or-brief`, `compliance-or-ethics`, `method-or-analysis-plan`, `production-receipts` |
| `concept-card-or-scenario-stimulus` | `proposal-or-brief`, `compliance-or-ethics`, `method-or-analysis-plan`, `production-receipts` |
| `research-question-to-method-mapping` | `project-frame`, `proposal-or-brief`, `method-or-analysis-plan`, `production-receipts` |
| `analysis-plan` | `proposal-or-brief`, `source-readiness`, `method-or-analysis-plan`, `compliance-or-ethics` |
| `stakeholder-facing-decision-memo` | `project-frame`, `proposal-or-brief`, `method-or-analysis-plan`, `production-receipts` |
| `chapter-or-section-formal-draft` | `project-frame`, `proposal-or-brief`, `source-readiness`, `method-or-analysis-plan`, `production-receipts` |

## Confirmation Boundary

Older files may be superseded by later files, but the agent must not declare them irrelevant by itself. If a downstream task appears to conflict with an older proposal, brief, protocol, or compliance file, record it as `needs confirmation` unless a later source-of-record explicitly resolves the conflict.
