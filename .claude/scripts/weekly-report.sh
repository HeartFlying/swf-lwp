#!/bin/bash

mkdir -p .claude/reports/weekly

WEEK=$(date +%Y-W%U)

DATA=""

for file in .claude/memory/*.jsonl
do
DATA="$DATA\n$(cat "$file")"
done

PROMPT=$(cat <<EOF
根据以下JSONL记录生成本周工作周报：

$DATA

输出：

# 本周工作总结

## 完成事项

## 技术决策

## 风险问题

## 下周计划

EOF
)

claude -p "$PROMPT" > ".claude/reports/weekly/${WEEK}.md"
