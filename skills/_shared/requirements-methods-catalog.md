# Requirements Methods Catalog

说明：

1. 本文档沉淀 requirements 阶段的标准方法目录，供 `G100`、`G101`、`G102`、`G103` 统一引用。
2. 目录主体优先整理自 `skills/_shared/brain-methods.csv` 中可直接服务 requirements 阶段的方法；对当前 requirements 正式 SKILL 已采用但不在 CSV 中的方法，补充项目内扩展定义，确保执行时只有一个统一引用源。
3. `G100~G103` 中出现的方法名，应以本目录为唯一标准引用来源；具体在哪个步骤使用，以各 SKILL 的 `SKILL.md`、`template.md` 和 `references/execution-details.md` 为准。

| category | technique_name | applicable_skill | source | description |
|---|---|---|---|---|
| requirements_entry | 第一性原理 | `G100`、`G101`、`G102`、`G103` | `brain-methods.csv / First Principles Thinking` | 将事实、假设、推导和不确定项拆开，避免在需求阶段直接把经验判断写成结论。 |
| requirements_entry | 问题风暴 | `G100`、`G101`、`G102`、`G103` | `brain-methods.csv / Question Storming` | 先生成关键问题清单，再决定需要澄清、分析或冻结的内容，避免过早收敛到单一路径。 |
| requirements_entry | 约束映射 | `G100`、`G101`、`G102`、`G103` | `brain-methods.csv / Constraint Mapping` | 从业务、资源、时间、技术、合规等维度识别限制条件，并区分真实约束与可突破边界。 |
| requirements_entry | 思维导图 | `G100`、`G101`、`G102` | `brain-methods.csv / Mind Mapping` | 用树状结构整理问题域、需求分组或市场因素，减少遗漏并帮助后续结构化归并。 |
| business_context | 角色扮演 | `G101`、`G102`、`G103` | `brain-methods.csv / Role Playing` | 从用户、业务、运营、技术或竞品等不同视角验证结论，避免只保留单一角色立场。 |
| business_context | 决策树 | `G101`、`G102`、`G103` | `brain-methods.csv / Decision Tree Mapping` | 将关键取舍条件、分支路径和结果显式展开，支撑需求优先级、MVP 范围和竞品策略判断。 |
| business_context | 特征迁移 | `G101`、`G102` | `brain-methods.csv / Trait Transfer` | 从成熟产品或相邻领域提炼可借鉴特征，再判断哪些能力适合迁入当前需求背景。 |
| business_context | 类比思维 | `G101`、`G102`、`G103` | `brain-methods.csv / Analogical Thinking` | 通过同类产品、相邻行业或历史案例寻找可比对象，辅助补齐风险、约束或机会判断。 |
| business_context | 用户旅程图 | `G101`、`G102` | `project-extension` | 按用户目标、触点、行为和阻塞点展开关键场景，帮助定位痛点来源并验证需求覆盖范围。 |
| business_context | 五问法（5 Whys） | `G101`、`G102` | `project-extension` | 对高优先级痛点或约束持续追问根因，避免把症状误当成真正的问题定义。 |
| requirements_baseline | 失败分析 | `G101`、`G102`、`G103` | `brain-methods.csv / Failure Analysis` | 从失败案例、缺陷模式和不可接受结果反推应纳入的需求、验收和风险控制。 |
| requirements_baseline | 假设反转 | `G101`、`G102`、`G103` | `brain-methods.csv / Assumption Reversal` | 对当前假设或边界做反向验证，识别伪约束、隐藏风险或延后项的触发条件。 |
| requirements_baseline | 解决方案矩阵 | `G101`、`G102`、`G103` | `brain-methods.csv / Solution Matrix` | 将价值、成本、风险、验收和依赖映射到统一矩阵，用于需求收敛、范围判定和追溯检查。 |
| requirements_baseline | 六顶思考帽 | `G101`、`G102`、`G103` | `brain-methods.csv / Six Thinking Hats` | 从事实、收益、风险、创意、情感和过程六个维度复核需求、MVP 和业务背景结论。 |
| requirements_baseline | SCAMPER | `G101`、`G102`、`G103` | `brain-methods.csv / SCAMPER Method` | 在已形成基线后补充替代、组合、删减或简化方案，帮助产生更可执行的改进路径。 |

## 使用建议

1. `G100` 作为入口编排 SKILL，不直接执行深度业务分析，但在模式判定、澄清与下游路由时，应将本目录作为 requirements 阶段方法边界的统一来源。
2. `G101` 优先使用 `business_context` 与 `requirements_baseline` 类方法，侧重市场、竞品、痛点和机会收敛。
3. `G102` 优先使用 `requirements_baseline` 类方法，侧重需求基线冻结、约束分层、优先级和验收追溯。
4. `G103` 优先使用 `requirements_baseline` 类方法，侧重 MVP 范围、范围边界、发布门槛和风险收敛。
5. 如果某方法被写入步骤、模板或执行细则，应使用本目录中的标准名称，不使用同义词、英文别名或临时命名。
