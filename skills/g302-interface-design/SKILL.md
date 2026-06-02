---
name: g302-interface-design
description: 接口详细设计，用于在 `complete` 模式下消费 `G301` 组件交接边界，形成稳定的接口契约、交互语义、错误语义和供 `DD-07`、`GS-Quality-Check`、`GS-Review` 消费的结构化接口设计字段。
version: 1.0.0
---

# G302 接口详细设计 SKILL

## 元信息与执行契约

说明：完整机读契约以文档头部 YAML 为准；本章节仅提供执行摘要。

### 基本信息

| 项目 | 内容 |
|---|---|
| skill_id | `G302` |
| skill_type | `core` |
| 中文名称 | 接口详细设计 |
| 适用阶段 | `detailed_design` |
| 执行模式 | `complete` |
| 前置依赖 | `DD-01 ~ DD-03` 已收敛，`G300` 已冻结本轮接口设计输入，`G301` 已完成组件交接边界 |
| 后置依赖 | `DD-07`、`GS-Quality-Check`、`GS-Review` |
| 输出主文档 | `artifacts/detailed-design/003-interface-design.md` |

### 执行契约摘要

| 项目 | 内容 |
|---|---|
| 运行时任务映射 | `task_id=DD-05`，`skill_id=G302` |
| Skill 生命周期 | 主起草任务为 `DD-05`；后续由 `G300` 统一推进 `DD-07=design-review-validation`、`DD-08=GS-Quality-Check`、`DD-09=GS-Review` |
| 运行时台账路径 | `artifacts/detailed-design/000-task-tracker.md` |
| 证据路径 | `evidence/DD-05/` |
| 必选输入 | `artifacts/detailed-design/001-design-plan.md`、`artifacts/detailed-design/002-component-design.md`、`artifacts/architecture/003-architecture-blueprint.md`、`artifacts/architecture/001-technical-strategy.md` |
| 按需输入 | `artifacts/architecture/004-adr.md`、requirements 阶段主输出、`G300` 澄清记录 |
| 模板与参考 | `template.md`、`references/execution-details.md`、`references/role-definition.md`、`../_shared/detailed-design-methods-catalog.md` |
| 交付前置摘要 | 必须形成接口清单、契约字段、时序交互、错误语义、版本与幂等、可测试性和接口风险的结构化字段 |

## 1. 目标

在 `G300` 已冻结的 `complete` 模式和 `G301` 已输出的组件交接边界基础上，形成可执行的接口详细设计，明确：

1. 接口边界、提供方与消费方责任。
2. 请求、响应、异步消息或回调的契约语义。
3. 关键调用链、时序交互和超时/重试/补偿边界。
4. 错误语义、幂等、版本和兼容策略。
5. 可供 `DD-07`、`GS-Quality-Check`、`GS-Review` 直接消费的结构化最小字段。

## 2. 角色定义

`G302` 的角色边界、职责和输出风格见：

- [role-definition.md](references/role-definition.md)

`G302` 的实际执行记录与步骤细化统一使用以下本地文件：

- [template.md](template.md)
- [execution-details.md](references/execution-details.md)

执行要求：

1. `template.md`用于记录本轮输出细则。
2. `execution-details.md` 用于补足各步骤的推进条件、结束条件与回写要求。

## 3. 前置条件

1. `artifacts/detailed-design/001-design-plan.md` 已存在，且 `final_mode=complete`，`skills_to_run` 包含 `G302`。
2. `artifacts/detailed-design/002-component-design.md` 已存在且可读取，尤其是 `interface_handoff_contracts`、`component_catalog`、`state_transition_models`、`exception_handling_specs`。
3. `artifacts/architecture/003-architecture-blueprint.md` 与 `artifacts/architecture/001-technical-strategy.md` 可读取。
4. 当前任务映射固定为：`DD-05` 为起草任务；后续由 `G300` 联动推进 `DD-07=design-review-validation`、`DD-08=GS-Quality-Check`、`DD-09=GS-Review`。
5. 若 `G301` 未明确 `provider/consumer`、调用语义、错误语义边界或待细化接口项，应由 `G300` 先完成澄清后再触发当前 Skill。

## 4. 输入输出契约

### 4.1 输入

