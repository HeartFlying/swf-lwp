#!/bin/bash

DATE=${1:-$(date +%F)}

FILE=".claude/memory/${DATE}.jsonl"

if [ ! -f "$FILE" ]; then
echo "No memory found."
exit 1
fi

PROMPT=$(cat <<EOF
根据以下JSONL记录生成Markdown日报：

$(cat "$FILE")

格式：

# 工作日报

## 今日完成

## 关键决策

## 遇到问题

## 明日计划

EOF
)

mkdir -p .claude/reports/daily

claude -p "$PROMPT" > ".claude/reports/daily/${DATE}.md"

echo "Daily report generated."
