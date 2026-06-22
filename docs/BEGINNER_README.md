# Beginner README: Using This Kit With Codex And GitHub

This guide is for people who are new to Codex, GitHub, and research-agent workflows.

You do not need to understand every file in this repository before using it. The aim is to give an AI coding agent a local project workspace with clear rules, source boundaries, and checks.

## What This Repository Is

This is a starter kit for building a local research assistant around your own project.

It helps an AI coding agent:

- read your project rules before writing;
- check sources before making claims;
- keep small tasks lightweight;
- record evidence when important checks run;
- help flag weak formal documents before delivery;
- avoid leaking private research material into public GitHub.

It is not a finished dissertation, thesis, paper, report, or app. You customise it for your own project.

## What You Need

Minimum:

- a computer with this repository downloaded;
- Python 3.9 or newer;
- a coding agent that can read local files, such as Codex, Claude Code, Cursor, or another local coding assistant.

Helpful but optional:

- a GitHub account;
- basic Git installed on your computer;
- Obsidian if you like visual notes;
- Claude Code if you want optional independent review.

You can still use many files as checklists even if you are not comfortable with Git yet.

## The Simplest Way To Start

1. Download or clone the repository.
2. Open the folder in your coding-agent tool.
3. Read `README.md` for the normal overview.
4. Copy `templates/AGENTS.example.md` to `AGENTS.md` if you are making a fresh project.
5. Fill in only confirmed project facts. Leave unknown fields as `TO CONFIRM`.
6. Ask your agent to run the local checks.

Useful first prompt:

```text
Please read AGENTS.md, PROJECT_AGENT_PREFERENCES.md, and RESEARCH_PROJECT_BRIEF_TEMPLATE.md.
Help me adapt this starter kit to my project.
Do not draft formal text yet. First identify what project facts and source files are still TO CONFIRM.
```

## If You Do Not Know GitHub

Think of GitHub as an online backup and sharing place for code and text files.

Basic terms:

| Term | Meaning |
|---|---|
| Repository / repo | A project folder tracked by Git |
| Commit | A saved checkpoint of file changes |
| Push | Upload local commits to GitHub |
| Pull | Download newer GitHub changes to your computer |
| Branch | A separate line of work |
| Pull request | A review page for merging a branch into the main project |

If you are new, do not push private research data. Keep raw data, transcripts, participant records, credentials, and private institutional material outside public GitHub.

Before sharing publicly, run:

```bash
bash scripts/privacy_check.sh
```

Then manually review `PRIVACY_CHECKLIST.md`.

## If You Do Not Know Codex

Codex is an AI coding agent. In this project, you can ask it to inspect files, update rules, run checks, and create research-workflow documents.

The enforcement layer is the local project rules and Python checks, such as `AGENTS.md` and `scripts/`; the agent helps run and follow them.

Good beginner prompts:

```text
Please classify this task before acting. Tell me which files you need to read first.
```

```text
Please run the runtime preflight for this task and explain whether it is a bounded task or a formal-writing task.
```

```text
Please check whether this source is only metadata, partially reviewed, or citation-ready. Do not upgrade status without source-section review.
```

```text
Please prepare a formal document only after source-first, claim-support, integrity, and document-quality checks.
```

Avoid vague prompts such as:

```text
Make this perfect.
```

Instead, say what the output is for, who will read it, and which sources are allowed.

## The Most Important Files

| File | Why it matters |
|---|---|
| `AGENTS.md` | Main rules the agent should follow |
| `PROJECT_AGENT_PREFERENCES.md` | Your preferences and project boundaries |
| `RESEARCH_PROJECT_BRIEF_TEMPLATE.md` | Template for describing your project |
| `PROJECT_TYPE_PROFILES.md` | Helps choose whether this is a thesis, paper, report, grant, etc. |
| `knowledge-base/SOURCE_READINESS_MATRIX.md` | Tracks whether sources are metadata-only, partly reviewed, or ready to cite |
| `research-wiki/TASK_STATE.md` | Project memory and current status |
| `research-wiki/STAGE_GRAPH.md` | Helps later work remember earlier decisions |
| `research-wiki/CLAIM_LEDGER_LITE_PROTOCOL.md` | Keeps formal claims within evidence boundaries |
| `research-wiki/VISIBLE_OUTPUT_QA_PROTOCOL.md` | Makes the agent check visible outputs, not only source files |

## Three Task Types

### 1. Bounded Task

Small task. Keep it lightweight.

Examples:

- check whether a paper has a useful section;
- fix a citation key;
- sort source-reading priorities;
- summarise what is still missing.

The agent should not run the full formal-writing chain unless the task grows into formal writing or protected file changes.

### 2. Formal Writing Task

Higher-risk task. Needs checks.

Examples:

- write formal paragraphs;
- revise a thesis chapter;
- prepare a report section;
- make a stakeholder-facing document.

The agent should use source-first checks, claim boundaries, integrity checks, self-review, style checks, and document-quality gates.

### 3. Visible Delivery Task

The reader will see a rendered output.

Examples:

- Word document;
- PDF;
- figure;
- public GitHub README;
- Obsidian graph/page;
- browser page.

The agent should use Visible Output QA. A file existing on disk is not enough.

## Safe Working Habits

- Keep private data out of public GitHub.
- Do not ask the agent to invent citations or facts.
- Treat search results as candidates, not evidence.
- Keep `TO CONFIRM` when a fact is not proven.
- Use commits as checkpoints.
- Run validation before trusting a major update.

## Basic Validation

After setup or major changes, run:

```bash
python scripts/run_skill_evals.py
python scripts/validate_agent_schemas.py
python scripts/session_log_integrity_check.py --strict --no-report
python scripts/borrowed_pattern_boundary_lint.py --no-report
python -m unittest discover -s tests
bash scripts/privacy_check.sh
```

If you do not know how to run commands, ask Codex:

```text
Please run the basic validation commands for this starter kit and explain the result in plain language.
```

## Noncommercial License

This repository is provided under the PolyForm Noncommercial License. Personal learning, education, and non-commercial research use are allowed. Commercial use, resale, paid hosting/SaaS, paid training, consulting productisation, or redistribution as part of a paid product require prior written permission.

Read `LICENSE` before sharing or reusing the kit beyond personal or educational use.

## First-Day Checklist

- [ ] Download or clone the repository.
- [ ] Open it in Codex or another coding agent.
- [ ] Read this guide and `README.md`.
- [ ] Create or customise `AGENTS.md`.
- [ ] Fill project facts only when confirmed.
- [ ] Keep private material outside public GitHub.
- [ ] Run the basic validation commands.
- [ ] Ask the agent to classify your first real task before drafting.
