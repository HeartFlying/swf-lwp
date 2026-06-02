---
name: g300-detailed-design-entry
description: detailed_design 阶段入口编排 SKILL，负责消费 architecture 交接产物，进行模式消费、澄清分流，编排 G301/G302/G303、GS-Quality-Check 和 GS-Review，维护阶段任务台账、阶段交接记录、恢复闭环和子代理执行闭环。
version: 1.2.0
disable-model-invocation: false
argument-hint: [user-request]
---

# G300 Detailed Design Entry SKILL

## 元信息与执行契约

说明：`G300` 是 `detailed_design` 阶段当前入口编排 SKILL。它只定义阶段入口的控制面，不替代 `G301/G302/G303` 的专业设计产出。

### 基本信息

| 项目 | 内容 |
|---|---|
| skill_id | `G300` |
| skill_type | `core` |
| 中文名称 | detailed_design 阶段入口编排 |
| 适用阶段 | `detailed_design` |
| 执行模式 | `standard`、`complete` |
| 前置依赖 | 上游 `architecture` 阶段交接产物、`artifacts/detailed-design/000-task-tracker.md`、共享治理与 manifest 契约 |
| 后置依赖 | `G301`、`G302`（条件）、`G303`（条件）、`reviewing-software-design`、`GS-Quality-Check`、`GS-Review` |
| 输出主文档 | `artifacts/detailed-design/001-design-plan.md` |
| 入口属性 | 阶段入口编排 SKILL，负责 detailed_design 的模式消费、路由、门禁、交接与恢复 |

### 执行契约摘要

| 项目 | 内容 |
|---|---|
| 运行时任务映射 | `DD-01` 到 `DD-11` 的入口编排 |
| 运行时台账路径 | `artifacts/detailed-design/000-task-tracker.md` |
| 必选输入 | `architecture_outputs`、`review_outputs`、`change_outputs`、`final_mode` |
| 按需输入 | `mode_preference`、已有 `000-task-tracker.md`、本地治理 references |
| 关键引用 | `references/role-definition.md`、`references/execution-details.md`、`template.md`、`../_shared/governance/*.md` |
| 入口属性 | 当前阶段正式入口编排 SKILL，负责 detailed_design 阶段的模式消费、路由生成、质量门与评审门推进 |

## 1. 目标

承载 `detailed_design` 阶段全部入口编排能力，覆盖：

1. 上游 `architecture` 交接消费与阶段上下文建立
2. 模式消费与模式一致性校验
3. 澄清分流与恢复中断后的续跑
4. `G301/G302/G303` 的路由控制
5. `reviewing-software-design`、`GS-Quality-Check` 与 `GS-Review` 的阶段门推进
6. 阶段交接前置判断与正式交接记录写入

## 2. 角色定义

`G300` 的角色定义、边界、决策优先级和输出风格见：

- [role-definition.md](references/role-definition.md)

执行时应将其视为本 SKILL 的角色说明基线。

### 2.1 执行模板与细化说明

`G300` 的实际执行记录与步骤细化统一使用以下本地文件：

- [template.md](template.md)
- [execution-details.md](references/execution-details.md)

执行要求：

1. `template.md` 用于记录本轮入口编排的模式判定、执行清单、门禁结果与交接摘要。
2. `execution-details.md` 用于补足各步骤的推进条件、结束条件、回写要求与恢复闭环。

## 3. 前置条件

1. `artifacts/architecture/000-task-tracker.md` 或上游交接内容可读，且能定位本次 `detailed_design` 输入。
2. `artifacts/detailed-design/000-task-tracker.md` 结构符合 [runtime-task-tracker-spec.md](../_shared/governance/runtime-task-tracker-spec.md)。
3. 上游 `final_mode` 必须可读，或由用户在本轮显式确认覆盖。
4. `G301`、`G302`、`G303`、`GS-Quality-Check`、`GS-Review` 的路径在 manifest 中可解析。

## 4. 输入输出契约

### 4.1 输入

1. 上游 `architecture_outputs` 与 `review_outputs`
2. `change_outputs` 或变更回传记录
3. `final_mode` 与 `mode_preference`（按需）
4. `artifacts/detailed-design/000-task-tracker.md`（恢复执行时必读）
5. 本地治理 references：
   - [runtime-task-tracker-spec.md](../_shared/governance/runtime-task-tracker-spec.md)
   - [quality-checker-requirements.md](../_shared/governance/quality-checker-requirements.md)
