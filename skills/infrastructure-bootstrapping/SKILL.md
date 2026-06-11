---
name: infrastructure-bootstrapping
description: >
  当项目完成设计阶段、需要从零搭建可构建可验证的工程基座时使用本技能。
  负责仓库目录结构、契约层(proto/openapi)、数据库迁移基线、各语言的构建骨架、
  容器化开发环境、CI/CD 流水线等基础设施的创建与验证。
  只要用户提到"搭工程骨架"、"初始化项目"、"搭脚手架"、"创建工程基座"、
  "init project"、"bootstrap"、"setup infrastructure"、"项目初始化"、
  "搭建开发环境"、"创建构建系统"，或项目处于设计完成后需要开始写第一行代码的阶段，
  就必须使用本技能。
  本技能不写业务代码，只创建能让业务代码开始编写的最小工程基座。
---

# Infrastructure Bootstrapping（工程基座初始化）

## 目标

从设计文档出发，搭建一个**能编译、能迁移、能启动**的工程基座。结束后，业务代码可以立即在其上开始编写，不需要再处理构建配置、数据库连接、契约生成等基础设施问题。

## 核心原则

1. **从设计文档读，不向用户问**：技术栈、数据库类型、契约格式等信息必须从设计文档中提取，不向用户提问已有答案的问题
2. **创建即验证**：每个模块创建后立即运行对应的验证命令（编译/迁移/lint），不等最后统一验证
3. **最小骨架**：每种语言只创建能证明工具链可用的最小文件（一个 main 函数、一个测试桩），不提前写业务结构
4. **语言无差别对待**：Go / C++ / Java / Rust / Python / TypeScript / C# 等所有编译语言适用同一套判定流程，具体工具映射从 references/ 引用文件查表获取

## 输入

设计阶段交接文档，或 `implementation-kickoff` 产出的研发启动设计文档。至少需要包含：技术栈清单、数据库选型、契约定义方式和模块拓扑。

---

## 阶段 1：技术栈识别

从设计文档中提取结构化的技术栈信息。不假设任何语言或工具，完全从文档内容判定。

**提取方式**：在文档中搜索以下信号，每种信号对应一种技术要素：

| 信号（文档中出现的关键词/模式） | 判定为 |
|--------------------------------|--------|
| go.mod / Go 1.xx / go work | Go |
| CMakeLists.txt / C++17/C++20 / gcc / clang | C++ |
| Cargo.toml / Rust edition / rustc | Rust |
| pom.xml / build.gradle / build.gradle.kts / maven / gradle | Java |
| pyproject.toml / setup.py / setup.cfg / requirements.txt | Python |
| package.json / tsconfig.json / node_modules / npm / yarn | TypeScript / JavaScript |
| .csproj / .sln / dotnet / NuGet | C# / .NET |
| PostgreSQL / pgx / postgres / psql | PostgreSQL |
| MySQL / mariadb / InnoDB / mysql2 | MySQL |
| MongoDB / mongodb / collection / document | MongoDB |
| SQLite / sqlite3 / libsqlite | SQLite |
| .proto / protobuf / protoc | Protobuf |
| openapi / swagger / OpenAPI 3.x | OpenAPI |
| graphql / schema.graphql / Apollo | GraphQL |
| Docker / docker-compose / container | Docker |
| .github/workflows / GitHub Actions | GitHub Actions |
| .gitlab-ci.yml / GitLab CI | GitLab CI |
| Jenkinsfile / Jenkins | Jenkins |

**输出**：`技术栈判定表`

```markdown
| 维度 | 判定结果 | 依据 |
|------|---------|------|
| 编译语言 | Go, C++ | go.work + CMakeLists.txt |
| 数据库 | PostgreSQL | ART-003 数据设计 |
| 契约 | Protobuf, OpenAPI | IFC-004, IFC-006 |
| 容器化 | Docker | docker-compose.dev.yml |
| CI 平台 | GitHub Actions | .github/workflows/ |
```

**边界处理**：
- 若某个语言的构建文件信号无法确定（如 `build.gradle` vs `build.gradle.kts`），默认选择更常见的那一种，并在记录中标注
- 若设计文档中的信息不足以判定，**仅在这种情况下**向用户确认

---

## 阶段 2：路由判定

将阶段 1 的判定表输入决策矩阵，确定需要创建哪些基础设施模块。具体工具选择从 references/ 引用文件查表，不在本流程中硬编码。

