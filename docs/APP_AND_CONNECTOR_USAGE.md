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
| Obsidian | Optional | Reads `knowledge-base/` or a copied `templates/obsidian-vault/` as a linked Markdown knowledge layer | Use if you want a visual note-taking layer. Open knowledge-base/ as your Obsidian vault. Do not open the repository root. |
| Microsoft Word | Optional but useful | Final editing, comments, and `.docx` review | Use for formal documents or stakeholder drafts |
| LibreOffice | Optional | Free `.docx` opening and rendering | Use if Microsoft Word is unavailable |
| Poppler | Optional | PDF/page-image rendering checks | Use when layout verification matters |
| Zotero | Optional | Reference manager for literature collections and citation workflows | Use when your project has a serious bibliography workflow |
| Playwright | Optional | Browser automation for read-only checks, local previews, and UI verification | Use only when browser workflows are needed |
| MarkItDown | Optional | Converts documents into Markdown for source review or knowledge-base ingestion | Use only after privacy review and tool availability check |
| External review bundle | Included local workflow | Builds a local prompt bundle for Codex, ChatGPT, Claude, Gemini, or human review | Use when you want a second opinion without making Claude Code required |
| Claude Code | Optional external reviewer runner | Can provide a direct separate review pass when the user has access | Use only as one optional review path; do not treat it as source evidence |
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
| `scripts/build_external_review_bundle.py` | Included | Builds a local review bundle and reusable prompt for Codex, ChatGPT, Claude, Gemini, or human review |
| `scripts/claude_independent_review.py` | Included | Optional privacy-gated Claude Code runner for the same external-review role |
| `scripts/academic_integrity_preflight.py` | Included | Checks concrete integrity risks before formal drafting or delivery |
| `scripts/authorial_voice_scan.py` | Included | Flags detector-evasion framing, disclosure hiding, prompt residue, generic AI-style phrasing, inflated vocabulary, and possible overclaiming |
| `scripts/style_fingerprint_scan.py` | Included | Scans repeated binary negative-contrast templates such as `rather than`, `not...but`, `不是...而是`, and `而不是` |
| `scripts/skill_execution_receipt.py` | Included | Creates/checks auditable receipts proving required skills produced evidence artifacts |
| `scripts/document_quality_check.py` | Included | Checks whether a document-quality review contains concrete evidence rather than generic approval wording |
| `scripts/self_review_loop_check.py` | Included | Checks whether a self-review loop includes concrete findings, revisions, and a fresh second-pass judgement |
| `scripts/material_passport.py` | Included | Packages source, compliance/requirement, citation, and open-confirmation status before formal artifacts move forward |
| `scripts/pre_delivery_lock.py` | Included | Creates/checks local pre-delivery lock receipts before formal delivery |
| `scripts/formal_delivery_guard.py` | Included | Blocks formal delivery when required evidence is missing, with an explicit override audit path |
| `scripts/claim_ledger_lite_check.py` | Included | Checks formal-claim ledger structure, evidence-status boundaries, cannot-prove fields, concept contracts, and metadata-only overclaims |
| `scripts/visible_output_qa_check.py` | Included | Checks visible-output QA notes for rendered/preview evidence, deterministic checks, visual inspection, baseline/regression boundary, unresolved risks, and verdict |
| `scripts/borrowed_pattern_boundary_lint.py` | Included | Blocks unsafe borrowed style/workflow wording such as detector-evasion, detector-score, authorship-verdict, or humanising-as-evasion promises |
| `scripts/kb_health_check.py` | Included | Checks self-growing knowledge-base structure, raw-inbox triage, unresolved markers, and private-data boundary hits |
| `scripts/build_agent_index.py` | Included | Builds a local SQLite index of project memory files |
| `scripts/local_retrieval_search.py` | Included | Runs local FTS and hashed-vector retrieval over project files |
| `scripts/build_vector_index.py` | Optional vector deps | Builds a local ChromaDB neural vector index when vector dependencies are installed |
| `scripts/vector_retrieval_smoke_test.py` | Optional vector deps | Tests whether known queries retrieve expected template files |
| `scripts/privacy_check.sh` | Included | Scans for common privacy risks before sharing |
| `scripts/academic_database_connector.py` | Included | Public metadata search and subscription credential boundary checks |
| `scripts/citation_style_check.py` | Included | Citation/reference consistency check |
| `scripts/citation_claim_audit.py` | Included | Creates a claim-support verification queue |

