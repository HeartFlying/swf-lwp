# G100 执行细化说明

## 1. 作用

本文件用于细化 `G100` 在 requirements 阶段的入口编排执行方式，补齐 `SKILL.md` 与共享入口编排流程中的规则到“如何落地执行”的映射，确保：

1. 模式判定有固定决策顺序。
2. 澄清、起草、门禁、交接有明确推进条件。
3. 产出记录可直接落到 `template.md` 与 `000-task-tracker.md`。

## 2. 执行原则

1. `G100` 自身不替代 `G101/G102/G103` 的专业分析工作，只负责入口编排。
2. 所有“是否进入下一步”的判断，必须同时满足：
   - 当前步骤产出已形成
   - 对应 task 状态已回写
   - 下游输入已可消费
3. `G100` 每推进一轮，都应优先更新：
   - `artifacts/requirements/001-requirements-intake.md`
   - `artifacts/requirements/000-task-tracker.md`
   - 基于 [template.md](../template.md) 维护的入口编排记录

## 3. 模式判定落地流程

### 3.1 判定输入

必须至少读取以下信息：

1. 当前用户请求
2. 显式模式偏好（如存在）
3. 历史 `000-task-tracker.md`（如为恢复执行）
4. 输入完整度评分结果

### 3.2 判定输出

模式判定必须输出以下字段：

1. `recommended_mode`
2. `final_mode`
3. `mode_decision_basis`
4. `clarification_required`
5. `missing_fields`
6. `skills_to_run`
7. `skills_skipped`

### 3.3 判定说明要求

`mode_decision_basis` 不能只写结论，至少要说明：

1. 用户是否指定模式
2. 当前评分区间
3. 是否存在强制降级或升级条件
4. 为什么选择当前模式而不是其他模式

### 3.4 CONTEXT.md 生命周期管理

**格式来源**：`references/context-format.md`（本地拷贝，不引用外部技能）

**初始化**：

- 时机：RA-01 阶段检查，RA-08 前如不存在则必须产出
- 规则：lazy creation——仅当至少有一个领域特定术语需要记录时才创建文件
- 最小结构：

  ```md
  # {项目名称} 领域术语词典

  {1-2 句说明本词典的用途和范围。}

  ## 术语定义

  **{术语 1}**:
  {一句话定义}
  _Avoid_: {禁止使用的别名，逗号分隔}

  ## 术语关系

  - **{术语 A}** 包含一个或多个 **{术语 B}**

  ## 示例对话

  > **Dev:** ...
  > **Domain expert:** ...

  ## 标记的歧义

  - ...
  ```

**维护**：

- G101 执行期间：从市场/竞品分析中提取领域术语，增量写入
- G102 执行期间：基于 FR/NFR 命名验证术语一致性，标记冲突
- G103 执行期间：基于 scope 边界补充遗漏术语
- 阶段交接时：CONTEXT.md 作为 `requirements_outputs` 的一部分传递给 architecture 阶段

**术语写入原则**：

- 只包含本项目业务领域的特定概念
- 通用编程概念（超时、错误类型、工具类）不写入
- 为每个术语给出规范名称和应避免的别名（Avoid 列表）

## 4. 澄清闭环

### 4.1 必须澄清的情况

以下情况不得跳过澄清：

1. 目标不清晰，无法冻结问题定义
2. 范围边界不清晰，无法判断 MVP
3. 验收标准缺失，无法判定完成条件
4. 用户模式偏好与评分结果冲突

requirements 阶段下游方法边界统一参考：

1. [requirements-methods-catalog.md](../../_shared/requirements-methods-catalog.md)
2. `G100` 不直接规定 `G101/G102/G103` 的逐步分析方法，但在编排、澄清和恢复说明中应默认以下游 SKILL 对该目录的引用为准。

### 4.2 澄清输出要求

每轮澄清至少输出：

1. `clarification_reason`
2. `clarification_questions`
3. `working_assumptions`
4. `risk_if_unanswered`

### 4.3 澄清结束条件

符合以下任一条件可结束澄清：

1. 关键信息已补齐，可以进入 `G101/G102/G103`
2. 已达到最大澄清轮次，且必须以工作假设继续
3. 用户明确接受当前信息不完整带来的风险

## 5. 下游 SKILL 编排细则

### 5.0 子代理启动与关闭总则

