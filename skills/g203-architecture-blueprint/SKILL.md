---
name: g203-architecture-blueprint
description: 架构蓝图定义，用于基于 G201 的技术策略形成可交付的系统蓝图、关键视图和 ADR 集，并产出可供 G204 消费的结构化输入。
version: 0.1.0
---

# G203 架构蓝图定义 SKILL

## 元信息与执行契约

说明：完整机读契约以文档头部 YAML 为准；本章节仅提供执行摘要。

### 基本信息

| 项目 | 内容 |
|---|---|
| skill_id | `G203` |
| skill_type | `core` |
| 中文名称 | 架构蓝图定义 |
| 适用阶段 | `architecture` |
| 执行模式 | `fast`、`standard`、`complete` |
| 前置依赖 | `AD-04`（`G201` 已完成） |
| 后置依赖 | `G204` |
| 输出主文档 | `artifacts/architecture/003-architecture-blueprint.md`、`artifacts/architecture/004-adr.md` |

### 执行契约摘要

| 项目 | 内容 |
|---|---|
| 运行时任务映射 | `task_id=AD-05`，`skill_id=G203` |
| Skill 生命周期 | 主起草任务为 `AD-05`；质量检查与用户评审分别承接到共享服务任务 `AD-07(GS-Quality-Check)`、`AD-08(GS-Review)`；`skill_id` 维持各任务原定义，不重写为 `G203` |
| 运行时台账路径 | `artifacts/architecture/000-task-tracker.md` |
| 证据路径 | `evidence/AD-05/` |
| 必选输入 | `artifacts/architecture/001-technical-strategy.md`、`artifacts/architecture/002-architecture-vision.md` |
| 按需输入 | `artifacts/architecture/001-architecture-intake.md`、requirements 阶段主输出、上游评审结论 |
| 模板与参考 | `template.md`、`references/execution-details.md`、`references/role-definition.md`、`../_shared/architecture-methods-catalog.md` |
| 质量门摘要 | `overall_status` 仅允许 `pass/pass_with_warning`，且不得有 `critical/major` 问题 |

## 1. 目标

在已冻结的架构愿景与技术策略基础上，形成可执行的架构蓝图，明确：

1. 系统结构主线、关键视图和职责边界
2. 组件、数据、接口和部署关系
3. 需要正式固化的 ADR 集
4. 供 `G204` 消费的蓝图验证输入

## 2. 角色定义

`G203` 的角色边界、职责和输出风格见：

- [role-definition.md](references/role-definition.md)

`G203` 的实际执行记录与步骤细化统一使用以下本地文件：

- [template.md](template.md)
- [execution-details.md](references/execution-details.md)

执行要求：

1. `template.md`用于记录本轮输出细则。
2. `execution-details.md` 用于补足各步骤的推进条件、结束条件与回写要求。

## 3. 前置条件

1. `AD-04` 已完成，并已产出 `artifacts/architecture/001-technical-strategy.md`。
2. `artifacts/architecture/002-architecture-vision.md` 已存在且可读取。
3. `G201` 最小消费字段可完整读取。
4. 当前任务映射固定为：`AD-05` 为起草任务；质量门和评审门由 `AD-07/AD-08` 统一承接。

## 4. 输入输出契约

### 4.1 输入

1. `artifacts/architecture/001-technical-strategy.md`（必选）
2. `artifacts/architecture/002-architecture-vision.md`（必选）
3. `artifacts/architecture/001-architecture-intake.md`（按需）
4. `artifacts/requirements/003-requirements-baseline.md`（按需）
5. `artifacts/requirements/004-mvp-definition.md`（按需）
6. `artifacts/reviews/001-requirements-review.md`（按需）

### 4.2 输出

1. 主输出：`artifacts/architecture/003-architecture-blueprint.md`
2. ADR 输出：`artifacts/architecture/004-adr.md`
3. 证据目录：`evidence/AD-05/`

### 4.3 质量约束

