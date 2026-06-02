---
name: g102-requirements-baseline
description: 需求基线定义（requirements baseline），用于冻结功能/非功能需求、约束、优先级与验证标准，输出可供 G103 消费的需求基线。
version: 1.0.0
---

# G102 需求基线定义 SKILL

## 元信息与执行契约

说明：完整机读契约以文档头部 YAML 为准；本章节仅提供执行摘要。

### 基本信息

| 项目          | 内容                                                    |
| ----------- | ----------------------------------------------------- |
| skill\_id   | `G102`                                                |
| skill\_type | `core`                                                |
| 中文名称        | 需求基线定义                                                |
| 适用阶段        | `requirements`                                        |
| 执行模式        | `fast`、`standard`、`complete`                          |
| 前置依赖        | `RA-02`（必选），`RA-03`（conditional）                      |
| 后置依赖        | `G103`                                                |
| 输出主文档       | `artifacts/requirements/003-requirements-baseline.md` |

### 执行契约摘要

| 项目      | 内容                                                                                                              |
| ------- | --------------------------------------------------------------------------------------------------------------- |
| 运行时任务映射 | 主起草任务为 `RA-04`；质量检查与用户评审分别承接到共享服务任务 `RA-06(GS-Quality-Check)`、`RA-07(GS-Review)`；`skill_id` 维持各任务原定义，不重写为 `G102` |
| Skill 生命周期 | `drafting -> quality_check -> user_review(stage_gate=RA-07) -> completed`（返工回路：`quality_check/user_review -> rework -> drafting`） |
| 运行时台账路径 | `artifacts/requirements/000-task-tracker.md`                                                                    |
| 证据路径    | `evidence/RA-04/`                                                                                               |
| 必选输入    | `user_request`、`artifacts/requirements/001-requirements-intake.md`                                              |
| 按需输入    | `artifacts/requirements/001a-requirements-clarification.md`、`artifacts/requirements/002-business-context.md`    |
| 模板与参考   | `template.md`、`references/role-definition.md`、`references/execution-details.md`、`../_shared/requirements-methods-catalog.md`                                 |
| 质量门摘要   | `overall_status` 仅允许 `pass/pass_with_warning`，且不得有 `critical/major` 问题                                          |

## 1. 目标

形成可冻结、可追溯、可验证的需求基线，明确功能需求、非功能需求、约束条件、优先级和验收标准，作为 `G103` 输入基线。

## 2. 前置条件

1. `RA-01` 已完成，并已产出 `artifacts/requirements/001-requirements-intake.md`。
2. `RA-02` 已完成；若存在澄清轮次，必须读取 `artifacts/requirements/001a-requirements-clarification.md` 并完成“澄清闭环”。
3. 若 `G101` 已执行，需消费 `artifacts/requirements/002-business-context.md`；若未执行，必须在主文档显式声明缺失上下文与影响范围。
4. `G102` 起草固定映射到 `RA-04`；质量门复用 requirements 阶段公共任务 `RA-06/RA-07`。

## 3. 输入输出契约

### 3.1 输入

1. 用户需求描述（必选）
2. `artifacts/requirements/001-requirements-intake.md`（必选）
3. `artifacts/requirements/001a-requirements-clarification.md`（按需）
4. `artifacts/requirements/002-business-context.md`（按需）

### 3.1A 方法目录引用

`G102` 中出现的方法名以 [requirements-methods-catalog.md](../_shared/requirements-methods-catalog.md) 为唯一标准引用来源。

### 3.2 输出

1. 主输出：`artifacts/requirements/003-requirements-baseline.md`
2. 证据目录：`evidence/RA-04/`
3. 追溯矩阵：写入主文档章节；如需单独文件可额外输出 `artifacts/requirements/003a-requirements-traceability.csv`

### 3.3 供 G103 消费的最小字段

1. `requirements_catalog`：FR/NFR 的唯一 ID、描述、来源、优先级。
2. `scope_baseline`：Must/Should/Could/Won't 分层结果。
3. `constraints_baseline`：业务/技术/合规/资源/时间约束及强制性标记，约束编号格式为 `CST-xxx`。
4. `acceptance_baseline`：每条需求的验收标准与验证方式。
5. `open_issues`：未决事项、工作假设、风险与解除条件。

### 3.4 质量约束

1. 输出必须使用 Markdown；追溯矩阵可内嵌或补充 CSV。
2. 文档规模 `< 10000` 行；超限必须拆分且每个文件自包含。
3. 路径统一使用 `/`。
4. 每条 `Must/Should` 需求必须存在 `来源 -> 优先级 -> 验收标准 -> 风险` 关系。

