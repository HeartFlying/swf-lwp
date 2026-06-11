---
name: g402-implementation-refinement
description: >
  当 G401 技术实现定型完成后，将 G301/G302/G303 的架构级设计细化为编码级定义时使用。
  负责消费架构设计产物 + G401 技术栈选择，产出数据对象定义、接口定义、组件定义、契约制品草稿，
  存放于 artifacts/implementation/。本技能是"架构设计→编码实现"的转化层，
  plan-generation、infrastructure-bootstrapping、layered-parallel-implementation
  均以本技能产出为唯一权威来源。
  触发场景："细化设计定义"、"生成编码级接口定义"、"design refinement"、
  "从架构设计到编码定义"、"生成实现级定义文件"、"G402"。
  前置条件：G401 已完成，artifacts/detailed-design/005-technology-realization.md 可读取。
---

# G402 实现级设计细化

## 目标

将上游架构级设计产物（G301 组件设计、G302 接口设计、G303 数据设计）结合 G401 技术栈选择，
细化为编码级定义，确保每个组件、每个接口、每个数据对象都有精确到编程语言类型的定义文档，
并产出契约制品草稿。

**核心增值**：填补"架构设计"与"直接编码"之间的粒度差距：

- **架构设计说**："组件 A 负责设备管理，提供设备查询接口"
- **本技能细化到**："组件 A 包含 `DeviceManager` 类，成员变量 `_deviceRepo DeviceRepository`，
  公共方法 `GetDeviceList(ctx, filter) ([]Device, error)`，实现 IFC-003 的 `GetDeviceList` RPC"

## 核心原则

1. **数据对象优先**：数据对象先定义，接口才能引用精确类型，组件才能引用精确签名。链不断。
2. **全量细化**：所有接口、数据对象、组件均做细化，不区分跨组/组内。组内定义的细化同样支撑后续编码。
3. **技术栈绑定**：所有类型定义必须使用 G401 确定的具体编程语言类型，不允许模糊表述。
4. **类型可追溯**：接口参数/返回值中的类型必须能追溯到数据对象定义文件；组件方法签名必须能追溯到接口定义文件。
5. **独立工件**：细化定义存放于 `artifacts/implementation/`，与上游 G301/G302/G303 保持单向引用关系。
   上游设计可独立演进，细化定义随实现推进可调整而不污染设计基线。

## 输入

| 输入文件 | 来源 | 提取内容 |
|----------|------|----------|
| `artifacts/detailed-design/002-component-design.md` | G301 | component_catalog, internal_structure_specs, component_dependencies |
| `artifacts/detailed-design/003-interface-design.md` | G302 | interface_catalog, interface_contract_specs, version_idempotency_specs |
| `artifacts/detailed-design/004-data-design.md` | G303 | data_object_catalog, storage_boundary_specs, consistency_semantics_specs |
| `artifacts/detailed-design/005-technology-realization.md` | G401 | tech_stack_catalog, component_technology_specs, interface_technology_specs, data_technology_specs |
| `artifacts/architecture/003-architecture-blueprint.md` | G203 | 系统架构视图、组件部署拓扑 |

## 执行流程

```
步骤 1: 数据对象定义细化 ──（消费 G303 + G401）
    │
    ▼
步骤 2: 接口定义细化 ──（消费 G302 + G401 + 步骤1产出）
    │
    ▼
步骤 3: 组件定义细化 ──（消费 G301 + G401 + 步骤1 + 步骤2产出）
    │
    ▼
步骤 4: 契约制品草稿生成 ──（消费 步骤2产出 + G401协议选择）
```

### 步骤 1: 数据对象定义细化

**输入来源**：
- G303 数据设计文档中的 data_object_catalog
- G401 技术实现定型中的 data_technology_specs（编程语言类型映射）
- G301 组件设计文档中涉及的数据结构描述

**动作**：

1. 从数据设计文档和组件设计文档中提取所有数据对象（不区分跨组/组内）。

2. 为每个数据对象建立独立定义文件，路径：`artifacts/implementation/data-defs/<object-name>.md`，内容必须包含：

   | 字段 | 说明 |
   |------|------|
   | **对象名称** | 编程语言级命名（如 `DeviceInfo`、`TrackEvent`） |
   | **所属来源** | 追溯至 G303 中的 data_object_id |
   | **用途简述** | 一句话说明该对象的业务含义 |
   | **编程语言** | 从 G401 获取的主编程语言 |
   | **字段清单** | 每个字段的：字段名、编程语言类型（如 `int32`/`string`/`time.Time`/`[]TrackPoint`）、是否必填、约束（长度/范围/格式/枚举值）、默认值 |
   | **关联关系** | 引用其他数据对象的字段，标注引用的对象定义文件路径 |
   | **序列化要求** | json / protobuf / 自定义，以及特殊处理（如 omitempty、enum 映射） |

