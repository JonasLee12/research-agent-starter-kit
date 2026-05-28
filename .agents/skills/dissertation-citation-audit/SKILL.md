---
name: dissertation-citation-audit
description: Audit dissertation citations, bibliography entries, source metadata, quote accuracy, and whether cited sources actually support the attached claims.
---

# Dissertation Citation Audit

Use when checking references, citations, literature review drafts, theoretical claims, methodology citations, or final dissertation readiness.

## Workflow

1. Identify the files to audit.
2. Extract claims with citations.
3. Check whether each citation supports the exact claim.
4. Flag missing page numbers for direct quotes if required by the style guide.
5. Flag unverifiable or suspicious references.
6. Check consistency between in-text citations and bibliography.

## Status Labels

- `VERIFIED`: citation exists and supports the claim.
- `WEAK SUPPORT`: source is relevant but does not fully support the claim.
- `MISMATCH`: source does not support the claim.
- `MISSING`: citation key or bibliography entry missing.
- `NEEDS VERIFICATION`: source details are incomplete or not locally verifiable.

## Output

Create or update `audit-reports/CITATION_AUDIT.md`.

## Guardrails

Read `../dissertation-shared/references/citation-discipline.md`.
Do not invent source metadata. If internet access is needed for verification, say so clearly.
