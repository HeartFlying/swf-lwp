# Language Routing Reference

编译语言到构建系统、包管理、检查工具、测试框架和最小骨架的映射表。新增一种语言时只需在此表加一行，不动 SKILL.md。

## 路由表

| 语言 | 构建命令 | 包管理 | 静态检查 | 测试运行 | Workspace 工具 | 最小骨架文件 | 构建产物(需进 .gitignore) |
|------|----------|--------|----------|----------|---------------|-------------|--------------------------|
| **Go** | `go build ./...` | `go mod tidy` | `go vet ./...` | `go test ./...` | `go.work` (≥2 modules) | `go.mod` + `cmd/main.go` | `*.exe`, `*.test`, 二进制文件 |
| **C++** | `cmake -B build -S . && cmake --build build` | (无包管理器，依赖系统库或 FetchContent) | `-Werror` (CMake 编译选项) | `ctest --output-on-failure` | (无) | `CMakeLists.txt` + `src/main.cpp` + `tests/CMakeLists.txt` | `build/`, `*.o`, `*.obj`, `*.so`, `*.dll`, `*.a` |
| **Rust** | `cargo build` | `cargo` | `cargo clippy -- -D warnings` | `cargo test` | `Cargo.toml` 中 `[workspace]` (≥2 crates) | `Cargo.toml` + `src/main.rs` | `target/` |
| **Java (Maven)** | `mvn compile` | `mvn dependency:resolve` | `mvn checkstyle:check` | `mvn test` | `<modules>` in parent pom.xml | `pom.xml` + `src/main/java/<pkg>/Main.java` + `src/test/java/<pkg>/MainTest.java` | `target/` |
| **Java (Gradle)** | `gradle build` | `gradle dependencies` | `gradle check` | `gradle test` | `settings.gradle` + multi-project | `build.gradle` (或 `.kts`) + `src/main/java/<pkg>/Main.java` | `build/`, `.gradle/` |
| **Python** | (无编译步骤，语法检查用 `python -m compileall .`) | `pip install -e .` 或 `poetry install` | `ruff check .` 或 `flake8` | `pytest` | (无，用 venv 隔离) | `pyproject.toml` 或 `setup.py` + `src/<pkg>/__init__.py` | `__pycache__/`, `*.pyc`, `*.egg-info/`, `dist/` |
| **TypeScript** | `npm run build` (tsc 或 vite build) | `npm install` | `npx tsc --noEmit` | `npm run test` (vitest/jest) | npm workspaces (`package.json` 中 `"workspaces"`) 或 pnpm workspaces | `package.json` + `tsconfig.json` + `src/index.ts` | `node_modules/`, `dist/`, `.tsbuildinfo` |
| **C# / .NET** | `dotnet build` | `dotnet restore` | `dotnet format` | `dotnet test` | `.sln` 文件 (≥2 projects) | `<Project>.csproj` + `Program.cs` | `bin/`, `obj/` |

## 最小骨架内容模板

### Go
```
<module-dir>/
├── go.mod             ← module <module-path>\n\ngo 1.22
├── cmd/
│   └── main.go        ← package main\n\nimport "fmt"\n\nfunc main() { fmt.Println("ready") }
└── internal/           ← (空目录，后续业务代码在此)
```

### C++
```
<algorithm-dir>/
├── CMakeLists.txt      ← cmake_minimum_required + project + add_executable + enable_testing + add_subdirectory(tests)
├── src/
│   └── main.cpp        ← #include <iostream>\nint main() { std::cout << "ready" << std::endl; return 0; }
└── tests/
    ├── CMakeLists.txt  ← find_package(GTest) + add_executable + gtest_discover_tests
    └── test_main.cpp   ← #include <gtest/gtest.h>\nTEST(Smoke, Ready) { EXPECT_TRUE(true); }
```

### Rust
```
<project-dir>/
├── Cargo.toml          ← [package] name + version + edition = "2021"
├── src/
│   └── main.rs         ← fn main() { println!("ready"); }
└── tests/
    └── smoke.rs        ← #[test]\nfn ready() { assert!(true); }
```

### Java (Maven)
```
<project-dir>/
├── pom.xml              ← groupId + artifactId + version + properties(maven.compiler) + dependencies(junit)
├── src/
│   ├── main/java/<pkg>/
│   │   └── Main.java    ← public class Main { public static void main(String[] args) { System.out.println("ready"); } }
│   └── test/java/<pkg>/
│       └── MainTest.java ← import org.junit.*; public class MainTest { @Test public void ready() { assertTrue(true); } }
```

### Python
```
<project-dir>/
├── pyproject.toml       ← [project] name + version + requires-python + [project.optional-dependencies] dev(pytest)
├── src/<pkg>/
│   └── __init__.py      ← (空文件，标记为 package)
└── tests/
    └── test_smoke.py    ← def test_ready(): assert True
```

### TypeScript
```
<project-dir>/
├── package.json         ← "name" + "scripts"{"build":"tsc","test":"vitest run"}
├── tsconfig.json        ← "compilerOptions"{"target":"ES2022","module":"ESNext","strict":true}
├── src/
│   └── index.ts         ← console.log("ready")
└── tests/
    └── smoke.test.ts    ← import { describe, it, expect } from 'vitest'\ndescribe('smoke', () => { it('ready', () => { expect(true).toBe(true) }) })
```

### C# / .NET
```
<project-dir>/
├── <Project>.csproj     ← <Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><OutputType>Exe</OutputType><TargetFramework>net8.0</TargetFramework>...
├── Program.cs           ← Console.WriteLine("ready");
└── Tests/
    ├── Tests.csproj     ← 引用主项目 + coverlet + xunit
    └── SmokeTest.cs     ← using Xunit; public class SmokeTest { [Fact] public void Ready() { Assert.True(true); } }
```

## 未覆盖语言的处理

若设计文档中出现本表未列出的编译语言（如 Kotlin、Swift、Zig 等），按以下优先级处理：
1. 在同生态中查找最接近语言的配置（如 Kotlin → Gradle、Swift → SwiftPM）
2. 若无法推断，仅创建该语言的入口文件和构建占位注释，标注 `FIXME: 需补充 <语言名> 构建配置`
3. 在端到端验证报告中记录为 ENV_GAP，继续处理其他语言
