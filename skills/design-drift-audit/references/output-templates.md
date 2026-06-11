# 设计漂移审计 — 输出模板

## 1. Markdown 报告模板

保存路径: `docs/superpowers/specs/YYYY-MM-DD-design-drift-audit-report.md`

```markdown
# 设计漂移审计报告

**审计时间**: YYYY-MM-DD HH:MM
**审计范围**: [第N轮编码后 / 设计vX.Y更新后 / 用户指定]
**设计基线**:
  - [文档路径] (版本 vX.Y, 批准日期 YYYY-MM-DD)
  - ...
**代码范围**:
  - [目录路径] ([技术栈])
  - ...

---

## 统计摘要

| 指标 | 数量 |
|------|------|
| 审计总项 | N |
| 通过 | N |
| 漂移项 | N |
| ├ CRITICAL | N |
| ├ MAJOR | N |
| └ MINOR | N |
| 未登记项(需确认) | N |

---

## 漂移项清单

### CRITICAL

| ID | 维度 | 设计定义 | 代码现状 | 影响 |
|----|------|----------|----------|------|
| DRIFT-001 | 存在性 | [来源文档] 定义了 [对象名]：[简述] | 代码中完全不存在 | 阻塞 [下游计划/任务] |
| DRIFT-002 | ... | ... | ... | ... |

### MAJOR

| ID | 维度 | 设计定义 | 代码现状 | 影响 |
|----|------|----------|----------|------|
| DRIFT-003 | 完整性 | [来源文档] [对象名].[字段名] 类型为 [T] | 代码中类型为 [T'] | [下游影响描述] |
| DRIFT-004 | ... | ... | ... | ... |

### MINOR

| ID | 维度 | 设计定义 | 代码现状 | 影响 |
|----|------|----------|----------|------|
| DRIFT-005 | 存在性 | ... | ... | ... |

---

## 跨栈一致性详情

### [数据对象名]

| 技术栈 | 字段 | 设计定义 | 实际定义 | 判定 |
|--------|------|----------|----------|------|
| Proto | pile_number | int64 | int64 | PASS |
| SQL | pile_number | BIGINT | BIGINT | PASS |
| Go | PileNumber | int64 | float64 | **FAIL** — 类型不一致 |
| TS | pile_number | number | number | PASS |
| C++ | pile_number | int64_t | (不存在) | **FAIL** — 字段缺失 |

---

## 未登记项（代码有、设计无，需确认意图）

| ID | 代码位置 | 定义 | 可能的意图 | 建议动作 |
|----|----------|------|-----------|----------|
| UNREG-001 | [文件:行号] | [struct/interface名] | [推测的用途] | 补充设计文档 / 标记 by-design |

---

## 审计后建议

### 必须在下一轮编码前修复 (CRITICAL)
1. DRIFT-001: [简述 + 建议修复方式]

### 建议在下一轮编码前修复 (MAJOR)
1. DRIFT-003: [简述 + 建议修复方式]

### 可延后处理 (MINOR)
1. DRIFT-005: [简述]

### 未登记项确认
1. UNREG-001: 请确认 [对象名] 是设计遗漏还是实现细节
```

---

## 2. JSON Schema

保存路径: 与 MD 报告同目录，文件名 `YYYY-MM-DD-design-drift-audit-report.json`