6. 本地执行辅助：
   - [template.md](template.md)
   - [execution-details.md](references/execution-details.md)

### 4.2 输出

1. `artifacts/detailed-design/001-design-plan.md`
2. `recommended_mode`
3. `final_mode`
4. `mode_source`
5. `mode_decision_basis`
6. `clarification_required`
7. `missing_fields`
8. `clarification_questions`
9. `working_assumptions`
10. `risk_if_unanswered`
11. `skills_to_run`
12. `skills_skipped`
13. `detailed_design_outputs`
14. `review_outputs`
15. `change_outputs`
16. `review_summary`
17. `handoff_summary`
18. `handoff_record`
19. `artifacts/detailed-design/007-engineering-readiness-review.md`

### 4.3 供恢复与下游消费的最小字段

1. `recommended_mode`
2. `final_mode`
3. `mode_source`
4. `mode_decision_basis`
5. `clarification_required`
6. `resume_from`
7. `detailed_design_outputs`
8. `review_outputs`
9. `change_outputs`
10. `review_summary.decision`
11. `review_summary.pass_rate`
12. `engineering_readiness`
13. `handoff_summary`

### 4.4 输出约束

1. 路径统一使用项目根相对路径与 `/` 分隔符。
2. 所有状态变更必须同步回写 `artifacts/detailed-design/000-task-tracker.md`。
3. `G300` 只负责编排与推进，不直接替代 `G301/G302/G303` 的主文档产出。

## 5. 决策与编排规则

### 5.1 模式消费规则

1. 优先消费上游已确认的 `final_mode`。
2. 若上游模式缺失、不可读或与当前交接内容冲突，当前阶段必须转 `blocked` 并请求补齐或用户确认。
3. `detailed_design` 只消费 `standard` 与 `complete`；若上游模式为 `fast`，必须直接阻塞并要求补正模式，不得强行进入详细设计执行。
4. 用户显式覆盖模式时，必须记录 `mode_source=user_override`，并说明覆盖原因与生效范围。

### 5.2 路由差异

| skill_id | standard | complete | 说明 |
|---|---|---|---|
| `G301` | execute | execute | 组件详细设计，始终执行 |
| `G302` | **conditional** | execute | 接口详细设计；standard 模式下若存在 `has_frontend_ui=yes` 的 MVP 则强制执行，否则跳过 |
| `G303` | skip | execute | 数据详细设计，仅在 `complete` 执行 |

### 5.3 澄清闭环

1. 组件边界、接口契约、数据归属、主键/索引策略、幂等性语义或一致性规则不清晰时，必须发起澄清。
2. 每轮澄清最多 3 轮。
3. 每轮澄清至少记录 `clarification_questions`、`working_assumptions`、`risk_if_unanswered`。
4. 关键信息收敛后才能进入 `G301`；若无法收敛，必须保留风险并阻塞交接。

### 5.4 子代理执行规则

1. `G301/G302/G303/GS-Quality-Check/GS-Review` 的实际执行必须通过独立子代理启动。
2. 一个子代理一次只承载一个后续 SKILL。
3. 子代理启动时必须显式绑定：目标 SKILL、输入路径、输出路径、验收要求、回写任务位。
4. 子代理结果完成后，必须先验收并完成台账回写，再关闭该子代理。
5. 未通过验收不得直接关闭子代理；已通过验收不得长期保留子代理驻留。

### 5.5 门禁与交接规则

1. `reviewing-software-design`（DD-08）必须先于 `GS-Quality-Check`（DD-09）。
2. `GS-Quality-Check` 必须先于 `GS-Review`。
3. `reviewing-software-design` 的 `review_result` 必须为 `pass` 或 `pass_with_conditions` 才能推进到 `DD-09`。
4. `critical=0`、`major=0` 才能推进到评审门。
5. `review_summary.decision=pass` 且 `review_summary.pass_rate >= 85` 才能推进交接。
6. 若 `reviewing-software-design` 的 `review_result=pass_with_conditions`，非阻塞问题可并行关闭，但阻塞问题必须清零。
7. 交接前必须写入正式阶段交接记录，且记录字段必须对齐 `handoff_id/from_stage/to_stage/required_outputs/review_gate/status/notes/updated_at`。

