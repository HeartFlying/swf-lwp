---
name: g401-technology-realization
description: Complete-mode technology realization skill for detailed_design stage. Use when G301/G302/G303 have completed their outputs, and Codex needs to finalize technology implementation decisions including tech stack catalog, component/interface/data technology specs, runtime/deployment specs, technology risk specs, and technology baseline.
version: 1.0.0
---

# G401 技术实现定型 SKILL

## 元信息与执行契约

说明：完整机读契约以文档头部 YAML 为准；本章节仅提供执行摘要。

### 基本信息

| 项目 | 内容 |
|---|---|
| skill_id | `G401` |
| skill_type | `core` |
| 中文名称 | 技术实现定型 |
| 适用阶段 | `detailed_design` |
| 执行模式 | `complete` |
| 前置依赖 | `G301`、`G302`、`G303` 已完成输出，`artifacts/detailed-design/002-component-design.md`、`artifacts/detailed-design/003-interface-design.md`、`artifacts/detailed-design/004-data-design.md` 可读取 |
| 后置依赖 | 研发实现阶段 |
| 输出主文档 | `artifacts/detailed-design/005-technology-realization.md` |

### 执行契约摘要

| 项目 | 内容 |
|---|---|
| 必选输入 | `artifacts/detailed-design/002-component-design.md`（G301）、`artifacts/detailed-design/003-interface-design.md`（G302）、`artifacts/detailed-design/004-data-design.md`（G303）、`artifacts/architecture/003-architecture-blueprint.md`（G203）、`artifacts/architecture/001-technical-strategy.md`（G201） |
| 按需输入 | `artifacts/architecture/004-adr.md`、`artifacts/detailed-design/001-design-plan.md` |
| 模板与参考 | `template.md`、`references/role-definition.md`、`references/execution-details.md` |
| 交付前置摘要 | 必须形成 tech_stack_catalog、component_technology_specs、interface_technology_specs、data_technology_specs、runtime_deployment_specs、technology_risk_specs、technology_baseline |

## 1. 目标

在 G301 组件设计、G302 接口设计、G303 数据设计已完成的基础上，完成系统最终技术实现方案收敛：

1. 建立组件技术画像，明确 compute_profile、io_profile、latency_requirement、throughput_requirement、statefulness、deployment_constraint。
2. 完成编程语言、框架、中间件、存储技术选型，每个组件形成唯一主技术栈。
3. 定义接口实现技术（协议、序列化、SDK）和兼容策略。
4. 定义数据存储映射和访问模式。
5. 定义运行时与部署规格，执行技术一致性检查。
6. 输出技术风险与备选方案、系统级技术基线。
7. 为研发实现、CI/CD、测试、部署交付提供稳定输入。

## 2. 角色定义

`G401` 的角色边界、职责和输出风格见：

- [role-definition.md](references/role-definition.md)

## 3. 前置条件

1. `artifacts/detailed-design/002-component-design.md` 已存在且可读取，尤其是 `component_catalog`、`internal_structure_specs`、`component_dependencies`。
2. `artifacts/detailed-design/003-interface-design.md` 已存在且可读取，尤其是 `interface_catalog`、`interface_contract_specs`、`version_idempotency_specs`。
3. `artifacts/detailed-design/004-data-design.md` 已存在且可读取，尤其是 `data_object_catalog`、`storage_boundary_specs`、`consistency_semantics_specs`。
4. `artifacts/architecture/003-architecture-blueprint.md` 与 `artifacts/architecture/001-technical-strategy.md` 可读取。
5. 若关键组件、接口或数据对象缺失，应阻塞执行并提示缺失文件。

## 4. 输入输出契约

### 4.1 输入

**必选输入**（G300 阶段关联紧密输出）：

| 输入文件 | 来源 SKILL | 提取内容 |
|---|---|---|
| `artifacts/detailed-design/002-component-design.md` | G301 | component_catalog, internal_structure_specs, component_dependencies |
| `artifacts/detailed-design/003-interface-design.md` | G302 | interface_catalog, interface_contract_specs, version_idempotency_specs |
| `artifacts/detailed-design/004-data-design.md` | G303 | data_object_catalog, storage_boundary_specs, consistency_semantics_specs |
| `artifacts/architecture/003-architecture-blueprint.md` | G203 | 系统架构视图、技术约束 |
| `artifacts/architecture/001-technical-strategy.md` | G201 | 技术策略约束、选型边界 |

**按需输入**：

