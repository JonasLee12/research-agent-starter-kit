# Self-Growing Knowledge Base

This folder is the controlled intake and synthesis layer for a research-project knowledge base.

It helps a project grow from reading, source searches, stakeholder feedback, project decisions, and planning notes while keeping source status visible.

## Folder Structure

| Path | Use |
|---|---|
| `raw-inbox/` | Temporary intake queue for new notes, source pointers, exports, or reading-list material |
| `growth-queue.md` | Triage table showing what needs reading, compilation, verification, or sync |
| `compiled-wiki/` | Theme-level synthesis pages that link back to source-of-record files |
| `health-checks/` | Placeholder folder for generated health-check reports; generated reports should stay out of public commits |

## Operating Rule

Every item must answer four questions before it is used in formal writing:

1. What is the source?
2. What is the evidence status?
3. What project theme can it support?
4. What can it not support yet?

## Evidence Labels

- `CONFIRMED`: directly supported by local project files or user-confirmed facts.
- `LITERATURE-SUPPORTED`: supported by a screened academic source.
- `CONTEXTUAL`: useful for planning but not formal evidence.
- `METADATA ONLY`: bibliographic metadata found, but source content not reviewed.
- `INFERENCE`: synthesis or implication drawn by the agent/researcher.
- `TO CONFIRM`: needs user, supervisor, PI, reviewer, client, ethics/IRB, rubric, journal, funder, or source verification.

## Minimal Growth Workflow

1. Add new material to `raw-inbox/` or to the appropriate canonical folder.
2. Add a row to `growth-queue.md`.
3. Compile useful knowledge into source notes, literature maps, method decisions, or compiled-wiki pages.
4. Link Obsidian or another note app only to canonical project files or short navigation summaries.
5. Run `python3 scripts/kb_health_check.py --write`.

## Boundary

Do not place raw participant material, signed forms, interview recordings, identifiable records, private client files, restricted LMS content, or credentials here.

Compiled wiki pages are navigation and synthesis aids. They do not replace source registers, source-readiness checks, source notes, official requirements, or claim-support review.
