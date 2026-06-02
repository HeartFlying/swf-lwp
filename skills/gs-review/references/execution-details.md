# GS-Review 执行细化说明

## 1. 阶段映射

| stage | review_task_id | quality_task_id | caller_skill | review_gate | review_report_path | quality_report_path |
|---|---|---|---|---|---|---|
| `requirements` | `RA-07` | `RA-06` | `G100` | `RG-requirements` | `artifacts/reviews/001-requirements-review.md` | `artifacts/reviews/requirements-quality-check.md` |
| `architecture` | `AD-08` | `AD-07` | `G200` | `RG-architecture` | `artifacts/reviews/002-architecture-review.md` | `artifacts/reviews/architecture-quality-check.md` |
| `detailed_design` | `DD-09` | `DD-08` | `G300` | `RG-detailed-design` | `artifacts/reviews/003-detailed-design-review.md` | `artifacts/reviews/detailed-design-quality-check.md` |

## 2. 对 GS-Quality-Check 的消费边界

### 2.1 最小必需字段

1. `quality_gate_ref.task_id`
1. `quality_gate_ref.overall_status`
2. `quality_gate_ref.issue_count`
3. `quality_gate_ref.issues`
4. `quality_gate_ref.evidence.report_path`

### 2.2 可选扩展字段

1. `quality_gate_ref.checked_documents`
2. `quality_gate_ref.failed_documents`
3. `quality_gate_ref.evidence.tracker_path`

### 2.3 归一化规则

`GS-Review` 不直接消费 `quality_check_summary` 或 `validation_summary` 原始结构。来自 `GS-Quality-Check` 的输出必须先归一化为：

1. `quality_task_id -> quality_gate_ref.task_id`
2. `quality_check_summary.overall_status -> quality_gate_ref.overall_status`
3. `validation_summary.issue_count -> quality_gate_ref.issue_count`
4. `issues -> quality_gate_ref.issues`
5. `evidence.report_path -> quality_gate_ref.evidence.report_path`
6. `validation_summary.checked_documents -> quality_gate_ref.checked_documents`
7. `validation_summary.failed_documents -> quality_gate_ref.failed_documents`
8. `evidence.tracker_path -> quality_gate_ref.evidence.tracker_path`

### 2.4 消费规则

1. `overall_status=pass` 时，可正常进入汇总评审。
2. `overall_status=pass_with_warning` 时，必须把 `issues` 显式带入评审结论和返工动作。
3. `overall_status=fail` 时，当前任务必须转 `blocked`，不得启动评审门。
4. `GS-Review` 不负责重新计算质量门结果，只负责消费与放大其影响。
5. `quality_gate_ref.evidence.report_path` 是质量门结果的唯一正式报告字段；独立 `quality_report_path` 仅属于外部兼容输入，不属于本技能最小输入契约。

## 3. 评审决策规则

### 3.1 `decision=pass`

同时满足以下条件：

1. `pass_rate >= min_pass_rate`
2. 无 `critical/major` 阻塞问题
3. 当前阶段正式文档包齐备
4. 质量门问题已通过 `quality_issue_disposition` 明确为 `accepted` 或 `closed`

### 3.2 `decision=fail`

适用于以下任一情况：

1. 存在 `minor/warning` 问题需要返工
2. 评审新增发现需要修改但不构成立即阻塞
3. `pass_rate < min_pass_rate`，但问题可通过返工闭环解决

### 3.3 `decision=pending`

适用于以下任一情况：

1. 最小输入字段缺失
2. 输出路径或阶段映射非法
3. `GS-Quality-Check` 未通过或质量报告不可用
4. 当前阶段正式文档包不完整，无法形成有效汇总评审

### 3.4 `decision` 与 `gate_decision` 的固定映射

1. `gate_decision=pass -> decision=pass`
2. `gate_decision=rework -> decision=fail`
3. `gate_decision=blocked -> decision=pending`
4. `failed_items = rework_items + blocked_items`
5. `quality_issue_disposition` 必须覆盖所有 `quality_gate_ref.issues`
6. `quality_issue_disposition.disposition=rework_required` 时，必须至少命中一条 `rework_actions.source_issue_ids`
7. `quality_issue_disposition.disposition=blocked` 时，必须至少命中一条 `blocking_issues.issue_id`

## 4. 子代理执行闭环

### 4.1 启动

启动时必须显式绑定：

1. `stage`
2. `review_task_id`
3. `tracker_path`
4. `review_report_path`
5. `stage_documents`
6. `quality_gate_ref`
7. `acceptance_threshold`
8. `required_outputs`
9. `acceptance_requirements`

### 4.2 验收

验收时必须检查：

