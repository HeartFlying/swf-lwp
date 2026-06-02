---
name: prd-design-readiness-review
description: 当需要评审PRD是否具备进入系统设计阶段条件、执行Design Readiness Review、生成准入Gate结论、输出研发工作流状态流转依据时使用。
---

# PRD 设计准入评审

## 概述

本 Skill 用于在研发工作流中执行 PRD 进入系统设计阶段前的准入评审。评审者以资深系统架构师身份工作，基于量化清单判断 PRD 是否可进入系统设计，并输出可供调度层消费的结构化结果。

核心原则：评审 PRD 的业务输入完整度，不要求 PRD 提前完成系统设计。

## 角色属性

使用本 Skill 时，必须采用以下角色设定：

| 属性 | 要求 |
| --- | --- |
| 角色 | 资深系统架构师 / Design Readiness Reviewer |
| 经验假设 | 具备中大型系统、企业级系统、平台型系统、微服务项目的设计与交付经验 |
| 评审立场 | 严格、可复核、面向工程落地 |
| 关注重点 | 业务目标、范围、角色、流程、状态、规则、核心对象、外部依赖、验收标准、需求收敛 |
| 禁止行为 | 不替 PRD 编造缺失信息；不要求 PRD 提供详细技术设计；不输出泛泛表扬 |

## 输入要求

开始评审前，确认至少具备以下输入之一：

- PRD 正文。
- PRD 文件路径。
- PRD 摘要和关键章节。

如 PRD 内容不足以评审，仍必须输出评审结果，`gate_result` 应为 `FAIL`，并在 `required_prd_actions` 中列出需要补充的材料。

## 输出要求

评审完成后，必须输出结构化评审结果（JSON 格式）和 Markdown 评审报告。

### 输出路径规范

当作为 requirements 阶段入口编排（G100）的子代理调用时，评审报告输出路径固定为：

```
artifacts/reviews/001a-prd-design-readiness-review.md
```

独立执行时，可根据调用方指定路径输出，但必须符合 `artifacts/reviews/` 目录规范。

### 输出形态

1. **结构化 JSON**：必须包含 `gate_result`、`workflow_transition`、`final_score`、`blocker_avg_score`、`checklist_used` 等核心字段。
2. **Markdown 报告**：必须包含评审摘要、检查项评分、失败 Blocker 详情、Major 问题、补齐建议、设计阶段说明。

## 强制评审依据

详细量化清单在 `references/checklist.md`。

硬性规则：

- 执行完整 PRD 准入评审时，必须读取 `references/checklist.md`。
- 未读取 `references/checklist.md` 时，不得输出 `PASS` 或 `CONDITIONAL_PASS`。
- 完整评审必须逐项覆盖 `references/checklist.md` 中所有适用检查项。
- 完整评审的 `item_scores` 必须覆盖所有适用检查项；否则 `gate_result` 最多只能为 `CONDITIONAL_PASS`。
- 快速预审也必须覆盖所有 BLOCKER 项，并在输出中将 `review_mode` 标记为 `QUICK_BLOCKER_REVIEW`。
- 若用户要求“是否可进入系统设计”“准入评审”“Gate 结论”“DRR 评审”，默认执行完整评审。

输出中必须提供 checklist 使用证据：

```json
{
  "checklist_used": true,
  "checklist_reference": "references/checklist.md",
  "checklist_version": "prd-design-readiness-review/references/checklist.md",
  "checklist_items_evaluated": ["A1", "A2", "A3"],
  "missing_checklist_items": []
}
```

如果无法读取 `references/checklist.md`，必须输出：

```json
{
  "gate_result": "FAIL",
  "workflow_transition": "RETURN_TO_PRD_REWORK",
  "checklist_used": false,
  "checklist_load_error": "无法读取 references/checklist.md，完整准入评审无效。"
}
```

## SOP 工作流

### 1. 建立评审上下文

识别 PRD 所属项目类型、业务域、阶段和评审目标。

必须判断：

- 当前评审是完整 DRR，还是快速预审。
- PRD 是否是进入系统设计前的输入文档。
- 是否存在明显缺失的 PRD 内容。

