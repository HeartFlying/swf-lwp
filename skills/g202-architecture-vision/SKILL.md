---
name: g202-architecture-vision
description: 架构愿景定义，用于基于需求交接冻结系统目标、架构驱动因素、边界和质量属性，产出可供 G201 消费的 architecture vision。
version: 0.1.0
---

# G202 架构愿景定义 SKILL

## 元信息与执行契约

说明：完整机读契约以文档头部 YAML 为准；本章节仅提供执行摘要。

### 基本信息

| 项目 | 内容 |
|---|---|
| skill_id | `G202` |
| skill_type | `core` |
| 中文名称 | 架构愿景定义 |
| 适用阶段 | `architecture` |
| 执行模式 | `fast`、`standard`、`complete` |
| 前置依赖 | `AD-01`、`AD-02`、requirements 阶段交接已完成 |
| 后置依赖 | `G201` |
| 输出主文档 | `artifacts/architecture/002-architecture-vision.md` |

### 执行契约摘要

| 项目 | 内容 |
|---|---|
| 运行时任务映射 | `task_id=AD-03`，`skill_id=G202` |
| Skill 生命周期 | 主起草任务为 `AD-03`；质量检查与用户评审分别承接到共享服务任务 `AD-07(GS-Quality-Check)`、`AD-08(GS-Review)`；`skill_id` 维持各任务原定义，不重写为 `G202` |
| 运行时台账路径 | `artifacts/architecture/000-task-tracker.md` |
| 证据路径 | `evidence/AD-03/` |
| 必选输入 | `artifacts/architecture/001-architecture-intake.md`、`artifacts/requirements/003-requirements-baseline.md`、`artifacts/requirements/004-mvp-definition.md`、`artifacts/requirements/005-handoff-summary.md` |
| 按需输入 | `artifacts/requirements/002-business-context.md`、`artifacts/reviews/001-requirements-review.md` |
| 模板与参考 | `template.md`、`references/execution-details.md`、`references/role-definition.md`、`../_shared/architecture-methods-catalog.md` |
| 质量门摘要 | `overall_status` 仅允许 `pass/pass_with_warning`，且不得有 `critical/major` 问题 |

## 1. 目标

形成 architecture 阶段的统一问题定义与目标边界，明确：

1. 架构目标与成功标准
2. 关键业务场景与系统边界
3. 架构驱动因素、质量属性与约束
4. 供 `G201` 消费的决策输入与风险上下文

## 2. 角色定义

`G202` 的角色边界、职责和输出风格见：

- [role-definition.md](references/role-definition.md)

`G202` 的实际执行记录与步骤细化统一使用以下本地文件：

- [template.md](template.md)
- [execution-details.md](references/execution-details.md)

执行要求：

1. `template.md`用于记录本轮输出细则。
2. `execution-details.md` 用于补足各步骤的推进条件、结束条件与回写要求。

## 3. 前置条件

1. `AD-01` 已完成，并已产出 `artifacts/architecture/001-architecture-intake.md`。
2. `AD-02` 已完成；若未触发澄清，必须按 `no-op` 收口并置为 `done`。
3. 上游 requirements 阶段交接已可消费，至少可读取 `final_mode`、`handoff_summary`、requirements 输出主文档路径。
4. 当前任务映射固定为：`AD-03` 为起草任务；质量门和评审门由 `AD-07/AD-08` 统一承接。

## 4. 输入输出契约

### 4.1 输入

1. `artifacts/architecture/001-architecture-intake.md`（必选）
2. requirements 阶段交接摘要与交接记录（必选）
3. `artifacts/requirements/003-requirements-baseline.md`（必选）
4. `artifacts/requirements/004-mvp-definition.md`（必选）
5. `artifacts/requirements/002-business-context.md`（按需）
6. `artifacts/reviews/001-requirements-review.md`（按需）

### 4.2 输出

1. 主输出：`artifacts/architecture/002-architecture-vision.md`
2. 证据目录：`evidence/AD-03/`

### 4.3 质量约束

1. 输出必须使用 Markdown。
2. 文档规模 `< 10000` 行；超限必须拆分且每个文件自包含。
3. 路径统一使用 `/`。
4. 每个关键结论必须显式标注来源、假设或推导依据。

## 5. 执行步骤

执行说明：

1. `G202` 由 architecture 阶段入口编排 SKILL `G200` 触发，并必须在独立子代理中执行。
2. 子代理仅负责本 Skill 文档产出；任务状态验收、台账回写和关闭动作均由 `G200` 统一执行。

### 步骤 1：冻结系统目标与边界

- 操作主体：`G202-SKILL`
- 具体任务：
  - 提炼系统目标、阶段目标和成功标准
  - 明确 in-scope / out-of-scope 与对下游设计的边界
  - 形成系统上下文边界描述
- 方法论（架构视角）：
  - 必用：`系统上下文图`
  - 必用：`约束分层法`
  - 必用：`架构驱动识别`
  - 可选：`第一性原理`
- 输入：requirements 阶段交接、architecture intake
- 输出：目标与边界结论（写入主文档）
- 依赖关系：无

