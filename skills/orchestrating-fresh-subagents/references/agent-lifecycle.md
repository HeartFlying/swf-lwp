# Agent Lifecycle

Use this reference when dispatching step agents under `orchestrating-fresh-subagents`.

The controller agent must use the current environment's native subagent facility. This reference intentionally avoids platform-specific tool names so it can apply across Codex, Claude Code, and other runtimes.

## Step Types

### Plan Normalizer Agent

Purpose:
- convert spec files plus a free-form external implementation plan into the normalized DAG task graph in `plan-template.md`
- preserve user scope without doing implementation work

Allowed:
- read the external plan
- read the referenced spec files
- infer explicit task nodes, dependencies, files, verification commands, and acceptance checks from the spec-backed plan
- report missing information instead of guessing

Not allowed:
- edit production or test code
- start TDD execution
- use plan-only assumptions as behavior truth
- keep private assumptions that are not represented in the normalized graph

Expected output:
- a Markdown normalized plan containing exactly one `orchestration-task-graph` JSON block
- or a blocker summary that explains what required information is missing

Source-of-truth rule:
- every task must include spec file paths and a spec excerpt
- if the plan conflicts with the spec, report a blocker instead of choosing silently

### Test Agent

Purpose:
- create or refine the next failing test
- prove red with a real command
- derive assertions from the task's spec refs, spec excerpt, and spec-derived acceptance checks

Allowed:
- edit test files
- add targeted fixtures or test helpers

Not allowed:
- edit production implementation files
- weaken assertions to make red easier
- infer behavior from implementation details or plan-only assumptions

Expected statuses:
- `RED_CONFIRMED`
- `NEEDS_CONTEXT`
- `BLOCKED`

### Development Agent

Purpose:
- implement the minimum code that turns the current red test green

Allowed:
- edit implementation files
- make minimal test updates only when required by legitimate interface alignment

Not allowed:
- redefine task scope
- silently relax behavior

Expected statuses:
- `GREEN_CONFIRMED`
- `NEEDS_CONTEXT`
- `BLOCKED`

### Self-Check Agent

Purpose:
- run spec review first
- run code-quality review second
- emit a structured review report that satisfies `review-rules.md`

Review order:
1. spec review
2. code quality review

Expected statuses:
- `APPROVED`
- `SPEC_GAPS`
- `QUALITY_GAPS`
- `NEEDS_CONTEXT`

Required outputs:
- verdict matching the step result
- structured JSON review report with all required inputs and rules

## Cleanup Rules

After every step:
- capture the result
- close or release the subagent in the current environment
- record that closure with `close-agent`

After every task:
- close every agent created for the task
- close descendants too
- verify no task agent remains open before moving on

## Enforcement Boundary

The orchestration script records external agent IDs and blocks invalid state transitions. It cannot independently prove that the runtime created a truly fresh subagent. The controller is responsible for using a new isolated subagent for every step and for never reusing an agent ID.

## Escalation Rules

Use `superpowers:systematic-debugging` when:
- a test fails for an unexpected reason
- the implementation does not produce the expected green state
- the self-check identifies a symptom but root cause is unclear

Use `superpowers:receiving-code-review` when:
- converting self-check feedback into follow-up changes

Use `superpowers:verification-before-completion` before:
- claiming a step passed
- claiming a task is complete
- claiming the full plan is complete
