---
name: g303-data-design
description: Complete-mode data detailed design for detailed_design stage. Use when G300 has frozen scope and technical strategy, G301 has produced data_handoff_contracts, and Codex needs to draft broad data design covering data objects, ownership, storage boundaries, lifecycle, consistency, evolution, migration risk, and DD-06 outputs.
version: 1.0.0
---

# G303 数据详细设计 SKILL

## 元信息与执行契约

说明：完整机读契约以文档头部 YAML 为准；本章节仅提供执行摘要。

### 基本信息

| 项目 | 内容 |
|---|---|
| skill_id | `G303` |
| skill_type | `core` |
| 中文名称 | 数据详细设计 |
| 适用阶段 | `detailed_design` |
| 执行模式 | `complete` |
| 前置依赖 | `DD-01 ~ DD-03` 已收敛，`G300` 已冻结本轮数据设计输入，`G301` 已完成组件交接边界，且 `artifacts/detailed-design/001-design-plan.md`、`artifacts/architecture/001-technical-strategy.md` 可读取 |
| 后置依赖 | `DD-07`、`GS-Quality-Check`、`GS-Review` |
| 输出主文档 | `artifacts/detailed-design/004-data-design.md` |

### 执行契约摘要

| 项目 | 内容 |
|---|---|
| 运行时任务映射 | `task_id=DD-06`，`skill_id=G303` |
| Skill 生命周期 | 主起草任务为 `DD-06`；后续由 `G300` 统一推进 `DD-07=design-review-validation`、`DD-08=GS-Quality-Check`、`DD-09=GS-Review` |
| 运行时台账路径 | `artifacts/detailed-design/000-task-tracker.md` |
| 证据路径 | `evidence/DD-06/` |
| 必选输入 | `artifacts/detailed-design/001-design-plan.md`、`artifacts/detailed-design/002-component-design.md`、`artifacts/architecture/003-architecture-blueprint.md`、`artifacts/architecture/001-technical-strategy.md` |
| 按需输入 | `artifacts/detailed-design/003-interface-design.md`、`artifacts/architecture/004-adr.md`、requirements 阶段主输出、`G300` 澄清记录 |
| 模板与参考 | `template.md`、`references/execution-details.md`、`references/role-definition.md`、`../_shared/detailed-design-methods-catalog.md` |
| 交付前置摘要 | 必须形成数据对象、所有权与读写边界、存储边界、生命周期/状态、Consistency/演化/迁移、异常处理、可测试性和风险的结构化字段 |

## 1. 目标

在 `G300` 已冻结的 `complete` 模式和 `G301` 已输出的组件交接边界基础上，形成可执行的数据详细设计，明确：

1. 数据对象、属性族、关系、聚合边界和生命周期。
2. 数据所有权、读写边界、消费语义和存储边界。
3. 一致性级别、并发语义、版本演化、迁移与回填风险。
4. 异常处理、可观测性和可测试性设计。
5. 可供 `DD-07`、`GS-Quality-Check`、`GS-Review` 直接消费的结构化最小字段。

## 2. 角色定义

`G303` 的角色边界、职责和输出风格见：

- [role-definition.md](references/role-definition.md)

`G303` 的实际执行记录与步骤细化统一使用以下本地文件：

- [template.md](template.md)
- [execution-details.md](references/execution-details.md)

执行要求：

1. `template.md`用于记录本轮输出细则。
2. `execution-details.md` 用于补足各步骤的推进条件、结束条件与回写要求。

## 3. 前置条件

1. `artifacts/detailed-design/001-design-plan.md` 已存在，且 `final_mode=complete`，`skills_to_run` 包含 `G303`。
2. `artifacts/detailed-design/002-component-design.md` 已存在且可读取，尤其是 `data_handoff_contracts`、`component_catalog`、`responsibility_matrix`、`state_transition_models`、`exception_handling_specs`。
3. `artifacts/architecture/003-architecture-blueprint.md` 与 `artifacts/architecture/001-technical-strategy.md` 可读取。
4. `artifacts/detailed-design/003-interface-design.md` 若存在，应作为数据消费语义的补充约束读取，但不得覆盖 `G301.data_handoff_contracts` 的主契约。
5. 当前任务映射固定为：`DD-06` 为起草任务；后续由 `G300` 联动推进 `DD-07=design-review-validation`、`DD-08=GS-Quality-Check`、`DD-09=GS-Review`。
6. 若关键数据对象边界、所有权、读写语义、存储边界或迁移约束仍未冻结，应由 `G300` 先完成澄清后再触发当前 Skill。

## 4. 输入输出契约

### 4.1 输入