1. 输出必须使用 Markdown。
2. 文档规模 `< 10000` 行；超限必须拆分且每个文件自包含。
3. 路径统一使用 `/`。
4. 蓝图结论必须同时能追溯到 `G201` 的技术策略与 `G202` 的愿景约束；缺少 `002-architecture-vision.md` 时不得启动当前 Skill。
5. 必须显式给出 `S5-A02/S5-A03/S5-A04/S5-A05` 的覆盖声明，且覆盖声明、正文章节与第 7 章最小字段之间不得互相矛盾。

## 5. 执行步骤

执行说明：

1. `G203` 由 architecture 阶段入口编排 SKILL `G200` 触发，并必须在独立子代理中执行。
2. 子代理仅负责本 Skill 文档产出；任务状态验收、台账回写和关闭动作均由 `G200` 统一执行。

### 步骤 1：建立蓝图主线与视图边界

- 操作主体：`G203-SKILL`
- 具体任务：
  - 提炼蓝图目标、范围边界和需要覆盖的视图集合
  - 建立系统上下文、结构、交互、部署视图的主线关系
  - 形成 `S5-A02/S5-A03/S5-A04/S5-A05` 到蓝图视图与结构化字段的覆盖声明
  - 明确哪些内容进入蓝图，哪些保留到详细设计阶段
- 方法论（架构视角）：
  - 必用：`蓝图范围切片`
  - 必用：`架构视图映射`
  - 必用：`约束落图`
  - 可选：`蓝图追溯映射`
- 输入：`001-technical-strategy.md`
- 输出：蓝图主线与视图边界结论（写入主文档）
- 依赖关系：无

### 步骤 2：定义组件、数据与接口结构

- 操作主体：`G203-SKILL`
- 具体任务：
  - 定义核心组件、职责分配和边界归属
  - 定义核心数据对象、权威存储边界、数据流转、一致性/主从边界和生命周期要求
  - 形成关键交互链路、接口边界、调用方式、契约约束、异常语义和集成模式
  - 对组件依赖和集成约束做显式说明
- 方法论（架构视角）：
  - 必用：`组件职责分解`
  - 必用：`接口与依赖建模`
  - 必用：`关键链路走查`
  - 可选：`视图一致性检查`
- 输入：步骤 1 输出
- 输出：组件、数据与接口结论（写入主文档）
- 依赖关系：依赖步骤 1 完成

### 步骤 3：定义部署拓扑与运行边界

- 操作主体：`G203-SKILL`
- 具体任务：
  - 形成运行节点、部署单元和环境边界
  - 明确高可用、伸缩、隔离和安全边界
  - 标记部署约束对蓝图结构的影响
- 方法论（架构视角）：
  - 必用：`部署拓扑建模`
  - 必用：`约束落图`
  - 必用：`视图一致性检查`
  - 可选：`关键链路走查`
- 输入：步骤 1-2 输出
- 输出：部署拓扑结论（写入主文档）
- 依赖关系：依赖步骤 1-2 完成

### 步骤 4：固化 ADR 与评审关注点

- 操作主体：`G203-SKILL`
- 具体任务：
  - 将需要正式固化的关键决策沉淀为 ADR 条目
  - 建立 ADR 与视图、组件、约束之间的关联
  - 输出供 `G204` 使用的评审关注点和蓝图风险
- 方法论（架构视角）：
  - 必用：`ADR 固化`
  - 必用：`蓝图追溯映射`
  - 必用：`视图一致性检查`
  - 可选：`风险热点复核`
- 输入：步骤 1-3 输出
- 输出：ADR 与评审关注点结论（写入主文档）
- 依赖关系：依赖步骤 1-3 完成

### 步骤 5：生成架构蓝图与 ADR 文档

- 操作主体：`G203-SKILL`
- 具体任务：
  - 按模板整合章节并完成结构自检
  - 校验最小消费字段、路径格式和编号一致性
  - 持久化到目标路径