3. 产出数据对象清单（汇总表），记录：对象名 → 文件路径 → 来源(data_object_id) → 编程语言类型。

**输出**：
- `artifacts/implementation/data-defs/` 目录，每个数据对象一个独立 Markdown 文件
- 数据对象清单（写入主输出文件或独立索引文件）

**完成标准**：
- 所有数据对象均已建立独立定义文件
- 每个文件包含对象名称、来源追溯、字段清单（含具体编程语言类型）、约束、序列化要求
- 数据对象之间的引用关系可追溯（字段类型能指向其他数据对象定义文件）
- 所有类型均来自 G401 确定的技术栈

---

### 步骤 2: 接口定义细化

**输入来源**：
- G302 接口设计文档中的 interface_catalog
- G401 技术实现定型中的 interface_technology_specs（协议绑定、序列化方式）
- 步骤 1 的数据对象定义
- G301 组件设计文档中的接口交接边界

**动作**：

1. 从接口设计文档中提取所有接口（不区分跨组/组内）。

2. 为每个接口建立独立定义文件，路径：`artifacts/implementation/interface-defs/<interface-name>.md`，内容必须包含：

   | 字段 | 说明 |
   |------|------|
   | **接口名称** | 编程语言级命名（如 `GetDeviceList`、`SubscribeTrackEvents`） |
   | **调用约定** | gRPC unary / gRPC server-streaming / REST GET / REST POST / 函数调用 / 消息队列 publish-subscribe |
   | **提供方组件** | 实现该接口的组件名称（引用组件设计文档中的 component_id） |
   | **消费方组件** | 调用/订阅该接口的组件列表 |
   | **输入参数** | 每个参数：名称、类型（引用数据对象定义或基本类型）、是否必填、默认值、校验规则 |
   | **输出** | 返回类型（引用数据对象定义）、错误码列表（每个错误码含语义说明和调用方处理建议） |
   | **协议绑定** | 具体协议映射：proto 的 service + method 名 / REST 的 method + path + query params / 函数签名 / 消息 topic + 消息体格式 |
   | **幂等与重试** | 幂等键（如有）、重复调用语义、建议重试策略 |
   | **性能约束** | 预期延迟、超时时间、并发限制（如有） |

3. 参数/返回值中的类型**必须**可追溯到步骤 1 的数据对象定义文件或基本类型。

4. 产出接口覆盖清单（汇总表），记录：接口名 → 提供方 → 消费方 → 协议 → 协议绑定 → 文件路径。

**输出**：
- `artifacts/implementation/interface-defs/` 目录，每个接口一个独立 Markdown 文件
- 接口覆盖清单

**完成标准**：
- 所有接口均已建立独立定义文件
- 每个文件包含接口名称、调用约定、输入参数（含具体类型）、输出（含类型和错误码）、协议绑定
- 参数/返回值中的类型可追溯到数据对象定义文件或基本类型
- 无模糊描述——所有类型均为具体编程语言类型
- 协议绑定来自 G401 的 interface_technology_specs

---

### 步骤 3: 组件定义细化

**输入来源**：
- G301 组件设计文档中的 component_catalog, internal_structure_specs
- G401 技术实现定型中的 component_technology_specs
- G203 架构蓝图中的组件划分
- 步骤 1 的数据对象定义
- 步骤 2 的接口定义

**动作**：

1. 从组件设计文档中提取所有待实现的组件。

