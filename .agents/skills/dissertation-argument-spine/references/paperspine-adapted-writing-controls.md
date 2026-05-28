# PaperSpine-Adapted Dissertation Writing Controls

Use this reference when a dissertation proposal, chapter, supervisor brief, or major revision needs stronger writing logic than ordinary outlining.

Source basis:

- Repository: `https://github.com/WUBING2023/PaperSpine`
- Commit reviewed: `e215cecb2a925a66337f2de77a4f0f8967c01423`
- Source files reviewed:
  - `dist/codex/paper-spine/references/writing-rationale-matrix.md`
  - `dist/codex/paper-spine/references/motivation-thread-writing.md`
  - `dist/codex/paper-spine/references/rewrite-matrix.md`
  - `dist/codex/paper-spine/references/logic-transfer-audit.md`
  - `dist/codex/paper-spine/scripts/artifact_check.py`
- Licence checked: MIT.
- Attribution: PaperSpine contributors, MIT License. This local file paraphrases and adapts workflow ideas for dissertation use; it does not copy or activate PaperSpine executable code.

These controls adapt PaperSpine ideas for the project owner's dissertation. They do not activate PaperSpine scripts, LaTeX tooling, journal-submission workflow, or external style imitation.

## 1. Dissertation Section Rationale Matrix

Use before drafting or deeply revising a proposal/chapter section.

Purpose: make every important section, subsection, paragraph group, figure, table, or supervisor-facing decision explain its job before prose is polished.

| Row ID | Dissertation Unit | Current Problem Or Planned Function | Motivation Link | Literature / Method Pattern Learned | Module / Rubric / Genre Requirement | Source Or Evidence Anchor | Planned Text Move | Final Text Check |
|---|---|---|---|---|---|---|---|---|
| F1 | Whole document or chapter framework |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |

Quality bar:

- The first row must justify the whole document or chapter structure.
- Use one row per meaningful writing decision, not one row per heading by default.
- Include headings, tables, figures, concept-card descriptions, or supervisor questions when they carry argument logic.
- Avoid generic reasons such as `improve clarity`, `make academic`, `polish wording`, or `add detail`.
- Each row should connect the section job to the dissertation motivation, evidence boundary, and next writing move.

For the current dissertation, a strong row should usually answer:

- How does this unit connect active learning implementation, AI-agent support, teacher perceptions, and adoption conditions?
- Does the chosen conceptual lens help here, or is responsible AI / teacher autonomy literature needed?
- What source, LMS rule, ethics constraint, supervisor note, or literature note anchors the claim?
- What should the final text prove, limit, or ask the supervisor to decide?

## 2. Motivation Thread Model

Use when the project feels scattered or when a proposal/chapter needs a clearer controlling line.

Dissertation arc:

```text
field problem -> specific gap -> conceptual lens -> method response -> evidence route -> expected contribution -> boundary
```

Current project version:

```text
Active learning implementation is difficult in higher education.
AI agents may support planning, adaptation, or reflection.
The missing issue is teacher-informed acceptability, trust, autonomy, workload, and adoption conditions.
the chosen conceptual lens helps organise adoption conditions, but responsible AI and teacher autonomy literature are needed for the AI-specific risks.
Interviews, supported by an AI-agent concept card where appropriate, can generate teacher-informed adoption conditions and design boundaries without claiming to evaluate a full prototype.
```

Use this table when writing or reviewing a proposal/chapter:

| Arc Element | Working Content | Source Anchor | Required Section | Boundary |
|---|---|---|---|---|
| Field problem |  |  | Introduction / Literature Review |  |
| Specific gap |  |  | Introduction / Literature Review |  |
| Conceptual lens |  |  | Literature Review / Methodology |  |
| Method response |  |  | Methodology |  |
| Evidence route |  |  | Methodology / Findings |  |
| Expected contribution |  |  | Introduction / Discussion |  |
| Boundary |  |  | Methodology / Limitations |  |

Surface map:

