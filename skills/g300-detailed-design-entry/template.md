# Detailed Design 阶段入口编排记录

## 文档元信息

| 项目 | 内容 |
|---|---|
| stage_id | `detailed_design` |
| entry_skill_id | `G300` |
| 文档版本 | `v1.2` |
| 生成日期 | `YYYY-MM-DD` |
| 最后更新 | `YYYY-MM-DD` |
| 作者 | `G300` |
| 状态 | 草稿 / 评审中 / 已通过 |

## 1. 输入摘要

| 项目 | 内容 |
|---|---|
| user_request |  |
| mode_preference |  |
| tracker_path | `artifacts/detailed-design/000-task-tracker.md` |
| governance_refs | `../_shared/governance/*.md` |

### 1.1 初始摘要

- 目标：
- 范围：
- 约束：
- 待确认项：

### 1.2 范围基线（SCP-MVP-FR 三联映射表）

| SCP-ID | MVP-ID | FR-ID | 功能描述 | 优先级 | 组件覆盖 | **has_frontend_ui** | **uiux_ref** |
|---|---|---|---|---|---|---|---|
| SCP-001 | MVP-001 | FR-001 | （从 004-mvp-definition.md 提取） | Must | CMP-XXX | yes / no | UI-001 |
| ... | ... | ... | ... | ... | ... | ... | ... |

**收敛规则**：

- 功能描述以 `artifacts/requirements/004-mvp-definition.md` 3.1 章为准
- 阶段内统一使用 MVP-XXX 编号引用
- 组件覆盖从 `artifacts/architecture/003-architecture-blueprint.md` 3.1 章提取
- `uiux_ref` 从上游 `004-mvp-definition.md` 3.1 的 `frontend_ui_ref` 字段提取，编号保持一致

### 1.x 输入溯源与校验报告（G300 生成，强制章节）

| 校验项 | 源文档 | 校验结果 | 备注 |
|---|---|---|---|
| 系统名称一致性 (V-05) | `003-architecture-blueprint.md` 1.1 | ✅/❌ | 系统名称：HTVT 隧道车辆跟踪系统 |
| 编号系统收敛 (V-02) | 统一收敛到 MVP-XXX | ✅/⚠️ | 原始编号：FR-XXX |
| 范围数量一致 (V-01) | SCP vs MVP 计数 | ✅/❌ | SCP: X 项, MVP: X 项 |
| 功能描述一致 (V-03) | 蓝图 vs MVP 哈希比对 | ✅/⚠️ | 差异：X% |
| 组件覆盖完整 (V-04) | 28 组件覆盖 X 项功能 | ✅/❌ | 覆盖率：X% |
| 前端界面映射一致性 (V-06) | `004-mvp-definition.md` 3.1 / `003-requirements-baseline.md` 10.2 | ✅/❌ | has_frontend_ui=yes 的 MVP 必须有 uiux_ref |

**异常记录**：

- [ ] 无异常
- [x] 存在异常（详见下方）

| 异常ID | 检查点 | 描述 | 处理措施 |
|---|---|---|---|
| EX-01 | | | |

**校验执行人**: G300  
**校验时间**: YYYY-MM-DD  
**校验结论**: ✅ 通过 / ❌ 未通过（转澄清/阻断）

### 1.y 下游消费约定

G301/G302/G303 及下游 skill：

- ✅ **必须** 以本章 1.2 节"范围基线"为功能范围唯一基准
- ✅ **必须** 以本章 1.x 节"输入溯源与校验报告"为输入验证依据
- ❌ **禁止** 直接读取上游 requirements/architecture 阶段原始文档
- ⚠️ 如需补充信息，应通过 G300 触发澄清，不得自行追溯上游

## 2. 模式判定

| 项目 | 值 |
|---|---|
| total_score |  |
| dimension_scores.D1 |  |
| dimension_scores.D2 |  |
| dimension_scores.D3 |  |
| dimension_scores.D4 |  |
| recommended_mode |  |
| final_mode |  |
| mode_source | upstream / user_override |
| mode_decision_basis |  |
| clarification_required | yes / no |

### 2.1 缺失字段

- missing_fields:
- clarification_questions:
- working_assumptions:
- risk_if_unanswered:

