# G301 执行细化说明

## 1. 作用

本文件用于细化 `G301` 的执行方式，补齐 `SKILL.md` 中“如何真正落地到组件详细设计文档”的步骤约束。

## 2. 执行原则

1. `G301` 必须以 `G300` 已冻结的范围和 `G203` 蓝图为边界，不得自行扩大到接口字段定稿或数据库物理设计。
2. 输出必须同时覆盖职责、内部结构、状态转换、关键算法/规则、异常处理、可测试性和交接边界，不得只写组件列表。
3. 输出必须直接满足 `G302/G303/DD-07` 的最小消费字段，不得只保留概念性描述；其中 `G302/G303` 当前按预留稳定契约消费，不应表述为已完成实证闭环。
4. 子代理只负责起草文档；运行时任务状态、返工入口、共享门禁推进和子代理关闭均由 `G300` 在验收后统一执行。
5. 当组件关系、交互流程、协作链路、状态迁移、内部结构分层、异常处理闭环、测试覆盖或追溯链仅靠表格不够直观时，可在 Markdown 中补充 Mermaid 图；但图必须与结构化字段同名同义，不得替代表格契约。

## 3. 固定方法名

本 Skill 的方法检查与步骤描述统一使用以下标准名称：

1. `设计范围冻结`
2. `约束回链`
3. `职责-协作映射`
4. `风险热点预判`
5. `内部结构分解`
6. `契约驱动设计`
7. `依赖反转校验`
8. `时序建模`
9. `状态机建模`
10. `规则决策表`
11. `前置/后置条件建模`
12. `并发与一致性分析`
13. `失败模式分析`
14. `可测试性分层设计`
15. `接口数据边界对齐`
16. `可观测性设计`

方法来源：

- [detailed-design-methods-catalog.md](../../_shared/detailed-design-methods-catalog.md)

## 4. 输入消费顺序

1. 优先读取 `artifacts/detailed-design/001-design-plan.md`，确认 `final_mode`、澄清结论、执行清单和范围冻结结果。
2. 再读取 `artifacts/architecture/003-architecture-blueprint.md`，提取蓝图组件、依赖与上游边界。
3. 继续读取 `artifacts/architecture/001-technical-strategy.md` 和 `artifacts/architecture/002-architecture-vision.md`，校准设计约束和质量属性。
4. 若需要补足设计依据，再读取 `artifacts/architecture/004-adr.md`、requirements 阶段主输出与 `G300` 澄清记录。

## 5. 步骤级要求

### 5.1 范围与组件清单

1. 必须显式写出 in-scope、out-of-scope 和 deferred 项。
2. 必须至少给出 3 个核心组件或明确说明为何少于 3 个。
3. 每个组件都要给出设计目标、职责和所属边界。
4. 必须建立来源回链，说明组件设计来自哪一项蓝图元素、策略约束或澄清结论。

### 5.2 职责与内部结构

1. 每个核心组件都必须形成职责分配与协作关系，不得只给单组件孤立描述。
2. 每个核心组件都必须至少给出 1 个内部模块/层或明确说明其为单体职责单元。
3. 必须显式标记关键依赖、调用方向和耦合约束。
4. 若某组件需要由 `G302` 或 `G303` 继续展开，必须在当前轮先冻结交接边界。
5. 若组件协作关系复杂，建议补充 Mermaid 组件关系图或时序图，帮助下游快速识别责任边界与交互方向。
6. 若组件内部层次或扩展点较复杂，建议补充 Mermaid 分层图，帮助评审快速识别模块组织和依赖方向。

### 5.3 状态与算法/规则

1. 存在状态变化的组件必须给出状态对象、状态说明、持久化方式、回滚/恢复要求、触发条件、迁移规则和失败行为；若当前组件不涉及状态变化，必须显式写明 `N/A` 与原因。
2. 存在决策逻辑或复杂处理路径的组件必须给出关键算法或规则条目；若当前组件无复杂规则，必须显式写明 `N/A` 与原因。
3. 算法/规则必须说明输入、输出、关键步骤或决策点，不得只写“按业务规则处理”。
4. `state_transition_models` 在第 7 章必须拆成 `state_models` 与 `state_transitions` 两张子表，分别以 `state_model_id` 和 `transition_id` 为主键。
5. 若状态模型与算法规则存在耦合，必须在字段中建立回指关系。
6. 若状态迁移较复杂，建议补充 Mermaid `stateDiagram-v2` 或 `flowchart`，但图中状态名与迁移语义必须与结构化字段保持一致。

