# GS-Review 实例模板

## 1. 实例元信息

| 字段 | 说明 |
|---|---|
| stage | `requirements / architecture / detailed_design` |
| review_task_id | `RA-07 / AD-08 / DD-09` |
| quality_task_id | `RA-06 / AD-07 / DD-08` |
| tracker_path | `requirements -> artifacts/requirements/000-task-tracker.md; architecture -> artifacts/architecture/000-task-tracker.md; detailed_design -> artifacts/detailed-design/000-task-tracker.md` |
| review_report_path | `artifacts/reviews/001-requirements-review.md / 002-architecture-review.md / 003-detailed-design-review.md` |
| quality_gate_ref.evidence.report_path | `artifacts/reviews/requirements-quality-check.md / architecture-quality-check.md / detailed-design-quality-check.md` |
| review_gate | `RG-requirements / RG-architecture / RG-detailed-design` |
| min_pass_rate | `85` |
| min_decision | `pass` |
| updated_at | `YYYY-MM-DD` |

## 2. 子代理执行记录

| 序号 | task_id | skill_id | input_paths | quality_gate_binding | output_paths | acceptance_threshold | required_outputs | acceptance_requirements | tracker_binding | start_status | acceptance_status | close_status | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `RA-07 / AD-08 / DD-09` | `GS-Review` | `tracker_path; stage_documents; quality_gate_ref` | `quality_gate_ref(task_id; overall_status; issue_count.critical; issue_count.major; issue_count.minor; issue_count.warning; issues; evidence.report_path)` | `review_report_path` | `min_pass_rate=85; min_decision=pass` | `review_summary; rework_actions; quality_issue_disposition; consumed_quality_gate.task_id; evidence.report_path; evidence.tracker_path; execution_status; updated_at; blocking_issues(gate_decision=blocked only)` | `decision=pass/fail/pending`; `pass_rate>=85`; `failed_items` 已回填；`rework_required -> rework_actions`; `blocked -> blocking_issues`; `acceptance_status=passed`; `close_status=closed` | `review_task_id` | 待启动 / 已启动 | `pending / passed / failed` | `pending / closed` | 若调用方仍以独立 `quality_report_path` 启动，视为外部兼容输入而非本技能硬依赖 |

## 3. 输入检查

### 3.1 阶段文档包

| path | required | document_role | exists | notes |
|---|---|---|---|---|
|  | `true / false` | `stage_output / review_report / skill_contract` | `true / false` |  |

### 3.2 质量门引用

| 字段 | 值 |
|---|---|
| quality_gate_ref.task_id | 与 `quality_task_id` 一致 |
| quality_gate_ref.overall_status | `pass / pass_with_warning` |
| quality_gate_ref.issue_count.critical |  |
| quality_gate_ref.issue_count.major |  |
| quality_gate_ref.issue_count.minor |  |
| quality_gate_ref.issue_count.warning |  |
| quality_gate_ref.evidence.report_path |  |
| quality_gate_ref.checked_documents | 可选 |
| quality_gate_ref.failed_documents | 可选 |
| quality_gate_ref.evidence.tracker_path | 可选 |

### 3.3 质量门问题清单

| issue_id | checker | severity | owner_document | message | evidence_ref |
|---|---|---|---|---|---|
|  |  | `critical / major / minor / warning` |  |  |  |

## 4. 评审结论

### 4.1 review_summary

| 字段 | 值 |
|---|---|
| decision | `pass / fail / pending` |
| gate_decision | `pass / rework / blocked` |
| pass_rate |  |
| **frontend_readiness** | **Ready / Ready with conditions / Not ready** — 基于前端消费契约评估前端独立开发准备度 |
| reviewed_items |  |
| passed_items |  |
| failed_items |  |
| rework_items |  |
| blocked_items |  |
| quality_gate_status | `pass / pass_with_warning` |

### 4.2 blocking_issues

| issue_id | severity | owner_task_id | owner_document | source | message |
|---|---|---|---|---|---|
|  | `critical / major / minor / warning` |  |  | `quality_gate / stage_review` |  |

### 4.3 rework_actions

| action_id | owner_task_id | target_document | action | source_issue_ids |
|---|---|---|---|---|
|  |  |  |  | `issue-001, issue-002` |

### 4.4 quality_issue_disposition

| issue_id | disposition | closure_note | closure_evidence |
|---|---|---|---|
|  | `accepted / closed / rework_required / blocked` |  |  |

## 5. consumed_quality_gate

| 字段 | 值 |
|---|---|
| task_id | 与 `quality_gate_ref.task_id` 一致 |
| overall_status | `pass / pass_with_warning` |
| issue_count.critical |  |
| issue_count.major |  |
| issue_count.minor |  |
| issue_count.warning |  |
| issues | `issue_id 列表` |
| evidence.report_path |  |
| optional_extensions.checked_documents | 可选 |
| optional_extensions.failed_documents | 可选 |
| optional_extensions.tracker_path | 可选 |

## 6. 证据与输出

| 字段 | 值 |
|---|---|
| evidence.report_path | `artifacts/reviews/001-requirements-review.md / 002-architecture-review.md / 003-detailed-design-review.md` |
| evidence.reviewed_document_paths | `path 列表` |
| evidence.tracker_path | 与 `tracker_path` 一致 |
| execution_status.acceptance_status | `pending / passed / failed` |
| execution_status.close_status | `pending / closed` |
| updated_at | `YYYY-MM-DD` |

## 7. 运行时任务推进表回写

| task_id | skill_id | skill_stage | step_name | description | inputs | outputs | dependencies | status_code | status_label | review_result | resume_from | evidence_path | updated_at |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `RA-07 / AD-08 / DD-09` | `GS-Review` | `user_review / rework` | `review-gate` | 执行阶段汇总评审门；返工时将 `skill_stage` 改为 `rework` 且保持 `status_code=in_progress`，阻塞时保持 `user_review` | `stage_documents; quality_gate_ref; tracker_path` | `review_report_path` | `GS-Quality-Check 已通过` | `todo / in_progress / done / blocked` | `未开始 / 进行中 / 完成 / 阻塞` | `pass / rework / blocked` | `返工时写 owner_task_id；阻塞时写当前 review_task_id` | `由调用方按阶段既有证据入口维护` | `YYYY-MM-DD` |

## 8. 交付与返工记录

| 字段 | 值 |
|---|---|
| handoff_ready | `yes / no` |
| required_review_gate | `RG-requirements / RG-architecture / RG-detailed-design` |
| return_to_task_ids | `RA-03~RA-05 / AD-03~AD-06 / DD-03~DD-07` |
| acceptance_result | `通过 / 不通过` |
| notes |  |