### 2.2 澄清判定

| 项目 | 值 |
|---|---|
| clarification_required | yes / no |
| clarification_round | 0 |
| clarification_reason |  |

### 2.3 路由差异

| skill_id | standard | complete | 说明 |
|---|---|---|---|
| `G301` | execute | execute | 组件详细设计，始终执行 |
| `G302` | **conditional** | execute | 接口详细设计；standard 模式下若存在 `has_frontend_ui=yes` 的 MVP 则强制执行，否则跳过 |
| `G303` | skip | execute | 数据详细设计，仅在 `complete` 执行 |

## 3. 执行清单

| 顺序 | skill_id | 是否执行 | 原因 | 输入 | 输出 |
|---|---|---|---|---|---|
| 1 | `G301` | yes | 组件详细设计必选 | architecture 输出、澄清记录（如有） | `artifacts/detailed-design/002-component-design.md` |
| 2 | `G302` | yes / no | `standard` 模式下若存在 `has_frontend_ui=yes` 则强制执行，否则跳过；`complete` 下必须执行 | `G301` 产物、技术策略 | `artifacts/detailed-design/003-interface-design.md` |
| 3 | `G303` | yes / no | `standard` 下固定跳过，不启动子代理，`complete` 下必须执行 | `artifacts/detailed-design/001-design-plan.md`、`artifacts/detailed-design/002-component-design.md`、`artifacts/architecture/003-architecture-blueprint.md`、`artifacts/architecture/001-technical-strategy.md` | `artifacts/detailed-design/004-data-design.md` |
| 4 | `DD-07` | yes | 汇总设计评审验证与追溯材料 | `G301/G302/G303` 产物 | `artifacts/detailed-design/005-design-review-validation.md`; `artifacts/detailed-design/006-architecture-design-traceability.md` |
| 5 | `reviewing-software-design` | yes | 工程可实现性评审门，判断研发能否基于设计文档开工 | `G301/G302/G303` 产物、`DD-07` 追溯文档 | `artifacts/detailed-design/007-engineering-readiness-review.md` |
| 6 | `GS-Quality-Check` | yes | 质量门必须先于评审门 | detailed_design 正式文档 | `artifacts/reviews/detailed-design-quality-check.md` |
| 7 | `GS-Review` | yes | 汇总评审门 | 质量门结果、正式文档 | `artifacts/reviews/003-detailed-design-review.md` |

### 3.1 子代理执行记录

| 顺序 | task_id | target_skill | input_paths | output_paths | acceptance_requirements | writeback_task_id | subagent_id | 启动状态 | 验收状态 | 关闭状态 | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `DD-04` | `G301` | architecture_outputs; design_plan; clarification_outputs(conditional) | `artifacts/detailed-design/002-component-design.md` | 组件设计可支撑 G302/G303 或直接进入 DD-07 | `DD-04` |  | 待启动 / 已启动 | 待验收 / 通过 / 不通过 | 待关闭 / 已关闭 |  |
| 2 | `DD-05` | `G302` | `artifacts/detailed-design/001-design-plan.md`; `artifacts/detailed-design/002-component-design.md`; `artifacts/architecture/003-architecture-blueprint.md`; `artifacts/architecture/001-technical-strategy.md` | `artifacts/detailed-design/003-interface-design.md` | complete 模式下接口设计形成且可追溯；standard 模式下仅当 has_frontend_ui=yes 时启动 | `DD-05` |  | 待启动 / 已启动 | 待验收 / 通过 / 不通过 | 待关闭 / 已关闭 | `standard` 条件触发，`complete` 必启动 |
| 3 | `DD-06` | `G303` | `artifacts/detailed-design/001-design-plan.md`; `artifacts/detailed-design/002-component-design.md`; `artifacts/architecture/003-architecture-blueprint.md`; `artifacts/architecture/001-technical-strategy.md` | `artifacts/detailed-design/004-data-design.md` | complete 模式下数据设计形成且可追溯 | `DD-06` |  | 待启动 / 已启动 | 待验收 / 通过 / 不通过 | 待关闭 / 已关闭 | `standard` 跳过，`complete` 启动 |
| 4 | `DD-08` | `reviewing-software-design` | `artifacts/detailed-design/002-component-design.md`; `003-interface-design.md`(conditional); `004-data-design.md`(conditional); `005-design-review-validation.md`; `006-architecture-design-traceability.md` | `artifacts/detailed-design/007-engineering-readiness-review.md` | 报告含结论/分数/否决状态/阻塞问题/整改计划/开工准备度；standard 下接口/数据分类标记不适用 | `DD-08` |  | 待启动 / 已启动 | 待验收 / 通过 / 不通过 | 待关闭 / 已关闭 | 先于质量门；存在阻塞问题时禁止关闭并进入 rework |
| 5 | `DD-09` | `GS-Quality-Check` | detailed_design_outputs; `artifacts/detailed-design/006-architecture-design-traceability.md` | `artifacts/reviews/detailed-design-quality-check.md` | overall_status=pass/pass_with_warning 且 critical=0 major=0 | `DD-09` |  | 待启动 / 已启动 | 待验收 / 通过 / 不通过 | 待关闭 / 已关闭 | 先于评审门 |
| 6 | `DD-10` | `GS-Review` | quality_gate_ref; detailed_design_outputs; `artifacts/detailed-design/007-engineering-readiness-review.md` | `artifacts/reviews/003-detailed-design-review.md` | decision=pass 且 pass_rate>=85；quality_gate_ref.overall_status=pass/pass_with_warning；Engineering readiness ≠ Not ready | `DD-10` |  | 待启动 / 已启动 | 待验收 / 通过 / 不通过 | 待关闭 / 已关闭 | 启动前先完成质量门输出归一化 |

