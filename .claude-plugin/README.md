# SWF Plugin

软件研发工作流（Software Workflow Framework）插件，为 Claude Code 提供产品研发全阶段的能力扩展。

[![GitHub](https://img.shields.io/badge/GitHub-hxie%2Fswf--lwp-blue)](https://github.com/hxie/swf-lwp)

## 功能

覆盖软件研发的三大核心阶段：

- **需求分析**（G100~G103）：业务背景分析、需求基线定义、MVP 范围收敛
- **架构设计**（G200~G204）：技术策略、架构愿景、蓝图定义、架构评审
- **详细设计**（G300~G401）：组件设计、接口设计、数据设计、技术实现

## 安装

```bash
claude plugin install /path/to/swf-lwp/.claude-plugin
```

## 包含的 Skills

| Skill | 说明 |
|-------|------|
| g100-requirements-entry | 需求阶段入口编排 |
| g101-business-context | 业务背景分析 |
| g102-requirements-baseline | 需求基线定义 |
| g103-mvp-definition | MVP 范围定义 |
| g200-architecture-entry | 架构阶段入口编排 |
| g201-technical-strategy | 技术策略定义 |
| g202-architecture-vision | 架构愿景定义 |
| g203-architecture-blueprint | 架构蓝图定义 |
| g204-architecture-review | 架构评审验证 |
| g300-detailed-design-entry | 详细设计阶段入口编排 |
| g301-component-design | 组件详细设计 |
| g302-interface-design | 接口详细设计 |
| g303-data-design | 数据详细设计 |
| g401-technology-realization | 技术实现决策 |
| gs-quality-check | 阶段质量检查 |
| gs-review | 阶段汇总评审 |
| layered-parallel-implementation | 分层并行实施 |
| prd-design-readiness-review | PRD 设计就绪评审 |
| progress-recorder | 进度记录与恢复 |
| reviewing-software-design | 软件设计评审 |
| software-fmea-review | FMEA 失效模式分析 |
| feature-detailed-design | Feature 详细设计 |

## 使用

安装后，在 Claude Code 中通过 `/skill-name` 调用各阶段 skill。

例如：
- `/g100-requirements-entry` 启动需求分析阶段
- `/g200-architecture-entry` 启动架构设计阶段
- `/g300-detailed-design-entry` 启动详细设计阶段

## 作者

hxie

## 许可证

MIT
