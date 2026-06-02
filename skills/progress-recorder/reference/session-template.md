# Session Record Template

Template for generating daily session record files.

## File Naming
`{YYYY-MM-DD}.md`

## Template Structure

```markdown
# Session Record: {YYYY-MM-DD}

## Basic Information

| Item | Content |
|------|---------|
| Session Date | {YYYY-MM-DD} |
| Session Topic | {topic} |
| Status | {In Progress / Completed} |

---

## Work Results

### Completed Tasks

1. **{task-name-1}**
   - {task-detail-1}
   - {task-detail-2}

2. **{task-name-2}**
   - {task-detail-1}

### Created Files

| File Path | Description |
|-----------|-------------|
| `{file-path-1}` | {file-description-1} |
| `{file-path-2}` | {file-description-2} |

---

## File Changes

| Operation Type | File Path | Description |
|----------------|-----------|-------------|
| {Create/Modify/Delete} | `{file-path}` | {description} |

---

## Todo Items

| Task | Priority | Status | Description |
|------|----------|--------|-------------|
| {task-desc} | {P0/P1/P2} | {Pending/In Progress} | {detail} |

---

## Issues and Solutions

| Issue | Solution | Status |
|-------|----------|--------|
| {issue-desc} | {solution-desc} | {Resolved/Pending} |

---

## Key Decisions

| Decision Content | Decision Reason | Impact |
|------------------|-----------------|--------|
| {decision-content} | {reason} | {impact} |

---

## Session Summary

{summary-content}

---

*Created At: {timestamp}*
```

## Variable Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `{YYYY-MM-DD}` | Session date | 2026-03-21 |
| `{topic}` | Session topic/title | Skill System Development |
| `{task-name}` | Task name | Project Initialization |
| `{file-path}` | Relative file path | `.ai_memory/progress/index.md` |
| `{P0/P1/P2}` | Priority level | P0 = Critical, P1 = High, P2 = Normal |
| `{timestamp}` | Creation timestamp | 2026-03-21 23:51:00 |
