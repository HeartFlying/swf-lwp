---
name: g203-architecture-blueprint
description: 基于 G201 技术策略与 G202 架构愿景，产出架构蓝图与 ADR 集
version: 0.2.0
---

# G203 架构蓝图定义

## 输入

| 文件 | 必要性 |
|---|---|
| artifacts/architecture/001-technical-strategy.md | 必选 |
| artifacts/architecture/002-architecture-vision.md | 必选 |
| artifacts/requirements/004-mvp-definition.md | 必选 |
| artifacts/requirements/003-requirements-baseline.md | 按需 |
| artifacts/architecture/001-architecture-intake.md | 按需 |
| artifacts/reviews/001-requirements-review.md | 按需 |

## 输出

| 文件 | 说明 |
|---|---|
| artifacts/architecture/003-architecture-blueprint.md | 主蓝图文档 |
| artifacts/architecture/004-adr.md | 架构决策记录 |
| evidence/AD-05/ | 证据目录（校验结果、约束覆盖记录） |

## 核心约束

### 必须覆盖的视图

蓝图必须包含以下架构视图，每类视图必须有对应的 Mermaid 图表：

| 视图类型 | 图表类型 | 触发条件 |
|---|---|---|
| context（上下文视图） | System Context Diagram | 始终必须 |
| structure（结构视图） | Component Structure Diagram | 始终必须 |
| interaction（交互视图） | Sequence/Flow Diagram | 始终必须 |
| deployment（部署视图） | Deployment Topology Diagram | 始终必须 |
| exception（异常处理视图） | State Machine Diagram | 当 G201 包含 AC-EXCEPTION-* 时 |

### 必须满足的追溯约束

1. G201 中所有 `mandatory=yes` 的约束（CST-*/IC-*/CST-EXCEPT-*）必须在蓝图中被显式承接，或显式标注 `deferred`/`out_of_scope` 并说明理由。
2. `004-mvp-definition.md` 中所有 in-scope MVP 必须有非空组件覆盖（至少一个 CMP-XXX）。
3. 蓝图结论必须能追溯到 G201 的技术策略与 G202 的愿景约束。

### 图表约束

- 图表中出现的所有标识符（CMP-*/DAT-*/IFC-*/TOP-*）必须在正文对应表格中有定义。
- 图表与正文表格互为补充，不得仅用图表替代表格。
- Mermaid 语法必须有效，确保可被标准渲染器渲染。

### 格式约束

- 输出使用 Markdown。
- 路径统一使用 `/`。
- 文档规模 < 10000 行，超限必须拆分且每个文件自包含。

## 质量门

| 检查项 | 标准 |
|---|---|
| 主文档章节对齐 | 至少包含：蓝图目标与范围、架构视图、组件与职责（含 MVP 覆盖映射）、关键交互与依赖、部署拓扑与运行边界、ADR 清单、追溯与证据 |
| 强制约束承接 | G201 中 mandatory=yes 的约束无遗漏 |
| MVP 覆盖完整性 | 所有 in-scope MVP 有非空组件覆盖 |
| 图表完整性 | 至少 4 张 Mermaid 图表（exception 不适用时），标识符与正文一致 |
| 整体状态 | 仅允许 pass 或 pass_with_warning，不得有 critical/major 问题 |

## 失败处理

- 若上游必选输入缺失或不完整 → 标记为 blocked，写明缺失项。
- 若质量门未通过 → 标记为 rework，按检查结果修正。
- 恢复时优先读取 artifacts/architecture/000-task-tracker.md 的 resume_from。

## 参考

- template.md
- references/execution-details.md
- references/role-definition.md
- ../_shared/architecture-methods-catalog.md