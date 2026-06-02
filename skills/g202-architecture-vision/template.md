# G202 架构愿景文档模板

## 1. 架构目标与范围

### 1.1 目标摘要

- 系统目标：
- 阶段目标：
- 成功标准：

### 1.2 范围边界

- In Scope：
- Out of Scope：
- 系统边界说明：

## 2. 架构驱动因素

### 2.1 业务驱动

| driver_id | 描述 | 优先级 | 来源 | 影响 |
|---|---|---|---|---|
| BD-001 |  | P0 / P1 / P2 |  |  |

### 2.2 技术与合规驱动

| driver_id | 类型 | 描述 | 优先级 | 来源 | 影响 |
|---|---|---|---|---|---|
| TD-001 | technical / compliance / delivery |  | P0 / P1 / P2 |  |  |

## 3. 关键场景与质量属性

### 3.1 关键场景

| scenario_id | 场景名称 | 触发者 | 描述 | 优先级 | 关联驱动 |
|---|---|---|---|---|---|
| SCN-001 |  |  |  | P0 / P1 / P2 |  |

### 3.2 质量属性场景

| qa_id | 质量属性 | 场景描述 | 目标值/边界 | 优先级 | 验证提示 |
|---|---|---|---|---|---|
| QA-001 | performance / reliability / security / scalability |  |  | P0 / P1 / P2 |  |

## 4. 架构原则与边界

| principle_id | 原则 | 说明 | 对后续设计的约束 |
|---|---|---|---|
| AP-001 |  |  |  |

## 5. 风险与假设

### 5.1 工作假设

| assumption_id | 假设 | 影响范围 | 验证方式 | 状态 |
|---|---|---|---|---|
| ASM-001 |  |  |  | open / validated / rejected |

### 5.2 风险清单

| risk_id | 风险 | 概率 | 影响 | 缓解措施 | 解除条件 |
|---|---|---|---|---|---|
| RSK-001 |  | High / Medium / Low | High / Medium / Low |  |  |

## 6. 方法检查清单

填写规则：

1. `已执行方法` 只能填写 [architecture-methods-catalog.md](../_shared/architecture-methods-catalog.md) 中已定义的标准方法名。
2. 不得使用同义词、缩写、临时命名或自由改写名称。
3. 若某步骤启用了可选方法，也必须使用方法目录中的标准名称。

### 6.1 核心步骤方法对齐

| step_id | 必用方法 | 可选方法 | 已执行方法 | 备注 |
|---|---|---|---|---|
| step-1 | 系统上下文图；约束分层法；架构驱动识别 | 第一性原理 |  |  |
| step-2 | 架构驱动识别；质量属性场景；质量属性效用树 | 风险驱动分析 |  |  |
| step-3 | 质量属性场景；场景优先级排序；系统上下文图 | 事件风暴 |  |  |
| step-4 | 风险驱动分析；假设清单与验证计划；约束分层法 | 假设反转 |  |  |

## 7. 质量检查对齐信息

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

## 8. 追溯与证据

| conclusion_id | 结论 | 来源文档/输入 | 证据说明 |
|---|---|---|---|
| TR-001 |  |  |  |
