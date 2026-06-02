# G204 架构评审验证文档模板

## 1. 评审范围与文档包

### 1.1 评审目标

- 评审目标：
- 本轮范围：
- 评审结论摘要：

### 1.2 文档包范围

| document_id | path | required | document_role | produced_by | status |
|---|---|---|---|---|---|
| DOC-001 | artifacts/architecture/001-technical-strategy.md | yes | stage_output | G201 | ready / missing / blocked |
| DOC-002 | artifacts/architecture/002-architecture-vision.md | yes | stage_output | G202 | ready / missing / blocked |
| DOC-003 | artifacts/architecture/003-architecture-blueprint.md | yes | stage_output | G203 | ready / missing / blocked |
| DOC-004 | artifacts/architecture/004-adr.md | yes | stage_output | G203 | ready / missing / blocked |
| DOC-005 | artifacts/architecture/005-architecture-review-validation.md | yes | stage_output | G204 | ready / missing / blocked |

## 2. 一致性验证

### 2.1 愿景与策略承接

| check_id | 验证主题 | 来源输入 | 蓝图/ADR 体现 | 结论 | 备注 |
|---|---|---|---|---|---|
| AC-001 |  |  |  | pass / rework / blocked |  |

### 2.2 关键约束与原则映射

| mapping_id | 约束/原则 | 来源文档 | 当前承接位置 | 缺口说明 | 处理建议 |
|---|---|---|---|---|---|
| MAP-001 |  |  |  |  |  |

## 3. 质量与风险验证

### 3.1 质量属性验证

| qa_check_id | 质量属性 | 场景/目标 | 当前设计承接 | 结论 | 风险说明 |
|---|---|---|---|---|---|
| QA-CHK-001 |  |  |  | pass / rework / blocked |  |

### 3.2 风险与权衡验证

| risk_check_id | 风险/权衡主题 | 当前结论 | 剩余风险 | 缓解动作 | 触发条件 |
|---|---|---|---|---|---|
| RW-001 |  |  |  |  |  |

## 4. 评审结论与返工动作

### 4.1 review_findings

| finding_id | severity | owner_document | summary | disposition | evidence_ref |
|---|---|---|---|---|---|
| FND-001 | critical / major / minor / warning |  |  | pass / rework / blocked |  |

### 4.2 rework_actions

| action_id | owner_document | action | trigger_condition | done_criteria |
|---|---|---|---|---|
| ACT-001 |  |  |  |  |

### 4.3 评审结论摘要

| 项目 | 内容 |
|---|---|
| overall_decision | pass / rework / blocked |
| quality_gate_ready | yes / no |
| blocking_count |  |
| rework_count |  |
| notes |  |

## 5. 供 GS-Quality-Check 预组装的部分输入字段

说明：

1. 本章只填写 `G204` 直接产出的文档级字段。
2. `stage`、`quality_task_id`、`tracker_path` 以及共享服务运行时上下文由 `G200` 在触发 `AD-07` 时补齐。

### 5.1 target_documents

| document_id | path | required | document_role | produced_by | status |
|---|---|---|---|---|---|
| DOC-001 | artifacts/architecture/001-technical-strategy.md | yes | stage_output | G201 | ready / missing / blocked |
| DOC-002 | artifacts/architecture/002-architecture-vision.md | yes | stage_output | G202 | ready / missing / blocked |
| DOC-003 | artifacts/architecture/003-architecture-blueprint.md | yes | stage_output | G203 | ready / missing / blocked |
| DOC-004 | artifacts/architecture/004-adr.md | yes | stage_output | G203 | ready / missing / blocked |
| DOC-005 | artifacts/architecture/005-architecture-review-validation.md | yes | stage_output | G204 | ready / missing / blocked |

### 5.2 g203_review_targets

| target_id | source_field | source_ids | review_focus | status | evidence_ref |
|---|---|---|---|---|---|
| RVT-001 | blueprint_scope / architecture_views / coverage_declaration / component_inventory / data_architecture / interface_architecture / interaction_flows / deployment_topology / adr_index / blueprint_risks / adr_contract |  |  | pass / rework / blocked |  |

### 5.3 review_findings

| finding_id | severity | owner_document | summary | disposition | evidence_ref |
|---|---|---|---|---|---|
| FND-001 | critical / major / minor / warning |  |  | pass / rework / blocked |  |

### 5.4 quality_gate_readiness

| check_id | check_item | status | gap | note |
|---|---|---|---|---|
| QGR-001 | 正式文档包齐备 | ready / rework / blocked |  |  |

### 5.5 rework_actions

| action_id | owner_document | action | trigger_condition | done_criteria |
|---|---|---|---|---|
| ACT-001 |  |  |  |  |

## 6. 方法检查清单

填写规则：

1. `已执行方法` 只能填写 [architecture-methods-catalog.md](../_shared/architecture-methods-catalog.md) 中已定义的标准方法名。
2. 不得使用同义词、缩写、临时命名或自由改写名称。
3. 若某步骤启用了可选方法，也必须使用方法目录中的标准名称。

### 6.1 核心步骤方法对齐

| step_id | 必用方法 | 可选方法 | 已执行方法 | 备注 |
|---|---|---|---|---|
| step-1 | 系统上下文图；架构原则约束映射；约束分层法 | 假设清单与验证计划 |  |  |
| step-2 | 架构原则约束映射；技术域分层分析；ADR 思维；蓝图追溯映射 | 视图一致性检查；替代路线与触发条件分析 |  |  |
| step-3 | 质量属性场景；ATAM 权衡分析；风险驱动分析；视图一致性检查 | 风险驱动决策 |  |  |
| step-4 | 风险驱动决策；假设清单与验证计划；ADR 思维 | 替代路线与触发条件分析 |  |  |

## 7. 质量检查对齐信息

| 项目 | 内容 |
|---|---|
| checker_tool | GS-Quality-Check |
| preflight_consumer | G200 |
| quality_report_path | artifacts/reviews/architecture-quality-check.md |
| required_preflight_fields | target_documents / g203_review_targets / review_findings / quality_gate_readiness / rework_actions |
| blocked_rule | 若 quality_gate_readiness 存在 blocked，则当前轮不得进入 AD-07 |
| note | GS-Quality-Check 的正式输出字段不在本模板中维护，由共享服务独立产出 |

## 8. 追溯与证据

| conclusion_id | 结论 | 来源输入 | 证据说明 |
|---|---|---|---|
| TR-001 |  |  |  |
