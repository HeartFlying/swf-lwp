#!/bin/bash

set -e

########################################

# 防递归

########################################

if [ "$CLAUDE_SUMMARY_INTERNAL" = "true" ]; then
exit 0
fi

export CLAUDE_SUMMARY_INTERNAL=true

########################################

# Git检查

########################################

if git rev-parse --git-dir >/dev/null 2>&1; then
if git diff --quiet HEAD 2>/dev/null; then
echo "No changes."
exit 0
fi
fi

########################################

# 路径

########################################

MEMORY_DIR=".claude/memory"

mkdir -p "$MEMORY_DIR"

TODAY=$(date +%F)

JSONL_FILE="${MEMORY_DIR}/${TODAY}.jsonl"

########################################

# Prompt

########################################

PROMPT=$(cat <<EOF
分析当前工作区：

* git status
* git diff
* 当前上下文

输出严格JSON：

{
"timestamp":"",
"task":"",
"completed":[],
"files":[],
"decisions":[],
"issues":[],
"next":[]
}

不要解释
不要markdown
EOF
)

RESULT=$(claude -p "$PROMPT")

echo "$RESULT" >> "$JSONL_FILE"

echo "Memory saved: $JSONL_FILE"
