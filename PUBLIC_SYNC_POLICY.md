# Public Sync Policy

This policy keeps a private research-agent workspace and the public starter kit aligned without leaking private project content.

## Purpose

The public starter kit is a generic template. A private project workspace may contain institution-specific rules, supervisor or client feedback, ethics records, participant data, local automation receipts, personal names, email addresses, and project-specific source notes.

Do not sync files from a private workspace to this repository unless they pass the checks below.

## Shared Core Files

These files may be kept broadly aligned between a private workspace and the public starter kit, after privacy review and generalisation:

- `.agents/skills/agent-orchestration/SKILL.md`
- `.agents/skills/dissertation-agent-self-debug/SKILL.md`
- `.agents/skills/project-skill-creator-governance/SKILL.md`
- `.agents/skills/release-surface-verification/SKILL.md`
- `.agents/skills/material-passport/SKILL.md`
- `.agents/skills/formal-delivery-guard/SKILL.md`
- `scripts/agent_runtime.py`
- `scripts/claude_independent_review.py`
- `scripts/academic_integrity_preflight.py`
- `scripts/material_passport.py`
- `scripts/pre_delivery_lock.py`
- `scripts/formal_delivery_guard.py`
- `scripts/citation_claim_audit.py`
- `scripts/build_vector_index.py`
- `scripts/vector_retrieval_smoke_test.py`
- `scripts/run_skill_evals.py`
- `scripts/run_behavioral_evidence_checks.py`
- `research-wiki/SKILL_EVAL_REGISTRY.md`
- `research-wiki/RETRIEVAL_PROTOCOL.md`
- `research-wiki/DOCUMENT_PIPELINE.md`

Shared does not mean byte-identical. Public versions must stay generic; private versions may include local gates, local paths, and project-specific rules.

## Private-Only Content

Never sync these from a private workspace into the public starter kit:

- supervisor, PI, client, funder, participant, or reviewer feedback that is not public;
- signed consent forms, raw transcripts, recordings, interview notes, screenshots, or identifiable participant data;
- LMS, Canvas, VLE, intranet, subscription database, journal portal, or client-portal content;
- personal names, private email addresses, institution-specific identifiers, module links, local usernames, API keys, tokens, cookies, or browser profiles;
- generated runtime receipts, automation feedback queues, local audit logs, vector databases, Zotero library IDs, Obsidian workspace state, or raw/private knowledge-base notes;
- assessment rubrics, marking criteria, ethics forms, or institutional guidance unless they are public and clearly allowed to be redistributed.

## Public-Only Content

These files are designed for onboarding public users and may not belong in a private project workspace:

- `docs/`
- `templates/obsidian-vault/`
- `compliance/PROJECT_COMPLIANCE_TRACKER.md`
- `quality-gates/PROJECT_DELIVERY_REVIEW_GATE.md`
- `PROJECT_TYPE_PROFILES.md`
- `RESEARCH_PROJECT_BRIEF_TEMPLATE.md`
- generic README, release, and contribution documentation

Private projects may copy these only when useful, then customise them locally.

## Sync Workflow

Before copying any improvement from a private workspace into the public starter kit:

1. Identify whether the change is a reusable behaviour, generic template, helper script, or private project rule.
2. Strip or replace all private names, emails, institution identifiers, local paths, URLs, screenshots, source notes, and project-specific claims.
3. Run:

```bash
bash scripts/privacy_check.sh
python3 scripts/run_skill_evals.py
python3 scripts/validate_agent_schemas.py
python3 -m unittest discover -s tests -v
git diff --check
```

4. If the change affects public release, README, tag, About, topics, rendered docs, or setup instructions, use `release-surface-verification` before claiming it is complete.
5. Record the sync in `CHANGELOG.md`.

## Release Boundary

A pushed commit is not the same as a public release.

Before saying a release is complete, verify:

- the intended tag exists and points to the intended commit;
- the GitHub Release page exists and is marked as the latest release when appropriate;
- the release tarball/tag contains the expected files;
- the repository About/sidebar, topics, rendered README, Chinese README, and important links show the expected public state.

If only `main` has the update, describe it as a main-branch update, not a released version.
