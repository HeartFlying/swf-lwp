---
name: g201-technical-strategy
description: 技术策略定义，用于基于 G202 的架构愿景收敛技术路线、关键选型、权衡原则和实施约束，产出可供 G203 消费的 technical strategy。
version: 0.1.0
---

# G201 技术策略定义 SKILL

## 元信息与执行契约

说明：完整机读契约以文档头部 YAML 为准；本章节仅提供执行摘要。

### 基本信息

| 项目 | 内容 |
|---|---|
| skill_id | `G201` |
| skill_type | `core` |
| 中文名称 | 技术策略定义 |
| 适用阶段 | `architecture` |
| 执行模式 | `fast`、`standard`、`complete` |
| 前置依赖 | `AD-03`（`G202` 已完成） |
| 后置依赖 | `G203` |
| 输出主文档 | `artifacts/architecture/001-technical-strategy.md` |

### 执行契约摘要

| 项目 | 内容 |
|---|---|
| 运行时任务映射 | `task_id=AD-04`，`skill_id=G201` |
| Skill 生命周期 | 主起草任务为 `AD-04`；质量检查与用户评审分别承接到共享服务任务 `AD-07(GS-Quality-Check)`、`AD-08(GS-Review)`；`skill_id` 维持各任务原定义，不重写为 `G201` |
| 运行时台账路径 | `artifacts/architecture/000-task-tracker.md` |
| 证据路径 | `evidence/AD-04/` |
| 必选输入 | `artifacts/architecture/002-architecture-vision.md`、`artifacts/requirements/005-handoff-summary.md` |
| 按需输入 | `artifacts/architecture/001-architecture-intake.md`、requirements 阶段输出、上游评审结论 |
| 模板与参考 | `template.md`、`references/execution-details.md`、`references/role-definition.md`、`../_shared/architecture-methods-catalog.md` |
| 质量门摘要 | `overall_status` 仅允许 `pass/pass_with_warning`，且不得有 `critical/major` 问题 |

## 1. 目标

在已冻结的架构愿景基础上，形成可执行的技术策略，明确：

1. 技术路线与总体实现方向
2. 关键选型候选、权衡与推荐结论
3. 与质量属性匹配的策略约束
4. 供 `G203` 消费的蓝图级设计输入

## 2. 角色定义

`G201` 的角色边界、职责和输出风格见：

- [role-definition.md](references/role-definition.md)
## 2.1 执行模板与细化说明

`G201` 的实际执行记录与步骤细化统一使用以下本地文件：

- [template.md](template.md)
- [execution-details.md](references/execution-details.md)

执行要求：

1. `template.md` 用于记录本轮输出细则。
2. `execution-details.md` 用于补足各步骤的推进条件、结束条件与回写要求。

## 3. 前置条件

1. `AD-03` 已完成，并已产出 `artifacts/architecture/002-architecture-vision.md`。
2. `G202` 最小消费字段可完整读取。
3. 当前任务映射固定为：`AD-04` 为起草任务；质量门和评审门由 `AD-07/AD-08` 统一承接。

## 4. 输入输出契约

### 4.1 输入

1. `artifacts/architecture/002-architecture-vision.md`（必选）
2. `artifacts/architecture/001-architecture-intake.md`（按需）
3. `artifacts/requirements/003-requirements-baseline.md`（按需）
4. `artifacts/requirements/004-mvp-definition.md`（按需）
5. `artifacts/reviews/001-requirements-review.md`（按需）

### 4.2 输出

1. 主输出：`artifacts/architecture/001-technical-strategy.md`
2. 证据目录：`evidence/AD-04/`

### 4.3 质量约束

1. 输出必须使用 Markdown。
2. 文档规模 `< 10000` 行；超限必须拆分且每个文件自包含。
3. 路径统一使用 `/`。
4. 推荐结论必须同时给出理由、替代方案和不采用原因。

## 5. 执行步骤

执行说明：

1. `G201` 由 architecture 阶段入口编排 SKILL `G200` 触发，并必须在独立子代理中执行。
2. 子代理仅负责本 Skill 文档产出；任务状态验收、台账回写和关闭动作均由 `G200` 统一执行。

### 步骤 1：提炼策略目标

- 操作主体：`G201-SKILL`
- 具体任务：
  - 从 `G202` 提取技术策略目标和约束边界
  - 识别必须优先满足的质量属性与架构原则
  - 冻结策略判断基线
- 方法论（架构视角）：
  - 必用：`架构原则约束映射`
  - 必用：`约束驱动选型`
  - 必用：`技术域分层分析`
  - 可选：`假设清单与验证计划`
- 输入：`002-architecture-vision.md`
- 输出：策略目标与约束结论（写入主文档）
- 依赖关系：无

