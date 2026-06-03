---
name: g203-architecture-blueprint
description: 架构蓝图定义，用于基于 G201 的技术策略形成可交付的系统蓝图、关键视图和 ADR 集，并产出可供 G204 消费的结构化输入。
version: 0.1.0
---

# G203 架构蓝图定义 SKILL

## 元信息与执行契约

说明：完整机读契约以文档头部 YAML 为准；本章节仅提供执行摘要。

### 基本信息

| 项目 | 内容 |
|---|---|
| skill_id | `G203` |
| skill_type | `core` |
| 中文名称 | 架构蓝图定义 |
| 适用阶段 | `architecture` |
| 执行模式 | `fast`、`standard`、`complete` |
| 前置依赖 | `AD-04`（`G201` 已完成） |
| 后置依赖 | `G204` |
| 输出主文档 | `artifacts/architecture/003-architecture-blueprint.md`、`artifacts/architecture/004-adr.md` |

### 执行契约摘要

| 项目 | 内容 |
|---|---|
| 运行时任务映射 | `task_id=AD-05`，`skill_id=G203` |
| Skill 生命周期 | 主起草任务为 `AD-05`；质量检查与用户评审分别承接到共享服务任务 `AD-07(GS-Quality-Check)`、`AD-08(GS-Review)`；`skill_id` 维持各任务原定义，不重写为 `G203` |
| 运行时台账路径 | `artifacts/architecture/000-task-tracker.md` |
| 证据路径 | `evidence/AD-05/` |
| 必选输入 | `artifacts/architecture/001-technical-strategy.md`、`artifacts/architecture/002-architecture-vision.md` |
| 按需输入 | `artifacts/architecture/001-architecture-intake.md`、requirements 阶段主输出、上游评审结论 |
| 模板与参考 | `template.md`、`references/execution-details.md`、`references/role-definition.md`、`../_shared/architecture-methods-catalog.md` |
| 质量门摘要 | `overall_status` 仅允许 `pass/pass_with_warning`，且不得有 `critical/major` 问题 |

## 1. 目标

在已冻结的架构愿景与技术策略基础上，形成可执行的架构蓝图，明确：

1. 系统结构主线、关键视图和职责边界
2. 组件、数据、接口和部署关系
3. 需要正式固化的 ADR 集
4. 供 `G204` 消费的蓝图验证输入

## 2. 角色定义

`G203` 的角色边界、职责和输出风格见：

- [role-definition.md](references/role-definition.md)

`G203` 的实际执行记录与步骤细化统一使用以下本地文件：

- [template.md](template.md)
- [execution-details.md](references/execution-details.md)

执行要求：

1. `template.md`用于记录本轮输出细则。
2. `execution-details.md` 用于补足各步骤的推进条件、结束条件与回写要求。

## 3. 前置条件

1. `AD-04` 已完成，并已产出 `artifacts/architecture/001-technical-strategy.md`。
2. `artifacts/architecture/002-architecture-vision.md` 已存在且可读取。
3. `G201` 最小消费字段可完整读取。
4. 当前任务映射固定为：`AD-05` 为起草任务；质量门和评审门由 `AD-07/AD-08` 统一承接。

## 4. 输入输出契约

### 4.1 输入

1. `artifacts/architecture/001-technical-strategy.md`（必选）
2. `artifacts/architecture/002-architecture-vision.md`（必选）
3. `artifacts/architecture/001-architecture-intake.md`（按需）
4. `artifacts/requirements/003-requirements-baseline.md`（按需）
5. `artifacts/requirements/004-mvp-definition.md`（**必选**）
6. `artifacts/reviews/001-requirements-review.md`（按需）

### 4.2 输出

1. 主输出：`artifacts/architecture/003-architecture-blueprint.md`
2. 蓝图主文档必须包含的视图类型：context（上下文视图）、structure（结构视图）、interaction（交互视图）、deployment（部署视图）。当 G201 包含异常验收标准或异常处理相关决策时，还必须包含 exception（异常处理架构视图）。
3. 蓝图主文档除结构化表格外，应针对每类视图生成对应的 Mermaid 可视化图表，形成"表格+图表"双轨表达：
   - context 视图 → 系统上下文图（System Context Diagram）
   - structure 视图 → 组件结构图/分层图（Component Structure Diagram）
   - interaction 视图 → 关键交互时序图/流程图（Sequence/Flow Diagram）
   - deployment 视图 → 部署拓扑图（Deployment Topology Diagram）
   - exception 视图 → 异常状态转换图/降级链路图（State Machine Diagram）
   图表必须使用 Mermaid 语法嵌入 Markdown，确保可被标准渲染器直接渲染。图表中的标识符必须与正文表格严格一致。
