# Claim Ledger Lite Protocol

Adopted: 2026-06-22

## Purpose

Claim Ledger Lite is a lightweight control for formal research claims. It keeps a draft from becoming stronger than its evidence without forcing every small lookup or formatting edit into a heavy evidence ledger.

Use it as a claim-strength boundary: what can the project safely say, what can it not yet prove, and what wording is allowed until source-section review or project confirmation exists.

## When To Use

Use Claim Ledger Lite when any of these apply:

- formal proposal, thesis/dissertation, manuscript, report, grant, protocol, recommendation, or stakeholder-facing prose introduces or revises core claims;
- a citation claim-support audit covers a section, chapter, formal paragraph set, or stakeholder-facing argument;
- source-readiness, claim-support, or citation-boundary status is upgraded or downgraded;
- a high-risk concept is used as a warrant, such as implementation, effectiveness, impact, adoption condition, responsible AI, safety, trust, autonomy, workload, user agency, professional identity, or causal/significant effect.

Do not require it for:

- bounded single-source lookup;
- metadata-only source discovery;
- citation-key or reference-format repair;
- typo, layout, or formatting-only work;
- source reading that does not change a formal claim, source-readiness status, or stakeholder-facing judgement.

If a bounded task drifts into formal claim support, reroute before continuing.

## Ownership

- `dissertation-citation-audit` owns claim-support status and the ledger check.
- `cognitive-frameworks` prepares candidate claims, warrants, limitations, and concept contracts before drafting.
- `dissertation-argument-spine` consumes the ledger to keep the argument thread within the allowed evidence boundary.
- The ledger is an audit artifact. It is not a source register, not a source note, and not proof that a source is citation-ready.

## Ordering And Precedence

Use this as an additive boundary layer:

| Step | Relationship |
|---|---|
| Source-first / Material Passport | Must happen before formal drafting; Claim Ledger Lite does not replace source mapping. |
| `cognitive-frameworks` | Prepares candidate claims, warrants, limitations, and concept contracts before or while the ledger is drafted. |
| `dissertation-citation-audit` | Owns the ledger check and remains the authority for citation claim-support verification. |
| `dissertation-argument-spine` | Uses `allowed_wording` to keep the argument thread within the evidence boundary. |
| Integrity / compliance / rubric / journal / client gates | Always override a ledger pass. If these gates block, the composite result is blocked. |
| Formal delivery / document quality | Can consume ledger status but cannot treat it as document-quality or source-readiness proof. |

Conflict rule: if Claim Ledger Lite passes but citation claim-support, source-first, compliance, academic-integrity, requirement, or document-quality gates fail, the overall output is not deliverable. The ledger only constrains claim strength; it never clears another gate.

## Where To Store

For formal files, store the ledger near the artifact, for example:

- `outputs/<task>/<ARTIFACT>_CLAIM_LEDGER_LITE_YYYY-MM-DD.md`
- `audit-reports/<task>/Claim_Ledger_Lite_<artifact>_YYYY-MM-DD.md`

For a small stakeholder-facing memo, the ledger may live inside the thinking or delivery checkpoint.

## Template

```markdown
# Claim Ledger Lite

| claim_id | claim | output_location | source_anchor | evidence_status | cannot_prove | concept_contract | allowed_wording | review_action |
|---|---|---|---|---|---|---|---|---|
| CLM-001 | ... | Section 2.1 paragraph 3 | `knowledge-base/sources/...md` | PARTIAL SUPPORT | Does not prove ... | adoption condition: define scope and failure condition | "may suggest..." | qualify before drafting |
```

## Field Rules

- `claim_id`: stable local ID, `CLM-001`, `CLM-002`, etc.
- `claim`: the actual claim or the smallest faithful paraphrase.
- `output_location`: section/paragraph, report location, or stakeholder memo location.
- `source_anchor`: concrete local source note, source register row, audit report, or explicit `source needed`.
- `evidence_status`: one of `DIRECT SUPPORT`, `PARTIAL SUPPORT`, `BACKGROUND ONLY`, `METADATA ONLY`, `INSUFFICIENT`, `SOURCE NEEDED`, or `TO CONFIRM`.
- `cannot_prove`: what the source or evidence cannot support.
- `concept_contract`: definition, limit, failure condition, or `none - low-risk descriptive claim`.
- `allowed_wording`: wording strength allowed in prose.
- `review_action`: keep, qualify, source-section verify, delete, ask stakeholder/supervisor/client, or mark `TO CONFIRM`.

## Boundary

Claim Ledger Lite controls claim strength. It does not prove source access, citation readiness, compliance readiness, rubric/journal/client requirement compliance, or document quality.

Do not use it to make metadata-only sources citation-ready. Do not cite a ledger as evidence in formal prose.

## Rollback / Override Path

If Claim Ledger Lite causes over-routing on a bounded task, do not delete the protocol. First rerun runtime preflight and record one of:

- `not applicable - bounded lookup only, no formal claim or source-readiness change`;
- `not applicable - citation-key/reference-format repair only`;
- `rerouted - task drifted into formal claim support`.

If repeated false positives occur, update `scripts/agent_runtime.py` and add or amend a `RUNTIME-*` eval before relaxing the rule.
