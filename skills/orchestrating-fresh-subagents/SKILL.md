---
name: orchestrating-fresh-subagents
description: Use when executing an implementation plan and you need stricter orchestration than superpowers:subagent-driven-development, with a fresh agent for every step, explicit TDD tension between testing and implementation, mandatory spec and quality review, proactive dependent-skill invocation, and agent cleanup after each task.
---

# Orchestrating Fresh Subagents

## Overview

Execute a written implementation plan with a stricter controller loop than `superpowers:subagent-driven-development`. Use a fresh agent for each step, force test-first development, require review before task completion, and close every spawned agent once the task ends.

Announce at start: `I'm using orchestrating-fresh-subagents to execute this plan with fresh agents per step.`

Use the bundled script at `scripts/orchestrate_plan.py` as the workflow state machine. The script does not spawn agents itself; it keeps task state, enforces step order, records agent IDs, blocks invalid transitions, validates self-check review reports, and generates the next agent work order.

> **Script Location Note:** The `scripts/` directory is co-located with this skill file in the skill's base directory. The controller must run the script from the skill's base directory (or copy/symlink it into the project workspace). All command examples below assume the script is invoked from the skill base directory. If running from the project root, use the absolute path to the skill installation or copy the script into the project first.

This skill requires the controller agent to dispatch subagents using whatever subagent mechanism the current AI environment provides. Keep the workflow platform-neutral: do not name environment-specific tools in the skill body or agent prompts.

The script expects a normalized DAG task graph with spec traceability. If the user provides a free-form plan, first dispatch a fresh `plan-normalizer` subagent to map spec file paths plus the plan to the template in `references/plan-template.md`, then validate the normalized plan before initialization.

Spec files are the only source of truth for behavior and test assertions. Plans and DAG tasks are execution aids only.

## Use This Instead Of

- Use this instead of `superpowers:subagent-driven-development` when the original workflow is too loose about step boundaries or agent reuse.
- Use this instead of `superpowers:executing-plans` when the user wants same-session orchestration with stronger isolation.
- Do not use this without a written plan. If no plan exists, first use `superpowers:writing-plans`.

## Required Skill Chain

Invoke these skills proactively as part of the workflow:

- `superpowers:using-git-worktrees` before any implementation
- `superpowers:test-driven-development` for development and testing steps
- `superpowers:systematic-debugging` whenever a step fails unexpectedly or the root cause is unclear
- `superpowers:receiving-code-review` when processing review feedback from the self-check agent
- `superpowers:verification-before-completion` before claiming a step, task, or whole plan is complete
- `superpowers:finishing-a-development-branch` after all tasks pass

## Controller Responsibility

The main agent is the controller. The controller must create subagents; the skill file and script only define the workflow and state gates.

For every step returned by `next`, the controller must:

1. dispatch a fresh subagent using the generated prompt
2. ensure the subagent receives only the step-local context
3. prevent the subagent from inheriting hidden controller conversation history
4. wait for the subagent result
5. record the result with `complete-step`
6. close or release the subagent in the current environment
7. record that closure with `close-agent`

If the current environment does not support subagents, stop and report that this skill cannot be executed as designed. Do not silently fall back to inline execution, because inline execution violates the fresh-agent isolation requirement.

Use platform-neutral terms in prompts:

- `dispatch a fresh subagent`
- `wait for the subagent result`
- `close or release the subagent`
- `do not reuse this subagent for any later step`

Avoid platform-specific names in this skill:

- do not write environment tool names such as `Task`, `spawn_agent`, or `wait_agent`
- do not assume Claude Code, Codex, Gemini, or any other runtime
- let the executing platform map these neutral operations to its own tools

## Scripted Control Loop

**以下执行的所有脚本的路径都是相对该SKILL存储的路径**
Validate the normalized plan before creating state:

```bash
python scripts/orchestrate_plan.py validate-plan \
  --plan docs/plans/<normalized-plan>.md
```

Initialize the workflow state once per plan:

```bash
python scripts/orchestrate_plan.py init \
  --plan docs/plans/<plan>.md \
  --state .orchestration/<plan>.json
```

Use these commands during execution:

