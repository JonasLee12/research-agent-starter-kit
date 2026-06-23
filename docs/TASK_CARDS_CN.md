# 任务卡：选择你的工作流

当你知道自己想做什么，但不知道该让 research agent 走哪条流程时，先看这页。

这个设计借鉴的是“任务中心”的产品形态：先把任务说清楚，提前收集必要输入，显示大概会走轻量还是完整流程，并记录任务状态。它不是论文代写平台。下面的任务卡必须保留本 starter kit 的 source-first、学术/专业诚信、citation、privacy 和 delivery 边界。

## 不要用这个 Kit 做这些事

不要为以下任务创建或改造任务卡：

- 代写 thesis、dissertation、paper、proposal、report 或 assignment；
- 降重、隐藏复制文本，或规避查重；
- 降 AI、规避 AI detector、优化 detector score、操纵 authorship verdict；
- 编造 citations、data、participants、supervisor feedback、institutional requirements 或 source support；
- 在没有 source check、用户判断和作者边界的情况下，把 reviewer/supervisor comments 直接改成最终作者文本；
- 在这个非商业 starter kit 里加入付费转售、积分池、支付、代理分销工作流。

## 任务状态

可以在 task-state、receipt index 或 dashboard 里使用这些状态：

| Status | 意思 |
|---|---|
| `submitted` | 任务 intake 已定义，但还没开始做。 |
| `running` | agent 正在读文件、检查、起草、渲染或验证。 |
| `blocked` | 缺证据、缺用户确认、缺凭据或 gate 失败，暂时不能继续。 |
| `needs_confirmation` | 需要用户决定边界、source、输出类型或 override。 |
| `completed` | 请求的输出和必要检查已完成。 |
| `failed` | 工具、检查或动作尝试失败。 |
| `cancelled` | 用户或维护者明确停止任务。 |

## 先做 Intake

使用任何任务卡前，先填写或复制 [`templates/SOURCE_FIRST_INTAKE_CARD.md`](../templates/SOURCE_FIRST_INTAKE_CARD.md)。不知道的事实保留 `TO CONFIRM`，不要让 agent 凭记忆补。

最低 intake：

- task goal；
- target artifact；
- allowed source corpus；
- evidence/citation boundary；
- output surface；
- privacy/compliance constraints（隐私/合规边界）；
- expected route：bounded、standard 或 full；
- status label。

## 路由层级

| Route | 适用情况 | 不适用情况 |
|---|---|---|
| `bounded` | source lookup、source-section verification、source planning、citation-key 修复、reference-format 修复、typo repair，或其他不改变实质内容的小任务。 | 正式正文、Word/PDF 交付、stakeholder-facing 输出、protected source-of-record 编辑、引用就绪升级、method/design 变更。 |
| `standard` | source-register 更新、可见页面检查、维护、public sync、dashboard/status 更新、结构化知识库工作。 | 代写、降重、降 AI、规避 detector、编造 source support，或没有已 review 证据的 source-readiness 升级。 |
| `full` | 正式正文、Word/PDF 交付、stakeholder/submission-facing 输出、protected source-of-record 编辑、method/design/ethics 变更，或高风险 Stage Continuity 任务。 | 任何要求跳过 source check、写无证据最终作者文本、隐藏 AI 使用、编造证据，或把 intake 当 citation proof 的请求。 |

## 任务卡

### 1. Project Setup / Profile Card

适用：把 starter kit 适配为 thesis、article、report、grant、review 或其他研究项目。

需要输入：

- 项目类型；
- 已确认标题或 working topic；
- 已有 source folders；
- 不能公开的 private folders；
- 预期输出类型。

建议路线：`standard`

使用：

- `PROJECT_TYPE_PROFILES.md`
- `RESEARCH_PROJECT_BRIEF_TEMPLATE.md`
- `templates/AGENTS.example.md`

输出：

- 适配后的 `AGENTS.md`；
- 保留 `TO CONFIRM` 的 project brief；
- 首轮 validation。

### 2. Literature Search / Source Discovery Card

适用：寻找候选文献、规划检索词。

需要输入：

- research question 或 topic；
- 允许使用的数据库或网页来源；
- 日期/语言限制；
- inclusion/exclusion criteria；
- candidate notes 存放位置。

建议路线：`bounded`

必要边界：

- 搜索结果在 source section review 前都是 `METADATA ONLY`。

输出：

- search log；
- candidate list；
- next-reading priority；
- 不做 citation-ready（引用就绪）升级，除非 source section 已 review。

### 3. Source-Section Verification Card