## 4. 执行步骤

执行说明：

1. `G102` 由 requirements 阶段入口编排 SKILL `G100` 触发，并必须在独立子代理中执行。
2. 子代理仅负责本 Skill 文档产出；状态回写由阶段宿主 `RA-Agent` 统一执行。

### 步骤 1：功能性需求识别

- 操作主体：`G102-SKILL`
- 具体任务：
  - 提取功能性需求并赋予 `FR-xxx` 唯一编号
  - 明确需求描述、业务价值、触发场景、需求来源
  - 输出功能需求清单
- 方法论（产品经理视角）：
  - 必用：`第一性原理`（拆分事实、假设、推断）。
  - 必用：`问题风暴`（先列问题再归并为需求）。
  - 必用：`用户旅程图`（确保需求覆盖关键触点）。
  - 可选：`思维导图`（用于分组与层次化）。
- 输入：需求描述、需求接收与澄清产物
- 输出：功能需求清单（写入主文档）
- 依赖关系：无

### 步骤 2：非功能性需求识别

- 操作主体：`G102-SKILL`
- 具体任务：
  - 识别性能、安全、可用性、可扩展性、可维护性需求
  - 赋予 `NFR-xxx` 唯一编号
  - 用可验证指标表达阈值
- 方法论（产品经理视角）：
  - 必用：`约束映射`（明确质量属性受到的边界）。
  - 必用：`失败分析`（从历史失败反推必要 NFR）。
  - 必用：`决策树`（明确不同质量目标的取舍路径）。
  - 可选：`特征迁移`（参考成熟产品质量目标）。
- 输入：需求接收与澄清结果、业务背景（如有）
- 输出：非功能需求清单（写入主文档）
- 依赖关系：可与步骤 1 并行启动，最终合并校对

### 步骤 3：约束条件基线化

- 操作主体：`G102-SKILL`
- 具体任务：
  - 提炼业务、技术、合规、资源、时间约束
  - 区分“强约束/弱约束”
  - 输出约束条件清单
- 方法论（产品经理视角）：
  - 必用：`约束映射`（全量列举与分级）。
  - 必用：`假设反转`（验证约束是否被误判为事实）。
  - 必用：`五问法（5 Whys）`（追根到约束来源）。
  - 可选：`类比思维`（参考相近项目约束处理策略）。
- 输入：需求接收与澄清产物、业务背景（如有）
- 输出：约束条件清单（写入主文档）
- 依赖关系：可与步骤 1 并行执行

### 步骤 4：需求优先级排序

- 操作主体：`G102-SKILL`
- 具体任务：
  - 基于 `MoSCoW` 完成 Must/Should/Could/Won't 分层
  - 标识需求依赖关系与冲突
  - 形成优先级矩阵
- 方法论（产品经理视角）：
  - 必用：`决策树`（处理冲突需求与取舍路径）。
  - 必用：`解决方案矩阵`（价值、成本、风险对齐）。
  - 必用：`角色扮演`（用户/业务/技术多视角权衡）。
  - 可选：`六顶思考帽`（复核结论偏差）。
- 输入：步骤 1、2、3 输出
- 输出：优先级矩阵（写入主文档）
- 依赖关系：依赖步骤 1、2、3 完成

### 步骤 5：验证标准定义

- 操作主体：`G102-SKILL`
- 具体任务：
  - 为每条需求定义验证方式与验收标准
- 方法论（产品经理视角）：
  - 必用：`解决方案矩阵`（需求、验证、证据映射）。
  - 必用：`失败分析`（逆向检查验收缺口）。
  - 必用：`六顶思考帽`（事实/风险/收益维度复核）。
  - 可选：`SCAMPER`（补充替代验收路径）。
- 输入：步骤 4 输出
- 输出：验收标准清单（写入主文档）
- 依赖关系：依赖步骤 4 完成

### 步骤 6：追溯关系建立

- 操作主体：`G102-SKILL`
- 具体任务：
  - 建立 `FR/NFR/CST -> 来源 -> 澄清 -> 验收 -> 风险` 的追溯关系
  - 汇总未决事项与解除条件
- 方法论（产品经理视角）：
  - 必用：`解决方案矩阵`（需求、来源、验收、风险映射）。
  - 必用：`失败分析`（逆向检查追溯缺口）。
  - 必用：`六顶思考帽`（事实/风险/收益维度复核）。
  - 可选：`SCAMPER`（补充替代追溯路径）。
- 输入：步骤 5 输出
- 输出：验证与追溯矩阵（写入主文档，必要时输出 CSV）
- 依赖关系：依赖步骤 5 完成