1. 每个后续 SKILL 必须由独立子代理执行。
2. 子代理输入至少包含：目标 SKILL、输入路径、输出路径、evidence 路径、验收标准、回写任务位。evidence 路径格式固定为 `evidence/{task_id}/`，子代理必须将分析/评审过程中的关键证据写入该目录。
3. 子代理完成后，主执行方必须先检查三项输出：(a) 主文档是否达到验收标准；(b) evidence 目录是否非空且包含至少 1 份过程证据文件；(c) 台账是否已回写。
4. 只有在”主文档可验收 + evidence 已产出 + 台账已回写”三个条件都满足后，才允许关闭该子代理。
5. 若结果未通过验收，子代理应继续用于返工或重新拉起新的子代理承接，不得在未形成可恢复状态前直接关闭。

### 5.1 G101

1. `fast` 模式默认不执行。
2. `standard/complete` 模式原则上执行。
3. 若业务背景已在用户输入中非常完整，可在 `standard` 模式下标记为“已覆盖”并记录跳过原因，但必须保证 `G102` 输入不缺背景基线。
4. `G101` 必须由独立子代理执行，验收通过并完成 `RA-03` 回写后关闭该子代理。

### 5.2 G102

1. 必执行。
2. 进入 `G102` 前，应确认目标、范围、约束、验收标准已有最小冻结版本。
3. 若无法形成最小冻结版本，不得将 `RA-04` 标记为完成。
4. `G102` 必须由独立子代理执行，验收通过并完成 `RA-04` 回写后关闭该子代理。

### 5.3 G103

1. 必执行。
2. 输入必须来自 `G102` 的可解析需求基线，而不是直接绕过基线文档。
3. 输出必须能支撑下游阶段进行边界与优先级判断。
4. `G103` 必须由独立子代理执行，验收通过并完成 `RA-05` 回写后关闭该子代理。

### 5.4 执行清单字段要求

`skills_to_run` 必须是完整的阶段内执行链，而不是只写分析类 SKILL：

1. `fast`：`G102 -> G103 -> GS-Quality-Check -> PRD-Design-Readiness-Review -> GS-Review`
2. `standard`：`G101 -> G102 -> G103 -> GS-Quality-Check -> PRD-Design-Readiness-Review -> Software-FMEA-Review(轻量) -> GS-Review`
3. `complete`：`G101 -> G102 -> G103 -> GS-Quality-Check -> PRD-Design-Readiness-Review -> Software-FMEA-Review(完整) -> GS-Review`

`skills_skipped` 必须记录被跳过的 skill 与原因，例如：

1. `G101(skipped_in_fast)`
2. `G101(already_covered_by_input)`

## 6. 门禁推进细则

### 6.1 GS-Quality-Check

进入质量门前至少应具备：

1. intake 文档
2. requirements 基线文档
3. MVP 定义文档
4. 必要时的业务背景文档

若任一主文档缺失，不应进入 `RA-06`。
5. `GS-Quality-Check` 必须由独立子代理执行，验收通过并完成 `RA-06` 回写后关闭该子代理。

### 6.2 GS-Review

进入评审门前至少应满足：

1. `quality_check_summary.overall_status` 为 `pass` 或 `pass_with_warning`
2. `critical = 0`
3. `major = 0`
4. `prd-design-readiness-review.gate_result` 为 `PASS` 或 `CONDITIONAL_PASS`
5. `software-fmea-review` 中 AP=H 的风险项均已具备预防措施和探测措施（`fast` 模式免检）
6. 启动前必须先将 `GS-Quality-Check` 输出归一化为 `quality_gate_ref`，不得并列传入原始 `quality_check_summary` / `validation_summary`
7. 启动前必须将 `prd-design-readiness-review` 评审报告路径和 `software-fmea-review` 评审报告路径纳入 `stage_documents`
8. 所有返工项均已回写
9. `GS-Review` 必须由独立子代理执行，验收通过并完成 `RA-07c` 回写后关闭该子代理。
10. `decision=fail` 时，必须回写 `skill_stage=rework + status_code=in_progress + status_label=进行中 + review_result=rework + resume_from=首个 owner_task_id`。
11. `decision=pending` 时，必须回写 `skill_stage=user_review + status_code=blocked + review_result=blocked + resume_from=RA-07c`。

**调用参数映射**：

启动 GS-Review 子代理时，必须传入以下参数：

