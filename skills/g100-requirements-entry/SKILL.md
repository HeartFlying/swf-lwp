---
name: g100-requirements-entry
description: requirements 阶段入口编排 SKILL，负责模式判定、澄清分流、G101/G102/G103 编排、阶段门禁推进与阶段交接前置判断，并复用 skills/_shared 下的共享治理与入口编排流程。
version: 1.7.0
disable-model-invocation: false
argument-hint: [user-request]
---

# G100 Requirements Entry SKILL

## 元信息与执行契约

说明：`G100` 是 requirements 阶段当前入口编排 SKILL。其角色定义、阶段专属细则与共享治理契约共同定义 requirements 阶段的入口执行方式。

### 基本信息

| 项目 | 内容 |
|---|---|
| skill_id | `G100` |
| skill_type | `core` |
| 中文名称 | requirements 阶段入口编排 |
| 适用阶段 | `requirements` |
| 执行模式 | `fast`、`standard`、`complete` |
| 前置依赖 | 无 |
| 后置依赖 | `G101`（条件）、`G102`、`G103`、`GS-Quality-Check`、`prd-design-readiness-review`、`software-fmea-review`、`GS-Review` |
| 输出主文档 | `artifacts/requirements/001-requirements-intake.md` |

### 执行契约摘要

| 项目 | 内容 |
|---|---|
| 运行时任务映射 | `RA-01` 到 `RA-08` 的入口编排 |
| 运行时台账路径 | `artifacts/requirements/000-task-tracker.md` |
| 必选输入 | `user_request` |
| 按需输入 | `mode_preference`、已有 `000-task-tracker.md`、本地治理 references |
| 关键引用 | `references/role-definition.md`、`references/execution-details.md`、`template.md`、`../_shared/governance/*.md`、`../_shared/requirements-methods-catalog.md`、`../g101-business-context/SKILL.md`、`../g102-requirements-baseline/SKILL.md`、`../g103-mvp-definition/SKILL.md`、`../gs-quality-check/SKILL.md`、`../prd-design-readiness-review/SKILL.md`、`../software-fmea-review/SKILL.md`、`../gs-review/SKILL.md` |
| 入口属性 | 当前阶段正式入口编排 SKILL，负责 requirements 阶段的模式判定、路由生成与门禁推进 |

## 1. 目标

承载 requirements 阶段全部入口编排能力，覆盖：

1. 输入接收与 intake 建立
2. 模式判定与澄清分流
3. `G101/G102/G103` 触发顺序
4. `GS-Quality-Check` 与 `GS-Review` 的阶段门推进
5. `RA-08` 的阶段交接前置判断

## 2. 角色定义

`G100` 的角色定义、边界、决策优先级和输出风格见：

- [role-definition.md](references/role-definition.md)

执行时应将其视为本 SKILL 的角色说明基线。

## 2.1 执行模板与细化说明

`G100` 的实际执行记录与步骤细化统一使用以下本地文件：

- [template.md](template.md)
- [execution-details.md](references/execution-details.md)

执行要求：

1. `template.md` 用于记录本轮入口编排的模式判定、执行清单、门禁结果与交接摘要。
2. `execution-details.md` 用于补足各步骤的推进条件、结束条件与回写要求。
3. `SKILL.md`、`template.md`、`execution-details.md` 与共享骨架必须保持一致，不得出现规则与模板字段脱节。

## 3. 前置条件

1. `artifacts/requirements/000-task-tracker.md` 结构必须符合 [runtime-task-tracker-spec.md](../_shared/governance/runtime-task-tracker-spec.md)。
2. `G101/G102/G103/GS-*` 已具备可调用定义。

## 4. 输入输出契约

### 4.1 输入

1. `user_request`（必选）
2. `mode_preference`（按需）
3. `artifacts/requirements/000-task-tracker.md`（按需，恢复执行时必读）
4. 本地治理 references：
   - [input-completeness-scoring-spec.md](../_shared/governance/input-completeness-scoring-spec.md)
   - [runtime-task-tracker-spec.md](../_shared/governance/runtime-task-tracker-spec.md)
   - [quality-checker-requirements.md](../_shared/governance/quality-checker-requirements.md)
5. requirements 方法目录：
   - [requirements-methods-catalog.md](../_shared/requirements-methods-catalog.md)
6. 本地执行辅助：
   - [template.md](template.md)
   - [execution-details.md](references/execution-details.md)
7. 共享服务契约：
   - `../gs-quality-check/SKILL.md`
   - `../prd-design-readiness-review/SKILL.md`
   - `../gs-review/SKILL.md`