- `status`: show current task, blocked steps, open agents, and completion state
- `next`: print the next actionable step plus the prompt payload for the fresh agent
- `next-parallel`: show all steps whose tasks have no pending dependencies and can be dispatched in parallel
- `register-agent`: bind a fresh external agent ID to the current step
- `complete-step`: record the step outcome such as `RED_CONFIRMED`, `GREEN_CONFIRMED`, or `APPROVED`
- for `self-check`, `complete-step` must include `--report <path-to-review-report.json>`
- `close-agent`: mark the agent as closed after its output is consumed
- `cancel-agent`: cancel an open agent and reset its step to pending (use when complete-step fails)
- `retry-step`: reset a blocked step after providing context or resolving the blocker
- `check`: assert the full plan is complete and no agents remain open

This is the expected loop:

1. run `next`
2. dispatch a fresh subagent using the generated prompt
3. run `register-agent`
4. consume the agent result
5. run `complete-step`
6. run `close-agent`
7. repeat until `check` passes

For plans where the DAG allows parallel execution (e.g., diamond pattern where two branches depend on the same root), use `next-parallel` to get the current parallel-ready set, dispatch all returned steps as concurrent subagents, then register/complete/close each independently. When `next-parallel` returns only one step (or you prefer strict sequential mode), use `next` instead.

## Workflow

### 0. Normalize External Plan

If the input plan is not already a normalized DAG task graph:

1. Read `references/plan-template.md` **and** `references/plan-normalizer-contract.md`.
2. Dispatch a fresh `plan-normalizer` subagent.
3. Give the normalizer:
   - the spec file paths and the external plan
   - the normalization contract from `references/plan-template.md`
   - the **strict format checklist** from `references/plan-normalizer-contract.md`
4. Require the normalizer to output a Markdown plan containing one `orchestration-task-graph` JSON block.
5. Require every node to include spec refs, spec excerpt, exact files, targeted verification, full verification, acceptance checks, and dependencies.
6. Require the normalizer to complete the **Pre-Output Checklist** in `references/plan-normalizer-contract.md` before returning output.
7. Refuse to continue if the normalizer reports missing information instead of producing a valid graph.
8. Close or release the normalizer subagent after consuming its output.

The normalizer must decompose the work into a DAG. The controller executes the DAG sequentially in topological order for now; do not attempt parallel execution until the workflow explicitly supports it.

If a plan conflicts with the spec, the normalizer must report a blocker instead of choosing silently. If a task cannot be tied to concrete spec file paths and a spec excerpt, do not execute it.

Run `validate-plan` on the normalized plan.

If validate-plan fails:
- Collect the exact error messages from `validate-plan`.
- Determine if the failure is a **trivial formatting issue** (defined as: wrong fence tag, trailing whitespace, missing final newline only).
- If trivial: you may repair it inline.
- If not trivial: dispatch a **fresh** normalizer subagent with the original inputs + the previous output + the validation errors. Do NOT repair non-trivial format errors inline.

Set a maximum of 3 normalizer retries. After 3 failures:
1. Collect all validation error messages across all attempts.
2. Report them as a structured blocker summary.
3. Ask the user whether to:
   - fix the external plan and retry
   - accept partial normalization and proceed with what can be validated
   - skip normalization and execute tasks from the original plan in legacy mode

After validate-plan passes, run the semantic coverage check:

```bash
python scripts/validate_plan_coverage.py <plan>.md
```

Review any warnings. Fix genuine issues (e.g., non-existent spec refs) before `init`.
Warnings about files that will be created by the implementation are expected and can be ignored.

### 1. Load Normalized Plan

1. Read the normalized plan file once.
2. Extract every DAG task node with its full text, files, commands, dependencies, and acceptance checks.
3. Refuse to start implementation if the normalized plan is missing:
   - exact file targets
   - verification commands
   - acceptance checks
   - spec refs and spec excerpt
   - dependency reasons for every dependency
   - enough detail to execute without guessing
4. Create a controller checklist for all tasks in topological order before dispatching any implementation agent.
5. Initialize orchestration state with `scripts/orchestrate_plan.py init`.

### 2. Prepare Workspace

Before Task 1:

- Announce use of `superpowers:using-git-worktrees`
- Create or enter an isolated worktree
- **Copy the normalized plan file into the worktree if it is not tracked by git.** Git worktrees do not share untracked files. The plan file created during normalization exists in the original working directory and must be copied to the same relative path inside the worktree before running `init`.
- Run project setup
- Run baseline verification