### 2. 加载强制清单

执行完整评审时，先读取 `references/checklist.md`，再开始评分。

必须建立检查项集合：

- `all_checklist_items`：清单中定义的全部检查项。
- `applicable_items`：本次 PRD 适用的检查项。
- `not_applicable_items`：本次 PRD 不适用的检查项，并说明原因。
- `checklist_items_evaluated`：实际完成评分的检查项。
- `missing_checklist_items`：适用但未评分的检查项。

完整评审完成前必须校验：

```text
missing_checklist_items = applicable_items - checklist_items_evaluated
```

若 `missing_checklist_items` 非空：

- 不得输出 `PASS`。
- 必须在 `required_prd_actions` 或 `review_process_issues` 中说明遗漏项。
- 若遗漏项包含 BLOCKER，`gate_result` 必须为 `FAIL`。

### 3. 明确设计边界

评审时必须区分：

| PRD 必须提供 | 系统设计阶段展开 |
| --- | --- |
| 业务目标、范围、主流程、异常流程、状态、规则、验收标准 | 技术选型、接口协议、存储模型、重试策略、容灾架构 |
| 外部依赖的业务用途、交互时机、集成模式、实时性要求、失败后的业务期望 | API 字段、错误码、鉴权、超时、熔断、补偿机制、服务编排、中间件选型 |
| 业务不可接受的错误结果 | 幂等键、锁、事务、消息顺序、对账实现 |
| 安全隐私、数据主权、部署约束、合规认证要求 | 加密策略、网络架构、区域部署、租户隔离、审计实现 |

如果发现问题属于系统设计阶段展开内容，不得作为 PRD 严重缺陷扣重分；应放入 `design_stage_notes`。

### 4. 执行量化评分

对每个适用项执行：

1. 判断是否适用，不适用则标记 `N/A` 并说明原因。
2. 核验 `required_fields`。
3. 按 0-5 分评分。
4. 记录 PRD 中的证据或缺失原因。
5. 对低于 3 分的项输出补充建议。

统一评分：

| 分值 | 含义 |
| ---: | --- |
| 0 | 完全缺失 |
| 1 | 只有关键词级提及 |
| 2 | 有描述但不可执行 |
| 3 | 基本明确，可支持初步设计 |
| 4 | 明确可验证 |
| 5 | 完整闭环 |

权重：

| 等级 | 权重 |
| --- | ---: |
| BLOCKER | 3 |
| MAJOR | 2 |
| MINOR | 1 |
| N/A | 0 |

### 5. 计算 Gate 结论

计算：

```text
item_weighted_score = item_score * item_weight
max_item_weighted_score = 5 * item_weight

final_score =
  sum(item_weighted_score for applicable items)
  / sum(max_item_weighted_score for applicable items)
  * 100

blocker_avg_score =
  sum(score for applicable BLOCKER items)
  / count(applicable BLOCKER items)
```

Gate 规则：

| 结论 | 条件 |
| --- | --- |
| PASS | 无 BLOCKER 得分 <= 2；final_score >= 85；blocker_avg_score >= 4.0 |
| CONDITIONAL_PASS | 无 BLOCKER 得分 <= 2；final_score >= 70；存在需补齐的 MAJOR/MINOR 问题 |
| FAIL | 任一 BLOCKER 得分 <= 2；或 final_score < 70；或关键未决项无 Owner/时间 |

附加规则：

- `checklist_used != true` 时，必须为 `FAIL`。
- `missing_checklist_items` 非空时，不得为 `PASS`。
- MAJOR 项得分 <= 2 的数量 >= 4，最多只能给 `CONDITIONAL_PASS`。
- 核心 Blocker 平均分低于 4.0，即使总分 >= 85，也最多只能给 `CONDITIONAL_PASS`。
- 发现资损、越权、重复履约、严重合规等业务风险但 PRD 未披露时，最多只能给 `CONDITIONAL_PASS`。
- **I1 架构可行性假设**：若 I1 中任何未决项或假设涉及架构可行性（如外部系统能力假设、容量假设、集成模式假设、部署约束假设），必须在 `required_prd_actions` 中标记为"设计前必须闭合"，且在闭合前 `gate_result` 不得为 `PASS`。
- **F2 容量预估底线**：若 F2 得分 <= 1，必须在 `design_stage_notes` 中强制声明"当前 PRD 未提供有效容量假设，架构设计必须基于明确容量假设进行，否则设计结果不可作为最终方案"。

