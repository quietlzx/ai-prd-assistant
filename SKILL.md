---
name: ai-prd-assistant
description: 将原始产品需求通过确定性串行流程转换为结构化 Brief、Gate 判定、PRD、AI 风险清单、人工审核记录和单文件 HTML 报告。适用于整理需求、生成或评审 PRD、分析 AI 产品风险，以及校验 AI 产品交付物结构。
license: MIT
metadata:
  short-description: 分阶段 PRD 与 AI 风险工作流
  version: "0.2.0"
  framework-version: "v1.0-framework"
---

# AI PRD Assistant

把未整理的产品需求转换为可审核的 PRD 交付包。流程必须串行执行，避免后续阶段继承完整对话中的注意力漂移。

## 固定工作流

按以下顺序执行：

1. 输入归一化：只生成结构化 Brief。
2. 需求校验：生成歧义清单和一个 Gate 结论。
3. PRD 生成：消费已校验的 Brief，并按模板生成 PRD。
4. AI 风险识别：按六大风险类别分析 Brief 与 PRD。
5. 人工审核门禁：等待 `review_state=approved` 后再组装报告。
6. 报告组装：生成 Markdown 和单文件 HTML。

第 1 至第 4 阶段是生产阶段。人工审核是位于 AI 风险识别和报告组装之间的控制门禁。

## 状态模型

流水线主状态只能使用：

- `RUNNING`
- `READY`
- `DRAFT_WITH_GAPS`
- `BLOCKED`
- `HARNESS_FAILED`

人工审核状态单独存储在 `review_state`：

- `pending`
- `approved`
- `rejected`
- `revision`

禁止把审核状态加入流水线主状态枚举。

## Gate 规则

- 关键缺口或硬冲突输出 `BLOCKED`。
- `BLOCKED` 只输出澄清问题并终止。
- 非关键缺口输出 `DRAFT_WITH_GAPS`。
- `DRAFT_WITH_GAPS` 可以继续执行，未决事项标记为 `[待确认:Gxx]`。
- 信息充足时输出 `READY`。
- `HARNESS_FAILED` 记录失败后立即终止，不得重试或进入下一阶段。
- 人工审核不能把 `BLOCKED` 或 `HARNESS_FAILED` 转为通过。
- 人工审核不能把 Gate 升级为 `READY`。

## 阶段契约

每个阶段必须写入结构化产物。下游阶段读取产物文件，不读取完整对话。

```text
run.json
01_brief.json
02_validation.json
03_prd.md
04_ai_risks.md
04_review_packet.json
04_human_review.json
05_report.md
05_report.html
```

统一使用以下来源标记：

- `[来源]`：用户输入直接支持的内容。
- `[推断]`：为完成设计而进行的必要推断。
- `[假设]`：为继续流程而采用的临时假设。
- `[待确认:Gxx]`：引用末尾集中管理的未决事项。

禁止编造公司事实、制度值、指标、角色、权限或模型能力。未决信息必须进入附录，不能静默补全。

## PRD 要求

每个能力必须定义：

- 用户目标
- 输入
- 处理规则
- 输出
- 失败状态
- 边界条件
- 验收标准

所有未决事项必须集中到末尾章节 `附录 A：待确认事项清单`。每项必须包含可选方案、业务影响、开发影响、推荐方案、决策人和 Gate 影响。

生成或修订 PRD 时，阅读 [references/prd-template.md](references/prd-template.md)。

## 风险要求

必须分析以下六大类别：

1. 事实幻觉与错误引用。
2. 模型能力边界。
3. 输入歧义与数据质量。
4. 错误传播与自动化失控。
5. 人机确认与责任边界。
6. 评测、监控与回滚。

每条风险必须包含：

`风险编号｜类别｜触发条件｜影响｜当前控制｜降级方案｜验证方法｜状态`

生成 AI 风险清单时，阅读 [references/risk-taxonomy.md](references/risk-taxonomy.md)。

## 人工审核

在第 4 阶段之后、第 5 阶段之前：

1. 冻结当前产物版本。
2. 生成审核包。
3. 设置 `review_state=pending`。
4. 等待 `approved`、`rejected` 或 `revision`。
5. 收到 `revision` 后，回到受影响的生产阶段并重新生成审核包。
6. 收到 `rejected` 后，保留产物并终止。
7. 收到 `approved` 后，锁定版本并进入报告组装。

完整流转契约见 [references/workflow.md](references/workflow.md)。

## 报告组装

基于审核通过的版本生成 Markdown 和一个单文件 HTML。HTML 不得依赖外部脚本、样式或网络资源。

组装最终报告前，阅读 [references/output-contract.md](references/output-contract.md)。

## Harness

使用确定性校验工具：

```bash
python scripts/harness.py validate <运行目录>
python scripts/harness.py self-test
```

Harness 只校验结构、阶段顺序、字段存在性、状态值、审核状态和产物引用。它不判断产品需求或 PRD 内容的业务质量。
