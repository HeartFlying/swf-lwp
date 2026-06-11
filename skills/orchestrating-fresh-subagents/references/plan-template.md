# Normalized Plan Template

Use this reference when converting spec files and an external implementation plan before running `orchestrate_plan.py`.

The controller should dispatch a fresh `plan-normalizer` subagent to produce this format. The normalizer must not implement code, edit product files, or run the development workflow. Its only job is to map spec files plus the external plan into a normalized DAG task graph.

Spec files are the only source of truth for behavior. The implementation plan is only a decomposition and scheduling aid.

## Output Contract

The normalized plan is Markdown that contains exactly one fenced `orchestration-task-graph` JSON block:

````markdown
# Normalized Implementation Plan

```orchestration-task-graph
{
  "version": 1,
  "tasks": [
    {
      "id": "stable-task-id",
      "title": "Short task title",
      "goal": "Concrete outcome this task must deliver.",
      "spec_refs": ["docs/specs/example.md"],
      "spec_excerpt": "Minimal quoted or paraphrased spec text that justifies the task behavior and test assertions.",
      "depends_on": [],
      "dependency_reasons": {},
      "files": {
        "test": ["tests/test_example.py"],
        "implementation": ["src/example.py"],
        "docs": []
      },
      "verification": {
        "targeted": ["python -m pytest tests/test_example.py -q"],
        "full": ["python -m pytest -q"]
      },
      "acceptance": [
        "Observable requirement that proves this task is complete."
      ],
      "notes": []
    }
  ]
}
```
````

## Field Rules

- `version`: must be `1`.
- `id`: stable lowercase identifier using letters, digits, and hyphens.
- `title`: concise human-readable title.
- `goal`: concrete task outcome, not an implementation guess.
- `spec_refs`: non-empty list of spec file paths that justify this task. URLs are not valid here.
- `spec_excerpt`: non-empty spec excerpt that justifies the task behavior and test assertions.
- `depends_on`: list of task IDs that must complete first.
- `dependency_reasons`: object with one non-empty reason per dependency.
- `files.test`: exact test files or tightly-scoped test helpers.
- `files.implementation`: exact production implementation files.
- `files.docs`: exact documentation files, or an empty list.
- `verification.targeted`: commands proving the task behavior.
- `verification.full`: commands proving broader regression safety.
- `acceptance`: concrete checks derived from the spec that the self-check agent must enforce.
- `notes`: optional clarifications, risks, or assumptions.

## Spec Rules

- Treat spec files as the only source of truth for behavior and tests.
- Use the implementation plan only to help split and order work.
- If the plan conflicts with spec files, output a blocker summary instead of choosing one silently.
- If a task cannot be tied to a concrete spec file path and excerpt, output a blocker summary instead of guessing.
- Do not create tests from implementation details, current code behavior, or plan-only assumptions.

## DAG Rules

- Do not create cycles.
- Do not invent hidden dependencies; include a dependency only when task order affects correctness.
- Split large work into independently reviewable task nodes.
- Preserve the spec scope; do not add extra features.
- If the external plan lacks enough information to create exact files or verification, output a concise blocker summary instead of guessing.

## Sequential Execution Rule

The current controller executes tasks sequentially in topological order. The DAG exists to make dependencies explicit now and to support future parallel scheduling later.
