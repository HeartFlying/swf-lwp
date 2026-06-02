# G103 执行细则

## 1. 目标

补充 `G103` 的执行级约束，确保 MVP 范围定义具备可冻结、可验证、可交接属性。

## 2. 执行前检查

1. 确认 `RA-05` 已进入 `drafting` 并完成台账回写。
2. 校验 `003-requirements-baseline.md` 可解析 `FR/NFR/CST`、优先级和验收信息。
3. 若存在业务背景输入（`002`），用于辅助范围取舍，不可替代基线约束。
4. `evidence_path` 固定为 `evidence/RA-05/`，与 SKILL 与模板保持一致。

## 3. 边界收敛规则

1. **in-scope 必须覆盖基线中全部 `Must` 和全部 `Should` 需求，不可遗漏或排除任何 Must 或 Should。**
2. 每个 in-scope 条目必须可追溯到至少 1 个基线需求 ID。
3. Out-of-scope 条目必须有延后原因与触发回归条件；`Must` 和 `Should` 需求不得出现在 out-of-scope 中。
4. 发布门槛必须可判定，避免”描述性门槛”。
5. 架构关键输入摘要（模板第 7 章）中的依赖关系图必须覆盖所有 in-scope 功能。
6. NFR 约束分级必须从 G102 的 NFR 清单中提取，不得凭空新增未在基线中定义的 NFR。
7. 架构敏感风险必须是从风险清单（第 5 章）中筛选的子集，不得遗漏对架构有直接影响的风险项。

## 4. 编号与追溯规则

1. MVP 条目编号：`MVP-001` 起连续。
2. 验收标准编号：`AC-001` 起连续。
3. 风险编号：`R-001` 起连续。
4. 追溯矩阵必须覆盖 `MVP-ID -> 来源需求ID -> CST -> AC -> R`。

## 5. 质量检查闭环规则

1. 质量检查报告固定路径：`artifacts/reviews/requirements-quality-check.md`。
2. 最小字段：
   - `quality_check_summary.overall_status`
   - `quality_check_summary.scores.completeness`
   - `quality_check_summary.scores.traceability`
   - `quality_check_summary.scores.markdown_format`
   - `validation_summary.issue_count.critical`
   - `validation_summary.issue_count.major`
   - `validation_summary.issue_count.minor`
3. 缺失最小字段即不通过，不得推进到 `done`。
4. 通过判定必须同时满足：
   - `quality_check_summary.overall_status` 仅允许 `pass` 或 `pass_with_warning`
   - `validation_summary.issue_count.critical = 0`
   - `validation_summary.issue_count.major = 0`

## 6. 常见失败模式

1. in-scope/out-of-scope 没有明确边界依据，或 Must/Should 需求被遗漏/排除。
2. 候选功能有结论但无对应验收标准。
3. 风险只罗列不带缓解和状态。
4. 追溯矩阵缺少 `CST` 或 `AC` 映射。
5. 架构关键输入摘要遗漏跨功能强依赖，导致架构师低估耦合复杂度。
6. NFR 约束分级将所有 NFR 标记为硬约束，缺少软约束和降级口径。
7. 架构敏感风险仅原文照搬风险清单，未补充"设计阶段需闭合的假设"。

## 7. 方法论参考映射

中文方法名与 [requirements-methods-catalog.md](../../_shared/requirements-methods-catalog.md) 对齐：

| 中文方法名 | CSV technique_name | 用途 |
|---|---|---|
| 第一性原理 | `First Principles Thinking` | 识别最小必要功能与价值前提 |
| 问题风暴 | `Question Storming` | 先收敛问题再定范围 |
| 决策树 | `Decision Tree Mapping` | 明确取舍路径与结果 |
| 角色扮演 | `Role Playing` | 从多角色视角验证范围决策 |
| 约束映射 | `Constraint Mapping` | 把 `CST` 映射到边界与门槛 |
| 解决方案矩阵 | `Solution Matrix` | 价值/成本/风险平衡 |
| 六顶思考帽 | `Six Thinking Hats` | 多维复核边界与风险 |
| 假设反转 | `Assumption Reversal` | 反向验证延后项与边界假设 |
| 失败分析 | `Failure Analysis` | 定义阻断风险与缓解策略 |
| SCAMPER | `SCAMPER Method` | 生成可替代方案并优化门槛 |
| 类比思维 | `Analogical Thinking` | 通过同类案例补齐风险识别 |

步骤级执行产出要求（防止流于勾选）：

1. 步骤 1 需产出候选清单并标注每条条目的价值与可行性结论。
2. 步骤 2 需产出 in-scope/out-of-scope 边界表并标注 `CST` 依据。
3. 步骤 3 需产出整体验收标准 + 条目级 `AC` 清单。
4. 步骤 4 需产出三类风险并给出缓解与状态。
5. 步骤 5 需完成追溯矩阵与格式自检，并产出架构关键输入摘要（功能依赖关系、迭代优先级映射、NFR 约束分级、架构敏感风险）。

示例输出参考：`examples/sample-004-mvp-definition.md`。
