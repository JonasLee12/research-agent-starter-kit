# Distinction Delivery Review Gate

Last updated: 2026-05-24

Purpose: before any formal dissertation document is delivered, require a rubric-aligned self-review, concrete revision pass, and final readiness statement against the target quality band.

## Trigger

Use this gate before delivering:

- proposal drafts;
- dissertation chapter drafts;
- methodology, literature review, findings, or discussion sections;
- ethics documents when they affect assessed proposal or dissertation quality;
- participant-facing materials included as appendices or supervisor-facing evidence;
- interview guides, concept cards, or appendices prepared for supervisor or submission use;
- supervisor-facing Word/PDF documents;
- any document the user may revise, share, or submit.

This gate is mandatory when the user asks for Distinction, 75+, high distinction, rubric-aligned improvement, marking criteria, or assessed quality.

## Evidence Boundary

This is an internal readiness review. It is not an official mark.

Before giving any grade-band claim, apply:

- `university-guidance/RUBRIC_EVIDENCE_GATE.md`
- the project-specific rubric or marking-criteria file
- the project-specific module-requirements file
- the project-specific format file

Evidence labels:

- `OFFICIAL ORIGINAL TEXT`
- `LOCAL SUMMARY`
- `INFERENCE FROM LOCAL SUMMARY`
- `EVIDENCE INSUFFICIENT`

If only local summaries are available, do not claim exact official wording for any numeric grade. Use an indicative readiness band.

## Readiness Bands

Use these labels unless official rubric wording supports a more precise judgement:

- `Below target`
- `Borderline target readiness`
- `Target-ready working draft`
- `High-band potential`
- `Evidence insufficient for band judgement`

Do not call a document `submission-ready` if any required source, appendix, consent/ethics detail, word-count rule, format rule, or citation check remains unresolved.

## Required Review Loop

1. Identify the document type, audience, assessment target, and current status.
2. Apply the rubric evidence gate and state the evidence level.
3. Check relevant project sources:
   - `research-wiki/TASK_STATE.md`
   - `knowledge-base/SOURCE_READINESS_MATRIX.md` for citation-heavy work
   - `ethics/ETHICS_READINESS_TRACKER.md` for ethics-facing work
   - relevant proposal/chapter/source-map files
4. Review the document against the quality matrix below.
5. Create a short pre-revision finding list:
   - high-impact weaknesses;
   - concrete fixes;
   - items that cannot be fixed without user/supervisor confirmation.
6. Revise the document before delivery when the fix is within scope.
7. Re-check the revised version.
8. Save a review note beside the output when the task is substantial:
   - suggested filename pattern: `*_DELIVERY_REVIEW_GATE_YYYY-MM-DD.md`
9. Register the gate in `research-wiki/TASK_STATE.md` or `research-wiki/PRODUCTION_RUN_REGISTER.md` if that register is enabled.

## Quality Matrix

| Area | Target Question | Evidence Needed | Failure Label |
|---|---|---|---|
| Golden thread | Does the document keep a clear line from problem, gap, research questions, method, ethics, and contribution? | Proposal/chapter text and project overview | `golden-thread gap` |
| Literature grounding | Does the text use relevant, citation-ready literature rather than broad claims? | Source readiness matrix, source notes, citation audit | `source-readiness gap` |
| Critical engagement | Does the text evaluate tensions, limits, and implications rather than only describe topics? | Draft text and source support | `descriptive-writing risk` |
| Methodology fit | Does the method match the research questions, sample, ethics, and project stage? | Proposal/method text, ethics tracker | `method-fit gap` |
| Ethics and governance | Are consent, privacy, power, data handling, and participant burden treated critically? | Ethics tracker, ethics drafts, participant materials | `ethics-depth gap` |
| Original contribution | Is the contribution credible for the dissertation level and not overclaimed? | Research questions, output claims, boundaries | `overclaim risk` |
| Structure and signposting | Can a marker quickly see section jobs and progression? | Headings, transitions, word allocation | `structure gap` |
| Academic style | Is the prose concise, cautious, and free from generic AI-style phrasing? | File-level style scan | `style gate gap` |
| Referencing | Are claims supported by real sources with consistent citation practice? | Citation audit, source register, references | `citation gap` |
| Format compliance | Does the document follow module format, word count, appendix, and declaration rules? | University guidance files, document pipeline | `format gap` |

## Final Chat Delivery

Use this compact report:

```text
Delivery review:
- Evidence level:
- Readiness after revision:
- Main fixes made:
- Remaining risks:
```

## Maintenance Audit

Maintenance should flag these as bugs:

- `delivery review gap`: a formal document was delivered without this gate.
- `self-revision gap`: weaknesses were reviewed but feasible issues were not revised before delivery.
- `readiness overclaim`: the agent claimed a grade or submission readiness without sufficient evidence.
- `rubric evidence gap`: the review omitted the evidence level from `RUBRIC_EVIDENCE_GATE.md`.
- `file-inspection gap`: the agent reviewed only the chat answer, not the document source or rendered output.