| 输入文件 | 来源 | 提取内容 |
|---|---|---|
| `artifacts/architecture/004-adr.md` | G203/G204 | 架构决策记录（技术选型相关） |
| `artifacts/detailed-design/001-design-plan.md` | G300 | 设计计划、模式冻结结果 |

### 4.2 输出

1. 主输出：`artifacts/detailed-design/005-technology-realization.md`

### 4.3 输出模板使用约束

1. **必须严格使用 `template.md` 作为输出文档结构模板**，不得自行增删章节或调整章节顺序。
2. 输出文档章节必须与 `template.md` 完全对齐，章节编号和章节名称必须一致。
3. `template.md` 中定义的表格字段为必填项，不得遗漏或替换为自由文本。
4. 若某章节内容不适用，必须显式标注 `N/A` 并说明原因，不得直接删除该章节。
5. 输出文档必须包含 `template.md` 定义的以下核心结构化字段：
   - 执行摘要
   - 技术栈目录（tech_stack_catalog）
   - 组件技术规格（component_technology_specs）
   - 接口技术规格（interface_technology_specs）
   - 数据技术规格（data_technology_specs）
   - 运行时与部署规格（runtime_deployment_specs）
   - 技术风险规格（technology_risk_specs）
   - 系统技术基线（technology_baseline）

### 4.4 质量约束

1. 输出必须使用 Markdown。
2. 文档规模 `< 5000` 行；超限必须拆分且每个文件自包含。
3. 路径统一使用 `/`。
4. 所有技术决策必须有可追溯依据，不得凭空决策。
5. 每个组件必须形成唯一主技术栈，禁止多语言主实现、多框架并存、模糊技术选型。
6. 必须执行并输出技术一致性检查结果（语言、运行时、协议、数据链路）。

## 5. 执行步骤

执行说明：G401 独立执行，不依赖运行时台账，失败时直接重新执行。

### 步骤 1：冻结技术实现范围与来源追溯

- 操作主体：`G401-SKILL`
- 具体任务：
  - 从 G301/G302/G303 输出中冻结本轮技术实现范围
  - 建立 component_id / interface_id / data_object_id 的来源追溯
  - 识别必须定稿的技术选型、延后项和约束
- 方法论：
  - 必用：`技术画像分析`
  - 必用：`约束回链`
- 输入：G301/G302/G303 输出、技术策略、架构蓝图
- 输出：范围与来源追溯结论（写入主文档）
- 依赖关系：无

### 步骤 2：建立技术栈目录

- 操作主体：`G401-SKILL`
- 具体任务：
  - 为每个技术类别生成候选清单（语言、框架、中间件、存储、运行时）
  - 根据技术策略约束过滤候选项
  - 形成技术栈目录
- 方法论：
  - 必用：`技术候选生成`
  - 必用：`技术约束过滤`
- 输入：步骤 1 输出、技术策略
- 输出：`tech_stack_catalog`（写入主文档）
- 依赖关系：依赖步骤 1 完成

### 步骤 3：定义组件技术规格

- 操作主体：`G401-SKILL`
- 具体任务：
  - 为每个组件确定最终语言、框架、运行时、中间件选型
  - 说明选择原因和放弃原因
  - 形成组件技术规格
- 方法论：
  - 必用：`技术栈收敛`
- 输入：步骤 2 输出、G301 输出
- 输出：`component_technology_specs`（写入主文档）
- 依赖关系：依赖步骤 2 完成

### 步骤 4：定义接口技术规格

- 操作主体：`G401-SKILL`
- 具体任务：
  - 为每个接口确定协议、传输方式、序列化格式、SDK/框架
  - 说明兼容策略（版本、兼容窗口、弃用策略、灰度策略）
  - 形成接口技术规格
- 方法论：
  - 必用：`技术栈收敛`
- 输入：步骤 2 输出、G302 输出
- 输出：`interface_technology_specs`（写入主文档）
- 依赖关系：依赖步骤 2 完成

### 步骤 5：定义数据技术规格

- 操作主体：`G401-SKILL`
- 具体任务：
  - 为每个数据对象确定存储技术、数据类型、一致性模型、生命周期
  - 说明访问模式（读写模式、缓存策略、索引策略）
  - 形成数据技术规格
- 方法论：
  - 必用：`技术栈收敛`
- 输入：步骤 2 输出、G303 输出
- 输出：`data_technology_specs`（写入主文档）
- 依赖关系：依赖步骤 2 完成

### 步骤 6：定义运行时与部署规格

- 操作主体：`G401-SKILL`
- 具体任务：
  - 为每个组件确定镜像、容器化方式、编排平台
  - 说明运行环境约束（CPU、内存、网络）
  - 说明可观测性技术（日志、指标、追踪）
  - 执行技术一致性检查（语言、运行时、协议、数据链路）
