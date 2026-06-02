# G203 架构蓝图文档模板

## 1. 蓝图目标与范围

### 1.1 蓝图目标

- 蓝图目标摘要：
- 对齐的技术策略目标：
- 成功标准：

### 1.2 范围边界

| scope_id | 范围项 | 类型 | 说明 | 来源约束 | 备注 |
|---|---|---|---|---|---|
| SCP-001 |  | in_scope / out_of_scope / deferred |  |  |  |

## 2. 架构视图

### 2.1 蓝图视图清单

| view_id | 视图类型 | 目标 | 覆盖对象 | 关键约束 |
|---|---|---|---|---|
| VW-001 | context / structure / interaction / deployment |  |  |  |

### 2.2 视图说明

| view_id | 视图名称 | 核心内容 | 输入来源 | 关联 ADR |
|---|---|---|---|---|
| VW-001 |  |  |  |  |

### 2.3 视图覆盖声明

| legacy_capability | coverage_view_ids | coverage_fields | 覆盖说明 |
|---|---|---|---|
| S5-A02 架构视图 | VW-001 | architecture_views / component_inventory / interaction_flows |  |
| S5-A03 数据架构 | VW-001 | data_architecture |  |
| S5-A04 接口架构 | VW-001 | interface_architecture / interaction_flows |  |
| S5-A05 部署架构 | VW-001 | deployment_topology |  |

## 3. 组件与职责

### 3.1 组件清单

| component_id | 组件/模块 | 所属边界 | 核心职责 | **frontend_consumer** | 上游依赖 | 下游依赖 |
|---|---|---|---|---|---|---|
| CMP-001 |  |  |  | yes / no |  |  |

### 3.2 核心数据对象与存储边界

| data_object_id | 数据对象 | 所属业务边界 | 权威写入位置 | 读取/派生位置 | 一致性/主从边界 | 生命周期要求 |
|---|---|---|---|---|---|---|
| DAT-001 |  |  |  |  | strong / eventual / read_write_split / master_slave |  |

### 3.3 数据流转与治理约束

| data_flow_id | 数据对象 | 来源 | 目标 | 流转方式 | 一致性要求 | 生命周期阶段 |
|---|---|---|---|---|---|---|
| DFL-001 | DAT-001 |  |  | sync / async / batch / stream |  | create / use / archive / delete |

## 4. 关键交互与依赖

### 4.1 关键交互链路

| flow_id | 链路名称 | 触发者 | 主要步骤 | 异常路径 | 关联组件 |
|---|---|---|---|---|---|
| FLW-001 |  |  |  |  |  |

### 4.2 接口架构清单

| interface_id | 接口边界 | 提供方 | 消费方 | **frontend_consumer_refs** | 调用方式 | 契约约束 | 异常语义 | 集成模式 |
|---|---|---|---|---|---|---|---|---|
| IFC-001 | internal / external |  |  | - | sync_api / async_event / batch / file / stream |  |  | request_response / publish_subscribe / callback / pipeline |

### 4.3 关键依赖与集成约束

| dependency_id | 来源组件 | 目标组件/系统 | 依赖类型 | 集成约束 | 稳定性/版本约束 | risk_ref_id |
|---|---|---|---|---|---|---|
| DEP-001 |  |  | sync_api / async_event / data / runtime |  |  |  |

## 5. 部署拓扑与运行边界

| topology_id | 运行节点/部署单元 | 所属环境 | 部署职责 | 高可用/隔离要求 | 关联约束 |
|---|---|---|---|---|---|
| TOP-001 |  |  |  |  |  |

## 6. ADR 清单

### 6.1 ADR 条目

| adr_id | 决策主题 | 状态 | 决策结论 | 关联视图/组件 | 依据 |
|---|---|---|---|---|---|
| ADR-001 |  | proposed / accepted / deferred |  |  |  |

### 6.2 ADR 文档索引

| adr_id | 文档位置 | 关联决策/约束 | 后续动作 |
|---|---|---|---|
| ADR-001 | `artifacts/architecture/004-adr.md#adr-001` |  |  |

### 6.3 ADR 最小结构契约

| adr_id | context | decision | consequences | source_view_ids | source_component_ids |
|---|---|---|---|---|---|
| ADR-001 |  |  |  | VW-001 | CMP-001 |

## 7. 方法检查清单

填写规则：

1. `已执行方法` 只能填写 [architecture-methods-catalog.md](../_shared/architecture-methods-catalog.md) 中已定义的标准方法名。
2. 不得使用同义词、缩写、临时命名或自由改写名称。
3. 若某步骤启用了可选方法，也必须使用方法目录中的标准名称。

### 7.1 核心步骤方法对齐

| step_id | 必用方法 | 可选方法 | 已执行方法 | 备注 |
|---|---|---|---|---|
| step-1 | 蓝图范围切片；架构视图映射；约束落图 | 蓝图追溯映射 |  |  |
| step-2 | 组件职责分解；接口与依赖建模；关键链路走查 | 视图一致性检查 |  |  |
| step-3 | 部署拓扑建模；约束落图；视图一致性检查 | 关键链路走查 |  |  |
| step-4 | ADR 固化；蓝图追溯映射；视图一致性检查 | 风险热点复核 |  |  |

## 8. 质量检查对齐信息

| 项目 | 内容 |
|---|---|
| checker_tool | GS-Quality-Check |
| quality_report_path | artifacts/reviews/architecture-quality-check.md |
| quality_check_summary.overall_status | pass / pass_with_warning / fail |
| quality_check_summary.scores.completeness |  |
| quality_check_summary.scores.consistency |  |
| validation_summary.issue_count.critical |  |
| validation_summary.issue_count.major |  |
| validation_summary.issue_count.minor |  |
| validation_summary.issue_count.warning |  |
| checked_at | YYYY-MM-DD HH:mm |

## 9. 追溯与证据

| conclusion_id | 结论 | 来源输入 | 证据说明 |
|---|---|---|---|
| TR-001 |  |  |  |