4. ADR 输出：`artifacts/architecture/004-adr.md`
5. 证据目录：`evidence/AD-05/`

### 4.3 质量约束

1. 输出必须使用 Markdown。
2. 文档规模 `< 10000` 行；超限必须拆分且每个文件自包含。
3. 路径统一使用 `/`。
4. 蓝图结论必须同时能追溯到 `G201` 的技术策略与 `G202` 的愿景约束；缺少 `002-architecture-vision.md` 时不得启动当前 Skill。
5. 必须显式给出 `S5-A02/S5-A03/S5-A04/S5-A05` 的覆盖声明，且覆盖声明、正文章节与第 7 章最小字段之间不得互相矛盾。当 G201 包含异常验收标准时，还应体现对异常处理架构的覆盖。

## 5. 执行步骤

执行说明：

1. `G203` 由 architecture 阶段入口编排 SKILL `G200` 触发，并必须在独立子代理中执行。
2. 子代理仅负责本 Skill 文档产出；任务状态验收、台账回写和关闭动作均由 `G200` 统一执行。

### 步骤 1：建立蓝图主线与视图边界

- 操作主体：`G203-SKILL`
- 具体任务：
  - 提炼蓝图目标、范围边界和需要覆盖的视图集合
  - 建立系统上下文、结构、交互、部署视图的主线关系
  - 形成 `S5-A02/S5-A03/S5-A04/S5-A05` 到蓝图视图与结构化字段的覆盖声明
  - 明确哪些内容进入蓝图，哪些保留到详细设计阶段
  - **约束全覆盖检查**：读取 G201 全部 `constraint_id`（CST-* / IC-* / CST-EXCEPT-*），逐条确认在蓝图中存在显式承接点（范围边界 SCP-*、组件 CMP-*、数据对象 DAT-*、接口 IFC-*、部署拓扑 TOP-* 或 ADR-*）。对 `mandatory=yes` 的约束不得遗漏。若某约束因范围原因不进入蓝图，必须在范围边界中显式说明并标注 `deferred` 或 `out_of_scope`。
  - **建立 SCP-MVP 映射**：读取 `004-mvp-definition.md` 的 in-scope MVP 列表，与蓝图 1.2 节的 SCP 列表建立显式映射。若 SCP 数量与 MVP 数量不一致，必须说明收敛规则（扩展 SCP 项或合并 MVP 项），确保映射可追溯到下游阶段。映射关系必须写入蓝图 3.1 节。
  - **生成系统上下文图**：使用 Mermaid 生成系统上下文图（VW-001），标注 系统边界、外部系统及数据流向。图中节点必须使用与正文一致的 scope_id 或 component_id。
- 方法论（架构视角）：
  - 必用：`蓝图范围切片`
  - 必用：`架构视图映射`
  - 必用：`约束落图`
  - 可选：`蓝图追溯映射`
- 输入：`001-technical-strategy.md`
- 输出：蓝图主线与视图边界结论（写入主文档），含约束覆盖检查表（template.md 9.2 节）
- 依赖关系：无

### 步骤 2：定义组件、数据与接口结构

- 操作主体：`G203-SKILL`
- 具体任务：
  - 定义核心组件、职责分配和边界归属
  - 定义核心数据对象、权威存储边界、数据流转、一致性/主从边界和生命周期要求
  - 形成关键交互链路、接口边界、调用方式、契约约束、异常语义和集成模式
  - 对组件依赖和集成约束做显式说明
  - **预留/扩展决策显式承接**：对 G201 中标记为"预留"或"预留扩展"的技术选型（如 PostGIS、FAISS 索引、GIS 扩展），必须在数据对象定义（DAT-*）或组件核心职责（CMP-*）中显式预留扩展字段、接口或配置锚点，不能仅在 ADR 中说明。
  - **物理/环境约束向算法/数据追溯**：对 G201 中涉及物理部署参数、硬件规格、环境约束的条目（如摄像头间距、画面重叠区、NPU 型号、算力上限），必须在算法组件职责（CMP-*）或配置类数据对象（DAT-*）中显式体现，建立从物理约束→算法参数→数据配置的完整追溯链。
  - **建立 MVP→组件覆盖映射**：为每个 in-scope MVP 指定其对应的组件覆盖（CMP-XXX 列表），并写入蓝图 3.1 节。所有 MVP 必须有非空组件覆盖。
  - **前端组件一致性**：对 `004-mvp-definition.md` 中标记为 `has_frontend_ui=yes` 的 MVP，其组件覆盖中必须至少包含一个 `frontend_consumer=yes` 的组件；若 `004-mvp-definition.md` 无此字段，则依据功能描述自行推断并标记。
  - **生成组件结构图**：使用 Mermaid 生成组件分层图（VW-002），区分边缘侧/中心侧/基础设施/外部系统四层，层间连线标注接口 ID（IFC-XXX）。
  - **生成数据流全景图**：使用 Mermaid 生成数据流图，覆盖全部核心数据对象，箭头标注 data_flow_id。
  - **生成关键交互时序图**：为所有核心链路生成 Mermaid 时序图，时序图中必须体现异常路径的触发条件。
