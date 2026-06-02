# G300 执行细化说明

## 1. 作用

本文件用于细化 `G300` 在 `detailed_design` 阶段的入口编排执行方式，补齐 `SKILL.md` 与共享入口编排流程中的规则到“如何落地执行”的映射，确保：

1. 模式消费有固定决策顺序。
2. 澄清、起草、门禁、交接有明确推进条件。
3. 产出记录可直接落到 `template.md` 与 `000-task-tracker.md`。

## 2. 执行原则

1. `G300` 自身不替代 `G301/G302/G303` 的专业设计工作，只负责入口编排。
2. `detailed_design` 只消费 `standard` 与 `complete`；`fast` 不是本阶段执行模式。
3. 所有“是否进入下一步”的判断，必须同时满足：
   - 当前步骤产出已形成
   - 对应 task 状态已回写
   - 下游输入已可消费
4. `G300` 每推进一轮，都应优先更新：
   - `artifacts/detailed-design/001-design-plan.md`
   - `artifacts/detailed-design/000-task-tracker.md`
   - 基于 [template.md](../template.md)维护的入口编排记录

## 3. 模式消费与一致性校验

### 3.0 输入溯源与一致性校验门（V-01~V-05）

**执行顺序**：V-05 → V-02 → V-01 → V-03 → V-04

#### V-05：系统名称一致性校验（阻断项）

| 项目 | 内容 |
|---|---|
| 目的 | 检测数据源是否来自其他项目，防止功能范围混淆 |
| 检测对象 | P1~P3 输入文档中的系统名称、功能描述关键词 |
| 检测规则 | 扫描"车牌识别"/"LPR"/"License Plate" /"实时识别" /"出入口识别"等非 HTVT 系统关键词 |
| 基准 | 蓝图 1.1 章应明确为 "HTVT 隧道车辆跟踪系统" 或等价描述 |
| 执行时机 | P0~P3 读取完成后，三联表建立前 |
| 阻断条件 | 任一 P1~P3 文档出现异系统关键词 |
| 阻断信息 | "检测到数据源可能来自其他项目，当前系统关键词 '[词]' 与蓝图系统名称 '[系统]' 不符，请确认 P1~P3 输入正确" |
| 处理措施 | blocked，等待人工确认数据源 |

#### V-02：编号系统收敛（警告项）

| 项目 | 内容 |
|---|---|
| 目的 | 统一阶段内引用编号，避免 FR-XXX/MVP-XXX 混用导致理解偏差 |
| 检测对象 | P1~P3 中使用的功能编号格式 |
| 收敛规则 | 统一收敛到 MVP-XXX 格式；FR-XXX 仅作为追溯字段 |
| 执行时机 | V-05 通过后 |
| 警告条件 | 发现 FR-XXX 作为主体引用 |
| 处理措施 | warning，自动收敛到 MVP-XXX，记录原始 FR-XXX 到三联表 |

#### V-01：范围数量一致性（阻断项）

| 项目 | 内容 |
|---|---|
| 目的 | 确保 SCP、MVP、三联表条目数量一致 |
| 检测对象 | `len(SCP-in-scope)` vs `len(MVP-in-scope)` vs `len(三联表)` |
| 执行时机 | 三联表建立后 |
| 阻断条件 | 数量不一致 |
| 处理措施 | blocked，转 DD-03 澄清，列出差异项 |

#### V-03：功能描述一致性（警告项）

| 项目 | 内容 |
|---|---|
| 目的 | 检测蓝图与 MVP 对同一功能的描述是否存在重大偏差 |
| 检测方式 | 计算功能描述的文本相似度（哈希或编辑距离） |
| 阈值 | 差异 < 20% 为正常，>= 20% 为警告 |
| 执行时机 | V-01 通过后 |
| 警告条件 | 任一功能描述差异 >= 20% |
| 处理措施 | warning，以 P3 (MVP) 描述为准，记录差异 |

#### V-04：组件覆盖完整性（阻断项）

| 项目 | 内容 |
|---|---|
| 目的 | 确保所有 MVP 功能均有组件映射，无遗漏 |
| 检测对象 | 三联表中"组件覆盖"列非空检查 |
| 执行时机 | V-03 通过后 |
| 阻断条件 | 任一 MVP 无组件覆盖（空值或"未映射"） |
| 处理措施 | blocked，列出未覆盖 MVP，要求从蓝图 3.1 章补全或澄清 |

### 3.1 判定输入

必须至少读取以下信息：

