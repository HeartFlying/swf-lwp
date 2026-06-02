---
name: g301-component-design
description: 组件详细设计，用于基于 architecture 阶段蓝图、技术策略和 detailed_design 阶段执行计划形成可实现的组件级详细设计主文档，并产出可供 G302、G303 与 DD-07 消费的结构化组件设计字段。
version: 1.1.0
---

# G301 组件详细设计 SKILL

## 元信息与执行契约

说明：完整机读契约以文档头部 YAML 为准；本章节仅提供执行摘要。

### 基本信息

| 项目 | 内容 |
|---|---|
| skill_id | `G301` |
| skill_type | `core` |
| 中文名称 | 组件详细设计 |
| 适用阶段 | `detailed_design` |
| 执行模式 | `standard`、`complete` |
| 前置依赖 | `DD-01 ~ DD-03` 已收敛，且 `G300` 已冻结本轮组件设计输入 |
| 后置依赖 | `G302`、`G303`、`DD-07` |
| 输出主文档 | `artifacts/detailed-design/002-component-design.md` |

### 执行契约摘要

| 项目 | 内容 |
|---|---|
| 运行时任务映射 | `task_id=DD-04`，`skill_id=G301` |
| Skill 生命周期 | 主起草任务为 `DD-04`；后续由 `G300` 统一推进 `DD-07=design-review-validation`、`DD-08=GS-Quality-Check`、`DD-09=GS-Review` |
| 运行时台账路径 | `artifacts/detailed-design/000-task-tracker.md` |
| 证据路径 | `evidence/DD-04/` |
| 必选输入 | `artifacts/detailed-design/001-design-plan.md`、`artifacts/architecture/003-architecture-blueprint.md`、`artifacts/architecture/001-technical-strategy.md`、`artifacts/architecture/002-architecture-vision.md` |
| 按需输入 | `artifacts/architecture/004-adr.md`、requirements 阶段主输出、`G300` 产出的澄清记录 |
| 模板与参考 | `template.md`、`references/execution-details.md`、`references/role-definition.md`、`../_shared/detailed-design-methods-catalog.md` |
| 交付前置摘要 | 必须形成组件职责、内部结构、状态转换、关键算法/规则、异常处理、可测试性、接口/数据消费边界的结构化字段 |

## 1. 目标

在已冻结的 detailed_design 输入基础上，形成可执行的组件级详细设计，明确：

1. 组件职责、边界与协作关系。
2. 组件内部结构、关键模块和依赖方向。
3. 关键状态转换、核心算法和规则落点。
4. 异常处理、恢复策略和可测试性设计。
5. 可供 `G302`、`G303` 与 `DD-07` 直接消费的结构化最小字段。

## 2. 角色定义

`G301` 的角色边界、职责和输出风格见：

- [role-definition.md](references/role-definition.md)

`G301` 的实际执行记录与步骤细化统一使用以下本地文件：

- [template.md](template.md)
- [execution-details.md](references/execution-details.md)

执行要求：

1. `template.md`用于记录本轮输出细则。
2. `execution-details.md` 用于补足各步骤的推进条件、结束条件与回写要求。

## 3. 前置条件

1. `artifacts/detailed-design/001-design-plan.md` 已存在，且能读取 `final_mode`、`skills_to_run`、澄清结论与当前轮范围冻结结果。
2. `artifacts/architecture/003-architecture-blueprint.md` 已存在且可读取。
3. `artifacts/architecture/001-technical-strategy.md` 与 `artifacts/architecture/002-architecture-vision.md` 可读取。
4. 当前任务映射固定为：`DD-04` 为起草任务；后续由 `G300` 联动推进 `DD-07=design-review-validation`、`DD-08=GS-Quality-Check`、`DD-09=GS-Review`。
5. 若关键组件边界、核心状态、接口责任归属或数据所有权仍未冻结，应由 `G300` 先完成澄清后再触发当前 Skill。

## 4. 输入输出契约

### 4.1 输入

1. `artifacts/detailed-design/001-design-plan.md`（必选）
2. `artifacts/architecture/003-architecture-blueprint.md`（必选）
3. `artifacts/architecture/001-technical-strategy.md`（必选）
4. `artifacts/architecture/002-architecture-vision.md`（必选）
5. `artifacts/architecture/004-adr.md`（按需）
6. requirements 阶段主输出与上游评审摘要（按需）
7. `G300` 澄清记录与工作假设（按需）