## Important Boundaries

- Public metadata is not source evidence.
- External reviewer feedback from Codex, ChatGPT, Claude, Gemini, or a human reviewer is not source evidence.
- Claude Code is optional. Users without Claude can use `scripts/build_external_review_bundle.py` and paste the generated prompt into a separate reviewer.
- Authorial voice checks are not AI detectors. They improve evidence-led style and block detector-evasion or disclosure-hiding requests.
- Borrowed-pattern lint is not an AI detector. It only checks whether imported public style/workflow language accidentally creates unsafe detector-evasion, detector-score, authorship-verdict, or humanising-as-evasion instructions.
- Claim Ledger Lite is not source proof. It records claim boundaries and allowed wording until source-section review or project confirmation exists.
- Visible Output QA is not approval. It verifies that the visible surface was checked; content, compliance, citation, and quality gates still apply.
- Style fingerprint scans are not AI detectors. They only flag repeated surface templates that may make formal prose feel mechanical.
- Skill execution receipts prove a required check produced an evidence artifact. They do not prove that the evidence is academically sufficient or that the agent revised deeply.
- Subscription databases need lawful access.
- Browser automation must not submit, upload, download, or modify private sites unless explicitly confirmed.
- Zotero collection membership does not make a source citation-ready.
- Obsidian is a reading/navigation layer; the source of record stays in the project files.
- Open knowledge-base/ as your Obsidian vault. Do not open the repository root, because it will index system files such as `research-wiki/`, `scripts/`, `tests/`, and audit logs.
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
| Obsidian | 可选 | 把 `knowledge-base/` 或复制后的 `templates/obsidian-vault/` 当作 Markdown 知识层阅读 | 想要可视化笔记层时。请把 knowledge-base/ 作为 Obsidian vault 打开，不要打开整个仓库根目录。 |
| Microsoft Word | 可选但常用 | 最终文档编辑、批注和 `.docx` 检查 | 有正式文档或给他人看的 draft 时 |
| LibreOffice | 可选 | 免费打开和渲染 `.docx` | 没有 Microsoft Word 时 |
| Poppler | 可选 | PDF/page-image 渲染检查 | 需要检查版面时 |
| Zotero | 可选 | 管理文献 collection 和 citation workflow | 项目有正式参考文献管理需求时 |
| Playwright | 可选 | 浏览器自动化、只读检查、本地预览、UI 验证 | 项目真的需要浏览器流程时 |
| MarkItDown | 可选 | 把文档转成 Markdown，用于 source review 或知识库导入 | 做过隐私检查并确认工具可用后 |
| External review bundle | 已包含的本地流程 | 为 Codex、ChatGPT、Claude、Gemini 或人工 reviewer 生成本地 prompt bundle | 想要第二意见但不想把 Claude Code 设为必需工具时 |
| Claude Code | 可选 external reviewer runner | 有权限时可直接运行独立 review | 只是一个可选 review path，不可当作 source evidence |
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
| `scripts/build_external_review_bundle.py` | 已包含 | 为 Codex、ChatGPT、Claude、Gemini 或人工 review 生成本地质审包和通用 prompt |
| `scripts/claude_independent_review.py` | 已包含 | 同一 external-review 角色的可选 Claude Code runner，带隐私 gate 和 timeout handling |
| `scripts/academic_integrity_preflight.py` | 已包含 | 正式 drafting 或 delivery 前检查具体 academic/professional integrity 风险 |
| `scripts/authorial_voice_scan.py` | 已包含 | 检查检测规避表述、隐藏 AI-use disclosure、prompt residue、泛泛 AI 式表达、虚高词汇和可能的 overclaiming |
| `scripts/style_fingerprint_scan.py` | 已包含 | 扫描 `rather than`、`not...but`、`不是...而是`、`而不是` 等重复二元对比模板 |
| `scripts/skill_execution_receipt.py` | 已包含 | 创建/检查必做 skill 是否留下证据文件的执行回执 |
| `scripts/document_quality_check.py` | 已包含 | 检查 document-quality review 是否有具体证据，而不是泛泛说“已检查” |
| `scripts/self_review_loop_check.py` | 已包含 | 检查 self-review loop 是否包含具体发现、修改动作和新的二轮判断 |
| `scripts/material_passport.py` | 已包含 | 在正式文档推进前打包 source、compliance/requirement、citation 和 open-confirmation 状态 |
| `scripts/pre_delivery_lock.py` | 已包含 | 正式交付前创建/检查本地 pre-delivery lock receipts |
| `scripts/formal_delivery_guard.py` | 已包含 | 缺少必要证据时阻止正式交付，并提供明确的 override audit path |
| `scripts/claim_ledger_lite_check.py` | 已包含 | 检查 formal-claim ledger 的字段、evidence-status boundary、cannot-prove、concept contract 和 metadata-only overclaim |
| `scripts/visible_output_qa_check.py` | 已包含 | 检查 visible-output QA note 是否有 rendered/preview evidence、deterministic checks、visual inspection、baseline/regression boundary、unresolved risks 和 verdict |
| `scripts/borrowed_pattern_boundary_lint.py` | 已包含 | 阻止把外部 style/workflow 语言变成 detector-evasion、detector-score、authorship-verdict 或 humanising-as-evasion 承诺 |
| `scripts/kb_health_check.py` | 已包含 | 检查 self-growing knowledge base 结构、raw-inbox triage、未解决标记和 private-data boundary hits |
| `scripts/build_agent_index.py` | 已包含 | 为项目记忆文件建立本地 SQLite index |
| `scripts/local_retrieval_search.py` | 已包含 | 对项目文件运行本地 FTS 和 hashed-vector retrieval |
| `scripts/build_vector_index.py` | 可选 vector dependencies | 安装 vector dependencies 后建立本地 ChromaDB neural vector index |
| `scripts/vector_retrieval_smoke_test.py` | 可选 vector dependencies | 测试已知 query 是否能检索到预期模板文件 |
| `scripts/privacy_check.sh` | 已包含 | 分享前扫描常见隐私风险 |
| `scripts/academic_database_connector.py` | 已包含 | 公共 metadata search 和 subscription credential boundary checks |
| `scripts/citation_style_check.py` | 已包含 | citation/reference consistency check |
| `scripts/citation_claim_audit.py` | 已包含 | 生成 claim-support verification queue |

