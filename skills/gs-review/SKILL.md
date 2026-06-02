---
name: gs-review
description: 阶段汇总评审共享服务 SKILL，在 GS-Quality-Check 通过后统一执行 requirements、architecture、detailed_design 阶段评审门，产出正式评审报告、返工结论和运行时回写结果。
version: 1.3.0
---

# GS-Review 阶段汇总评审 SKILL

说明：角色边界见 [references/role-definition.md](references/role-definition.md)，执行细则见 [references/execution-details.md](references/execution-details.md)。

## 1. 元信息与执行契约

### 1.1 基本信息

| 项目 | 内容 |
|---|---|
| skill_id | `GS-Review` |
| skill_type | `shared_service` |
| 适用阶段 | `requirements`、`architecture`、`detailed_design` |
| 触发方式 | 当前阶段正式文档包完成，且 `GS-Quality-Check` 输出为 `pass` 或 `pass_with_warning` 后触发 |
| 输出主文档 | `artifacts/reviews/001-requirements-review.md` / `artifacts/reviews/002-architecture-review.md` / `artifacts/reviews/003-detailed-design-review.md` |
| 上游依赖 | `GS-Quality-Check` |
| 下游作用 | 形成阶段评审门结论，决定交接或返工 |
| 运行时主锚点 | 当前阶段 `000-task-tracker.md` |

### 1.2 任务映射

| stage | review_task_id | quality_task_id | caller_skill | review_gate | report_path |
|---|---|---|---|---|---|
| `requirements` | `RA-07` | `RA-06` | `G100` | `RG-requirements` | `artifacts/reviews/001-requirements-review.md` |
| `architecture` | `AD-08` | `AD-07` | `G200` | `RG-architecture` | `artifacts/reviews/002-architecture-review.md` |
| `detailed_design` | `DD-09` | `DD-08` | `G300` | `RG-detailed-design` | `artifacts/reviews/003-detailed-design-review.md` |

### 1.3 目标

1. 统一消费 `GS-Quality-Check` 的正式结果，避免阶段入口绕过质量门直接形成评审结论。
2. 对阶段正式文档包形成一次汇总评审，而不是拆成多个单文档独立用户评审。
3. 输出可机读 `review_summary`、`blocking_issues`、`rework_actions`、`consumed_quality_gate` 与 `evidence`。
4. 为阶段入口提供可验收的 `decision`、`pass_rate`、返工说明和报告路径。
5. 在子代理执行完成后完成验收、台账回写、关闭子代理与恢复闭环。

## 2. 输入契约

### 2.1 最小输入

```yaml
gs_review_input:
  stage: [requirements, architecture, detailed_design]
  review_task_id: string
  tracker_path: string
  stage_documents:
    - path: string
      required: boolean
      document_role: [stage_output, review_report, skill_contract]
  quality_gate_ref:
    task_id: string
    overall_status: [pass, pass_with_warning]
    issue_count:
      critical: integer
      major: integer
      minor: integer
      warning: integer
    issues:
      - issue_id: string
        checker: string
        severity: [critical, major, minor, warning]
        owner_document: string
        message: string
        evidence_ref: string
    evidence:
      report_path: string
  acceptance_threshold:
    min_pass_rate: number
    min_decision: [pass]
```

### 2.2 可选扩展输入

```yaml
gs_review_optional_input:
  review_report_path: string
  review_gate: string
  quality_gate_ref:
    checked_documents:
      - string
    failed_documents:
      - string
    evidence:
      tracker_path: string
  stage_summary:
    final_mode: [fast, standard, complete]
    handoff_target: string
  existing_review_report: string
```

### 2.3 归一化映射

`GS-Review` 只接收 `quality_gate_ref` 这一种固定输入形态。来自 `GS-Quality-Check` 的正式输出在进入本技能前，必须按下表归一化：

| GS-Quality-Check 输出字段 | GS-Review 固定输入字段 |
|---|---|
| `quality_task_id` | `quality_gate_ref.task_id` |
| `quality_check_summary.overall_status` | `quality_gate_ref.overall_status` |
| `validation_summary.issue_count` | `quality_gate_ref.issue_count` |
| `issues` | `quality_gate_ref.issues` |
| `evidence.report_path` | `quality_gate_ref.evidence.report_path` |
| `validation_summary.checked_documents` | `quality_gate_ref.checked_documents` |
| `validation_summary.failed_documents` | `quality_gate_ref.failed_documents` |
| `evidence.tracker_path` | `quality_gate_ref.evidence.tracker_path` |

### 2.4 输入约束

1. `quality_gate_ref.overall_status` 只允许 `pass` 或 `pass_with_warning`；若为 `fail` 或缺失，当前任务必须转 `blocked`。
2. `quality_gate_ref` 的最小必需消费字段固定为：
   - `task_id`
   - `overall_status`
   - `issue_count`
   - `issues`
   - `evidence.report_path`