```json
{
  "$schema": "设计漂移审计报告 v1.0",
  "audit_metadata": {
    "timestamp": "2026-06-07T14:30:00Z",
    "audit_scope": "Plan A~D 完成后 / 设计 v2.1 对齐检查",
    "design_baseline": {
      "path": "artifacts/detailed-design/",
      "version": "v2.1",
      "documents": [
        {
          "path": "artifacts/detailed-design/002-component-design.md",
          "version": "v2.1",
          "type": "component_design"
        },
        {
          "path": "artifacts/detailed-design/003-interface-design.md",
          "version": "v2.1",
          "type": "interface_design"
        },
        {
          "path": "artifacts/detailed-design/004-data-design.md",
          "version": "v2.1",
          "type": "data_design"
        }
      ]
    },
    "code_scope": {
      "directories": [
        "contracts/proto/",
        "contracts/openapi/",
        "center/db/migration/",
        "center/services/",
        "edge/algorithm/",
        "edge/services/",
        "frontend/center-web/",
        "frontend/edge-web/"
      ],
      "tech_stacks": ["protobuf", "openapi", "sql", "go", "cpp17", "typescript"]
    }
  },

  "summary": {
    "total_items_checked": 87,
    "passed": 72,
    "drift_total": 12,
    "critical": 2,
    "major": 7,
    "minor": 3,
    "unregistered_items": 2
  },

  "drift_items": [
    {
      "id": "DRIFT-001",
      "dimension": "existence",
      "severity": "critical",
      "design_definition": {
        "source_doc": "artifacts/detailed-design/004-data-design.md",
        "source_ref": "DAT-013 camera_config 表定义",
        "item_name": "camera_config",
        "item_type": "data_object",
        "description": "摄像机配置表，包含 lane_count, lane_boundaries, install_height, pitch_angle, focal_length, principal_point 等标定参数",
        "required_fields": [
          {"name": "camera_id", "type": "VARCHAR(64)", "constraints": "NOT NULL, UNIQUE"},
          {"name": "physical_pile", "type": "BIGINT", "constraints": "NOT NULL"},
          {"name": "direction", "type": "VARCHAR(16)", "constraints": "NOT NULL, CHECK IN ('UPSTREAM','DOWNSTREAM')"},
          {"name": "lane_count", "type": "INT", "constraints": "NOT NULL DEFAULT 2"},
          {"name": "lane_boundaries", "type": "INT[]", "constraints": "NOT NULL"},
          {"name": "install_height", "type": "DOUBLE PRECISION", "constraints": "NULLABLE"},
          {"name": "pitch_angle", "type": "DOUBLE PRECISION", "constraints": "NULLABLE"},
          {"name": "focal_length", "type": "DOUBLE PRECISION", "constraints": "NULLABLE"},
          {"name": "principal_point_x", "type": "DOUBLE PRECISION", "constraints": "NULLABLE"},
          {"name": "principal_point_y", "type": "DOUBLE PRECISION", "constraints": "NULLABLE"}
        ]
      },
      "code_reality": {
        "files_checked": [
          "center/db/migration/V1__baseline.sql",
          "center/services/db/model/model.go"
        ],
        "status": "missing",
        "actual_state": "DDL 中无 camera_config 表，Go model 中无 CameraConfig struct",
        "notes": ""
      },
      "impact": {
        "description": "CMP-004 车道识别算法无法获取摄像机标定参数，轨迹坐标计算的精度无法保证",
        "affected_downstream": ["Plan D CMP-004", "Plan E 轨迹 REST API"],
        "blocks_next_round": true
      }
    },
    {
      "id": "DRIFT-002",
      "dimension": "completeness",
      "severity": "major",
      "design_definition": {
        "source_doc": "artifacts/detailed-design/003-interface-design.md",
        "source_ref": "IFC-004 TrajectoryPoint message",
        "item_name": "TrajectoryPoint.pile_number",
        "item_type": "field",
        "description": "隧道内桩号，int64 类型，替代 v1.0 的 x,y,z 坐标",
        "required_fields": [
          {"name": "pile_number", "type": "int64", "constraints": "NOT NULL"}
        ]
      },
      "code_reality": {
        "files_checked": [
          "contracts/proto/crosshost.proto",
          "center/db/migration/V1__baseline.sql",
          "center/services/db/model/model.go",
          "center/services/internal/ws/message.go",
          "frontend/center-web/src/api/types.ts",
          "edge/algorithm/src/common/types.h"
        ],
        "status": "divergent",
        "actual_state": "proto 中为 double x=3, double y=4, double z=5 (旧 v1.0 坐标)；SQL 中无 pile_number 列；Go model 中为 X/Y/Z float64；TS 中为 x/y/z number；C++ 中为 float x,y,z",
        "notes": "全栈仍在使用已废弃的 x,y,z 坐标体系"
      },
      "impact": {
        "description": "Plan E 中所有轨迹相关功能（DAO/API/前端展示/算法输出）都基于错误的坐标字段，联调时数据无法正确传递",
        "affected_downstream": ["Plan E 轨迹 DAO", "Plan E 轨迹 REST API", "Plan E 前端轨迹展示", "Plan D 轨迹计算输出"],
        "blocks_next_round": false
      }
    }
  ],

  "cross_stack_inconsistencies": [
    {
      "concept_name": "TrajectoryPoint",
      "stacks_checked": ["proto", "sql", "go_backend", "typescript", "cpp"],
      "field_name": "pile_number",
      "stack_states": {
        "proto": {"status": "divergent", "actual": "double x, y, z (field 3-5)"},
        "sql": {"status": "missing", "actual": null},
        "go_backend": {"status": "divergent", "actual": "X, Y, Z float64"},
        "typescript": {"status": "divergent", "actual": "x, y, z number"},
        "cpp": {"status": "divergent", "actual": "float world_x, world_y, world_z"}
      }
    }
  ],

  "unregistered_items": [
    {
      "id": "UNREG-001",
      "code_location": "edge/services/internal/ipc/server.go:15",
      "definition": "type IPCServer struct { listener net.Listener; handler *Handler }",
      "possible_intent": "C++ 算法与 Go 边缘服务的 UDS 通信通道",
      "suggested_action": "补充到设计文档的组件通信章节，或标记为内部实现细节"
    }
  ],

  "recommendations": {
    "must_fix_before_next_round": ["DRIFT-001"],
    "should_fix_before_next_round": ["DRIFT-002", "DRIFT-003"],
    "can_defer": ["DRIFT-008", "DRIFT-009"],
    "needs_human_decision": ["UNREG-001"]
  }
}
```