- 方法论：
  - 必用：`运行时建模`
  - 必用：`部署技术映射`
  - 必用：`技术一致性校验`
- 输入：步骤 3-5 输出
- 输出：`runtime_deployment_specs`、一致性检查结果（写入主文档）
- 依赖关系：依赖步骤 3-5 完成

### 步骤 7：生成技术风险与技术基线文档

- 操作主体：`G401-SKILL`
- 具体任务：
  - 识别技术风险，形成风险清单和备选方案
  - 输出系统级技术基线（主语言、主框架、通信栈、中间件栈、存储栈、部署栈）
  - **严格按 `template.md` 结构整合章节**，不得自行增删章节或调整顺序
  - 校验所有必填字段完整性，确保与 `template.md` 定义的表格字段一致
  - 执行结构自检，确认章节编号、章节名称与 `template.md` 完全对齐
  - 持久化到目标路径
- 方法论：
  - 必用：`技术风险分析`
  - 必用：`技术基线构建`
- 输入：步骤 2-6 输出
- 输出：`technology_risk_specs`、`technology_baseline`、`artifacts/detailed-design/005-technology-realization.md`
- 依赖关系：依赖步骤 2-6 完成

## 6. 验收标准

### 6.1 执行检查闭环（强制）

1. 主文档存在且路径正确：`artifacts/detailed-design/005-technology-realization.md`。
2. **文档结构必须与 `template.md` 完全对齐**：
   - 章节编号和章节名称必须一致
   - 不得自行增删章节或调整章节顺序
   - `template.md` 中定义的表格字段必须填写，不得遗漏或替换为自由文本
   - 不适用的章节必须显式标注 `N/A` 并说明原因
3. 文档必须包含以下章节（与 `template.md` 对齐）：
   - `1. 执行摘要`
   - `2. 技术实现目标与范围`
   - `3. 技术决策输入追溯`
   - `4. 技术栈目录（tech_stack_catalog）`
   - `5. 组件技术规格（component_technology_specs）`
   - `6. 接口技术规格（interface_technology_specs）`
   - `7. 数据技术规格（data_technology_specs）`
   - `8. 运行时与部署规格（runtime_deployment_specs）`
   - `9. 技术一致性检查`
   - `10. 技术风险（technology_risk_specs）`
   - `11. 系统技术基线（technology_baseline）`
   - `12. 方法检查清单`
   - `13. 供研发实施消费的最小字段`
   - `14. 追溯与证据`
4. 所有组件必须形成完整技术栈闭环（语言→框架→运行时→中间件）。
5. 所有接口必须形成实现技术闭环（协议→序列化→SDK）。
6. 所有数据对象必须形成存储技术闭环（存储技术→一致性模型→生命周期）。
7. 必须执行并输出四类一致性检查结果（语言、运行时、协议、数据链路）。
8. 必须输出系统级技术基线。
9. 所有技术决策必须有可追溯依据，追溯到 G301/G302/G303 或技术策略。
10. 若 `tech_stack_catalog`、`component_technology_specs`、`interface_technology_specs`、`data_technology_specs`、`runtime_deployment_specs`、`technology_risk_specs`、`technology_baseline` 任一缺失，当前轮视为不通过。

## 7. 失败与恢复

1. 若 G301/G302/G303 输出缺失导致无法冻结技术范围，应阻塞执行并提示缺失文件。
2. 若技术策略约束冲突导致无法收敛，应阻塞执行并提示冲突项。
3. 若组件技术栈无法收敛，应阻塞执行并列出候选项和过滤原因。
4. 若一致性检查失败（语言、运行时、协议、数据链路任一为 fail），应阻塞执行并列出不一致项。
5. **若输出文档结构与 `template.md` 不对齐**（章节缺失、章节顺序错误、表格字段遗漏），应阻塞执行并提示具体偏差项。
6. 恢复机制：直接重新执行 SKILL，输出文档第 1 章包含执行摘要记录执行状态。

## 8. References

- [template.md](template.md)
- [role-definition.md](references/role-definition.md)
- [execution-details.md](references/execution-details.md)
- [G301 component design](../g301-component-design/SKILL.md)
- [G302 interface design](../g302-interface-design/SKILL.md)
- [G303 data design](../g303-data-design/SKILL.md)
- [G201 technical strategy](../g201-technical-strategy/SKILL.md)
- [G203 architecture blueprint](../g203-architecture-blueprint/SKILL.md)
