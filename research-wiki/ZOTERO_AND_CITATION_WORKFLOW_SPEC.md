# Zotero And Citation Workflow Spec

Purpose: define safe citation and reference-management support.

## Current Default

No Zotero account or library is connected by default.

The template supports:

- source registers;
- metadata imports;
- citation consistency checks;
- claim-support audit queues.

## Local Tools

- `scripts/citation_style_check.py`
- `scripts/citation_claim_audit.py`

## Rule

A reference can be formatted correctly and still fail to support the claim. Use claim-support audit before treating citation-heavy prose as ready.
