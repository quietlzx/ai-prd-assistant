# 串行工作流与审核门禁

## 生产阶段

```text
输入归一化
→ 需求校验
→ PRD 生成
→ AI 风险识别
→ 人审门禁
→ 报告组装
```

前四个阶段负责生成产物。人工审核是控制门禁，不是第六个流水线状态。

## Gate 结论

### BLOCKED

当关键缺口或硬冲突导致无法负责任地生成 PRD 草案时使用。只输出澄清问题并终止。

### DRAFT_WITH_GAPS

当核心范围可以理解，但仍存在重要未决事项时使用。继续执行，并将未决项标记为 `[待确认:Gxx]`。

### READY

当 Brief 在结构上足够完整且没有重要冲突时使用。这不代表其中的假设一定正确。

### HARNESS_FAILED

当结构校验失败时使用。写入失败日志并终止，不得重试、静默修复或继续执行。

## 产物归属

每个阶段只负责一类产物：

- 第 1 阶段负责 Brief。
- 第 2 阶段负责需求校验和 Gate 结论。
- 第 3 阶段负责 PRD。
- 第 4 阶段负责 AI 风险清单。
- 人工审核负责审核决策。
- 报告组装负责 Markdown 和 HTML。

下游阶段读取产物文件，而不是重新读取完整对话。

## 审核状态

```text
pending
approved
rejected
revision
```

状态流转：

```text
pending → approved
pending → revision → 重建受影响产物 → pending
pending → rejected → 终止
```

只有 `approved` 允许进入报告组装。审核过程中 Gate 状态保持不变。