### 4.2 输出

1. 主输出：`artifacts/detailed-design/002-component-design.md`
2. 证据目录：`evidence/DD-04/`

### 4.3 质量约束

1. 输出必须使用 Markdown。
2. 文档规模 `< 10000` 行；超限必须拆分且每个文件自包含。
3. 路径统一使用 `/`。
4. 组件设计必须能回溯到蓝图组件、技术策略约束或上游澄清结论，不得脱离架构蓝图另起一套结构。
5. 对组件之间的关系、关键交互流程、协作关系、状态迁移、异常处理闭环、内部结构分层、测试覆盖映射或追溯链，若仅靠表格难以清晰表达，应用 Markdown 内嵌 Mermaid 图辅助说明；图形作为正文说明增强，不替代表格中的结构化字段。

## 5. 执行步骤

执行说明：

1. `G301` 由 detailed_design 阶段入口编排 SKILL `G300` 触发，并必须在独立子代理中执行。
2. 子代理仅负责本 Skill 文档产出；任务状态验收、台账回写、共享门禁推进和子代理关闭均由 `G300` 统一执行。

### 步骤 1：冻结组件设计范围与对象清单

- 操作主体：`G301-SKILL`
- 具体任务：
  - 从蓝图与 design plan 中冻结本轮要展开的组件范围
  - 识别核心组件、设计优先级、延后项和约束来源
  - 形成组件目录与范围边界
- 方法论（详细设计视角）：
  - 必用：`设计范围冻结`
  - 必用：`约束回链`
  - 必用：`职责-协作映射`
  - 可选：`风险热点预判`
- 输入：`001-design-plan.md`、`003-architecture-blueprint.md`
- 输出：范围与组件清单结论（写入主文档）
- 依赖关系：无

### 步骤 2：定义职责分配与内部结构

- 操作主体：`G301-SKILL`
- 具体任务：
  - 细化每个组件的职责、协作边界和输入输出
  - 设计组件内部模块、分层、依赖方向和扩展点
  - 识别对 `G302/G303` 有影响的接口与数据边界
  - 必要时用 Mermaid 展示组件关系图、协作图、内部结构分层图或关键交互图
- 方法论（详细设计视角）：
  - 必用：`内部结构分解`
  - 必用：`契约驱动设计`
  - 必用：`依赖反转校验`
  - 可选：`时序建模`
- 输入：步骤 1 输出、技术策略、架构愿景
- 输出：职责与内部结构结论（写入主文档）
- 依赖关系：依赖步骤 1 完成

### 步骤 3：定义状态转换与关键算法/规则

- 操作主体：`G301-SKILL`
- 具体任务：
  - 识别状态对象、状态迁移、触发事件和持久化要求
  - 设计关键算法、决策规则、复杂度约束和失败语义
  - 说明状态与算法如何约束组件协作
  - 必要时用 Mermaid 展示关键时序、状态迁移或协作流程
- 方法论（详细设计视角）：
  - 必用：`状态机建模`
  - 必用：`规则决策表`
  - 必用：`前置/后置条件建模`
  - 可选：`并发与一致性分析`
- 输入：步骤 2 输出、requirements 主输出（按需）
- 输出：状态与算法/规则结论（写入主文档）
- 依赖关系：依赖步骤 2 完成

### 步骤 4：定义异常处理、测试与交接边界

- 操作主体：`G301-SKILL`
- 具体任务：
  - 识别异常场景、检测点、恢复/补偿/降级方案和可观测性要求
  - 定义可测试单元、关键测试场景、测试替身和验收方式
  - 固化接口交接边界与数据交接边界，供 `G302/G303` 消费
  - 必要时用 Mermaid 展示异常处理流程、测试覆盖关系或交接追溯关系
- 方法论（详细设计视角）：
  - 必用：`失败模式分析`
  - 必用：`可测试性分层设计`
  - 必用：`接口数据边界对齐`
  - 可选：`可观测性设计`
- 输入：步骤 2-3 输出、蓝图接口/数据相关内容
- 输出：异常、测试与交接边界结论（写入主文档）
- 依赖关系：依赖步骤 2-3 完成

