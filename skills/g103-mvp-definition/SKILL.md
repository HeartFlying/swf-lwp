---
name: g103-mvp-definition
description: MVP 范围定义，用于从需求基线中收敛 in-scope/out-of-scope、验收标准和风险，形成最小可交付范围。
version: 1.0.0
---

# G103 MVP 范围定义 SKILL

## 元信息与执行契约

说明：完整机读契约以文档头部 YAML 为准；本章节仅提供执行摘要。

### 基本信息

| 项目 | 内容 |
|---|---|
| skill_id | `G103` |
| skill_type | `core` |
| 中文名称 | MVP 范围定义 |
| 适用阶段 | `requirements` |
| 执行模式 | `fast`、`standard`、`complete` |
| 前置依赖 | `RA-04`（`G102` 已完成） |
| 后置依赖 | 无（进入 requirements 阶段质量门与评审门） |
| 输出主文档 | `artifacts/requirements/004-mvp-definition.md` |

### 执行契约摘要

| 项目 | 内容 |
|---|---|
| 运行时任务映射 | 主起草任务为 `RA-05`；质量检查与用户评审分别承接到共享服务任务 `RA-06(GS-Quality-Check)`、`RA-07(GS-Review)`；`skill_id` 维持各任务原定义，不重写为 `G103` |
| Skill 生命周期 | `drafting -> quality_check -> user_review(stage_gate=RA-07) -> completed`（返工回路：`quality_check/user_review -> rework -> drafting`） |
| 运行时台账路径 | `artifacts/requirements/000-task-tracker.md` |
| 证据路径 | `evidence/RA-05/` |
| 必选输入 | `artifacts/requirements/003-requirements-baseline.md` |
| 按需输入 | `artifacts/requirements/002-business-context.md`、用户补充业务约束 |
| 模板与参考 | `template.md`、`references/role-definition.md`、`references/execution-details.md` |
| 质量门摘要 | `overall_status` 仅允许 `pass/pass_with_warning`，且不得有 `critical/major` 问题 |

## 1. 目标

从需求基线中冻结 MVP 的最小可交付范围，明确 in-scope/out-of-scope、发布门槛与风险，形成可执行的范围边界文档。

## 2. 前置条件

1. `RA-04` 已完成，并已产出 `artifacts/requirements/003-requirements-baseline.md`。
2. `G102` 的 `FR/NFR/CST` 及优先级结果可解析，且关键约束已收敛。
3. 当前任务映射固定为：`RA-05` 为起草任务；质量门复用 `RA-06/RA-07`。

## 3. 输入输出契约

### 3.1 输入

1. `artifacts/requirements/003-requirements-baseline.md`（必选）
2. `artifacts/requirements/002-business-context.md`（按需）
3. 用户补充的时间、资源、业务优先级约束（按需）

### 3.2 输出

1. 主输出：`artifacts/requirements/004-mvp-definition.md`
2. 证据目录：`evidence/RA-05/`

### 3.3 供 AD-Agent 消费的最小字段

1. `mvp_scope.in_scope`：MVP 纳入项（含需求 ID、价值、依赖）。
2. `mvp_scope.out_of_scope`：MVP 明确不纳入项（含延后原因）。
3. `mvp_acceptance`：MVP 整体与条目级验收标准。
4. `mvp_risks`：技术/业务/项目风险及缓解策略。
5. `release_gate`：发布门槛和未决事项解除条件。
6. `arch_input.functional_dependencies`：in-scope 功能间依赖关系与耦合点。
7. `arch_input.iteration_priority_map`：按架构交付节奏分组的功能集。
8. `arch_input.nfr_hard_constraints`：MVP 发布前必须满足的 NFR 及架构影响。
9. `arch_input.nfr_soft_constraints`：可延后的 NFR 及当前降级口径。
10. `arch_input.architecture_sensitive_risks`：影响架构决策的风险及设计阶段需闭合的假设。

### 3.4 质量约束

1. 输出必须使用 Markdown。
2. 文档规模 `< 10000` 行；超限必须拆分且每个文件自包含。
3. 路径统一使用 `/`。
4. 每个 in-scope 条目必须可追溯到 `G102` 需求 ID 与对应约束。

### 3.5 方法与示例引用

1. 方法库基线：[requirements-methods-catalog.md](../_shared/requirements-methods-catalog.md)（用于术语和方法定义对齐）。
2. 执行细则：`references/execution-details.md`（用于步骤级约束与时间基线）。
3. 示例输出：`examples/sample-004-mvp-definition.md`（用于格式与粒度对齐）。

