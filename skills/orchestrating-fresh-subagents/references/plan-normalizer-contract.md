# Plan Normalizer Contract

Use this reference when dispatching a `plan-normalizer` subagent under `orchestrating-fresh-subagents`.

## Purpose

Convert spec files plus a free-form external implementation plan into a normalized DAG task graph that passes `orchestrate_plan.py validate-plan` on the first attempt.

## Output Contract

The normalizer must output a Markdown file containing exactly one fenced `orchestration-task-graph` JSON block.

### Critical Format Rules

These rules are enforced by the validator. Any violation causes `validate-plan` to fail.

| Field | Required Type | Common Mistake | Example Correct Value |
|---|---|---|---|
| `version` | **integer** `1` | string `"1.0"` | `1` |
| `dependency_reasons` | **object** `{}` | array `[]` or `["reason"]` | `{"task-a": "reason text"}` |
| `files` | **object** with 3 keys | array `["file1"]` | `{"test": ["t.py"], "implementation": ["s.py"], "docs": []}` |
| `files.test` | **non-empty** string array | empty `[]` or missing | `["tests/test_x.py"]` |
| `files.implementation` | **non-empty** string array | empty `[]` or missing | `["src/x.py"]` |
| `files.docs` | string array (can be empty) | missing key entirely | `[]` or `["docs/x.md"]` |
| `verification.targeted` | **non-empty** string array | single string `"cmd"` | `["pytest tests/test_x.py"]` |
| `verification.full` | **non-empty** string array | single string `"cmd"` | `["pytest"]` |
| `acceptance` | **non-empty** string array | single string | `["Requirement A is met"]` |
| `notes` | string array (can be empty) | single string `"note"` | `[]` or `["Assumes Python 3.11"]` |

### Dependency Reasons Object Rules

- `dependency_reasons` must be an object, not an array.
- Every task ID in `depends_on` must have a matching key in `dependency_reasons`.
- Every key in `dependency_reasons` must exist in `depends_on`.
- Each value must be a non-empty string explaining why the dependency exists.

**Incorrect:**
```json
"depends_on": ["task-a"],
"dependency_reasons": ["needs task-a output"]
```

**Correct:**
```json
"depends_on": ["task-a"],
"dependency_reasons": {"task-a": "needs task-a output"}
```

### Files Object Rules

- `files` must be an object with exactly three keys: `test`, `implementation`, `docs`.
- `files.test` must not be empty. If a task genuinely has no dedicated test file, place a structural or smoke-test file path here (e.g., `tests/structure/test_skeleton.go`).
- `files.implementation` must not be empty. If a task is purely testing (e.g., contract tests), place framework or mock helper paths here.
- `files.docs` can be an empty array `[]`.

### Fence Rules

- Use exactly ` ```orchestration-task-graph ` as the opening fence.
- Do NOT use ` ```json `, ` ```javascript `, or any other language tag.
- The closing fence is ` ``` ` with no language tag.

## Pre-Output Checklist

The normalizer must verify every item below before emitting output. If any item fails, the normalizer must fix it internally before returning.

- [ ] Markdown contains exactly one `orchestration-task-graph` fenced block
- [ ] Opening fence is ` ```orchestration-task-graph `, not ` ```json `
- [ ] `version` is the integer `1`, not `"1"` or `"1.0"`
- [ ] Every task has `id`, `title`, `goal`, `spec_refs`, `spec_excerpt`, `depends_on`, `dependency_reasons`, `files`, `verification`, `acceptance`, `notes`
- [ ] `dependency_reasons` is an object, keys match `depends_on` exactly
- [ ] `files` is an object with keys `test`, `implementation`, `docs`
- [ ] `files.test` is a non-empty array
- [ ] `files.implementation` is a non-empty array
- [ ] `verification.targeted` is a non-empty string array
- [ ] `verification.full` is a non-empty string array
- [ ] `notes` is a string array (can be empty `[]`)
- [ ] No circular dependencies exist in the DAG

## Input to Provide the Normalizer

When dispatching the normalizer, the controller must provide:

1. The external plan file path (or its full text)
2. The spec file paths (the only source of truth for behavior)
3. The path to this contract file (`references/plan-normalizer-contract.md`)
4. The path to `references/plan-template.md`

The normalizer must read both reference files before producing output.

## Progressive Generation Strategy

If the plan is large (5+ tasks), generate the DAG in two passes:

**Pass 1 — Structure only:**
- Extract task IDs, titles, and goals
- Map dependency graph (depends_on, dependency_reasons)
- Verify no cycles exist in the intended graph

**Pass 2 — Fill details per task:**
- For each task, fill spec_refs, spec_excerpt, files, verification, acceptance
- Run the Pre-Output Checklist after each task individually
- Do not proceed to the next task until the current one passes all checks

This two-pass approach reduces the chance of JSON formatting errors
because the structural skeleton is validated before details are filled in.

## On Validation Failure

If `validate-plan` fails after the normalizer returns:

1. The controller must collect the exact error messages from `validate-plan`.
2. The controller must dispatch a **fresh** normalizer subagent.
3. The fresh normalizer must receive: the original inputs + the previous output + the validation error messages.
4. The controller must NOT repair the graph inline unless the failure is a trivial fence-tag typo (e.g., ` ```json ` instead of ` ```orchestration-task-graph `).

"Trivial formatting issue" is defined as:
- Wrong fence language tag
- Trailing whitespace in string values
- Missing newline at end of file

Everything else (type mismatches, missing keys, empty arrays) is **not** trivial and requires a fresh normalizer.