```
识别到的技术要素              对应基础设施模块              工具细节参考
──────────────────────────────────────────────────────────────────
存在关系数据库                 需要 migration/ + model/        references/database-routing.md
存在 ≥2 种编译语言             需要 contracts/ 契约层         references/contract-routing.md
存在 Protobuf                 需要 proto/ + 生成脚本          references/contract-routing.md
存在 OpenAPI → REST           需要 openapi/ + lint 配置       references/contract-routing.md
存在 GraphQL                  需要 graphql/ + schema 文件     references/contract-routing.md
存在 Go                       需要 go.mod + 最小 main         references/language-routing.md
存在 C++                      需要 CMakeLists.txt + main.cpp  references/language-routing.md
存在 Rust                     需要 Cargo.toml + main.rs       references/language-routing.md
存在 Java(Maven)              需要 pom.xml + 源码目录          references/language-routing.md
存在 Java(Gradle)             需要 build.gradle + 源码目录     references/language-routing.md
存在 Python                   需要 pyproject.toml + __init__  references/language-routing.md
存在 TypeScript               需要 package.json + tsconfig    references/language-routing.md
存在 C#/.NET                  需要 .csproj + Program.cs       references/language-routing.md
存在 Docker                   需要 Dockerfile + compose 文件   组合判定（见阶段 4）
常用语言 ≥ 2 个模块/包         需要 workspace 机制             references/language-routing.md 对应行
存在 CI 平台                  需要对应 workflow 文件           按 CI 平台文件名生成
```

**路由铁律**：
- "存在 ≥2 种编译语言"这个判定**只看编译语言**（Go/C++/Rust/Java/C# 等），不包括 SQL / YAML / JSON 这类配置语言
- 若只有 1 种编译语言，无条件跳过 contracts/ 层（无跨语言契约同步需求）
- 若存在关系数据库但设计文档未指定迁移工具，从 `database-routing.md` 中选取该数据库生态最常用的工具

**输出**：`基础设施模块清单`，按类型分组，每个模块标注：
- 是否需要创建
- 路由依据（从哪个技术要素触发的）
- 工具选择（从哪个引用文件查到的）
- 输出路径

---

## 阶段 3：依赖排序

模块间存在硬依赖关系。按以下层排列执行顺序，同层内可并行：

```
第 0 层（无依赖，最先执行）:
  ├─ 仓库顶层目录结构
  └─ .gitignore

第 1 层（仅依赖第 0 层）:
  ├─ contracts/proto/           ← 若存在 Protobuf
  ├─ contracts/openapi/         ← 若存在 OpenAPI
  ├─ contracts/graphql/         ← 若存在 GraphQL
  └─ db/migration/              ← 若存在关系数据库

第 2 层（依赖第 1 层的生成产物）:
  ├─ 代码生成脚本               ← 若存在 Protobuf
  └─ db/model/                  ← 依赖 migration/ 已创建

第 3 层（依赖第 2 层的生成产物）:
  ├─ 各语言的构建骨架            ← 若存在 Proto 需等生成代码就位
  ├─ workspace 配置             ← 若语言级需要（go.work / Cargo workspace 等）
  └─ .editorconfig / .clang-format 等编辑器配置

第 4 层（依赖第 3 层构建系统就位）:
  ├─ docker-compose.dev.yml     ← 若存在 Docker + 数据库
  ├─ Dockerfile.build-*         ← 若编译环境需容器化（如 C++ 交叉编译）
  └─ CI workflow 文件           ← 若存在 CI 平台

第 5 层（依赖所有前序层）:
  └─ 端到端验证                  ← 编译 + 迁移 + 启动全链路
```

**依赖铁律**：
- contracts 层是跨语言的单一事实来源，必须在任何语言工程之前就位
- 数据库迁移（DDL）必须在 model 代码之前（model 反映 DDL 的结构）
- Docker 和 CI 必须在各语言工程能编译通过之后才能验证

**输出**：`执行顺序表` — 按层排列的任务列表，标注同层内可并行的任务对。

---

## 阶段 4：逐模块执行

按阶段 3 的顺序，对每个模块执行"创建 → 验证 → 记录"三步循环。同一层内无依赖关系的模块可并行创建。

### 4.1 目录结构

按阶段 2 的模块清单创建目录。顶层目录命名遵循设计文档中的模块拓扑（如 edge/ vs center/，或 core/ vs services/），不强制使用固定命名。

创建 `.gitignore`，覆盖所有识别的编译语言对应的构建产物和 IDE 文件。具体忽略规则从 `references/language-routing.md` 各语言的"构建产物"列获取。

### 4.2 契约层

根据 `references/contract-routing.md` 中对应契约类型的模板创建文件：

- **Protobuf**：创建 `.proto` 文件，内容从设计文档的接口契约提取 message/service 定义。创建 `scripts/protoc-gen.sh` 生成脚本，覆盖所有编译语言的代码生成命令
- **OpenAPI**：创建 `openapi.yaml`，内容从设计文档的 REST API 定义提取。配置 lint 工具（如 `redocly`）
- **GraphQL**：创建 `schema.graphql`，配置 schema 校验

**验证**：运行生成脚本（Protobuf）或 lint 命令（OpenAPI/GraphQL），确认零错误。

### 4.3 数据库迁移

根据 `references/database-routing.md` 中对应数据库的迁移工具创建基线脚本：

- 从设计文档的数据设计章节提取 DDL，生成 `V1__baseline.sql`（或对应工具的等效文件）
- 表名、字段名、类型、约束**必须与设计文档完全一致**，不做自行发挥

**验证**：启动数据库容器 → 执行迁移命令 → 确认所有表创建成功。

### 4.4 语言构建骨架