| 参数 | 值 | 说明 |
|---|---|---|
| `stage` | `requirements` | 当前阶段标识 |
| `review_task_id` | `RA-07c` | G100 编排层使用的任务位编号 |
| `tracker_path` | `artifacts/requirements/000-task-tracker.md` | 运行时台账路径 |
| `review_report_path` | `artifacts/reviews/001-requirements-review.md` | 评审报告输出路径 |
| `stage_documents` | 含 `001a-prd-design-readiness-review.md`、`001b-fmea-risk-review.md` | 必须包含 PRD 设计准入评审报告和 FMEA 风险评审报告 |
| `quality_gate_ref` | 来自 RA-06 归一化输出 | 质量门归一化结果 |

**说明**：GS-Review 共享服务的任务映射表使用 `RA-07`，但 G100 编排层内部已拆分为 `RA-07a`（PRD 准入评审）、`RA-07b`（FMEA 风险评审）和 `RA-07c`（汇总评审）。调用时 `review_task_id` 应传 `RA-07c`，由 G100 编排层负责在台账回写时映射到正确的任务位。

### 6.3 PRD-Design-Readiness-Review

进入 PRD 设计准入评审门前至少应具备：

1. requirements 基线文档（G102 产出）
2. MVP 定义文档（G103 产出）
3. intake 文档
4. 质量门已通过（RA-06 为 pass 或 pass_with_warning）

若任一主文档缺失，不应进入 `RA-07a`。

1. `PRD-Design-Readiness-Review` 必须由独立子代理执行，验收通过并完成 `RA-07a` 回写后关闭该子代理。
2. 验收标准：
   - `gate_result != FAIL`
   - `checklist_used = true`
   - `missing_checklist_items` 为空（完整评审时）
3. `gate_result = FAIL` 时，必须回写 `skill_stage=rework + status_code=in_progress + status_label=进行中 + review_result=rework + resume_from=RA-07a`。
4. `gate_result = CONDITIONAL_PASS` 时，`required_prd_actions` 必须完整归档，并作为 `RA-07b` 的 `stage_documents` 组成部分传入。
5. `design_stage_notes` 中记录的内容（系统设计阶段展开事项）不得作为 PRD 缺陷返回给 G102/G103 返工。

### 6.4 Software-FMEA-Review

进入 FMEA 风险评审门前至少应具备：

1. requirements 基线文档（G102 产出）
2. MVP 定义文档（G103 产出）
3. intake 文档
4. 质量门已通过（RA-06 为 pass 或 pass_with_warning）
5. PRD 设计准入评审已通过（RA-07a 为 PASS 或 CONDITIONAL_PASS）
6. PRD 准入评审报告可读取

若任一主文档或前置评审缺失，不应进入 `RA-07b`。

1. `fast` 模式跳过本任务，`RA-07b` 回写 `status_code=skipped` + `review_result=skipped`。

2. `standard` 模式（轻量 FMEA）：
   - 传入执行深度参数 `lightweight`
   - 使用 12 种失效模式库（`software-fmea-reference.md`）对 top 3-5 高风险功能做 checklist 扫描
   - 对核心主链路功能执行 S/O/D 评分和 AP 判定
   - 产出至少包含：风险表（FE/FM/FC + S/O/D/AP）、整改清单、NFR 专项摘要
   - 子代理验收通过并完成 `RA-07b` 回写后关闭

3. `complete` 模式（完整 FMEA）：
   - 传入执行深度参数 `full`
   - 执行全 9 步工作流：策划与边界 → 结构分析 → 功能分析 → 失效分析 → 风险分析 → 优化措施 → 闭环验证 → 结果保存 → 知识库沉淀
   - 覆盖全部 in-scope MVP 功能 + NFR 专项检查（性能/容量、安全/权限、数据一致性、可观测性、可恢复性/回滚、合规/审计）
   - 对每个关键分析单元推导 FE/FM/FC 因果链
   - 子代理验收通过并完成 `RA-07b` 回写后关闭

4. 验收标准：
    - FMEA 报告路径为 `artifacts/reviews/001b-fmea-risk-review.md`
    - AP=H 的风险项必须在整改清单中有对应的预防措施和探测措施
    - 预防措施和探测措施必须可区分（预防消除原因，探测发现问题）
    - 每项中高风险整改必须具备 Owner 角色、验证方式和验收证据

5. `AP=H` 风险项缺少预防/探测措施时，必须回写 `skill_stage=rework + status_code=in_progress + status_label=进行中 + review_result=rework + resume_from=RA-07b`。

6. FMEA 报告的 AP=H 项和 NFR 专项结论必须作为 `RA-07c` 的 `stage_documents` 组成部分传入。