### 步骤 2：识别架构驱动因素

- 操作主体：`G202-SKILL`
- 具体任务：
  - 识别业务、技术、合规、交付约束驱动
  - 形成驱动优先级和相互冲突关系
  - 明确必须优先满足的关键驱动
- 方法论（架构视角）：
  - 必用：`架构驱动识别`
  - 必用：`质量属性场景`
  - 必用：`质量属性效用树`
  - 可选：`风险驱动分析`
- 输入：步骤 1 输出、requirements baseline、MVP 定义
- 输出：架构驱动清单（写入主文档）
- 依赖关系：依赖步骤 1 完成

### 步骤 3：定义关键场景与质量属性

- 操作主体：`G202-SKILL`
- 具体任务：
  - 提炼关键业务场景、关键用户旅程和异常场景
  - 为关键质量属性定义场景化目标
  - 标记驱动与场景的映射关系
- 方法论（架构视角）：
  - 必用：`质量属性场景`
  - 必用：`场景优先级排序`
  - 必用：`系统上下文图`
  - 可选：`事件风暴`
- 输入：步骤 2 输出
- 输出：关键场景和质量属性结论（写入主文档）
- 依赖关系：依赖步骤 2 完成

### 步骤 4：形成架构原则、假设与风险

- 操作主体：`G202-SKILL`
- 具体任务：
  - 总结架构原则与决策边界
  - 列出当前工作假设、未决事项和风险
  - 形成后续 `G201` 的决策前提
- 方法论（架构视角）：
  - 必用：`风险驱动分析`
  - 必用：`假设清单与验证计划`
  - 必用：`约束分层法`
  - 可选：`假设反转`
- 输入：步骤 1-3 输出
- 输出：原则、假设与风险结论（写入主文档）
- 依赖关系：依赖步骤 1-3 完成

### 步骤 5：生成架构愿景文档

- 操作主体：`G202-SKILL`
- 具体任务：
  - 按模板整合章节并完成结构自检
  - 校验追溯、路径格式和最小消费字段
  - 持久化到目标路径
- 输入：步骤 1-4 输出
- 输出：`artifacts/architecture/002-architecture-vision.md`
- 依赖关系：依赖步骤 1-4 完成

## 6. 与运行时台账对齐

推荐任务映射：

- `task_id`: `AD-03`
- `skill_id`: `G202`
- 生命周期口径：`AD-03` 负责 `drafting` 与返工后的再次起草；`AD-07` 负责 `quality_check`；`AD-08` 负责 `user_review`
- 返工回路：`AD-07/AD-08 -> AD-03(rework) -> drafting`

执行要求：

1. `AD-03` 只负责当前 Skill 的起草与返工后的再次起草。
2. `status_code/status_label/skill_stage/review_result/resume_from/evidence_path/updated_at` 的正式回写由 `G200` 在子代理验收后统一执行。
3. `AD-03` 起草完成后保持 `in_progress`，由 `G200` 推进到 `AD-07/AD-08`。
4. 质量检查结果写入质量报告字段，不写入 `review_result`。

## 7. 验收标准

### 7.1 执行检查闭环（强制）

为避免质量门数据来源后置，`G202` 在本 SKILL 内固定以下检查闭环：

| 项目 | 固定定义 |
|---|---|
| 质量检查工具 | `GS-Quality-Check` |
| 触发任务 | `AD-07` |
| 质量报告路径 | `artifacts/reviews/architecture-quality-check.md` |

1. 主文档存在且路径正确：`artifacts/architecture/002-architecture-vision.md`。
2. 文档章节必须与 `template.md` 对齐，至少包含：`1. 架构目标与范围`、`2. 架构驱动因素`、`3. 关键场景与质量属性`、`4. 架构原则与边界`、`5. 风险与假设`、`6. 方法检查清单`、`8. 追溯与证据`。
3. 质量检查结果必须满足：`overall_status` 为 `pass` 或 `pass_with_warning`，且 `critical/major` 问题均为 `0`。
4. 关键结论必须明确标注来源、工作假设或待确认项。

## 8. 失败与恢复

1. 若 requirements 交接缺失导致无法建立驱动与边界，标记 `blocked`，在 `resume_from` 写明待补齐输入。
2. 若关键场景、质量属性或原则无法收敛，保持 `in_progress` 并进入 `rework`。
3. 恢复时优先读取 `artifacts/architecture/000-task-tracker.md` 的 `resume_from`。
4. 若 `G201` 最小消费字段不完整，视为当前轮不可交付并返工。

## 9. References

- [template.md](template.md)
- [role-definition.md](references/role-definition.md)
- [execution-details.md](references/execution-details.md)
- [architecture-methods-catalog.md](../_shared/architecture-methods-catalog.md)
- [runtime-task-tracker-spec.md](../_shared/governance/runtime-task-tracker-spec.md)
- [quality-checker-requirements.md](../_shared/governance/quality-checker-requirements.md)
- [G200 architecture entry](../g200-architecture-entry/SKILL.md)
- [GS-Quality-Check](../gs-quality-check/SKILL.md)
- [GS-Review](../gs-review/SKILL.md)