适用：检查某个 source 是否支持某个 claim 或 section。

需要输入：

- source path 或 citation；
- 需要核查的 claim/section；
- 已知 page/section；
- 当前 source-readiness status；
- 允许输出的位置。

建议路线：`bounded`

输出：

- support status：direct support、partial support、background only、metadata only、insufficient evidence；
- cannot-prove boundary；
- 只有确认 source support 后，才给 allowed wording。

### 4. Source Register / Readiness Update Card

适用：更新 source register、readiness matrix 或 bibliography tracker。

需要输入：

- source note path；
- 已 review 的 evidence；
- metadata fields；
- requested status change；
- 变更理由。

建议路线：`standard`

必要边界：

- metadata、abstract、保存的 PDF 或搜索结果本身不能让 source 变成 citation-ready。

输出：

- 更新后的 source register/readiness matrix；
- status evidence path；
- residual risk 或 `TO CONFIRM`。

### 5. Formal Draft Planning Card

适用：准备正式 section、report、proposal、methodology、literature review 或 stakeholder-facing draft。

需要输入：

- target section/artifact；
- allowed source corpus；
- claim-support policy；
- audience；
- output format；
- 必须继承的 upstream decisions。

建议路线：`full`

必要 gates：

- source-first；
- Material Passport；
- cognitive protocol；
- integrity preflight；
- 触发时运行 Stage Continuity。

输出：

- section plan、source map 和 drafting boundary；
- 如证据不足，不交付正式正文。

### 6. Formal Draft Review / Revision Card

适用：审查或修改已有正式文本。

需要输入：

- draft path；
- review purpose；
- allowed change scope；
- citation/claim-support status；
- 是否 supervisor-facing、stakeholder-facing 或 submission-facing。

建议路线：`full`

必要 gates：

- claim 改变时先 source-first；
- academic integrity；
- self-review loop；
- authorial voice 和 style fingerprint；
- document-quality gate。

输出：

- revision queue；
- 只有 source 和作者边界清楚时才给 revised draft；
- residual risks。

### 7. Method / Instrument / Design Continuity Card

适用：改变或产出 method plan、research questions、interview guide、concept card、analysis plan 或 design decision。

需要输入：

- target artifact；
- upstream source-of-record files；
- 不能静默改变的 decisions；
- ethics/compliance constraints；
- open confirmations。

建议路线：`full`

必要 gates：

- Token-Aware Recall；
- Stage Continuity Capsule；
- source-first；
- participant-facing 或 fieldwork-facing 时加 responsible/ethics checks。

输出：

- continuity capsule；
- design decision summary；
- next action 或 user confirmation request。

### 8. Word / DOCX Delivery Card

适用：生成、修改或交付 Word/PDF。

需要输入：

- source Markdown/doc；
- target `.docx` 或 `.pdf`；
- previous accepted baseline；
- output audience；
- style/template constraints。

建议路线：`full`

必要 gates：

- pre-delivery lock；
- formal delivery guard；
- Markdown-DOCX structure check；
- DOCX layout review；
- Visible Output QA。

输出：

- deliverable artifact；
- delivery checkpoint；
- visible-output verdict；
- 如接受风险，必须有 override record。

### 9. Visible Surface / Public Release Card

适用：检查 GitHub README、release、公开页面、figure、Obsidian view 或 browser surface。

需要输入：

- visible URL 或 artifact path；
- communication job；
- baseline；
- privacy boundary。

建议路线：`standard`

必要 gates：

- Visible Output QA；
- GitHub/public release 使用 release-surface verification；
- 公开分享前 privacy check。

输出：

- source-layer status；
- rendered/visible status；
- remaining `TO VERIFY` items。

### 10. Agent Maintenance / Runtime Guard Card

适用：检查 agent failure、runaway logs、stale receipts、routing drift、automation 问题或 dirty working tree。

需要输入：

- symptom；
- affected files/tools；
- 是否允许写操作；
- backup/rollback boundary。

建议路线：`standard`

必要 gates：

- 相关时运行 runtime/session-log integrity checks；
- `logs_*.sqlite` 增长时使用 Codex SQLite log guard；
- public sync 前 privacy check；
- Git staging 必须按文件路径显式添加，不能 `git add -A`。

输出：

- diagnosis；
- applied fix 或 audited risk；
- validation result；
- clean 或 classified Git status。

## 可直接复制的提示词

```text
请使用 Task Cards workflow。先选择最小合适的任务卡，再只问缺失的 intake 字段。source-first 和 integrity 边界没清楚前，不要写正式正文。
```
