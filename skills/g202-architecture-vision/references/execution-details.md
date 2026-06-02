# G202 执行细化说明

## 1. 作用

本文件用于细化 `G202` 的执行方式，补齐 `SKILL.md` 中“如何真正落地到架构愿景文档”的步骤约束。

## 2. 执行原则

1. `G202` 的目标是建立问题定义和架构边界，不提前替代 `G201` 输出技术策略。
2. 每项关键结论都必须关联来源、工作假设或待确认项。
3. 输出必须直接满足 `G201` 的最小消费字段，不得只写概念性描述。
4. 子代理只负责起草文档；运行时任务状态、返工入口、`review_result` 和 `resume_from` 由 `G200` 在验收后统一回写。

## 3. 输入消费顺序

1. 优先读取 `artifacts/architecture/001-architecture-intake.md`。
2. 再读取 requirements 阶段交接摘要、交接记录和 `final_mode`。
3. 核心 requirements 输入按优先级为：
   - `artifacts/requirements/004-mvp-definition.md`
   - `artifacts/requirements/003-requirements-baseline.md`
   - `artifacts/requirements/002-business-context.md`（如存在）
   - `artifacts/reviews/001-requirements-review.md`（如存在）

## 4. 步骤级要求

### 4.1 目标与边界

1. 必须至少给出 1 版系统目标摘要。
2. 必须显式写出 in-scope / out-of-scope。
3. 若边界无法冻结，当前轮不得进入 `G201`。

### 4.2 驱动因素

1. 必须覆盖业务、技术、合规/交付三类驱动。
2. 每类至少列出 1 项；确无则说明原因。
3. 必须标记优先级和影响范围。

### 4.3 关键场景与质量属性

1. 必须至少给出 2 个关键业务场景。
2. 必须至少给出 3 个质量属性场景。
3. 每个质量属性场景都要有目标值或明确边界。

### 4.4 原则、假设与风险

1. 架构原则至少 3 条。
2. 工作假设至少 2 条，且每条有验证方式。
3. 风险至少覆盖技术、业务、交付三类。

## 5. 与 G201 的衔接要求

进入 `G201` 前，`G202` 输出至少要保证：

1. 可直接转成策略目标。
2. 可直接转成技术决策输入。
3. 可直接转成质量策略与权衡依据。
4. 可直接约束技术选型与蓝图设计。

## 6. 质量与恢复要求
1. 中断恢复时仅以 `artifacts/architecture/000-task-tracker.md` 为主锚点，`template.md` 作为辅助证据。
2. 若质量门或评审门未通过，由 `G200` 统一回写：`AD-03` 保持 `status_code=in_progress`、`skill_stage=rework`，并在 `resume_from` 中写明首个返工任务位和待处理问题。
