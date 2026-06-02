---
name: g101-business-context
description: 业务背景分析（business context），用于 market analysis、competitor analysis、pain points 识别并产出结构化业务上下文。
version: 1.0.1
---

# G101 业务背景分析 SKILL

## 元信息与执行契约

说明：完整机读契约以文档头部 YAML 为准；本章节仅提供执行摘要，避免与 YAML 形成双维护。

### 基本信息

| 项目 | 内容 |
|---|---|
| skill_id | `G101` |
| skill_type | `optional` |
| 中文名称 | 业务背景分析 |
| 适用阶段 | `requirements` |
| 执行模式 | `standard`、`complete` |
| 前置依赖 | `RA-01`（必选），`RA-02`（前置任务；未触发澄清时按 no-op 完成并置 `done`） |
| 后置依赖 | `G102` |
| 输出主文档 | `artifacts/requirements/002-business-context.md` |

### 执行契约摘要

| 项目 | 内容 |
|---|---|
| 运行时任务映射 | `task_id=RA-03`，`skill_id=G101` |
| 任务阶段流转 | `drafting -> quality_check -> user_review(stage_gate=RA-07) -> completed`（返工回路：`quality_check/user_review -> rework -> drafting`） |
| 运行时台账路径 | `artifacts/requirements/000-task-tracker.md` |
| 证据路径 | `evidence/RA-03/` |
| 必选输入 | `user_request`、`artifacts/requirements/001-requirements-intake.md` |
| 按需输入 | `artifacts/requirements/001a-requirements-clarification.md`、行业资料、竞品信息 |
| 模板与参考 | `template.md`、`references/role-definition.md`、`references/execution-details.md`、`../_shared/requirements-methods-catalog.md` |
| 质量门摘要 | `overall_status` 仅允许 `pass/pass_with_warning`，且不得有 `critical/major` 问题 |

---

## 1. 目标

在需求基线冻结前，产出可追溯、可评审的业务背景分析，覆盖市场、竞品、痛点与机会识别，为 `G102` 提供业务上下文输入。

---

## 2. 前置条件

1. `RA-01` 已完成，并已产出 `artifacts/requirements/001-requirements-intake.md`。
2. 若触发澄清，`RA-02` 已完成，并已产出 `artifacts/requirements/001a-requirements-clarification.md`；若未触发澄清，`RA-02` 应按 no-op 收口并置为 `done` 后继续。
3. 当前 `final_mode` 为 `standard` 或 `complete`；`fast` 模式默认跳过 `G101`。
4. 任务映射关系固定为：`RA-01`、`RA-02` 为前置任务，`RA-03` 为本 Skill 运行时任务。

---

## 3. 输入输出契约

### 3.1 输入

1. 用户需求描述（必选）
2. `artifacts/requirements/001-requirements-intake.md`（必选）
3. `artifacts/requirements/001a-requirements-clarification.md`（按需）
4. 用户补充的行业资料/竞品信息（按需）

### 3.1A 方法目录引用

`G101` 中出现的方法名以 [requirements-methods-catalog.md](../_shared/requirements-methods-catalog.md) 为唯一标准引用来源。

### 3.2 输出

1. 主输出：`artifacts/requirements/002-business-context.md`
2. 证据目录：`evidence/RA-03/`

### 3.3 供 G102 消费的最小字段

`G101` 输出需至少包含以下可结构化消费信息：

1. 目标市场与目标用户分层结论（含关键场景）。
2. 竞品对比矩阵（至少 3 个竞品，不足时写明原因）。
3. 关键业务痛点列表与优先级。
4. 机会点列表（含对应痛点映射）。
5. 工作假设与风险清单（含置信度标记）。

### 3.4 质量约束

1. 输出必须使用 Markdown。
2. 文档规模 `< 10000` 行；超限必须拆分且每个文件自包含。
3. 路径统一使用 `/`。
4. 文档必须可追溯到输入证据与关键结论来源。

---

## 4. 执行步骤

执行说明：

1. `G101` 由 requirements 阶段入口编排 SKILL `G100` 触发，并必须在独立子代理中执行。
2. 子代理仅负责本 Skill 文档产出；状态回写由阶段宿主 `RA-Agent` 统一执行。

