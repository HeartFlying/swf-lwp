# G303 执行细化说明

## 1. 作用

本文件用于细化 `G303` 的执行方式，补齐 `SKILL.md` 中“如何真正落地到数据详细设计文档”的步骤约束。

## 2. 执行原则

1. `G303` 仅在 `complete` 模式执行，且必须以 `G300` 已冻结的范围和 `G301` 已明确的组件交接边界为基础。
2. 输出必须直接满足 `DD-07`、`GS-Quality-Check`、`GS-Review` 的最小消费字段，不得只保留概念性描述。
3. 子代理只负责起草文档；运行时任务状态、返工入口、共享门禁推进和子代理关闭均由 `G300` 在验收后统一执行。
4. 数据详细设计必须覆盖对象、所有权、存储边界、一致性、演化、迁移、异常与测试，不得退化成单纯的物理库表设计。
5. 当数据关系、边界、状态、迁移或异常恢复仅靠表格不够直观时，可在 Markdown 中补充 Mermaid 图；但图必须与结构化字段同名同义，不得替代表格契约。
6. 结构化最小字段必须可直接回链到 `G301.data_handoff_contracts` 的 `data_contract_id/source_table/source_anchor`，且 `6.5 ~ 6.11` 必须额外写入 `source_data_contract_id/source_table/source_anchor`，不得只依赖自由文本或间接回链。

## 3. 固定方法名

本 Skill 的方法检查与步骤描述统一使用以下标准名称：

1. `设计范围冻结`
2. `约束回链`
3. `数据对象建模`
4. `读写边界分析`
5. `契约驱动设计`
6. `接口数据边界对齐`
7. `一致性与演化设计`
8. `数据保留与归档策略设计`
9. `并发与一致性分析`
10. `前置/后置条件建模`
11. `失败模式分析`
12. `迁移切换策略设计`
13. `可测试性分层设计`
14. `可观测性设计`
15. `风险热点预判`

方法来源：

- [detailed-design-methods-catalog.md](../../_shared/detailed-design-methods-catalog.md)

## 4. 输入消费顺序

1. 优先读取 `artifacts/detailed-design/001-design-plan.md`，确认 `final_mode=complete`、`skills_to_run`、澄清结论和范围冻结结果。
2. 再读取 `artifacts/detailed-design/002-component-design.md`，重点提取 `data_handoff_contracts`、`component_catalog`、`responsibility_matrix`、`state_transition_models`、`exception_handling_specs`、`component_design_risks`。
3. 若已存在，读取 `artifacts/detailed-design/003-interface-design.md` 作为数据消费语义的补充约束，但不得把接口设计替代数据设计。
4. 继续读取 `artifacts/architecture/003-architecture-blueprint.md` 和 `artifacts/architecture/001-technical-strategy.md`，校准数据边界、质量属性和技术限制。
5. 若需要补足设计依据，再读取 `artifacts/architecture/004-adr.md`、requirements 阶段主输出与 `G300` 澄清记录。

## 5. 步骤级要求

### 5.1 范围与数据对象清单

1. 必须显式写出 in-scope、out-of-scope 和 deferred 项。
2. 必须至少给出 1 组核心数据对象和 1 组边界说明；若对象少于 3 个，必须写入模板中的 `object_count_note_id` 槽位，并显式解释原因与边界收敛方式。
3. 每个对象都要给出设计目标、职责和所属边界。
4. 必须建立来源回链，说明数据设计来自哪一项蓝图元素、`G301.data_handoff_contracts`、技术策略约束或澄清结论；回链字段至少包含 `source_data_contract_id/source_table/source_anchor`。

### 5.2 所有权与存储边界

1. 每个核心对象都必须形成所有权与读写边界，不得只给对象列表。
2. 每个核心对象都必须至少给出 1 个存储边界或明确说明其为逻辑对象且不单独落存。
3. 存储边界必须显式拆分 `落库/落存位置` 与 `访问层次`，不得合并为单列自由文本。
4. 必须显式标记写入责任、读取视图、边界责任和消费语义。
5. 若对象需要由 `G301` 继续展开，必须在当前轮先冻结交接边界。
6. 若对象关系复杂，建议补充 Mermaid 数据关系图或读写流向图，帮助下游快速识别所有权与流向。

### 5.3 生命周期、一致性与迁移

1. 存在状态变化的数据对象必须给出状态对象、状态说明、持久化方式、回滚/恢复要求、触发条件、迁移规则和失败行为；若当前对象不涉及状态变化，必须显式写明 `N/A` 与原因。
2. 若对象存在生命周期治理要求，`3.2` 与 `6.5.1` 必须显式给出保留、归档和删除策略，不能只写“按平台默认处理”。
3. 数据一致性必须说明一致性级别、可见性、顺序性和冲突处理，不得只写“最终一致”而不解释边界。
4. 生命周期治理应显式使用 `数据保留与归档策略设计`，把保留周期、归档触发、删除条件、恢复窗口和审计要求收敛成可执行规则。
5. 版本演化必须说明兼容窗口、字段变更、切换条件和消费方影响；如存在弃用窗口，也必须并入切换条件统一说明。
6. 迁移设计应显式使用 `迁移切换策略设计`，说明双写/双读、回填、校验点、切换门槛、切换条件和回滚条件。
7. 若迁移路径较复杂，建议补充 Mermaid 状态图、版本路径图或迁移流程图，但图中状态名与迁移语义必须与结构化字段保持一致。