## 6. 执行步骤

### 步骤 1：初始化阶段上下文与输入溯源

#### 1.1 输入优先级读取（强制顺序）

按以下优先级顺序读取输入，低优先级仅作为校验参考：

| 优先级 | 文档路径 | 读取章节 | 用途 | 缺失处理 |
|:---:|---|---|---|---|
| P0 | `artifacts/architecture/000-task-tracker.md` | 阶段交接记录 | 确定交接状态 | blocked，等待上游就绪 |
| P1 | `artifacts/architecture/003-architecture-blueprint.md` | 1.2 范围边界 (SCP-XXX) | 获取架构范围项 | blocked，缺失核心输入 |
| P2 | `artifacts/architecture/003-architecture-blueprint.md` | 3.1 MVP In-Scope 功能覆盖映射 | 获取 SCP→MVP/FR 映射 | blocked，缺失核心输入 |
| P3 | `artifacts/requirements/004-mvp-definition.md` | 3.1 In-scope | 获取功能描述基准 | blocked，缺失核心输入 |
| P4 | `artifacts/requirements/003-requirements-baseline.md` | 功能需求清单 | 追溯 FR 原始定义 | warning，继续但记录 |
| P5 | `artifacts/architecture/001-architecture-intake.md` | 3.2 范围 | 辅助参考 | skip，非必需 |

**约束**：
- P0~P3 任一缺失 → 立即 `blocked`，不得进入 1.2
- P1 与 P3 内容冲突 → 采信 P1，但记录冲突并触发澄清

#### 1.2 功能范围收敛（三联表建立）

建立 SCP-MVP-FR 三联映射表，作为阶段内统一功能范围基准：

| SCP-ID | MVP-ID | FR-ID | 功能描述（以 P3 为准） | 优先级 | 组件覆盖 |
|---|---|---|---|---|---|
| SCP-001 | MVP-001 | FR-001 | （从 004-mvp-definition.md 提取） | Must | CMP-XXX |
| ... | ... | ... | ... | ... | ... |

**收敛规则**：
1. 功能描述必须以 P3 (004-mvp-definition.md) 为准，不得重新描述
2. FR-ID 仅作为追溯字段，阶段内引用统一使用 MVP-ID
3. 优先级必须与 P3 保持一致
4. 组件覆盖从 P2 (蓝图 3.1 章) 提取

#### 1.3 一致性校验门（强制阻断）

执行 V-01 ~ V-06 检查点，任一阻断项失败即停止：

| 检查点 | 校验内容 | 执行顺序 | 失败处理 |
|:---:|:---|:---:|:---|
| V-01 | 范围数量一致性：`len(SCP-in-scope) == len(MVP-in-scope)` | 3 | **blocked**，触发澄清 |
| V-02 | 编号系统收敛：统一使用 MVP-XXX，禁止 FR-XXX 作为主体引用 | 2 | warning，自动收敛到 MVP-XXX |
| V-03 | 功能描述一致性：`hash(蓝图描述)` vs `hash(MVP描述)` 差异 < 20% | 4 | warning，记录差异 |
| V-04 | 组件覆盖完整性：所有 MVP 均有组件映射（非空）；`has_frontend_ui=yes` 的 MVP，其组件映射中必须至少包含一个 `frontend_consumer=yes` 的组件；`has_frontend_ui=yes` 的 MVP 必须标记为"需产出前后端接口契约" | 5 | **blocked**，补全或澄清 |
| V-05 | 系统名称一致性：检测"车牌识别"/"LPR"/"实时识别"等非 HTVT 系统关键词 | 1 | **blocked**，提示"数据源可能来自其他项目" |
| V-06 | 前端界面映射一致性：`has_frontend_ui=yes` 的 MVP 必须有非空 `uiux_ref` | 6 | **blocked**，补全前端界面映射 |

**执行约束**：
- 阻断项（V-05, V-01, V-04, V-06）失败 → 立即停止，不得进入 1.5
- 警告项（V-02, V-03）触发 → 记录 `working_assumptions`，可继续

#### 1.4 异常分流

