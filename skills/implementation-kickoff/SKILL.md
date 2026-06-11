---
name: "implementation-kickoff"
description: "将设计阶段产出转化为研发启动策略文档（WHAT & WHY）。在用户提到'开始编码'、'进入研发'、'怎么落地'、'开工'、'研发启动'、'进入开发阶段'，或项目处于 design 完成后需推进到 code 阶段时触发。不生成可执行任务计划（HOW）。"
---

# 研发启动编排

## 不变量

1. **禁止跳过上游文档**：上游设计产物是唯一可信来源，禁止直接询问用户"有哪些模块"。
2. **禁止修改上游产出**：只读消费 `artifacts/implementation/` 和 `artifacts/requirements/`，不创建或修改设计定义文件。
3. **禁止产出含 TBD/TODO/placeholder 的策略文档**：交付物必须完整、可执行、无占位符。
4. **职责边界止于策略设计文档通过 review**：不生成任务计划、不定义检查点门槛、不执行编码。
5. **范围聚焦研发启动阶段**：不扩展到具体代码实现或部署上线。

## 预警基因

> 当模块数 < 8 时 → 检查是否可压缩为两轮启动 → 优先减少管理 overhead → 不能因此跳过骨架搭建。

> 当存在跨语言/跨部署域接口时 → 需要明确双 Owner 和契约委员会 → 优先锁定契约再编码 → 不能假设接口自然对齐。

> 当阻塞问题无法快速解决时 → 需要并行 POC/压测与编码 → 仅阻塞依赖它的特定模块 → 不能整体阻塞研发启动。

> 当上游文档缺失或不一致时 → 标记为中断并记录证据缺口 → 明确缺失文件和不一致位置 → 不能自行补全或假设。

## 极简执行流程

### Step 1: 消费上游交接产物
- 读取 `artifacts/implementation/`（g402 细化定义）和 `artifacts/requirements/`（g100 需求基线+MVP）
- 提取阻塞问题清单（critical/major）和模块就绪状态表
- 交叉验证 g402 与上游设计文档的一致性
- **输出**：`模块启动就绪状态表`、`阻塞问题清单`

### Step 2: 制定分层启动策略
- 按"骨架 → 核心链路 → 补齐联调"分轮次，参考 `references/layered-template.md`
- 标注并行 POC/压测轮次
- 绘制模块依赖图
- **输出**：`分层策略方向`、`模块依赖图`

### Step 3: 设计团队协作模式
- 选择治理深度（A/B/C），参考 `references/governance-models.md`
- 确定关键接口清单和 Owner 分配
- 制定契约委员会运行规则
- **输出**：`Owner 分配表`、`关键接口清单`、`委员会运行规则`

### Step 4: 确定工程基础设施
- 仓库策略，参考 `references/repo-structure.md`
- CI/CD 分层触发，参考 `references/ci-strategy.md`
- 测试框架选型，参考 `references/test-framework-guide.md`
- 数据库迁移策略，参考 `references/db-migration-rules.md`
- **输出**：`仓库结构图`、`CI 策略表`、`开发环境配置方案`、`测试框架选型表`、`数据库迁移规则`

### Step 5: 定义验收原则
- 量化原则、分层验收原则、阻塞清零原则、契约先行原则
- **输出**：`验收原则`（供 IPG 配置检查点时参考）

### Step 6: 风险与回退方案
- 针对阻塞问题和协作/工程风险，制定可执行的回退方案
- **输出**：`风险登记表`

### Step 7: 汇总为研发启动设计文档
- 整合 Step 1~6 产出，自检无 TBD、内部一致、范围聚焦、无歧义
- 保存至 `docs/superpowers/specs/YYYY-MM-DD-implementation-kickoff-design.md`
- 提交用户 review，确认后职责完成
- **下游交接**：明确指向 `implementation-plan-generation`

## 产出物清单

| 产出物 | 来源步骤 | 下游消费者 |
|--------|----------|-----------|
| 模块启动就绪状态表 | Step 1 | IPG |
| 阻塞问题清单 | Step 1 | IPG |
| 分层策略方向 | Step 2 | IPG |
| 模块依赖图 | Step 2 | IPG |
| Owner 分配表 | Step 3 | IPG |
| 关键接口清单 | Step 3 | IPG / 契约委员会 |
| 委员会运行规则 | Step 3 | 团队 |
| 仓库结构图 | Step 4 | 基础设施子计划 |
| CI 策略表 | Step 4 | 基础设施子计划 |
| 开发环境配置方案 | Step 4 | 基础设施子计划 |
| 测试框架选型表 | Step 4 | 基础设施子计划 |
| 数据库迁移规则 | Step 4 | 基础设施子计划 |
| 验收原则 | Step 5 | IPG（检查点配置） |
| 风险登记表 | Step 6 | IPG |
| 研发启动设计文档 | Step 7 | IPG / 用户 review |

## 职责边界

**本 skill 到此结束。完整管道**：
1. G401 技术实现定型 →
2. G402 设计细化 →
3. **本 skill**（消费 G402 制定策略）→
4. `implementation-plan-generation`（消费本文档生成计划体系）→
5. `infrastructure-bootstrapping`（消费 IPG 基础设施子计划）→
6. `layered-dev`（消费 IPG 主计划执行编码）

**不属于本 skill**：
- 转化为可执行任务计划 → `implementation-plan-generation`
- 定义具体检查点和合格门槛 → `implementation-plan-generation` Step 5
- 编写具体子计划 → `implementation-plan-generation`
- 执行编码 → `layered-dev` 或 `orchestrating-fresh-subagents`
- 设计漂移审计 → `design-drift-audit`
