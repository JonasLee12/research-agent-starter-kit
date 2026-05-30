# Software And Plugin Requirements

This template is mostly Markdown, project rules, and local Codex skills. It is intentionally lightweight.

For a plain-language status table of apps, connectors, and optional tools, read [`APP_AND_CONNECTOR_USAGE.md`](APP_AND_CONNECTOR_USAGE.md).

## Minimum Setup

| Requirement | Link | Plain-English Purpose |
|---|---|---|
| Codex | [Codex](https://chatgpt.com/codex/) or [Codex CLI](https://github.com/openai/codex) | Runs the agent and reads the local project files. |
| GitHub account | [Sign up](https://github.com/signup) | Lets you clone, share, and update the template. |
| Git | [Download Git](https://git-scm.com/downloads) | Tracks changes and lets you pull updates. |
| Terminal or shell | [Apple Terminal](https://support.apple.com/guide/terminal/welcome/mac), [Windows Terminal](https://github.com/microsoft/terminal), Git Bash, or Linux terminal | Runs simple setup and privacy-check commands. |
| Python 3 | [Download Python](https://www.python.org/downloads/) | Runs the local helper scripts such as runtime preflight, cognitive protocol checks, skill evals, and connector checks. |

## Strongly Recommended

| Tool | Link | Use |
|---|---|---|
| GitHub Desktop | [Download](https://desktop.github.com/download/) | Beginner-friendly clone, commit, pull, and push. |
| GitHub CLI `gh` | [Install](https://cli.github.com/) | Helpful for checking repo access and GitHub Actions. |
| ChatGPT Codex Connector | [GitHub App](https://github.com/apps/chatgpt-codex-connector) | Lets Codex inspect repository files through the GitHub connector. |

## Optional For Research Work

| Tool | Link | Use |
|---|---|---|
| Obsidian | [Download](https://obsidian.md/download) | Reads the Markdown knowledge base like a linked notebook. |
| LibreOffice | [Download](https://www.libreoffice.org/download/) | Free `.docx` opening and rendering. |
| Microsoft Word | [Word](https://www.microsoft.com/en-us/microsoft-365/word) | Final document editing and comments. |
| Poppler | [Project site](https://poppler.freedesktop.org/) | Optional PDF/page-image checks for generated documents. |
| Node.js / npm | [Node.js](https://nodejs.org/) | Optional. Needed only if you choose CLI browser automation workflows that depend on npm/npx. |
| Playwright | [Playwright](https://playwright.dev/) | Optional. Browser automation for read-only checks, local previews, or UI verification. |
| MarkItDown | [Microsoft MarkItDown](https://github.com/microsoft/markitdown) | Optional. Converts documents into Markdown for source review or knowledge-base ingestion. |
| Claude Code | [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | Optional. Can be used through `scripts/claude_independent_review.py` as a privacy-gated independent reviewer if the user has access. It is not required by this template. |
| ChromaDB + sentence-transformers | [ChromaDB](https://www.trychroma.com/) / [Sentence Transformers](https://www.sbert.net/) | Optional. Needed only for neural vector retrieval via `requirements-vector.txt`. |

## Not Needed At First

- OpenAI credential
- Node.js
- npm packages
- Python packages beyond the standard library
- external MCP servers
- browser automation
- MarkItDown

Python 3 itself is needed for the local scripts if you want runtime preflight, skill evals, connector checks, or cognitive protocol checks. Extra Python packages are not needed for the default workflow.

Install extra tools only when your project workflow clearly needs them.

## Beginner Setup Checklist

1. Install Codex or open Codex in ChatGPT.
2. Create a GitHub account.
3. Install Git.
4. Install or confirm Python 3 is available if you plan to run the local scripts.
5. Clone or download this repository.
6. Copy `RESEARCH_PROJECT_BRIEF_TEMPLATE.md` to `RESEARCH_PROJECT_BRIEF.md`.
7. Choose a project profile from `PROJECT_TYPE_PROFILES.md`.
8. Fill placeholders slowly. Use `TO CONFIRM` when unsure.
9. Open the folder in Codex.
10. Ask Codex to read `AGENTS.md`, `PROJECT_AGENT_PREFERENCES.md`, `RESEARCH_PROJECT_BRIEF.md`, `PROJECT_TYPE_PROFILES.md`, and `.agents/skills/`.
11. Run the privacy check before sharing:

```bash
./scripts/privacy_check.sh
```

## Common Confusions

`Git` and `GitHub` are different.

- Git is the local version-control tool.
- GitHub is the website where the repository can live.

`Codex` and `GitHub Connector` are different.

- Codex runs the agent.
- The GitHub Connector lets Codex inspect GitHub repository content after authorisation.

`Obsidian` is optional.

- The project works without it.
- It just makes Markdown notes easier to browse.

`Python` and `Python packages` are different.

- Python 3 runs the built-in scripts.
- Extra Python packages are not needed unless you choose optional extensions.

`SQLite/local retrieval` and `neural vector retrieval` are different.

- `scripts/build_agent_index.py` and `scripts/local_retrieval_search.py` use local Python/SQLite workflows.
- `scripts/build_vector_index.py` and `scripts/vector_retrieval_smoke_test.py` require optional vector packages from `requirements-vector.txt`.
- Retrieval finds candidate files. It does not prove source support.

`Claude Code` and the Claude review wrapper are different.

- Claude Code is the optional external reviewer.
- `scripts/claude_independent_review.py` is the local wrapper that checks privacy, applies a timeout, writes a review report, and reminds users that Claude feedback is advisory only.
