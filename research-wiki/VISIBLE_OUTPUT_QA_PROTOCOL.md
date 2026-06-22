# Visible Output QA Protocol

Adopted: 2026-06-22

## Purpose

Visible Output QA prevents a source-layer success from being mistaken for a user-visible success.

The goal is to stop an agent from claiming a visible output is complete when a reader would see broken layout, missing tables, clipped text, unreadable figures, stale README links, or a mismatch against a previous accepted version.

## When To Use

Use Visible Output QA for:

- formal, stakeholder-facing, reviewer-facing, client-facing, supervisor-facing, submission-facing, Word/PDF, proposal, manuscript, report, grant, compliance, or participant-facing outputs;
- important figures, diagrams, tables, visual summaries, or rendered pages;
- layout repair, Markdown-to-DOCX conversion, PDF export, or previous-version comparison;
- public GitHub pages, Obsidian graph/vault surfaces, browser pages, or other visible surfaces where the fix is visible only after rendering or opening.

Do not require it for:

- pure Markdown notes with no visible delivery claim;
- bounded source lookup;
- source register/readiness edits with no Word/PDF/figure/browser surface;
- chat-only advice.

## Required Loop

1. Define the visible output job.
2. Produce or locate the visible artifact.
3. Run deterministic checks relevant to the surface.
4. Inspect the rendered output or preview.
5. Compare against a previous accepted baseline when one exists.
6. Fix and re-render until pass, or record an explicit accepted risk.

## Ordering And Precedence

Use this as a visible-surface layer after the artifact exists. It does not replace upstream content gates.

| Step | Relationship |
|---|---|
| Source-first, citation, compliance, privacy, requirement, and academic-integrity gates | Must remain authoritative for content/evidence. Visible Output QA cannot clear them. |
| Document-quality gate | Owns the visible-output QA record for document/figure/browser-visible deliveries. |
| Structural parity / layout / delivery guard scripts | Feed deterministic evidence into Visible Output QA for Word/PDF outputs. |
| Visual inspection | Confirms the user-visible surface was opened or rendered and checked against the communication job. |
| External reviewer layout advice | Optional only for a specific unresolved visual delta after local checks; advisory, not a replacement for local verdicts. |

Conflict rule: if Visible Output QA passes but citation support, compliance, privacy, academic integrity, structural parity, layout review, or delivery guard fails, the overall output remains blocked or draft-only. A visible pass means the surface was checked, not that the content is academically, professionally, legally, or administratively ready.

## Surface-Specific Checks

Word/PDF:

- `scripts/markdown_docx_structure_check.py` for Markdown-to-DOCX table/list structure.
- `scripts/docx_layout_review_check.py` for heading hierarchy, table/list counts, and previous accepted baseline comparison.
- `scripts/formal_delivery_guard.py` for formal delivery aggregation.
- PDF/rendered page inspection when available.

Figures/diagrams:

- state the figure job and evidence boundary;
- render to an inspectable image or PDF;
- check labels, clipping, legend overlap, colour/greyscale distinguishability, and panel alignment.

Browser/GitHub/Obsidian:

- verify the user-visible page or vault surface directly where possible;
- do not treat local file existence, commit, tag, or script output as visible-surface proof.

## Visible Output QA Template

```text
Visible Output QA:
- Artifact:
- Communication job:
- Rendered output / preview:
- Deterministic checks:
- Visual inspection:
- Baseline / regression check:
- Unresolved risks:
- Delivery verdict:
```

Accepted verdicts:

- `passed`
- `delta-accepted`
- `risk-accepted-by-user`
- `draft-not-rendered`
- `blocked`
- `not-applicable - reason`

## Boundary

Visible Output QA proves only that a visible surface was checked against named criteria. It does not prove citation support, compliance readiness, rubric/journal/client requirement compliance, academic/professional quality, or submission readiness.

An unresolved visual risk cannot be described as a pass. It must be fixed, explicitly accepted by the user, or labelled as blocked/draft.

## Scope And Rollback Path

For this starter kit, the highest-priority surfaces are formal Word/PDF outputs, important figures/diagrams, and public GitHub documentation. Browser and Obsidian surfaces use this protocol when the user-visible surface is the actual deliverable or failure point.

If Visible Output QA causes over-routing on a bounded task, do not delete the protocol. First rerun runtime preflight and record one of:

- `not applicable - no visible delivery surface`;
- `not applicable - Markdown/source note only`;
- `rerouted - task drifted into Word/PDF/figure/browser-visible delivery`.

If repeated false positives occur, update `scripts/agent_runtime.py` and add or amend a `RUNTIME-*` eval before relaxing the rule.