If the baseline is red, stop and ask whether to fix the baseline first. Do not mix new work with a broken baseline.

> **Worktree + Plan File Note:** If you initialized the worktree before creating the normalized plan, the plan file will not appear in the worktree automatically. Copy it explicitly:
> ```bash
> cp docs/plans/<plan>.md .worktrees/<branch>/docs/plans/
> ```

### 3. Decompose Each Task Into Step Units

Every task must be split into at least these three step units:

1. `test`
2. `develop`
3. `self-check`

You may add more units when needed, for example:

- `context-gathering`
- `migration`
- `docs`
- `debug`
- `refactor`

But never collapse `test`, `develop`, and `self-check` into one agent or one prompt.

### 4. Run Test and Develop as TDD Opposition

For each task, create a fresh agent per step. Minimum three fresh agents per task.
The controller must perform the actual subagent dispatch. The script only provides the step prompt and records the external agent ID.

#### Step A: Test Agent

Dispatch a new testing agent with:

- only the current task text and immediate context
- explicit instruction to use `superpowers:test-driven-development`
- explicit instruction that spec refs and spec excerpt are the only source of truth for assertions
- ownership limited to test artifacts for the current task

The testing agent must:

1. identify the first behavior slice to prove
2. write or update the failing test from the spec refs, spec excerpt, and spec-derived acceptance checks
3. run the targeted test
4. confirm the failure is the expected red state
5. report one of:
   - `RED_CONFIRMED`
   - `NEEDS_CONTEXT`
   - `BLOCKED`

The testing agent must not implement production code.
The testing agent must return `NEEDS_CONTEXT` instead of guessing when the spec evidence is missing, ambiguous, or conflicts with the task.

Controller actions around this step:

```bash
python scripts/orchestrate_plan.py next --state .orchestration/<plan>.json
python scripts/orchestrate_plan.py register-agent --state .orchestration/<plan>.json --agent-id <fresh-test-agent-id>
python scripts/orchestrate_plan.py complete-step --state .orchestration/<plan>.json --agent-id <fresh-test-agent-id> --result RED_CONFIRMED --notes "<summary>"
python scripts/orchestrate_plan.py close-agent --state .orchestration/<plan>.json --agent-id <fresh-test-agent-id>
```

#### Step B: Development Agent

Only after `RED_CONFIRMED`, dispatch a brand-new development agent with:

- the same task text
- the failing-test evidence
- explicit instruction to use `superpowers:test-driven-development`
- ownership limited to implementation files for the current step

The development agent must:

1. implement the minimum code to satisfy the failing test
2. run the targeted test
3. run any task-level verification required by the plan
4. report one of:
   - `GREEN_CONFIRMED`
   - `NEEDS_CONTEXT`
   - `BLOCKED`

The development agent must not rewrite the test goal or relax assertions without evidence and explanation.
The development agent must preserve the spec-derived test intent. It must not redefine behavior from the plan or implementation convenience.

Controller actions around this step:

```bash
python scripts/orchestrate_plan.py next --state .orchestration/<plan>.json
python scripts/orchestrate_plan.py register-agent --state .orchestration/<plan>.json --agent-id <fresh-dev-agent-id>
python scripts/orchestrate_plan.py complete-step --state .orchestration/<plan>.json --agent-id <fresh-dev-agent-id> --result GREEN_CONFIRMED --notes "<summary>"
python scripts/orchestrate_plan.py close-agent --state .orchestration/<plan>.json --agent-id <fresh-dev-agent-id>
```

#### Step C: Repeat Until Task Scope Is Implemented

If the task contains multiple behavior slices, repeat:

`fresh test agent -> fresh development agent`

until the task implementation is complete.

Never reuse the previous test or development agent, even for follow-up edits.

### 5. Self-Check With a Fresh Review Agent

After the task implementation reaches green, dispatch a new self-check agent.

This agent performs two gates in order:

1. `spec review`
2. `code quality review`

The self-check agent must first answer:

- did the implementation satisfy the referenced spec exactly
- is anything missing
- did the implementation add unrequested behavior
- did tests and acceptance checks derive from the spec rather than plan-only assumptions

If spec review fails, stop there. Do not start code-quality review first.

If spec review passes, the same self-check agent then checks:

