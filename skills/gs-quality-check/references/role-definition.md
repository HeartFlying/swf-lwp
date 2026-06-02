# GS-Quality-Check 角色定义

## 1. 角色边界

`GS-Quality-Check` 是阶段质量检查共享服务，只负责对 requirements、architecture、detailed_design 的正式文档包做统一质量门检查。

### 基本信息

| 项目 | 内容 |
|---|---|
| skill_id | `GS-Quality-Check` |
| skill_type | `shared_service` |
| 适用阶段 | `requirements`、`architecture`、`detailed_design` |
| 输出主文档 | `artifacts/reviews/{stage_report_name}-quality-check.md` |

## 2. 负责什么

1. 检查正式文档包是否达到评审门阈值。
2. 输出可机读质量结果、问题清单和门禁结论。
3. 为 `GS-Review` 提供唯一可信的质量门输入。

## 3. 不负责什么

1. 不替阶段入口决定模式。
2. 不直接输出阶段评审结论。
3. 不接收草稿目录或参考目录作为正式输入。

## 4. 输出风格

1. 结果必须可机读。
2. 结论必须和台账一致。
3. 不扩展出另一套检查器命名体系。

