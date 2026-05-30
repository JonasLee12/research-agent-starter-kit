# Weekly Literature Gap-Watch Automation

This template turns a broad "find new literature every week" automation into a staged, priority-weighted gap watch.

Use it when a project already has a working literature map and needs better signal, not more noise.

## Core Boundary

The automation is candidate discovery and source-readiness triage only.

It must not automatically write candidates into:

- `knowledge-base/SOURCE_REGISTER.md`
- `knowledge-base/SOURCE_READINESS_MATRIX.md`
- source notes
- Obsidian or another note app
- Zotero or another citation manager
- formal research text

Candidates stay `METADATA ONLY`, `NEEDS VERIFICATION`, or `TO CONFIRM` until a human or supervised Production run reviews the relevant source sections.

## Stage Logic

### Stage A: Weekly Candidate Discovery

Use this as the default mode.

Each run searches only the current priority tracks and returns a small candidate set.

### Stage B: User-Confirmed Follow-Up

Only after user confirmation should a Production task:

- read the source;
- create or update a source note;
- update the source register;
- update source-readiness status;
- add the source to Zotero or Obsidian.

### Stage C: Source-Readiness Upgrade Queue

Activate Stage C when formal literature review, methodology, manuscript, proposal, or stakeholder-facing drafting begins.

In Stage C, the automation should reduce new-source discovery and prioritise:

- sources already selected but not yet reviewed;
- high-value candidates that need full-text or section review;
- claim-support gaps identified by citation audits.

## Prompt Template

```text
Run the Weekly Literature Gap-Watch Update for this local research project.

Project path: [PROJECT_PATH]

Priority boundary:
- This automation supports literature and methodology planning only.
- It is candidate discovery and source-readiness triage, not final citation approval.
- Do not write candidate sources into SOURCE_REGISTER, SOURCE_READINESS_MATRIX, source notes, Obsidian, Zotero, or formal research text unless the user later confirms ingestion.
- Treat OpenAlex, Crossref, Semantic Scholar, and other public metadata search as METADATA ONLY until source sections are reviewed.
- Do not claim subscription database coverage unless lawful credentials/endpoints/institutional entitlement are configured and a connector status report confirms it.

Read first:
- AGENTS.md
- PROJECT_AGENT_PREFERENCES.md
- research-wiki/TASK_STATE.md latest relevant entries
- research-wiki/EXTERNAL_RESEARCH_CONNECTOR_SPEC.md
- research-wiki/RETRIEVAL_PROTOCOL.md
- knowledge-base/SOURCE_READINESS_MATRIX.md
- knowledge-base/SOURCE_REGISTER.md
- current literature or methodology plan files if present
- .agents/skills/dissertation-research-search-protocol/SKILL.md
- .agents/skills/dissertation-learning-loop/SKILL.md
- .agents/skills/dissertation-literature-review/SKILL.md
- .agents/skills/dissertation-citation-audit/SKILL.md

Before search:
- Run deterministic runtime preflight with scripts/agent_runtime.py when available and write the receipt.
- Check whether the project is in Stage A or Stage C using TASK_STATE and local chapter/manuscript/project status.

Stage logic:
- Stage A default: weekly candidate discovery.
- Stage B is not automatic ingestion. It begins only after the user confirms a candidate should be target-read or ingested.
- Stage C activates when formal drafting has started, when a relevant draft exists, when TASK_STATE/source-readiness notes say the source base should be stabilised, or when the user explicitly asks for Stage C. In Stage C, shift from new-source discovery to source-readiness upgrade queue.

Default search tracks:
1. [TRACK 1: the highest-value topic or gap]
2. [TRACK 2: the second highest-value topic or gap]
3. [TRACK 3: a theory, method, or interpretive lens gap]

Methodology track:
- Default: OFF.
- Only include methodology search when methodology writing is active, TASK_STATE identifies a concrete methodology evidence gap, or the user explicitly asks.

Exclusion rules:
- Exclude sources whose primary contribution is not connected to the current literature or methodology gap, even if the keywords match.
- Exclude generic topic literature unless it directly supports the current project argument.
- Exclude survey-only or methods-mismatched studies unless they support framing.
- Exclude opinion/news/hype unless the project explicitly needs policy or public-discourse evidence.

Candidate limit and format:
- Return top 5-8 candidates only.
- If fewer than 3 credible candidates are found, report the real number and briefly explain why.
- Each candidate must include:
  - first discovered date;
  - source type;
  - DOI or URL;
  - relevance to the current literature/methodology gap;
  - possible claim it may support;
  - why it is not citation-ready yet;
  - action tag: ignore / monitor / target-read / ask user to confirm ingestion.

Action tag rules:
- ignore: weak fit; do not surface again unless scope changes.
- monitor: plausible but not urgent; keep for at most two future cycles with the original relevance note, then downgrade to ignore unless new evidence appears.
- target-read: likely useful; needs full-text or relevant-section review before citation-ready use.
- ask user to confirm ingestion: high relevance and likely worth adding to the project source workflow, but still requires user confirmation before writing to registers, notes, Obsidian, Zotero, or formal text.

Output requirements:
- Write a dated candidate report under knowledge-base/weekly-literature-updates/ or the equivalent project folder.
- Add a concise digest in the automation feedback queue if that workflow is enabled.
- Append a session event when a report is created.
- Mark uncertain items as NEEDS VERIFICATION or TO CONFIRM.
```

## Recommended Report Fields

| Field | Purpose |
|---|---|
| Candidates found this cycle | Shows that the automation actually ran, even when there are few candidates |
| First discovered date | Prevents stale sources from looking new |
| Source type and DOI/URL | Keeps metadata review possible |
| Relevance to current gap | Prevents keyword-only matches |
| Possible claim supported | Shows how the source might be used |
| Why not citation-ready | Preserves source-readiness boundary |
| Action tag | Keeps the follow-up queue manageable |

## Boundary

This automation pattern improves literature monitoring. It does not replace full-text reading, source-section verification, citation auditing, or project-specific evidence judgement.