1. `artifacts/detailed-design/001-design-plan.md`（必选）
2. `artifacts/detailed-design/002-component-design.md`（必选）
3. `artifacts/architecture/003-architecture-blueprint.md`（必选）
4. `artifacts/architecture/001-technical-strategy.md`（必选）
5. `artifacts/architecture/004-adr.md`（按需）
6. requirements 阶段主输出与上游评审摘要（按需）
7. `G300` 澄清记录与工作假设（按需）

### 4.2 输出

1. 主输出：`artifacts/detailed-design/003-interface-design.md`
2. 证据目录：`evidence/DD-05/`

### 4.3 质量约束

1. 输出必须使用 Markdown。
2. 文档规模 `< 10000` 行；超限必须拆分且每个文件自包含。
3. 路径统一使用 `/`。
4. 对接口边界、关键时序交互、错误语义分层或版本兼容路径，若仅靠表格难以清晰表达，应用 Markdown 内嵌 Mermaid 图辅助说明；图形作为正文说明增强，不替代表格中的结构化字段。

## 5. 执行步骤

执行说明：

1. `G302` 由 detailed_design 阶段入口编排 SKILL `G300` 触发，并且仅在 `complete` 模式通过独立子代理执行。
2. 子代理仅负责本 Skill 文档产出；任务状态验收、台账回写、共享门禁推进和子代理关闭均由 `G300` 统一执行。

### 步骤 1：冻结接口设计范围与来源边界

- 操作主体：`G302-SKILL`
- 具体任务：
  - 从 design plan 与 component design 中冻结本轮接口设计范围
  - 识别必须定稿的接口项、延后项和来源约束
  - 建立 `G301.interface_handoff_contracts -> G302` 的承接映射
- 方法论（接口设计视角）：
  - 必用：`设计范围冻结`
  - 必用：`约束回链`
  - 必用：`契约驱动设计`
- 输入：`001-design-plan.md`、`002-component-design.md`
- 输出：范围与接口清单结论（写入主文档）
- 依赖关系：无

### 步骤 2：定义接口目录与契约字段

- 操作主体：`G302-SKILL`
- 具体任务：
  - 明确接口清单、提供方/消费方和交互类型
  - 细化请求、响应、消息体和字段约束
  - 对齐组件状态、异常场景和边界责任
  - 必要时用 Mermaid 展示接口边界图或契约分层关系图
- 方法论（接口设计视角）：
  - 必用：`契约驱动设计`
  - 必用：`契约一致性校验`
  - 必用：`接口数据边界对齐`
- 输入：步骤 1 输出、蓝图、技术策略
- 输出：接口目录与契约结论（写入主文档）
- 依赖关系：依赖步骤 1 完成

### 步骤 3：定义交互时序与错误语义

- 操作主体：`G302-SKILL`
- 具体任务：
  - 识别关键调用链、同步/异步时序、重试和超时路径
  - 定义错误码、失败语义、调用方责任和降级建议
  - 建立错误语义与组件异常/状态模型的回链
  - 必要时用 Mermaid 展示时序交互图或错误处理流程图
- 方法论（接口设计视角）：
  - 必用：`时序交互建模`
  - 必用：`错误语义分层`
  - 必用：`失败模式分析`
  - 必用：`幂等与重试语义设计`
- 输入：步骤 2 输出、`G301.state_transition_models`、`G301.exception_handling_specs`
- 输出：时序与错误语义结论（写入主文档）
- 依赖关系：依赖步骤 2 完成

### 步骤 4：定义版本、幂等、可观测与测试约束

- 操作主体：`G302-SKILL`
- 具体任务：
  - 明确版本策略、兼容规则、幂等键和顺序性约束
  - 设计日志、指标、追踪、安全要求和脱敏规则
  - 设计契约测试、集成测试和异常测试关注点
  - 必要时用 Mermaid 展示版本兼容路径图或测试覆盖关系图
- 方法论（接口设计视角）：
  - 必用：`兼容性策略设计`
  - 必用：`幂等与重试语义设计`
  - 必用：`可测试性分层设计`
  - 必用：`可观测性设计`
  - 必用：`契约一致性校验`
- 输入：步骤 2-3 输出、技术策略
- 输出：版本、治理与测试结论（写入主文档）
- 依赖关系：依赖步骤 2-3 完成

### 步骤 5：生成接口详细设计文档

- 操作主体：`G302-SKILL`
- 具体任务：
  - 按模板整合章节并完成结构自检
  - 校验供 `DD-07`、`GS-Quality-Check`、`GS-Review` 消费的最小字段、编号和回链完整性
  - 持久化到目标路径
