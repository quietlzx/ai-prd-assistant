# AI PRD Assistant

AI PRD Assistant 是一个 Codex Skill，用于把原始产品需求转换为结构化、可审核的 PRD 交付包。

它采用串行工作流、明确的 Gate 判定、阶段化产物、人工审核门禁和确定性的结构校验 Harness。

## 工作流

```text
输入归一化
→ 需求校验
→ PRD 生成
→ AI 风险识别
→ 人工审核
→ 报告组装
```

前四个阶段负责生产工作产物。人工审核是位于 AI 风险识别和最终报告组装之间的控制门禁。

## 输出产物

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

最终 HTML 报告为单文件，不依赖外部脚本、样式、字体或网络资源。

## 状态模型

流水线主状态：

```text
RUNNING
READY
DRAFT_WITH_GAPS
BLOCKED
HARNESS_FAILED
```

人工审核状态：

```text
pending
approved
rejected
revision
```

`review_state` 不会改变流水线主状态枚举。

## Gate 规则

- 出现关键缺口或硬冲突时输出 `BLOCKED`。
- `BLOCKED` 只输出澄清问题并终止。
- 非关键缺口输出 `DRAFT_WITH_GAPS`。
- `DRAFT_WITH_GAPS` 使用 `[待确认:Gxx]` 标记未决事项。
- `HARNESS_FAILED` 记录失败并立即终止。
- 人工审核不能绕过 `BLOCKED`。
- 人工审核不能绕过 `HARNESS_FAILED`。
- 人工审核不会自动把 Gate 升级为 `READY`。

## 安装

将本仓库克隆到 Codex Skills 目录：

```powershell
git clone https://github.com/quietlzx/ai-prd-assistant.git
Copy-Item -Recurse -Force `
  ".\ai-prd-assistant" `
  "$env:USERPROFILE\.codex\skills\ai-prd-assistant"
```

在 Codex 中调用：

```text
使用 $ai-prd-assistant 把这份原始需求转换为分阶段 PRD 交付包。
```

## 使用方法

提供原始需求，并要求输出 Brief、需求校验、PRD、风险清单和待审核的报告包。

Skill 会执行以下流程：

1. 把输入整理为结构化 Brief。
2. 判定为 `READY`、`DRAFT_WITH_GAPS` 或 `BLOCKED`。
3. 需求校验完成后才生成 PRD。
4. 按六大类别分析 AI 产品风险。
5. 在人工审核处停止。
6. 只有 `review_state=approved` 后才组装 Markdown 和 HTML。

## Harness

运行内置结构校验：

```bash
python scripts/harness.py self-test
python scripts/harness.py validate <运行目录>
```

Harness 校验以下内容：

- 阶段顺序
- 必需文件
- 必需字段
- 状态枚举
- 人工审核状态流转
- 产物引用
- 未编号的 `[待确认]` 标记
- 单文件 HTML 约束
- 强制免责提示

Harness 不判断业务语义，也不评价 PRD 内容质量。

## 仓库结构

```text
ai-prd-assistant/
|-- SKILL.md
|-- agents/
|   `-- openai.yaml
|-- llm-default.yaml
|-- references/
|   |-- output-contract.md
|   |-- prd-template.md
|   |-- risk-taxonomy.md
|   `-- workflow.md
|-- scripts/
|   `-- harness.py
`-- test-cases/
    |-- conflict/
    |-- empty-input/
    |-- missing-info/
    `-- normal/
```

## 配置

`llm-default.yaml` 提供通用默认模型配置。请使用环境变量管理凭据和部署地址，不要在仓库中提交 API Key、私有模型地址或内部文档。

## 开发

```bash
python -m venv .venv
python -m pip install -e ".[dev]"
pytest
ruff check .
python scripts/harness.py self-test
```

## 贡献

请阅读 `CONTRIBUTING.md`。修改状态值、Gate 行为、`review_state` 流转或输出结构属于破坏性变更，必须同步更新测试和 `CHANGELOG.md`。

## 安全

请阅读 `SECURITY.md`。不要提交真实公司文档、客户数据、凭据、私有地址或未脱敏的运行产物。

## 许可证

MIT
