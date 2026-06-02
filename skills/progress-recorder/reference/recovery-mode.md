# Recovery Mode

When users trigger recovery mode, execute the following steps:

## Table of Contents

- [2.1 Check Index File](#21-check-index-file)
- [2.2 Read Recent Session Record](#22-read-recent-session-record)
- [2.3 Display Recovery Information](#23-display-recovery-information)
- [2.4 Confirm Recovery](#24-confirm-recovery)
- [2.5 No Historical Record Handling](#25-no-historical-record-handling)
- [2.6 Error Detection and Recovery](#26-error-detection-and-recovery)

## 2.1 Check Index File

Check if `./.ai_memory/progress/index.md` exists:
- **Exists**: Read the index file to get project and session status
- **Does not exist**: Prompt the user that no historical progress records were found

## 2.2 Read Recent Session Record

Get the most recent session information from the index file and read the corresponding session record file.

## 2.3 Display Recovery Information

Display the following information to the user:

```
【Task Recovery】

Project Status:
- Current Stage: {stage}
- Completion Progress: {progress}
- Todo Items: {todo-count} items

Recent Session: {date}
Topic: {topic}

Completed Work:
- {completed-1}
- {completed-2}

Todo Items:
- [P0] {todo-1}
- [P1] {todo-2}

Next Steps:
1. {next-step-1}
2. {next-step-2}

Related Files:
- {file-1}
- {file-2}

Continue with last work?
```

## 2.4 Confirm Recovery

- After user confirmation, load related files into context
- Continue work according to the next steps plan
- If the user has other needs, execute according to user instructions

## 2.5 No Historical Record Handling

If no historical progress records are found:

```
【No Historical Progress Found】

No progress record files found in the current project directory.

To start a new project, please describe your requirements.
To specify another project directory, please provide the path.
```

## 2.6 Error Detection and Recovery

In recovery mode, automatically detect the following error scenarios and attempt recovery:

### Error Types

| Error Type | Detection Condition | Recovery Strategy |
|------------|---------------------|-------------------|
| File Lost | Session file linked in index does not exist | Recover key information from core content index |
| File Corrupted | File content cannot be parsed normally | Prompt user, suggest rebuilding from core content |
| Index Invalid | Index file does not exist or format error | Scan directory to rebuild index |
| Core Content Lost | Files missing in core/ directory | Re-extract from session records |

### Recovery Process

1. **Detection Phase**:
   - Check if index file exists
   - Validate effectiveness of all links in the index
   - Check integrity of core content directory

2. **Recovery Phase**:
   - **Index Lost**: Scan `.ai_memory/progress/` directory, rebuild index file
   - **Session File Lost**: Get key information from core content index, display to user
   - **Core Content Lost**: Scan all session records, re-extract core content

3. **User Notification**:
```
【Data Anomaly Detected】

Anomaly Type: {error-type}
Impact Scope: {affected-files}

Recovery Plan:
- {recovery-action-1}
- {recovery-action-2}

Execute automatic recovery?
```

### Manual Recovery Guidance

If automatic recovery fails, provide the following manual recovery guidance:

1. **Check Backup**: Check if there are manually backed up progress files
2. **Rebuild Index**: Delete index.md, regenerate new index by triggering record mode
3. **Core Content Recovery**: Check decision, architecture, risk records in core/ directory
4. **Session Record Recovery**: Check Git history, recover deleted files