### 4.2 输出

1. `artifacts/requirements/001-requirements-intake.md`
2. `artifacts/requirements/000-task-tracker.md`
3. `recommended_mode`
4. `final_mode`
5. `mode_decision_basis`
6. `clarification_required`
7. `missing_fields`
8. `clarification_questions`
9. `working_assumptions`
10. `risk_if_unanswered`
11. `skills_to_run`
12. `skills_skipped`
13. `review_summary`（通过共享服务回写）
14. `handoff_summary`（供下游阶段消费）
15. `handoff_record`（写入阶段交接固定表头）
16. `context_path`：`artifacts/requirements/CONTEXT.md`（按需产出，首轮 intake 阶段检查，RA-08 前如不存在则产出）

### 4.3 供阶段恢复与下游消费的最小字段

1. `recommended_mode`
2. `final_mode`
3. `mode_decision_basis`
4. `clarification_required`
5. `resume_from`
6. `review_summary.decision`
7. `review_summary.pass_rate`
8. `handoff_summary`

### 4.4 输出约束

1. 路径统一使用项目根相对路径与 `/` 分隔符。
2. 所有状态变更必须同步回写 `000-task-tracker.md`。
3. `G100` 不直接替代 `G101/G102/G103` 的主文档产出，只负责编排与推进。

## 5. 决策与编排规则

### 5.1 模式判定顺序

1. 用户显式指定 `complete` 时，优先 `complete`。
2. 用户显式指定 `fast` 且 `total_score >= 90` 且 `D1 >= 50` 时，进入 `fast`。
3. `D2 < 25` 或 `D3 < 25` 时，强制进入 `complete`。
4. `total_score < 60` 时，进入 `complete`。
5. `60 <= total_score < 90` 时，进入 `standard`。
6. `total_score >= 90` 且用户未要求快速时，默认进入 `standard`。

### 5.2 澄清触发规则

满足以下任一条件必须发起澄清：

1. `total_score < 60`
2. `60 <= total_score < 90` 且 `D1` 或 `D2` 存在关键字段缺失
3. 目标、范围边界、验收标准任一无法冻结
4. 用户指定模式与评分结果冲突

### 5.3 模式下的内部编排

1. `fast`：`G102 -> G103 -> GS-Quality-Check -> PRD-Design-Readiness-Review -> GS-Review`（跳过 FMEA）
2. `standard`：`G101 -> G102 -> G103 -> GS-Quality-Check -> PRD-Design-Readiness-Review -> Software-FMEA-Review(轻量) -> GS-Review`
3. `complete`：`G101 -> G102 -> G103 -> GS-Quality-Check -> PRD-Design-Readiness-Review -> Software-FMEA-Review(完整) -> GS-Review`

### 5.4 共享服务与专业评审门禁规则

1. `RA-06(GS-Quality-Check)` 必须先于 `RA-07a(PRD-Design-Readiness-Review)`。
2. `quality_check_summary.overall_status` 非 `pass/pass_with_warning` 时，禁止推进 `RA-07a`。
3. 启动 `RA-07a` 前，必须先将 `GS-Quality-Check` 原始输出归一化为 `quality_gate_ref`。
4. `RA-07a(PRD-Design-Readiness-Review)` 必须先于 `RA-07b(Software-FMEA-Review)`。
5. `prd-design-readiness-review.gate_result` 为 `FAIL` 时，禁止推进 `RA-07b`；必须回写 `skill_stage=rework + status_code=in_progress + resume_from=RA-07a`。
6. `prd-design-readiness-review.gate_result` 为 `CONDITIONAL_PASS` 时，允许推进 `RA-07b`，但 `required_prd_actions` 必须完整传入后续 stage_documents。
7. 启动 `RA-07b` 前，必须将 `prd-design-readiness-review` 评审报告路径纳入 `stage_documents`。
8. `RA-07b(Software-FMEA-Review)` 必须先于 `RA-07c(GS-Review)`。
9. `fast` 模式跳过 `RA-07b`；`standard` 模式执行轻量 FMEA（12 种失效模式 checklist 扫描 + top 3-5 高风险功能 S/O/D 评分）；`complete` 模式执行完整 FMEA（全 9 步工作流，覆盖全部 in-scope 功能 + NFR 专项）。
10. `software-fmea-review` 中 AP=H 的风险项必须在整改清单中有对应的预防措施和探测措施，否则禁止推进 `RA-07c`。
11. 启动 `RA-07c` 前，必须将 `software-fmea-review` 评审报告路径纳入 `stage_documents`。
12. 启动 `RA-07c` 前，必须先将 `GS-Quality-Check` 原始输出归一化为 `quality_gate_ref`，不得把 `quality_check_summary`、`validation_summary` 作为并列输入直接传给 `GS-Review`。
13. `RA-07c` 通过前，禁止推进 `RA-08`。
14. 门禁结果必须同时回写到 `template.md` 中的”质量门与评审门”章节。