| 异常场景 | 自动处理 |
|---|---|
| V-01 范围数量不一致 | 转 `DD-03` 澄清，`clarification_required=yes`，记录差异项 |
| V-02/V-03 警告 | 记录 `working_assumptions`，说明收敛/差异处理方式 |
| V-04 组件覆盖不完整 | blocked，列出未覆盖 MVP，要求补全映射或澄清 |
| V-06 前端界面映射不一致 | blocked，列出缺失 uiux_ref 的 MVP，要求补全前端界面映射 |
| V-05 检测到异系统关键词 | blocked，错误信息："检测到数据源可能来自其他项目，当前系统关键词 '[词]' 与蓝图系统名称 '[系统]' 不符，请确认 P1~P3 输入正确" |


#### 1.5 初始化确认输出

写入 `001-design-plan.md`，**必须包含**以下章节：

1. **1.1 输入摘要** → 上游交接产物清单
2. **1.2 范围基线** → SCP-MVP-FR 三联映射表（阶段内权威）
3. **1.3 输入溯源与校验报告**（新增强制章节）→ V-01~V-06 执行结果

**输出约束**：
- 未通过校验门（存在阻断项）→ 不得写入 `001-design-plan.md`
- `001-design-plan.md` 必须可读、可验证、可作为恢复辅助

### 步骤 2：执行模式判定

- 读取上游 `final_mode`
- 若上游模式缺失、非法或冲突，转 `blocked` 并请求补齐或用户确认
- 产出 `recommended_mode`、`final_mode`、`mode_source`、`mode_decision_basis`
- 若模式为 `fast`，直接阻塞并请求用户或上游补正

### 步骤 3：判定是否澄清

- 若存在冻结失败项，推进 `DD-03`
- 若无需澄清，按 `no-op` 收口
- 每轮澄清后必须重新校验模式与范围边界

### 步骤 4：生成执行清单

- `standard`：`G301 -> G302(conditional) -> GS-Quality-Check -> GS-Review`
  - 注：`G302` 在 `standard` 模式下仅当存在 `has_frontend_ui=yes` 的 MVP 时执行，否则跳过
- `complete`：`G301 -> G302 -> G303 -> GS-Quality-Check -> GS-Review`
- 产出 `skills_to_run`
- 标记 `skills_skipped`

### 步骤 5：登记任务状态与证据路径

- 回写 `task_id/skill_id/skill_stage/step_name/description/inputs/outputs/dependencies/status_code/status_label/review_result/resume_from/evidence_path/updated_at`
- 初始化 detailed_design 阶段任务位 `DD-01 ~ DD-11`

### 步骤 6：触发 `G301`

- 通过独立子代理启动 `G301`
- `G301` 固定执行
- 子代理结果验收通过并完成 `DD-04` 回写后关闭该子代理

### 步骤 7：触发 `G302`（`complete` 或 `conditional`）

- `complete` 模式下通过独立子代理启动 `G302`，必须执行
- `standard` 模式下，若存在 `has_frontend_ui=yes` 的 MVP，则强制执行 `G302`；否则跳过，不启动子代理，并回写原因
- 子代理结果验收通过并完成 `DD-05` 回写后关闭该子代理

### 步骤 8：触发 `G303`（仅 `complete`）

- `complete` 模式下通过独立子代理启动 `G303`
- `standard` 模式固定跳过，不启动子代理，并回写原因
- `complete` 模式必须执行
- 子代理结果验收通过并完成 `DD-06` 回写后关闭该子代理

### 步骤 9：推进 `reviewing-software-design` 工程可实现性评审

- 通过独立子代理启动 `reviewing-software-design`
- 输入至少包含 `G301/G302/G303` 产物与 `DD-07` 追溯文档
- 输出 `artifacts/detailed-design/007-engineering-readiness-review.md`
- 验收要求：报告包含结论、分数、否决状态、阻塞/非阻塞问题数、整改计划、工程开工准备度
- `standard` 模式下接口/数据分类标记为"不适用"并提供理由
- 子代理结果验收通过并完成 `DD-08` 回写后关闭该子代理
- 若存在否决项、阻塞问题、分数 < 60 或 Engineering readiness = `Not ready`，禁止进入 `DD-09`，进入 rework

### 步骤 10：推进设计评审验证与质量门

- 汇总 `G301/G302/G303` 输出并形成 `DD-07`
- 通过独立子代理启动 `GS-Quality-Check`
- 消费 `GS-Quality-Check` 输出，并在推进 `GS-Review` 前先归一化为 `quality_gate_ref`
- 子代理结果验收通过并完成 `DD-09` 回写后关闭该子代理
- 若存在 `critical/major`，禁止进入评审门

