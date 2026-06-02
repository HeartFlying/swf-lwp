# swf-lwp GitHub 推送实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 补全 swf-lwp 项目的开源文档并推送到 GitHub 新建公开仓库。

**Architecture:** 基于已批准的设计文档，按文件逐个创建/修改，最后统一提交并推送。无复杂架构，纯文档与 Git 操作。

**Tech Stack:** Git, GitHub CLI (`gh`)

---

### Task 1: 创建 LICENSE（MIT）

**Files:**
- Create: `LICENSE`

- [ ] **Step 1: 写入 MIT 许可证全文**

```text
MIT License

Copyright (c) 2026 hxie

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

### Task 2: 更新 README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: 修正安装路径为 `swf-lwp`**

将 `README.md` 第 16 行：

```bash
claude plugin install /path/to/srs-work-v4-skill/.claude-plugin
```

替换为：

```bash
claude plugin install /path/to/swf-lwp/.claude-plugin
```

- [ ] **Step 2: 在标题下方添加仓库链接段落（插入到第 3 行之后）**

```markdown
[![GitHub](https://img.shields.io/badge/GitHub-hxie%2Fswf--lwp-blue)](https://github.com/hxie/swf-lwp)
```

---

### Task 3: 创建 CONTRIBUTING.md

**Files:**
- Create: `CONTRIBUTING.md`

- [ ] **Step 1: 写入贡献指南**

```markdown
# 贡献指南

感谢你对 swf-lwp 项目的关注！

## 如何安装开发环境

1. 克隆仓库：`git clone https://github.com/hxie/swf-lwp.git`
2. 进入目录：`cd swf-lwp`
3. 安装插件：`claude plugin install ./.claude-plugin`

## 如何提交 Issue

- 请使用对应的 Issue 模板（Bug 报告或功能请求）
- 尽可能提供复现步骤和上下文信息

## 如何提交 Pull Request

1. Fork 本仓库
2. 创建你的功能分支：`git checkout -b feature/my-feature`
3. 提交更改：`git commit -m "feat: add my feature"`
4. 推送到分支：`git push origin feature/my-feature`
5. 打开一个 Pull Request，并填写 PR 模板

## 代码规范

- 遵循现有代码风格和目录结构
- 修改文件前先阅读现状和相邻边界
```

---

### Task 4: 创建 CODE_OF_CONDUCT.md

**Files:**
- Create: `CODE_OF_CONDUCT.md`

- [ ] **Step 1: 写入行为准则**

```markdown
# 行为准则

## 我们的承诺

为了营造一个开放和友好的环境，我们作为贡献者和维护者承诺：无论年龄、体型、残疾、种族、性别特征、性别认同和表达、经验水平、教育、社会经济地位、国籍、个人外貌、种族、宗教或性身份和取向如何，参与我们的项目和社区的每个人都不会受到骚扰。

## 我们的标准

有助于创造积极环境的行为包括：

- 使用友好和包容的语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

不可接受的行为包括：

- 使用性化语言或图像，以及不受欢迎的性关注或挑逗
- 恶意挑衅、侮辱/贬损性评论，以及人身或政治攻击
- 公开或私下骚扰
- 未经明确许可发布他人的私人信息，如物理或电子地址
- 其他在专业环境中可合理认定为不适当的行为

## 执行

可通过 [GitHub Issues](https://github.com/hxie/swf-lwp/issues) 向项目维护者举报滥用、骚扰或其他不可接受的行为。

## 来源

本行为准则改编自 [Contributor Covenant](https://www.contributor-covenant.org)，版本 2.1。
```

---

### Task 5: 创建 docs/.gitkeep

**Files:**
- Create: `docs/.gitkeep`

- [ ] **Step 1: 创建空文件保留 docs 目录**

```bash
# 空文件，用于保留 docs 目录
```

文件内容为空即可。

---

### Task 6: 创建 GitHub Issue 模板

**Files:**
- Create: `.github/ISSUE_TEMPLATE/bug_report.md`
- Create: `.github/ISSUE_TEMPLATE/feature_request.md`

- [ ] **Step 1: 创建 Bug 报告模板**

```markdown
---
name: Bug 报告
about: 报告一个问题
title: '[Bug] '
labels: bug
assignees: ''

---

## 问题描述

清晰简洁地描述 Bug。

## 复现步骤

1. 步骤一
2. 步骤二
3. 步骤三

## 预期行为

描述你期望发生的行为。

## 实际行为

描述实际发生的行为。

## 环境信息

- 操作系统：
- Claude Code 版本：
- 插件版本：

## 附加信息

添加任何其他上下文或截图。
```

- [ ] **Step 2: 创建功能请求模板**

```markdown
---
name: 功能请求
about: 建议一个新功能
title: '[Feature] '
labels: enhancement
assignees: ''

---

## 功能描述

清晰简洁地描述你希望添加的功能。

## 使用场景

描述这个功能会在什么场景下使用，解决什么问题。

## 可能的实现方案

如果你有任何实现思路，请在这里描述。

## 替代方案

你是否考虑过其他替代方案？

## 附加信息

添加任何其他上下文或截图。
```

---

### Task 7: 创建 GitHub PR 模板

**Files:**
- Create: `.github/PULL_REQUEST_TEMPLATE.md`

- [ ] **Step 1: 写入 PR 模板**

```markdown
## 变更内容

描述这个 PR 做了什么变更。

## 相关 Issue

Fixes #(issue 编号)

## 检查清单

- [ ] 我已阅读并遵循了贡献指南
- [ ] 我的变更不会产生新的警告
- [ ] 我已测试了我的变更

## 附加说明

添加任何其他说明或截图。
```

---

### Task 8: Git 初始化与提交

**Files:**
- 所有新增/修改的文件

- [ ] **Step 1: 初始化 Git 仓库**

Run: `git init`
Expected: `Initialized empty Git repository in ...`

- [ ] **Step 2: 添加所有文件**

Run: `git add .`
Expected: 无输出（成功）

- [ ] **Step 3: 提交**

Run: `git commit -m "initial commit with full documentation"`
Expected: 显示若干文件被创建/修改的统计信息

---

### Task 9: GitHub 仓库创建与推送

- [ ] **Step 1: 使用 gh CLI 创建公开仓库并推送**

Run: `gh repo create swf-lwp --public --source=. --push`
Expected: 输出类似 `✓ Created repository hxie/swf-lwp on GitHub`

- [ ] **Step 2: 验证推送成功**

Run: `git remote -v`
Expected: 显示 `origin  https://github.com/hxie/swf-lwp.git`

Run: `git log --oneline -1`
Expected: 显示 `initial commit with full documentation`

---

## 自检

1. **设计覆盖：** 所有设计文档中的文件（LICENSE、README、CONTRIBUTING、CODE_OF_CONDUCT、docs/.gitkeep、.github 模板）均有对应任务。
2. **无占位符：** 每个任务均包含可直接复制执行的完整内容。
3. **一致性：** README 中的仓库链接、Issue 模板中的仓库链接、贡献指南中的克隆地址均一致指向 `hxie/swf-lwp`。