### 5.5 子代理执行规则

1. `G101/G102/G103/GS-Quality-Check/PRD-Design-Readiness-Review/Software-FMEA-Review/GS-Review` 的实际执行必须通过独立子代理启动。
2. 每个子代理一次只承载一个后续 SKILL，不得在同一子代理中并发执行多个核心 SKILL。
3. 子代理启动时必须显式绑定：目标 SKILL、输入路径、输出路径、evidence 路径、验收要求、回写任务位。evidence 路径必须指向 `evidence/{task_id}/` 目录。
4. 子代理产出完成后，必须先完成三项验收再关闭该子代理：(a) 主文档产出达到验收标准；(b) evidence 目录至少包含 1 份过程证据文件（评分明细、决策依据或分析过程记录）；(c) 台账状态已回写。
5. 未完成验收前不得关闭子代理；已确认通过验收后不得保持子代理长期驻留。
6. `Software-FMEA-Review` 子代理启动时，必须根据当前 `final_mode` 传入执行深度参数（`lightweight` / `full`），`fast` 模式不启动此子代理。

## 6. 执行步骤

### 步骤 1：初始化阶段上下文

- 建立或读取 `artifacts/requirements/000-task-tracker.md`
- 初始化 `RA-01`
- 产出 `001-requirements-intake.md`
- 校验治理契约与 manifest 可用性
- **CONTEXT.md 检查**：
  1. 检查 `artifacts/requirements/CONTEXT.md` 是否已存在
  2. 若已存在：
     - 加载全部术语定义，作为 G101/G102/G103 共享输入的组成部分
     - 在 `001-requirements-intake.md` 中标注"领域术语词典已加载"
  3. 若不存在：
     - 将 `context_status` 设为 `pending`
     - 在 `001-requirements-intake.md` 中标注"领域术语词典待产出"
     - 标记：需在 requirements 阶段完成前产出初版术语词典

### 步骤 2：执行信息完整度评分

- 读取评分规范
- 输出 `dimension_scores`、`total_score`、`recommended_mode`
- 若存在恢复上下文，保留已有 `resume_from`

### 步骤 3：判定是否澄清

- 若满足澄清条件，推进 `RA-02`
- 若无需澄清，按 `no-op` 收口 `RA-02`
- 每轮澄清后必须重新评分
- 连续澄清与采访，直到所有问题全部澄清完毕
- 澄清记录必须至少包含 `clarification_questions`、`working_assumptions`、`risk_if_unanswered`

### 步骤 4：生成执行清单

- `fast`：`G102 -> G103 -> GS-Quality-Check -> PRD-Design-Readiness-Review -> GS-Review`（跳过 FMEA）
- `standard`：`G101 -> G102 -> G103 -> GS-Quality-Check -> PRD-Design-Readiness-Review -> Software-FMEA-Review(轻量) -> GS-Review`
- `complete`：`G101 -> G102 -> G103 -> GS-Quality-Check -> PRD-Design-Readiness-Review -> Software-FMEA-Review(完整) -> GS-Review`
- 产出 `skills_to_run`
- 标记 `skills_skipped`

### 步骤 5：登记任务状态与证据路径

- 回写 `task_id/skill_id/skill_stage/step_name/description/inputs/outputs/dependencies/status_code/status_label/review_result/resume_from/evidence_path/updated_at`
- 初始化 requirements 阶段任务位 `RA-01 ~ RA-08`

### 步骤 6：触发 `G101`（如适用）

- 通过独立子代理启动 `G101`
- `fast` 模式默认跳过
- `standard/complete` 模式触发 `G101`
- 子代理结果验收通过（含 evidence 产出检查：证据目录非空且包含至少 1 份过程证据文件）并完成状态回写后关闭该子代理
- 失败时保持 `in_progress` 并进入 `rework`

### 步骤 7：触发 `G102`

- 通过独立子代理启动 `G102`
- 固定触发 `G102`
- 消费 `G101` 产物（如执行）
- 子代理结果验收通过（含 evidence 产出检查）并完成状态回写后关闭该子代理
- 若缺失关键基线字段，转 `blocked` 或进入返工

### 步骤 8：触发 `G103`

