---
name: g200-architecture-entry
description: architecture 阶段入口编排 SKILL，负责模式消费、澄清分流、G202/G201/G203/G204 编排、阶段门禁推进与阶段交接前置判断，并复用 skills/_shared 下的共享治理与入口编排流程。
version: 1.1.0
disable-model-invocation: false
argument-hint: [user-request]
---

# G200 Architecture Entry SKILL

## 元信息与执行契约

说明：`G200` 是 architecture 阶段当前入口编排 SKILL。其角色定义、阶段专属细则与共享治理契约共同定义 architecture 阶段的入口执行方式。

### 基本信息

| 项目 | 内容 |
|---|---|
| skill_id | `G200` |
| skill_type | `core` |
| 中文名称 | 架构阶段入口编排 |
| 适用阶段 | `architecture` |
| 执行模式 | `fast`、`standard`、`complete`（默认消费上游冻结模式） |
| 前置依赖 | `requirements` 阶段已完成交接；`artifacts/requirements/000-task-tracker.md`、requirements 阶段交接记录可读取 |
| 后置依赖 | `G202`、`G201`、`G203`、`G204`、`GS-Quality-Check`、`GS-Review` |
| 输出主文档 | `artifacts/architecture/001-architecture-intake.md` |

### 执行契约摘要

| 项目 | 内容 |
|---|---|
| 运行时任务映射 | `AD-01` 到 `AD-09` 的入口编排 |
| 运行时台账路径 | `artifacts/architecture/000-task-tracker.md` |
| 必选输入 | requirements 阶段交接输出、`final_mode`、`user_request` 或等效阶段请求上下文 |
| 按需输入 | `mode_preference`、已有 `000-task-tracker.md`、本地治理 references |
| 关键引用 | `references/role-definition.md`、`references/execution-details.md`、`template.md`、`../_shared/governance/*.md`、`../g202-architecture-vision/SKILL.md`、`../g201-technical-strategy/SKILL.md`、`../g203-architecture-blueprint/SKILL.md`、`../g204-architecture-review/SKILL.md`、`../gs-quality-check/SKILL.md`、`../gs-review/SKILL.md` |
| 入口属性 | 当前阶段正式入口编排 SKILL，负责 architecture 阶段的模式消费、路由生成、门禁推进与阶段交接前置判断 |

## 1. 目标

承载 architecture 阶段全部入口编排能力，覆盖：

1. requirements 阶段交接输入接收与 intake 建立
2. 模式消费、模式一致性校验与澄清分流
3. `G202/G201/G203/G204` 触发顺序控制
4. `GS-Quality-Check` 与 `GS-Review` 的阶段门推进
5. `AD-09` 的阶段交接前置判断

## 2. 角色定义

`G200` 的角色定义、边界、决策优先级和输出风格见：

- [role-definition.md](references/role-definition.md)

执行时应将其视为本 SKILL 的角色说明基线。

## 2.1 执行模板与细化说明

`G200` 的实际执行记录与步骤细化统一使用以下本地文件：

- [template.md](template.md)
- [execution-details.md](references/execution-details.md)

执行要求：

1. `template.md` 用于记录本轮入口编排的模式判定、执行清单、门禁结果与交接摘要。
2. `execution-details.md` 用于补足各步骤的推进条件、结束条件与回写要求。

## 3. 前置条件

1. `artifacts/requirements/000-task-tracker.md` 结构必须符合 [runtime-task-tracker-spec.md](../_shared/governance/runtime-task-tracker-spec.md)。
2. requirements 阶段交接记录必须存在，且 `review_gate` 已通过。
3. `final_mode` 必须在上游交接中可读，或由用户在当前轮显式确认覆盖。
4. `G202/G201/G203/G204/GS-*` 已具备可调用定义。

## 4. 输入输出契约

### 4.1 输入

1. requirements 阶段交接输出
2. `user_request` 或等效阶段请求上下文
3. `final_mode` 与 `mode_preference`（按需）
4. `artifacts/architecture/000-task-tracker.md`（恢复执行时必读）
5. 本地治理 references：
   - [input-completeness-scoring-spec.md](../_shared/governance/input-completeness-scoring-spec.md)
   - [runtime-task-tracker-spec.md](../_shared/governance/runtime-task-tracker-spec.md)
   - [quality-checker-requirements.md](../_shared/governance/quality-checker-requirements.md)