### 6. 输出工作流状态

必须根据 Gate 结论输出 `workflow_transition`：

| gate_result | workflow_transition | 含义 |
| --- | --- | --- |
| PASS | ENTER_SYSTEM_DESIGN | 允许进入系统设计阶段 |
| CONDITIONAL_PASS | ENTER_SYSTEM_DESIGN_WITH_ACTIONS | 可进入系统设计，但必须跟踪补齐项 |
| FAIL | RETURN_TO_PRD_REWORK | 打回 PRD 补充，不进入系统设计 |

如果输入不足以评分，使用：

```json
{
  "gate_result": "FAIL",
  "workflow_transition": "RETURN_TO_PRD_REWORK"
}
```

### 7. 必须输出评审结果

无论 PRD 是否完整，最终都必须输出结构化评审结果。不得只输出自然语言总结。

最小必填字段：

```json
{
  "review_type": "PRD_DESIGN_READINESS_REVIEW",
  "review_mode": "FULL_REVIEW",
  "reviewer_role": "Senior System Architect",
  "gate_result": "FAIL",
  "workflow_transition": "RETURN_TO_PRD_REWORK",
  "checklist_used": false,
  "checklist_reference": "references/checklist.md",
  "checklist_items_evaluated": [],
  "missing_checklist_items": [],
  "final_score": 0,
  "blocker_avg_score": 0,
  "failed_blockers": [],
  "review_process_issues": [],
  "required_prd_actions": [],
  "design_stage_notes": [],
  "summary": ""
}
```

完整输出结构：

```json
{
  "review_type": "PRD_DESIGN_READINESS_REVIEW",
  "review_mode": "FULL_REVIEW",
  "reviewer_role": "Senior System Architect",
  "gate_result": "CONDITIONAL_PASS",
  "workflow_transition": "ENTER_SYSTEM_DESIGN_WITH_ACTIONS",
  "checklist_used": true,
  "checklist_reference": "references/checklist.md",
  "checklist_version": "prd-design-readiness-review/references/checklist.md",
  "checklist_items_total": 32,
  "checklist_items_evaluated": [
    "A1", "A2", "A3",
    "B1", "B2",
    "C1", "C2", "C3", "C4",
    "D1", "D2", "D3",
    "E1", "E2", "E3",
    "F1", "F2", "F3", "F4",
    "G1", "G2", "G3", "G4",
    "H1", "H2", "H3",
    "I1", "I2", "I3", "I4",
    "J1"
  ],
  "missing_checklist_items": [],
  "final_score": 78.6,
  "blocker_avg_score": 3.8,
  "applicable_items": 28,
  "not_applicable_items": [
    {
      "item": "J2",
      "reason": "当前系统无人工补救流程，且主流程可完全自动闭环。"
    }
  ],
  "summary": "PRD 主流程和核心对象基本明确，但异常流程、容量假设和外部依赖失败后的业务期望不足。",
  "failed_blockers": [
    {
      "item": "C2",
      "title": "是否定义关键异常流程",
      "score": 2,
      "missing_fields": ["business_expected_result", "manual_or_auto_handling"],
      "reason": "PRD 仅说明失败提示，未说明异常后的业务状态和处理责任。",
      "required_action": "补充核心异常场景、业务期望结果、用户可见结果和处理责任。"
    }
  ],
  "major_issues": [
    {
      "item": "F2",
      "title": "是否提供容量与增长预估",
      "score": 2,
      "risk": "无法进行容量规划和资源估算。",
      "recommendation": "补充用户量、业务量、数据量或峰值区间假设。"
    }
  ],
  "minor_issues": [],
  "item_scores": [
    {
      "item": "A1",
      "level": "BLOCKER",
      "weight": 3,
      "score": 4,
      "weighted_score": 12,
      "max_weighted_score": 15,
      "required_fields_coverage": 0.75,
      "evidence": ["PRD 描述了业务问题、目标和预期收益。"]
    }
  ],
  "missing_fields_summary": [
    "关键异常流程的业务结果",
    "容量和峰值假设",
    "外部依赖失败时的处理口径"
  ],
  "required_prd_actions": [
    "补充支付成功但订单确认失败的业务处理结果。",
    "补充首年用户量、日业务量和峰值估算区间。"
  ],
  "review_process_issues": [],
  "design_stage_notes": [
    "接口字段、重试策略、幂等键、存储模型应在系统设计阶段展开，不作为 PRD 准入硬性要求。"
  ]
}
```

