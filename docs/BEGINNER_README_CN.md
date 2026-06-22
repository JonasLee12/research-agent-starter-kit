# 新手 README：完全不熟悉 Codex 和 GitHub 也可以开始

这份指南写给第一次接触 Codex、GitHub 和 research-agent 工作流的人。

你不需要先看懂仓库里的每一个文件。这个 starter kit 的作用，是给 AI coding agent 一个本地项目工作区，让它按规则读文件、查证据、做检查，而不是只生成一段看起来流畅的文字。

## 这个仓库是什么

这是一个本地优先的 research-agent starter kit。

它可以帮助 AI coding agent：

- 写作前先读项目规则；
- 下判断前先查 source；
- 小任务走轻量流程；
- 重要检查留下证据；
- 帮助在交付前标出薄弱的正式 Word/PDF 或 stakeholder-facing 输出；
- 避免把私人研究材料泄露到公开 GitHub。

它不是一篇已经完成的 dissertation、thesis、paper、report 或 app。你需要把它改成适合自己项目的版本。

## 你需要准备什么

最低要求：

- 一台电脑；
- Python 3.9 或更新版本；
- 一个可以读本地文件的 coding agent，例如 Codex、Claude Code、Cursor 或类似工具。

可选但有帮助：

- GitHub 账号；
- 本地安装 Git；
- Obsidian，如果你喜欢可视化笔记；
- Claude Code，如果你想要额外的独立 review。

如果你还不会 Git，也可以先把这个仓库当作一套本地文件和检查清单来用。

## 最简单的开始方式

1. 下载或 clone 这个仓库。
2. 在 Codex 或其他 coding agent 中打开这个文件夹。
3. 先读 `README_CN.md`。
4. 如果是新项目，把 `templates/AGENTS.example.md` 复制成 `AGENTS.md`。
5. 只填写已经确认的项；不确定的项保留 `TO CONFIRM`。
6. 让 agent 先跑基础检查，不要一上来就写正式正文。

可以直接这样问：

```text
请先读取 AGENTS.md、PROJECT_AGENT_PREFERENCES.md 和 RESEARCH_PROJECT_BRIEF_TEMPLATE.md。
帮我把这个 starter kit 适配到我的项目。
先不要写正式正文，先告诉我哪些项目事实和 source 文件还需要 TO CONFIRM。
```

## 如果你不懂 GitHub

可以先把 GitHub 理解成一个在线项目备份和分享平台。

几个基础词：

| 词 | 意思 |
|---|---|
| Repository / repo | 被 Git 管理的项目文件夹 |
| Commit | 一次保存下来的文件变更快照 |
| Push | 把本地 commit 上传到 GitHub |
| Pull | 把 GitHub 上的新变化下载到本地 |
| Branch | 一条单独的工作线 |
| Pull request | 用来 review 和合并分支的页面 |

如果你是新手，不要把私人研究数据 push 到公开 GitHub。raw data、transcripts、participant records、账号凭据、学校/机构内部材料，都应该留在公开仓库外。

公开分享前先运行：

```bash
bash scripts/privacy_check.sh
```

然后人工检查 `PRIVACY_CHECKLIST.md`。

## 如果你不懂 Codex

Codex 是一个 AI coding agent。你可以让它读文件、改规则、跑检查、整理项目记忆、生成研究工作流文档。

真正的执行边界来自本地项目规则和 Python 检查，例如 `AGENTS.md` 和 `scripts/`；agent 的作用是读取、运行并遵守这些规则。

比较好的新手提示词：

```text
请先分类这个任务，再行动。告诉我你需要先读哪些文件。
```

```text
请先为这个任务运行 runtime preflight，并解释它是 bounded task 还是 formal-writing task。
```

```text
请检查这个 source 现在是 metadata-only、partly reviewed，还是 citation-ready。没有 source-section review 不要升级状态。
```

```text
请只在完成 source-first、claim-support、integrity 和 document-quality 检查后，再准备正式文档。
```