- implementation structure
- test quality
- unnecessary complexity
- obvious regression risk
- verification coverage

The self-check agent reports one of:

- `APPROVED`
- `SPEC_GAPS`
- `QUALITY_GAPS`
- `NEEDS_CONTEXT`

The self-check agent must also emit a structured JSON review report that follows `references/review-rules.md`, including the spec file paths and spec excerpt used for review.
Free-text review summaries are not sufficient for approval.

Controller actions around this step:

```bash
python scripts/orchestrate_plan.py next --state .orchestration/<plan>.json
python scripts/orchestrate_plan.py register-agent --state .orchestration/<plan>.json --agent-id <fresh-review-agent-id>
python scripts/orchestrate_plan.py complete-step --state .orchestration/<plan>.json --agent-id <fresh-review-agent-id> --result APPROVED --report <review-report.json> --notes "<summary>"
python scripts/orchestrate_plan.py close-agent --state .orchestration/<plan>.json --agent-id <fresh-review-agent-id>
```

## Review Loop

If self-check returns `SPEC_GAPS` or `QUALITY_GAPS`:

1. Announce use of `superpowers:receiving-code-review`
2. Process the review technically, not performatively
3. Dispatch a brand-new test agent if the fix changes expected behavior or adds missing coverage
4. Dispatch a brand-new development agent for the fix
5. Dispatch a brand-new self-check agent again

Return to the TDD loop until the current task gets `APPROVED`.

If any step hits unclear failures, announce use of `superpowers:systematic-debugging` and investigate root cause before further edits.

The script creates the next cycle automatically when self-check returns `SPEC_GAPS` or `QUALITY_GAPS`. After closing the review agent, run `next` again and start the new cycle with a fresh test agent.
The script rejects:

- `APPROVED` reports with any failing rule
- `QUALITY_GAPS` reports that actually fail `spec-compliance`
- any review report missing required inputs or required rules
- any review report where `verification-evidence` fails
- any plan or review that lacks spec refs and spec excerpt

## Agent Lifecycle Rules

Read `references/agent-lifecycle.md` before dispatching agents.
Read `references/review-rules.md` before dispatching any self-check agent.

Non-negotiable rules:

- each step gets a fresh agent
- the controller must dispatch that agent through the current environment's subagent facility
- no step agent inherits hidden assumptions from a previous step
- no agent owns more than one step at a time
- close step agents after their result is consumed with `close-agent`
- when a task finishes, close every agent created for that task, including reviewers and any descendants
- do not leave idle agents open between tasks

## Task Completion Gate

Before marking a task complete:

1. run the task verification commands fresh
2. confirm self-check is `APPROVED`
3. confirm all task agents are closed in orchestration state
4. announce task completion with evidence, following `superpowers:verification-before-completion`

Then and only then continue to the next task.

## Plan Completion

After the final task passes:

1. run the full required verification for the branch
2. confirm no task agents remain open
3. announce use of `superpowers:finishing-a-development-branch`
4. hand off to that skill for merge, PR, keep, or discard flow

Use:

```bash
python scripts/orchestrate_plan.py check --state .orchestration/<plan>.json
```

before claiming the orchestration is fully complete.

## Dispatch Contract

When dispatching any step agent, provide only:

- the current task text
- spec file paths and spec excerpt for the current task
- the current step goal
- exact file ownership for that step
- exact commands to run
- relevant prior evidence only

Do not make the agent read the full plan file when the controller can provide the relevant task excerpt directly.

## Red Flags

Never:

- reuse a step agent for another step
- let a development agent start before a testing agent proves red
- let a testing agent create assertions from the plan alone
- skip self-check because the tests are green
- run code-quality review before spec review passes
- accept review feedback without technical evaluation
- keep task agents open after the task is done
- claim success without fresh verification evidence
- continue implementation when debugging has not reached root cause
- execute steps inline when the workflow requires a fresh subagent
- hard-code platform-specific subagent tool names into this skill

## Minimal Task Pattern

The minimum correct per-task sequence is:

1. fresh test agent proves red
2. fresh development agent makes it green
3. repeat red-green pairs as needed
4. fresh self-check agent runs spec review
5. fresh self-check agent runs code-quality review
6. if gaps exist, loop back through fresh test and development agents
7. verify
8. close all task agents
9. move to next task
