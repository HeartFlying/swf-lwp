# Requirements 阶段入口编排记录

## 文档元信息

| 项目 | 内容 |
|---|---|
| skill_id | G100 |
| 文档版本 | v1.2 |
| 生成日期 | YYYY-MM-DD |
| 最后更新 | YYYY-MM-DD |
| 作者 | G100 |
| 状态 | 草稿 / 评审中 / 已通过 |

## 1. 输入摘要

| 项目 | 内容 |
|---|---|
| user_request |  |
| mode_preference |  |
| tracker_path | artifacts/requirements/000-task-tracker.md |
| governance_refs | ../_shared/governance/*.md |

### 1.1 初始需求摘要

- 目标：
- 范围：
- 约束：
- 待确认项：
- 领域术语状态：已加载 / 待产出 / 无术语需记录
- CONTEXT.md 路径：artifacts/requirements/CONTEXT.md

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

## 3. 执行清单

| 顺序 | skill_id | 是否执行 | 原因 | 输入 | 输出 |
|---|---|---|---|---|---|
| 1 | G101 | yes / no |  |  | artifacts/requirements/002-business-context.md |
| 2 | G102 | yes |  |  | artifacts/requirements/003-requirements-baseline.md |
| 3 | G103 | yes |  |  | artifacts/requirements/004-mvp-definition.md |
| 4 | GS-Quality-Check | yes |  |  | artifacts/reviews/requirements-quality-check.md |
| 5 | PRD-Design-Readiness-Review | yes | 执行 PRD 设计准入专业评审，判断需求产出是否具备进入系统设计的条件 | requirements 阶段正式文档包 | artifacts/reviews/001a-prd-design-readiness-review.md |
| 6 | Software-FMEA-Review | yes / no（fast 模式跳过） | 执行系统化失效模式与风险分析；standard 模式轻量扫描 top 3-5 高风险功能，complete 模式覆盖全部 in-scope 功能 + NFR 专项 | requirements 阶段正式文档包 + PRD 准入评审报告 | artifacts/reviews/001b-fmea-risk-review.md |
| 7 | GS-Review | yes | 统一消费 `quality_gate_ref` 归一化输入，汇总评审阶段文档包（含 PRD 设计准入评审报告和 FMEA 风险评审报告） | quality_gate_ref; prd-readiness-report; fmea-risk-report; requirements_outputs | artifacts/reviews/001-requirements-review.md |

### 3.1 子代理执行记录

| 顺序 | skill_id | subagent_required | subagent_id | 启动状态 | evidence 状态 | 验收状态 | 关闭状态 |
|---|---|---|---|---|---|---|---|
| 1 | G101 | yes |  | 待启动 / 已启动 | 待产出 / 已产出 / 缺失 | 待验收 / 通过 / 不通过 | 待关闭 / 已关闭 |
| 2 | G102 | yes |  | 待启动 / 已启动 | 待产出 / 已产出 / 缺失 | 待验收 / 通过 / 不通过 | 待关闭 / 已关闭 |
| 3 | G103 | yes |  | 待启动 / 已启动 | 待产出 / 已产出 / 缺失 | 待验收 / 通过 / 不通过 | 待关闭 / 已关闭 |
| 4 | GS-Quality-Check | yes |  | 待启动 / 已启动 | 待产出 / 已产出 / 缺失 | 待验收 / 通过 / 不通过 | 待关闭 / 已关闭 |
| 5 | PRD-Design-Readiness-Review | yes |  | 待启动 / 已启动 | 待产出 / 已产出 / 缺失 | 待验收 / 通过 / 不通过 | 待关闭 / 已关闭 |
| 6 | Software-FMEA-Review | yes / no（fast 模式不启动） |  | 待启动 / 已启动 | 待产出 / 已产出 / 缺失 / N/A | 待验收 / 通过 / 不通过 | 待关闭 / 已关闭 |
| 7 | GS-Review | yes |  | 待启动 / 已启动 | 待产出 / 已产出 / 缺失 | 待验收 / 通过 / 不通过 | 待关闭 / 已关闭 |

## 4. 运行时任务推进

| task_id | skill_id | skill_stage | step_name | description | inputs | outputs | dependencies | status_code | status_label | review_result | resume_from | evidence_path | evidence_status | updated_at |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RA-01 | stage-shared | intake | intake-init | 建立阶段 intake 与初始上下文 | user_request | artifacts/requirements/001-requirements-intake.md | - | in_progress / done / blocked | 进行中 / 完成 / 阻塞 | - |  | evidence/RA-01/ | N/A | YYYY-MM-DD |
| RA-02 | stage-shared | clarification | clarification-loop | 执行澄清分流、记录问题与假设 | intake、评分结果 | clarification_questions、working_assumptions | RA-01 | todo / in_progress / done / blocked | 未开始 / 进行中 / 完成 / 阻塞 | no-op / - |  | evidence/RA-02/ | N/A | YYYY-MM-DD |
| RA-03 | G101 | drafting / rework | business-context | 产出业务背景分析或记录跳过原因 | intake、clarification_outputs | artifacts/requirements/002-business-context.md | RA-02 | todo / in_progress / done / blocked | 未开始 / 进行中 / 完成 / 阻塞 | skipped / pass / rework |  | evidence/RA-03/ | 待产出 / 已产出 / 缺失 | YYYY-MM-DD |
| RA-04 | G102 | drafting / rework | baseline-build | 冻结需求基线 | intake、G101_outputs | artifacts/requirements/003-requirements-baseline.md | RA-02, RA-03 | todo / in_progress / done / blocked | 未开始 / 进行中 / 完成 / 阻塞 | - |  | evidence/RA-04/ | 待产出 / 已产出 / 缺失 | YYYY-MM-DD |
| RA-05 | G103 | drafting / rework | mvp-build | 形成 MVP 定义 | G102_outputs | artifacts/requirements/004-mvp-definition.md | RA-04 | todo / in_progress / done / blocked | 未开始 / 进行中 / 完成 / 阻塞 | - |  | evidence/RA-05/ | 待产出 / 已产出 / 缺失 | YYYY-MM-DD |
| RA-06 | GS-Quality-Check | quality_check / rework | quality-gate | 执行 requirements 阶段质量门 | intake、G10x_outputs | artifacts/reviews/requirements-quality-check.md | RA-03, RA-04, RA-05 | todo / in_progress / done / blocked | 未开始 / 进行中 / 完成 / 阻塞 | pass / pass_with_warning / fail |  | evidence/RA-06/ | 待产出 / 已产出 / 缺失 | YYYY-MM-DD |
| RA-07a | prd-design-readiness-review | professional_review | prd-readiness-review | 执行 PRD 设计准入专业评审 | requirements 阶段正式文档包 | artifacts/reviews/001a-prd-design-readiness-review.md | RA-06 | todo / in_progress / done / blocked | 未开始 / 进行中 / 完成 / 阻塞 | PASS / CONDITIONAL_PASS / FAIL |  | evidence/RA-07a/ | 待产出 / 已产出 / 缺失 | YYYY-MM-DD |
| RA-07b | software-fmea-review | professional_review / rework | fmea-risk-review | 执行系统化失效模式与风险分析；fast 模式跳过；standard 模式轻量扫描 top 3-5 高风险功能；complete 模式覆盖全部 in-scope 功能 + NFR 专项 | intake、G10x_outputs、PRD 准入评审报告 | artifacts/reviews/001b-fmea-risk-review.md | RA-07a | todo / in_progress / done / blocked / skipped | 未开始 / 进行中 / 完成 / 阻塞 / 跳过 | AP=H 需预防/探测措施 / pass / rework |  | evidence/RA-07b/ | 待产出 / 已产出 / 缺失 / N/A | YYYY-MM-DD |
| RA-07c | GS-Review | user_review / rework | review-gate | 执行 requirements 阶段汇总评审门；启动前先把质量门输出归一化为 `quality_gate_ref`，并将 PRD 设计准入评审报告和 FMEA 风险评审报告纳入 stage_documents；返工时改为 `rework` 且保持 `status_code=in_progress` | quality_gate_ref、prd-readiness-report、fmea-risk-report、G10x_outputs | artifacts/reviews/001-requirements-review.md | RA-07a, RA-07b（如执行） | todo / in_progress / done / blocked | 未开始 / 进行中 / 完成 / 阻塞 | pass / rework / blocked |  | evidence/RA-07c/ | 待产出 / 已产出 / 缺失 | YYYY-MM-DD |
| RA-08 | stage-shared | handoff / completed | handoff-ready | 生成交接摘要并登记阶段交接记录 | review_outputs、requirements_outputs | handoff_summary、handoff_record | RA-07c | todo / in_progress / done / blocked | 未开始 / 进行中 / 完成 / 阻塞 | - |  | evidence/RA-08/ | N/A | YYYY-MM-DD |

说明：

- `evidence_status` 用于追踪 evidence 目录的产出状态。
- 子代理执行的阶段（RA-03~RA-07c）：`evidence_status` 必须为 `已产出` 才能关闭子代理；`缺失` 表示 evidence 目录为空或缺少过程证据文件。
- 入口编排自身执行的阶段（RA-01/RA-02/RA-08）：`evidence_status` 为 `N/A`（证据已在 intake/tracker/handoff 中记录）。
- `fast` 模式跳过 RA-07b 时，`evidence_status` 为 `N/A`。

## 5. 质量门与评审门

### 5.1 质量检查结果

| 项目 | 值 |
|---|---|
| checker_tool | GS-Quality-Check |
| quality_report_path | artifacts/reviews/requirements-quality-check.md |
| quality_check_summary.overall_status | pass / pass_with_warning / fail |
| quality_check_summary.scores.completeness |  |
| quality_check_summary.scores.traceability |  |
| quality_check_summary.scores.markdown_format |  |
| validation_summary.issue_count.critical |  |
| validation_summary.issue_count.major |  |
| validation_summary.issue_count.minor |  |
| validation_summary.issue_count.warning |  |
| quality_gate_ref.task_id | RA-06 |
| quality_gate_ref.overall_status | pass / pass_with_warning |
| quality_gate_ref.issue_count.critical | 归一化自 validation_summary.issue_count.critical |
| quality_gate_ref.issue_count.major | 归一化自 validation_summary.issue_count.major |
| quality_gate_ref.issue_count.minor | 归一化自 validation_summary.issue_count.minor |
| quality_gate_ref.issue_count.warning | 归一化自 validation_summary.issue_count.warning |
| quality_gate_ref.issues | 归一化自 issues，`pass_with_warning` 时必须完整带入 |
| quality_gate_ref.evidence.report_path | artifacts/reviews/requirements-quality-check.md |
| checked_at | YYYY-MM-DD HH:mm |

### 5.2 评审结果

| 项目 | 值 |
|---|---|
| review_summary.decision | pass / fail / pending |
| review_summary.gate_decision | pass / rework / blocked |
| review_summary.pass_rate |  |
| review_summary.reviewed_items |  |
| review_summary.passed_items |  |
| review_summary.failed_items |  |
| review_report_path | artifacts/reviews/001-requirements-review.md |

### 5.3 PRD 设计准入评审结果

| 项目 | 值 |
|---|---|
| prd_readiness_checker | prd-design-readiness-review |
| prd_readiness_report_path | artifacts/reviews/001a-prd-design-readiness-review.md |
| prd_readiness_summary.gate_result | PASS / CONDITIONAL_PASS / FAIL |
| prd_readiness_summary.final_score |  |
| prd_readiness_summary.blocker_avg_score |  |
| prd_readiness_summary.review_mode | FULL_REVIEW / QUICK_BLOCKER_REVIEW |
| prd_readiness_summary.checklist_used | true / false |
| prd_readiness_summary.failed_blockers |  |
| prd_readiness_summary.required_prd_actions |  |
| prd_readiness_summary.design_stage_notes |  |
| checked_at | YYYY-MM-DD HH:mm |

### 5.4 FMEA 风险评审结果

| 项目 | 值 |
|---|---|
| fmea_checker | software-fmea-review |
| fmea_report_path | artifacts/reviews/001b-fmea-risk-review.md |
| fmea_summary.execution_depth | full / lightweight / skipped |
| fmea_summary.risk_items_total |  |
| fmea_summary.ap_h_count |  |
| fmea_summary.ap_m_count |  |
| fmea_summary.ap_l_count |  |
| fmea_summary.top_risks |  |
| fmea_summary.nfr_conclusion |  |
| fmea_summary.remediation_open_count |  |
| checked_at | YYYY-MM-DD HH:mm |

## 6. 交接摘要

| 项目 | 内容 |
|---|---|
| handoff_ready | yes / no |
| handoff_summary |  |
| requirements_outputs |  |
| review_outputs |  |
| change_outputs |  |
| downstream_target | architecture |

### 6.1 供下游阶段消费的最小字段

- recommended_mode:
- final_mode:
- mode_decision_basis:
- handoff_summary:
- requirements_outputs:
- review_summary.decision:
- prd_readiness_summary.gate_result:
- prd_readiness_summary.required_prd_actions:
- fmea_summary.ap_h_count:
- fmea_summary.top_risks:
- fmea_summary.nfr_conclusion:
- context_path:
- context_status:

### 6.2 阶段交接记录

| handoff_id | from_stage | to_stage | required_outputs | review_gate | status | notes | updated_at |
|---|---|---|---|---|---|---|---|
| HO-REQ-001 | requirements | architecture | artifacts/requirements/001-requirements-intake.md; artifacts/requirements/003-requirements-baseline.md; artifacts/requirements/004-mvp-definition.md; artifacts/reviews/001a-prd-design-readiness-review.md; artifacts/reviews/001b-fmea-risk-review.md | RG-requirements | ready / blocked |  | YYYY-MM-DD |

## 7. 风险与恢复

### 7.1 当前风险

- 风险：

### 7.2 恢复入口

- 已完成动作：
- 下一步动作：
- 阻塞条件：
- 解除条件：