1. `artifacts/detailed-design/001-design-plan.md`（必选）
2. `artifacts/detailed-design/002-component-design.md`（必选）
3. `artifacts/architecture/003-architecture-blueprint.md`（必选）
4. `artifacts/architecture/001-technical-strategy.md`（必选）
5. `artifacts/detailed-design/003-interface-design.md`（按需）
6. `artifacts/architecture/004-adr.md`（按需）
7. requirements 阶段主输出与上游评审摘要（按需）
8. `G300` 澄清记录与工作假设（按需）

### 4.2 输出

1. 主输出：`artifacts/detailed-design/004-data-design.md`
2. 证据目录：`evidence/DD-06/`

### 4.3 质量约束

1. 输出必须使用 Markdown。
2. 文档规模 `< 10000` 行；超限必须拆分且每个文件自包含。
3. 路径统一使用 `/`。
4. 设计重点必须覆盖数据对象、存储边界、一致性、演化、迁移与恢复风险，不得只写数据库物理结构。
5. 对数据关系、存储边界、生命周期、迁移路径或异常恢复，若仅靠表格难以清晰表达，应用 Markdown 内嵌 Mermaid 图辅助说明；图形作为正文说明增强，不替代表格中的结构化字段。

## 5. 执行步骤

执行说明：

1. `G303` 由 detailed_design 阶段入口编排 SKILL `G300` 触发，并且仅在 `complete` 模式通过独立子代理执行。
2. 子代理仅负责本 Skill 文档产出；任务状态验收、台账回写、共享门禁推进和子代理关闭均由 `G300` 统一执行。

### 步骤 1：冻结数据设计范围与来源边界

- 操作主体：`G303-SKILL`
- 具体任务：
  - 从 design plan、component design 与 architecture 中冻结本轮数据设计范围
  - 识别必须定稿的数据对象、延后项和来源约束
  - 建立 `G301.data_handoff_contracts -> G303` 的承接映射，并以 `data_contract_id` 作为稳定主键
- 方法论（数据设计视角）：
  - 必用：`设计范围冻结`
  - 必用：`约束回链`
  - 必用：`数据对象建模`
  - 可选：`风险热点预判`
- 输入：`001-design-plan.md`、`002-component-design.md`
- 输出：范围与数据对象清单结论（写入主文档）
- 依赖关系：无

### 步骤 2：定义数据对象、所有权与存储边界

- 操作主体：`G303-SKILL`
- 具体任务：
  - 明确核心数据对象、属性族、关系和生命周期归属
  - 细化所有权、写入责任、读取视图、消费语义和边界责任
  - 设计逻辑/物理存储边界、访问层次和扩展点
  - 必要时用 Mermaid 展示数据关系图、边界图或读写流向图
- 方法论（数据设计视角）：
  - 必用：`数据对象建模`
  - 必用：`读写边界分析`
  - 必用：`契约驱动设计`
  - 必用：`接口数据边界对齐`
  - 输入：步骤 1 输出、`G301.data_handoff_contracts`、蓝图数据视图、`artifacts/detailed-design/001-design-plan.md`、`artifacts/architecture/001-technical-strategy.md`
- 输出：对象、所有权与存储边界结论（写入主文档）
- 依赖关系：依赖步骤 1 完成

### 步骤 3：定义生命周期、一致性与演化/迁移策略

- 操作主体：`G303-SKILL`
- 具体任务：
  - 识别数据状态、状态迁移、保留/归档/删除和恢复要求
  - 设计一致性级别、并发约束、冲突处理和可见性规则
  - 设计版本演化、兼容窗口、字段变更、双写/双读、回填和回滚策略
  - 必要时用 Mermaid 展示状态迁移图、演化路径图或迁移流程图
- 方法论（数据设计视角）：
  - 必用：`一致性与演化设计`
  - 必用：`数据保留与归档策略设计`
  - 必用：`并发与一致性分析`
  - 必用：`前置/后置条件建模`
  - 可选：`失败模式分析`
  - 可选：`迁移切换策略设计`
- 输入：步骤 2 输出、requirements 主输出（按需）
- 输出：生命周期、一致性与演化/迁移结论（写入主文档）
- 依赖关系：依赖步骤 2 完成

### 步骤 4：定义异常处理、测试与风险闭环

- 操作主体：`G303-SKILL`
- 具体任务：
  - 识别异常场景、检测点、恢复/补偿/降级方案和可观测性要求
  - 定义数据契约测试、`handoff_contract` / `boundary` 级测试点、迁移测试、回填测试、恢复测试和观察点
  - 固化迁移风险、`ownership_boundary` / `data_handoff` / `boundary` 级风险对象、回滚条件和待确认项，供 `DD-07` 与评审门消费
  - 必要时用 Mermaid 展示异常处理流程、测试覆盖关系或迁移回退路径
- 方法论（数据设计视角）：
  - 必用：`失败模式分析`
  - 必用：`迁移切换策略设计`
  - 必用：`可测试性分层设计`
  - 必用：`可观测性设计`
  - 可选：`约束回链`
