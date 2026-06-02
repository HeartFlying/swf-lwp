# swf-lwp GitHub 推送设计

## 目标

将 `swf-lwp` 项目以完整公开仓库形态推送到 GitHub，首次提交即包含所有必要文档。

## 背景

- 项目当前无 `.git` 仓库，需初始化
- `README.md` 中声明 MIT 许可证，但无实际 `LICENSE` 文件
- 公开仓库需补充开源协作文档

## 文档清单

| 文件/目录 | 说明 |
|-----------|------|
| `LICENSE` | MIT 许可证全文 |
| `README.md` | 更新安装路径为 `swf-lwp`、补充仓库链接 |
| `CONTRIBUTING.md` | 贡献指南（安装、Issue、PR） |
| `CODE_OF_CONDUCT.md` | 行为准则（Contributor Covenant） |
| `docs/.gitkeep` | 保留 docs 目录（暂不创建子目录） |
| `.github/ISSUE_TEMPLATE/bug_report.md` | Bug 报告模板 |
| `.github/ISSUE_TEMPLATE/feature_request.md` | 功能请求模板 |
| `.github/PULL_REQUEST_TEMPLATE.md` | PR 描述模板 |

## 执行流程

1. 本地创建上述所有文件
2. `git init`
3. `git add .`
4. `git commit -m "initial commit with full documentation"`
5. `gh repo create swf-lwp --public --source=. --push`

## 成功标准

- GitHub 上 `hxie/swf-lwp` 仓库可见且为 Public
- 默认分支为 `main`
- 包含完整的开源文档（LICENSE、README、CONTRIBUTING、CODE_OF_CONDUCT）
- `.github/` Issue/PR 模板生效
