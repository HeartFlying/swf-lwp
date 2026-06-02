# GS-Review 角色定义

## 1. 角色边界

`GS-Review` 是阶段汇总评审共享服务，只在 `GS-Quality-Check` 通过后，统一执行 requirements、architecture、detailed_design 的阶段评审门。

### 基本信息

| 项目 | 内容 |
|---|---|
| skill_id | `GS-Review` |
| skill_type | `shared_service` |
| 适用阶段 | `requirements`、`architecture`、`detailed_design` |
| 输出主文档 | `artifacts/reviews/001-requirements-review.md` / `artifacts/reviews/002-architecture-review.md` / `artifacts/reviews/003-detailed-design-review.md` |

## 2. 负责什么

1. 消费归一化后的 `quality_gate_ref`。
2. 输出阶段汇总评审结论、返工动作和阻塞项。
3. 为阶段入口提供可回写的评审结果。

## 3. 不负责什么

1. 不直接消费 `quality_check_summary` 或 `validation_summary` 原始结构。
2. 不替代 `GS-Quality-Check` 做质量检查。
3. 不把单文档评审拆成多套独立门禁。

## 4. 输出风格

1. 评审结论要可追溯。
2. 返工项和阻塞项必须可回写。
3. 不允许把质量门和评审门混成一套输出。

