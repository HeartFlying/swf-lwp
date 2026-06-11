---
name: implementation-plan-generation
description: >
  当项目已完成研发启动设计（implementation-kickoff 产出）或其他设计阶段产物、需要将设计转化为可执行的计划体系时使用。
  负责：消费上游 implementation-kickoff 设计产物（优先）或其他设计产物 → 提取8项信息基线 → 按组件类型拆分子计划 → 生成二维矩阵（交付特征×分层轮次） →
  为每个任务注入设计→需求追溯链 → 配置检查点 → 输出主计划+子计划+追踪文件+结构化证据JSON。
  触发场景："生成实施计划"、"拆分子计划"、"从设计到计划"、"create implementation plan"、
  "generate sub-plans"、"把设计转化为可执行计划"、"design to plan"。
  即使没有明确说"计划生成"，只要是"设计做完了怎么开始实现"或"怎么从设计过渡到编码"类的问题都应触发。
  本技能是"设计→计划"的转化层，上游优先消费 implementation-kickoff 设计文档，下游编排 superpowers:writing-plans 等功能引擎。
  计划体系产出后，由 infrastructure-bootstrapping 消费基础设施子计划，再由 layered-parallel-implementation 消费主计划执行编码。
---

# Implementation Plan Generation（实施计划生成）

## 目标

将上游设计产物中的策略决策转化为可执行的计划体系，确保：

1. 每个子计划有明确的类型、验收标准和执行引擎
2. 每个任务可反向追溯至关联的设计文档和需求条目
3. 子计划之间埋入质量检查点，不等到全部完成才发现问题
4. 追溯完整性是计划完成时的强制验收标准

---

## 不变量（硬边界，必须遵守）

以下规则不可协商、不可绕过。违反任一条均视为计划生成失败。

| # | 不变量 | 触发方式 |
|---|--------|----------|
| **I1** | 组件清单缺失或不完整 → **中断**，不可继续 | 步骤 1 缺口检测时验证 |
| **I2** | 每个 Task 必须有追溯链，**无例外** | 步骤 4 注入时逐 Task 检查；步骤 5 检查点 CP-3 复验 |
| **I3** | 每个需求 ID 必须至少在追溯链中出现一次（无孤儿需求） | 步骤 4 注入后 grep 交叉验证 |
| **I4** | 每个设计章节引用必须至少在追溯链中出现一次 | 步骤 4 注入后 grep 交叉验证 |
| **I5** | 追溯链完整性不通过 → 计划**不可**标记为"完成" | 全部计划执行完毕后强制验收 |
| **I6** | 主计划和所有子计划中**禁止**出现 TBD、TODO、placeholder、`<待补充>` 等占位符。集成联调类子计划的前置条件未满足时使用 `条件待展开` 状态标记（见 `references/plan-templates.md` §3），但不得在任务描述中使用占位符 | 步骤 6 输出前逐文件扫描 |

---

## 预警基因（经验预警，缩短搜索路径）

以下模式在推理前加载。当遇到对应场景时，按"触发 → 该怀疑什么 → 需要什么证据 → 不能直接推出什么"的路径使用，而非直接套用结论。

| 基因 | 触发条件 | 该怀疑什么 | 需要什么证据 |
|------|----------|-----------|-------------|
| **分类后拆分** | 开始拆分子计划 | 是否错误按技术栈/团队而非交付特征分类？ | 对照组件清单中每个组件的"验证方式"字段，确认与分类一致 |
| **类型路由** | 为子计划选择引擎 | 是否给基础设施类分配了 TDD？是否给功能实现类分配了命令执行？ | 核对 `references/plan-templates.md` 中该类型的验收特征 |
| **引擎按特征匹配** | 拿不准组件归属 | 该组件的"完成"如何验证——命令退出码？测试通过？端到端断言？ | 回溯 design doc 中的验证标准 |
| **可追溯优先于可执行** | 任务拆分时遇到模糊区 | 是否为了实现方便而添加了无法追溯到需求的"便利任务"？ | grep 每个 Task 的需求 ID 确认存在于需求文档 |
| **检查点预埋** | 每轮计划输出完成 | 是否等到所有计划完成才验收？是否在某轮包含 10+ 无依赖任务时遗漏了子轮次检查点？ | 确认每个子计划后面都有 CP 标记，且 CP 间距离合理 |
| **缺口暴露** | 信息提取不完整 | 是否用"默认值"掩盖了"不知道"？"待确认"占比是否已超阈值？ | 计算 gaps 三指标，对照阻断阈值 |

---

## 执行流程

### 步骤 1：提取与规范化上游设计信息

**输入**：上游设计产物。**标准流程下优先消费 `implementation-kickoff` 的设计文档**。非标准流程下也可消费其他形式的设计产物（g402 细化定义、详细设计交接摘要、架构蓝图 + PRD 等）。

