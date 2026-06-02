# G401 执行细化说明

## 1. 作用

本文件用于细化 `G401` 的执行方式，补齐 SKILL.md 中"如何真正落地到技术实现定型文档"的步骤约束。

## 2. 执行原则

### 2.1 技术收敛原则

每个组件必须形成唯一主技术栈。

禁止：
- 多语言主实现（如同时使用 Java + Go 作为主语言）
- 多框架并存（如同时使用 Gin + Spring 作为主框架）
- 模糊技术选型（如"可根据场景选择"）

### 2.2 决策依据原则

所有技术决策必须来源于：
- 技术策略约束（G201）
- 架构蓝图约束（G203）
- 组件设计约束（G301）
- 接口设计约束（G302）
- 数据设计约束（G303）

不得凭空决策，不得引入无来源依据的新技术。

### 2.3 一致性原则

必须执行四类一致性检查：
1. 语言一致性检查：避免 Java + Go + Rust + Python 无序混用
2. 运行时一致性检查：避免 Runtime 冲突
3. 协议一致性检查：避免 gRPC + REST + MQTT 无治理混用
4. 数据链路一致性检查：避免 Kafka + MQ + ETL 链路断裂

### 2.4 可落地原则

输出必须能够直接指导：
- 开发编码（语言、框架、SDK）
- CI/CD（构建工具、测试框架）
- 测试（测试框架、mock 策略）
- 部署（容器化、编排平台、配置管理）

### 2.5 独立执行原则

G401 独立执行，不依赖运行时台账：
- 执行失败直接重新执行
- 输出文档中包含执行摘要记录执行状态
- 不需要子代理编排

## 3. 固定方法名

本 Skill 的方法检查与步骤描述统一使用以下标准名称：

1. `技术画像分析`
2. `约束回链`
3. `技术候选生成`
4. `技术约束过滤`
5. `技术栈收敛`
6. `技术一致性校验`
7. `技术风险分析`
8. `技术基线构建`
9. `运行时建模`
10. `部署技术映射`

方法来源：本文件定义，与 detailed-design-methods-catalog.md 方法命名风格保持一致。

## 4. 输入消费顺序

### 4.1 第一优先级（G300 阶段关联紧密输出）

按以下顺序读取：

| 优先级 | 文档路径 | 来源 SKILL | 提取内容 |
|:---:|---|---|---|
| P0 | `artifacts/detailed-design/002-component-design.md` | G301 | component_catalog, internal_structure_specs, component_dependencies |
| P1 | `artifacts/detailed-design/003-interface-design.md` | G302 | interface_catalog, interface_contract_specs, version_idempotency_specs |
| P2 | `artifacts/detailed-design/004-data-design.md` | G303 | data_object_catalog, storage_boundary_specs, consistency_semantics_specs |

**约束**：P0~P2 任一缺失 → 立即阻塞执行，提示缺失文件。

### 4.2 第二优先级（架构阶段输出）

| 优先级 | 文档路径 | 来源 SKILL | 提取内容 |
|:---:|---|---|---|
| P3 | `artifacts/architecture/003-architecture-blueprint.md` | G203 | 系统架构视图、技术约束 |
| P4 | `artifacts/architecture/001-technical-strategy.md` | G201 | 技术策略约束、选型边界 |

**约束**：P3~P4 任一缺失 → 立即阻塞执行，提示缺失文件。

### 4.3 第三优先级（按需读取）

| 优先级 | 文档路径 | 来源 | 提取内容 |
|:---:|---|---|---|
| P5 | `artifacts/architecture/004-adr.md` | G203/G204 | 架构决策记录（技术选型相关） |
| P6 | `artifacts/detailed-design/001-design-plan.md` | G300 | 设计计划、模式冻结结果 |

**约束**：P5~P6 缺失 → warning，继续执行但记录缺失。

## 5. 步骤级要求

### 5.1 冻结技术实现范围与来源追溯

必须显式写出：
1. in-scope 组件清单（来自 G301.component_catalog）
2. in-scope 接口清单（来自 G302.interface_catalog）
3. in-scope 数据对象清单（来自 G303.data_object_catalog）
4. out-of-scope 和 deferred 项

必须建立来源回链：
- 每个组件追溯到 G301.component_catalog 的 component_id
- 每个接口追溯到 G302.interface_catalog 的 interface_id
- 每个数据对象追溯到 G303.data_object_catalog 的 data_object_id