6. 本地执行辅助：
   - [template.md](template.md)
   - [execution-details.md](references/execution-details.md)
7. 共享服务契约：
   - `../gs-quality-check/SKILL.md`
   - `../gs-review/SKILL.md`

### 4.2 输出

1. `artifacts/architecture/001-architecture-intake.md`
2. `artifacts/architecture/000-task-tracker.md`

### 4.3 输出约束

1. 路径统一使用项目根相对路径与 `/` 分隔符。
2. 所有状态变更必须同步回写 `000-task-tracker.md`。
3. `G200` 不直接替代 `G202/G201/G203/G204` 的主文档产出，只负责编排与推进。

## 5. 决策与编排规则

### 5.1 模式消费顺序

1. 优先消费 requirements 阶段已冻结的 `final_mode`。
2. 若上游 `final_mode` 缺失、非法或与交接内容冲突，当前阶段必须转 `blocked` 并请求补齐或用户确认，不得自行继续执行。
3. 若用户显式覆盖模式且不违反硬约束，则以用户覆盖为准，并记录 `mode_source=user_override`。
4. 模式消费结果必须输出 `recommended_mode`、`final_mode`、`mode_source`、`mode_decision_basis`。

### 5.2 模式一致性校验

1. `mode_source` 允许值固定为：`upstream`、`user_override`。
2. `recommended_mode` 默认等于上游 `final_mode`；仅当用户显式覆盖时，才允许与上游不一致。
3. 用户覆盖前必须校验 `input-completeness-scoring-spec.md` 中的 `total_score`、`D1`、`D2`、`D3` 阈值，不得违反共享硬约束。
4. `mode_decision_basis` 必须写明上游模式值、评分结果、是否存在用户覆盖，以及为什么当前模式仍稳定。
5. 若 `G100` 未交接 `final_mode`，`G200` 不存在“默认继续执行”的本地兜底逻辑，必须转 `blocked` 并请求补齐或用户确认。

### 5.3 澄清触发规则

满足以下任一条件必须发起澄清：

1. requirements 交接摘要或交接记录缺失关键字段
2. architecture 目标、边界、约束、验收标准任一无法冻结
3. 上游模式与用户覆盖或当前交接约束冲突且无法直接收敛
4. 下游输入依赖存在不可解析缺口

### 5.4 模式下的内部编排

1. `fast`：`G202 -> G201 -> G203 -> G204 -> GS-Quality-Check -> GS-Review`
2. `standard`：`G202 -> G201 -> G203 -> G204 -> GS-Quality-Check -> GS-Review`
3. `complete`：`G202 -> G201 -> G203 -> G204 -> GS-Quality-Check -> GS-Review`
4. 当前 `G200` 在三种模式下都不跳过任何 architecture 阶段核心 SKILL；模式差异只影响模式来源、记录口径、澄清和门禁说明，不改变核心执行链。
5. 因此，只要前置条件满足且 `final_mode` 已完成交接或已被用户显式确认，`G200` 就可以直接开始执行。

### 5.5 共享服务门禁规则

1. `AD-07(GS-Quality-Check)` 必须先于 `AD-08(GS-Review)`。
2. `quality_check_summary.overall_status` 非 `pass/pass_with_warning` 时，禁止推进 `AD-08`。
3. 启动 `AD-08` 前，必须先将 `GS-Quality-Check` 原始输出归一化为 `quality_gate_ref`，不得把 `quality_check_summary`、`validation_summary` 作为并列输入直接传给 `GS-Review`。
4. `AD-08` 通过前，禁止推进 `AD-09`。
5. 门禁结果必须同时回写到 `template.md` 中的“质量门与评审门”章节。

### 5.6 子代理执行规则