## 4. 运行时任务推进

| task_id | skill_id | skill_stage | step_name | description | inputs | outputs | dependencies | status_code | status_label | review_result | resume_from | evidence_path | updated_at |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `DD-01` | `stage-shared` | `intake` | `design-intake` | 建立 detailed_design 阶段 intake 与初始上下文 | architecture 交接产物 | `001-design-plan.md` | `-` | `in_progress` / `done` / `blocked` | 进行中 / 完成 / 阻塞 | `-` |  | `evidence/DD-01/` | `YYYY-MM-DD` |
| `DD-02` | `stage-shared` | `planning` | `mode-and-route` | 消费阶段模式并确认 `G302/G303` 执行策略 | 输入摘要、模式上下文、复杂度上下文 | `001-design-plan.md` | `DD-01` | `todo` / `in_progress` / `done` / `blocked` | 未开始 / 进行中 / 完成 / 阻塞 | `-` |  | `evidence/DD-02/` | `YYYY-MM-DD` |
| `DD-03` | `stage-shared` | `clarification` | `design-clarification` | 对关键设计缺失项发起澄清并形成回传记录（如触发） | `001-design-plan.md` | `001a-design-clarification.md` | `DD-02` | `todo` / `in_progress` / `done` / `blocked` | 未开始 / 进行中 / 完成 / 阻塞 | `no-op` / `pass` / `rework` |  | `evidence/DD-03/` | `YYYY-MM-DD` |
| `DD-04` | `G301` | `drafting` | `component-design` | 输出组件职责、边界、依赖、异常处理和验收要点 | 设计计划、架构蓝图、澄清记录（如有） | `002-component-design.md` | `DD-02`、`DD-03(conditional)` | `todo` / `in_progress` / `done` / `blocked` | 未开始 / 进行中 / 完成 / 阻塞 | `pass` / `rework` / `blocked` |  | `evidence/DD-04/` | `YYYY-MM-DD` |
| `DD-05` | `G302` | `drafting` | `interface-design` | 输出接口契约、错误码、幂等性、版本策略；`standard` 模式跳过时改为 `skill_stage=completed`、`review_result=skipped`，返工时改为 `rework` | `001-design-plan.md`; `002-component-design.md`; `003-architecture-blueprint.md`; `001-technical-strategy.md` | `003-interface-design.md` | `DD-04` | `todo` / `in_progress` / `done` / `blocked` | 未开始 / 进行中 / 完成 / 阻塞 | `skipped` / `pass` / `rework` |  | `evidence/DD-05/` | `YYYY-MM-DD` |
| `DD-06` | `G303` | `drafting` | `data-design` | 输出数据对象、所有权、存储边界、一致性、生命周期、演化、迁移、异常、测试与风险设计；`standard` 模式跳过时改为 `skill_stage=completed`、`review_result=skipped`，返工时改为 `rework` | `artifacts/detailed-design/001-design-plan.md`; `artifacts/detailed-design/002-component-design.md`; `artifacts/architecture/003-architecture-blueprint.md`; `artifacts/architecture/001-technical-strategy.md` | `004-data-design.md` | `DD-04` | `todo` / `in_progress` / `done` / `blocked` | 未开始 / 进行中 / 完成 / 阻塞 | `skipped` / `pass` / `rework` |  | `evidence/DD-06/` | `YYYY-MM-DD` |
| `DD-07` | `stage-shared` | `drafting` | `design-review-validation` | 收敛设计问题并输出评审验证主文档与追溯文档；返工时改为 `rework` | 组件/接口/数据设计文档 | `005-design-review-validation.md`; `006-architecture-design-traceability.md` | `DD-04`、`DD-05(conditional)`、`DD-06(conditional)` | `todo` / `in_progress` / `done` / `blocked` | 未开始 / 进行中 / 完成 / 阻塞 | `pass` / `rework` / `blocked` |  | `evidence/DD-07/` | `YYYY-MM-DD` |
| `DD-08` | `reviewing-software-design` | `user_review` | `engineering-readiness-review` | 对 detailed_design 产出进行工程可实现性评审，判断研发能否基于设计文档开工 | 组件/接口/数据设计文档；追溯文档 | `007-engineering-readiness-review.md` | `DD-04`、`DD-05`(conditional)、`DD-06`(conditional)、`DD-07` | `todo` / `in_progress` / `done` / `blocked` | 未开始 / 进行中 / 完成 / 阻塞 | `pass` / `pass_with_conditions` / `rework` / `blocked` |  | `evidence/DD-08/` | `YYYY-MM-DD` |
| `DD-09` | `GS-Quality-Check` | `quality_check` | `quality-gate` | 执行 detailed_design 阶段质量门 | detailed_design 正式文档 | `artifacts/reviews/detailed-design-quality-check.md` | `DD-08` | `todo` / `in_progress` / `done` / `blocked` | 未开始 / 进行中 / 完成 / 阻塞 | `pass` / `pass_with_warning` / `fail` |  | `evidence/DD-09/` | `YYYY-MM-DD` |
| `DD-10` | `GS-Review` | `user_review` | `review-gate` | 执行 detailed_design 阶段汇总评审门；启动前先把质量门输出归一化为 `quality_gate_ref`，返工时改为 `rework` 且保持 `status_code=in_progress` | quality_gate_ref、正式文档 | `artifacts/reviews/003-detailed-design-review.md` | `DD-09` | `todo` / `in_progress` / `done` / `blocked` | 未开始 / 进行中 / 完成 / 阻塞 | `pass` / `rework` / `blocked` |  | `evidence/DD-10/` | `YYYY-MM-DD` |
| `DD-11` | `stage-shared` | `handoff` | `handoff-ready` | 生成交接摘要并登记阶段交接记录 | 评审通过结果、正式文档 | `handoff_summary`; `handoff_record` | `DD-10` | `todo` / `in_progress` / `done` / `blocked` | 未开始 / 进行中 / 完成 / 阻塞 | `-` |  | `evidence/DD-11/` | `YYYY-MM-DD` |