- 输入：步骤 2-3 输出、蓝图数据相关内容
- 输出：异常、测试与风险结论（写入主文档）
- 依赖关系：依赖步骤 2-3 完成

### 步骤 5：生成数据详细设计文档

- 操作主体：`G303-SKILL`
- 具体任务：
  - 按模板整合章节并完成结构自检
  - 校验供 `G300`、`G301`、`DD-07` 与 `GS-*` 消费的最小字段、编号和回链完整性
  - 持久化到目标路径
- 输入：步骤 1-4 输出
- 输出：`artifacts/detailed-design/004-data-design.md`
- 依赖关系：依赖步骤 1-4 完成

## 6. 与运行时台账对齐

推荐任务映射：

- `task_id`: `DD-06`
- `skill_id`: `G303`
- 生命周期口径：`DD-06` 负责 `drafting` 与返工后的再次起草；后续由 `G300` 推进 `DD-07=design-review-validation`、`DD-08=GS-Quality-Check`、`DD-09=GS-Review`
- 返工回路：`DD-07/DD-08/DD-09 -> DD-06(rework) -> drafting`

执行要求：

1. `DD-06` 只负责当前 Skill 的起草与返工后的再次起草。
2. `status_code/status_label/skill_stage/review_result/resume_from/evidence_path/updated_at` 的正式回写由 `G300` 在子代理验收后统一执行。
3. `DD-06` 起草完成后保持 `in_progress`，由 `G300` 决定是否汇总进入 `DD-07`，以及是否继续推进 `DD-08/DD-09`。
4. 本 Skill 只产出数据设计文档和结构化消费字段，不直接回写运行时状态，不直接推进共享门禁，也不关闭子代理。

## 7. 验收标准

### 7.1 执行检查闭环（强制）

为避免 `DD-07 design-review-validation` 汇总时再补数据结构字段，`G303` 在本 SKILL 内固定以下检查闭环：

| 项目 | 固定定义 |
|---|---|
| 汇总消费任务 | `DD-07=design-review-validation` |
| 质量检查工具 | `GS-Quality-Check` |
| 质量报告路径 | `artifacts/reviews/detailed-design-quality-check.md` |

1. 主文档存在且路径正确：`artifacts/detailed-design/004-data-design.md`。
2. 文档章节必须与 `template.md` 对齐，至少包含：`1. 设计目标与范围`、`2. 数据对象、所有权与边界`、`3. 生命周期、状态与存储边界`、`4. 一致性、演化与迁移`、`5. 异常处理、可测试性与风险`、`6. 方法检查清单`、`7. 质量检查预组装对齐信息`、`8. 追溯与证据`。
3. 所有关键数据对象都必须至少覆盖所有权、存储边界、一致性、生命周期和测试关注点；状态/演化/迁移如适用必须完整给出，不适用时需显式说明，不得只给对象列表。
4. `数据对象、所有权与边界`、`生命周期、状态与存储边界`、` 一致性、演化与迁移`、`异常处理、可测试性与风险`, 必须能明确说明 owner/consumer、边界责任、兼容规则和失败语义，不得只写“按系统默认处理”。
5. 第 `7` 章仅作为 `G300/DD-07` 预组装共享质量门时的占位信息，不作为 `G303` 单独通过与否的判定项。
6. 若正文使用 Mermaid 图，图中涉及的数据对象、状态、迁移路径、异常对象或边界名称必须与表格中的稳定字段一致，不得引入未在结构化字段中定义的新核心对象名。
7. Mermaid 图遵循“复杂时必画，简单时可省略”原则；当对象关系简单且表格已足够清晰时，不要求为每一节强制补图。

## 8. 失败与恢复

1. 若 design plan、component design 或蓝图缺失导致无法冻结数据范围，应由 `G300` 将当前任务判定为 `blocked`，并在 `resume_from` 写明缺失输入。
2. 若数据对象边界、所有权、存储边界、一致性策略、版本演化或迁移约束无法收敛，应由 `G300` 保持当前任务 `in_progress` 并推进到 `rework`。
3. 恢复时优先读取 `artifacts/detailed-design/000-task-tracker.md` 的 `resume_from`。
4. 若评审不通过，视为当前轮不可交付并返工。

## 9. References

- [template.md](template.md)
- [role-definition.md](references/role-definition.md)
- [execution-details.md](references/execution-details.md)
- [G300 detailed design entry](../g300-detailed-design-entry/SKILL.md)
- [G301 component design](../g301-component-design/SKILL.md)
- [G302 interface design](../g302-interface-design/SKILL.md)
- [runtime-task-tracker-spec.md](../_shared/governance/runtime-task-tracker-spec.md)
- [quality-checker-requirements.md](../_shared/governance/quality-checker-requirements.md)
- [detailed-design-methods-catalog.md](../_shared/detailed-design-methods-catalog.md)