---

## 3. JSON 字段说明

### drift_item 对象

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 漂移项唯一标识，格式 `DRIFT-NNN` |
| dimension | enum | 是 | `existence` / `completeness` / `cross_stack_consistency` / `redundancy` |
| severity | enum | 是 | `critical` / `major` / `minor` |
| design_definition | object | 是 | 设计文档中的定义，包含来源、字段列表 |
| design_definition.source_doc | string | 是 | 来源设计文档路径 |
| design_definition.source_ref | string | 是 | 文档内引用（章节号/编号） |
| design_definition.item_name | string | 是 | 被检查项的名称 |
| design_definition.item_type | enum | 是 | `data_object` / `field` / `interface` / `component` / `message` / `endpoint` |
| design_definition.required_fields | array | 否 | 当 item_type 为 data_object/message 时的字段列表 |
| code_reality | object | 是 | 代码中的实际情况 |
| code_reality.files_checked | array | 是 | 检查过的文件路径列表 |
| code_reality.status | enum | 是 | `missing` / `partial` / `divergent` / `extra` |
| code_reality.actual_state | string | 是 | 代码现状的文字描述 |
| impact | object | 是 | 影响评估 |
| impact.description | string | 是 | 影响描述 |
| impact.affected_downstream | array | 是 | 受影响的下游计划/任务/组件 |
| impact.blocks_next_round | boolean | 是 | 是否阻塞下一轮编码启动 |

### cross_stack_inconsistency 对象

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| concept_name | string | 是 | 跨栈数据对象名称 |
| stacks_checked | array | 是 | 检查过的技术栈列表 |
| field_name | string | 是 | 不一致的字段名称 |
| stack_states | object | 是 | 各技术栈的实际状态，key 为技术栈名，value 为 {status, actual} |

### unregistered_item 对象

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 格式 `UNREG-NNN` |
| code_location | string | 是 | 代码位置（文件:行号） |
| definition | string | 是 | 代码中的定义 |
| possible_intent | string | 是 | 推测的用途 |
| suggested_action | string | 是 | 建议的处理方式 |
