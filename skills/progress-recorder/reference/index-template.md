# Index Template

Template for generating and maintaining the project progress index file.

## Table of Contents

- [File Naming](#file-naming)
- [Template Structure](#template-structure)
- [Variable Reference](#variable-reference)
- [Index Update Rules](#index-update-rules)
- [Example](#example)

## File Naming

`index.md`

Fixed name, located at `./.ai_memory/progress/index.md`

## Template Structure

```markdown
# Project Progress Index

## Project Overview

| Item | Content |
|------|---------|
| Project Name | {project-name} |
| Current Status | {current-status} |
| Last Updated | {YYYY-MM-DD} |

---

## Recent Sessions

| Date | Topic | Core Results | Detail Link |
|------|-------|--------------|-------------|
| {YYYY-MM-DD} | {latest-topic} | {latest-results} | [View]({YYYY-MM-DD}.md) |
| {YYYY-MM-DD} | {historical-topic} | {historical-results} | [View]({YYYY-MM-DD}.md) |

---

## Core Content Index

### Decisions

<!-- List all decision records with links -->
- [DEC-001: {decision-title}](core/decisions/DEC-001.md)
- [DEC-002: {decision-title}](core/decisions/DEC-002.md)

*No decision records yet*

### Architecture

<!-- List all architecture records with links -->
- [ARCH-001: {architecture-title}](core/architecture/ARCH-001.md)

*No architecture records yet*

### Risks

<!-- List all risk records with links -->
- [RISK-001: {risk-title}](core/risks/RISK-001.md)

*No risk records yet*

---

## Project Milestones

| Milestone | Status | Target Date | Completion Date |
|-----------|--------|-------------|-----------------|
| {milestone-1} | {status-1} | {target-date-1} | {completion-date-1} |
| {milestone-2} | {status-2} | {target-date-2} | {completion-date-2} |

---

## Quick Links

- [Latest Session]({latest-session-file}.md)
- [Project Root]({relative-path-to-root})

---

*Last Updated: {timestamp}*
```

## Variable Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `{project-name}` | Project name | Skill System Development |
| `{current-status}` | Current project status | In Progress, Testing Phase |
| `{YYYY-MM-DD}` | Date | 2026-03-21 |
| `{topic}` | Session topic/title | Skill System Initialization |
| `{results}` | Core results summary | Progress system created |
| `{milestone}` | Milestone name | Progress System Setup |
| `{status}` | Milestone status | ✅ Completed, 🔄 In Progress, ⏳ Pending |
| `{timestamp}` | Update timestamp | 2026-03-21 23:51:00 |
| `{relative-path-to-root}` | Relative path to project root | `../..` or `../../..` |

## Index Update Rules

### 1. Session List Maintenance
- Most recent sessions at the top
- Arrange in reverse chronological order
- Each entry includes: date, topic, core results, detail link
- Retain all historical session links

### 2. Link Validation
- Before updating, check if all linked files exist
- Existing files: retain link
- Non-existing files: mark as "[Expired]" and retain link text

### 3. Core Content Index
- Automatically update when core content is created
- Maintain links to all decision, architecture, and risk records
- Display "*No records yet*" when empty

### 4. Milestone Tracking
- Update status as milestones progress
- Record completion dates when finished
- Use emoji indicators for quick status recognition:
  - ✅ Completed
  - 🔄 In Progress
  - ⏳ Pending
  - ❌ Blocked

## Example

```markdown
# Project Progress Index

## Project Overview

| Item | Content |
|------|---------|
| Project Name | Skill System Development |
| Current Status | Initialization Complete, Testing Phase |
| Last Updated | 2026-03-21 |

---

## Recent Sessions

| Date | Topic | Core Results | Detail Link |
|------|-------|--------------|-------------|
| 2026-03-21 | Skill System Initialization | Progress system created, skills inventoried | [View](2026-03-21.md) |

---

## Core Content Index

### Decisions

*No decision records yet*

### Architecture

*No architecture records yet*

### Risks

*No risk records yet*

---

## Project Milestones

| Milestone | Status | Target Date | Completion Date |
|-----------|--------|-------------|-----------------|
| Progress System Setup | ✅ Completed | 2026-03-21 | 2026-03-21 |
| Progress Recorder Testing | 🔄 In Progress | 2026-03-21 | - |
| Skill Evaluator Testing | ⏳ Pending | TBD | - |

---

## Quick Links

- [Latest Session](2026-03-21.md)
- [Project Root](../..)

---

*Last Updated: 2026-03-21 23:51:00*
```
