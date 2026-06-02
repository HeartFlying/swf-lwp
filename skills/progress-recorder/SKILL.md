---
name: progress-recorder
description: "Records AI session progress to disk files and supports task recovery. When users mention keywords like \"record progress\", \"save session\", \"work summary\", \"task recovery\", \"continue work\", or \"load progress\", this Skill is triggered to save or restore session state."
---

# Progress Recorder Skill

Records AI session progress, including work results, file changes, todo items, issues and solutions, key decisions, and risks. Supports task recovery and cross-session work. Provides milestone tracking, risk dashboard, and workload statistics.

---

## Table of Contents

- [Progress Recorder Skill](#progress-recorder-skill)
  - [Table of Contents](#table-of-contents)
  - [Core Features](#core-features)
    - [Feature Boundaries](#feature-boundaries)
  - [Trigger Modes](#trigger-modes)
    - [Execution Instructions](#execution-instructions)
  - [Directory Structure](#directory-structure)
  - [Quick Start](#quick-start)
    - [Example 1: Record Work Progress](#example-1-record-work-progress)
    - [Example 2: Recover Task](#example-2-recover-task)
  - [Output Files](#output-files)
  - [Acceptance Criteria](#acceptance-criteria)
    - [Must Meet](#must-meet)
    - [Quality Checks](#quality-checks)
  - [Notes](#notes)
  - [Reference Documentation](#reference-documentation)

---

## Core Features

| Feature | Description | Use Case |
|---------|-------------|----------|
| Session Recording | Record current session work, results, decisions | Session end, milestone completion |
| Index Maintenance | Maintain unified entry index file | Auto-update on each record |
| Task Recovery | Support resuming tasks in new sessions | New session start, continue work |
| Core Content Extraction | Intelligently identify and extract decisions, architecture, risks | Auto-execute when recording |
| Milestone Tracking | Track project milestone progress | Project management |
| Risk Dashboard | Identify and track project risks | Risk management |
| Workload Statistics | Statistics on sessions and project workload | Efficiency analysis |

### Feature Boundaries

**Applicable for**:
- Scenarios requiring cross-session context preservation  
- Complex multi-phase task tracking
- Team collaboration requiring historical progress visibility
- Long-term project milestone recording

**Not applicable for**:
- Simple one-time task recording
- Scenarios not requiring cross-session recovery
- Pure code version management (use Git instead)

---

## Trigger Modes

This Skill supports two trigger modes:

| Mode | Trigger Keywords | Function | Typical Scenario |
|------|------------------|----------|------------------|
| Record Mode | record progress, save session, work summary, session summary, save work, save progress | Save current session progress | Session end, milestone completion |
| Recovery Mode | recover task, continue work, load progress, task recovery, continue last, recover last work | Load historical progress to continue | New session start, continue work |

### Execution Instructions
The relative paths of the reference files are all the directory paths where the current skill is stored.

**When user triggers Record Mode:**
1. Read `reference/record-mode.md` for detailed steps
2. Execute steps 1.1 through 1.6 in order:
   - 2.1 Confirm Save Path (create directory structure if not exists)
   - 2.2 Collect Session Information
   - 2.3 Generate/Update Session Record File
   - 2.4 Update Index File
   - 2.5 Extract Core Content (if applicable)
   - 2.6 Confirm Save

**When user triggers Recovery Mode:**
1. Read `reference/recovery-mode.md` for detailed steps
2. Execute steps 2.1 through 2.6 in order:
   - 2.1 Check Index File
   - 2.2 Read Recent Session Record
   - 2.3 Display Recovery Information
   - 2.4 Confirm Recovery
   - 2.5 No Historical Record Handling (if applicable)
   - 2.6 Error Detection and Recovery (if applicable)

---

## Directory Structure

```
./.ai_memory/progress/
├── index.md                    # Session and project entry index
├── core/                       # Core content storage
│   ├── decisions/              # Decision records
│   │   └── DEC-{NNN}.md
│   ├── architecture/           # Architecture impact records
│   │   └── ARCH-{NNN}.md
│   └── risks/                  # Risk decision records
│       └── RISK-{NNN}.md
├── {YYYY-MM-DD}.md             # Daily session records
└── ...                         # Other date records
```

**Path Notes**:
- Use relative path `./.ai_memory/progress/` for cross-platform compatibility
- Session records named by date for easy lookup
- Index file serves as unified entry point
- `core/` directory stores high-value content independently

---

## Quick Start

### Example 1: Record Work Progress

**Input:**
```
User: Please record this session's work progress
```

**Output:**
```
AI: Collecting session information...

【Saved】
- Session Record: ./.ai_memory/progress/2026-03-15.md
- Index Updated: ./.ai_memory/progress/index.md

This Session:
- Work Results: Completed Skill testing
- File Changes: 4 files
- Todo Items: 3 items

Please confirm if satisfied?
```

### Example 2: Recover Task

**Input:**
```
User: Recover last task
```

**Output:**
```
AI: Loading project progress...

【Task Recovery】
Project Status: Skill system construction complete, entering test phase
Last Session: 2026-03-15
Todo Items: [P0] Other Skill tests, [P0] Pilot project selection

Continue last work?
```

---

## Output Files

| Output | Path | Description |
|--------|------|-------------|
| Session Record | `./.ai_memory/progress/{YYYY-MM-DD}.md` | Daily session record |
| Index File | `./.ai_memory/progress/index.md` | Project progress index |
| Decision Record | `./.ai_memory/progress/core/decisions/DEC-{NNN}.md` | Technical decision record |
| Architecture Record | `./.ai_memory/progress/core/architecture/ARCH-{NNN}.md` | Architecture impact record |
| Risk Record | `./.ai_memory/progress/core/risks/RISK-{NNN}.md` | Risk decision record |

---

## Acceptance Criteria

### Must Meet

- [ ] Session record files generated/updated correctly
- [ ] Index file maintained properly
- [ ] Content structure matches template
- [ ] File paths correct
- [ ] Task recovery function works
- [ ] Historical session files not deleted or overwritten
- [ ] Index contains valid links to all session records
- [ ] Core content identified and stored correctly
- [ ] Core content index updated correctly

### Quality Checks

- [ ] Information complete without omission
- [ ] Format standardized
- [ ] Summary accurate
- [ ] Supports task recovery
- [ ] Cross-date data persistence normal
- [ ] All index links valid
- [ ] Core content categorized correctly

---

## Notes

1. **Append Mode**: Multiple saves on same day should append, not overwrite
2. **Index Sync**: Update index file each time session record is saved
3. **Summary Quality**: Keep index summaries concise for quick understanding
4. **Path Handling**: Create directory structure and use relative paths for cross-platform compatibility
5. **Recovery Confirmation**: Show info for user confirmation before recovery
6. **File Loading**: Load files on demand during recovery to avoid context overload

**Data Security Notes (Important)**:
7. **Historical File Protection**: Historical session records are important assets, never delete
8. **Cross-Date Handling**: Create new date files when system date changes, keep all historical files
9. **Index Link Validation**: Validate all link effectiveness when updating index
10. **File Integrity**: Ensure directory exists before writing; verify file creation after writing

---

## Reference Documentation

For detailed information, see the reference documentation:

- [Record Mode Details](reference/record-mode.md) - Detailed steps for recording mode
- [Recovery Mode Details](reference/recovery-mode.md) - Detailed steps for recovery mode

---