## 重要边界

- 公共 metadata 不是正式证据。
- Codex、ChatGPT、Claude、Gemini 或人工 reviewer 给出的 external feedback 都不是正式证据。
- Claude Code 是可选工具。没有 Claude 的用户可以使用 `scripts/build_external_review_bundle.py`，把生成的 prompt 复制到另一个 reviewer。
- Authorial voice check 不是 AI detector。它用于改进 evidence-led style，并阻止检测规避或隐藏 AI-use disclosure 的请求。
- Borrowed-pattern lint 不是 AI detector。它只检查借鉴外部公开 style/workflow 语言时，是否误生成检测规避、检测分数优化、作者身份判断或 humanising-as-evasion 规则。
- Claim Ledger Lite 不是 source proof。它只记录 claim boundary 和 allowed wording，直到 source-section review 或项目确认完成。
- Visible Output QA 不是正式批准。它只证明可见表面被检查过；content、compliance、citation 和 quality gates 仍然适用。
- Style fingerprint scan 不是 AI detector。它只检查会让正式文本显得机械的重复表层句式。
- Skill execution receipts 只证明必做检查产出了证据文件，不证明证据已经足够或 agent 已经深度修改。
- 订阅数据库需要合法访问权限。
- 浏览器自动化不能默认提交、上传、下载或修改私有网站内容。
- Zotero collection membership 不等于文献已经 citation-ready。
- Obsidian 是阅读和导航层，项目文件仍然是 source of record。
- 请把 knowledge-base/ 作为 Obsidian vault 打开，不要打开整个仓库根目录；否则 `research-wiki/`、`scripts/`、`tests/` 和审计日志都会进入图谱。
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