1. 上游 `final_mode` 或等价模式结论
2. 当前 architecture 交接产物
3. 显式模式偏好（如存在）
4. 历史 `000-task-tracker.md`（如为恢复执行）
5. 当前 detailed_design 阶段输入完整度与复杂度信号

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

### 3.3 模式一致性规则

1. 若上游已给出可消费的 `standard` 或 `complete`，直接继承。
2. 若上游模式缺失、非法或与当前交接内容冲突，必须转 `blocked` 并请求补齐或用户确认。
3. 若上游模式为 `fast`，不得强行执行 detailed_design，必须阻塞并要求补正。
4. 用户覆盖仅允许在 `standard` 与 `complete` 之间切换，且必须说明原因、评分依据和生效范围。

### 3.4 `mode_decision_basis` 写法要求

`mode_decision_basis` 不能只写结论，至少要说明：

1. 采用的是上游模式还是用户覆盖
2. 触发该结论的输入依据是什么
3. 为什么选择当前模式而不是另一种
4. `G302/G303` 为什么执行或跳过

## 4. 模式与路由差异

### 4.1 路由矩阵

| mode | G301 | G302 | G303 | reviewing-software-design | GS-Quality-Check | GS-Review |
|---|---|---|---|---|---|---|
| `standard` | execute | skip | skip | execute | execute | execute |
| `complete` | execute | execute | execute | execute | execute | execute |

### 4.2 约束说明

1. `G301` 为 detailed_design 的核心必选项。
2. `G302`、`G303` 仅在 `complete` 中执行。
3. `standard` 下，`G302/G303` 必须保留任务位并明确写入跳过原因。
4. `complete` 下，`G302/G303` 必须各自通过独立子代理执行，不能合并为同一子代理的复合任务。

## 5. 澄清闭环

### 5.1 必须澄清的情况

以下情况不得跳过澄清：

1. 组件职责边界不清晰，无法稳定拆解到 `G301`
2. 接口契约关键字段缺失，影响 `G302`
3. 数据实体映射、主键/索引策略或事务边界不明确，影响 `G303`
4. architecture 交接不足以确定 detailed_design 的最小冻结范围

### 5.2 澄清输出要求

每轮澄清至少输出：

1. `clarification_reason`
2. `clarification_questions`
3. `working_assumptions`
4. `risk_if_unanswered`

### 5.3 澄清结束条件

符合以下任一条件可结束澄清：

1. 关键信息已补齐，可以进入 `G301`
2. 已达到最大澄清轮次，且必须以工作假设继续
3. 用户明确接受当前信息不完整带来的风险

## 6. 下游 SKILL 编排细则

### 6.0 子代理启动与关闭总则

1. 每个后续 SKILL 必须由独立子代理执行。
2. 子代理输入至少包含：目标 SKILL、输入路径、输出路径、验收标准、回写任务位。
3. 子代理完成后，主执行方必须先检查输出是否达到当前步骤验收标准。
4. 只有在“结果可验收 + 台账已回写”两个条件都满足后，才允许关闭该子代理。
5. 若结果未通过验收，子代理应继续用于返工或重新拉起新的子代理承接，不得在未形成可恢复状态前直接关闭。

### 6.1 G301

1. `G301` 必执行。
2. `G301` 的输入必须来自 architecture 交接产物与当前澄清结果。
3. `G301` 必须由独立子代理执行，验收通过并完成 `DD-04` 回写后关闭该子代理。

### 6.2 G302

1. `G302` 仅在 `complete` 模式执行。
2. `standard` 模式下，`G302` 固定跳过，并在任务表与模板中记录原因，同时以 `status_code=done`、`skill_stage=completed`、`review_result=skipped` 收口。
3. `G302` 必须由独立子代理执行，验收通过并完成 `DD-05` 回写后关闭该子代理。

### 6.3 G303

1. `G303` 仅在 `complete` 模式执行。
2. `standard` 模式下，`G303` 固定跳过，并在任务表与模板中记录原因，同时以 `status_code=done`、`skill_stage=completed`、`review_result=skipped` 收口。
3. `G303` 必须由独立子代理执行，输入至少包含 `artifacts/detailed-design/001-design-plan.md`、`artifacts/detailed-design/002-component-design.md`、`artifacts/architecture/003-architecture-blueprint.md`、`artifacts/architecture/001-technical-strategy.md`，验收通过并完成 `DD-06` 回写后关闭该子代理。

### 6.4 评审验证与质量门

