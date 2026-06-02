# G200 执行细化说明

## 1. 作用

本文件用于细化 `G200` 在 architecture 阶段的入口编排执行方式，补齐 `SKILL.md` 与共享入口编排流程中的规则到“如何落地执行”的映射，确保：

1. 模式消费有固定决策顺序。
2. 澄清、起草、门禁、交接有明确推进条件。
3. 产出记录可直接落到 `template.md` 与 `000-task-tracker.md`。

## 2. 执行原则

1. `G200` 自身不替代 `G202/G201/G203/G204` 的专业分析工作，只负责入口编排。
2. 所有“是否进入下一步”的判断，必须同时满足：
   - 当前步骤产出已形成
   - 对应 task 状态已回写
   - 下游输入已可消费
3. `G200` 每推进一轮，都应优先更新：
   - `artifacts/architecture/001-architecture-intake.md`
   - `artifacts/architecture/000-task-tracker.md`
   - 基于 [template.md](../template.md) 维护的入口编排记录

## 3. 模式消费与一致性校验

### 3.1 判定输入

必须至少读取以下信息：

1. requirements 阶段交接摘要与交接记录
2. 当前用户请求或阶段请求上下文
3. 上游 `final_mode` 与显式模式偏好（如存在）
4. 历史 `000-task-tracker.md`（如为恢复执行）
5. 输入完整度评分结果

### 3.2 判定输出

模式判定必须输出以下字段：

1. `recommended_mode`
2. `final_mode`
3. `mode_source`
4. `mode_decision_basis`
5. `clarification_required`
6. `missing_fields`
7. `skills_to_run`
8. `skills_skipped`

### 3.3 判定说明要求

`mode_decision_basis` 不能只写结论，至少要说明：

1. requirements 阶段是否已冻结有效 `final_mode`
2. 当前评分区间与 architecture 交接完整度
3. 是否存在用户覆盖
4. 为什么选择当前模式而不是其他模式

### 3.4 模式一致性规则

1. 若 requirements 阶段 `final_mode` 可用且无冲突，则直接消费。
2. 若上游模式缺失、非法或与本阶段交接冲突，则必须转 `blocked` 并请求补齐或用户确认。
3. 若用户显式覆盖模式且不违反共享硬约束，则以用户覆盖为准，并记录 `mode_source=user_override`。
4. 模式消费结果不得据此跳过任何核心 SKILL。
5. 若存在用户覆盖，请按共享评分口径记录 `total_score`、`D1`、`D2`、`D3`，并在 `mode_decision_basis` 中说明未触发的硬阻塞条件。
6. 当前 `G200` 在 `fast/standard/complete` 下的核心执行链保持一致，不存在因模式不同而跳过 `G202/G201/G203/G204` 的情况；只要模式可消费且前置条件满足，即可直接启动执行链。

## 4. 澄清闭环

### 4.1 必须澄清的情况

以下情况不得跳过澄清：

1. requirements 交接产物缺失或不完整
2. architecture 目标不清晰，无法冻结架构问题定义
3. 范围边界不清晰，无法判断架构分解边界
4. 约束或验收标准缺失，无法判定完成条件
5. 用户模式偏好与评分结果冲突

### 4.2 澄清输出要求

每轮澄清至少输出：

1. `clarification_reason`
2. `clarification_questions`
3. `working_assumptions`
4. `risk_if_unanswered`

### 4.3 澄清结束条件

符合以下任一条件可结束澄清：

1. 关键信息已补齐，可以进入 `G202/G201/G203/G204`
2. 已达到最大澄清轮次，且必须以工作假设继续
3. 用户明确接受当前信息不完整带来的风险

## 5. 下游 SKILL 编排细则

### 5.0 子代理启动与关闭总则

1. 每个后续 SKILL 必须由独立子代理执行。
2. 子代理输入至少包含：目标 SKILL、输入路径、输出路径、验收标准、回写任务位。
3. 子代理完成后，主执行方必须先检查输出是否达到当前步骤验收标准。
4. 只有在“结果可验收 + 台账已回写”两个条件都满足后，才允许关闭该子代理。
5. 若结果未通过验收，子代理应继续用于返工或重新拉起新的子代理承接，不得在未形成可恢复状态前直接关闭。

### 5.1 G202