**当同时存在 implementation-kickoff 文档和其他设计产物时，implementation-kickoff 文档为权威来源**（分层策略方向、Owner 分配、验收原则），其他产物用于补充技术细节。

> 详细规则（8 项必需信息、容错原则、缺口检测决策表、规范化输出模板）见 **[references/extraction-guide.md](references/extraction-guide.md)**。

**执行要点**：
1. 扫描用户指定的设计文档目录或文件
2. 按 extraction-guide 逐项提取，填入信息基线结构
3. 缺口检测：只中断于组件清单缺失（I1），其余缺口用推导或默认值填充，**显式标注置信度**（"已确认"/"已推导"/"待确认"）
4. **必须输出缺口汇总**（见 extraction-guide §4），写入主计划头部：
   - 组件"待确认"占比 > 30%：警告（不阻断）
   - 组件"待确认"占比 > 50%：**阻断**
5. 规范化输出为统一结构，供步骤 2~5 消费

---

### 步骤 2：组件分类与子计划拆分

**核心逻辑**：按组件的**交付特征**分类，同类合并为一个子计划。

| 类型 | 交付特征 | 验收方式 | 典型案例 |
|------|----------|----------|----------|
| **基础设施** | 产出是可运行的工程基座 | 命令执行通过 | 仓库初始化、CI/CD、DB 基线 |
| **功能实现** | 产出是业务功能代码 | TDD 红绿循环 + 接口契约断言 | 后端 API、前端页面、算法模块 |
| **集成联调** | 产出是全链路闭环 | 端到端断言 + 性能基准 | 跨组件联调、流媒体对接 |
| **补齐修复** | 产出是"当前→目标"变更 | 前后对比 + 一致性检查 | 设计漂移修复、技术债务清偿 |

**动作**：
1. 将每个组件归入四种类型之一
2. 同类型按依赖排序（被依赖先做）
3. 按优先级排列：基础设施 → 功能实现（可并行） → 集成联调
4. 生成主计划（子计划清单），标注类型、覆盖组件、前置依赖、可并行标记、推荐引擎
5. 回填组件清单的"所属执行组"列

#### 2.1 生成二维矩阵（交付特征 × 时间轮次）

将四类交付特征与上游分层策略方向交叉，生成矩阵并验证每个组件落在唯一单元格。若某组件在两个维度下归属冲突（如 implementation-kickoff 说第1轮但本技能判定为集成联调类），在矩阵中标注冲突并提请用户裁决。

---

### 步骤 3：按类型路由生成子计划

不同类型使用不同的生成引擎。**不要手动展开细节**——按路由表选择正确的引擎或模板：

| 类型 | 生成方式 | 参考模板 | 验收模式 |
|------|----------|----------|----------|
| **基础设施** | 按模板填充（契约、DB、CI 等） | `references/plan-templates.md` §1 | 命令退出码 |
| **功能实现** | **委托 `superpowers:writing-plans`**（传入设计片段 + 需求 ID + g402 定义路径 + 接口契约引用）。不要自己展开 TDD 步骤 | `references/plan-templates.md` §2 | TDD 红绿 |
| **集成联调** | 生成条件展开框架（标注前置条件、预留框架、不展开详细步骤）。前置条件满足后重新触发展开 | `references/plan-templates.md` §3 | 端到端断言 |
| **补齐修复** | 按对照式模板（当前状态→目标状态→变更文件清单） | `references/plan-templates.md` §4 | 前后对比 |

**g402 定义引用规则**：writing-plans 生成的 Task 中，类型定义和接口签名应引用 g402 产出文件路径，而非内联完整代码骨架。writing-plans 传入的上下文必须包含相关 g402 定义文件的路径列表。

---

### 步骤 4：注入追溯链

> 详细格式规范、完整性规则、验收标准、验证命令见 **[references/traceability-guide.md](references/traceability-guide.md)**。

每个 Task 必须标注追溯链，格式为：

```
> **追溯链** | 设计: <设计文档路径> §<章节号> | g402: <细化定义文件路径> | 需求: <需求ID列表>
```

**为什么必须做**：三个月后有人问"这段代码为什么这么写"，你能沿着计划→设计→需求一路追溯到原始决策。没有追溯链的计划，只是一堆操作清单，不是合格的工程计划。

---

### 步骤 5：配置检查点

在子计划之间埋入质量检查点，防止问题层层传递。