必须使用方法：`技术画像分析`、`约束回链`。

### 5.2 建立技术栈目录

必须为每个技术类别生成候选清单：
- language_candidates（编程语言候选）
- framework_candidates（框架候选）
- middleware_candidates（中间件候选）
- storage_candidates（存储技术候选）
- runtime_candidates（运行时候选）

必须使用技术策略约束过滤候选项：
- 性能约束
- 吞吐约束
- 延迟约束
- 边缘部署约束
- 运维复杂度约束

必须使用方法：`技术候选生成`、`技术约束过滤`。

### 5.3 定义组件技术规格

每个组件必须输出：
- final_language（最终语言选型）
- final_framework（最终框架选型）
- final_runtime（最终运行时选型）
- final_middleware（最终中间件依赖）

必须说明：
- 选择原因（decision_reason）
- 放弃原因（reject_reason）

必须使用方法：`技术栈收敛`。

### 5.4 定义接口技术规格

每个接口必须输出：
- protocol（协议：REST / gRPC / MQTT / WebSocket）
- transport_mode（传输方式：sync / async / stream）
- serialization_format（序列化格式：JSON / Protobuf / Avro）
- sdk_framework（SDK/框架）

必须说明兼容策略：
- 当前版本（current_version）
- 兼容窗口（compatibility_window）
- 弃用策略（deprecation_policy）
- 灰度策略（rollout_strategy）

必须使用方法：`技术栈收敛`。

### 5.5 定义数据技术规格

每个数据对象必须输出：
- storage_technology（存储技术）
- data_type（数据类型：relational / document / key-value / time-series / file）
- consistency_model（一致性模型：strong / eventual）
- lifecycle_policy（生命周期策略）

必须说明访问模式：
- read_write_mode（读写模式）
- cache_strategy（缓存策略）
- index_strategy（索引策略）

必须使用方法：`技术栈收敛`。

### 5.6 定义运行时与部署规格

每个组件必须输出：
- container_image（镜像）
- containerization_method（容器化方式：Docker / other）
- orchestration_platform（编排平台：Kubernetes / Docker Swarm / other）

必须说明运行环境约束：
- cpu_requirement
- memory_requirement
- network_requirement
- special_constraint

必须说明可观测性技术：
- log_technology
- metric_technology
- trace_technology

必须使用方法：`运行时建模`、`部署技术映射`。

### 5.7 生成技术风险与技术基线

必须执行四类一致性检查：
- language_consistency_check
- runtime_consistency_check
- protocol_consistency_check
- data_pipeline_consistency_check

检查结果必须为：pass / warning / fail。

每个关键技术决策必须形成：
- risk_id
- risk_type（performance / compatibility / security / availability / maintainability）
- impact_scope
- mitigation_strategy
- fallback_option

必须输出系统级技术基线：
- primary_language
- primary_framework
- communication_stack
- middleware_stack
- storage_stack
- deployment_stack

必须使用方法：`技术一致性校验`、`技术风险分析`、`技术基线构建`。

## 6. 与研发实现阶段衔接要求

进入研发前必须保证：

### 6.1 技术栈闭环

形成：组件 → 语言 → 框架 → Runtime → 中间件 完整闭环。

### 6.2 接口实现闭环

形成：接口 → 协议 → 序列化方式 → SDK 完整闭环。

### 6.3 数据实现闭环

形成：数据对象 → 存储 → 索引 → 生命周期 完整闭环。

### 6.4 部署实现闭环

形成：组件 → 镜像 → 容器 → 编排 → 部署 完整闭环。

## 7. 质量与恢复要求

### 7.1 当前轮不通过条件

以下任一缺失视为不通过：
- tech_stack_catalog
- component_technology_specs
- interface_technology_specs
- data_technology_specs
- runtime_deployment_specs
- technology_risk_specs
- technology_baseline

### 7.2 一致性检查失败处理

- language_consistency=fail → 阻塞执行，列出语言冲突组件
- runtime_consistency=fail → 阻塞执行，列出运行时冲突组件
- protocol_consistency=fail → 阻塞执行，列出协议冲突接口
- data_pipeline_consistency=fail → 阻塞执行，列出数据链路断裂点

### 7.3 恢复机制

直接重新执行 SKILL：
- 输出文档第 1 章包含执行摘要
- 记录输入文件完整性校验结果
- 记录输出字段完整性自检结果
- 记录可追溯性校验结果