1. `G202/G201/G203/G204/GS-Quality-Check/GS-Review` 的实际执行必须通过独立子代理启动。
2. 每个子代理一次只承载一个后续 SKILL，不得在同一子代理中并发执行多个核心 SKILL。
3. 子代理启动时必须显式绑定：目标 SKILL、输入路径、输出路径、验收要求、回写任务位。
4. 子代理产出完成后，必须先完成结果验收与状态回写，再关闭该子代理。
5. 未完成验收前不得关闭子代理；已确认通过验收后不得保持子代理长期驻留。

## 6. 执行步骤

### 步骤 1：初始化阶段上下文

- 建立或读取 `artifacts/architecture/000-task-tracker.md`
- 初始化 `AD-01`
- 产出 `001-architecture-intake.md`
- 校验治理契约、模式契约与 workflow manifest 可用性

### 步骤 2：消费模式并判定是否澄清

- 读取 requirements 阶段 `final_mode` 与交接记录
- 若上游模式可用，优先消费；若不可用，转 `blocked` 并请求补齐或用户确认
- 输出 `mode_source`、`recommended_mode`、`final_mode`、`mode_decision_basis`
- 若存在恢复上下文，保留已有 `resume_from`

### 步骤 3：执行澄清闭环

- 若满足澄清条件，推进 `AD-02`
- 若无需澄清，按 `no-op` 收口 `AD-02`
- 每轮澄清后必须重新校验模式稳定性
- 最多连续 3 轮澄清；超限后输出工作假设与风险
- 澄清记录必须至少包含 `clarification_questions`、`working_assumptions`、`risk_if_unanswered`

### 步骤 4：生成执行清单

- `fast`：`G202 -> G201 -> G203 -> G204 -> GS-Quality-Check -> GS-Review`
- `standard`：`G202 -> G201 -> G203 -> G204 -> GS-Quality-Check -> GS-Review`
- `complete`：`G202 -> G201 -> G203 -> G204 -> GS-Quality-Check -> GS-Review`
- 产出 `skills_to_run`
- 标记 `skills_skipped`
- **严格禁止并行执行以上编排的SKILL,必须按照固定顺序逐一触发子代理执行**，不得跳过任何核心 SKILL

### 步骤 5：登记任务状态与证据路径

- 回写 `task_id/skill_id/skill_stage/step_name/description/inputs/outputs/dependencies/status_code/status_label/review_result/resume_from/evidence_path/updated_at`
- 初始化 architecture 阶段任务位 `AD-01 ~ AD-09`

### 步骤 6：触发 `G202`

- 通过独立子代理启动 `G202`
- 固定触发 `G202`
- 消费 requirements 阶段交接输出
- 子代理结果验收通过并完成状态回写后关闭该子代理
- 失败时保持 `in_progress` 并进入 `rework`

### 步骤 7：触发 `G201`

- 通过独立子代理启动 `G201`
- 固定触发 `G201`
- 消费 `G202` 产物
- 子代理结果验收通过并完成状态回写后关闭该子代理
- 失败时保持 `in_progress` 并进入 `rework`

### 步骤 8：触发 `G203`

- 通过独立子代理启动 `G203`
- 固定触发 `G203`
- 依赖 `G201` 已形成可解析策略约束
- 子代理结果验收通过并完成状态回写后关闭该子代理
- 输出面向 architecture 包装的蓝图级内容与 ADR 集

### 步骤 9：触发 `G204`

- 通过独立子代理启动 `G204`
- 固定触发 `G204`
- 依赖 `G203` 已形成可解析蓝图与 ADR 结论
- 子代理结果验收通过并完成状态回写后关闭该子代理
- 输出 architecture 阶段内部评审验证结论

### 步骤 10：推进 `GS-Quality-Check`

- 通过独立子代理启动 `GS-Quality-Check`
- 统一要求 architecture 阶段文档包进入 `AD-07`
- 消费 `GS-Quality-Check` 输出字段
- 子代理结果验收通过并完成状态回写后关闭该子代理
- 若存在 `critical/major`，禁止进入 `AD-08`

### 步骤 11：推进 `GS-Review`