1. 正式评审报告已写入阶段固定路径
2. `review_summary` 完整
3. `rework_actions`、`quality_issue_disposition` 完整；`gate_decision=blocked` 时 `blocking_issues` 也必须完整
4. `consumed_quality_gate` 完整
5. `updated_at` 已回写
6. 运行时台账目标任务位已回写
7. `pass_with_warning` 输入下，每条质量门问题都已有机读处置结果
8. `evidence.report_path`、`evidence.tracker_path`、`execution_status.acceptance_status` 已生成

### 4.3 关闭

1. 验收通过前不得关闭子代理
2. 回写未完成前不得关闭子代理
3. 关闭前必须把最终 `decision` 和 `report_path` 交回调用方
4. 关闭完成后必须回写 `execution_status.close_status=closed`

## 5. 运行时台账回写规则

### 5.1 回写目标

| stage | review_task_id |
|---|---|
| `requirements` | `RA-07` |
| `architecture` | `AD-08` |
| `detailed_design` | `DD-09` |

### 5.2 回写字段

1. `status_code`
2. `status_label`
3. `skill_stage`
4. `review_result`
5. `resume_from`
6. `updated_at`

### 5.3 回写结果

1. `decision=pass` -> `skill_stage=user_review`、`status_code=done`、`status_label=完成`、`review_result=pass`
2. `decision=fail` -> `skill_stage=rework`、`status_code=in_progress`、`status_label=进行中`、`review_result=rework`、`resume_from=首个 owner_task_id`
3. `decision=pending` -> `skill_stage=user_review`、`status_code=blocked`、`status_label=阻塞`、`review_result=blocked`、`resume_from=current review_task_id`
4. `evidence_path` 保持调用方既有证据入口语义，本技能不强制覆盖

## 6. 恢复规则

1. 恢复只依赖当前阶段 `000-task-tracker.md`
2. 读取 `stage`、`review_task_id`、`tracker_path` 与任务位当前状态
3. 按阶段映射推导 `review_report_path`
4. 若报告已存在，则进入验收/补写流程；若不存在，则重新执行评审步骤
5. 若外部阶段入口尚未同步 `execution_status`、`consumed_quality_gate.task_id` 等新增字段，属于外部依赖，在联调时单独核验，不影响本目录内契约收口

## 7. 对阶段入口的影响

1. `G100` 只应消费 `artifacts/reviews/001-requirements-review.md`
2. `G200` 只应消费 `artifacts/reviews/002-architecture-review.md`
3. `G300` 只应消费 `artifacts/reviews/003-detailed-design-review.md`
4. 阶段入口不得以 `{stage}-review.md` 这类动态命名替代固定输出

## 8. 前端独立开发可行性评审视角

### 8.1 适用阶段

仅在 `detailed_design` 阶段执行。

### 8.2 评审输入

1. `artifacts/requirements/003-requirements-baseline.md` 第 10 章（UI/UX 交付物）
2. `artifacts/requirements/004-mvp-definition.md` 3.1 章（`has_frontend_ui` + `frontend_ui_ref`）
3. `artifacts/detailed-design/003-interface-design.md` 第 2.3 章（前端消费契约，参见 G302 执行细化）

### 8.3 评审检查项

| 检查项 | 通过标准 | 失败处理 |
|---|---|---|
| UI/UX 交付物完整性 | G102 `10.1` 中所有 `has_frontend_ui=yes` 的 MVP 都有对应的 UI/UX 交付物 | `major` 问题，要求补全 |
| 前端消费契约完整性 | G302 `2.3` 中所有 `frontend-backend` 接口都有 TypeScript类型 + 调用示例 + Mock方案 | `major` 问题，要求补全 |
| 前端独立开发可行性 | 基于 `2.3` 的 Mock方案 + 错误处理建议，前端团队能否在缺少后端的情况下完成 80% 以上的界面开发 | `minor` 问题（默认）；若项目明确需要前后端并行开发则升级为 `major`） |
| 前后端接口语义一致性 | G302 `2.3` 中的 TypeScript类型 与 `2.2` 中的字段约束是否一致 | `critical` 问题，必须修复 |

### 8.4 评审角色

增加以下评审角色（按需参与）：

| 角色 | 职责 | 是否必须 |
|---|---|:---:|
| 前端技术负责人 | 评估前端消费契约是否足够支撑独立开发 | **是**（当存在 frontend-backend 接口时） |
| 产品经理/UX设计师 | 确认 UI/UX 交付物覆盖度 | 建议 |

**输出要求**：前端评审结论并入 `artifacts/reviews/003-detailed-design-review.md` 的 `4.1 review_summary` 与 `4.3 rework_actions` 中，不单独产出报告。