- 输入：步骤 1-4 输出
- 输出：`artifacts/detailed-design/003-interface-design.md`
- 依赖关系：依赖步骤 1-4 完成

## 6. 与运行时台账对齐

推荐任务映射：

- `task_id`: `DD-05`
- `skill_id`: `G302`
- 生命周期口径：`DD-05` 负责 `drafting` 与返工后的再次起草；后续由 `G300` 推进 `DD-07=design-review-validation`、`DD-08=GS-Quality-Check`、`DD-09=GS-Review`
- 返工回路：`DD-07/DD-08/DD-09 -> DD-05(rework) -> drafting`

执行要求：

1. `DD-05` 只负责当前 Skill 的起草与返工后的再次起草。
2. `status_code/status_label/skill_stage/review_result/resume_from/evidence_path/updated_at` 的正式回写由 `G300` 在子代理验收后统一执行。
3. `DD-05` 起草完成后保持 `in_progress`，由 `G300` 决定是否汇总进入 `DD-07`，以及是否继续推进 `DD-08/DD-09`。
4. 本 Skill 只产出接口设计文档和结构化消费字段，不直接回写运行时状态，不直接推进共享门禁，也不关闭子代理。

## 7. 验收标准

### 7.1 执行检查闭环（强制）

为避免 `DD-07 design-review-validation` 汇总时再补接口结构字段，`G302` 在本 SKILL 内固定以下检查闭环：

| 项目 | 固定定义 |
|---|---|
| 汇总消费任务 | `DD-07=design-review-validation` |
| 质量检查工具 | `GS-Quality-Check` |
| 质量报告路径 | `artifacts/reviews/detailed-design-quality-check.md` |

1. 主文档存在且路径正确：`artifacts/detailed-design/003-interface-design.md`。
2. 文档章节必须与 `template.md` 对齐，至少包含：`1. 设计目标与范围`、`2. 接口目录与契约`（含 `2.1 接口清单` 的 `interface_type` 和 `2.3 前端消费契约`）、`3. 交互时序与错误语义`、`4. 版本、治理与测试约束`、`5. 可测试性设计`、`6. 方法检查清单`、`7. 质量检查预组装对齐信息`、`8. 追溯与证据`。
3. 所有关键接口都必须至少覆盖接口契约、错误语义、版本/幂等和测试关注点；时序交互如适用必须完整给出，不适用时需显式说明，不得只给接口列表。
4. `接口目录与契约`、`交互时序与错误语义`、`版本、治理与测试约束` 必须能明确说明调用方责任、边界责任、兼容规则和失败语义，不得只写“按系统默认处理”。
5. 第 `7` 章仅作为 `G300/DD-07` 预组装共享质量门时的占位信息，不作为 `G302` 单独通过与否的判定项。
6. 若正文使用 Mermaid 图，图中涉及的接口、错误码、版本策略、交互节点或测试点名称必须与表格中的稳定字段一致，不得引入未在结构化字段中定义的新核心对象名。
7. Mermaid 图遵循“复杂时必画，简单时可省略”原则；当接口数量少且交互关系简单时，不要求为每一节强制补图。

## 8. 失败与恢复

1. 若 design plan、component design 或蓝图缺失导致无法冻结接口范围，应由 `G300` 将当前任务判定为 `blocked`，并在 `resume_from` 写明缺失输入。
2. 若接口提供方/消费方责任、关键字段约束、版本策略或错误语义无法收敛，应由 `G300` 保持当前任务 `in_progress` 并推进到 `rework`。
3. 恢复时优先读取 `artifacts/detailed-design/000-task-tracker.md` 的 `resume_from`。
4. 若第 `6` 章最小消费字段不完整，或回链无法支撑 `DD-07/GS-*` 消费，视为当前轮不可交付并返工。

## 9. References

- [template.md](template.md)
- [role-definition.md](references/role-definition.md)
- [execution-details.md](references/execution-details.md)
- [G300 detailed design entry](../g300-detailed-design-entry/SKILL.md)
- [G301 component design](../g301-component-design/SKILL.md)
- [runtime-task-tracker-spec.md](../_shared/governance/runtime-task-tracker-spec.md)
- [quality-checker-requirements.md](../_shared/governance/quality-checker-requirements.md)
- [detailed-design-methods-catalog.md](../_shared/detailed-design-methods-catalog.md)