1. `G202` 必执行。
2. 它负责先建立 architecture 愿景与目标边界，再供后续技能消费。
3. `G202` 必须由独立子代理执行，验收通过并完成 `AD-03` 回写后关闭该子代理。

### 5.2 G201

1. `G201` 必执行。
2. 它负责基于 `G202` 产物收敛技术策略与决策依据。
3. `G201` 必须由独立子代理执行，验收通过并完成 `AD-04` 回写后关闭该子代理。

### 5.3 G203

1. `G203` 必执行。
2. 它负责将技术策略落到架构蓝图级结构，并同步沉淀 ADR 集。
3. `G203` 必须由独立子代理执行，验收通过并完成 `AD-05` 回写后关闭该子代理。

### 5.4 G204

1. `G204` 必执行。
2. 它负责对 architecture 包进行内部评审验证，形成可供质量门消费的验证结论。
3. `G204` 必须由独立子代理执行，验收通过并完成 `AD-06` 回写后关闭该子代理。

### 5.5 执行清单字段要求

`skills_to_run` 必须是完整的阶段内执行链，而不是只写分析类 SKILL：

1. `fast`：`G202 -> G201 -> G203 -> G204 -> GS-Quality-Check -> GS-Review`
2. `standard`：`G202 -> G201 -> G203 -> G204 -> GS-Quality-Check -> GS-Review`
3. `complete`：`G202 -> G201 -> G203 -> G204 -> GS-Quality-Check -> GS-Review`

`skills_skipped` 仅在外部阻塞或恢复截断时记录跳过项与原因；正常架构入口不应跳过任何核心 SKILL。

## 6. 门禁推进细则

### 6.1 GS-Quality-Check

进入质量门前至少应具备：

1. intake 文档
2. architecture 视图文档
3. technical strategy 文档
4. architecture blueprint 文档
5. ADR 文档
6. architecture review validation 文档

若任一主文档缺失，不应进入 `AD-07`。
`GS-Quality-Check` 必须由独立子代理执行，验收通过并完成 `AD-07` 回写后关闭该子代理。

### 6.2 GS-Review

进入评审门前至少应满足：

1. `quality_check_summary.overall_status` 为 `pass` 或 `pass_with_warning`
2. `critical = 0`
3. `major = 0`
4. 启动前必须先将 `GS-Quality-Check` 输出归一化为 `quality_gate_ref`，不得并列传入原始 `quality_check_summary` / `validation_summary`
5. 所有返工项均已回写
6. `GS-Review` 必须由独立子代理执行，验收通过并完成 `AD-08` 回写后关闭该子代理。
7. `decision=fail` 时，必须回写 `skill_stage=rework + status_code=in_progress + status_label=进行中 + review_result=rework + resume_from=首个 owner_task_id`。
8. `decision=pending` 时，必须回写 `skill_stage=user_review + status_code=blocked + review_result=blocked + resume_from=AD-08`。

## 7. 交接细则

### 7.1 可交接条件

只有同时满足以下条件，`handoff_ready` 才能标记为 `yes`：

1. `review_summary.decision = pass`
2. `review_summary.pass_rate >= 85`
3. `architecture_outputs` 完整可读取
4. `review_outputs` 完整可读取
5. `change_outputs` 已包含本轮关键修订摘要

### 7.2 交接摘要最小内容

交接摘要至少包括：

1. 当前执行模式
2. 已完成 SKILL 列表
3. 未解决风险
4. 供下游阶段关注的范围边界与验收约束

### 7.3 阶段交接记录要求

除 `handoff_summary` 外，还必须同步生成一条正式交接记录，字段固定为：

1. `handoff_id`
2. `from_stage`
3. `to_stage`
4. `required_outputs`
5. `review_gate`
6. `status`
7. `notes`
8. `updated_at`

该记录必须与 `runtime-task-tracker-spec.md` 第 9 章固定表头一致。

## 8. 恢复与回写

1. 恢复时仅以 `000-task-tracker.md` 作为运行时恢复主锚点；`001-architecture-intake.md` 与 `template.md` 只作为辅助证据。
2. `resume_from` 至少包含：已完成的最后动作、当前待继续动作、未完成的检查或评审、缺失输入或待确认项。
3. 每次恢复都必须同步校正 `mode_source`、`final_mode`、`skills_to_run`、`skills_skipped` 与任务状态。
4. 运行时台账更新后，才能继续执行后续子代理或关闭当前子代理。