- 方法论（架构视角）：
  - 必用：`组件职责分解`
  - 必用：`接口与依赖建模`
  - 必用：`关键链路走查`
  - 可选：`视图一致性检查`
- 输入：步骤 1 输出
- 输出：组件、数据与接口结论（写入主文档）
- 依赖关系：依赖步骤 1 完成

### 步骤 3：定义部署拓扑与运行边界

- 操作主体：`G203-SKILL`
- 具体任务：
  - 形成运行节点、部署单元和环境边界
  - 明确高可用、伸缩、隔离和安全边界。安全边界必须包括：1）安全域划分（management / business / video / edge）；2）传输加密要求（TLS 1.2+ / mTLS）在各接口上的映射；3）等保二级控制点（访问控制、安全审计、数据完整性、数据保密性、入侵防范）在各部署单元上的分配。
  - 标记部署约束对蓝图结构的影响
  - **生成部署拓扑图**：使用 Mermaid 生成部署拓扑图（VW-004），标注 6 个拓扑节点（TOP-001~006）及其所属 security_zone，节点间通信链路标注对应的 security_protocol（TLS 1.2+ / mTLS / none）。
- 方法论（架构视角）：
  - 必用：`部署拓扑建模`
  - 必用：`约束落图`
  - 必用：`视图一致性检查`
  - 可选：`关键链路走查`
- 输入：步骤 1-2 输出
- 输出：部署拓扑结论（写入主文档）
- 依赖关系：依赖步骤 1-2 完成

### 步骤 4：固化 ADR 与评审关注点

- 操作主体：`G203-SKILL`
- 具体任务：
  - 将需要正式固化的关键决策沉淀为 ADR 条目
  - 建立 ADR 与视图、组件、约束之间的关联
  - **ADR 状态机图要求**：涉及状态转换的 ADR（如应急状态机）必须在 ADR 文档中附带 Mermaid 状态图。复杂 ADR（如跨主机传递协议）可附架构示意图。
  - 输出供 `G204` 使用的评审关注点和蓝图风险
- 方法论（架构视角）：
  - 必用：`ADR 固化`
  - 必用：`蓝图追溯映射`
  - 必用：`视图一致性检查`
  - 可选：`风险热点复核`
- 输入：步骤 1-3 输出
- 输出：ADR 与评审关注点结论（写入主文档）
- 依赖关系：依赖步骤 1-3 完成

### 步骤 5：生成架构蓝图与 ADR 文档

- 操作主体：`G203-SKILL`
- 具体任务：
  - 按模板整合章节并完成结构自检
  - 校验最小消费字段、路径格式和编号一致性
  - **校验图表与表格一致性**：图表中出现的所有 CMP-*/DAT-*/IFC-*/TOP-*/FLW-* 标识符必须在正文对应表格中有定义；图表中的连线关系必须与接口清单或依赖清单一致；所有 Mermaid 代码块语法正确，可被标准 Markdown 渲染器渲染。
  - 持久化到目标路径
- 输入：步骤 1-4 输出
- 输出：`artifacts/architecture/003-architecture-blueprint.md`、`artifacts/architecture/004-adr.md`
- 依赖关系：依赖步骤 1-4 完成

## 6. 与运行时台账对齐

推荐任务映射：

- `task_id`: `AD-05`
- `skill_id`: `G203`
- 生命周期口径：`AD-05` 负责 `drafting` 与返工后的再次起草；`AD-07` 负责 `quality_check`；`AD-08` 负责 `user_review`
- 返工回路：`AD-07/AD-08 -> AD-05(rework) -> drafting`

执行要求：

1. `AD-05` 只负责当前 Skill 的起草与返工后的再次起草。
2. `status_code/status_label/skill_stage/review_result/resume_from/evidence_path/updated_at` 的正式回写由 `G200` 在子代理验收后统一执行。
3. `AD-05` 起草完成后保持 `in_progress`，由 `G200` 推进到 `AD-07/AD-08`。
4. 质量检查结果写入质量报告字段，不写入 `review_result`。

## 7. 验收标准

### 7.1 执行检查闭环（强制）

为避免质量门数据来源后置，`G203` 在本 SKILL 内固定以下检查闭环：

