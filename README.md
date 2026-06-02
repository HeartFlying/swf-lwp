# SWF-LWP（软件研发工作流插件）

[![GitHub](https://img.shields.io/badge/GitHub-hxie%2Fswf--lwp-blue)](https://github.com/hxie/swf-lwp)

为 Claude Code 提供产品研发全阶段能力扩展的插件集合，覆盖需求分析、架构设计、详细设计三大核心阶段。

## 项目概述

SWF（Software Workflow Framework）是一组结构化、可复用的 Claude Code Skills，旨在将软件工程的最佳实践融入 AI 辅助编程工作流。通过分阶段、分层次的 Skill 设计，帮助团队在产品研发各阶段保持一致的方法论和输出标准。

## 覆盖阶段

| 阶段 | 编号 | 说明 |
|------|------|------|
| **需求分析** | G100~G103 | 业务背景分析、需求基线定义、MVP 范围收敛 |
| **架构设计** | G200~G204 | 技术策略、架构愿景、蓝图定义、架构评审 |
| **详细设计** | G300~G401 | 组件设计、接口设计、数据设计、技术实现 |

## 仓库结构

```
swf-lwp/
├── .claude-plugin/          # 插件入口（plugin.json、marketplace.json、README）
├── skills/                  # 所有 Skill 定义
│   ├── _shared/            # 共享模板与治理规范
│   ├── g100~g103/          # 需求分析阶段 Skills
│   ├── g200~g204/          # 架构设计阶段 Skills
│   ├── g300~g401/          # 详细设计阶段 Skills
│   └── gs-*/               # 通用治理与质量 Skills
├── commands/               # 插件命令（预留）
├── docs/                   # 设计文档与执行计划
├── .github/                # GitHub 模板与 CI 配置
├── LICENSE                 # MIT 许可证
├── CONTRIBUTING.md         # 贡献指南
└── CODE_OF_CONDUCT.md      # 行为准则
```

## 安装

### 方式一：从 GitHub 安装（推荐）

```bash
claude plugin marketplace add https://github.com/HeartFlying/swf-lwp
claude plugin install swf
```

### 方式二：本地安装

```bash
git clone https://github.com/HeartFlying/swf-lwp.git
claude plugin install ./swf-lwp/.claude-plugin
```

安装后执行 `/reload-plugins` 加载 Skills。

## 包含的 Skills

共 22 个 Skills，涵盖产品研发全阶段：

**需求分析（4 个）**
- `g100-requirements-entry` — 需求阶段入口编排
- `g101-business-context` — 业务背景分析
- `g102-requirements-baseline` — 需求基线定义
- `g103-mvp-definition` — MVP 范围定义

**架构设计（5 个）**
- `g200-architecture-entry` — 架构阶段入口编排
- `g201-technical-strategy` — 技术策略定义
- `g202-architecture-vision` — 架构愿景定义
- `g203-architecture-blueprint` — 架构蓝图定义
- `g204-architecture-review` — 架构评审验证

**详细设计（6 个）**
- `g300-detailed-design-entry` — 详细设计阶段入口编排
- `g301-component-design` — 组件详细设计
- `g302-interface-design` — 接口详细设计
- `g303-data-design` — 数据详细设计
- `g401-technology-realization` — 技术实现决策
- `feature-detailed-design` — Feature 详细设计

**通用治理（7 个）**
- `gs-quality-check` — 阶段质量检查
- `gs-review` — 阶段汇总评审
- `layered-parallel-implementation` — 分层并行实施
- `prd-design-readiness-review` — PRD 设计就绪评审
- `progress-recorder` — 进度记录与恢复
- `reviewing-software-design` — 软件设计评审
- `software-fmea-review` — FMEA 失效模式分析

## 使用示例

安装后在 Claude Code 中通过 `/skill-name` 调用：

```
/g100-requirements-entry    # 启动需求分析阶段
/g200-architecture-entry    # 启动架构设计阶段
/g300-detailed-design-entry # 启动详细设计阶段
```

## CI 状态

本仓库使用 GitHub Actions 进行持续集成，检查项包括：
- JSON 语法验证（plugin.json、marketplace.json）
- Shell 脚本语法检查
- 必需文件存在性检查
- Skills 目录结构完整性

## 贡献

欢迎提交 Issue 和 Pull Request。请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可证

[MIT](LICENSE)