### 步骤 1：市场数据分析

- 操作主体：`G101-SKILL`
- 具体任务：
  - 提炼目标市场与目标人群范围
  - 形成市场规模、趋势、细分结论
  - 标记数据来源、数据置信度与工作假设
- 方法论（产品经理视角）：
  - 必用：`第一性原理`，先拆解“已知事实/假设/不确定项”，避免直接套行业结论。
  - 必用：`问题风暴`，先产出关键问题清单，再组织数据采集与验证。
  - 必用：`约束映射`，识别政策、资源、时间、技术约束及可突破边界。
  - 可选：`思维导图`，用于整理市场因素与细分关系，减少分析遗漏。
  - 保留分析框架：`TAM/SAM/SOM`、`PESTEL`、`JTBD`。
- 产出要求：
  - 至少给出 1 版 `TAM/SAM/SOM` 估算与口径说明。
  - 至少识别 3 条关键外部驱动（来自 `PESTEL`）并标注机会/风险属性。
  - 至少输出 2 个基于 `JTBD` 的细分任务场景。
- 输入：需求描述、用户提供行业资料
- 输出：市场分析结论（写入主文档）
- 依赖关系：无

### 步骤 2：竞品分析

- 操作主体：`G101-SKILL`
- 具体任务：
  - 识别 3-5 个主要竞品（不足时写明原因）
  - 形成功能差异、优劣势与机会点
  - 产出竞品对比矩阵
- 方法论（产品经理视角）：
  - 必用：`角色扮演`，分别从用户、运营、销售、技术与竞品方视角评估差异。
  - 必用：`决策树`，拆解竞品关键策略路径与可能结果。
  - 必用：`特征迁移`，提炼竞品有效能力并判断“可借鉴/不可借鉴”。
  - 可选：`类比思维`，参考相邻行业对标对象寻找替代方案。
  - 保留分析框架：`直接/间接/替代` 分层、`五力模型`、`战略画布`、`SWOT`。
- 产出要求：
  - 竞品清单需覆盖直接、间接、替代三类（每类至少 1 个，确无则说明）。
  - 至少输出 1 版价值维度战略画布结论（文字或表格）。
  - 对 Top2 竞品给出结构化 `SWOT` 摘要。
- 输入：需求描述、竞品信息
- 输出：竞品分析结论（写入主文档）
- 依赖关系：可与步骤 1 并行

### 步骤 3：业务痛点识别

- 操作主体：`G101-SKILL`
- 具体任务：
  - 汇总目标用户、核心场景与现有痛点
  - 形成痛点-机会矩阵
  - 标记关键不确定项与影响
- 方法论（产品经理视角）：
  - 必用：`用户旅程图`，按场景拆解触点并定位痛点发生环节。
  - 必用：`五问法（5 Whys）`，对 P0/P1 痛点做根因下钻。
  - 必用：`失败分析`，复盘历史失败案例，避免重复踩坑。
  - 可选：`假设反转`，对关键假设做反向验证，识别隐藏风险。
  - 保留优先级框架：`Kano`、`RICE/ICE`。
- 产出要求：
  - 至少输出 1 条核心用户旅程并标注关键痛点节点。
  - 对 P0 痛点至少完成 1 轮 `5 Whys` 根因分析。
  - 痛点机会矩阵需包含优先级评分字段（可用 `RICE/ICE`）。
- 输入：步骤 1、步骤 2 的分析结论
- 输出：痛点与机会识别结论（写入主文档）
- 依赖关系：依赖步骤 1、2 完成

### 步骤 4：生成业务背景报告

- 操作主体：`G101-SKILL`
- 具体任务：
  - 按模板整合章节并完成自检
  - 校验结构完整性、路径格式、追溯引用
  - 持久化到目标路径
- 方法论（收敛评审）：
  - 必用：`解决方案矩阵`，将“痛点-机会-价值-优先级”做统一映射收敛。
  - 必用：`六顶思考帽`，按事实、收益、风险、创意、情感、流程进行交叉复核。
  - 可选：`SCAMPER`，用于补充改进建议与替代方案。