### 步骤 11：推进评审门

- 通过独立子代理启动 `GS-Review`
- 先将 `GS-Quality-Check` 输出归一化为 `quality_gate_ref`
- 消费质量门结果与正式设计文档
- 子代理结果验收通过并完成 `DD-10` 回写后关闭该子代理
- `decision=fail` 时，必须回写 `skill_stage=rework + status_code=in_progress + status_label=进行中 + review_result=rework + resume_from=首个 owner_task_id`
- `decision=pending` 时，必须回写 `skill_stage=user_review + status_code=blocked + review_result=blocked + resume_from=DD-10`

### 步骤 12：生成交接前置判断

- 当评审通过后，生成 `handoff_summary`
- 同步写入 `handoff_record`
- 明确 `detailed_design_outputs/review_outputs/change_outputs` 是否可消费
- 完成 `DD-11` 并允许阶段交接

## 7. 与运行时台账对齐

1. `G300` 自身不单独占用新 task_id，而是驱动 `DD-01 ~ DD-11`。
2. 所有状态回写必须落到 `artifacts/detailed-design/000-task-tracker.md`。
3. `DD-05`、`DD-06` 在 `standard` 模式下必须保留为任务位，但以 `status_code=done`、`skill_stage=completed`、`review_result=skipped` 收口。
4. `DD-03` 未触发澄清时，必须回写 `done/completed` 且 `review_result=no-op`。
5. `DD-09/DD-10` 的门禁结果必须与质量报告和评审报告保持一致。
6. 恢复时仅以 `000-task-tracker.md` 作为运行时恢复主锚点；`001-design-plan.md` 与 `template.md` 只作为辅助证据，不得作为恢复前置依赖。

## 8. 验收标准

1. 能生成 detailed_design 阶段最小执行清单与模式判定结果。
2. 能明确 `G301` 必执行，`G302` 在 `standard` 模式下条件执行、`complete` 模式下必执行，`G303` 仅在 `complete` 执行。
3. 能对齐 `reviewing-software-design` 先于 `GS-Quality-Check` 先于 `GS-Review` 的门禁顺序。
4. 能基于 `reviewing-software-design` 输出工程开工准备度结论，且阻塞问题未清零时禁止进入下游门禁。
5. 能输出可供恢复与下游阶段消费的 `detailed_design_outputs`、`review_outputs`、`change_outputs`、`review_summary` 与 `handoff_summary`。
6. 不与现有 `G301/G302/G303`、`reviewing-software-design`、`GS-*`、manifest 契约冲突。
7. 能基于 `template.md` 形成一次完整入口编排记录，且字段与 `000-task-tracker.md` 可相互映射。

## 9. 失败与恢复

1. 若上游交接产物缺失或无法冻结，标记 `blocked`。
2. 若模式为 `fast` 或模式冲突未收敛，必须阻塞并请求补正为 `standard/complete`。
3. 若 `G301` 失败，保持 `in_progress` 并进入返工。
4. 若 `G302/G303` 在 `complete` 中任一失败，保持 `in_progress` 并进入返工，不得跳过质量门。
5. 若 `reviewing-software-design`（DD-08）未通过（否决项触发、Not ready、分数 < 60），回写 `skill_stage=rework + status_code=in_progress + review_result=rework + resume_from=首个 owner_task_id`。
6. 若 DD-08 存在阻塞问题，保持 `in_progress` 并进入返工；返工完成后必须重新执行 `DD-07` 和 `DD-08`，不得跳过。
7. 若质量门未通过，禁止进入 `GS-Review`。
8. 若评审未通过，必须以 `rework/blocked` 的合法台账组合回写，不得写入完成交接。
9. 恢复时仅以 `000-task-tracker.md` 作为运行时恢复主锚点；`001-design-plan.md` 与 `template.md` 只作为辅助证据。

## 10. References

本 SKILL 的本地 references 目录如下：

1. [role-definition.md](references/role-definition.md)
2. [execution-details.md](references/execution-details.md)
3. [template.md](template.md)
4. [runtime-task-tracker-spec.md](../_shared/governance/runtime-task-tracker-spec.md)
5. [quality-checker-requirements.md](../_shared/governance/quality-checker-requirements.md)
