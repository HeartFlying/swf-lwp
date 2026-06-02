---
name: g204-architecture-review
description: 架构评审验证，用于基于 G203 蓝图、ADR 与上游架构约束形成 architecture 阶段正式评审验证文档，并为 GS-Quality-Check 预组装其所需的文档级输入字段。
version: 0.1.0
---

# G204 架构评审验证 SKILL

## 元信息与执行契约

说明：完整机读契约以文档头部 YAML 为准；本章节仅提供执行摘要。

### 基本信息

| 项目 | 内容 |
|---|---|
| skill_id | `G204` |
| skill_type | `core` |
| 中文名称 | 架构评审验证 |
| 适用阶段 | `architecture` |
| 执行模式 | `fast`、`standard`、`complete` |
| 前置依赖 | `AD-05`（`G203` 已完成） |
| 后置依赖 | `GS-Quality-Check` |
| 输出主文档 | `artifacts/architecture/005-architecture-review-validation.md` |

### 执行契约摘要

| 项目 | 内容 |
|---|---|
| 运行时任务映射 | `task_id=AD-06`，`skill_id=G204` |
| Skill 生命周期 | 主起草任务为 `AD-06`；质量检查与用户评审分别承接到共享服务任务 `AD-07(GS-Quality-Check)`、`AD-08(GS-Review)`；`skill_id` 维持各任务原定义，不重写为 `G204` |
| 运行时台账路径 | `artifacts/architecture/000-task-tracker.md` |
| 证据路径 | `evidence/AD-06/` |
| 必选输入 | `artifacts/architecture/003-architecture-blueprint.md`、`artifacts/architecture/004-adr.md`、`artifacts/architecture/001-technical-strategy.md`、`artifacts/architecture/002-architecture-vision.md` |
| 按需输入 | `artifacts/architecture/001-architecture-intake.md`、`artifacts/reviews/001-requirements-review.md`、requirements 阶段交接摘要 |
| 模板与参考 | `template.md`、`references/execution-details.md`、`references/role-definition.md`、`../_shared/architecture-methods-catalog.md` |
| 质量门摘要 | `overall_status` 仅允许 `pass/pass_with_warning`，且不得有 `critical/major` 问题 |

## 1. 目标

对 architecture 阶段已形成的愿景、技术策略、蓝图与 ADR 进行一次结构化评审验证，明确：

1. 蓝图是否真实承接上游愿景、策略与约束
2. 关键质量属性、风险和实现边界是否在蓝图中得到覆盖
3. 当前 architecture 文档包是否具备进入 `GS-Quality-Check` 的条件
4. 需要返工的事项、证据和下一步动作

## 2. 角色定义

`G204` 的角色边界、职责和输出风格见：

- [role-definition.md](references/role-definition.md)

`G204` 的实际执行记录与步骤细化统一使用以下本地文件：

- [template.md](template.md)
- [execution-details.md](references/execution-details.md)

执行要求：

1. `template.md`用于记录本轮输出细则。
2. `execution-details.md` 用于补足各步骤的推进条件、结束条件与回写要求。

## 3. 前置条件

1. `AD-05` 已完成，并已产出 `artifacts/architecture/003-architecture-blueprint.md`。
2. `artifacts/architecture/004-adr.md` 已存在，且能与蓝图中的关键决策对应。
3. `artifacts/architecture/001-technical-strategy.md` 与 `artifacts/architecture/002-architecture-vision.md` 可读取。
4. 当前任务映射固定为：`AD-06` 为起草任务；质量门和评审门由 `AD-07/AD-08` 统一承接。

## 4. 输入输出契约

### 4.1 输入

1. `artifacts/architecture/003-architecture-blueprint.md`（必选）
2. `artifacts/architecture/004-adr.md`（必选）
3. `artifacts/architecture/001-technical-strategy.md`（必选）
4. `artifacts/architecture/002-architecture-vision.md`（必选）
5. `artifacts/architecture/001-architecture-intake.md`（按需）
6. requirements 阶段交接摘要与 `artifacts/reviews/001-requirements-review.md`（按需）

### 4.2 输出

1. 主输出：`artifacts/architecture/005-architecture-review-validation.md`
2. 证据目录：`evidence/AD-06/`

### 4.3 供 GS-Quality-Check 预组装的部分输入字段

说明：