| Surface Element | Current Wording | Motivation Role | Proposed Wording / Strategy | Status |
|---|---|---|---|---|
| Title |  |  |  |  |
| Aim |  |  |  |  |
| Research questions |  |  |  |  |
| Introduction topic sentences |  |  |  |  |
| Literature Review subsection headings |  |  |  |  |
| Methodology rationale |  |  |  |  |
| Concept card description |  |  |  |  |
| Supervisor questions |  |  |  |  |

## 3. Dissertation Revision Matrix

Use for supervisor feedback, major proposal revision, or chapter rewrite.

Purpose: make the revision operation explicit before editing.

| Section | Unit ID | Current Function | Needed Function | Motivation Link | Operation | Evidence Source | Claim Strength | Decision |
|---|---|---|---|---|---|---|---|---|
|  | P1 |  |  |  | KEEP / REWRITE / SPLIT / MERGE / MOVE / DELETE / ADD |  |  |  |

Rules:

- `KEEP` is allowed only when the unit already has the right job and evidence boundary.
- `ADD` should not be the default fix; weak structure often needs `MOVE`, `SPLIT`, `MERGE`, `DELETE`, or `REWRITE`.
- Mark missing support as `[NEED SOURCE]`, `[NEED CITATION]`, or `[TO CONFIRM]`.
- For a major rewrite, extract facts and source anchors first, then rewrite from the blueprint instead of editing weak prose line by line.

Revision summary:

| Section | Main Change | Evidence Preserved | Claim Softened / Strengthened | Remaining User Or Supervisor Decision |
|---|---|---|---|---|
|  |  |  |  |  |

## 4. Dissertation Logic-Transfer Audit

Use after a major rewrite to check whether the argument actually improved.

Purpose: compare original logic, target dissertation logic, and revised logic.

| Section | Original Logic | Target Dissertation Logic | Revised Logic | Evidence Of Transfer | Verdict |
|---|---|---|---|---|---|
| Introduction |  |  |  |  | pass / risk |
| Literature Review |  |  |  |  | pass / risk |
| Methodology |  |  |  |  | pass / risk |
| Findings / Expected Findings |  |  |  |  | pass / risk |
| Discussion / Contribution |  |  |  |  | pass / risk |

Seven-anchor dissertation test:

1. title or subtitle promise
2. first Introduction problem sentence
3. main gap sentence
4. aim or research-question sentence
5. methodology rationale sentence
6. expected contribution or first findings headline
7. limitation / boundary / implication sentence

The anchors should form one project story. If the chain breaks, fix the section blueprint before polishing language.

Common defects:

| Defect | Meaning |
|---|---|
| `background-stack` | literature is listed without narrowing to a dissertation gap |
| `gap-vague` | gap is broad or not interviewable |
| `method-recipe` | method is described without explaining why it answers the RQs |
| `concept-card-overclaim` | concept card is treated as prototype evidence |
| `claim-leap` | interpretation exceeds literature or participant evidence |
| `discussion-repeat` | discussion repeats results without answering the project motivation |

## 5. Dissertation Artifact Completeness Check

Use before delivering an important planning document, proposal draft, chapter plan, or revision package.

Minimum expected artifacts for a serious planning or revision task:

| Artifact | Required When | Pass / Risk | Location Or Note |
|---|---|---|---|
| Source map | formal or source-heavy work |  |  |
| Working or confirmed motivation | proposal/chapter/major revision |  |  |
| Motivation thread model | scattered or high-stakes writing |  |  |
| Section blueprint | any substantive drafting |  |  |
| Section rationale matrix | proposal/chapter/rewrite planning |  |  |
| Revision matrix | supervisor feedback or major rewrite |  |  |
| Logic-transfer audit | after major rewrite |  |  |
| Citation/source status | citation-heavy writing |  |  |
| `TO CONFIRM` list | any uncertain fact or decision |  |  |
| Word/render check | important `.docx` output |  |  |

Pass standard:

- The document can be traced from source map to motivation, section decisions, evidence boundaries, and final output.
- Missing artifacts are acceptable only when the task is small or the final report explicitly explains why they were not needed.
