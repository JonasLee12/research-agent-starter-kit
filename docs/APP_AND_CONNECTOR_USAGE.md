# App And Connector Usage

语言：English | 中文说明见下方

This file explains which apps, connectors, and external tools are required, recommended, optional, or not included by default.

## English

## Core Rule

Start with the minimum setup. Add optional apps only when your project has a real workflow need.

This repository does not bundle private credentials, browser sessions, subscription database access, or paid software.

## Usage Status

| App / Connector | Status | Use In This Starter Kit | Install / Connect When |
|---|---|---|---|
| Codex / Codex CLI | Required | Runs the agent and reads local project files | Always needed |
| Git | Required | Tracks local changes and supports updates | Always needed |
| GitHub account | Required for sharing | Hosts private or public template repositories | Needed for cloning, sharing, or updating via GitHub |
| Terminal / shell | Required | Runs privacy checks, runtime preflight, and validation scripts | Always useful |
| Python 3 | Required for local scripts | Runs runtime preflight, cognitive protocol checks, skill evals, connector checks, and citation audit scripts | Needed if you use the built-in scripts |
| GitHub Desktop | Recommended | Beginner-friendly Git interface | Use if command-line Git feels difficult |
| GitHub CLI `gh` | Recommended | Checks remote repo status, About text, Actions, and pushes | Use for maintenance and GitHub verification |
| ChatGPT Codex Connector / GitHub App | Recommended | Lets Codex inspect GitHub repository files through the connected app | Use when Codex needs GitHub-side repository context |
| Obsidian | Optional | Reads `research-wiki/` and `knowledge-base/` as a linked Markdown knowledge base | Use if you want a visual note-taking layer |
| Microsoft Word | Optional but useful | Final editing, comments, and `.docx` review | Use for formal documents or stakeholder drafts |
| LibreOffice | Optional | Free `.docx` opening and rendering | Use if Microsoft Word is unavailable |
| Poppler | Optional | PDF/page-image rendering checks | Use when layout verification matters |
| Zotero | Optional | Reference manager for literature collections and citation workflows | Use when your project has a serious bibliography workflow |
| Playwright | Optional | Browser automation for read-only checks, local previews, and UI verification | Use only when browser workflows are needed |
| MarkItDown | Optional | Converts documents into Markdown for source review or knowledge-base ingestion | Use only after privacy review and tool availability check |
| Claude Code | Optional independent reviewer | Can provide a separate review pass when the user has access | Use only as review feedback; do not treat it as source evidence |
| OpenAlex / Crossref / Semantic Scholar APIs | Available through script | Public metadata search via `scripts/academic_database_connector.py` | Use for metadata discovery, not claim evidence |
| Scopus / Web of Science / EBSCO | Connector-ready only | Status checks and credential-aware boundaries | Use only with lawful institutional credentials |
| OpenAI credential | Not required by default | Not needed for the template itself | Only needed if you build separate API-powered tools |
| External MCP servers | Not required by default | Not bundled or required | Add only after a clear project need and security review |

## Local Script Tools

These scripts are included in the repository and use Python 3 standard-library features unless a script-specific note says otherwise.

| Script | Status | Use |
|---|---|---|
| `scripts/agent_runtime.py` | Included | Deterministic routing, required-gate checks, runtime receipts, and session-log events |
| `scripts/cognitive_protocol_check.py` | Included | Checks whether a planning note has section type, gap/problem type, claim, evidence, warrant, boundary, and rhetorical plan |
| `scripts/run_skill_evals.py` | Included | Static checks that high-risk skill routes point to real local skills/tools |
| `scripts/run_behavioral_evidence_checks.py` | Included | Checks whether project files show evidence of runtime, source-readiness, self-review, and checkpoint workflows |
| `scripts/validate_agent_schemas.py` | Included | Validates local workflow schema files |
| `scripts/claude_independent_review.py` | Included | Optional privacy-gated Claude Code independent review wrapper with timeout handling |
| `scripts/privacy_check.sh` | Included | Scans for common privacy risks before sharing |
| `scripts/academic_database_connector.py` | Included | Public metadata search and subscription credential boundary checks |
| `scripts/citation_style_check.py` | Included | Citation/reference consistency check |
| `scripts/citation_claim_audit.py` | Included | Creates a claim-support verification queue |

## Important Boundaries

- Public metadata is not source evidence.
- Claude Code feedback is not source evidence.
- Subscription databases need lawful access.
- Browser automation must not submit, upload, download, or modify private sites unless explicitly confirmed.
- Zotero collection membership does not make a source citation-ready.
- Obsidian is a reading/navigation layer; the source of record stays in the project files.
- Do not commit credentials, tokens, cookies, `.env` files, browser profiles, or private local database files.

## Recommended Minimal Setup

1. Codex or Codex CLI.
2. Git.
3. GitHub account.
4. Terminal or shell.
5. Python 3 for local scripts.
6. This repository cloned locally.

Then run:

```bash
./scripts/privacy_check.sh
python3 scripts/agent_runtime.py "set up this research project" --window Maintenance --write --strict
```

## 中文

## 核心原则

先用最小配置。只有当你的项目真的需要某个工作流时，再安装或连接额外 App。