2. 为每个组件建立独立定义文件，路径：`artifacts/implementation/component-defs/<component-name>.md`，内容必须包含：

   | 字段 | 说明 |
   |------|------|
   | **组件名称** | 编程语言级组件名（如 `DeviceManager`、`TrackService`） |
   | **来源** | 追溯至 G301 中的 component_id |
   | **职责简述** | 一句话说明该组件的核心职责 |
   | **目标文件路径** | 该组件在代码仓库中的预期文件路径（如 `center/services/internal/device/manager.go`） |
   | **编程语言** | 从 G401 获取的主编程语言 |
   | **类/结构体定义** | 类名、继承/实现关系、可见性 |
   | **成员变量** | 每个成员：变量名、类型（引用数据对象定义或基本类型）、可见性、说明、默认值 |
   | **公共方法** | 每个方法：方法名、完整签名（参数名+类型、返回值类型+含义）、所属接口追溯（该方法实现接口定义中的哪个操作）、前置/后置条件 |
   | **依赖注入** | 该组件依赖的外部接口列表（引用接口定义文件）、注入方式（构造函数/Setter/框架注入） |
   | **组件关联** | 本组件直接依赖的其他组件列表（含依赖关系类型：同步调用/异步事件/数据管线）、被哪些组件依赖（反向追溯）。关联关系在 `_dependency-matrix.md` 中全局索引，每项标注所属层（edge/center/frontend） |
   | **内部类图** | 本组件内部的类/结构体及其关系（Mermaid classDiagram 片段），包含：本组件核心类、成员变量类型引用、类间依赖/聚合/继承关系。该片段将被汇总到全局系统拓扑图 `_system-topology.md` 中 |
   | **内部状态** | 关键状态及转换条件（如有状态机） |
   | **错误处理** | 该组件需要处理的关键异常类型和处理策略 |

3. 组件方法签名中的参数/返回值类型**必须**可追溯到接口定义文件或数据对象定义文件。

4. 产出组件覆盖清单。

5. **生成组件依赖矩阵**（`_dependency-matrix.md`）：
   - 从各组件的"组件关联"字段汇总，生成 N×N 依赖矩阵
   - 行 = 依赖方组件，列 = 被依赖方组件，单元格标注依赖关系类型（同步调用 SYNC / 异步事件 ASYNC / 数据管线 PIPE）
   - 矩阵下方列出每个组件所属的系统层（edge / center / frontend）
   - 标注跨层依赖（如 frontend→center 通过 REST API）和同层依赖（如 center 内部通过 gRPC）

6. **生成全局系统拓扑图**（`_system-topology.md`）：
   - 产出**三层 Mermaid classDiagram**：
     - **层间拓扑**：展示 edge / center / frontend 三层，层之间通过接口和协议关联（如 frontend ↔ center 通过 REST + WebSocket，edge ↔ center 通过 gRPC + MQ）
     - **组件间拓扑**：展示全体组件通过接口的关联关系，每个组件作为一个 class，接口作为 class 的 method，组件间连线标注依赖关系类型和对应接口名
     - **组件内部类图**：将各组件的"内部类图"片段汇总，每个组件一个 classDiagram 区块，展示组件内类/结构体的依赖、聚合、继承关系
   - 各层组件用不同样式/颜色区分
   - 所有关系线必须标注来源（对应哪个接口定义文件或数据对象定义文件）

**输出**：
- `artifacts/implementation/component-defs/` 目录，每个组件一个独立 Markdown 文件
- 组件覆盖清单
- `artifacts/implementation/component-defs/_dependency-matrix.md` — 全局组件依赖矩阵
- `artifacts/implementation/component-defs/_system-topology.md` — 全局系统拓扑图（Mermaid）

**完成标准**：
- 所有待实现组件均已建立独立定义文件
- 每个文件包含类名、目标文件路径、成员变量（含具体类型+可见性）、公共方法（含完整签名）、依赖接口追溯
- 每个文件包含组件关联关系和内部类图片段
- 方法签名与其提供的接口定义一致（可交叉验证）
- 成员变量的类型与数据对象定义一致（可交叉验证）
- 编程语言与 G401 技术栈一致
- 依赖矩阵覆盖全部组件，无遗漏，每个单元格标注了关系类型
- 系统拓扑图覆盖三层（层间/组件间/组件内部），所有连线可追溯到接口定义文件

---

### 步骤 4: 契约制品草稿生成

**输入来源**：
- 步骤 2 的接口定义（含协议绑定信息）
- 步骤 1 的数据对象定义（含序列化要求）

**动作**：

1. 对步骤 2 中每个有协议绑定的接口，生成对应协议的契约制品草稿：
   - gRPC 接口 → `.proto` 文件（含 service、rpc、message 定义）
   - REST 接口 → OpenAPI 路径/组件片段
   - 前端契约 → TypeScript 类型定义文件雏形
   - 消息队列 → 消息体 schema 文件

2. 契约制品的消息/参数/返回值结构必须与步骤 1 的数据对象定义和步骤 2 的接口定义一致。

3. 产出契约覆盖清单（汇总表），记录：契约制品文件 → 对应接口定义 → 提供方 → 消费方。

**输出**：
- `artifacts/implementation/contracts/` 目录（含 proto、openapi、ts-types 等）
- 契约覆盖清单