## 5. 质量门与评审门

### 5.1 质量检查结果

| 项目 | 值 |
|---|---|
| checker_tool | `GS-Quality-Check` |
| quality_report_path | `artifacts/reviews/detailed-design-quality-check.md` |
| quality_check_summary.overall_status | pass / pass_with_warning / fail |
| quality_check_summary.scores.completeness |  |
| quality_check_summary.scores.markdown_format |  |
| quality_check_summary.scores.traceability |  |
| validation_summary.issue_count.critical |  |
| validation_summary.issue_count.major |  |
| validation_summary.issue_count.minor |  |
| validation_summary.issue_count.warning |  |
| quality_gate_ref.task_id | DD-09 |
| quality_gate_ref.overall_status | pass / pass_with_warning |
| quality_gate_ref.issue_count.critical | 归一化自 validation_summary.issue_count.critical |
| quality_gate_ref.issue_count.major | 归一化自 validation_summary.issue_count.major |
| quality_gate_ref.issue_count.minor | 归一化自 validation_summary.issue_count.minor |
| quality_gate_ref.issue_count.warning | 归一化自 validation_summary.issue_count.warning |
| quality_gate_ref.issues | 归一化自 issues，`pass_with_warning` 时必须完整带入 |
| quality_gate_ref.evidence.report_path | artifacts/reviews/detailed-design-quality-check.md |
| checked_at | `YYYY-MM-DD HH:mm` |