### 步骤 7：生成需求基线文档

- 操作主体：`G102-SKILL`
- 具体任务：
  - 按模板整合并完成结构自检
  - 校验编号唯一性、路径格式、追溯完整性
  - 持久化到目标路径
- 输入：步骤 1-6 输出
- 输出：`artifacts/requirements/003-requirements-baseline.md`
- **术语一致性**（新增）：
  - FR/NFR 命名中使用的术语应与 `artifacts/requirements/CONTEXT.md` 中的规范名称一致（如该文件已存在）
  - 若引入新的领域术语，同步追加到 `artifacts/requirements/CONTEXT.md`
  - 若发现已有术语使用不一致，标记为 minor issue
- 依赖关系：依赖步骤 1-6 完成

## 5. 与运行时台账对齐

推荐任务映射：

- `task_id`: `RA-04`（起草主任务）
- `skill_id`: `G102`
- Skill 生命周期：`drafting -> quality_check -> user_review(stage_gate=RA-07) -> completed`
- 返工回路：`quality_check/user_review -> rework -> drafting`

执行要求：

1. `RA-04` 负责 `drafting` 与返工后的再次起草；`RA-06` 负责 `quality_check`；`RA-07` 负责 `user_review`。
2. 状态变更时同步更新当前任务的 `status_code/status_label/skill_stage/resume_from/evidence_path/updated_at`。
3. `RA-04` 在起草完成后保持 `in_progress`，由 `RA-Agent` 推进到 `RA-06/RA-07`，不得将质量门写回为 `RA-04` 的固定阶段。
4. `RA-07` 阶段汇总评审通过后，由 `RA-Agent` 按任务分工将正式文档相关任务收口为 `done`。
5. 质量检查结果写入质量报告字段（如 `validation_summary` 或治理定义等效字段），不写入 `review_result`。

## 6. 验收标准

### 6.1 执行检查闭环（强制）

为避免质量门数据来源后置，`G102` 在本 SKILL 内固定以下检查闭环：

| 项目 | 固定定义 |
|---|---|
| 质量检查工具 | `GS-Quality-Check` |
| 触发任务 | `RA-06` |
| 质量报告路径 | `artifacts/reviews/requirements-quality-check.md` |
| 最小字段 | `quality_check_summary.overall_status`、`quality_check_summary.scores.*`（按 RA 阶段验收要求）、`validation_summary.issue_count` |
| 消费任务 | `RA-07`（阶段汇总评审）与本 SKILL 第 6 章验收判断 |
| 缺失处理 | 任一最小字段缺失即判定当前轮不通过，不得推进 `done` |

1. 主文档存在且路径正确：`artifacts/requirements/003-requirements-baseline.md`。
2. 文档章节与 `template.md` 对齐，至少包含：`1. 需求基线摘要`、`2. 功能性需求（FR）`、`3. 非功能性需求（NFR）`、`4. 约束条件`、`5. 优先级矩阵`、`6. 验证与追溯`、`7. 未决事项与风险`。
3. `FR-xxx/NFR-xxx/CST-xxx` 编号唯一，且每条 `Must/Should` 需求都有来源、验收标准与风险链路。
4. 澄清闭环完整：`001a` 中的关键问题必须在基线中有“采纳/拒绝/待定”结论。
5. 质量检查结果来源必须为 `artifacts/reviews/requirements-quality-check.md`，并满足：`quality_check_summary.overall_status` 为 `pass` 或 `pass_with_warning`，且 `validation_summary.issue_count`（或治理定义等效字段）中 `critical/major` 问题数量均为 `0`。
6. 不引入治理层未定义字段作为通过条件。
7. `evidence/RA-04/` 目录非空，至少包含 1 份过程证据文件（编号校验记录、追溯矩阵生成过程、MoSCoW分层依据、约束强度判定依据）。
8. `G102` 为 `G103` 上游硬门，`requirements` 阶段最终通过门槛以 `agents/ra-agent.md` 第 8 章定义为准。

## 7. 失败与恢复

1. 若关键输入缺失导致无法继续，标记 `blocked`，在 `resume_from` 写明解除条件。
2. 若结构不完整、编号冲突或追溯断链，保持 `in_progress` 并进入 `rework`。
3. 恢复时优先读取 `artifacts/requirements/000-task-tracker.md` 的 `resume_from`。
4. 若存在未闭环澄清项但继续推进，视为阻断缺陷并返工。
5. 若 `Must/Should` 需求缺少验收标准或风险链路，视为不可交付并返工。
