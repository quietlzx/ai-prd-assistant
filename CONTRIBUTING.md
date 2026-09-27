# 贡献指南

## 提交 Pull Request 前

1. 描述问题和解决问题所需的最小行为变更。
2. 新增或更新测试。
3. 运行：

```bash
pytest
ruff check .
python scripts/harness.py self-test
```

4. Update `CHANGELOG.md`.
5. Confirm that no private documents, credentials, endpoints, or run logs are
   included.

## 规则变更

以下变更属于破坏性变更：

- 新增或删除流水线主状态
- 修改 Gate 行为
- 修改 `review_state` 流转
- 修改必需阶段顺序
- 修改报告产物契约

破坏性变更必须提供迁移说明。

## 数据规则

只使用合成示例。禁止提交公司文档、客户数据、个人信息、API Key、私有地址或模型凭据。