- 通过独立子代理启动 `G103`
- 固定触发 `G103`
- 依赖 `G102` 已形成可解析基线
- 子代理结果验收通过（含 evidence 产出检查）并完成状态回写后关闭该子代理
- 输出面向架构阶段的 MVP 范围边界

### 步骤 9：推进 `GS-Quality-Check`

- 通过独立子代理启动 `GS-Quality-Check`
- 统一要求 requirements 阶段文档包进入 `RA-06`
- 消费 `GS-Quality-Check` 输出字段
- 子代理结果验收通过（含 evidence 产出检查）并完成状态回写后关闭该子代理
- 若存在 `critical/major`，禁止进入 `RA-07a`

### 步骤 10：推进 `PRD-Design-Readiness-Review`

- 通过独立子代理启动 `prd-design-readiness-review`
- 统一要求 requirements 阶段正式文档包（intake、基线、MVP 定义）进入 `RA-07a`
- 消费 `prd-design-readiness-review` 输出字段：`gate_result`、`final_score`、`blocker_avg_score`、`required_prd_actions`
- 子代理结果验收通过（含 evidence 产出检查）并完成状态回写后关闭该子代理
- `gate_result=FAIL` 时，必须回写 `skill_stage=rework + status_code=in_progress + status_label=进行中 + review_result=rework + resume_from=RA-07a`
- `gate_result=CONDITIONAL_PASS` 时，必须将 `required_prd_actions` 和 `design_stage_notes` 归档到 `stage_documents`

### 步骤 11：推进 `Software-FMEA-Review`

- 通过独立子代理启动 `software-fmea-review`
- `fast` 模式跳过本步骤，保留 G103 内建风险分析
- `standard` 模式：传入执行深度 `lightweight`，对 top 3-5 高风险功能做 12 种失效模式 checklist 扫描 + S/O/D 评分
- `complete` 模式：传入执行深度 `full`，覆盖全部 in-scope MVP 功能 + NFR 专项检查
- 统一要求 requirements 阶段正式文档包（intake、基线、MVP 定义、PRD 准入评审报告）进入 `RA-07b`
- 消费 `software-fmea-review` 输出字段：`AP=H` 风险项、整改清单（预防措施 + 探测措施 + Owner + 验证方式）、NFR 专项结论、风险热力图
- 子代理结果验收通过（含 evidence 产出检查）并完成状态回写后关闭该子代理
- `AP=H` 风险项缺少预防措施或探测措施时，必须回写 `skill_stage=rework + status_code=in_progress + status_label=进行中 + review_result=rework + resume_from=RA-07b`
- FMEA 报告路径固定为 `artifacts/reviews/001b-fmea-risk-review.md`

### 步骤 12：推进 `GS-Review`

- 通过独立子代理启动 `GS-Review`
- 统一要求 requirements 阶段汇总文档包进入 `RA-07c`
- 先将 `GS-Quality-Check` 输出归一化为 `quality_gate_ref`
- 将 `prd-design-readiness-review` 评审报告路径和 `software-fmea-review` 评审报告路径纳入 `stage_documents`
- 消费 `review_summary.pass_rate` 与 `review_summary.decision`
- 子代理结果验收通过（含 evidence 产出检查）并完成状态回写后关闭该子代理
- `decision=fail` 时，必须回写 `skill_stage=rework + status_code=in_progress + status_label=进行中 + review_result=rework + resume_from=首个 owner_task_id`
- `decision=pending` 时，必须回写 `skill_stage=user_review + status_code=blocked + review_result=blocked + resume_from=RA-07c`

### 步骤 13：生成交接前置判断

- 当 `RA-07a`、`RA-07b`（如执行）和 `RA-07c` 均通过后，生成 `handoff_summary`
- 同步写入 `handoff_record`，字段必须对齐 `handoff_id/from_stage/to_stage/required_outputs/review_gate/status/notes/updated_at`
- 明确 `requirements_outputs/review_outputs/change_outputs` 是否可消费
- FMEA 的 AP=H 项和 NFR 专项结论必须写入交接摘要的 `notes` 字段
- **CONTEXT.md 产出检查**：
  - 若 `artifacts/requirements/CONTEXT.md` 仍不存在：
    - 汇总 G101/G102/G103 执行过程中识别的领域特定术语
    - 按 `references/context-format.md` 格式生成 `artifacts/requirements/CONTEXT.md`
    - 将 `context_path` 写入 `handoff_summary` 的 `requirements_outputs`
  - 若已存在：
    - 确保 G101/G102/G103 新增的术语已增量写入