1. `DD-07` 用于设计评审验证与追溯材料收敛。
2. `DD-08` 必须在 `DD-07` 之后启动。
3. 进入 `DD-08` 前至少应具备 `002-component-design.md`、`005-design-review-validation.md`、`006-architecture-design-traceability.md`，以及 `003-interface-design.md` / `004-data-design.md` 的适用集合。
4. 若存在 `critical` 或 `major`，不得进入 `DD-09`。

### 6.5 GS-Review

1. `DD-10` 仅在质量门通过后启动。
2. 启动前必须先将 `GS-Quality-Check` 输出归一化为 `quality_gate_ref`，不得并列传入原始 `quality_check_summary` / `validation_summary`。
3. `review_summary.decision=pass` 的必要条件是 `review_summary.pass_rate >= 85` 且无 `critical/major` 阻塞问题。
4. `decision=fail` 时，必须回写 `skill_stage=rework + status_code=in_progress + status_label=进行中 + review_result=rework + resume_from=首个 owner_task_id`。
5. `decision=pending` 时，必须回写 `skill_stage=user_review + status_code=blocked + review_result=blocked + resume_from=DD-10`。

### 6.6 reviewing-software-design

1. `reviewing-software-design` 在 `standard` 和 `complete` 模式下均执行。
2. 必须由独立子代理执行，验收通过并完成 `DD-08` 回写后关闭该子代理。
3. `standard` 模式下，评审报告中涉及 `G302/G303` 的评审分类必须标记为"不适用"并提供理由。
4. `complete` 模式下，全部分类按 `review-rubric.md` 逐项评审。
5. 启动前输入至少包含：`002-component-design.md`、`005-design-review-validation.md`、`006-architecture-design-traceability.md`，以及 `003-interface-design.md` / `004-data-design.md` 的适用集合。
6. 验收标准：产出 `007-engineering-readiness-review.md`，且必须包含结论、分数、否决状态、阻塞/非阻塞问题清单、整改计划、工程开工准备度。
7. 若 Engineering readiness = `Not ready`、存在否决项或阻塞问题，禁止进入 `DD-09`，进入 rework。

## 7. 交接细则

### 7.1 可交接条件

只有同时满足以下条件，`handoff_ready` 才能标记为 `yes`：

1. `review_summary.decision = pass`
2. `review_summary.pass_rate >= 85`
3. `DD-08` 已完成且 `review_result ∈ [pass, pass_with_conditions]`
4. 若 `review_result=pass_with_conditions`，`change_outputs` 必须包含非阻塞问题并行关闭计划
5. `detailed_design_outputs` 完整可读取
6. `review_outputs` 完整可读取
7. `change_outputs` 已包含本轮关键修订摘要

### 7.2 交接摘要最小内容

交接摘要至少包括：

1. 当前执行模式
2. 已完成 SKILL 列表
3. 未解决风险
4. 供下游 implementation 关注的范围边界与验收约束

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

该记录必须与 `runtime-task-tracker-spec.md` 的固定表头一致。

## 8. 运行时任务与恢复闭环

### 8.1 任务位含义

| task_id | 作用 |
|---|---|
| `DD-01` | detailed_design 输入接收与依赖校验 |
| `DD-02` | 模式与路由判定 |
| `DD-03` | 设计澄清闭环 |
| `DD-04` | `G301` 组件详细设计 |
| `DD-05` | `G302` 接口详细设计 |
| `DD-06` | `G303` 数据详细设计 |
| `DD-07` | 设计评审验证与追溯收敛 |
| `DD-08` | `reviewing-software-design` 工程可实现性评审 |
| `DD-09` | `GS-Quality-Check` |
| `DD-10` | `GS-Review` |
| `DD-11` | 交接给 implementation |

### 8.2 恢复规则

1. 中断后必须仅依赖 `000-task-tracker.md` 作为运行时恢复主锚点。
2. `resume_from` 至少包含：已完成的最后动作、当前待继续动作、未完成的检查或评审、缺失输入或待确认项。
3. `resume_from=DD-08` 时，必须重新读取 `G301/G302/G303` 产物和 `DD-07` 追溯文档，重新执行 `reviewing-software-design`。
4. `001-design-plan.md` 与 `template.md` 只作为辅助证据，不得作为恢复前置依赖。

### 8.3 状态更新要求

1. 进入澄清、质量检查、用户评审或交接时，必须立即更新 `skill_stage`。
2. 需要返工时，必须立即更新为 `rework`。
3. 发生阻塞时，必须立即更新为 `blocked`，并写明解除条件。
4. `DD-05`、`DD-06` 在 `standard` 下虽然跳过，但任务位不得删除，且必须使用合法枚举 `skill_stage=completed` 收口。
