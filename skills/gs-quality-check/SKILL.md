---
name: gs-quality-check
description: 阶段质量检查共享服务 SKILL，用于在 requirements、architecture、detailed_design 阶段的正式文档包完成后执行统一质量门检查，输出可机读质量报告、问题清单和门禁结论，并作为 GS-Review 的前置条件。
version: 1.3.0
---

# GS-Quality-Check Shared Service SKILL

## 元信息与执行契约

### 基本信息

| 项目 | 内容 |
|---|---|
| skill_id | `GS-Quality-Check` |
| skill_type | `shared_service` |
| 中文名称 | 阶段质量检查共享服务 |
| 适用阶段 | `requirements`、`architecture`、`detailed_design` |
| 触发方式 | 阶段核心文档包完成后，由阶段入口 SKILL 以独立子代理触发 |
| 输出主文档 | `artifacts/reviews/{stage_report_name}-quality-check.md` |

### 执行契约摘要

| 项目 | 内容 |
|---|---|
| 运行时任务映射 | `requirements: RA-06`、`architecture: AD-07`、`detailed_design: DD-08` |
| 上游调用方 | `G100`、`G200`、`G300` |
| 下游门禁 | `GS-Review` |
| 必选输入 | `stage`、`quality_task_id`、`target_documents`、`tracker_path` |
| 按需输入 | `report_path`、`stage_summary`、`review_gate`、已有质量报告、当前阶段模板记录 |
| 关键引用 | `template.md`、`references/role-definition.md`、`references/execution-details.md`、`../_shared/governance/*.md`、`../g100-requirements-entry/SKILL.md`、`../g200-architecture-entry/SKILL.md`、`../g300-detailed-design-entry/SKILL.md` |

## 1. 目标

提供统一的阶段质量门能力，覆盖：

1. 校验阶段正式文档包是否达到进入评审门的最小质量阈值
2. 产出可机读 `quality_check_summary`、`validation_summary`、`issues`
3. 明确 `pass / pass_with_warning / fail` 门禁结论
4. 将结果稳定回写到阶段运行时台账与证据目录
5. 为 `GS-Review` 提供唯一可信的质量门输入

## 2. 前置条件

1. `stage` 仅允许 `requirements`、`architecture`、`detailed_design`。
2. 当前阶段的 `000-task-tracker.md` 必须存在且结构符合 [runtime-task-tracker-spec.md](../_shared/governance/runtime-task-tracker-spec.md)。
3. `target_documents` 必须指向当前阶段正式文档包，不得混入草稿目录或参考目录。
4. 调用方必须已经完成阶段核心文档起草，并将质量门任务置为 `in_progress`。
5. 检查器集合由服务内部根据文档角色和门禁场景自动推导，调用方不需要显式传入检查器配置。

## 3. 输入输出契约

### 3.0 阶段命名映射

```yaml
stage_path_mapping:
  requirements:
    tracker_dir: artifacts/requirements/
    report_name: requirements
  architecture:
    tracker_dir: artifacts/architecture/
    report_name: architecture
  detailed_design:
    tracker_dir: artifacts/detailed-design/
    report_name: detailed-design
```

约束：

1. `stage=detailed_design` 时，路径必须落到 `artifacts/detailed-design/`，报告命名必须为 `artifacts/reviews/detailed-design-quality-check.md`。
2. 若调用方未提供 `report_path`，服务必须按 `stage_path_mapping` 自动推导。
3. 若 `tracker_path` 或 `report_path` 与阶段映射不一致，当前执行必须转 `blocked`。

### 3.0.1 文档角色到最小检查器映射

```yaml
document_role_minimal_checkers:
  stage_output:
    - QC-001
    - QC-002
    - QC-003
    - QC-004
    - QC-005
    - QC-006
    - QC-007
  review_report:
    - QC-001
    - QC-002
    - QC-003
    - QC-004
    - QC-005
    - QC-010
  skill_contract:
    - QC-001
    - QC-002
    - QC-003
    - QC-004
    - QC-005
    - QC-006
    - QC-009
```

说明：

1. `stage_output` 用于当前阶段正式产物文档。
2. `review_report` 用于质量报告或其他评审类文档。
3. `skill_contract` 仅用于本技能自身文档或同类技能契约检查，不默认作用于阶段正式产物文档。

### 3.1 输入

```yaml
gs_quality_check_input:
  stage: [requirements, architecture, detailed_design]
  quality_task_id: string
  tracker_path: string
  report_path: string
  target_documents:
    - path: string
      required: boolean
      document_role: [stage_output, review_report, skill_contract]
  stage_summary:
    review_gate: string
    current_mode: [fast, standard, complete]
    caller_skill: [G100, G200, G300]
    handoff_target: [architecture, detailed_design, none]
```

输入约束：

