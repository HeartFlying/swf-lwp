# PRD 设计准入量化检查项参考

本文件为 `prd-design-readiness-review` Skill 的详细评分参考。执行完整评审时，逐项使用本文件中的等级、权重、必填字段和评分要点。

## 统一评分

| 分值 | 含义 |
| ---: | --- |
| 0 | 完全缺失 |
| 1 | 只有关键词级提及 |
| 2 | 有描述但不可执行 |
| 3 | 基本明确，可支持初步设计 |
| 4 | 明确可验证 |
| 5 | 完整闭环 |

## 检查项索引

| 编号 | 检查项 | 等级 | 权重 | required_fields |
| --- | --- | --- | ---: | --- |
| A1 | 是否明确业务目标 | BLOCKER | 3 | why, problem, value, success_definition |
| A2 | 是否定义成功指标或容量假设 | MAJOR | 2 | business_metric, scale_assumption, metric_basis |
| A3 | 是否明确项目范围 | BLOCKER | 3 | in_scope, out_of_scope, future_scope |
| B1 | 是否定义核心用户与角色 | BLOCKER | 3 | roles, role_scenarios, role_relationship |
| B2 | 是否明确关键权限边界 | MAJOR | 2 | allowed_actions, forbidden_actions, approval_or_audit |
| C1 | 是否定义完整主流程 | BLOCKER | 3 | start_condition, main_steps, actor_or_system, step_result, end_condition |
| C2 | 是否定义关键异常流程 | BLOCKER | 3 | failure_scenarios, business_expected_result, manual_or_auto_handling, user_visible_result |
| C3 | 是否定义核心状态流转 | BLOCKER | 3 | core_states, allowed_transitions, terminal_states, forbidden_transitions |
| C4 | 是否定义关键状态转换条件 | MAJOR | 2 | trigger_event, pre_condition, post_condition |
| D1 | 是否定义核心业务规则 | BLOCKER | 3 | rule_subject, rule_condition, rule_result, rule_boundary |
| D2 | 是否定义规则冲突处理方式 | MAJOR | 2 | conflict_scenarios, priority, manual_override |
| D3 | 是否识别重复、乱序、并发等业务风险 | MAJOR | 2 | risk_scenarios, unacceptable_result, expected_consistent_result, business_impact |
| E1 | 是否识别核心业务对象 | BLOCKER | 3 | core_entities, entity_relationship, entity_owner |
| E2 | 是否定义关键对象的唯一识别口径 | MAJOR | 2 | business_identifier, external_identifier, internal_identifier, duplicate_judgement |
| E3 | 是否说明关键数据的保留、查询和合规要求 | MINOR | 1 | query_window, retention_period, sensitivity_level, confirmation_owner |
| F1 | 是否提供性能与响应时间目标 | MAJOR | 2 | core_scenario, response_expectation, priority_level |
| F2 | 是否提供容量与增长预估 | MAJOR | 2 | user_volume, transaction_volume, data_volume, peak_or_growth, assumption_basis |
| F3 | 是否说明可用性和故障影响等级 | MAJOR | 2 | critical_scenarios, failure_impact, degradable_scenarios, priority_level |
| F4 | 是否说明安全、隐私与审计要求 | MAJOR | 2 | sensitive_data, sensitive_operations, audit_requirement, compliance_requirement, data_residency, compliance_certification_required |
| G1 | 是否识别外部依赖 | BLOCKER | 3 | dependency_name, business_usage, dependency_owner, dependency_stage |
| G2 | 是否描述关键交互边界 | MAJOR | 2 | interaction_timing, interaction_direction, key_business_info, business_result |
| G3 | 是否说明外部依赖失败时的业务期望 | BLOCKER | 3 | failure_type, business_expected_state, retry_or_manual_policy, exception_record_requirement |
| G4 | 是否明确关键交互的集成模式与实时性要求 | MAJOR | 2 | integration_scenario, sync_or_async_pattern, real_time_requirement, batch_or_stream, architecture_impact_note |
| H1 | 是否定义核心验收标准 | BLOCKER | 3 | scenario, given, when, then, pass_criteria |
| H2 | 是否定义关键边界条件 | MAJOR | 2 | numeric_boundary, time_boundary, permission_boundary, state_boundary |
| H3 | 是否覆盖关键异常测试场景 | MAJOR | 2 | business_exception_cases, dependency_exception_cases, duplicate_or_concurrent_cases, permission_exception_cases |
| I1 | 是否列出未决项和假设条件 | BLOCKER | 3 | open_items, assumptions, owner, due_date, impact_if_unresolved |
| I2 | 是否明确跨团队责任边界 | MAJOR | 2 | involved_teams, module_owner, dependency_owner, coordination_items |
| I3 | 是否说明业务或技术约束 | MAJOR | 2 | business_constraints, technical_constraints, regulatory_constraints, deployment_constraints, hard_or_soft_constraint |
| I4 | 是否明确版本边界与需求变更机制 | MAJOR | 2 | version_goal, future_evolution, change_process, impact_assessment |
| J1 | 是否说明关键业务监控与告警诉求 | MINOR | 1 | business_metrics_to_monitor, alert_scenarios, notification_role, severity |
| J2 | 是否说明人工干预和补救入口 | MINOR | 1 | manual_handling_scenarios, operator_role, operation_result, operation_record |