- 允许推进 `RA-08`

## 7. 与运行时台账对齐

1. `G100` 自身不单独占用新 task_id，而是驱动 `RA-01 ~ RA-08`。
2. 所有状态回写必须落到 `artifacts/requirements/000-task-tracker.md`。
3. `G100` 是当前 requirements 阶段的入口编排技能。
4. `RA-02` 未触发澄清时，必须回写 `done/completed` 且 `review_result=no-op`。
5. `RA-04/RA-05` 在起草完成后允许保持 `in_progress`，统一由 `RA-07c` 收口。
6. `template.md` 的运行时任务推进表必须与 `runtime-task-tracker-spec.md` 的固定表头保持一致。
7. `template.md` 的阶段交接记录必须与 `runtime-task-tracker-spec.md` 第 9 章固定表头保持一致。
8. 如本轮为正式执行，应同步维护 `template.md` 对应的入口编排记录。

## 8. 验收标准

1. 能生成 requirements 阶段最小执行清单与模式判定结果。
2. 能明确 `G101` 条件执行、`G102/G103` 必执行。
3. 能对齐 `RA-06/RA-07a/RA-07b/RA-07c` 阶段汇总门口径。
4. 能输出可供阶段恢复与下游阶段消费的 `review_summary` 与 `handoff_summary`。
5. 不与现有 `G101/G102/G103`、`GS-*`、manifest 契约冲突。
6. 能基于 `template.md` 形成一次完整入口编排记录，且字段与 `000-task-tracker.md` 可相互映射。
7. requirements 阶段推进到 `RA-08` 前，必须满足：
   - `quality_check_summary.overall_status in [pass, pass_with_warning]`
   - `validation_summary.issue_count.critical = 0`
   - `validation_summary.issue_count.major = 0`
   - `prd_design_readiness_review.gate_result in [PASS, CONDITIONAL_PASS]`
   - `software_fmea_review` 中 AP=H 的风险项均已具备预防措施和探测措施（`fast` 模式免检）
   - `review_summary.decision = pass`
   - `review_summary.pass_rate >= 85`
8. `RA-03 ~ RA-07c` 的 evidence 目录（`evidence/RA-{03~07c}/`）均非空且包含至少 1 份过程证据文件。evidence 最低要求见 `execution-details.md` 第 5.5 节。
9. `artifacts/requirements/CONTEXT.md` 已产出或已确认无需产出（`context_status != pending`）。若步骤1标记为 `pending`，步骤13必须在 RA-08 前完成初版术语词典生成并写入 `handoff_summary.requirements_outputs`。

## 9. 失败与恢复

1. 若治理契约缺失，标记 `blocked`。
2. 若模式无法判定，必须输出最小澄清问题集。
3. 若 `G101/G102/G103` 任一失败，保持 `in_progress` 并进入返工。
4. 恢复时仅以 `artifacts/requirements/000-task-tracker.md` 作为运行时恢复主锚点；`001-requirements-intake.md` 与 `template.md` 只作为辅助证据，不得作为恢复前置依赖。
5. 若 `prd-design-readiness-review` 返回 `FAIL`，恢复时从 `RA-07a` 重新开始，需重新消费 G102/G103 的最新产出。
6. 若 `software-fmea-review` 存在 AP=H 风险项无预防/探测措施，恢复时从 `RA-07b` 重新开始，需重新消费 PRD 准入评审和 G102/G103 的最新产出。
7. `fast` 模式下跳过 `RA-07b`，不适用第 6 条恢复规则。
8. 若任一子代理的 evidence 目录为空，恢复时应要求该子代理补充过程证据文件后方可继续推进。

## 10. References

本 SKILL 的本地 references 目录如下：

1. [role-definition.md](references/role-definition.md)
2. [input-completeness-scoring-spec.md](../_shared/governance/input-completeness-scoring-spec.md)
3. [runtime-task-tracker-spec.md](../_shared/governance/runtime-task-tracker-spec.md)
4. [quality-checker-requirements.md](../_shared/governance/quality-checker-requirements.md)
5. [template.md](template.md)
6. [execution-details.md](references/execution-details.md)
7. [requirements-methods-catalog.md](../_shared/requirements-methods-catalog.md)

说明：
1. `skills/_shared` 提供 `G100`、未来 `G200/G300` 共用的治理与入口编排骨架。
2. `G100` 本地 references 仅保留阶段专属角色定义与执行细化，不再复制整套共享治理。
3. 若后续共享治理或共享编排骨架升级，应优先更新 `skills/_shared` 并回写版本台账。