1. `quality_task_id` 必须与阶段任务位对应：`RA-06`、`AD-07`、`DD-08`。
2. `tracker_path` 必须是当前阶段运行时台账路径。
3. `report_path` 若显式提供，必须位于 `artifacts/reviews/` 下；若未提供，由服务按阶段映射自动推导。
4. `target_documents.required=true` 的文档任一缺失，直接判定为 `fail`。
5. 服务必须按 [quality-checker-requirements.md](../_shared/governance/quality-checker-requirements.md) 与 `target_documents.document_role` 自动推导最小检查器集合。
6. `stage_output` 必须纳入 `QC-007`；`review_report` 必须纳入 `QC-010`。
7. `effective_checkers` 属于服务运行时产物，不属于调用输入字段。

### 3.2 输出

```yaml
gs_quality_check_output:
  stage: [requirements, architecture, detailed_design]
  quality_task_id: string
  quality_check_summary:
    overall_status: [pass, pass_with_warning, fail]
    scores:
      completeness: number
      markdown_format: number
      traceability: number
      consistency: number
    executed_checkers:
      - string
  validation_summary:
    issue_count:
      critical: integer
      major: integer
      minor: integer
      warning: integer
    checked_documents:
      - string
    failed_documents:
      - string
  issues:
    - issue_id: string
      checker: string
      severity: [critical, major, minor, warning]
      message: string
      evidence_ref: string
      owner_document: string
  evidence:
    report_path: string
    tracker_path: string
  updated_at: string
```

输出约束：

1. `critical > 0` 或 `major > 0` 时，`overall_status` 必须为 `fail`。
2. `critical = 0`、`major = 0` 且 (`minor > 0` 或 `warning > 0`) 时，允许 `pass_with_warning`。
3. 所有问题必须带 `checker`、`severity`、`message`、`evidence_ref`。
4. 任一最小字段缺失视为 `fail`。
5. `GS-Review` 只允许消费 `pass` 或 `pass_with_warning` 的结果。
6. `template.md` 必须能实例化 `quality_check_summary.executed_checkers`、`validation_summary.checked_documents`、`validation_summary.failed_documents`、`issues`、`evidence.report_path`、`evidence.tracker_path` 与 `updated_at`。

### 3.3 与阶段门禁的关系

1. `requirements` 阶段：`RA-06` 通过后，才允许 `RA-07(GS-Review)` 启动。
2. `architecture` 阶段：`AD-07` 通过后，才允许 `AD-08(GS-Review)` 启动。
3. `detailed_design` 阶段：`DD-08` 通过后，才允许 `DD-09(GS-Review)` 启动。
4. 质量门失败时，阶段入口必须回写返工入口，不得继续推进交接。

### 3.4 与 GS-Review 的接口边界

`GS-Review` 不直接消费 `quality_check_summary`、`validation_summary`、`issues` 原始结构。来自本技能的输出必须先由阶段入口归一化为 `quality_gate_ref`，再作为 `GS-Review` 的唯一 canonical 输入。

归一化后的 `quality_gate_ref` 最小必需消费字段仅包括：

1. `quality_gate_ref.task_id`
2. `quality_gate_ref.overall_status`
3. `quality_gate_ref.issue_count`
4. `quality_gate_ref.issues`
5. `quality_gate_ref.evidence.report_path`

`GS-Review` 可选扩展消费字段包括：

1. `quality_gate_ref.scores`
2. `quality_gate_ref.executed_checkers`
3. `quality_gate_ref.checked_documents`
4. `quality_gate_ref.failed_documents`
5. `quality_gate_ref.evidence.tracker_path`
6. `quality_gate_ref.updated_at`

说明：

1. 归一化映射固定为：`quality_task_id -> quality_gate_ref.task_id`、`quality_check_summary.overall_status -> quality_gate_ref.overall_status`、`validation_summary.issue_count -> quality_gate_ref.issue_count`、`issues -> quality_gate_ref.issues`、`evidence.report_path -> quality_gate_ref.evidence.report_path`。
2. 本技能不要求 `GS-Review` 在当前阶段必须消费全部扩展字段。
3. 若 `GS-Review` 尚未声明扩展字段契约，这些字段仍作为本技能完整输出保留。

## 4. 决策与执行规则

### 4.1 检查器选择规则

1. 阶段入口 SKILL 传入的 `target_documents` 决定当前质量门的检查范围。
2. 服务必须基于 `document_role_minimal_checkers` 自动生成 `effective_checkers`。
3. `stage_output` 文档默认跑 `QC-001 ~ QC-007`。
4. `review_report` 文档默认跑 `QC-001 ~ QC-005` 与 `QC-010`。
5. `skill_contract` 文档默认跑 `QC-001 ~ QC-006` 与 `QC-009`。

### 4.2 门禁判定规则

1. `critical > 0` 或 `major > 0`，直接 `fail`。
2. `critical = 0`、`major = 0`、(`minor > 0` 或 `warning > 0`) 时，统一判为 `pass_with_warning`，且问题必须进入评审输入。
3. `critical = 0`、`major = 0`、`minor = 0`、`warning = 0` 时，判为 `pass`。
4. `overall_status = fail` 时，不得启动 `GS-Review`。
5. `overall_status in [pass, pass_with_warning]` 时，才允许进入评审门。

