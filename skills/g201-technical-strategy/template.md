# G201 技术策略文档模板

## 1. 策略目标与约束

### 1.1 策略目标

- 目标摘要：
- 对齐的架构目标：
- 成功标准：

### 1.2 约束边界

| constraint_id | 类型 | 描述 | 强制性 | 来源 | 影响 |
|---|---|---|---|---|---|
| CST-001 | business / technical / compliance / delivery |  | yes / no |  |  |

## 2. 技术路线候选

| option_id | 技术域 | 候选方案 | 适用条件 | 优势 | 风险 |
|---|---|---|---|---|---|
| OPT-001 |  |  |  |  |  |

## 3. 关键选型与权衡

| decision_id | 决策主题 | 推荐方案 | 备选方案 | 推荐理由 | 不采用原因 |
|---|---|---|---|---|---|
| DEC-001 |  |  |  |  |  |

### 3.1 权衡摘要

| tradeoff_id | 维度 | 选择结论 | 收益 | 代价 | 备注 |
|---|---|---|---|---|---|
| TO-001 | performance / security / cost / delivery |  |  |  |  |

## 4. 实施约束与 ADR 候选

### 4.1 实施约束

| implementation_constraint_id | 约束 | 对蓝图的影响 | 必须遵守项 |
|---|---|---|---|
| IC-001 |  |  |  |

### 4.2 ADR 候选

| adr_candidate_id | 决策主题 | 进入 ADR 的原因 | 预期结论 |
|---|---|---|---|
| ADRC-001 |  |  |  |

## 5. 风险与替代路线

| risk_id | 风险 | 当前策略 | 替代路线 | 触发条件 |
|---|---|---|---|---|
| RSK-001 |  |  |  |  |

## 6. 方法检查清单

填写规则：

1. `已执行方法` 只能填写 [architecture-methods-catalog.md](../_shared/architecture-methods-catalog.md) 中已定义的标准方法名。
2. 不得使用同义词、缩写、临时命名或自由改写名称。
3. 若某步骤启用了可选方法，也必须使用方法目录中的标准名称。

### 6.1 核心步骤方法对齐

| step_id | 必用方法 | 可选方法 | 已执行方法 | 备注 |
|---|---|---|---|---|
| step-1 | 架构原则约束映射；约束驱动选型；技术域分层分析 | 假设清单与验证计划 |  |  |
| step-2 | 决策矩阵；ATAM 权衡分析；风险驱动决策 | 替代路线与触发条件分析 |  |  |
| step-3 | 决策矩阵；成本-收益-风险权衡；约束驱动选型 | ADR 思维 |  |  |
| step-4 | ADR 思维；假设清单与验证计划；替代路线与触发条件分析 | 架构原则约束映射 |  |  |

## 8. 质量检查对齐信息

| 项目 | 内容 |
|---|---|
| checker_tool | GS-Quality-Check |
| quality_report_path | artifacts/reviews/architecture-quality-check.md |
| quality_check_summary.overall_status | pass / pass_with_warning / fail |
| validation_summary.issue_count.critical |  |
| validation_summary.issue_count.major |  |
| validation_summary.issue_count.minor |  |
| validation_summary.issue_count.warning |  |
| checked_at | YYYY-MM-DD HH:mm |

## 9. 追溯与证据

| conclusion_id | 结论 | 来源输入 | 证据说明 |
|---|---|---|---|
| TR-001 |  |  |  |
