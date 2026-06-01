# Obsidian Setup

Language: English | 中文说明见下方

## English

## The Most Important Rule

Open knowledge-base/ as your Obsidian vault. Do not open the repository root.

If you open the whole repository root, Obsidian will index every Markdown file in the starter kit. Your graph will include system notes, scripts, tests, audit files, templates, runtime receipts, README files, and skill documentation. That is useful for maintaining the agent, but it is not a clean research knowledge base.

## Recommended Entry Points

| Choice | Open This Folder In Obsidian | Use When |
|---|---|---|
| Simple project vault | `knowledge-base/` | You want to browse sources, readiness notes, and the self-growing knowledge base inside this repository. |
| Clean personal vault | A copied version of `templates/obsidian-vault/` outside this repository | You want a tidy research notebook separated from the agent system files. |
| Do not use | Repository root | This pollutes the graph with system and maintenance files. |

## What Belongs In The Research Knowledge Layer

Use the knowledge layer for:

- source registers and source-readiness notes;
- source summaries and reading notes;
- literature clusters;
- methodology decisions;
- proposal planning notes;
- research tasks and next-reading queues;
- non-sensitive attachments you intentionally add.

The canonical source-of-record still stays in project files such as:

- `knowledge-base/SOURCE_REGISTER.md`;
- `knowledge-base/SOURCE_READINESS_MATRIX.md`;
- source notes under `knowledge-base/sources/`;
- compiled knowledge notes under `knowledge-base/self-growing/compiled-wiki/`.

Obsidian helps you navigate these files. It does not make a source citation-ready, and it does not replace source-section review.

## What Should Stay Out Of The Obsidian Vault

Do not treat these folders as research knowledge nodes:

- `research-wiki/` system memory, maintenance notes, and runtime policies;
- `scripts/` local helper scripts;
- `tests/` validation tests;
- `audit-reports/` review outputs;
- `.agents/skills/` operating instructions;
- `.agent-runtime/` generated local state;
- runtime receipts, skill-eval runs, vector smoke-test reports, and other generated logs.

These files can be useful for maintaining the agent, but they should not appear in a clean research graph.

## Option 1: Open `knowledge-base/`

1. Close any currently open Obsidian vault.
2. Open Obsidian.
3. Choose **Open folder as vault**.
4. Select the repository's `knowledge-base/` folder.
5. Do not select the repository root.

This gives you a project-linked vault without indexing system folders such as `scripts/` or `tests/`.

## Option 2: Copy The Clean Vault Template

1. Copy `templates/obsidian-vault/` to a location outside this repository.
2. Rename the copied folder for your own project.
3. Open the copied folder in Obsidian.
4. Add your own research notes there.
5. Keep private material in `09_Private_Data_DO_NOT_SYNC/` and do not push that folder to GitHub.

The template is intentionally generic. It does not contain dissertation content, institution names, supervisor details, email addresses, participant data, screenshots, or private documents.

## Privacy Boundary

Before moving material into an Obsidian vault, check whether it contains:

- private personal information;
- email addresses;
- participant data;
- private institutional guidance;
- assessment drafts;
- screenshots from private systems;
- raw interview material;
- consent forms or signatures;
- local paths, tokens, or credentials.

Keep private material outside public repositories unless you have explicitly decided it is safe to share.

## 中文

## 最重要的规则

请把 knowledge-base/ 作为 Obsidian vault 打开，不要打开整个仓库根目录。

如果你把整个仓库根目录作为 vault，Obsidian 会索引仓库里的所有 Markdown 文件。这样图谱里会出现系统说明、脚本、测试、审计文件、模板、runtime receipt、README 和 skill 文档。这对维护 agent 有用，但不是干净的研究知识库。

## 推荐入口

| 方案 | 在 Obsidian 中打开哪个文件夹 | 适合什么情况 |
|---|---|---|
| 简单项目 vault | `knowledge-base/` | 想直接查看 source register、source-readiness 和 self-growing knowledge base。 |
| 干净个人 vault | 把 `templates/obsidian-vault/` 复制到仓库外部后打开副本 | 想要一个和 agent 系统文件分离的研究笔记库。 |
| 不要使用 | 仓库根目录 | 会把系统文件和维护文件全部放进图谱。 |

## 哪些内容属于研究知识层

适合放入知识层的内容：

- source register 和 source-readiness notes；
- source summaries 和 reading notes；
- literature clusters；
- methodology decisions；
- proposal planning notes；
- research tasks 和 next-reading queues；
- 你明确想放入的非敏感附件。

真正的 source-of-record 仍然是项目文件，例如：

- `knowledge-base/SOURCE_REGISTER.md`；
- `knowledge-base/SOURCE_READINESS_MATRIX.md`；
- `knowledge-base/sources/` 下的 source notes；
- `knowledge-base/self-growing/compiled-wiki/` 下的 compiled knowledge notes。

Obsidian 只是阅读和导航层。它不能让某篇文献自动变成 citation-ready，也不能替代 source-section review。

## 哪些内容不应该进入 Obsidian 研究图谱

不要把这些文件夹当成研究知识节点：

- `research-wiki/` 系统记忆、维护记录和 runtime policies；
- `scripts/` 本地 helper scripts；
- `tests/` validation tests；
- `audit-reports/` review outputs；
- `.agents/skills/` agent 操作说明；
- `.agent-runtime/` 生成的本地状态；
- runtime receipts、skill-eval runs、vector smoke-test reports 和其他生成日志。

这些文件对维护 agent 有用，但不应该出现在干净的研究图谱里。

## 方案一：打开 `knowledge-base/`

1. 关闭当前已打开的 Obsidian vault。
2. 打开 Obsidian。
3. 选择 **Open folder as vault**。
4. 选择仓库里的 `knowledge-base/` 文件夹。
5. 不要选择仓库根目录。

这样可以直接查看项目知识库，同时避免 `scripts/`、`tests/` 等系统文件进入图谱。

## 方案二：复制干净 vault 模板

1. 把 `templates/obsidian-vault/` 复制到仓库外部。
2. 给复制后的文件夹改成你自己的项目名。
3. 用 Obsidian 打开复制后的文件夹。
4. 在里面加入自己的研究笔记。
5. 私人材料只放在 `09_Private_Data_DO_NOT_SYNC/`，不要把这个文件夹推送到 GitHub。

这个模板是通用模板。它不包含 dissertation 内容、学校名称、导师信息、邮箱、参与者数据、截图或私人文档。

## 隐私边界

把材料放进 Obsidian vault 前，先检查是否包含：

- 私人身份信息；
- 参与者数据；
- 非公开学校或机构说明；
- assessment drafts；
- 私有系统截图；
- 原始访谈材料；
- consent forms 或签名；
- 本机路径、tokens 或 credentials。

除非你明确确认安全，否则不要把私人材料放进公开仓库。