| 项目 | 固定定义 |
|---|---|
| 质量检查工具 | `GS-Quality-Check` |
| 触发任务 | `AD-07` |
| 质量报告路径 | `artifacts/reviews/architecture-quality-check.md` |

1. 主文档存在且路径正确：`artifacts/architecture/003-architecture-blueprint.md`、`artifacts/architecture/004-adr.md`。
2. 文档章节必须与 `template.md` 对齐，至少包含：`1. 蓝图目标与范围`、`2. 架构视图`（含 `2.3 视图覆盖声明`）、`3. 组件与职责`（含 **3.1 MVP In-Scope 功能覆盖映射**、数据架构承接小节）、`4. 关键交互与依赖`（含接口架构清单）、`5. 部署拓扑与运行边界`、`6. ADR 清单`、`9. 追溯与证据`；其中 `004-adr.md` 必须满足 `template.md` 第 `6.3` 章定义的 ADR 最小结构契约。
3. 所有蓝图结论必须能追溯到 `G201` 的策略约束或 `G202` 的愿景边界，并且能通过覆盖声明证明 `S5-A02/S5-A03/S5-A04/S5-A05` 已被当前蓝图完整承接。
4. **反向约束覆盖检查**：G201 中所有 `mandatory=yes` 的技术约束（CST-*）、实施约束（IC-*）和异常约束（CST-EXCEPT-*）必须在蓝图中存在显式承接。承接方式可以是：范围边界（SCP-*）、组件职责（CMP-*）、数据对象（DAT-*）、接口契约（IFC-*）或部署拓扑（TOP-*）。若蓝图结论能追溯到 G201（正向追溯），但 G201 的强制约束在蓝图中缺少承接（反向遗漏），视为不可交付并返工。
5. **MVP 覆盖映射完整性检查**：蓝图 3.1 节必须包含完整的 SCP-MVP-FR 三联映射表，且满足：
   - 所有 in-scope MVP 必须有非空 `组件覆盖`（至少一个 CMP-XXX）；
   - `has_frontend_ui=yes` 的 MVP，其 `组件覆盖` 中必须至少包含一个 `frontend_consumer=yes` 的组件；
   - `has_frontend_ui=yes` 的 MVP 必须有非空 `uiux_ref`。
6. 当 G201 包含异常验收标准（AC-EXCEPTION-*）时，蓝图必须包含异常架构视图（VW-*，类型为 exception），并在视图覆盖声明中体现。
7. **可视化图表完整性检查**：
   - 蓝图必须包含至少 5 张 Mermaid 图表，分别对应 5 类视图（context/structure/interaction/deployment/exception，若 exception 不适用则至少 4 张）；
   - 图表必须可被标准 Markdown 渲染器正确渲染，无 Mermaid 语法错误；
   - 图表中的标识符（CMP-*/DAT-*/IFC-*/TOP-*）必须与正文章节中的表格严格一致；
   - 图表与正文表格互为补充，同一信息应在表格（精确字段）和图表（直观结构）中同时存在，不得仅用图表替代表格。

## 8. 失败与恢复

1. 若 `G201` 输出不完整导致无法形成蓝图主线，应由 `G200` 将当前任务判定为 `blocked`，并在 `resume_from` 写明缺失项。
2. 若 `002-architecture-vision.md` 缺失或无法读取，应由 `G200` 将当前任务判定为 `blocked`，并在 `resume_from` 写明需先补齐愿景文档。
3. 若组件边界、数据权威边界、接口契约或部署拓扑无法收敛，应由 `G200` 保持当前任务 `in_progress` 并推进到 `rework`。
4. 恢复时优先读取 `artifacts/architecture/000-task-tracker.md` 的 `resume_from`。
5. 若“供 `G204` 消费的最小字段”不完整，或覆盖声明与数据/接口字段无法证明 `S5-A02/S5-A03/S5-A04/S5-A05` 已承接，或 G201 包含异常标准但蓝图缺少异常架构视图，视为当前轮不可交付并返工。

## 9. References

- [template.md](template.md)
- [role-definition.md](references/role-definition.md)
- [execution-details.md](references/execution-details.md)
- [architecture-methods-catalog.md](../_shared/architecture-methods-catalog.md) `G203` 方法论标准引用来源
- [runtime-task-tracker-spec.md](../_shared/governance/runtime-task-tracker-spec.md)
- [quality-checker-requirements.md](../_shared/governance/quality-checker-requirements.md)
- [G200 architecture entry](../g200-architecture-entry/SKILL.md)
- [GS-Quality-Check](../gs-quality-check/SKILL.md)
- [GS-Review](../gs-review/SKILL.md)
