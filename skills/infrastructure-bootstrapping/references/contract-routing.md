# Contract Routing Reference

跨语言契约（Protobuf、OpenAPI、GraphQL）到生成工具、lint 工具、代码输出格式的映射表。新增一种契约类型时只需在此表加一行。

## 路由表

| 契约类型 | 描述文件扩展名 | 代码生成工具 | Lint 工具 | 主要输出语言 | 生成脚本模板 |
|----------|--------------|-------------|----------|-------------|-------------|
| **Protobuf** | `.proto` | `protoc` + 各语言插件 | `buf lint` | Go, C++, TypeScript, Java, Python, Rust, C# | `scripts/protoc-gen.sh` |
| **OpenAPI** | `.yaml` / `.json` | `openapi-generator-cli` 或手写 | `redocly lint` | TypeScript (前端类型), Go (server stub) | 不需要（以 `.yaml` 为单一事实来源） |
| **GraphQL** | `.graphql` | `graphql-codegen` | `graphql-inspector` | TypeScript | `scripts/graphql-codegen.sh` |

## Protobuf 生成脚本模板

创建 `scripts/protoc-gen.sh`，覆盖所有编译语言的代码生成。脚本需检测 `protoc` 和各语言插件是否已安装，未安装时给出明确提示而非静默失败。

```bash
#!/usr/bin/env bash
set -euo pipefail

PROTO_DIR="$(cd "$(dirname "$0")/../contracts/proto" && pwd)"
GEN_DIR="${PROTO_DIR}/gen"

# 清理旧的生成代码
rm -rf "${GEN_DIR}"
mkdir -p "${GEN_DIR}/go" "${GEN_DIR}/cpp" "${GEN_DIR}/ts"

# 检测 protoc
if ! command -v protoc &> /dev/null; then
    echo "[ERROR] protoc 未安装，请先安装 protoc 25+"
    exit 1
fi

# 根据识别的编译语言，逐语言生成（不生成未使用语言的代码）
# Go 生成（若存在）
# protoc --go_out="${GEN_DIR}/go" --go_opt=paths=source_relative \
#   --go-grpc_out="${GEN_DIR}/go" --go-grpc_opt=paths=source_relative \
#   -I"${PROTO_DIR}" "${PROTO_DIR}"/*.proto

# C++ 生成（若存在）
# protoc --cpp_out="${GEN_DIR}/cpp" -I"${PROTO_DIR}" "${PROTO_DIR}"/*.proto

# TypeScript 生成（若存在）
# protoc --ts_out="${GEN_DIR}/ts" -I"${PROTO_DIR}" "${PROTO_DIR}"/*.proto

echo "[OK] 代码生成完成: ${GEN_DIR}"
```

生成时根据阶段 1 识别的编译语言清单，**只生成已有语言的代码**。未使用的语言段保持注释状态，不强制生成。

## OpenAPI 文件结构

```
contracts/openapi/
├── openapi.yaml          ← 单一事实来源
└── .redocly.yaml         ← lint 配置（可选）
```

`openapi.yaml` 的最小结构（从设计文档的接口契约提取）：
```yaml
openapi: 3.0.3
info:
  title: <从设计文档提取>
  version: 1.0.0
servers:
  - url: http://localhost:<端口>/api/v1
paths: {}   # 从设计文档的接口定义填充
components:
  schemas: {}  # 从设计文档的数据对象定义填充
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
```

**验证**：`npx @redocly/cli@latest lint contracts/openapi/openapi.yaml`，期望 0 error。

## 契约层必须同步的要素

跨语言契约一旦在 `contracts/` 中定义，必须确保：

1. **数据库 Schema 与契约一致**：DDL 中的字段名、类型与 proto/openapi 中的定义匹配
2. **各语言实体与契约一致**：Go struct / C++ struct / TS interface 从 proto/openapi 定义派生，不与 DDL 独立定义同样的实体
3. **CI 门禁**：contracts/ 变更时，自动运行生成脚本并校验生成代码是否已同步提交

## 单一事实来源原则

- **Protobuf 是单一事实来源** → Go/C++/TS 等语言的类型从 `.proto` 生成，不手写同名字段
- **OpenAPI 是单一事实来源** → 前端 API 客户端和后端路由签名以 `openapi.yaml` 为准
- 若同一个数据结构在 proto 和 openapi 中都有定义（如 `TrajectoryPoint`），两者必须保持字段名和类型一致，由契约委员会（或人工 review）确保