这个仓库不会自带私人凭据、浏览器登录状态、订阅数据库权限或付费软件。

## 使用状态表

| App / Connector | 状态 | 在这套系统里的用途 | 什么时候安装 / 连接 |
|---|---|---|---|
| Codex / Codex CLI | 必需 | 运行 Agent，读取本地项目文件 | 总是需要 |
| Git | 必需 | 追踪本地改动，支持版本更新 | 总是需要 |
| GitHub account | 分享时必需 | 托管 private 或 public template repository | 需要 clone、分享或通过 GitHub 更新时 |
| Terminal / shell | 必需 | 运行 privacy check、runtime preflight 和验证脚本 | 基本总会用到 |
| Python 3 | 本地脚本必需 | 运行 runtime preflight、cognitive protocol check、skill eval、connector check 和 citation audit scripts | 使用内置脚本时需要 |
| GitHub Desktop | 推荐 | 对新手更友好的 Git 图形界面 | 不熟悉命令行 Git 时 |
| GitHub CLI `gh` | 推荐 | 检查远端 repo、About、Actions 和 push 状态 | 做维护和 GitHub 验证时 |
| ChatGPT Codex Connector / GitHub App | 推荐 | 让 Codex 通过连接器读取 GitHub 仓库内容 | Codex 需要 GitHub 端仓库上下文时 |
| Obsidian | 可选 | 把 `research-wiki/` 和 `knowledge-base/` 当作 Markdown 知识库阅读 | 想要可视化笔记层时 |
| Microsoft Word | 可选但常用 | 最终文档编辑、批注和 `.docx` 检查 | 有正式文档或给他人看的 draft 时 |
| LibreOffice | 可选 | 免费打开和渲染 `.docx` | 没有 Microsoft Word 时 |
| Poppler | 可选 | PDF/page-image 渲染检查 | 需要检查版面时 |
| Zotero | 可选 | 管理文献 collection 和 citation workflow | 项目有正式参考文献管理需求时 |
| Playwright | 可选 | 浏览器自动化、只读检查、本地预览、UI 验证 | 项目真的需要浏览器流程时 |
| MarkItDown | 可选 | 把文档转成 Markdown，用于 source review 或知识库导入 | 做过隐私检查并确认工具可用后 |
| Claude Code | 可选 independent reviewer | 有权限时可作为独立审稿/审查工具 | 只作为反馈，不可当作 source evidence |
| OpenAlex / Crossref / Semantic Scholar APIs | 脚本可用 | 通过 `scripts/academic_database_connector.py` 做公共 metadata search | 用于发现文献 metadata，不可直接当 claim evidence |
| Scopus / Web of Science / EBSCO | 仅 connector-ready | 检查凭据状态和访问边界 | 只有具备合法 institutional credentials 时 |
| OpenAI credential | 默认不需要 | 模板本身不需要 | 只有你另建 API-powered tools 时 |
| External MCP servers | 默认不需要 | 模板不自带、不依赖 | 只有明确项目需求并完成安全审查后 |

## 本地脚本工具

这些脚本已包含在仓库中。默认使用 Python 3 标准库，除非某个脚本另有说明。

| Script | 状态 | 用途 |
|---|---|---|
| `scripts/agent_runtime.py` | 已包含 | 确定性路由、required-gate checks、runtime receipts 和 session-log events |
| `scripts/cognitive_protocol_check.py` | 已包含 | 检查 planning note 是否包含 section type、gap/problem type、claim、evidence、warrant、boundary 和 rhetorical plan |
| `scripts/run_skill_evals.py` | 已包含 | 检查高风险 skill routes 是否指向真实本地 skills/tools |
| `scripts/run_behavioral_evidence_checks.py` | 已包含 | 检查项目文件是否体现 runtime、source-readiness、self-review 和 checkpoint workflows |
| `scripts/validate_agent_schemas.py` | 已包含 | 验证本地 workflow schema files |
| `scripts/claude_independent_review.py` | 已包含 | 可选的 Claude Code 独立 review wrapper，带隐私 gate 和 timeout handling |
| `scripts/privacy_check.sh` | 已包含 | 分享前扫描常见隐私风险 |
| `scripts/academic_database_connector.py` | 已包含 | 公共 metadata search 和 subscription credential boundary checks |
| `scripts/citation_style_check.py` | 已包含 | citation/reference consistency check |
| `scripts/citation_claim_audit.py` | 已包含 | 生成 claim-support verification queue |

## 重要边界

- 公共 metadata 不是正式证据。
- Claude Code feedback 不是正式证据。
- 订阅数据库需要合法访问权限。
- 浏览器自动化不能默认提交、上传、下载或修改私有网站内容。
- Zotero collection membership 不等于文献已经 citation-ready。
- Obsidian 是阅读和导航层，项目文件仍然是 source of record。
- 不要提交 credentials、tokens、cookies、`.env` files、browser profiles 或私人本地数据库文件。

## 推荐最小配置

1. Codex 或 Codex CLI。
2. Git。
3. GitHub account。
4. Terminal 或 shell。
5. Python 3，用于运行本地脚本。
6. 本地 clone 这个 repository。

然后运行：

```bash
./scripts/privacy_check.sh
python3 scripts/agent_runtime.py "set up this research project" --window Maintenance --write --strict
```
