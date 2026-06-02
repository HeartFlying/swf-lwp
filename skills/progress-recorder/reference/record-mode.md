# Record Mode

When users trigger record mode, execute the following steps:

## Table of Contents

- [1.1 Confirm Save Path](#11-confirm-save-path)
- [1.2 Collect Session Information](#12-collect-session-information)
- [1.3 Generate/Update Session Record File](#13-generateupdate-session-record-file)
- [1.4 Update Index File](#14-update-index-file)
- [1.5 Extract Core Content](#15-extract-core-content)
- [1.6 Confirm Save](#16-confirm-save)

## 1.1 Confirm Save Path

Session records default save path: `./.ai_memory/progress/{YYYY-MM-DD}.md`
Session index default save path: `./.ai_memory/progress/index.md`

### Data Protection Principles (Must Follow)

- Each date's session record file is an independent persistent record and must be permanently retained
- Absolutely prohibit deleting, overwriting, or replacing any historical session record files
- New date session records should create new files, coexisting with historical files
- Only the current day's file can append content; historical date files can only be read, not modified

### Directory Management Principles (Must Follow)

- Always use relative path `./.ai_memory/progress/` instead of absolute paths
- Create directory structure if not exists
- Check if file exists:
  - **Exists and is current date**: Append content to the same date file (append mode)
  - **Exists but is not current date**: This is a historical file, must be retained, create a new file for the current day
  - **Does not exist**: Create a new file using the template format

### Template Reference

| Template | File | Purpose |
|----------|------|---------|
| Session Record | [session-template.md](session-template.md) | Daily session record files |
| Index | [index-template.md](index-template.md) | Project progress index |
| Core Content | [core-templates.md](core-templates.md) | Decision, Architecture, Risk records |

## 1.2 Collect Session Information

Extract the following information from the current session:

### Basic Information
- Session time
- Session topic
- Session status

### Work Results
List the main work completed in this session:
- Completed tasks
- Created/Modified/Deleted files
- Key deliverables

### File Changes
Record file change details:

| Operation Type | File Path | Description |
|----------------|-----------|-------------|
| Create | path/to/file | File purpose |
| Modify | path/to/file | Modification content |
| Delete | path/to/file | Deletion reason |

### Todo Items
Record tasks that need to be completed subsequently:

| Task | Priority | Status | Description |
|------|----------|--------|-------------|
| Task description | P0/P1/P2 | To be executed | Detailed description |

### Issues and Solutions
Record problems encountered and solutions:

| Issue | Solution | Status |
|-------|----------|--------|
| Issue description | Solution method | Resolved/Pending |

### Key Decisions
Record important technical or design decisions:

| Decision Content | Decision Reason | Impact |
|------------------|-----------------|--------|
| Decision description | Why this decision was made | Impact on the project |

## 1.3 Generate/Update Session Record File

Use the session template to generate or update the session record file.

### File Naming Rule

| File Type | Naming Pattern | Location |
|-----------|---------------|----------|
| Session Record | `{YYYY-MM-DD}-S{N}.md` | `.ai_memory/progress/` |
| Index | `index.md` | `.ai_memory/progress/` |
| Decision | `DEC-{NNN}.md` | `.ai_memory/progress/core/decisions/` |
| Architecture | `ARCH-{NNN}.md` | `.ai_memory/progress/core/architecture/` |
| Risk | `RISK-{NNN}.md` | `.ai_memory/progress/core/risks/` |

## 1.4 Update Index File

Check if `./.ai_memory/progress/index.md` exists:
- **Exists**: Update index content, including project core basic information, core summary of the most recent session, and index information of historical sessions
- **Does not exist**: Create index file

### Index Update Rules (Must Follow)

1. **Retain historical session links**: When updating the index, must retain all links to historical sessions
2. **Link validation mechanism**: Before updating the index, check if files pointed to by all links exist
   - Existing files: Retain link
   - Non-existing files: Mark as "[Expired]" and retain link text for traceability
3. **Session list maintenance**:
   - Most recent sessions at the top of the list
   - Arrange all historical sessions in reverse chronological order
   - Each session entry includes: date, topic, core results, detail link
4. **Index integrity**: Index file must contain links to all existing session record files

**Index File Structure**:
```markdown
## Recent Sessions
| Date | Topic | Core Results | Detail Link |
|------|-------|--------------|-------------|
| 2026-03-16 | Latest session topic | Latest results summary | [View](2026-03-16.md) |
| 2026-03-15 | Historical session topic | Historical results summary | [View](2026-03-15.md) |
```

## 1.5 Extract Core Content

When saving session records, intelligently identify and extract high-value core content, storing separately in the `core/` directory.

### Core Content Definition

| Content Type | Description | Example Recognition Keywords |
|--------------|-------------|------------------------------|
| Decision Mechanism | Technology selection, architecture decisions, design direction determination | "decided to adopt", "choose", "final solution", "technology selection" |
| Conflict Resolution | Technical conflicts, design disagreements, trade-offs | "trade-off", "conflict", "compromise", "priority", "balance" |
| Architecture Impact | Design decisions affecting overall project architecture | "architecture", "system design", "module division", "overall structure" |
| Key Constraints | Project-level constraint conditions | "must", "constraint", "limitation", "requirement", "cannot" |
| Risk Decisions | Risk identification and response decisions | "risk", "potential issue", "response measure", "prevention" |

### Extraction Process

1. **Scan session content**: Check if session contains core content types
2. **Identify core content**: Identify high-value content based on keywords and context
3. **Classify and store**: Store by type to corresponding directories
   - Decision mechanism → `core/decisions/DEC-{NNN}.md`
   - Architecture impact → `core/architecture/ARCH-{NNN}.md`
   - Risk decisions → `core/risks/RISK-{NNN}.md`
4. **Update index**: Add core content index to index.md

### Core Content File Format

```markdown
# {Type Prefix}-{Number}: {Title}

## Basic Information
| Item | Content |
|------|---------|
| Number | {PREFIX}-{NNN} |
| Creation Date | {YYYY-MM-DD} |
| Source Session | [{YYYY-MM-DD}](../{YYYY-MM-DD}.md) |
| Status | Active/Deprecated/Revised |

## Content Details

### Decision/Issue Description
{Core content description}

### Reason/Background
{Decision reason or issue background}

### Impact Scope
{Impact scope on the project}

### Related Files
- {file-1}
- {file-2}

---
*Creation Time: {timestamp}*
```

### Numbering Rules

- **DEC-001, DEC-002, ...**: Decision record numbers
- **ARCH-001, ARCH-002, ...**: Architecture impact record numbers
- **RISK-001, RISK-002, ...**: Risk decision record numbers

Numbers increment from 001, each type has independent numbering.

## 1.6 Confirm Save

- Display the saved file path
- Show a summary of the saved content
- Confirm if the user is satisfied