### 步骤 5：生成组件详细设计文档

- 操作主体：`G301-SKILL`
- 具体任务：
  - 按模板整合章节并完成结构自检
  - 校验供 `G302/G303/DD-07` 消费的最小字段、编号和回链完整性
  - 持久化到目标路径
- 输入：步骤 1-4 输出
- 输出：`artifacts/detailed-design/002-component-design.md`
- 依赖关系：依赖步骤 1-4 完成

## 6. 与运行时台账对齐

推荐任务映射：

- `task_id`: `DD-04`
- `skill_id`: `G301`
- 生命周期口径：`DD-04` 负责 `drafting` 与返工后的再次起草；后续由 `G300` 推进 `DD-07=design-review-validation`、`DD-08=GS-Quality-Check`、`DD-09=GS-Review`
- 返工回路：`DD-07/DD-08/DD-09 -> DD-04(rework) -> drafting`

执行要求：

1. `DD-04` 只负责当前 Skill 的起草与返工后的再次起草。
2. `status_code/status_label/skill_stage/review_result/resume_from/evidence_path/updated_at` 的正式回写由 `G300` 在子代理验收后统一执行。
3. `DD-04` 起草完成后保持 `in_progress`，由 `G300` 决定是否汇总进入 `DD-07`，以及是否继续推进 `DD-08/DD-09`。
4. 本 Skill 只产出组件设计文档和结构化消费字段，不直接回写运行时状态，不直接推进共享门禁，也不关闭子代理。

## 7. 验收标准

### 7.1 执行检查闭环（强制）

为避免 `DD-07 design-review-validation` 汇总时再补结构字段，`G301` 在本 SKILL 内固定以下检查闭环：

| 项目 | 固定定义 |
|---|---|
| 汇总消费任务 | `DD-07=design-review-validation` |
| 质量检查工具 | `GS-Quality-Check` |
| 质量报告路径 | `artifacts/reviews/detailed-design-quality-check.md` |

1. 主文档存在且路径正确：`artifacts/detailed-design/002-component-design.md`。
2. 文档章节必须与 `template.md` 对齐，至少包含：`1. 设计目标与范围`、`2. 组件职责与协作`、`3. 内部结构与依赖`、`4. 状态转换与关键算法/规则`、`5. 异常处理与交接边界`、`6. 可测试性设计`、`7. 方法检查清单`、`8. 质量检查预组装对齐信息`、`9. 追溯与证据`。
3. 所有关键组件都必须至少覆盖职责、内部结构、异常处理和测试关注点；状态/规则如适用必须完整给出，不适用时需显式说明，不得只给组件列表。
4. 若正文使用 Mermaid 图，图中涉及的组件、状态、交互、测试点、异常对象或边界名称必须与表格中的稳定字段一致，不得引入未在结构化字段中定义的新核心对象名。
5. Mermaid 图遵循“复杂时必画，简单时可省略”原则；当关系简单且表格已足够清晰时，不要求为每一节强制补图。

## 8. 失败与恢复

1. 若 design plan、蓝图或技术策略缺失导致无法冻结组件范围，应由 `G300` 将当前任务判定为 `blocked`，并在 `resume_from` 写明缺失输入。
2. 若组件边界、接口责任归属、状态机规则或数据所有权无法收敛，应由 `G300` 保持当前任务 `in_progress` 并推进到 `rework`。
3. 恢复时优先读取 `artifacts/detailed-design/000-task-tracker.md` 的 `resume_from`。
4. 若评审不通过，视为当前轮不可交付并返工。

## 9. References

- [template.md](template.md)
- [role-definition.md](references/role-definition.md)
- [execution-details.md](references/execution-details.md)
- [G300 detailed design entry](../g300-detailed-design-entry/SKILL.md)
- [G203 architecture blueprint](../g203-architecture-blueprint/SKILL.md)
- [G204 architecture review](../g204-architecture-review/SKILL.md)
- [runtime-task-tracker-spec.md](../_shared/governance/runtime-task-tracker-spec.md)
- [quality-checker-requirements.md](../_shared/governance/quality-checker-requirements.md)
- [detailed-design-methods-catalog.md](../_shared/detailed-design-methods-catalog.md)