## 单项评分细则

### A1 业务目标

- 0：完全没有业务目标。
- 1：只有“提升体验、优化能力”等口号。
- 2：描述了目标，但问题、价值或成功标准缺失。
- 3：说明了问题和目标，可支持初步设计。
- 4：目标、价值、成功标准明确。
- 5：同时包含现状、目标、成功标准和业务影响。

### A2 成功指标或容量假设

- 0：没有任何指标或规模信息。
- 1：只有“高并发、海量数据、快速响应”等形容词。
- 2：有指标，但没有口径、范围或来源。
- 3：至少有 1 类可用指标或估算区间。
- 4：有 2 类以上指标，且口径基本明确。
- 5：有当前值、目标值、峰值或增长假设，并说明来源。

### A3 项目范围

- 0：没有范围说明。
- 1：只有笼统范围，如“交易相关能力”。
- 2：有本期范围，但缺少排除项或边界模糊。
- 3：本期范围基本明确。
- 4：本期范围和排除项明确。
- 5：范围、排除项、后续演进边界均明确。

### B1 核心用户与角色

- 0：未定义用户或角色。
- 1：只有“用户、管理员”等泛化称呼。
- 2：有角色，但没有说明参与场景。
- 3：核心角色和场景基本明确。
- 4：角色、场景、关系明确。
- 5：角色、场景、关系、组织或租户边界均明确。

### B2 关键权限边界

- 0：没有权限边界。
- 1：只有“管理员、高级权限”等模糊描述。
- 2：有权限描述，但不能判断操作边界。
- 3：关键操作权限基本明确。
- 4：允许/禁止操作和审批要求明确。
- 5：权限、审批、复核、审计要求均明确。

### C1 完整主流程

- 0：没有主流程。
- 1：只有一句概括，如“用户完成购买”。
- 2：有流程片段，但缺少关键步骤或执行方。
- 3：主流程基本完整，可初步建模。
- 4：步骤、触发方、结果明确。
- 5：主流程完整，并覆盖开始、结束、关键分支。

### C2 关键异常流程

- 0：没有异常流程。
- 1：只有“失败提示、自动重试”等泛化描述。
- 2：有异常场景，但缺少业务结果或处理方式。
- 3：覆盖主要异常，业务期望基本明确。
- 4：异常场景、处理方式、用户结果明确。
- 5：异常闭环完整，含人工入口、记录或验收口径。

### C3 核心状态流转

- 0：没有状态定义。
- 1：只说“多个状态、自动更新状态”。
- 2：有状态列表，但没有转换关系。
- 3：状态和主要转换基本明确。
- 4：状态、转换、终态明确。
- 5：状态、转换、终态、禁止转换和异常状态均明确。

### C4 关键状态转换条件

- 0：没有转换条件。
- 1：只有“满足条件后自动流转”。
- 2：有触发描述，但条件不清。
- 3：关键转换条件基本明确。
- 4：触发事件、前置条件、后置结果明确。
- 5：同时覆盖异常触发和禁止触发条件。

### D1 核心业务规则

- 0：没有核心规则。
- 1：只有“特殊处理、按规则处理”等描述。
- 2：有规则，但条件或结果不明确。
- 3：核心规则基本可编码。
- 4：对象、条件、结果、边界明确。
- 5：规则完整，含例外、边界和验收口径。