### 5.4 异常、测试与交接边界

1. 每个核心组件至少要识别 1 类异常场景，若确无异常分支需显式说明。
2. 异常处理必须覆盖检测点和处理策略，必要时补充重试、补偿或降级。
3. 可测试性设计必须至少覆盖核心成功路径、关键异常路径和一项边界条件。
4. `interface_handoff_contracts` 必须说明 `provider_component_id`、`consumer_component_id`、`boundary_responsibility`、`consumption_semantics`、调用语义、幂等/版本要求和错误语义边界。
5. `data_handoff_contracts` 必须说明 `owner_component_id`、`consumer_component_id`、`boundary_responsibility`、`consumption_semantics`、读写边界、一致性和生命周期要求。
6. 必须显式产出 `component_design_risks`，并为每条 `risk_id` 绑定目标对象、影响范围、缓解/验证方式，以及至少一个正文稳定来源 ID（如 `TRS-*`、`IFC-H*`、`DAT-H*`、`EXC-*`）。
7. 若使用 Mermaid 图说明异常、补偿或交接流程，图中节点和交互必须能回链到 `EXC-*`、`IFC-H*`、`DAT-H*` 等稳定 ID 对应的结构化对象。
8. 若测试点较多或追溯链较长，建议分别补充 Mermaid 测试覆盖图和追溯关系图，但图中节点必须优先使用 `TST-*`、`CMP-*`、`TRS-*`、`IFC-H*`、`DAT-H*` 等稳定 ID。

## 6. 与 G302、G303、DD-07 的衔接要求

进入后续汇总前，`G301` 输出至少要保证：

1. `component_catalog` 可直接作为详细设计组件索引。
2. `responsibility_matrix` 可直接检查职责归属、协作方和输入输出是否闭环。
3. `internal_structure_specs` 可直接支撑接口设计与数据设计的责任定位。
4. `state_transition_models` 可直接支撑接口状态语义、数据状态落库或评审检查。
5. `algorithm_rule_specs` 可直接支撑关键规则审查和测试点提取。
6. `exception_handling_specs` 可直接支撑错误语义、恢复策略和质量风险检查。
7. `interface_handoff_contracts` 为 `G302` 后续消费预留稳定契约和最小字段，供其继续细化接口契约。
8. `data_handoff_contracts` 为 `G303` 后续消费预留稳定契约和最小字段，供其继续细化数据结构与存储设计。
9. `testability_design` 可直接作为 `DD-07 design-review-validation` 汇总时的测试可验证性证据。
10. `component_design_risks` 可直接作为 `DD-07 design-review-validation` 和后续评审汇总的风险输入。
11. 必须能证明 `component_scope -> component_catalog / responsibility_matrix -> internal_structure_specs / component_dependencies -> state_transition_models / algorithm_rule_specs / exception_handling_specs -> interface_handoff_contracts / data_handoff_contracts / testability_design / component_design_risks` 的追溯链完整。

## 7. 质量与恢复要求

1. 若主文档缺少“供 G302、G303 与 DD-07 消费的最小字段”章节，当前轮视为不通过。
2. 中断恢复时仅以 `artifacts/detailed-design/000-task-tracker.md` 为主锚点，`template.md` 作为辅助证据。
3. 若质量门或评审门未通过，由 `G300` 统一回写：`DD-04` 保持 `status_code=in_progress`、`skill_stage=rework`，并在 `resume_from` 中写明首个返工任务位和待处理问题。
4. 第 7 章回链必须以 `source_table + 稳定 ID` 为正式主定位键，`source_anchor` 与章节号仅作为人读辅助定位字符串。
5. `G301` 本地验收仅覆盖文档完整性、结构化最小字段和追溯关系；第 9 章质量检查区仅作为 `G300/DD-07` 预组装共享质量门时的占位信息，不并入 `G301` 自身验收结论。
6. 若 `component_scope`、`component_catalog`、`responsibility_matrix`、`internal_structure_specs`、`component_dependencies`、`state_transition_models`、`algorithm_rule_specs`、`exception_handling_specs`、`interface_handoff_contracts`、`data_handoff_contracts`、`testability_design` 或 `component_design_risks` 任一缺失，当前轮视为不通过。
