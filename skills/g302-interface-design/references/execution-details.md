# G302 执行细化说明

## 1. 作用

本文件用于细化 `G302` 的执行方式，补齐 `SKILL.md` 中“如何真正落地到接口详细设计文档”的步骤约束。

## 2. 执行原则

1. `G302` 仅在 `complete` 模式执行，且必须以 `G300` 已冻结的范围和 `G301` 已明确的组件交接边界为基础。
2. 输出必须直接满足 `DD-07`、`GS-Quality-Check`、`GS-Review` 的最小消费字段，不得只保留概念性描述。
3. 子代理只负责起草文档；运行时任务状态、返工入口、共享门禁推进和子代理关闭均由 `G300` 在验收后统一执行。
4. 当接口边界、关键时序、错误语义分层、版本兼容或测试覆盖仅靠表格不够直观时，可在 Markdown 中补充 Mermaid 图；但图必须与结构化字段同名同义，不得替代表格契约。

## 3. 固定方法名

本 Skill 的方法检查与步骤描述统一使用以下标准名称：

1. `设计范围冻结`
2. `约束回链`
3. `契约驱动设计`
4. `契约一致性校验`
5. `接口数据边界对齐`
6. `兼容性策略设计`
7. `幂等与重试语义设计`
8. `时序交互建模`
9. `错误语义分层`
10. `失败模式分析`
11. `可测试性分层设计`
12. `可观测性设计`

方法来源：

- [detailed-design-methods-catalog.md](../../_shared/detailed-design-methods-catalog.md)

## 4. 输入消费顺序

1. 优先读取 `artifacts/detailed-design/001-design-plan.md`，确认 `final_mode=complete`、`skills_to_run`、澄清结论和范围冻结结果。
2. 再读取 `artifacts/detailed-design/002-component-design.md`，重点提取 `interface_handoff_contracts`、`component_catalog`、`state_transition_models`、`exception_handling_specs`、`component_design_risks`。
3. 继续读取 `artifacts/architecture/003-architecture-blueprint.md` 和 `artifacts/architecture/001-technical-strategy.md`，校准接口边界、交互约束、质量属性和技术限制。
4. 若需要补足设计依据，再读取 `artifacts/architecture/004-adr.md`、requirements 阶段主输出与 `G300` 澄清记录。

## 5. 步骤级要求

### 5.1 范围与接口清单

1. 必须显式写出 in-scope、out-of-scope 和 deferred 项。
2. 每个 `G301.interface_handoff_contracts` 中进入本轮定稿的 `handoff_id`，都必须在 `G302` 中找到承接项或显式写明延后原因。
3. 每个接口都要给出提供方、消费方、交互类型和所属边界。
4. 必须建立来源回链，说明接口设计来自哪一项 `handoff_id`、蓝图交互、技术策略约束或澄清结论。

### 5.2 契约与字段约束

1. 每个关键接口都必须形成请求/响应或消息契约，不得只给接口名。
2. 字段约束至少覆盖必填/可空、格式/类型、默认值或校验规则。
3. 必须显式标记关键字段的来源、消费者期望和兼容要求。
4. 若接口边界复杂，建议补充 Mermaid 边界关系图，帮助评审快速识别 `provider/consumer` 和交互方向。

### 5.3 时序与错误语义

1. 存在多跳调用、异步回调、超时重试或补偿的接口，必须给出时序记录；若当前接口交互简单，可显式写明 `N/A` 与原因。
2. 每个关键接口至少要定义 1 类错误语义；若当前接口无显式业务错误码，也要说明失败语义如何传达。
3. 错误语义必须说明调用方责任、可否重试、是否需要降级或补偿，不得只写“失败返回错误”。
4. 若时序复杂，建议补充 Mermaid `sequenceDiagram`；若错误分支复杂，建议补充 Mermaid 错误流程图。
5. 存在重试、回调重放或重复消费风险的接口，应在本步骤先冻结幂等与重试语义，再在后续版本/治理章节正式落表。

### 5.4 版本、治理与测试

1. 每个关键接口都必须说明版本策略和兼容范围；若当前接口暂不版本化，必须说明原因和后续触发条件。
2. 存在重试、回调、异步去重或重复消费风险的接口，必须显式写出幂等键或去重规则。
3. 可观测性与安全约束至少覆盖日志/指标/追踪、鉴权/脱敏和告警触发条件。
4. 可测试性设计必须至少覆盖契约测试、异常测试和兼容性或集成测试之一。
5. 若版本兼容路径复杂，建议补充 Mermaid 版本兼容路径图；若测试点较多，建议补充 Mermaid 测试覆盖图。
6. 版本策略应至少说明兼容窗口、弃用触发条件和灰度切换方式；幂等设计应至少说明幂等键、去重窗口和重试责任边界。

## 6. 与 DD-07、GS-Quality-Check、GS-Review 的衔接要求

进入后续汇总前，`G302` 输出至少要保证：

1. `interface_catalog` 可直接作为详细设计接口索引。
2. `interface_contract_specs` 可直接检查请求/响应/消息体和字段约束是否闭环。
3. `interaction_sequence_specs` 可直接支撑接口时序语义和超时/重试行为检查。
4. `error_semantic_specs` 可直接支撑失败语义、调用方责任和质量风险检查。
5. `version_idempotency_specs` 可直接支撑兼容性和重复调用风险检查。
6. `observability_security_specs` 可直接支撑日志、追踪、安全和审计检查。
7. `interface_testability_design` 可直接作为 `DD-07` 汇总时的测试可验证性证据。
8. `interface_design_risks` 可直接作为 `DD-07` 和后续评审汇总的风险输入。
9. 必须能证明 `interface_scope -> interface_catalog / interface_contract_specs -> interaction_sequence_specs / error_semantic_specs -> version_idempotency_specs / observability_security_specs / interface_testability_design / interface_design_risks` 的追溯链完整。

## 7. 质量与恢复要求

1. 若主文档缺少“供 DD-07、GS-Quality-Check 与 GS-Review 消费的最小字段”章节，当前轮视为不通过。
2. 中断恢复时仅以 `artifacts/detailed-design/000-task-tracker.md` 为主锚点，`template.md` 作为辅助证据。
3. 若质量门或评审门未通过，由 `G300` 统一回写：`DD-05` 保持 `status_code=in_progress`、`skill_stage=rework`，并在 `resume_from` 中写明首个返工任务位和待处理问题。
4. 第 `6` 章回链必须以 `source_table + 稳定 ID` 为正式主定位键，`source_anchor` 与章节号仅作为人读辅助定位字符串。
5. `G302` 本地验收仅覆盖文档完整性、结构化最小字段和追溯关系；第 `8` 章质量检查区仅作为 `G300/DD-07` 预组装共享质量门时的占位信息，不并入 `G302` 自身验收结论。
6. 若 `interface_scope`、`interface_catalog`、`interface_contract_specs`、`interaction_sequence_specs`、`error_semantic_specs`、`version_idempotency_specs`、`observability_security_specs`、`interface_testability_design` 或 `interface_design_risks` 任一缺失，当前轮视为不通过。