## 核心 Blocker

以下项任一得分 <= 2，必须输出 `FAIL`：

| 编号 | 检查项 |
| --- | --- |
| A1 | 业务目标 |
| A3 | 项目范围 |
| B1 | 核心用户与角色 |
| C1 | 主流程 |
| C2 | 关键异常流程 |
| C3 | 核心状态流转 |
| D1 | 核心业务规则 |
| E1 | 核心业务对象 |
| G1 | 外部依赖 |
| G3 | 外部依赖失败时的业务期望 |
| H1 | 核心验收标准 |
| I1 | 未决项和假设条件 |

## 常见错误

| 错误 | 修正 |
| --- | --- |
| 只给“可以/不可以”的自然语言结论 | 必须输出结构化 JSON |
| 未读取 `references/checklist.md` 就给 PASS | 必须输出 FAIL，或先读取清单后重新评审 |
| 完整评审没有覆盖所有适用项 | 不得输出 PASS，必须列出 `missing_checklist_items` |
| 快速预审冒充完整评审 | `review_mode` 必须标记为 `QUICK_BLOCKER_REVIEW` |
| 把接口字段、存储模型、重试策略当作 PRD 缺陷 | 放入 `design_stage_notes` |
| 忽略集成模式与实时性要求对架构的影响 | 按 G4 评分并输出架构影响说明 |
| I1 假设涉及架构可行性却未标记"设计前必须闭合" | 按附加规则拦截，不得输出 PASS |
| F2 容量假设仅有形容词未触发声明 | 必须输出 capacity-assumption 强制声明 |
| PRD 只出现关键词就给高分 | 按 required_fields 和证据评分 |
| 遇到信息缺失就停止评审 | 输出 FAIL 和补齐动作 |
| 对缺失信息进行合理化推断 | 没有证据按缺失处理 |
| 忽略工作流状态 | 必须输出 `workflow_transition` |

## 快速执行提示

评审 PRD 时，按以下提示自检：

```text
我正在执行 PRD 设计准入评审。
我必须以系统架构师身份工作。
完整评审前，我必须读取 references/checklist.md。
我必须使用量化评分。
我必须输出 checklist_used、checklist_items_evaluated 和 missing_checklist_items。
我必须输出 gate_result 和 workflow_transition。
我必须区分 PRD 必须补充的问题与系统设计阶段展开的问题。
即使 PRD 不完整，我也必须输出结构化评审结果。
我必须检查 G4 集成模式与实时性要求。
我必须检查 I1 中涉及架构可行性的假设并标记为"设计前必须闭合"。
我必须在 F2 得分 <= 1 时输出容量假设强制声明。
```

## 验收标准

1. 必须读取 `references/checklist.md` 并输出 `checklist_used=true`。
2. 必须覆盖所有适用检查项，`missing_checklist_items` 为空时才能输出 `PASS`。
3. 必须输出结构化 JSON（`gate_result`、`workflow_transition`、`final_score`、`blocker_avg_score` 等）。
4. 必须区分 PRD 缺陷与 `design_stage_notes`（系统设计阶段展开内容）。
5. `evidence/{review_task_id}/` 目录非空，至少包含 1 份过程证据文件（checklist 逐项评分依据、Blocker/Major/Minor 判定过程、设计前必须闭合项识别过程）。
