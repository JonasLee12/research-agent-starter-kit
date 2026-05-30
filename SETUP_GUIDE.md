# Setup Guide

## 0. Install Required Software

Before cloning the template, read:

- [`docs/SOFTWARE_AND_PLUGIN_REQUIREMENTS.md`](docs/SOFTWARE_AND_PLUGIN_REQUIREMENTS.md)

Minimum setup:

- [Codex](https://chatgpt.com/codex/) or [Codex CLI](https://github.com/openai/codex)
- [GitHub account](https://github.com/)
- [Git](https://git-scm.com/downloads)
- Terminal or shell: [Apple Terminal](https://support.apple.com/guide/terminal/welcome/mac), [Windows Terminal](https://github.com/microsoft/terminal), Git Bash, or Linux terminal
- [Python 3](https://www.python.org/downloads/) for the built-in local scripts

Optional but useful:

- [GitHub CLI (`gh`)](https://cli.github.com/)
- [GitHub Desktop](https://desktop.github.com/download/)
- [ChatGPT Codex Connector](https://github.com/apps/chatgpt-codex-connector)
- [Obsidian](https://obsidian.md/download)
- [LibreOffice](https://www.libreoffice.org/download/) or [Microsoft Word](https://www.microsoft.com/en-us/microsoft-365/word)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) for optional independent review through `scripts/claude_independent_review.py` if you have access

## 1. Copy Or Clone

Clone the repository or copy this folder to a new project location. Keep it private until the public-release audit is complete.

Recommended project path pattern:

```text
~/Documents/research-agent-starter-kit
```

## 2. Fill In Project Basics

Create your own:

- `RESEARCH_PROJECT_BRIEF.md`
- `research-wiki/PROJECT_OVERVIEW.md`
- `research-wiki/OPEN_QUESTIONS.md`
- project-specific requirement notes, such as `compliance/PROJECT_COMPLIANCE_TRACKER.md` or `university-guidance/FORMAT_REQUIREMENTS.md`

Use the existing template files as starting points.

If your project is a dissertation or thesis, you may also create `DISSERTATION_BRIEF.md` from `DISSERTATION_BRIEF_TEMPLATE.md`.

## 3. Configure Agent Memory

Update:

- `AGENTS.md`
- `PROJECT_AGENT_PREFERENCES.md`
- `research-wiki/TASK_STATE.md`

Keep private information minimal. Use placeholders until a source file confirms a fact.

## 4. Use Skills

Project skills live in:

```text
.agents/skills/
```

Use the skills by name in agent prompts, or let `agent-orchestration` route tasks.

For formal writing, keep these files active:

- `.agents/skills/cognitive-frameworks/SKILL.md`
- `.agents/skills/academic-integrity-preflight/SKILL.md`
- `.agents/skills/academic-self-review-loop/SKILL.md`
- `research-wiki/WRITING_QUALITY_RUBRIC.md`
- `research-wiki/DOCUMENT_PIPELINE.md`

They help the agent plan the argument, self-review the draft, and record thinking/writing/delivery checkpoints.

For knowledge-base work, start here:

- `knowledge-base/self-growing/README.md`
- `knowledge-base/self-growing/growth-queue.md`
- `knowledge-base/self-growing/compiled-wiki/INDEX.md`

Then run:

```bash
python scripts/kb_health_check.py
python scripts/build_agent_index.py --rebuild --summary
python scripts/local_retrieval_search.py --rebuild --query "source readiness"
```

Optional specialist skills:

- `research-neural-network-figure` for real AI/model architecture diagrams.
- `research-nature-figure` for high-quality research figure planning.
- `research-nature-writing` for article-style structure after evidence checks.

These skills are quality layers. They do not replace source checks, compliance checks, citation review, or delivery gates.

## 5. Keep Evidence Boundaries

Use labels:

- `CONFIRMED`
- `LITERATURE-SUPPORTED`
- `CONTEXTUAL`
- `INFERENCE`
- `TO CONFIRM`
- `NEEDS VERIFICATION`

## 6. Before Sharing

Run:

```bash
./scripts/privacy_check.sh
python scripts/run_skill_evals.py
python scripts/validate_agent_schemas.py
python -m unittest discover -s tests
```

Review the output before pushing to GitHub or sharing with friends.