## 4. 执行步骤

执行说明：

1. `G103` 由 requirements 阶段入口编排 SKILL `G100` 触发，并必须在独立子代理中执行。
2. 子代理仅负责本 Skill 文档产出；状态回写由阶段宿主 `RA-Agent` 统一执行。

### 步骤 1：MVP 核心功能识别

- 操作主体：`G103-SKILL`
- 具体任务：
  - 从需求基线提取全部 `Must` 优先级功能，**所有 Must 必须纳入 MVP 候选清单**（Must 不可 out-of-scope）
  - 从需求基线提取全部 `Should` 优先级功能，**所有 Should 必须纳入 MVP 候选清单**（Should 不可 out-of-scope）
  - `Could` 默认不纳入，仅在有特殊业务约束时考虑
  - 评估每条候选功能的业务价值与可交付必要性
  - 形成 MVP 候选清单，标注每条来源需求的基线优先级（Must/Should/Could）
- 方法论（产品经理视角）：
  - 必用：`第一性原理`
  - 必用：`问题风暴`
  - 必用：`决策树`
  - 可选：`角色扮演`
- 输入：`003-requirements-baseline.md`
- 输出：MVP 候选清单（写入主文档）
- 依赖关系：无
- 时间建议：`30-45` 分钟；超时需在 `resume_from` 记录阻塞点和剩余问题。
- 超时回写模板：`step_id`、`elapsed_min`、`blocker`、`pending_questions`、`next_action`、`evidence_ref`。

### 步骤 2：MVP 范围边界定义

- 操作主体：`G103-SKILL`
- 具体任务：
  - 明确 in-scope/out-of-scope，**in-scope 必须包含基线中全部 `Must` 和全部 `Should` 需求**
  - `Could` 明确排除，标记延后版本与回归触发条件
  - 形成范围边界规则：**Must 全覆盖 + Should 全覆盖** → Could 延后
- 方法论（产品经理视角）：
  - 必用：`约束映射`
  - 必用：`解决方案矩阵`
  - 必用：`六顶思考帽`
  - 可选：`假设反转`
- 输入：步骤 1 输出、`CST` 约束清单
- 输出：范围边界定义（写入主文档）
- 依赖关系：依赖步骤 1 完成
- 时间建议：`30-45` 分钟；若边界争议未收敛，先产出候选方案并进入澄清。
- 超时回写模板：`step_id`、`elapsed_min`、`blocker`、`pending_questions`、`next_action`、`evidence_ref`。

### 步骤 3：MVP 验收标准定义

- 操作主体：`G103-SKILL`
- 具体任务：
  - 定义 MVP 整体验收标准
  - 定义条目级验收标准
  - 定义发布门槛
- 方法论（产品经理视角）：
  - 必用：`解决方案矩阵`
  - 必用：`失败分析`
  - 必用：`决策树`
  - 可选：`SCAMPER`
- 输入：步骤 1、2 输出
- 输出：验收标准定义（写入主文档）
- 依赖关系：依赖步骤 2 完成
- 时间建议：`20-30` 分钟；不得以描述性语言替代可验证标准。
- 超时回写模板：`step_id`、`elapsed_min`、`blocker`、`pending_questions`、`next_action`、`evidence_ref`。

### 步骤 4：MVP 风险识别

- 操作主体：`G103-SKILL`
- 具体任务：
  - 识别技术、业务、项目风险
  - 评估概率、影响与缓解策略
  - 标记发布阻断风险
- 方法论（产品经理视角）：
  - 必用：`失败分析`
  - 必用：`约束映射`
  - 必用：`六顶思考帽`
  - 可选：`类比思维`
- 输入：步骤 2、3 输出
- 输出：风险清单（写入主文档）
- 依赖关系：可与步骤 3 并行执行
- 时间建议：`20-30` 分钟；至少覆盖技术/业务/项目三类风险各 1 项。
- 超时回写模板：`step_id`、`elapsed_min`、`blocker`、`pending_questions`、`next_action`、`evidence_ref`。

### 步骤 5：生成 MVP 范围文档

- 操作主体：`G103-SKILL`
- 具体任务：
  - 按模板整合章节并完成结构自检
  - 校验追溯关系、路径格式、编号一致性
  - 产出架构关键输入摘要（功能依赖关系、迭代优先级映射、NFR 约束分级、架构敏感风险）
  - 持久化到目标路径