7. FMEA 中识别的高风险项应同步更新到 `template.md` 的"风险与恢复"章节。

## 7. 交接细则

### 7.1 可交接条件

只有同时满足以下条件，`handoff_ready` 才能标记为 `yes`：

1. `prd_readiness_summary.gate_result in [PASS, CONDITIONAL_PASS]`
2. `software_fmea_review` 中 AP=H 风险项均已具备预防/探测措施（`fast` 模式免检）
3. `review_summary.decision = pass`
4. `review_summary.pass_rate >= 85`
5. `requirements_outputs` 完整可读取
6. `change_outputs` 已包含本轮关键修订摘要
7. `context_status` 不为 `pending`（如存在待产出术语，必须先完成 `artifacts/requirements/CONTEXT.md`）
8. `RA-03 ~ RA-07c` 的 evidence 目录（`evidence/RA-{03~07c}/`）均非空且包含至少 1 份过程证据文件

### 7.2 交接摘要最小内容

交接摘要至少包括：

1. 当前执行模式
2. 已完成 SKILL 列表
3. 未解决风险
4. 供下游阶段关注的范围边界与验收约束
5. `context_path` 与 `context_status`（如已产出 CONTEXT.md，纳入 `requirements_outputs`）

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

## 5.5 evidence 内容最低要求

每个子代理在产出主文档的同时，必须向 `evidence/{task_id}/` 目录写入至少 1 份过程证据文件。证据文件类型按 SKILL 区分：

| task_id | 对应 SKILL | evidence 最低要求 |
|---|---|---|
| RA-03 | G101 | 市场数据来源与假设、竞品信息来源、痛点优先级评分过程（ICE/RICE）、机会点评分过程 |
| RA-04 | G102 | 需求编号校验记录、追溯矩阵生成过程、MoSCoW分层决策依据、约束强度判定依据 |
| RA-05 | G103 | MVP范围决策过程、in-scope/out-of-scope判定依据、迭代优先级映射依据、风险识别过程 |
| RA-06 | GS-Quality-Check | 检查器执行详细记录（QC-001~QC-007逐项结果）、评分过程和阈值依据、问题识别过程 |
| RA-07a | PRD-Design-Readiness-Review | checklist逐项评分依据、Blocker/Major/Minor判定过程、设计前必须闭合项识别过程 |
| RA-07b | Software-FMEA-Review | 12种失效模式checklist扫描记录、S/O/D评分明细和依据、AP判定过程 |
| RA-07c | GS-Review | 汇总评审维度检查记录、质量门问题处置过程、pass_rate计算过程 |

evidence 文件命名建议：`{task_id}-{evidence-type}.md`，如 `RA-03-scoring-details.md`。

evidence 质量约束：

1. 必须可追溯（说明数据来源、判定依据、假设条件）。
2. 必须可复核（另一评审者可基于证据文件复现结论）。
3. 不得与主文档重复（主文档放结论，evidence 放过程和依据）。

## 8. 建议执行记录方式

建议每次执行 `G100` 时：

1. 将关键结论同步回写到 `001-requirements-intake.md`。
2. 将状态字段同步回写到 `000-task-tracker.md`。
3. `template.md` 的运行时任务推进表和阶段交接记录表应直接镜像共享治理规定的固定表头。
4. 模板中应记录每个后续 SKILL 对应的子代理执行与关闭情况。
5. 运行时恢复仅以 `artifacts/requirements/000-task-tracker.md` 作为主锚点；`001-requirements-intake.md` 与 `template.md` 只作为辅助证据。
6. `RA-07a` 的评审结果应同步记录到 `template.md` 的"PRD 设计准入评审结果"章节。
7. `RA-07b` 的 FMEA 评审结果应同步记录到 `template.md` 的"FMEA 风险评审结果"章节，AP=H 风险项应同步更新到"风险与恢复"章节。
8. 若 `RA-07a` 为 `CONDITIONAL_PASS`，应在交接摘要的 `notes` 中明确列出 `required_prd_actions`，供 architecture 阶段跟踪。
9. 若 `RA-07b` 产出 AP=H 风险项，应在交接摘要的 `notes` 中明确列出 top 3 高风险及缓解状态，供 architecture 阶段跟踪。
10. 每个子代理关闭前，应确认 `evidence/{task_id}/` 目录非空；如为空，不得关闭子代理，应要求子代理补充过程证据文件。

这样可以保证入口编排、文档产出、运行时状态三者一致。
