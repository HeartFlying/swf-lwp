# GS-Quality-Check 执行细化说明

## 1. 作用

本文件补充 `GS-Quality-Check` 的阶段门执行细节、门禁判定、台账回写、恢复入口与子代理关闭规则。

## 2. 阶段门映射

| stage | quality_task_id | caller_skill | next_gate | review_gate |
|---|---|---|---|---|
| `requirements` | `RA-06` | `G100` | `RA-07 / GS-Review` | `RG-requirements` |
| `architecture` | `AD-07` | `G200` | `AD-08 / GS-Review` | `RG-architecture` |
| `detailed_design` | `DD-08` | `G300` | `DD-09 / GS-Review` | `RG-detailed-design` |

要求：

1. `quality_task_id` 与 `stage` 必须一一对应。
2. 任何跨阶段错配都视为输入错误，直接阻塞执行。
3. `detailed_design` 的路径落点必须使用 `detailed-design` 目录与报告命名，不得直接拼接 `detailed_design`。

## 3. 文档角色与检查器映射

### 3.1 最小映射

| document_role | minimal_checkers |
|---|---|
| `stage_output` | `QC-001, QC-002, QC-003, QC-004, QC-005, QC-006, QC-007` |
| `review_report` | `QC-001, QC-002, QC-003, QC-004, QC-005, QC-010` |
| `skill_contract` | `QC-001, QC-002, QC-003, QC-004, QC-005, QC-006, QC-009` |

要求：

1. `QC-009` 不作为所有阶段正式产物文档的默认最小检查器。
2. `QC-007` 是阶段正式产物文档的最小集合组成部分。
3. `QC-010` 仅在评审/质量报告或台账闭环场景作为最小集合组成部分。

## 4. 检查器执行细则

### 4.1 最小执行集合

对阶段正式文档包，按文档角色执行最小集合：

1. `stage_output`：`QC-001 ~ QC-007`
2. `review_report`：`QC-001 ~ QC-005`、`QC-010`
3. `skill_contract`：`QC-001 ~ QC-006`、`QC-009`

### 4.2 按需增强集合

满足以下条件时追加检查器：

1. 需要校验台账与证据闭环时，增加 `QC-010`
2. 需要额外校验技能目录结构或正式路径命名时，增加 `QC-009`
3. 调用方显式追加扩展检查器时，只能增加不能减少最小集合
4. 当阶段文档包中包含含前端界面的 MVP（`has_frontend_ui=yes`）时，追加 `QC-FE-001`、`QC-FE-002`、`QC-FE-003`。
5. `QC-FE-*` 检查器仅在 `detailed_design` 阶段执行；`requirements` 和 `architecture` 阶段不执行。

### 4.3 评分口径

1. `completeness` 由 `QC-001/QC-003/QC-004/QC-FE-001/QC-FE-002/QC-FE-003` 汇总。
2. `markdown_format` 由 `QC-002` 汇总。
3. `traceability` 由 `QC-007/QC-FE-001` 汇总。
4. `consistency` 由 `QC-006` 汇总。

### 4.4 检查器推导规则

1. 本服务不要求调用方显式传入检查器配置
2. 服务根据 `target_documents.document_role` 自动推导 `effective_checkers`
3. `effective_checkers` 是运行时产物，不是正式输入契约字段
4. `effective_checkers` 必须最终体现在：
   - `quality_check_summary.executed_checkers`
   - `template.md` 的“检查器配置”表
   - 质量报告正文

## 5. 门禁判定

### 5.1 通过规则

1. `critical > 0` 或 `major > 0` 时，必须判为 `fail`
2. `critical = 0`、`major = 0`、(`minor > 0` 或 `warning > 0`) 时，统一判为 `pass_with_warning`
3. `critical = 0`、`major = 0`、`minor = 0`、`warning = 0` 时，判为 `pass`

### 5.2 对下游 GS-Review 的影响

进入 `GS-Review` 前，阶段入口必须先把本技能输出归一化为 `quality_gate_ref`。`GS-Review` 不直接消费 `quality_check_summary`、`validation_summary` 或 `issues` 原始结构。