3. `checked_documents`、`failed_documents`、`quality_gate_ref.evidence.tracker_path` 属于可选扩展字段，不得作为启动前置硬依赖。
4. `review_report_path` 若未显式提供，必须按阶段映射自动推导，禁止使用 `{stage}-review.md` 这类动态命名。
5. `tracker_path` 必须是当前阶段运行时台账路径；恢复时也只以该路径为锚点。
6. `stage_documents` 必须覆盖当前阶段正式文档包；缺任何 `required=true` 文档时，当前任务必须转 `blocked` 或 `rework`，不得直接 `pass`。
7. 调用方不得把 `quality_check_summary`、`validation_summary` 直接作为并列输入传入本技能；若来源是 `GS-Quality-Check` 原始输出，必须先归一化到 `quality_gate_ref`。

## 3. 输出契约

### 3.1 正式输出

```yaml
gs_review_output:
  stage: [requirements, architecture, detailed_design]
  review_task_id: string
  review_summary:
    decision: [pass, fail, pending]
    gate_decision: [pass, rework, blocked]
    pass_rate: number
    reviewed_items: integer
    passed_items: integer
    failed_items: integer
    rework_items: integer
    blocked_items: integer
    quality_gate_status: [pass, pass_with_warning]
  blocking_issues:
    - issue_id: string
      severity: [critical, major, minor, warning]
      owner_task_id: string
      owner_document: string
      message: string
      source: [quality_gate, stage_review]
  rework_actions:
    - action_id: string
      owner_task_id: string
      target_document: string
      action: string
      source_issue_ids:
        - string
  quality_issue_disposition:
    - issue_id: string
      disposition: [accepted, closed, rework_required, blocked]
      closure_note: string
      closure_evidence: string
  consumed_quality_gate:
    task_id: string
    overall_status: [pass, pass_with_warning]
    issue_count:
      critical: integer
      major: integer
      minor: integer
      warning: integer
    issues:
      - issue_id: string
    evidence:
      report_path: string
    optional_extensions:
      checked_documents:
        - string
      failed_documents:
        - string
      tracker_path: string
  evidence:
    report_path: string
    reviewed_document_paths:
      - string
    tracker_path: string
  execution_status:
    acceptance_status: [pending, passed, failed]
    close_status: [pending, closed]
  updated_at: string
```

### 3.2 输出约束

1. `review_summary.decision=pass` 的必要条件：
   - `pass_rate >= acceptance_threshold.min_pass_rate`
   - 无 `critical`、`major` 阻塞问题
   - 当前阶段正式文档包已齐备
2. `review_summary.decision=fail` 适用于：
   - `minor`/`warning` 问题需要返工后重审
   - 评审发现新增非阻塞问题，但不足以直接 `blocked`
3. `review_summary.decision=pending` 适用于：
   - 输入缺失或路径非法
   - 质量门结果非法
   - 当前阶段正式文档包不完整且无法继续评审
4. `review_summary.gate_decision` 与阶段入口消费口径的对应关系固定为：
   - `pass -> pass`
   - `rework -> fail`
   - `blocked -> pending`
5. `review_summary.failed_items = review_summary.rework_items + review_summary.blocked_items`。
6. `quality_issue_disposition` 必须覆盖所有由 `quality_gate_ref.issues` 引入的质量门问题。
7. 当 `quality_gate_ref.overall_status=pass_with_warning` 且最终 `review_summary.decision=pass` 时，所有 `quality_issue_disposition.disposition` 只能是 `accepted` 或 `closed`。
8. 任一 `quality_issue_disposition.disposition=rework_required` 的问题，必须至少出现在一条 `rework_actions.source_issue_ids` 中。
9. 任一 `quality_issue_disposition.disposition=blocked` 的问题，必须至少出现在一条 `blocking_issues.issue_id` 中。
10. `consumed_quality_gate` 必须原样保留质量门最小消费字段，包括 `task_id`；可选扩展字段存在时可补入，但不得替代最小字段。
11. `evidence.report_path` 必须与阶段固定输出路径一致：
   - `requirements -> artifacts/reviews/001-requirements-review.md`
   - `architecture -> artifacts/reviews/002-architecture-review.md`
   - `detailed_design -> artifacts/reviews/003-detailed-design-review.md`
12. `evidence.tracker_path` 必须等于当前阶段 `000-task-tracker.md` 路径。
13. `execution_status.acceptance_status` 与 `execution_status.close_status` 必须反映本轮子代理验收和关闭结果。

## 4. 门禁与返工规则

### 4.1 门禁前提

1. `GS-Quality-Check` 未通过时不得启动本技能。
2. `pass_with_warning` 可以进入评审门，但必须显式消费 `issues`，不得忽略质量门问题。
3. 评审门只接受“阶段汇总评审”语义，不接受单文档独立用户评审任务替代。

### 4.2 返工闭环