### D2 规则冲突处理

- 0：没有冲突处理。
- 1：只说“多规则同时生效”。
- 2：识别了冲突，但没有裁决方式。
- 3：主要冲突有基本处理口径。
- 4：冲突场景和优先级明确。
- 5：冲突、优先级、人工干预和审计要求均明确。

### D3 重复、乱序、并发业务风险

- 0：没有识别相关风险。
- 1：只说“避免重复、保证一致”。
- 2：有风险描述，但没有说明业务影响。
- 3：主要风险和期望结果基本明确。
- 4：风险场景、不可接受结果、期望结果明确。
- 5：同时说明影响范围、人工处理或验收方式。

说明：这一项不要求 PRD 提供完整数据一致性设计，只要求 PRD 暴露业务不可接受的错误结果。

### E1 核心业务对象

- 0：没有核心对象。
- 1：只说“业务数据”。
- 2：有对象列表，但关系或归属不清。
- 3：核心对象和基本关系明确。
- 4：对象、关系、归属明确。
- 5：对象、关系、归属、关键属性和生命周期要求基本明确。

### E2 唯一识别口径

- 0：没有唯一识别口径。
- 1：只说“唯一 ID”。
- 2：有 ID，但没有说明业务含义或来源。
- 3：核心对象识别口径基本明确。
- 4：内外部标识和重复判断明确。
- 5：标识、来源、重复判断、跨系统映射均明确。

### E3 数据保留、查询和合规

- 0：没有相关说明。
- 1：只说“长期保留、安全保护”。
- 2：有部分要求，但时间或责任不清。
- 3：查询或保留要求基本明确。
- 4：查询、保留、敏感等级明确。
- 5：查询、保留、合规、责任方均明确。

### F1 性能与响应时间目标

- 0：没有性能或体验要求。
- 1：只说“快速响应”。
- 2：有要求但没有场景或范围。
- 3：核心场景有可接受范围。
- 4：多个核心场景有响应目标和优先级。
- 5：响应目标、峰值条件、降级容忍均明确。

### F2 容量与增长预估

- 0：没有容量信息。
- 1：只说“海量、大量、高并发”。
- 2：有单一容量信息，但缺少口径。
- 3：至少 2 类容量信息或区间明确。
- 4：用户量、业务量、峰值或增长基本明确。
- 5：容量、峰值、增长、估算来源均明确。

### F3 可用性和故障影响等级

- 0：没有可用性或故障影响说明。
- 1：只说“高可用”。
- 2：有影响描述，但不能判断优先级。
- 3：关键链路和影响基本明确。
- 4：关键链路、可降级链路、影响等级明确。
- 5：影响等级、用户影响、业务损失、降级口径均明确。

### F4 安全、隐私与审计

- 0：没有安全、隐私或审计要求。
- 1：只说“系统需要安全”。
- 2：有安全要求，但对象或操作不明确。
- 3：敏感数据或敏感操作基本明确。
- 4：敏感对象、操作、审计要求明确。
- 5：安全、隐私、审计、合规边界均明确。

### G1 外部依赖

- 0：没有外部依赖说明。
- 1：只说“对接第三方系统”。
- 2：有依赖名称，但用途或 Owner 不清。
- 3：主要依赖和业务用途明确。
- 4：依赖、用途、Owner、阶段明确。
- 5：依赖、用途、Owner、阶段、失败影响均明确。

### G2 关键交互边界

- 0：没有交互边界。
- 1：只说“提供回调、系统对接”。
- 2：有交互描述，但时机或方向不清。
- 3：时机、方向、关键信息基本明确。
- 4：交互时机、方向、信息、结果明确。
- 5：同步/异步期望、异常结果和责任边界均明确。

### G3 外部依赖失败时的业务期望

- 0：没有依赖失败说明。
- 1：只说“失败后自动重试”。
- 2：有失败描述，但业务状态不清。
- 3：主要失败类型和业务期望基本明确。
- 4：失败类型、业务状态、处理口径明确。
- 5：失败闭环完整，含人工处理、异常记录和验收口径。

### G4 关键交互的集成模式与实时性要求

