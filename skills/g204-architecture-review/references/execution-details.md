# G204 执行细化说明

## 1. 作用

本文件用于细化 `G204` 的执行方式，补齐 `SKILL.md` 中“如何真正落地到架构评审验证文档”的步骤约束。

方法来源说明：

1. 本文件中涉及的方法名，应以 `../_shared/architecture-methods-catalog.md` 为唯一标准引用来源。

## 2. 执行原则

1. `G204` 的目标是验证当前 architecture 文档包是否闭环，不重做 `G203` 蓝图设计。
2. 每项评审结论都必须绑定来源文档、证据或缺口说明。
3. 输出必须满足 `GS-Quality-Check` 所需文档级字段的预组装要求，不得只给自由文本总结。
4. 子代理只负责起草文档；运行时任务状态、返工入口、`review_result` 和 `resume_from` 由 `G200` 在验收后统一回写。

## 3. 输入消费顺序

1. 优先读取 `artifacts/architecture/003-architecture-blueprint.md`。
2. 再读取 `artifacts/architecture/004-adr.md`。
3. 再读取 `artifacts/architecture/001-technical-strategy.md` 与 `artifacts/architecture/002-architecture-vision.md`。
4. 如需补足范围和边界，再读取 `artifacts/architecture/001-architecture-intake.md` 与 requirements 阶段交接摘要。

## 4. 步骤级要求

### 4.1 评审范围与文档包

1. 必须覆盖 architecture 阶段正式文档包。
2. `target_documents` 至少包含 `001/002/003/004/005` 五份正式文档。
3. 任一必选文档缺失时，当前轮不得进入 `GS-Quality-Check`。

### 4.2 一致性验证

1. 必须至少输出 3 条一致性验证结论。
2. 必须覆盖愿景承接、策略承接和 ADR 对齐三类验证点。
3. 每条验证都要明确结论、缺口和处理建议。
4. 必须显式消费 `G203` 的 `blueprint_scope / architecture_views / coverage_declaration / component_inventory / data_architecture / interface_architecture / interaction_flows / deployment_topology / adr_index / blueprint_risks / adr_contract`，并将其转成可审计的评审对象。
5. 必须执行蓝图追溯映射，确认 `G202 -> G201 -> G203` 的关键约束和结论已建立回链。

### 4.3 质量与风险验证

1. 必须至少覆盖 3 个关键质量属性。
2. 必须至少覆盖 2 个主要风险或权衡主题。
3. 若蓝图无法证明对关键质量属性的承接，应明确标记为 `rework` 或 `blocked`。
4. 必须执行一次视图一致性检查，确认结构、交互、部署视图及 ADR 在评审口径下保持一致。

### 4.4 评审结论与返工动作

1. `review_findings` 至少 3 条；若确无问题，也必须显式说明。
2. `quality_gate_readiness` 必须逐项说明是否具备进入 `GS-Quality-Check` 的条件。
3. `rework_actions` 必须落到具体文档和明确完成判据。

## 5. 与 GS-Quality-Check 的衔接要求

进入 `GS-Quality-Check` 前，`G204` 输出至少要保证：

1. `target_documents` 可直接转成 `GS-Quality-Check.target_documents`。
2. `g203_review_targets` 必须完整覆盖 `G203` 的结构化最小消费字段，并明确每类对象的评审焦点和检查状态；其中 `coverage_declaration / data_architecture / interface_architecture` 不得缺失。
3. `review_findings` 可作为质量门问题和后续评审问题的上游证据。
4. `quality_gate_readiness` 能明确说明当前轮是否允许推进到 `AD-07`。
5. `rework_actions` 能为质量门失败或评审失败后的返工提供直接动作来源。
6. `stage`、`quality_task_id`、`tracker_path` 以及共享服务运行时上下文由 `G200` 在触发 `AD-07` 时补齐，`G204` 不负责这些字段，也不维护 `GS-Quality-Check` 的正式结果字段。

## 6. 质量与恢复要求

1. 若主文档缺少“供 GS-Quality-Check 预组装的部分输入字段”章节，当前轮视为不通过。
2. 中断恢复时仅以 `artifacts/architecture/000-task-tracker.md` 为主锚点，`template.md` 作为辅助证据。
3. 若质量门或评审门未通过，由 `G200` 统一回写：`AD-06` 保持 `status_code=in_progress`、`skill_stage=rework`，并在 `resume_from` 中写明首个返工任务位和待处理问题。
