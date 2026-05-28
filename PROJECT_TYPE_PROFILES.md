# Project Type Profiles

Use this file to adapt the starter kit to different research projects. Pick one primary profile, then adjust `RESEARCH_PROJECT_BRIEF.md`, `AGENTS.md`, and task prompts around that profile.

If you are using Codex, ask it to use `research-project-adapter` after choosing a profile.

## Core Profiles

| Profile | Best For | Default Outputs | Key Gates |
|---|---|---|---|
| Taught dissertation / thesis | undergraduate, master's, doctoral, capstone research | proposal, ethics files, chapters, supervisor notes | source-first, rubric evidence, ethics/compliance, document quality |
| Journal article / manuscript | article drafting, revision, response to reviewers | argument spine, literature synthesis, manuscript sections, reviewer response | source readiness, citation claim-support, target-journal style, document quality |
| Research proposal / grant | funding proposal, PhD proposal, project bid | aims, rationale, work packages, impact, risk plan | funder/source requirements, feasibility, contribution, budget/risk evidence |
| Qualitative fieldwork project | interviews, observations, focus groups, ethnography | protocol, topic guide, consent materials, coding plan, theme audit | ethics/compliance, participant privacy, qualitative evidence audit |
| Quantitative or computational study | survey, experiment, modelling, data analysis, reproducible research | analysis plan, data dictionary, methods section, results audit | data provenance, statistical/model validity, reproducibility, citation support |
| Design research / product research | co-design, UX research, prototype evaluation, design recommendations | concept cards, design principles, requirements, evaluation reports | user evidence, responsible design, traceability, privacy |
| Policy / practice report | organisational, professional, or public-facing report | evidence summary, recommendations, implementation risks | source hierarchy, stakeholder relevance, recommendation traceability |
| Literature review / evidence synthesis | standalone review, scoping review, systematic-style review | search log, screening table, synthesis matrix, review chapter | search protocol, source readiness, citation claim-support |
| Knowledge-base / RAG project | research memory, teaching resource base, organisational knowledge system | source schema, ingestion plan, retrieval tests, governance plan | privacy, source readiness, retrieval evaluation, update policy |
| Custom profile | projects that do not fit the list | define from project brief | define from source-first and quality requirements |

## Profile Selection Rule

Do not let the file names decide the project type. Some skills still use `dissertation-*` names for backwards compatibility, but the project profile controls how they should be interpreted.

## Minimal Setup For Any Profile

1. Copy `RESEARCH_PROJECT_BRIEF_TEMPLATE.md` to `RESEARCH_PROJECT_BRIEF.md`.
2. Select a primary profile in `RESEARCH_PROJECT_BRIEF.md`.
3. Fill only source-confirmed facts.
4. Run runtime preflight before substantial work:

```bash
python3 scripts/agent_runtime.py "set up this research project" --window Maintenance --write --strict
```

5. Keep source metadata separate from source evidence in `knowledge-base/SOURCE_READINESS_MATRIX.md`.

## When To Keep Dissertation-Specific Files

Keep `DISSERTATION_BRIEF_TEMPLATE.md`, `ethics/`, and `university-guidance/` when the project is assessed academic work or involves institutional requirements.

For non-dissertation projects, treat those files as optional examples unless the project has equivalent ethics, compliance, client, journal, or funder requirements.