1. `G204` 只负责产出文档级评审结果及其结构化字段，不直接构成 `GS-Quality-Check` 的完整执行输入。
2. `stage`、`quality_task_id`、`tracker_path` 以及共享服务运行时上下文由 `G200` 在触发 `AD-07` 时补齐。

1. `target_documents`：以 `document_id` 结构化记录当前 architecture 正式文档包，至少包含 `path`、`required`、`document_role`、`produced_by`、`status`。
2. `g203_review_targets`：以 `target_id` 结构化记录 `G203` 提供的 `blueprint_scope / architecture_views / coverage_declaration / component_inventory / data_architecture / interface_architecture / interaction_flows / deployment_topology / adr_index / blueprint_risks / adr_contract` 对应评审对象及检查状态。
3. `review_findings`：以 `finding_id` 结构化记录评审发现、严重级别、关联文档、处理建议和证据引用。
4. `quality_gate_readiness`：以 `check_id` 结构化记录进入 `GS-Quality-Check` 前的必备检查项、状态、缺口和补齐说明。
5. `rework_actions`：以 `action_id` 结构化记录返工动作、责任文档、触发条件和完成判据。

### 4.4 质量约束

1. 输出必须使用 Markdown。
2. 文档规模 `< 10000` 行；超限必须拆分且每个文件自包含。
3. 路径统一使用 `/`。
4. 所有评审结论必须标注来源文档、验证依据或未决假设。

## 5. 执行步骤

执行说明：

1. `G204` 由 architecture 阶段入口编排 SKILL `G200` 触发，并必须在独立子代理中执行。
2. 子代理仅负责本 Skill 文档产出；任务状态验收、台账回写和关闭动作均由 `G200` 统一执行。

### 步骤 1：冻结评审范围与文档包

- 操作主体：`G204-SKILL`
- 具体任务：
  - 确认本轮 architecture 正式文档包范围
  - 明确本轮评审要覆盖的蓝图、ADR、策略和愿景输入
  - 形成 `target_documents`
- 方法论（架构视角）：
  - 必用：`系统上下文图`
  - 必用：`架构原则约束映射`
  - 必用：`约束分层法`
  - 可选：`假设清单与验证计划`
- 输入：蓝图、ADR、技术策略、架构愿景
- 输出：评审范围与文档包结论（写入主文档）
- 依赖关系：无

### 步骤 2：验证蓝图与上游架构约束的一致性

- 操作主体：`G204-SKILL`
- 具体任务：
  - 验证蓝图是否承接架构目标、驱动和策略约束
  - 验证关键决策是否与 ADR 和技术策略一致
  - 识别结构缺口、约束漂移和未闭环事项
- 方法论（架构视角）：
  - 必用：`架构原则约束映射`
  - 必用：`技术域分层分析`
  - 必用：`ADR 思维`
  - 必用：`蓝图追溯映射`
  - 可选：`视图一致性检查`
  - 可选：`替代路线与触发条件分析`
- 输入：步骤 1 输出、蓝图、ADR、技术策略、架构愿景
- 输出：一致性验证结论（写入主文档）
- 依赖关系：依赖步骤 1 完成

### 步骤 3：验证质量属性、风险与权衡闭环

- 操作主体：`G204-SKILL`
- 具体任务：
  - 验证关键质量属性是否在蓝图中得到响应
  - 检查权衡结论与风险缓解是否被真实承接
  - 标记仍需返工或补证的事项
- 方法论（架构视角）：
  - 必用：`质量属性场景`
  - 必用：`ATAM 权衡分析`
  - 必用：`风险驱动分析`
  - 必用：`视图一致性检查`
  - 可选：`风险驱动决策`
- 输入：步骤 2 输出、架构愿景、技术策略、蓝图
- 输出：质量与风险验证结论（写入主文档）
- 依赖关系：依赖步骤 2 完成

### 步骤 4：形成评审结论与返工动作

- 操作主体：`G204-SKILL`
- 具体任务：
  - 汇总通过项、问题项和返工项
  - 形成 `review_findings`、`quality_gate_readiness`、`rework_actions`
  - 明确是否具备进入 `GS-Quality-Check` 的条件
- 方法论（架构视角）：
  - 必用：`风险驱动决策`
  - 必用：`假设清单与验证计划`
  - 必用：`ADR 思维`
  - 可选：`替代路线与触发条件分析`