- 0：没有集成模式或实时性说明。
- 1：只有“系统对接、实时同步”等泛化描述。
- 2：有模式描述，但关键交互的同步/异步选择不明确。
- 3：主要交互的模式和实时性要求基本明确。
- 4：关键交互的同步/异步、批处理/流式、实时性要求明确。
- 5：集成模式、实时性要求、架构影响说明均明确，并覆盖异常场景。

说明：本项关注业务侧对交互模式的约束（如“用户下单必须同步等待支付结果”或“对账文件可接受次日批量”），这些是服务编排、事务边界和中间件选型的直接输入。不要求提供具体协议或字段设计。

### H1 核心验收标准

- 0：没有验收标准。
- 1：只有“正确处理、符合预期”。
- 2：有验收描述，但不能判断通过或失败。
- 3：核心功能验收标准基本可测试。
- 4：Given/When/Then 或等价结构明确。
- 5：覆盖主流程、关键异常和边界验收。

### H2 关键边界条件

- 0：没有边界条件。
- 1：只说“大额、频繁、长期”等形容词。
- 2：有边界描述，但缺少具体阈值或口径。
- 3：关键边界基本明确。
- 4：数值、时间、权限或状态边界明确。
- 5：边界完整，并覆盖异常和验收口径。

### H3 关键异常测试场景

- 0：没有异常测试场景。
- 1：只说“测试异常情况”。
- 2：有异常测试，但场景不具体。
- 3：覆盖主要业务异常。
- 4：覆盖业务、依赖、权限等关键异常。
- 5：异常场景完整，并对应验收标准或业务结果。

### I1 未决项和假设条件

- 0：没有未决项或假设说明，但文档明显存在待确认内容。
- 1：大量“待定、后续确认、视情况”。
- 2：有未决项，但没有 Owner 或时间。
- 3：关键未决项、假设和 Owner 基本明确。
- 4：未决项、假设、Owner、时间明确。
- 5：同时说明影响、决策机制和跟踪方式。

### I2 跨团队责任边界

- 0：没有责任边界。
- 1：只说“相关团队协同”。
- 2：有团队名称，但职责不清。
- 3：主要团队和职责基本明确。
- 4：团队、Owner、协同事项明确。
- 5：同时包含排期依赖、决策人和升级机制。

### I3 业务或技术约束

- 0：没有约束说明。
- 1：只说“后续根据情况选型”。
- 2：有约束，但硬性程度不清。
- 3：主要约束基本明确。
- 4：业务、技术或合规约束明确。
- 5：约束完整，并区分硬约束、软约束和影响。

### I4 版本边界与需求变更机制

- 0：没有版本或变更机制。
- 1：只说“持续优化、后续迭代”。
- 2：有版本描述，但边界不清。
- 3：本期目标和后续方向基本明确。
- 4：版本边界和变更流程明确。
- 5：同时包含影响评估、决策人和准入条件。

### J1 业务监控与告警诉求

- 0：没有监控或告警诉求。
- 1：只说“系统需要监控”。
- 2：有监控诉求，但指标或角色不清。
- 3：关键指标或告警场景基本明确。
- 4：指标、告警、通知对象明确。
- 5：同时包含阈值、等级、处理时限或升级机制。

### J2 人工干预和补救入口

- 0：没有人工闭环说明。
- 1：只说“人工处理”。
- 2：有人工处理场景，但角色或结果不清。
- 3：人工处理场景和角色基本明确。
- 4：场景、角色、处理结果、记录要求明确。
- 5：同时包含权限、复核、审计和异常关闭条件。

## PRD 与系统设计边界

| PRD 应提供 | 系统设计阶段展开 |
| --- | --- |
| 业务目标、成功标准、范围 | 架构复杂度、成本投入、技术选型 |
| 用户、角色、权限边界 | 账号体系、租户模型、RBAC/ABAC |
| 主流程、异常流程、状态流转 | 服务编排、事务边界、事件模型 |
| 业务规则、冲突处理、不可接受结果 | 规则引擎、幂等键、锁、消息顺序、对账 |
| 核心对象、识别口径 | 数据库模型、表结构、ID 生成 |
| 外部依赖、交互时机、失败业务期望、集成模式与实时性要求 | API、字段、错误码、鉴权、重试、熔断、服务编排、事务边界、中间件选型 |
| 验收标准、边界条件、异常测试场景 | 自动化测试、集成测试、故障演练 |