- 通过独立子代理启动 `GS-Review`
- 统一要求 architecture 阶段汇总文档包进入 `AD-08`
- 先将 `GS-Quality-Check` 输出归一化为 `quality_gate_ref`
- 消费 `review_summary.pass_rate` 与 `review_summary.decision`
- 子代理结果验收通过并完成状态回写后关闭该子代理
- `decision=fail` 时，必须回写 `skill_stage=rework + status_code=in_progress + status_label=进行中 + review_result=rework + resume_from=首个 owner_task_id`
- `decision=pending` 时，必须回写 `skill_stage=user_review + status_code=blocked + review_result=blocked + resume_from=AD-08`

### 步骤 12：生成交接前置判断

- 当 `AD-08` 通过后，生成 `handoff_summary`
- 同步写入 `handoff_record`，字段必须对齐 `handoff_id/from_stage/to_stage/required_outputs/review_gate/status/notes/updated_at`
- 明确 `architecture_outputs/review_outputs/change_outputs` 是否可消费
- 允许推进 `AD-09`

## 7. 与运行时台账对齐

1. `G200` 自身不单独占用新 task_id，而是驱动 `AD-01 ~ AD-09`。
2. 所有状态回写必须落到 `artifacts/architecture/000-task-tracker.md`。
3. `G200` 是当前 architecture 阶段的入口编排技能。
4. `AD-02` 未触发澄清时，必须回写 `done/completed` 且 `review_result=no-op`。
5. `AD-03 ~ AD-06` 在起草完成后允许保持 `in_progress`，统一由 `AD-07` 收口。
6. `template.md` 的运行时任务推进表必须与 `runtime-task-tracker-spec.md` 的固定表头保持一致。
7. `template.md` 的阶段交接记录必须与 `runtime-task-tracker-spec.md` 第 9 章固定表头保持一致。
8. 如本轮为正式执行，应同步维护 `template.md` 对应的入口编排记录。

## 8. 验收标准

1. 能生成 architecture 阶段最小执行清单与模式判定结果。
2. 能明确 `G202/G201/G203/G204` 的固定路由顺序。
3. 能对齐 `AD-07/AD-08` 阶段汇总门口径。
4. 能基于 `template.md` 形成一次完整入口编排记录，且字段与 `000-task-tracker.md` 可相互映射。
5. architecture 阶段推进到 `AD-09` 前，必须满足：
   - `quality_check_summary.overall_status in [pass, pass_with_warning]`
   - `validation_summary.issue_count.critical = 0`
   - `validation_summary.issue_count.major = 0`
   - `review_summary.decision = pass`
   - `review_summary.pass_rate >= 85`

## 9. 失败与恢复

1. 若治理契约缺失，标记 `blocked`。
2. 若上游 `final_mode` 缺失、非法或冲突未收敛，必须转 `blocked` 并输出最小补齐问题集。
3. 若 `G202/G201/G203/G204` 任一失败，保持 `in_progress` 并进入返工。
4. 恢复时仅以 `000-task-tracker.md` 作为运行时恢复主锚点；`001-architecture-intake.md` 与 `template.md` 只作为辅助证据，不得作为恢复前置依赖。

## 10. References

本 SKILL 的本地 references 目录如下：

1. [role-definition.md](references/role-definition.md)
2. [execution-details.md](references/execution-details.md)
3. [input-completeness-scoring-spec.md](../_shared/governance/input-completeness-scoring-spec.md)
4. [runtime-task-tracker-spec.md](../_shared/governance/runtime-task-tracker-spec.md)
5. [quality-checker-requirements.md](../_shared/governance/quality-checker-requirements.md)
6. [template.md](template.md)
7. `../g202-architecture-vision/SKILL.md`
8. `../g201-technical-strategy/SKILL.md`
9. `../g203-architecture-blueprint/SKILL.md`
11. `../g204-architecture-review/SKILL.md`
12. `../gs-quality-check/SKILL.md`
13. `../gs-review/SKILL.md`

说明：

1. `skills/_shared` 提供 `G200`、`G100`、`G300` 共用的治理与入口编排骨架。
2. `G200` 本地 references 仅保留阶段专属角色定义与执行细化，不再复制整套共享治理。
3. 若后续共享治理或共享编排骨架升级，应优先更新 `skills/_shared` 并回写版本台账。
