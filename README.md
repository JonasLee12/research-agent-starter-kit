# Research Agent Starter Kit

A local, file-driven research-project agent with cognitive reasoning, writing quality self-review, and enforced delivery gates.

[中文说明](README_CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3](https://img.shields.io/badge/Python-3-green.svg)](https://www.python.org/)
[![Evals](https://img.shields.io/badge/Skill_Evals-17%2F17_passing-brightgreen.svg)](#validation)

## What is this?

This is a starter kit for building a local AI research agent that helps with dissertations, theses, articles, reports, proposals, and other formal research projects. It is designed for people who want AI assistance with research writing while maintaining source integrity, ethical compliance, and writing quality.

The system provides three layers of quality assurance that work together:

1. **Cognitive reasoning** — forces structured thinking (argument mapping, gap classification, warrant testing) before any formal writing begins
2. **Self-review loop** — requires a two-pass review-revise cycle after drafting, scored against internal writing quality criteria
3. **Delivery gates** — blocks formal document output until source verification, citation audit, and project-specific delivery review are complete

It runs entirely on your local machine using file-based rules and Python scripts. No hosted service, no API dependency for the core workflow.

The latest public version also includes runtime routing regression tests, a privacy-gated Claude Code review wrapper, optional high-impact figure/writing skills, and a weekly literature gap-watch automation template.

## Architecture

See [docs/architecture.md](docs/architecture.md) for the full system diagram.

The system is organised into seven layers:

| Layer | Purpose | Key files |
|---|---|---|
| Rules | Define how the agent works | `AGENTS.md`, `PROJECT_AGENT_PREFERENCES.md`, `.agents/skills/` |
| Task routing | Classify tasks, select skills and gates | `agent-orchestration` skill, `scripts/agent_runtime.py` |
| Evidence | Manage sources, ethics, rubric, citation readiness | `knowledge-base/`, `ethics/`, `university-guidance/` |
| Writing & delivery | Handle drafts, style, quality, and delivery review | `DOCUMENT_PIPELINE.md`, delivery scripts |
| Memory | Preserve project state across sessions | `TASK_STATE.md`, `USER_DASHBOARD.md`, `AGENT_MEMORY_STATUS.md` |
| Tools | Local scripts, Zotero, Obsidian, retrieval, browser | `scripts/`, `.agent-runtime/` |
| Audit | Verify Production runs were properly executed | automations, system audits, runtime receipts |

## Quick Start

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/research-agent-starter-kit.git
cd research-agent-starter-kit

# Install core dependencies
pip install -r requirements.txt

# Optional: install vector retrieval (ChromaDB + sentence-transformers)
pip install -r requirements-vector.txt

# Set up your project
cp templates/AGENTS.example.md AGENTS.md
# Edit AGENTS.md with your project details

# Verify installation
python scripts/run_skill_evals.py
python scripts/validate_agent_schemas.py
python -m unittest discover -s tests
```

## Key Features

| Feature | What it does |
|---|---|
| Source-first gate | Prevents the agent from fabricating facts — requires file evidence before writing |
| Cognitive frameworks | Forces argument mapping, gap classification, and warrant testing before formal writing |
| Academic self-review loop | Two-pass review after drafting: identify weaknesses → revise → fresh re-review |
| Writing quality rubric | Six internal criteria: one point per paragraph, argument progression, evidence integration, reader journey, redundancy control |
| Staged checkpoints | Three-phase pipeline: THINKING → WRITING → DELIVERY, each with its own verification |
| Delivery guard | Blocks formal output if pre-delivery lock, citation audit, or delivery review is missing |
| Retrieval protocol | Four-layer search: ChromaDB semantic / SQLite FTS keyword / Source Readiness Matrix / Obsidian thinking workspace |
| Dual-window workflow | Production Window for writing, Maintenance Window for system upkeep — state shared via files |
| Audit trail | Structured event log, runtime receipts, and automated Production audits |
| External integration | OpenAlex, Crossref, Semantic Scholar for metadata discovery; Zotero for reference management |
| Claude review wrapper | Optional privacy-gated independent review through Claude Code; feedback is advisory, not evidence |
| Research figure/writing skills | Optional `research-*` skills for neural-network figures, high-impact figures, and article-style prose |
| Literature gap-watch automation | Template for weekly candidate-only literature monitoring with Stage A/B/C source-readiness boundaries |

## Customisation

### Add your university materials

Place your marking criteria and module requirements in `university-guidance/`. See `university-guidance/EXAMPLE_RUBRIC_GUIDE.md` for the expected format.

### Add your own skills

Create a new directory in `.agents/skills/your-skill-name/` with a `SKILL.md` file. Register eval test cases in `research-wiki/SKILL_EVAL_REGISTRY.md`. See [CONTRIBUTING.md](CONTRIBUTING.md) for requirements.

### Configure Zotero

See `research-wiki/ZOTERO_AND_CITATION_WORKFLOW_SPEC.md` for setup instructions.

### Adapt cognitive frameworks

Edit `.agents/skills/cognitive-frameworks/SKILL.md` to adjust gap type classifications, warrant quality tests, or rhetorical move sequences for your discipline.

## What this system cannot do

- Automatically verify that a source supports a specific claim (it generates audit queues for human review)
- Access subscription databases like Scopus, Web of Science, or EBSCO (requires institutional API keys)
- Complete ethics approval (it tracks readiness but decisions require supervisor and ethics committee input)
- Guarantee any specific grade or mark
- Prevent you from manually bypassing the workflow outside the agent pipeline
- Replace supervisor judgment, peer review, or academic integrity requirements

## Validation

The system includes built-in validation:

```bash
# Run skill evaluations
python scripts/run_skill_evals.py

# Validate workflow schemas
python scripts/validate_agent_schemas.py

# Run routing regression tests
python -m unittest discover -s tests

# Check behavioural evidence rules
python scripts/run_behavioral_evidence_checks.py

# Run privacy check before sharing
./scripts/privacy_check.sh

# Check vector retrieval (requires requirements-vector.txt)
bash scripts/run_vector_index.sh --rebuild --summary
```

## Documentation

- [Dual Window Guide](docs/DUAL_WINDOW_GUIDE.md) — How Production and Maintenance windows work
- [Skill Development Guide](docs/SKILL_DEVELOPMENT_GUIDE.md) — How to create and test new skills
- [Weekly Literature Gap-Watch Automation](docs/WEEKLY_LITERATURE_GAP_WATCH_AUTOMATION.md) — Candidate-only weekly literature monitoring
- [Retrieval Protocol](research-wiki/RETRIEVAL_PROTOCOL.md) — How the four retrieval layers work together
- [Document Pipeline](research-wiki/DOCUMENT_PIPELINE.md) — The staged checkpoint delivery process

## Acknowledgements

See [ACKNOWLEDGEMENTS.md](ACKNOWLEDGEMENTS.md) for credits to open-source projects that inspired this system.

## License

[MIT](LICENSE)