- 输入：步骤 1-3 结论
- 输出：`artifacts/requirements/002-business-context.md`
- **术语发现**（新增）：
  - 从市场分析和竞品分析中提取领域特定术语
  - 区分"行业通用术语"和"本项目专用术语"
  - 为每个领域术语提议规范名称和 Avoid 别名
  - 增量写入 `artifacts/requirements/CONTEXT.md`（如已存在）；如不存在则汇总术语列表供 G100 在阶段收尾时统一产出
- 依赖关系：依赖步骤 1、2、3 完成

---

## 5. 与运行时台账对齐

推荐任务映射：

- `task_id`: `RA-03`
- `skill_id`: `G101`
- `skill_stage` 推进：`drafting -> quality_check -> user_review(stage_gate=RA-07) -> completed`
- 返工回路：`quality_check/user_review -> rework -> drafting`

执行要求：

1. 状态变更时同步更新 `status_code/status_label/skill_stage/resume_from/evidence_path/updated_at`。
2. 评审前保持 `in_progress`，`RA-07` 阶段汇总评审通过后再置 `done`。
3. 进入质量检查时由 `RA-Agent` 调用 `GS-Quality-Check`；对 `G101` 的正式回填只使用归一化后的 `quality_gate_ref.*`，不写入 `review_result`，也不并列暴露 `quality_check_summary` / `validation_summary` 原始结构。
4. `GS-Review` 统一由 `RA-07` 触发阶段汇总评审，评审未通过时任务保持 `in_progress` 并进入 `rework`。

---

## 6. 验收标准

### 6.1 执行检查闭环（强制）

为避免质量门数据来源后置，`G101` 在本 SKILL 内固定以下检查闭环：

| 项目 | 固定定义 |
|---|---|
| 质量检查工具 | `GS-Quality-Check` |
| 触发任务 | `RA-06` |
| 质量报告路径 | `artifacts/reviews/requirements-quality-check.md` |
| 最小字段 | `quality_gate_ref.overall_status`、`quality_gate_ref.scores.*`（按 RA 阶段验收要求）、`quality_gate_ref.issue_count.*`、`quality_gate_ref.evidence.report_path` |
| 消费任务 | `RA-07`（阶段汇总评审）与本 SKILL 第 6 章验收判断 |
| 缺失处理 | 任一最小字段缺失即判定当前轮不通过，不得推进 `done` |

1. 主文档存在且路径正确：`artifacts/requirements/002-business-context.md`。
2. 文档章节必须与 `template.md` 对齐，至少包含以下一级章节：`1. 市场分析`、`2. 竞品对比`、`3. 业务痛点识别`、`4. 机会识别与建议`、`5. 追溯与证据`。
3. 关键结论可追溯到输入或显式假设。
4. 质量检查结果来源必须为 `artifacts/reviews/requirements-quality-check.md`，并满足：`quality_gate_ref.overall_status` 为 `pass` 或 `pass_with_warning`，且 `quality_gate_ref.issue_count.critical`、`quality_gate_ref.issue_count.major` 均为 `0`（字段缺失视为不通过）。
5. 不引入治理层未定义字段作为通过条件。
6. 主文档需显式标注关键结论的数据来源与置信度（至少覆盖市场结论、竞品结论、机会点结论）。
7. `evidence/RA-03/` 目录非空，至少包含 1 份过程证据文件（市场数据来源、竞品信息来源、痛点/机会评分过程）。
8. `G101` 为 Skill 级验收门，`requirements` 阶段最终通过门槛以 `agents/ra-agent.md` 第 8 章定义为准。

---

## 7. 失败与恢复

1. 若关键输入缺失导致无法继续，标记 `blocked`，在 `resume_from` 写明解除条件。
2. 若结构不完整或质量检查失败，保持 `in_progress` 并进入 `rework`。
3. 恢复时优先读取 `artifacts/requirements/000-task-tracker.md` 的 `resume_from`。
4. 若竞品数量不足 3 且未说明原因，视为结构缺失并返工。
5. 若仅有描述性文字且缺少痛点优先级或机会映射，视为不可消费并返工。
6. 若路径格式混用（`\` 与 `/` 混用）导致引用不可解析，需统一修复后再提交评审。