1. 当 `review_summary.gate_decision=rework` 时，必须输出 `rework_actions` 与 `quality_issue_disposition`；`blocking_issues` 非必填。
2. 当 `review_summary.gate_decision=blocked` 时，必须输出 `blocking_issues` 与 `quality_issue_disposition`。
3. `rework_actions.owner_task_id` 必须指向当前阶段入口任务位或具体下游 SKILL 任务位，不能只写抽象说明。
4. 返工完成后必须重新经过 `GS-Quality-Check`，不得绕过质量门直接重开 `GS-Review`。
5. 同一阶段可多轮进入 `GS-Review`，但每轮都必须形成新的正式评审报告并覆盖当前结论。

## 5. 子代理执行与关闭规则

### 5.1 子代理启动

1. `GS-Review` 必须由独立子代理执行。
2. 单个子代理一次只执行一个 `review_task_id`。
3. 启动时必须显式绑定：
   - `stage`
   - `review_task_id`
   - `tracker_path`
   - `review_report_path`（可自动推导后回填）
   - `stage_documents`
   - `quality_gate_ref`
   - `acceptance_threshold`
   - 必检输出字段
   - 验收要求

### 5.2 子代理验收

1. 验收前必须确认正式评审报告已写入固定路径。
2. 必须确认 `review_summary`、`rework_actions`、`quality_issue_disposition`、`consumed_quality_gate`、`evidence.report_path`、`updated_at` 完整；`gate_decision=blocked` 时还必须确认 `blocking_issues` 完整。
3. `pass_with_warning` 输入下，必须确认质量门 `issues` 已被显式消费；若最终无需返工，也必须通过 `quality_issue_disposition` 记录 `accepted` 或 `closed` 的处置结果。
4. 必须确认 `execution_status.acceptance_status=passed` 后，才能进入关闭步骤。

### 5.3 子代理关闭

1. 只有在正式报告写入、运行时台账回写完成、验收通过后，子代理才允许关闭。
2. 若验收不通过，子代理不得关闭，必须继续修订或明确阻塞原因。
3. 关闭前必须把最终结论同步给调用方任务位，并把 `execution_status.close_status=closed`。

## 6. 运行时台账回写与恢复

### 6.1 台账回写

1. 回写目标任务位固定为：
   - `requirements -> RA-07`
   - `architecture -> AD-08`
   - `detailed_design -> DD-09`
2. 必须更新：
   - `skill_stage`
   - `status_code`
   - `status_label`
   - `review_result`
   - `resume_from`
   - `updated_at`
3. `evidence_path` 由调用方按阶段既有台账习惯维护，本技能不强制把该字段改写为评审报告路径。
4. 正式评审报告路径统一记录在本技能输出的 `evidence.report_path`。

### 6.2 恢复规则

1. 中断恢复只以当前阶段 `000-task-tracker.md` 为主锚点。
2. 恢复时先读取 `stage`、`review_task_id`、`tracker_path` 与任务位状态，再按阶段映射推导 `review_report_path`。
3. 若已存在正式评审报告，则基于现有报告和台账继续验收；若不存在，则从评审执行步骤重新开始。
4. `template.md` 只作为实例化记录模板，不作为恢复硬依赖。
5. 若外部阶段入口尚未同步本技能新增字段，属于外部依赖，需在联调复评时单独核验。

## 7. 执行步骤

1. 读取并校验 `stage`、`review_task_id`、`tracker_path`、`stage_documents`、`quality_gate_ref`。
2. 推导或校验当前阶段固定 `review_report_path`。
3. 检查质量门前提是否满足，并确认 `issues` 是否完整可消费。
4. 对阶段正式文档包执行汇总评审，形成通过项、返工项、阻塞项。
5. 对每条质量门问题生成 `quality_issue_disposition`，明确 `accepted / closed / rework_required / blocked`。
6. 计算 `pass_rate`，生成 `review_summary`、`blocking_issues`、`rework_actions`、`consumed_quality_gate`。
7. 输出正式评审报告。
8. 回写运行时台账。
9. 验收通过后关闭子代理，并把结果交给阶段入口用于交接或返工。

## 8. 验收标准

1. 能正式消费 `GS-Quality-Check` 的最小字段：`task_id`、`overall_status`、`issue_count`、`issues`、`evidence.report_path`。
2. 可选扩展字段边界明确：`checked_documents`、`failed_documents`、`evidence.tracker_path` 为增强信息，不影响最小执行闭环。
3. 输入只保留 `quality_gate_ref` 固定归一化形态，不再并列暴露未映射的 `quality_check_summary / validation_summary`。
4. 输出模型能兼容 `G100/G200/G300` 模板的 `review_summary.decision=pass/fail/pending` 与 `failed_items` 消费口径。
5. 已明确返工闭环在运行时台账中的合法组合：返工用 `skill_stage=rework + status_code=in_progress`，阻塞才用 `status_code=blocked`。
6. 已明确 `pass_with_warning -> issues -> quality_issue_disposition / rework_actions` 的机读闭环。
7. `evidence/{review_task_id}/` 目录非空，至少包含 1 份过程证据文件（汇总评审维度检查记录、质量门问题处置过程、pass_rate 计算过程）。