### 4.3 子代理执行与关闭规则

1. `GS-Quality-Check` 必须由阶段入口 SKILL 通过独立子代理启动。
2. 一个子代理一次只执行一个质量门任务，不得并发多个阶段或多个服务。
3. 子代理启动时必须显式绑定：`stage`、`quality_task_id`、`tracker_path`、`report_path`（可自动推导后回填）、`target_documents`、验收要求。
4. 子代理生成质量报告后，必须先完成结果验收、台账回写和证据路径确认，再关闭该子代理。
5. 若验收失败，子代理不得直接关闭，必须继续修复或明确转入 `blocked/rework`。

## 5. 执行步骤

### 步骤 1：建立质量门执行上下文

- 读取 `stage`、`quality_task_id`、`tracker_path`
- 按阶段映射推导或校验 `report_path`
- 校验阶段任务位是否匹配 `RA-06/AD-07/DD-08`
- 校验 `target_documents` 是否完整，并推导 `effective_checkers`
- 若任一关键输入缺失，直接标记 `fail`

### 步骤 2：执行最小检查器集合

- 对所有 `required=true` 文档执行按文档角色自动推导出的最小检查器集合
- 记录每个检查器的执行结果、分值与问题证据

### 步骤 3：汇总质量结论

- 生成 `quality_check_summary`
- 生成 `validation_summary`
- 汇总 `issues`
- 形成统一质量报告 `artifacts/reviews/{stage_report_name}-quality-check.md`

### 步骤 4：回写运行时台账

- 将对应任务位更新为：
  - 通过：`status_code=done`、`status_label=完成`、`skill_stage=quality_check`
  - 失败：`status_code=in_progress` 或 `blocked`，并写明返工/阻塞原因
- 更新 `review_result`、`resume_from`、`evidence_path`、`updated_at`
- `evidence.report_path` 统一记录质量报告路径；`evidence.tracker_path` 仅保留在服务输出中
- tracker 任务位中的 `evidence_path` 不强制改写为质量报告文件路径，可由调用方保持既有值，或写入其阶段既有证据目录

### 步骤 5：向下游评审门交付结果

- 若 `overall_status in [pass, pass_with_warning]`，先由阶段入口将本技能输出归一化为 `quality_gate_ref`，再把 `quality_gate_ref` 交给 `GS-Review`
- 若 `overall_status = fail`，明确返工入口与需修复问题，不得推进评审门

## 6. 与运行时台账对齐

1. `GS-Quality-Check` 不新增独立阶段任务号，只消费既有质量门任务位：`RA-06/AD-07/DD-08`。
2. 任务回写字段必须对齐：
   - `task_id`
   - `skill_id`
   - `skill_stage`
   - `step_name`
   - `description`
   - `inputs`
   - `outputs`
   - `dependencies`
   - `status_code`
   - `status_label`
   - `review_result`
   - `resume_from`
   - `evidence_path`
   - `updated_at`
3. `skill_stage` 仅允许使用共享治理定义的合法枚举，不得自造状态。
4. `evidence_path` 由调用方按阶段既有台账习惯维护，本技能只要求其能稳定指向本轮质量门的证据目录或既有证据入口，不要求强制等于质量报告文件路径。
5. 质量报告文件路径统一放在 `evidence.report_path`。
6. 质量门失败时，`resume_from` 必须写明下一步返工入口或补齐条件。

## 7. 验收标准

1. 能基于阶段文档包输出完整质量报告。
2. 能稳定产出 `quality_check_summary`、`validation_summary`、`issues`。
3. 能明确 `pass / pass_with_warning / fail`，并与问题级别一致。
4. 能与 `G100/G200/G300` 的质量门任务位和门禁顺序一致。
5. 能将结果回写到阶段台账并形成恢复入口。
6. 能在子代理执行完成后给出明确的验收与关闭条件。
7. `evidence/{quality_task_id}/` 目录非空，至少包含 1 份过程证据文件（检查器执行详细记录、评分过程和阈值依据、问题识别过程）。

## 8. 失败与恢复

1. 若关键输入缺失，标记 `blocked` 或 `fail`，并写明补齐条件。
2. 若报告写入失败或证据路径不可用，保持任务 `in_progress` 并进入返工。
3. 若阶段正式文档包未准备完成，不得伪造通过结论。
4. 恢复时仅以当前阶段 `000-task-tracker.md` 作为唯一运行时前置依赖；质量报告路径和本地 `template.md` 只作为辅助证据，不得作为恢复前置条件。

## 9. References

1. [template.md](template.md)
2. [execution-details.md](references/execution-details.md)
3. [runtime-task-tracker-spec.md](../_shared/governance/runtime-task-tracker-spec.md)
4. [quality-checker-requirements.md](../_shared/governance/quality-checker-requirements.md)
5. [G100 SKILL.md](../g100-requirements-entry/SKILL.md)
6. [G200 SKILL.md](../g200-architecture-entry/SKILL.md)
7. [G300 SKILL.md](../g300-detailed-design-entry/SKILL.md)