- 输入：步骤 1-4 输出
- 输出：`artifacts/architecture/003-architecture-blueprint.md`、`artifacts/architecture/004-adr.md`
- 依赖关系：依赖步骤 1-4 完成

## 6. 与运行时台账对齐

推荐任务映射：

- `task_id`: `AD-05`
- `skill_id`: `G203`
- 生命周期口径：`AD-05` 负责 `drafting` 与返工后的再次起草；`AD-07` 负责 `quality_check`；`AD-08` 负责 `user_review`
- 返工回路：`AD-07/AD-08 -> AD-05(rework) -> drafting`

执行要求：

1. `AD-05` 只负责当前 Skill 的起草与返工后的再次起草。
2. `status_code/status_label/skill_stage/review_result/resume_from/evidence_path/updated_at` 的正式回写由 `G200` 在子代理验收后统一执行。
3. `AD-05` 起草完成后保持 `in_progress`，由 `G200` 推进到 `AD-07/AD-08`。
4. 质量检查结果写入质量报告字段，不写入 `review_result`。

## 7. 验收标准

### 7.1 执行检查闭环（强制）

为避免质量门数据来源后置，`G203` 在本 SKILL 内固定以下检查闭环：

| 项目 | 固定定义 |
|---|---|
| 质量检查工具 | `GS-Quality-Check` |
| 触发任务 | `AD-07` |
| 质量报告路径 | `artifacts/reviews/architecture-quality-check.md` |

1. 主文档存在且路径正确：`artifacts/architecture/003-architecture-blueprint.md`、`artifacts/architecture/004-adr.md`。
2. 文档章节必须与 `template.md` 对齐，至少包含：`1. 蓝图目标与范围`、`2. 架构视图`（含 `2.3 视图覆盖声明`）、`3. 组件与职责`（含数据架构承接小节）、`4. 关键交互与依赖`（含接口架构清单）、`5. 部署拓扑与运行边界`、`6. ADR 清单`、`9. 追溯与证据`；其中 `004-adr.md` 必须满足 `template.md` 第 `6.3` 章定义的 ADR 最小结构契约。
3. 所有蓝图结论必须能追溯到 `G201` 的策略约束或 `G202` 的愿景边界，并且能通过覆盖声明证明 `S5-A02/S5-A03/S5-A04/S5-A05` 已被当前蓝图完整承接。

## 8. 失败与恢复

1. 若 `G201` 输出不完整导致无法形成蓝图主线，应由 `G200` 将当前任务判定为 `blocked`，并在 `resume_from` 写明缺失项。
2. 若 `002-architecture-vision.md` 缺失或无法读取，应由 `G200` 将当前任务判定为 `blocked`，并在 `resume_from` 写明需先补齐愿景文档。
3. 若组件边界、数据权威边界、接口契约或部署拓扑无法收敛，应由 `G200` 保持当前任务 `in_progress` 并推进到 `rework`。
4. 恢复时优先读取 `artifacts/architecture/000-task-tracker.md` 的 `resume_from`。
5. 若“供 `G204` 消费的最小字段”不完整，或覆盖声明与数据/接口字段无法证明 `S5-A02/S5-A03/S5-A04/S5-A05` 已承接，视为当前轮不可交付并返工。

## 9. References

- [template.md](template.md)
- [role-definition.md](references/role-definition.md)
- [execution-details.md](references/execution-details.md)
- [architecture-methods-catalog.md](../_shared/architecture-methods-catalog.md) `G203` 方法论标准引用来源
- [runtime-task-tracker-spec.md](../_shared/governance/runtime-task-tracker-spec.md)
- [quality-checker-requirements.md](../_shared/governance/quality-checker-requirements.md)
- [G200 architecture entry](../g200-architecture-entry/SKILL.md)
- [GS-Quality-Check](../gs-quality-check/SKILL.md)
- [GS-Review](../gs-review/SKILL.md)
