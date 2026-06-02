#!/bin/bash

MONTH=$(date +%Y-%m)

mkdir -p .claude/reports/monthly

DATA=$(cat .claude/memory/*.jsonl)

PROMPT=$(cat <<EOF
根据以下JSONL生成项目月报：

$DATA

输出：

# 月报

## 项目进展

## 关键成果

## 重要技术决策

## 风险

## 下月计划

EOF
)

claude -p "$PROMPT" > ".claude/reports/monthly/${MONTH}.md"