### 5.2 评审结果

| 项目 | 值 |
|---|---|
| review_summary.decision | pass / fail / pending |
| review_summary.gate_decision | pass / rework / blocked |
| review_summary.pass_rate |  |
| review_summary.reviewed_items |  |
| review_summary.passed_items |  |
| review_summary.failed_items |  |
| review_report_path | `artifacts/reviews/003-detailed-design-review.md` |
| acceptance_threshold.min_pass_rate | `85` |

### 5.3 工程可实现性评审结果

| 项目 | 值 |
|---|---|
| review_skill | `reviewing-software-design` |
| readiness_report_path | `artifacts/detailed-design/007-engineering-readiness-review.md` |
| review_summary.decision | pass / pass_with_conditions / fail |
| review_summary.score |  |
| review_summary.veto_triggered | yes / no |
| review_summary.blocking_issues.count |  |
| review_summary.non_blocking_issues.count |  |
| engineering_readiness | Ready / Ready with conditions / Not ready |
| readiness_gate_ref.task_id | DD-08 |
| readiness_gate_ref.decision | 归一化自 review_summary.decision |
| readiness_gate_ref.blocking_issues | 归一化自阻塞问题清单 |
| readiness_gate_ref.non_blocking_issues | 归一化自非阻塞问题清单 |
| readiness_gate_ref.evidence.report_path | artifacts/detailed-design/007-engineering-readiness-review.md |
| reviewed_at | `YYYY-MM-DD HH:mm` |

## 6. 交接摘要

| 项目 | 内容 |
|---|---|
| handoff_ready | yes / no |
| handoff_summary |  |
| detailed_design_outputs |  |
| review_outputs |  |
| change_outputs |  |
| downstream_target | implementation |

### 6.1 供下游阶段消费的最小字段

- recommended_mode:
- final_mode:
- mode_source:
- mode_decision_basis:
- handoff_summary:
- detailed_design_outputs:
- review_outputs:
- change_outputs:
- review_summary.decision:
- review_summary.pass_rate:
- engineering_readiness:

### 6.2 阶段交接记录

| handoff_id | from_stage | to_stage | required_outputs | review_gate | status | notes | updated_at |
|---|---|---|---|---|---|---|---|
| `HO-DD-001` | `detailed_design` | `implementation` | `artifacts/detailed-design/002-component-design.md; artifacts/detailed-design/005-design-review-validation.md; artifacts/detailed-design/006-architecture-design-traceability.md; artifacts/detailed-design/007-engineering-readiness-review.md; artifacts/reviews/003-detailed-design-review.md; artifacts/detailed-design/003-interface-design.md (complete only); artifacts/detailed-design/004-data-design.md (complete only); change_outputs=artifacts/detailed-design/001a-design-clarification.md (when DD-03 triggered, otherwise \`none\` must be recorded in notes)` | `RG-detailed-design` | ready / blocked | `required_outputs` 需随模式与澄清结果解释：`standard` 下不要求 `003/004`，`DD-03=no-op` 时必须显式记录 `change_outputs=none`；若 `DD-08=pass_with_conditions`，必须记录并行关闭的非阻塞问题清单及开工限制说明 | `YYYY-MM-DD` |

## 7. 风险与恢复

### 7.1 当前风险

- 风险：

### 7.2 恢复入口

- 已完成动作：
- 下一步动作：
- 阻塞条件：
- 解除条件：