归一化后的最小必需消费字段：

1. `quality_gate_ref.task_id`
2. `quality_gate_ref.overall_status`
3. `quality_gate_ref.issue_count.critical`
4. `quality_gate_ref.issue_count.major`
5. `quality_gate_ref.issue_count.minor`
6. `quality_gate_ref.issue_count.warning`
7. `quality_gate_ref.issues`
8. `quality_gate_ref.evidence.report_path`

可选扩展字段：

1. `quality_gate_ref.scores`
2. `quality_gate_ref.executed_checkers`
3. `quality_gate_ref.checked_documents`
4. `quality_gate_ref.failed_documents`
5. `quality_gate_ref.evidence.tracker_path`
6. `quality_gate_ref.updated_at`

固定映射：

1. `quality_task_id -> quality_gate_ref.task_id`
2. `quality_check_summary.overall_status -> quality_gate_ref.overall_status`
3. `validation_summary.issue_count.critical -> quality_gate_ref.issue_count.critical`
4. `validation_summary.issue_count.major -> quality_gate_ref.issue_count.major`
5. `validation_summary.issue_count.minor -> quality_gate_ref.issue_count.minor`
6. `validation_summary.issue_count.warning -> quality_gate_ref.issue_count.warning`
7. `issues -> quality_gate_ref.issues`
8. `evidence.report_path -> quality_gate_ref.evidence.report_path`
9. `validation_summary.checked_documents -> quality_gate_ref.checked_documents`
10. `validation_summary.failed_documents -> quality_gate_ref.failed_documents`
11. `quality_check_summary.executed_checkers -> quality_gate_ref.executed_checkers`
12. `quality_check_summary.scores -> quality_gate_ref.scores`
13. `evidence.tracker_path -> quality_gate_ref.evidence.tracker_path`
14. `updated_at -> quality_gate_ref.updated_at`

要求：

1. `overall_status = fail` 时，禁止启动 `GS-Review`
2. `overall_status = pass_with_warning` 时，归一化后的 `quality_gate_ref.issues` 必须完整交给 `GS-Review`
3. `GS-Review` 不得绕过本服务直接形成通过结论

## 6. 子代理执行、验收与关闭

### 6.1 启动

阶段入口 SKILL 启动本服务子代理时，必须传入：

1. `stage`
2. `quality_task_id`
3. `tracker_path`
4. `report_path`
5. `target_documents`
6. 验收条件

### 6.2 验收

子代理完成后，调用方至少验收：

1. 质量报告是否已写入 `report_path`
2. `quality_check_summary`、`validation_summary`、`issues` 是否完整
3. `executed_checkers`、`checked_documents`、`failed_documents`、`evidence.report_path`、`evidence.tracker_path`、`updated_at` 是否完整
4. 台账对应任务位是否已按共享治理回写
5. `overall_status` 是否与问题级别一致

### 6.3 关闭

1. 验收通过后，才允许关闭子代理
2. 若报告不完整、字段缺失、路径错误或台账未回写，不得关闭子代理
3. 关闭前必须记录 `subagent_id`、验收结果、输出路径和回写任务位

## 7. 运行时回写要求

### 7.1 通过

当质量门通过时：

1. `status_code=done`
2. `status_label=完成`
3. `skill_stage=quality_check`
4. `review_result=pass` 或 `pass_with_warning`
5. `evidence_path` 由调用方按阶段既有台账习惯维护，可保留既有值或指向证据目录
6. `evidence.report_path=artifacts/reviews/{stage_report_name}-quality-check.md`

### 7.2 失败

当质量门失败时：

1. 优先保持当前质量门任务 `in_progress` 并进入返工
2. 若缺少关键输入或路径不可读，可转 `blocked`
3. `review_result` 必须写明失败原因或阻塞原因
4. `resume_from` 必须写明返工入口、待修复文档和需重跑检查器

## 8. 恢复规则

