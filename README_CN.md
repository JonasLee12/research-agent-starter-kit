# Research Agent Starter Kit

一个本地、文件驱动的 research-project Agent starter kit，包含认知推理、写作质量自审和交付 gate。

[English README](README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3](https://img.shields.io/badge/Python-3-green.svg)](https://www.python.org/)
[![Evals](https://img.shields.io/badge/Skill_Evals-17%2F17_passing-brightgreen.svg)](#validation)

## 这是什么？

这是一个用于搭建本地 AI research agent 的 starter kit，可用于 dissertation、thesis、article、report、proposal 和其他正式研究项目。它适合希望使用 AI 辅助研究写作，同时仍然保持 source integrity、ethical compliance 和 writing quality 的用户。

系统提供三层质量控制：

1. **Cognitive reasoning** — 正式写作前先做 argument mapping、gap classification 和 warrant testing。
2. **Self-review loop** — 初稿后必须经过两轮 review-revise：找弱点、修改、再重新判断。
3. **Delivery gates** — 正式输出前检查 source verification、citation audit 和高质量交付 readiness。

核心工作流基于本地文件和 Python 脚本运行。默认不依赖 hosted service，也不需要 API dependency 才能使用核心流程。

最新版还加入了 runtime routing 回归测试、带隐私 gate 的 Claude Code 独立 review wrapper、可选的高质量科研图/写作 skills，以及 weekly literature gap-watch automation 模板。

## 架构

完整系统架构图请参见 [docs/architecture.md](docs/architecture.md)。

系统分成七层：

| Layer | Purpose | Key files |
|---|---|---|
| Rules | 定义 agent 如何工作 | `AGENTS.md`, `PROJECT_AGENT_PREFERENCES.md`, `.agents/skills/` |
| Task routing | 判断任务、选择 skills 和 gates | `agent-orchestration` skill, `scripts/agent_runtime.py` |
| Evidence | 管理 sources、ethics、rubric、citation readiness | `knowledge-base/`, `ethics/`, `university-guidance/` |
| Writing & delivery | 管理 draft、style、quality、delivery review | `DOCUMENT_PIPELINE.md`, delivery scripts |
| Memory | 跨 session 保存项目状态 | `TASK_STATE.md`, `USER_DASHBOARD.md`, `AGENT_MEMORY_STATUS.md` |
| Tools | 本地脚本、Zotero、Obsidian、retrieval、browser | `scripts/`, `.agent-runtime/` |
| Audit | 检查 Production runs 是否认真执行 | automations, system audits, runtime receipts |

## 快速开始

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

## 核心功能

| Feature | What it does |
|---|---|
| Source-first gate | 写正式事实前先查文件证据，减少编造 |
| Cognitive frameworks | 正式写作前强制做 argument mapping、gap classification、warrant testing |
| Academic self-review loop | 初稿后两轮自审：identify weaknesses → revise → fresh re-review |
| Writing quality rubric | 用六项内部标准检查段落和论证质量 |
| Staged checkpoints | 三阶段 pipeline：THINKING → WRITING → DELIVERY |
| Delivery guard | 缺少 pre-delivery lock、citation audit 或 delivery review 时阻止正式输出 |
| Retrieval protocol | 四层检索：semantic / keyword / source readiness / human source review |
| Dual-window workflow | Production Window 写作，Maintenance Window 维护；通过文件共享状态 |
| Audit trail | event log、runtime receipts、Production audits |
| External integration | OpenAlex、Crossref、Semantic Scholar metadata discovery；Zotero reference management |
| Claude review wrapper | 可选的 Claude Code 独立 review；有隐私 gate，反馈只作为建议，不是证据 |
| Research figure/writing skills | 可选 `research-*` skills，用于 neural-network figures、高质量科研图和 article-style prose |
| Literature gap-watch automation | weekly candidate-only 文献监测模板，带 Stage A/B/C 和 source-readiness 边界 |

## 自定义

### 添加你的学校材料

把 marking criteria 和 module requirements 放在 `university-guidance/`。格式参考 `university-guidance/EXAMPLE_RUBRIC_GUIDE.md`。

### 添加你自己的 skill

在 `.agents/skills/your-skill-name/` 下创建 `SKILL.md`，并在 `research-wiki/SKILL_EVAL_REGISTRY.md` 注册 eval test cases。具体要求见 [CONTRIBUTING.md](CONTRIBUTING.md)。

### 配置 Zotero

参考 `research-wiki/ZOTERO_AND_CITATION_WORKFLOW_SPEC.md`。

### 调整 cognitive frameworks

你可以修改 `.agents/skills/cognitive-frameworks/SKILL.md`，让 gap type、warrant quality tests 或 rhetorical moves 更适合你的学科。

## 这套系统不能做什么

- 不能自动证明某个 source 支持某个具体 claim；它只能生成 audit queue，仍需人工 source review。
- 不能直接访问 Scopus、Web of Science、EBSCO 等订阅数据库；这些需要合法机构凭据。
- 不能替代 ethics approval；它只能追踪 readiness，最终仍需 supervisor 或 ethics committee 判断。
- 不能保证分数、录用、资助或正式批准。
- 不能阻止你绕过 agent pipeline 手动复制文件。
- 不能替代 supervisor judgement、peer review 或 academic integrity 要求。

## Validation

系统内置验证：

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

## 文档

- [Dual Window Guide](docs/DUAL_WINDOW_GUIDE.md) — Production 和 Maintenance 窗口如何分工
- [Skill Development Guide](docs/SKILL_DEVELOPMENT_GUIDE.md) — 如何创建和测试新的 skill
- [Weekly Literature Gap-Watch Automation](docs/WEEKLY_LITERATURE_GAP_WATCH_AUTOMATION.md) — candidate-only weekly 文献监测
- [Retrieval Protocol](research-wiki/RETRIEVAL_PROTOCOL.md) — 四层 retrieval 如何协同
- [Document Pipeline](research-wiki/DOCUMENT_PIPELINE.md) — staged checkpoint delivery process

## Acknowledgements

开源项目和方法来源见 [ACKNOWLEDGEMENTS.md](ACKNOWLEDGEMENTS.md)。

## License

[MIT](LICENSE)
