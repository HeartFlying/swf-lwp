# Core Content Templates

Templates for extracting and storing high-value core content in the `core/` directory.

---

## Table of Contents

- [Decision Record Template](#decision-record-template-dec-nnnmd)
- [Architecture Record Template](#architecture-record-template-arch-nnnmd)
- [Risk Record Template](#risk-record-template-risk-nnnmd)
- [Variable Reference](#variable-reference)

---

## Decision Record Template (DEC-{NNN}.md)

### File Naming
`core/decisions/DEC-{NNN}.md`

Where `{NNN}` is a 3-digit sequential number starting from 001.

### Template

```markdown
# DEC-{NNN}: {Decision Title}

## Basic Information

| Item | Content |
|------|---------|
| Number | DEC-{NNN} |
| Creation Date | {YYYY-MM-DD} |
| Source Session | [{YYYY-MM-DD}](../{YYYY-MM-DD}.md) |
| Status | {Active/Deprecated/Revised} |

---

## Decision Description

{Detailed description of the decision made}

---

## Decision Reason

### Background
{Context and background information}

### Options Considered
1. **Option A**: {description}
   - Pros: {advantages}
   - Cons: {disadvantages}

2. **Option B**: {description}
   - Pros: {advantages}
   - Cons: {disadvantages}

### Final Decision
{Why this option was chosen}

---

## Impact Scope

### Affected Areas
- {area-1}
- {area-2}

### Related Files
- `{file-path-1}`
- `{file-path-2}`

### Dependencies
- {dependency-1}
- {dependency-2}

---

## Revision History

| Date | Version | Change Description |
|------|---------|-------------------|
| {YYYY-MM-DD} | 1.0 | Initial decision |

---

*Created At: {timestamp}*
```

---

## Architecture Record Template (ARCH-{NNN}.md)

### File Naming
`core/architecture/ARCH-{NNN}.md`

Where `{NNN}` is a 3-digit sequential number starting from 001.

### Template

```markdown
# ARCH-{NNN}: {Architecture Title}

## Basic Information

| Item | Content |
|------|---------|
| Number | ARCH-{NNN} |
| Creation Date | {YYYY-MM-DD} |
| Source Session | [{YYYY-MM-DD}](../{YYYY-MM-DD}.md) |
| Status | {Active/Deprecated/Revised} |

---

## Architecture Description

{Detailed description of the architecture decision or design}

---

## Design Rationale

### Goals
- {goal-1}
- {goal-2}

### Constraints
- {constraint-1}
- {constraint-2}

### Trade-offs
| Factor | Choice | Reason |
|--------|--------|--------|
| {factor-1} | {choice-1} | {reason-1} |
| {factor-2} | {choice-2} | {reason-2} |

---

## Impact Analysis

### System Components Affected
- {component-1}
- {component-2}

### Interface Changes
- {interface-change-1}
- {interface-change-2}

### Data Flow Impact
{Description of how data flow is affected}

### Related Files
- `{file-path-1}`
- `{file-path-2}`

---

## Diagrams

```
{ASCII or reference to external diagrams}
```

---

## Revision History

| Date | Version | Change Description |
|------|---------|-------------------|
| {YYYY-MM-DD} | 1.0 | Initial architecture |

---

*Created At: {timestamp}*
```

---

## Risk Record Template (RISK-{NNN}.md)

### File Naming
`core/risks/RISK-{NNN}.md`

Where `{NNN}` is a 3-digit sequential number starting from 001.

### Template

```markdown
# RISK-{NNN}: {Risk Title}

## Basic Information

| Item | Content |
|------|---------|
| Number | RISK-{NNN} |
| Creation Date | {YYYY-MM-DD} |
| Source Session | [{YYYY-MM-DD}](../{YYYY-MM-DD}.md) |
| Status | {Identified/Monitoring/Mitigated/Resolved} |

---

## Risk Description

{Detailed description of the risk}

---

## Risk Assessment

### Likelihood
{High/Medium/Low} - {justification}

### Impact
{High/Medium/Low} - {justification}

### Risk Level
{critical/high/medium/low} (calculated from likelihood × impact)

---

## Mitigation Strategy

### Prevention Measures
- {measure-1}
- {measure-2}

### Contingency Plan
{Plan if risk materializes}

### Monitoring Approach
- {monitoring-method-1}
- {monitoring-method-2}

---

## Related Items

### Related Decisions
- [DEC-{NNN}](decisions/DEC-{NNN}.md)

### Related Architecture
- [ARCH-{NNN}](architecture/ARCH-{NNN}.md)

### Affected Files
- `{file-path-1}`
- `{file-path-2}`

---

## Revision History

| Date | Version | Change Description |
|------|---------|-------------------|
| {YYYY-MM-DD} | 1.0 | Initial risk identification |

---

*Created At: {timestamp}*
```

---

## Variable Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `{NNN}` | Sequential number (3 digits) | 001, 002, 003 |
| `{YYYY-MM-DD}` | Date | 2026-03-21 |
| `{title}` | Descriptive title | API Rate Limiting Strategy |
| `{timestamp}` | Creation timestamp | 2026-03-21 23:51:00 |
| `{status}` | Current status | Active, Deprecated, Resolved |