对每种识别的编译语言，从 `references/language-routing.md` 查表获取：
- 构建命令
- 包管理命令
- 静态检查命令
- 测试运行命令
- 最小骨架文件列表和内容模板

每种语言创建以下通用结构：
1. **构建描述文件**（go.mod / Cargo.toml / pom.xml / pyproject.toml / package.json / .csproj）——声明语言版本和最小依赖
2. **入口文件**（main.go / main.cpp / main.rs / Main.java / main.py / index.ts / Program.cs）——打印版本号或输出 "ready"，不写业务逻辑
3. **测试桩**——一个空测试或断言 `true` 的测试，验证测试框架可用
4. **项目级目录**——按设计文档中的模块拓扑创建内部目录，但目录内暂不放文件

**验证**（对每种语言依次执行）：
1. 构建命令 → 确认编译成功
2. 静态检查命令 → 确认零 warning
3. 测试运行命令 → 确认测试通过

若验证失败，在当前语言内修复后重试。不同语言之间的验证失败可以独立处理，不需要回到起点。

### 4.5 容器化配置

仅在识别到 Docker 时创建：

- **docker-compose.dev.yml**：包含数据库（从阶段 1 判定）+ 其他中间件依赖。端口映射避免与宿主机常见端口冲突
- **Dockerfile.build-xxx**：仅当某编译语言需要预编译构建镜像时创建（如 C++ 需要 GStreamer/NPU-SDK 等系统库）。若语言的构建依赖可通过包管理器简单安装（Go 的 go mod、Rust 的 cargo build），则不需要单独的构建镜像

**验证**：`docker compose up -d` → 健康检查通过 → `docker compose down`

### 4.6 CI 配置

根据 CI 平台创建对应 workflow 文件。按阶段 2 识别的编译语言创建分层触发规则：

- **契约层变更** → 触发代码生成校验
- **某语言目录变更** → 触发该语言的构建 + 测试
- **全量集成** → 仅在 main/develop 分支合并前触发

从 `references/language-routing.md` 获取每种语言的构建和测试命令，填入 workflow 的 steps。

**验证**：运行 CI 平台的 lint 工具（如 `actionlint` for GitHub Actions、`gitlab-ci-lint` for GitLab CI）。

### 4.7 执行记录

每个模块创建完成后记录：
- 产出文件路径列表
- 验证命令及输出摘要
- 若验证失败过，记录失败原因和修复方式

---

## 阶段 5：端到端验证

所有模块创建完成后，按阶段 3 的依赖顺序运行全链路验证。任一环节失败，修复后从失败点继续，不回到开头。

```
验证序列（按依赖排序，存在则执行，不存在则跳过）:
  1. 契约生成:  代码生成脚本 → 确认生成的代码编译通过
  2. 数据库:    docker compose up db → 迁移工具执行 → 确认所有表存在
  3. Go:        go build ./... → go vet ./... → go test ./...
  4. C++:       cmake --build build → ctest
  5. Rust:      cargo build → cargo clippy → cargo test
  6. Java:      mvn/gradle build → mvn/gradle test
  7. Python:    pip install -e . → pytest 或等效
  8. TypeScript: npm run build → npx tsc --noEmit → npm run test
  9. C#:        dotnet build → dotnet test
  10. Docker:   docker compose up -d → curl 健康检查 → docker compose down
  11. CI:       对应平台 lint 工具
```

各语言的验证命令从 `references/language-routing.md` 查表获取，不硬编码。

**输出**：`端到端验证报告`

```markdown
| 序号 | 验证项 | 命令 | 结果 | 耗时 | 备注 |
|------|--------|------|------|------|------|
| 1 | Proto 生成 | protoc-gen.sh | PASS | 2s | |
| 2 | 数据库迁移 | flyway migrate | PASS | 5s | |
| 3 | Go 构建 | go build ./... | PASS | 8s | |
| ... | ... | ... | ... | ... | |
```

---

## 输出

1. **可运行的工程基座**：所有语言能编译、数据库能迁移、Docker 能启动
2. **端到端验证报告**：每步验证结果，失败项及修复记录
3. **checkpoint commit**：将全部基础设施产出提交为一次 checkpoint commit

---

## 与上下游 Skill 的关系

| 位置 | Skill | 关系 |
|------|-------|------|
| 上游 | `implementation-kickoff` | 消费其产出的设计文档，作为 Plan A 的第一步 |
| 上游 | `implementation-plan-generation` | 由其生成 Plan A 任务，调用本 Skill 执行 |
| 下游 | `subagent-driven-development` / `orchestrating-fresh-subagents` | 本 Skill 产出工程基座后，编码 Skill 在此基础上编写业务代码 |
| 下游 | `design-drift-audit` | 不直接关联（不同阶段的检查点） |

## 引用文件

当需要查明"某种语言用什么构建命令"、"某种数据库用什么迁移工具"时，读取对应文件：

- `references/language-routing.md` — 编译语言 → 构建/包管理/检查/测试/骨架模板
- `references/database-routing.md` — 数据库 → 迁移工具/驱动/DDL 特征
- `references/contract-routing.md` — 契约类型 → 生成工具/lint 工具/代码输出格式
