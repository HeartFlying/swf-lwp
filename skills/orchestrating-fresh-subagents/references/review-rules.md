# Review Rules

Use this rule set for every `self-check` step under `orchestrating-fresh-subagents`.

## Required Inputs

Every review report must include these inputs:

- `task_text`: the exact task text being reviewed
- `spec_refs`: spec file paths used as the source of truth for this task
- `spec_excerpt`: the spec excerpt used to derive tests and acceptance checks
- `test_evidence`: the current cycle's testing outcome and failure/pass evidence
- `develop_evidence`: the current cycle's implementation summary and verification notes
- `changed_files`: list of changed files reviewed for this cycle
- `verification_summary`: fresh verification command summary
- `previous_review_deltas`: what changed since the last failed review, or `none` on the first review

If any input is missing, the review is invalid.

## Required Rules

Every report must include exactly one entry for each rule below.

### 1. spec-compliance

Checks:
- did the implementation satisfy the referenced spec exactly
- is anything missing
- did the implementation add unrequested behavior
- did the tests and acceptance checks derive from the spec rather than plan-only assumptions

Gate:
- if this rule fails, the verdict must be `SPEC_GAPS`

### 2. behavioral-correctness

Checks:
- does the implementation satisfy the intended behavior, not just the literal test shape
- did the implementation preserve the expected behavior across affected paths

### 3. test-quality

Checks:
- do tests prove the required behavior
- are assertions meaningful
- are tests avoiding shallow mock-only validation when real behavior should be exercised

### 4. regression-risk

Checks:
- is there obvious risk of breaking nearby behavior
- were affected call paths or contracts considered

### 5. complexity-yagni

Checks:
- did the change avoid extra abstractions and unrequested features
- is the implementation proportionate to the task

### 6. interface-contract

Checks:
- are naming, signatures, return values, and error handling consistent
- were externally visible contracts changed intentionally and safely

### 7. verification-evidence

Checks:
- is there fresh evidence for claimed success
- do the cited commands and results actually support the verdict

Gate:
- this rule must pass for `APPROVED`
- for `SPEC_GAPS` or `QUALITY_GAPS`: must be present but may fail (the root cause is the spec/quality gap, not verification)

## Severity Rules

Allowed severities:

- `none`
- `minor`
- `important`
- `critical`

Use:
- `none` for passing rules
- `minor` for non-blocking quality concerns
- `important` for blocking issues that must be fixed before approval
- `critical` for severe correctness, contract, or regression problems

## Verdict Rules

### APPROVED

Allowed only when:
- all required rules are present
- every rule status is `pass`
- `verification-evidence` is `pass`

### SPEC_GAPS

Required when:
- `spec-compliance` fails

Do not downgrade a spec mismatch to `QUALITY_GAPS`.

### QUALITY_GAPS

Allowed only when:
- `spec-compliance` passes
- at least one non-spec rule fails
- `verification-evidence` still passes

## Report Shape

Use this JSON structure:

```json
{
  "verdict": "QUALITY_GAPS",
  "summary": "Implementation matches task scope but quality issues remain.",
  "inputs": {
    "task_text": "Task excerpt here",
    "spec_refs": ["docs/specs/parser.md"],
    "spec_excerpt": "Parser must reject missing delimiters and return structured records.",
    "test_evidence": "Red-green evidence here",
    "develop_evidence": "Implementation notes here",
    "changed_files": ["src/parser.py", "tests/test_parser.py"],
    "verification_summary": "pytest tests/test_parser.py -q -> 3 passed",
    "previous_review_deltas": "Extracted magic number into PARSER_DELIMITER constant"
  },
  "rules": [
    {
      "id": "spec-compliance",
      "status": "pass",
      "severity": "none",
      "evidence": "No missing or extra behavior found relative to the referenced spec.",
      "files": ["src/parser.py", "tests/test_parser.py"]
    }
  ]
}
```

Repeat the `rules` entry for all seven required rule IDs.