| 检查点位置 | 触发条件 | 检查内容 | 证据文件（通过后生成） |
|------------|----------|----------|----------------------|
| 基础设施完成后 | Plan A 结束 | 契约零 diff、DB 迁移通过、CI 语法有效、编译通过 | `docs/exec-plans/checkpoints/cp-1-report.json` |
| 每轮功能实现完成后 | 每个 Plan B/C/D 结束 | 测试覆盖率、编译零 warning、安全扫描、接口契约一致性 | `docs/exec-plans/checkpoints/cp-<n>-report.json` |
| 集成联调开始前 | Plan E 启动前 | 前置 POC 结论、上游子计划追溯链完整性 | `docs/exec-plans/checkpoints/cp-<n>-report.json` |
| 全部计划完成后 | 所有 Plan 结束 | 全链追溯完整性、八维度验收 | `docs/exec-plans/checkpoints/cp-final-report.json` |

**每个检查点通过后必须生成证据文件**，下游技能（`infrastructure-bootstrapping`、`layered-parallel-implementation`）按检查点 ID 查找对应证据文件，不依赖主计划中的文本状态标记。

**动作**：
1. 在主计划中标注每个检查点的位置、触发条件和 evidence_file 路径
2. 为每个检查点列出适用验收维度（D1~D8）和合格门槛
3. 在 `plan_tracker.md` 中预埋检查点条目，状态初始化为 `pending`

---

### 步骤 6：输出计划文件

生成以下文件：

```
docs/superpowers/plans/<date>-master-plan.md    # 主计划（子计划索引 + 依赖图 + 检查点配置 + 缺口汇总 + 组件→执行组映射表）
docs/superpowers/plans/<date>-<plan-a>.md        # 子计划 A（基础设施）
docs/superpowers/plans/<date>-<plan-b>.md        # 子计划 B（功能实现）
...                                              # 其他子计划
docs/exec-plans/plan_tracker.md                  # 初始化或更新追踪文件
docs/exec-plans/plan-evidence.json               # 结构化证据（按 plan-evidence.schema.json 生成）
```

每个文件的具体格式见 `references/plan-templates.md`。
结构化证据格式见 `references/schemas/plan-evidence.schema.json`。

---

### 步骤 7：执行交接

输出完成后，呈现计划体系摘要并给出执行选项。主计划 `master-plan.md` 必须包含以下结构化章节（供 `layered-parallel-implementation` 直接消费）：

1. **子计划索引**（类型、覆盖组件、引擎、前置依赖、并行标记）
2. **组件→执行组映射表**（含 Owner 列，从 implementation-kickoff 继承）
3. **依赖关系图**（Mermaid）
4. **检查点配置表**（含 evidence_file 路径）
5. **缺口汇总**（三指标 + 阻断状态）
6. **执行顺序建议**

**推荐执行引擎**：
- 基础设施类 → `superpowers:executing-plans`
- 功能实现类 → `superpowers:subagent-driven-development` 或 `orchestrating-fresh-subagents`
- 集成联调类 → 待前置条件满足后再选择引擎
- 补齐修复类 → `superpowers:executing-plans`

**所有计划执行完毕后，必须触发追溯链完整性验收（I5）。**

---

## 输出清单

- `docs/superpowers/plans/<date>-master-plan.md` — 主计划（含缺口汇总、组件→执行组映射表、依赖图、检查点配置）
- `docs/superpowers/plans/<date>-<subplan>.md` — 各子计划（每个 Task 含追溯链、明确文件路径和验证命令）
- `docs/exec-plans/plan_tracker.md` — 初始化的追踪文件
- `docs/exec-plans/plan-evidence.json` — 结构化证据（按 `references/schemas/plan-evidence.schema.json`）

---

## 与其他技能的关系

```
G402 implementation-refinement
    │  产出: artifacts/implementation/ 下的全部细化定义
    │
    ▼
implementation-kickoff
    │  产出: 研发启动设计文档（分层策略方向、Owner分配、验收原则、工程基础设施方案）
    │
    ▼
【本技能】implementation-plan-generation
    │  输入: implementation-kickoff 设计文档 + G402 细化定义
    │  产出: 信息基线 + 二维矩阵 + 主计划 + 子计划 + plan_tracker + plan-evidence.json
    │
    ├── 基础设施子计划 ──→ references/plan-templates.md §1
    ├── 功能实现子计划 ──→ superpowers:writing-plans（传入 g402 定义路径）
    ├── 集成联调子计划 ──→ 条件展开框架
    └── 补齐修复子计划 ──→ references/plan-templates.md §4
    │
    ↓  所有子计划产出完毕
infrastructure-bootstrapping（消费基础设施子计划 + plan-evidence.json）
    │
    ↓
layered-parallel-implementation（消费主计划 + 组件→执行组映射表 + plan-evidence.json）
    │
    ↓  所有子计划执行完毕
acceptance-gate（I5 追溯链完整性验收为强制项）
    │
    ↓
plan-completion-gate-review
```