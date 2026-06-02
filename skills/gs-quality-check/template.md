# GS-Quality-Check 执行模板

## 1. 服务信息

| 项目 | 内容 |
|---|---|
| stage | `requirements / architecture / detailed_design` |
| stage_tracker_dir | `requirements / architecture / detailed-design` |
| stage_report_name | `requirements / architecture / detailed-design` |
| quality_task_id | `RA-06 / AD-07 / DD-08` |
| caller_skill | `G100 / G200 / G300` |
| tracker_path | `artifacts/{stage_tracker_dir}/000-task-tracker.md` |
| report_path | `artifacts/reviews/{stage_report_name}-quality-check.md` |
| review_gate | `RG-requirements / RG-architecture / RG-detailed-design` |
| updated_at | `YYYY-MM-DD` |

## 2. 输入记录

### 2.1 目标文档

| document_role | path | required | exists | notes |
|---|---|---|---|---|
| `stage_output` / `review_report` / `skill_contract` |  | `true` |  |  |

### 2.2 检查器配置

| checker_id | source | required | executed | status | notes |
|---|---|---|---|---|---|
| `QC-001` | `derived_by_document_role` | `true` |  |  |  |
| `QC-002` | `derived_by_document_role` | `true` |  |  |  |
| `QC-003` | `derived_by_document_role` | `true` |  |  |  |
| `QC-004` | `derived_by_document_role` | `true` |  |  |  |
| `QC-005` | `derived_by_document_role` | `true` |  |  |  |
| `QC-006` | `derived_by_document_role` | `conditional` |  |  |  |
| `QC-007` | `derived_by_document_role` | `conditional` |  |  |  |
| `QC-009` | `derived_by_document_role` | `conditional` |  |  |  |
| `QC-010` | `derived_by_gate_closure` | `conditional` |  |  |  |
| `QC-FE-001` | `derived_by_frontend_flag` | `conditional` |  |  | `has_frontend_ui=yes 时触发` |
| `QC-FE-002` | `derived_by_frontend_flag` | `conditional` |  |  | `has_frontend_ui=yes 时触发` |
| `QC-FE-003` | `derived_by_frontend_flag` | `conditional` |  |  | `interface_type=frontend-backend 时触发` |

## 3. 子代理执行记录

| subagent_id | bound_skill | input_paths | output_paths | acceptance_rule | tracker_task_id | status | updated_at |
|---|---|---|---|---|---|---|---|
|  | `GS-Quality-Check` |  |  | `critical=0 && major=0 才允许推进评审门` |  |  |  |

## 4. 服务内部结果与对外归一化输出

本模板保留两层信息：

1. `4.1`、`4.2` 仅用于本技能内部形成质量报告与归一化映射，不作为调用方输入契约。
2. 调用方与下游技能只允许消费 `4.3 quality_gate_ref.*`。

### 4.1 服务内部原始结果（仅本技能内部使用）

| 字段 | 内容 |
|---|---|
| quality_check_summary.overall_status | `pass / pass_with_warning / fail` |
| quality_check_summary.executed_checkers |  |
| quality_check_summary.scores.completeness |  |
| quality_check_summary.scores.markdown_format |  |
| quality_check_summary.scores.traceability |  |
| quality_check_summary.scores.consistency |  |
| validation_summary.issue_count.critical |  |
| validation_summary.issue_count.major |  |
| validation_summary.issue_count.minor |  |
| validation_summary.issue_count.warning |  |
| validation_summary.checked_documents |  |
| validation_summary.failed_documents |  |

### 4.2 问题清单（内部原始问题）

| issue_id | checker | severity | owner_document | evidence_ref | message |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### 4.3 调用方唯一正式输出：quality_gate_ref

| 字段 | 内容 |
|---|---|
| quality_gate_ref.task_id | `RA-06 / AD-07 / DD-08` |
| quality_gate_ref.overall_status | `pass / pass_with_warning / fail` |
| quality_gate_ref.issue_count.critical | `validation_summary.issue_count.critical` |
| quality_gate_ref.issue_count.major | `validation_summary.issue_count.major` |
| quality_gate_ref.issue_count.minor | `validation_summary.issue_count.minor` |
| quality_gate_ref.issue_count.warning | `validation_summary.issue_count.warning` |
| quality_gate_ref.issues | `4.2 问题清单` |
| quality_gate_ref.evidence.report_path | `artifacts/reviews/{stage_report_name}-quality-check.md` |
| quality_gate_ref.scores.completeness | `quality_check_summary.scores.completeness` |
| quality_gate_ref.scores.markdown_format | `quality_check_summary.scores.markdown_format` |
| quality_gate_ref.scores.traceability | `quality_check_summary.scores.traceability` |
| quality_gate_ref.scores.consistency | `quality_check_summary.scores.consistency` |
| quality_gate_ref.executed_checkers | `quality_check_summary.executed_checkers` |
| quality_gate_ref.checked_documents | `validation_summary.checked_documents` |
| quality_gate_ref.failed_documents | `validation_summary.failed_documents` |
| quality_gate_ref.evidence.tracker_path | `artifacts/{stage_tracker_dir}/000-task-tracker.md` |
| quality_gate_ref.updated_at | `YYYY-MM-DD` |

## 5. 运行时任务推进

| task_id | skill_id | skill_stage | step_name | description | inputs | outputs | dependencies | status_code | status_label | review_result | resume_from | evidence_path | updated_at |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `RA-06 / AD-07 / DD-08` | `GS-Quality-Check` | `quality_check` | `stage_quality_gate` | `执行阶段质量门并形成统一报告` | `target_documents; stage_summary; tracker_path` | `artifacts/reviews/{stage_report_name}-quality-check.md` | `阶段核心文档已完成` |  |  |  |  | `由调用方按阶段既有证据入口维护` |  |

## 6. 门禁交付

| stage | next_gate | allowed | basis | notes |
|---|---|---|---|---|
|  | `GS-Review` |  | `quality_gate_ref.overall_status`；调用方不得并列传入 `quality_check_summary` / `validation_summary` |  |

## 7. 恢复入口

| 项目 | 内容 |
|---|---|
| restore_precondition | `artifacts/{stage_tracker_dir}/000-task-tracker.md` |
| last_completed_action |  |
| next_action |  |
| unresolved_issues |  |
| resume_from |  |