- 输入：步骤 1-4 输出
- 输出：`artifacts/requirements/004-mvp-definition.md`
- **术语补充**（新增）：
  - MVP 范围边界描述中涉及的领域术语应已存在于 `artifacts/requirements/CONTEXT.md`（如该文件已存在）
  - 若出现新术语，补充定义并增量写入 `artifacts/requirements/CONTEXT.md`
  - out-of-scope 功能涉及的关键术语也应记录，避免后续混淆
- 依赖关系：依赖步骤 1-4 完成
- 时间建议：`15-25` 分钟；输出前必须完成追溯完整性自检。
- 超时回写模板：`step_id`、`elapsed_min`、`blocker`、`pending_questions`、`next_action`、`evidence_ref`。

## 5. 与运行时台账对齐

推荐任务映射：

- `task_id`: `RA-05`（起草主任务）
- `skill_id`: `G103`
- Skill 生命周期：`drafting -> quality_check -> user_review(stage_gate=RA-07) -> completed`
- 返工回路：`quality_check/user_review -> rework -> drafting`

执行要求：

1. `RA-05` 负责 `drafting` 与返工后的再次起草；`RA-06` 负责 `quality_check`；`RA-07` 负责 `user_review`。
2. 状态变更时同步更新当前任务的 `status_code/status_label/skill_stage/resume_from/evidence_path/updated_at`。
3. `RA-05` 起草完成后保持 `in_progress`，由 `RA-Agent` 推进到 `RA-06/RA-07`。
4. 质量检查结果写入质量报告字段，不写入 `review_result`。

## 6. 验收标准

### 6.1 执行检查闭环（强制）

为避免质量门数据来源后置，`G103` 在本 SKILL 内固定以下检查闭环：

| 项目 | 固定定义 |
|---|---|
| 质量检查工具 | `GS-Quality-Check` |
| 触发任务 | `RA-06` |
| 质量报告路径 | `artifacts/reviews/requirements-quality-check.md` |
| 最小字段 | `quality_check_summary.overall_status`、`quality_check_summary.scores.completeness`、`quality_check_summary.scores.traceability`、`quality_check_summary.scores.markdown_format`、`validation_summary.issue_count.critical`、`validation_summary.issue_count.major`、`validation_summary.issue_count.minor` |
| 消费任务 | `RA-07`（阶段汇总评审）与本 SKILL 第 6 章验收判断 |
| 缺失处理 | 任一最小字段缺失即判定当前轮不通过，不得推进 `done` |

1. 主文档存在且路径正确：`artifacts/requirements/004-mvp-definition.md`。
2. 文档章节与 `template.md` 对齐，至少包含：`1. MVP 摘要`、`2. MVP 功能候选清单`、`3. 范围边界（In/Out）`、`4. 验收标准与发布门槛`、`5. 风险清单`、`6. 追溯与证据`、`7. 架构关键输入摘要`、`8. AD-Agent 消费字段映射`。
3. 每个 in-scope 条目需具备来源需求 ID、优先级依据、验收标准与风险映射。
4. **基线中所有 `Must` 和所有 `Should` 需求均有对应的 MVP-ID 映射（Must + Should 全覆盖检查），无任何 Must 或 Should 被遗漏或排除在 out-of-scope 中。**
5. 质量检查结果来源必须为 `artifacts/reviews/requirements-quality-check.md`，并满足：`quality_check_summary.overall_status` 为 `pass` 或 `pass_with_warning`，且 `validation_summary.issue_count` 中 `critical/major` 问题数量均为 `0`（字段缺失视为不通过）。
6. 不引入治理层未定义字段作为通过条件。
7. `evidence/RA-05/` 目录非空，至少包含 1 份过程证据文件（MVP范围决策过程、in-scope/out-of-scope判定依据、迭代优先级映射依据、风险识别过程）。
8. `G103` 输出须满足 `AD-Agent` 消费最小字段要求。

## 7. 失败与恢复

1. 若关键输入缺失导致无法继续，标记 `blocked`，在 `resume_from` 写明解除条件。
2. 若 in-scope/out-of-scope 边界不清或追溯断链，保持 `in_progress` 并进入 `rework`。
3. 恢复时优先读取 `artifacts/requirements/000-task-tracker.md` 的 `resume_from`。
4. 若缺少发布门槛定义或关键风险缓解方案，视为不可交付并返工。