### 5.4 异常、测试与风险

1. 每个核心对象至少要识别 1 类异常场景，若确无异常分支需显式说明。
2. 异常处理必须覆盖检测点和处理策略，必要时补充重试、补偿、降级或人工介入。
3. 可测试性设计必须至少覆盖核心成功路径、关键迁移路径和一项边界条件；若有交接契约风险，还必须显式覆盖 `handoff_contract` / `boundary` 级测试点。
4. `data_design_risks` 必须说明风险对象、影响范围、回指的状态/迁移/迁移任务和验证方式；`target_type` 允许直接使用 `ownership_boundary`、`data_handoff`、`boundary` 等上游交接/边界风险类型。
5. 若使用 Mermaid 图说明异常、迁移或回滚流程，图中节点和动作必须能回链到 `EXC-*`、`MIG-*`、`TRS-*`、`DAT-H*` 等稳定 ID 对应的结构化对象。

## 6. 与 G300、G301、DD-07 的衔接要求

进入后续汇总前，`G303` 输出至少要保证：

1. `data_object_catalog` 可直接作为数据设计对象索引。
2. `ownership_and_boundary_matrix` 可直接检查数据归属、读写责任和消费语义是否闭环。
3. `storage_boundary_specs` 可直接支撑存储位置、访问层次和扩展点定位。
4. `data_lifecycle_specs` 可直接支撑状态、归档、删除和恢复语义。
5. `consistency_semantics_specs` 可直接支撑一致性和并发审查。
6. `evolution_compatibility_specs` 可直接支撑兼容性和字段演化检查。
7. `migration_risk_specs` 可直接支撑迁移、回填、切换与回滚风险检查。
8. `data_exception_handling_specs` 可直接支撑错误语义、恢复策略和质量风险检查。
9. `data_testability_design` 可直接作为 `DD-07 design-review-validation` 汇总时的测试可验证性证据，并覆盖 `handoff_contract` / `boundary` 级测试点。
10. `data_design_risks` 可直接作为 `DD-07 design-review-validation` 和后续评审汇总的风险输入，并允许以 `ownership_boundary` / `data_handoff` / `boundary` 直接表达风险对象。
11. `data_lifecycle_specs`、`consistency_semantics_specs`、`evolution_compatibility_specs`、`migration_risk_specs`、`data_exception_handling_specs`、`data_testability_design`、`data_design_risks` 在第 `6` 章都必须显式携带 `source_data_contract_id/source_table/source_anchor`，不得仅依赖 `data_object_id` 间接回链。
12. 必须能证明 `data_scope -> data_object_catalog / ownership_and_boundary_matrix -> storage_boundary_specs / data_lifecycle_specs -> consistency_semantics_specs / evolution_compatibility_specs / migration_risk_specs -> data_exception_handling_specs / data_testability_design / data_design_risks` 的追溯链完整。

## 7. 质量与恢复要求

1. 若主文档缺少“供 G300、G301、DD-07、GS-Quality-Check 与 GS-Review 消费的最小字段”章节，当前轮视为不通过。
2. 中断恢复时仅以 `artifacts/detailed-design/000-task-tracker.md` 为主锚点，`template.md` 作为辅助证据。
3. 若质量门或评审门未通过，由 `G300` 统一回写：`DD-06` 保持 `status_code=in_progress`、`skill_stage=rework`，并在 `resume_from` 中写明首个返工任务位和待处理问题。
4. 第 `6` 章回链必须以 `source_table + 稳定 ID` 为正式主定位键，`source_anchor` 与章节号仅作为人读辅助定位字符串。
5. `G303` 本地验收仅覆盖文档完整性、结构化最小字段和追溯关系；第 `8` 章质量检查区仅作为 `G300/DD-07` 预组装共享质量门时的占位信息，不并入 `G303` 自身验收结论，且其 `quality_check_summary.scores` 口径需与共享质量门一致，采用 `completeness`、`markdown_format`、`traceability`。
6. 若 `data_scope`、`data_object_catalog`、`ownership_and_boundary_matrix`、`storage_boundary_specs`、`data_lifecycle_specs`、`consistency_semantics_specs`、`evolution_compatibility_specs`、`migration_risk_specs`、`data_exception_handling_specs`、`data_testability_design` 或 `data_design_risks` 任一缺失，当前轮视为不通过。