恢复时仅以当前阶段 `000-task-tracker.md` 作为前置依赖。

辅助证据可包括：

1. 已生成的质量报告 `artifacts/reviews/{stage_report_name}-quality-check.md`
2. 本地 `template.md`

禁止将辅助证据当作恢复前置，也禁止将历史评审记录、版本台账或旧流程文档作为恢复前置。

## 9. 与 G100/G200/G300 的一致性要求

1. `G100` 只允许在 `RA-06` 通过后进入 `RA-07`
2. `G200` 只允许在 `AD-07` 通过后进入 `AD-08`
3. `G300` 只允许在 `DD-08` 通过后进入 `DD-09`
4. 三个阶段入口都必须消费本服务的统一字段：
   - `quality_gate_ref.task_id`
   - `quality_gate_ref.overall_status`
   - `quality_gate_ref.issue_count.critical`
   - `quality_gate_ref.issue_count.major`
   - `quality_gate_ref.issue_count.minor`
   - `quality_gate_ref.issue_count.warning`
   - `quality_gate_ref.issues`
   - `quality_gate_ref.evidence.report_path`
   - `quality_gate_ref.checked_documents`
   - `quality_gate_ref.failed_documents`
   - `quality_gate_ref.evidence.tracker_path`

## 10. 前端覆盖度检查器（QC-FE 系列）

### 10.1 QC-FE-001：前端界面清单可追溯性

| 项目 | 内容 |
|---|---|
| 检查范围 | `artifacts/requirements/004-mvp-definition.md` + `artifacts/requirements/003-requirements-baseline.md` |
| 触发条件 | `detailed_design` 阶段且存在 `has_frontend_ui=yes` 的 MVP |
| 严重级别 | `major`（不可追溯）/ `minor`（引用不一致） |

检查项：
1. `has_frontend_ui=yes` 的 MVP，`uiux_ref` 是否非空。
2. `uiux_ref` 是否能在 G102 `10.2` 前端界面清单中找到对应条目。
3. G102 `10.2` 中的前端界面是否都有至少一个 `has_frontend_ui=yes` 的 MVP 引用（无悬空界面）。
4. `frontend_ui_map`（G103 7.5）是否与 G102 `10.2` 一致。

### 10.2 QC-FE-002：前后端接口契约完整性

| 项目 | 内容 |
|---|---|
| 检查范围 | `artifacts/detailed-design/002-component-design.md` + `artifacts/detailed-design/003-interface-design.md` |
| 触发条件 | `detailed_design` 阶段且存在 `has_frontend_ui=yes` 的 MVP |
| 严重级别 | `critical`（接口缺失）/ `major`（契约不完整）/ `minor`（字段遗漏） |

检查项：
1. `has_frontend_ui=yes` 的 MVP，其组件覆盖中至少有一个组件的 `frontend_consumer=yes`。
2. `frontend_consumer=yes` 的组件，在 G301 `5.2B` 中是否有前端消费边界记录。
3. G301 `5.2B` 中记录的每条前端消费边界，在 G302 中是否有对应的 `interface_type=frontend-backend` 接口。
4. G302 中所有 `interface_type=frontend-backend` 的接口，是否都有 `2.3` 前端消费契约章节。

### 10.3 QC-FE-003：前端消费字段可用性

| 项目 | 内容 |
|---|---|
| 检查范围 | `artifacts/detailed-design/003-interface-design.md` 第 2.3 章 |
| 触发条件 | `detailed_design` 阶段且存在 `frontend-backend` 接口 |
| 严重级别 | `major`（核心字段缺失）/ `minor`（建议字段缺失）/ `warning`（可优化） |

检查项：
1. `TypeScript类型定义` 是否非空且语法合理。
2. `调用示例` 是否非空（含 HTTP 方法 + 路径 + 参数）。
3. `鉴权/跨域策略` 是否非空（前端能否实际调用）。
4. `Mock方案` 是否非空（前端独立开发是否可行）。
5. `前端错误处理建议` 是否非空（错误码是否有 UI 映射）。