**注意**：本步骤产出的是语义内容正确的草稿，不要求通过编译/lint。
编译验证由 `infrastructure-bootstrapping` 执行，验证失败时回推到本技能修复。

---

## 出口条件（全部满足才算完成）

- [ ] 所有数据对象均有独立定义文件，字段类型为具体编程语言类型，追溯至 G303
- [ ] 所有接口均有独立定义文件，参数/返回值类型可追溯到数据对象定义，协议绑定来自 G401
- [ ] 所有组件均有独立定义文件，含类名、成员变量、公共方法签名、依赖注入、组件关联、内部类图，追溯至 G301
- [ ] 组件方法签名与接口定义交叉一致
- [ ] 组件依赖矩阵覆盖全部组件，每个单元格标注关系类型（SYNC/ASYNC/PIPE），区分跨层/同层依赖
- [ ] 全局系统拓扑图完整：层间拓扑（接口+协议）、组件间拓扑（Mermaid classDiagram）、组件内部类图（汇总自各组件片段）
- [ ] 拓扑图中所有连线可追溯到接口定义文件或数据对象定义文件
- [ ] 所有有协议绑定的接口均有对应的契约制品草稿
- [ ] 数据对象清单、接口覆盖清单、组件覆盖清单、契约覆盖清单均无"待确认"条目
- [ ] 所有类型使用 G401 确定的技术栈，无模糊表述

## 输出目录结构

```
artifacts/implementation/
├── data-defs/                  # 步骤 1: 每个数据对象一个文件
│   ├── DeviceInfo.md
│   ├── TrackEvent.md
│   └── ...
├── interface-defs/             # 步骤 2: 每个接口一个文件
│   ├── GetDeviceList.md
│   ├── SubscribeTrackEvents.md
│   └── ...
├── component-defs/             # 步骤 3: 每个组件一个文件 + 全局关联制品
│   ├── DeviceManager.md
│   ├── TrackService.md
│   ├── ...
│   ├── _dependency-matrix.md    # 步骤 3.5: 全局 N×N 组件依赖矩阵
│   └── _system-topology.md      # 步骤 3.6: 全局系统拓扑图（三层 Mermaid classDiagram）
└── contracts/                  # 步骤 4: 契约制品草稿
    ├── proto/
    ├── openapi/
    └── ts-types/
```

## 与其他技能的关系

```
G301/G302/G303（架构级设计）
        │
        ▼
G401（技术实现定型）
        │
        ▼
【本技能】g402-implementation-refinement
        │  产出：artifacts/implementation/ 下的全部细化定义
        │
        ├──→ implementation-kickoff（消费细化定义制定策略）
        ├──→ implementation-plan-generation（引用细化定义替代内联代码）
        ├──→ infrastructure-bootstrapping（编译验证契约制品草稿）
        └──→ layered-parallel-implementation（直接读取细化定义派发编码）
```

**职责边界**：
- 本技能只负责"架构级定义 → 编码级定义"的转化，不进行策略决策（那是 kickoff 的职责）
- 本技能不创建任务计划（那是 plan-generation 的职责）
- 本技能不执行编码（那是 layered-parallel 的职责）
- 出现冲突时以 G301/G302/G303/G401 为准，本技能只做细化不做修改

## 常见问题

**Q: 如果 G401 尚未完成怎么办？**
A: 本技能的前置条件是 G401 已完成。如 G401 未完成，应先运行 G401 确定技术栈后再执行本技能。

**Q: 细化定义是否要写回 G301/G302/G303？**
A: 不写回。细化定义是独立工件，存放于 `artifacts/implementation/`，与上游设计文档保持单向引用关系。

**Q: 如果某个接口的协议不支持代码生成怎么办？**
A: 契约制品的最低要求降级为：机器可校验的格式定义（如 JSON Schema）+ 提供方和消费方各自可运行校验命令。
接口定义文件仍产出，参数签名和调用约定精确到编程语言级。

**Q: 数据对象定义是否包含只在单个组件内部使用的私有数据结构？**
A: 默认不包含。仅组件内部使用的私有数据结构由编码阶段自行定义。
但如果某个私有数据结构是实现接口所必需的（如作为接口参数的类型嵌套结构），则需要纳入数据对象定义。

**Q: 契约草稿与最终契约是什么关系？**
A: 本技能产出的是语义正确的草稿（字段名、类型、结构正确）。
infrastructure-bootstrapping 负责将其放到正确仓库位置并编译验证。
如果编译失败（如 proto 语法错误），回推到本技能修复。
