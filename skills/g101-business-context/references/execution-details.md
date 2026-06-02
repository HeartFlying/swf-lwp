# G101 执行细则（参考）

## 1. 适用范围

本细则用于指导 `G101` 在 `standard`、`complete` 模式下的具体落地，不替代 `SKILL.md` 的正式契约。

## 2. 数据与证据策略

1. 优先使用用户提供资料。
2. 无外部资料时可基于输入推导，但必须标记“推导结论/置信度”。
3. 所有关键判断必须给出依据或假设，避免无来源断言。

## 3. 输出建议粒度

1. 市场分析聚焦“是否值得做”和“约束条件”。
2. 竞品分析聚焦“差异化机会”和“不可忽略风险”。
3. 痛点识别聚焦“对需求基线冻结有直接影响”的问题。
4. 机会建议需可被 `G102` 直接消费。

## 3.1 方法目录基线

`G101` 的方法名、适用范围与最小说明统一引用：

- [requirements-methods-catalog.md](../../_shared/requirements-methods-catalog.md)

## 4. 与 RA 任务映射建议

1. 在 `RA-03` 执行时写入 `skill_stage=drafting`。
2. 文档自检通过后更新 `skill_stage=quality_check`。
3. 质量检查结果对 `G101` 调用方只以 `quality_gate_ref.*` 归一化字段回填，不写入 `review_result`，也不并列暴露 `quality_check_summary` / `validation_summary` 原始结构。
4. 质量检查报告固定路径为 `artifacts/reviews/requirements-quality-check.md`，缺少最小字段（`quality_gate_ref.overall_status`、`quality_gate_ref.scores.completeness`、`quality_gate_ref.scores.traceability`、`quality_gate_ref.scores.markdown_format`、`quality_gate_ref.issue_count.critical`、`quality_gate_ref.issue_count.major`、`quality_gate_ref.issue_count.minor`、`quality_gate_ref.issue_count.warning`、`quality_gate_ref.evidence.report_path`）视为不通过。
5. 提交评审前更新 `skill_stage=user_review`，`review_result=待用户评审`。
6. 用户通过后收口为 `skill_stage=completed` 且 `status_code=done`。

## 5. 常见失败场景

1. 只输出描述性文本，缺少可用于 G102 的结构化结论。
2. 竞品数量不足且未说明原因。
3. 未给出痛点优先级，导致后续无法冻结范围。
4. 路径格式混用 `\\` 与 `/`。
