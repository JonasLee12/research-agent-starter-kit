# External Review Options

Language: English | 中文说明见下方

## Core Rule

External review is optional and advisory. It is not evidence, not source support, not compliance approval, not a grade, and not a delivery pass.

You do not need Claude Code to use this starter kit. The default quality path is still local:

1. source-first checks;
2. cognitive protocol;
3. academic self-review loop;
4. integrity preflight;
5. document-quality and delivery gates.

External review is an extra second opinion after those local checks.

## Three Review Paths

| Path | Requires | Best For | Boundary |
|---|---|---|---|
| Local self-review | Codex and local project files | Default workflow for every user | Runs inside your project rules; still needs source checks |
| Manual external-review bundle | Any separate Codex, ChatGPT, Claude, Gemini, or human reviewer | Users without Claude Code or users who want a visible copy/paste workflow | Bundle is local until you choose to paste it elsewhere |
| Claude Code runner | Claude Code installed and available | Users who already have Claude Code and want a direct wrapper | Advisory only; not required |

## Path 1: Local Self-Review

Use the built-in self-review workflow first. It checks writing quality and revision priorities without sending the artifact to another service.

For formal research writing, the project should route through:

- `cognitive-frameworks`;
- `academic-self-review-loop`;
- `academic-integrity-preflight`;
- `dissertation-document-quality-gate`.

## Path 2: Manual Review Bundle For Codex / ChatGPT / Claude / Gemini

Build a local review bundle:

```bash
python3 scripts/build_external_review_bundle.py path/to/draft.md
```

The script creates a folder under `.agent-runtime/external-review-bundles/`.

Open the generated folder and inspect:

- `privacy_scan.md`;
- `artifact.md`;
- `EXTERNAL_REVIEW_PROMPT.md`;
- `manifest.json`.

If the privacy scan is acceptable, copy `EXTERNAL_REVIEW_PROMPT.md` into a separate Codex window, ChatGPT chat, Claude chat, Gemini chat, or give it to a human reviewer.

The bundle builder does not call an LLM, does not connect to the internet, and does not upload files.

## Path 3: Claude Code Runner

If Claude Code is installed and available, you can run:

```bash
python3 scripts/claude_independent_review.py path/to/draft.md
```

This is one optional runner for the same external-review role. Claude feedback is advisory and must become a revision queue. It does not replace local source, privacy, citation, compliance, or delivery gates.

## Sensitive Material

The bundle builder and Claude runner block common sensitive content by default, including participant-related text, interview material, consent language, emails, private paths, tokens, and credentials.

If a sensitive item is blocked, use an anonymised draft. Only use override flags when you explicitly accept the risk.

## 中文

## 核心规则

External review 是可选的建议层。它不是证据、不是 source support、不是合规批准、不是分数，也不是正式交付通过。

这套 starter kit 不需要 Claude Code。默认质量流程仍然是本地流程：

1. source-first checks；
2. cognitive protocol；
3. academic self-review loop；
4. integrity preflight；
5. document-quality and delivery gates。

External review 只是这些本地检查之后的额外第二意见。

## 三种质审路径

| 路径 | 需要什么 | 适合什么情况 | 边界 |
|---|---|---|---|
| 本地 self-review | Codex 和本地项目文件 | 所有用户的默认流程 | 在本地项目规则内运行，但仍需要 source checks |
| 手动 external-review bundle | 另一个 Codex、ChatGPT、Claude、Gemini 或人工 reviewer | 没有 Claude Code 的用户，或想要可见复制粘贴流程的用户 | bundle 只在本地生成，除非你主动复制出去 |
| Claude Code runner | 已安装并可用的 Claude Code | 已有 Claude Code 的用户 | 只提供建议，不是必需工具 |

## 路径一：本地 Self-Review

先使用内置 self-review workflow。它可以在不发送给外部服务的情况下检查写作质量和修改优先级。

正式研究写作通常应经过：

- `cognitive-frameworks`；
- `academic-self-review-loop`；
- `academic-integrity-preflight`；
- `dissertation-document-quality-gate`。

## 路径二：给 Codex / ChatGPT / Claude / Gemini 的手动 Review Bundle

生成本地质审包：

```bash
python3 scripts/build_external_review_bundle.py path/to/draft.md
```

脚本会在 `.agent-runtime/external-review-bundles/` 下创建一个文件夹。

打开生成的文件夹，检查：

- `privacy_scan.md`；
- `artifact.md`；
- `EXTERNAL_REVIEW_PROMPT.md`；
- `manifest.json`。

如果隐私扫描可以接受，把 `EXTERNAL_REVIEW_PROMPT.md` 复制到另一个 Codex 窗口、ChatGPT、Claude、Gemini，或交给人工 reviewer。

这个 bundle builder 不调用 LLM，不联网，也不上传文件。

## 路径三：Claude Code Runner

如果你已经安装并能使用 Claude Code，可以运行：

```bash
python3 scripts/claude_independent_review.py path/to/draft.md
```

这只是同一个 external-review 角色的一个可选 runner。Claude feedback 只能作为 revision queue，不能替代本地 source、privacy、citation、compliance 或 delivery gates。

## 敏感材料

Bundle builder 和 Claude runner 默认会拦截常见敏感内容，包括 participant 相关文本、interview material、consent language、emails、private paths、tokens 和 credentials。

如果内容被拦截，优先使用匿名化草稿。只有在你明确接受风险时，才使用 override flags。