### 步骤 2：形成技术路线候选

- 操作主体：`G201-SKILL`
- 具体任务：
  - 形成核心技术方向、候选方案和适用边界
  - 对关键技术域给出推荐与备选
  - 标记候选之间的依赖与冲突
- 方法论（架构视角）：
  - 必用：`决策矩阵`
  - 必用：`ATAM 权衡分析`
  - 必用：`风险驱动决策`
  - 可选：`替代路线与触发条件分析`
- 输入：步骤 1 输出
- 输出：技术路线候选结论（写入主文档）
- 依赖关系：依赖步骤 1 完成

### 步骤 3：收敛技术选型与权衡

- 操作主体：`G201-SKILL`
- 具体任务：
  - 对关键技术点做推荐决策
  - 说明选择理由、不选理由和替代条件
  - 形成跨维度权衡摘要
- 方法论（架构视角）：
  - 必用：`决策矩阵`
  - 必用：`成本-收益-风险权衡`
  - 必用：`约束驱动选型`
  - 可选：`ADR 思维`
- 输入：步骤 2 输出
- 输出：选型与权衡结论（写入主文档）
- 依赖关系：依赖步骤 2 完成

### 步骤 4：定义实施约束与 ADR 候选

- 操作主体：`G201-SKILL`
- 具体任务：
  - 总结实现约束、接口边界、演进路径约束
  - 识别需要进入 ADR 的决策候选
  - 标记进入 `G203` 的强制输入
- 方法论（架构视角）：
  - 必用：`ADR 思维`
  - 必用：`假设清单与验证计划`
  - 必用：`替代路线与触发条件分析`
  - 可选：`架构原则约束映射`
- 输入：步骤 1-3 输出
- 输出：实施约束与 ADR 候选（写入主文档）
- 依赖关系：依赖步骤 1-3 完成

### 步骤 5：生成技术策略文档

- 操作主体：`G201-SKILL`
- 具体任务：
  - 按模板整合章节并完成结构自检
  - 校验最小消费字段、路径格式和编号一致性
  - 持久化到目标路径
- 输入：步骤 1-4 输出
- 输出：`artifacts/architecture/001-technical-strategy.md`
- 依赖关系：依赖步骤 1-4 完成

## 6. 与运行时台账对齐

推荐任务映射：

- `task_id`: `AD-04`
- `skill_id`: `G201`
- 生命周期口径：`AD-04` 负责 `drafting` 与返工后的再次起草；`AD-07` 负责 `quality_check`；`AD-08` 负责 `user_review`
- 返工回路：`AD-07/AD-08 -> AD-04(rework) -> drafting`

执行要求：

1. `AD-04` 只负责当前 Skill 的起草与返工后的再次起草。
2. `status_code/status_label/skill_stage/review_result/resume_from/evidence_path/updated_at` 的正式回写由 `G200` 在子代理验收后统一执行。
3. `AD-04` 起草完成后保持 `in_progress`，由 `G200` 推进到 `AD-07/AD-08`。
4. 质量检查结果写入质量报告字段，不写入 `review_result`。

## 7. 验收标准

### 7.1 执行检查闭环（强制）

为避免质量门数据来源后置，`G201` 在本 SKILL 内固定以下检查闭环：

| 项目 | 固定定义 |
|---|---|
| 质量检查工具 | `GS-Quality-Check` |
| 触发任务 | `AD-07` |
| 质量报告路径 | `artifacts/reviews/architecture-quality-check.md` |

1. 主文档存在且路径正确：`artifacts/architecture/001-technical-strategy.md`。
2. 文档章节必须与 `template.md` 对齐，至少包含：`1. 策略目标与约束`、`2. 技术路线候选`、`3. 关键选型与权衡`、`4. 实施约束与 ADR 候选`、`5. 风险与替代路线`、`6. 方法检查清单`、`9. 追溯与证据`。
3. 质量检查结果必须满足：`overall_status` 为 `pass` 或 `pass_with_warning`，且 `critical/major` 问题均为 `0`。
4. 所有推荐结论必须有推荐理由和未采用方案说明。

## 8. 失败与恢复

1. 若 `G202` 输出不完整导致无法形成策略基线，应由 `G200` 将当前任务判定为 `blocked`，并在 `resume_from` 写明缺失项。
2. 若关键选型、权衡或实施约束无法收敛，应由 `G200` 保持当前任务 `in_progress` 并推进到 `rework`。
3. 恢复时优先读取 `artifacts/architecture/000-task-tracker.md` 的 `resume_from`。
4. 若 `G203` 最小消费字段不完整，视为当前轮不可交付并返工。

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