- 输入：步骤 1-3 输出
- 输出：评审结论与返工动作（写入主文档）
- 依赖关系：依赖步骤 1-3 完成

### 步骤 5：生成架构评审验证文档

- 操作主体：`G204-SKILL`
- 具体任务：
  - 按模板整合章节并完成结构自检
  - 校验供 `GS-Quality-Check` 消费的最小字段和路径格式
  - 持久化到目标路径
- 输入：步骤 1-4 输出
- 输出：`artifacts/architecture/005-architecture-review-validation.md`
- 依赖关系：依赖步骤 1-4 完成

## 6. 与运行时台账对齐

推荐任务映射：

- `task_id`: `AD-06`
- `skill_id`: `G204`
- 生命周期口径：`AD-06` 负责 `drafting` 与返工后的再次起草；`AD-07` 负责 `quality_check`；`AD-08` 负责 `user_review`
- 返工回路：`AD-07/AD-08 -> AD-06(rework) -> drafting`

执行要求：

1. `AD-06` 只负责当前 Skill 的起草与返工后的再次起草。
2. `status_code/status_label/skill_stage/review_result/resume_from/evidence_path/updated_at` 的正式回写由 `G200` 在子代理验收后统一执行。
3. `AD-06` 起草完成后保持 `in_progress`，由 `G200` 推进到 `AD-07/AD-08`。
4. 本 Skill 只产出结构化评审验证内容和质量门所需的文档级部分输入字段，不直接推进共享门禁。

## 7. 验收标准

### 7.1 执行检查闭环（强制）

为避免质量门数据来源后置，`G204` 在本 SKILL 内固定以下检查闭环：

| 项目 | 固定定义 |
|---|---|
| 质量检查工具 | `GS-Quality-Check` |
| 触发任务 | `AD-07` |
| 质量报告路径 | `artifacts/reviews/architecture-quality-check.md` |
| G204 最小预组装字段 | `target_documents`、`g203_review_targets`、`review_findings`、`quality_gate_readiness`、`rework_actions` |
| 消费任务 | `G200` 在预组装并推进 `AD-07` 前的门禁准备校验；`AD-08` 仅消费 `GS-Quality-Check` 的正式输出 |
| 缺失处理 | 任一 `G204` 最小预组装字段缺失即判定当前轮 `G204` 产出不可提交给 `G200` 进入 `AD-07` |

1. 主文档存在且路径正确：`artifacts/architecture/005-architecture-review-validation.md`。
2. 文档章节必须与 `template.md` 对齐，至少包含：`1. 评审范围与文档包`、`2. 一致性验证`、`3. 质量与风险验证`、`4. 评审结论与返工动作`、`5. 供 GS-Quality-Check 预组装的部分输入字段`、`6. 方法检查清单`、`7. 质量检查对齐信息`、`8. 追溯与证据`。
3. `GS-Quality-Check` 预组装字段必须在 `template.md` 第 5 章结构化填写并完整可解析，其中 `g203_review_targets` 必须完整承接 `G203` 的结构化最小消费字段，至少覆盖 `coverage_declaration / data_architecture / interface_architecture` 的评审对象。
4. `quality_gate_readiness` 中若存在 `status=blocked` 的检查项，当前轮视为不可交付。
5. 所有 `review_findings` 必须关联来源文档、严重级别和处理建议。

## 8. 失败与恢复

1. 若蓝图、ADR 或技术策略缺失导致无法完成验证，应由 `G200` 将当前任务判定为 `blocked`，并在 `resume_from` 写明缺失输入。
2. 若评审结论无法收敛或仍存在结构性缺口，应由 `G200` 保持当前任务 `in_progress` 并推进到 `rework`。
3. 恢复时优先读取 `artifacts/architecture/000-task-tracker.md` 的 `resume_from`。
4. 若供 `GS-Quality-Check` 预组装的部分输入字段不完整，视为当前轮不可交付并返工。

## 9. References

- [template.md](template.md)
- [role-definition.md](references/role-definition.md)
- [execution-details.md](references/execution-details.md)
- [architecture-methods-catalog.md](../_shared/architecture-methods-catalog.md)
- [runtime-task-tracker-spec.md](../_shared/governance/runtime-task-tracker-spec.md)
- [G200 architecture entry](../g200-architecture-entry/SKILL.md)
- [GS-Quality-Check](../gs-quality-check/SKILL.md)
- [GS-Review](../gs-review/SKILL.md)