尽量避免这种模糊指令：

```text
帮我改到最好。
```

更好的方式是说明：这个输出给谁看、用途是什么、可以用哪些 source、哪些地方不能改。

## 最重要的文件

| 文件 | 作用 |
|---|---|
| `AGENTS.md` | agent 必须遵守的主规则 |
| `PROJECT_AGENT_PREFERENCES.md` | 你的项目偏好和边界 |
| `RESEARCH_PROJECT_BRIEF_TEMPLATE.md` | 项目说明模板 |
| `PROJECT_TYPE_PROFILES.md` | 判断项目类型：论文、报告、grant、evidence synthesis 等 |
| `knowledge-base/SOURCE_READINESS_MATRIX.md` | 记录 source 是 metadata-only、partly reviewed，还是可以引用 |
| `research-wiki/TASK_STATE.md` | 项目记忆和当前状态 |
| `research-wiki/STAGE_GRAPH.md` | 帮助后续阶段回顾前面阶段的重要决定 |
| `research-wiki/CLAIM_LEDGER_LITE_PROTOCOL.md` | 防止正式 claim 超出证据能支持的范围 |
| `research-wiki/VISIBLE_OUTPUT_QA_PROTOCOL.md` | 要求检查用户真正看到的输出，而不只是检查文件是否生成 |

## 三种常见任务

### 1. Bounded Task

小任务，应该保持轻量。

例如：

- 查一篇 paper 有没有可用章节；
- 修 citation key；
- 给阅读 source 排优先级；
- 总结现在缺什么。

这类任务不应该自动进入完整 formal-writing chain，除非任务变成正式写作或修改受保护文件。

### 2. Formal Writing Task

高风险任务，需要完整检查。

例如：

- 写正式段落；
- 改 thesis / dissertation 章节；
- 准备 report section；
- 写 stakeholder-facing 文档。

agent 应该做 source-first、claim boundary、integrity check、self-review、style check 和 document-quality gate。

### 3. Visible Delivery Task

用户或读者会看到渲染后的输出。

例如：

- Word 文档；
- PDF；
- figure；
- GitHub README；
- Obsidian graph/page；
- browser page。

这时要用 Visible Output QA。文件存在不等于读者看到的页面是好的。

## 安全使用习惯

- 不要把私人数据放进公开 GitHub。
- 不要让 agent 编造 citation 或事实。
- 搜索结果只是候选，不是证据。
- 没有确认的事实保留 `TO CONFIRM`。
- 用 commit 保存工作节点。
- 重大更新后先跑验证再信任。

## 基础验证

设置或大改后，运行：

```bash
python scripts/run_skill_evals.py
python scripts/validate_agent_schemas.py
python scripts/session_log_integrity_check.py --strict --no-report
python scripts/borrowed_pattern_boundary_lint.py --no-report
python -m unittest discover -s tests
bash scripts/privacy_check.sh
```

如果你不会运行命令，可以直接问 Codex：

```text
请帮我运行这个 starter kit 的基础验证命令，并用普通语言解释结果。
```

## 非商业许可

本仓库使用 PolyForm Noncommercial License。允许个人学习、教育和非商业研究使用。未经书面许可，不允许商业使用、转售、付费托管/SaaS、付费培训、咨询产品化，或作为付费产品的一部分再分发。

在分享或复用到个人/教育以外的场景前，请先阅读 `LICENSE`。

## 第一天检查清单

- [ ] 下载或 clone 仓库。
- [ ] 用 Codex 或其他 coding agent 打开。
- [ ] 阅读这份指南和 `README_CN.md`。
- [ ] 创建或自定义 `AGENTS.md`。
- [ ] 只填写已确认的项目事实。
- [ ] 私人材料不要放进公开 GitHub。
- [ ] 运行基础验证命令。
- [ ] 第一个正式任务前，让 agent 先分类任务，不要直接开写。
