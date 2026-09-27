# Serial Workflow and Review Gate

## Production Stages

```text
输入归一化
→ 需求校验
→ PRD 生成
→ AI 风险识别
→ 人审门禁
→ 报告组装
```

The first four stages produce artifacts. Human review is a control gate, not a
sixth pipeline status.

## Gate Conclusions

### BLOCKED

Use when a critical gap or hard conflict prevents a responsible PRD draft.
Output clarification questions only and terminate.

### DRAFT_WITH_GAPS

Use when the core scope is understandable but material decisions remain.
Continue while referencing every unresolved item as `[待确认:Gxx]`.

### READY

Use when the Brief is structurally sufficient and no material conflict remains.
This does not guarantee that assumptions are correct.

### HARNESS_FAILED

Use when structural validation fails. Write the failure log and stop. Do not
retry, repair silently, or continue.

## Artifact Ownership

Each stage owns one artifact type:

- Stage 1 owns the Brief.
- Stage 2 owns validation and Gate output.
- Stage 3 owns the PRD.
- Stage 4 owns the AI risk list.
- Human review owns the review decision.
- Report assembly owns Markdown and HTML.

Downstream stages read artifacts instead of replaying the full conversation.

## Review State

```text
pending
approved
rejected
revision
```

Transitions:

```text
pending → approved
pending → revision → rebuild affected artifacts → pending
pending → rejected → stop
```

Only `approved` permits report assembly. Gate status remains unchanged during
review.
