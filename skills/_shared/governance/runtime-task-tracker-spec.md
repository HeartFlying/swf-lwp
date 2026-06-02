# 运行时阶段任务跟踪规范

## 1. 目标

本规范定义各阶段在运行时必须维护的 `000-task-tracker.md` 文件格式、状态字段、更新时机和恢复流程。

本规范适用于：

1. `artifacts/requirements/000-task-tracker.md`
2. `artifacts/architecture/000-task-tracker.md`
3. `artifacts/detailed-design/000-task-tracker.md`

## 2. 路径与作用域

### 2.1 路径基准

所有运行时路径均以执行时项目根目录为基准。

### 2.2 固定文件路径

| stage | 运行时任务文件 |
|---|---|
| `requirements` | `artifacts/requirements/000-task-tracker.md` |
| `architecture` | `artifacts/architecture/000-task-tracker.md` |
| `detailed_design` | `artifacts/detailed-design/000-task-tracker.md` |

### 2.3 文件作用

运行时任务文件用于记录：

1. 当前阶段内的任务清单
2. 每个任务的执行状态
3. 中断恢复点
4. 证据路径与产物引用
5. 阶段完成后移交下游阶段的最小上下文

## 3. 固定文档结构

每个 `000-task-tracker.md` 必须包含以下一级章节：

1. `# {阶段名称}任务跟踪`
2. `## 1. 阶段信息`
3. `## 2. 状态说明`
4. `## 3. 任务清单与状态跟踪`
5. `## 4. 更新规则`
6. `## 5. 阶段交接记录`

## 4. 阶段信息结构

`## 1. 阶段信息` 必须使用固定表格：

| 项目 | 内容 |
|---|---|
| 阶段 | `{requirements/architecture/detailed_design}` |
| 入口技能 | `{G100/G200/G300 或当前阶段入口}` |
| 当前模式 | `{fast/standard/complete}` |
| 当前状态 | `{执行中/已完成/阻塞}` |
| 当前主文档 | `{当前正在产出的正式文档路径}` |
| 最后更新 | `YYYY-MM-DD` |

## 5. 任务清单字段

`## 3. 任务清单与状态跟踪` 必须使用固定表头：

| task_id | skill_id | skill_stage | step_name | description | inputs | outputs | dependencies | status_code | status_label | review_result | resume_from | evidence_path | updated_at |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

### 5.1 `skill_stage` 枚举

允许值固定为：

1. `intake`
2. `clarification`
3. `planning`
4. `drafting`
5. `quality_check`
6. `user_review`
7. `rework`
8. `handoff`
9. `completed`

## 6. 更新流程

### 6.1 初始化

阶段启动时，当前阶段入口必须：

1. 创建对应的 `000-task-tracker.md`
2. 写入阶段信息
3. 预填全部任务
4. 将首个任务状态置为 `in_progress`

### 6.2 开始任务时

开始执行某任务前必须：

1. 将该任务更新为 `in_progress / 进行中`
2. 写明当前主文档路径
3. 初始化 `skill_stage`
4. 初始化 `resume_from`
5. 建立对应 `evidence_path`
6. 对于由子代理执行的任务（drafting / quality_check / user_review），`evidence_path` 指向的目录在任务完成后必须非空（至少包含 1 份过程证据文件）

### 6.3 任务执行中

遇到以下情况必须立即更新：

1. 进入用户评审等待：`skill_stage = user_review`
2. 需要返工：`skill_stage = rework`
3. 发生阻塞：改为 `blocked`
4. 切换当前主文档：同步更新阶段信息中的 `当前主文档`
5. 进入质量检查：`skill_stage = quality_check`

## 7. 恢复规则

当任务中断后，必须仅依赖 `000-task-tracker.md` 即可恢复。

`resume_from` 至少包含：

1. 已完成的最后动作
2. 当前待继续动作
3. 未完成的检查或评审
4. 缺失输入或待确认项

## 8. 阻塞记录规则

当任务进入 `blocked` 时：

1. `review_result` 写阻塞原因
2. `resume_from` 写解除条件和恢复入口
3. 阶段信息中的 `当前状态` 更新为 `阻塞`

## 9. 阶段交接记录

`## 5. 阶段交接记录` 必须使用固定表头：

| handoff_id | from_stage | to_stage | required_outputs | review_gate | status | notes | updated_at |
|---|---|---|---|---|---|---|---|

规则：

1. 阶段完成后必须新增一条交接记录。
2. `required_outputs` 必须引用已通过评审的正式文档。
3. `review_gate` 必须记录本阶段对应评审门是否通过。

## 10. 验收标准

本规范通过条件：

1. 已明确各阶段运行时任务文件路径。
2. 已定义固定章节、固定字段和状态枚举。
3. 已定义开始、执行中、评审后、阻塞和恢复的更新流程。
4. 已定义阶段交接记录结构。
