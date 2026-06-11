#!/usr/bin/env python3
"""Semi-automatic executor for the orchestrating-fresh-subagents skill."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from os.path import basename as os_path_basename
from typing import Any, Dict, List, Optional


TASK_HEADING_RE = re.compile(r"^###\s+Task\s+(\d+):\s*(.+?)\s*$", re.MULTILINE)
FENCED_BLOCK_RE = re.compile(r"```([^\n`]*)\n(.*?)\n```", re.DOTALL)
STEP_ORDER = ["test", "develop", "self-check"]
STEP_RESULTS = {
    "test": {"RED_CONFIRMED", "NEEDS_CONTEXT", "BLOCKED"},
    "develop": {"GREEN_CONFIRMED", "NEEDS_CONTEXT", "BLOCKED"},
    "self-check": {"APPROVED", "SPEC_GAPS", "QUALITY_GAPS", "NEEDS_CONTEXT"},
}
STEP_ALLOWED_STATUSES = {"pending", "in_progress", "completed", "blocked"}
REVIEW_RULE_IDS = [
    "spec-compliance",
    "behavioral-correctness",
    "test-quality",
    "regression-risk",
    "complexity-yagni",
    "interface-contract",
    "verification-evidence",
]
REQUIRED_REVIEW_INPUTS = [
    "spec_refs",
    "spec_excerpt",
    "task_text",
    "test_evidence",
    "develop_evidence",
    "changed_files",
    "verification_summary",
    "previous_review_deltas",
]
RULE_SEVERITIES = {"none", "minor", "important", "critical"}
SPEC_RULE_IDS = {"spec-compliance"}


class OrchestrationError(RuntimeError):
    """Raised when a command would violate the orchestration contract."""


@dataclass
class StepRef:
    task_index: int
    cycle_number: int
    step_name: str


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def normalize_path(path: str) -> str:
    return str(Path(path).expanduser().resolve())


def new_step(name: str) -> Dict[str, Any]:
    return {
        "name": name,
        "status": "pending",
        "result": None,
        "notes": "",
        "report": None,
        "completed_at": None,
        "last_agent_id": None,
    }


def new_cycle(number: int) -> Dict[str, Any]:
    return {"number": number, "steps": [new_step(name) for name in STEP_ORDER]}


def require_non_empty_string(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise OrchestrationError(f"Task graph field '{path}' must be a non-empty string.")
    return value.strip()


def require_string_list(value: Any, path: str, *, allow_empty: bool = False) -> List[str]:
    if not isinstance(value, list):
        raise OrchestrationError(f"Task graph field '{path}' must be a list of strings.")
    if not allow_empty and not value:
        raise OrchestrationError(f"Task graph field '{path}' must not be empty.")
    result: List[str] = []
    for idx, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise OrchestrationError(f"Task graph field '{path}[{idx}]' must be a non-empty string.")
        result.append(item.strip())
    return result


def require_spec_ref_list(value: Any, path: str) -> List[str]:
    refs = require_string_list(value, path)
    for ref in refs:
        if "://" in ref:
            raise OrchestrationError(f"Task graph field '{path}' must contain file paths, not URLs.")
    return refs


def extract_task_graph_payload(content: str) -> Optional[str]:
    for match in FENCED_BLOCK_RE.finditer(content):
        info = match.group(1).strip().lower()
        body = match.group(2).strip()
        if "orchestration-task-graph" in info:
            return body
    return None


def validate_task_graph(graph: Any) -> List[Dict[str, Any]]:
    if not isinstance(graph, dict):
        raise OrchestrationError("Task graph must be a JSON object.")
    if graph.get("version") != 1:
        raise OrchestrationError("Task graph 'version' must be 1.")
    raw_tasks = graph.get("tasks")
    if not isinstance(raw_tasks, list) or not raw_tasks:
        raise OrchestrationError("Task graph must include a non-empty 'tasks' list.")

    seen_ids: Dict[str, Dict[str, Any]] = {}
    normalized: List[Dict[str, Any]] = []
    for idx, raw_task in enumerate(raw_tasks):
        if not isinstance(raw_task, dict):
            raise OrchestrationError(f"Task graph item tasks[{idx}] must be an object.")
        task_id = require_non_empty_string(raw_task.get("id"), f"tasks[{idx}].id")
        if task_id in seen_ids:
            raise OrchestrationError(f"Task graph contains duplicate task id '{task_id}'.")
        title = require_non_empty_string(raw_task.get("title"), f"tasks[{idx}].title")
        goal = require_non_empty_string(raw_task.get("goal"), f"tasks[{idx}].goal")
        spec_refs = require_spec_ref_list(raw_task.get("spec_refs"), f"tasks[{idx}].spec_refs")
        spec_excerpt = require_non_empty_string(raw_task.get("spec_excerpt"), f"tasks[{idx}].spec_excerpt")
        depends_on = require_string_list(raw_task.get("depends_on", []), f"tasks[{idx}].depends_on", allow_empty=True)
        acceptance = require_string_list(raw_task.get("acceptance"), f"tasks[{idx}].acceptance")

        reasons = raw_task.get("dependency_reasons", {})
        if not isinstance(reasons, dict):
            raise OrchestrationError(f"Task graph field 'tasks[{idx}].dependency_reasons' must be an object.")
        for dep in depends_on:
            if dep == task_id:
                raise OrchestrationError(f"Task '{task_id}' cannot depend on itself.")
            require_non_empty_string(reasons.get(dep), f"tasks[{idx}].dependency_reasons.{dep}")
        for key in reasons:
            if key not in depends_on:
                raise OrchestrationError(
                    f"Task graph field 'tasks[{idx}].dependency_reasons.{key}' "
                    f"does not appear in 'depends_on' for task '{task_id}'."
                )

        files = raw_task.get("files")
        if not isinstance(files, dict):
            raise OrchestrationError(f"Task graph field 'tasks[{idx}].files' must be an object.")
        normalized_files = {
            "test": require_string_list(files.get("test"), f"tasks[{idx}].files.test"),
            "implementation": require_string_list(files.get("implementation"), f"tasks[{idx}].files.implementation"),
            "docs": require_string_list(files.get("docs", []), f"tasks[{idx}].files.docs", allow_empty=True),
        }

        verification = raw_task.get("verification")
        if not isinstance(verification, dict):
            raise OrchestrationError(f"Task graph field 'tasks[{idx}].verification' must be an object.")
        normalized_verification = {
            "targeted": require_string_list(verification.get("targeted"), f"tasks[{idx}].verification.targeted"),
            "full": require_string_list(verification.get("full"), f"tasks[{idx}].verification.full"),
        }

        normalized_task = {
            "id": task_id,
            "title": title,
            "goal": goal,
            "spec_refs": spec_refs,
            "spec_excerpt": spec_excerpt,
            "depends_on": depends_on,
            "dependency_reasons": {dep: str(reasons[dep]).strip() for dep in depends_on},
            "files": normalized_files,
            "verification": normalized_verification,
            "acceptance": acceptance,
            "notes": require_string_list(raw_task.get("notes", []), f"tasks[{idx}].notes", allow_empty=True),
            "_source_order": idx,
        }
        seen_ids[task_id] = normalized_task
        normalized.append(normalized_task)

    known_ids = set(seen_ids)
    for task in normalized:
        for dep in task["depends_on"]:
            if dep not in known_ids:
                raise OrchestrationError(f"Task '{task['id']}' depends on unknown task '{dep}'.")

    return topological_sort_tasks(normalized)


def topological_sort_tasks(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    task_by_id = {task["id"]: task for task in tasks}
    incoming = {task["id"]: set(task["depends_on"]) for task in tasks}
    dependents: Dict[str, List[str]] = {task["id"]: [] for task in tasks}
    for task in tasks:
        for dep in task["depends_on"]:
            dependents[dep].append(task["id"])

    source_order = {task["id"]: task["_source_order"] for task in tasks}
    ready = deque(sorted(
        [task_id for task_id, deps in incoming.items() if not deps],
        key=lambda item: source_order[item],
    ))
    ordered: List[Dict[str, Any]] = []

    while ready:
        task_id = ready.popleft()
        ordered.append(task_by_id[task_id])
        for dependent_id in sorted(dependents[task_id], key=lambda item: source_order[item]):
            incoming[dependent_id].remove(task_id)
            if not incoming[dependent_id]:
                ready.append(dependent_id)
                ready = deque(sorted(ready, key=lambda item: source_order[item]))
        incoming.pop(task_id)

    if incoming:
        cycle_ids = ", ".join(sorted(incoming))
        raise OrchestrationError(f"Task graph contains a dependency cycle involving: {cycle_ids}.")

    return ordered


def load_task_graph(plan_file: Path, content: str) -> Optional[List[Dict[str, Any]]]:
    payload = extract_task_graph_payload(content)
    if payload is None:
        return None
    try:
        graph = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise OrchestrationError(f"Task graph JSON is invalid in {plan_file}: {exc}") from exc
    return validate_task_graph(graph)


def format_graph_task_body(task: Dict[str, Any], index: int) -> str:
    deps = ", ".join(task["depends_on"]) if task["depends_on"] else "none"
    lines = [
        f"### Task {index}: {task['title']}",
        "",
        f"Task ID: `{task['id']}`",
        f"Goal: {task['goal']}",
        "",
        "Spec source of truth:",
        f"- Spec refs: {', '.join(task['spec_refs'])}",
        f"- Spec excerpt: {task['spec_excerpt']}",
        "",
        f"Depends on: {deps}",
    ]
    if task["dependency_reasons"]:
        lines.append("")
        lines.append("Dependency reasons:")
        for dep, reason in task["dependency_reasons"].items():
            lines.append(f"- {dep}: {reason}")
    lines.extend(
        [
            "",
            "Files:",
            f"- Test: {', '.join(task['files']['test'])}",
            f"- Implementation: {', '.join(task['files']['implementation'])}",
            f"- Docs: {', '.join(task['files']['docs']) if task['files']['docs'] else 'none'}",
            "",
            "Verification:",
            f"- Targeted: {', '.join(task['verification']['targeted'])}",
            f"- Full: {', '.join(task['verification']['full'])}",
            "",
            "Acceptance:",
        ]
    )
    lines.extend(f"- {item}" for item in task["acceptance"])
    if task["notes"]:
        lines.append("")
        lines.append("Notes:")
        lines.extend(f"- {item}" for item in task["notes"])
    return "\n".join(lines)


def build_tasks_from_graph(graph_tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    tasks: List[Dict[str, Any]] = []
    for index, graph_task in enumerate(graph_tasks, start=1):
        task = {key: value for key, value in graph_task.items() if not key.startswith("_")}
        tasks.append(
            {
                "index": index,
                "task_id": graph_task["id"],
                "title": graph_task["title"],
                "body": format_graph_task_body(graph_task, index),
                "source_task": task,
                "status": "pending",
                "current_cycle": 1,
                "cycles": [new_cycle(1)],
            }
        )
    return tasks


def build_tasks_from_legacy_headings(content: str) -> List[Dict[str, Any]]:
    matches = list(TASK_HEADING_RE.finditer(content))
    if not matches:
        raise OrchestrationError(
            "Plan does not contain a normalized 'orchestration-task-graph' fenced JSON block "
            "or any legacy '### Task N: ...' sections."
        )

    tasks: List[Dict[str, Any]] = []
    for idx, match in enumerate(matches):
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(content)
        section = content[start:end].strip()
        task_index = int(match.group(1))
        title = match.group(2).strip()
        tasks.append(
            {
                "index": task_index,
                "task_id": f"task-{task_index}",
                "title": title,
                "body": section,
                "source_task": None,
                "status": "pending",
                "current_cycle": 1,
                "cycles": [new_cycle(1)],
            }
        )
    return tasks


def parse_plan(plan_path: str) -> Dict[str, Any]:
    plan_file = Path(plan_path).expanduser().resolve()
    content = plan_file.read_text(encoding="utf-8")
    graph_tasks = load_task_graph(plan_file, content)
    if graph_tasks is not None:
        tasks = build_tasks_from_graph(graph_tasks)
        plan_format = "orchestration-task-graph-v1"
    else:
        tasks = build_tasks_from_legacy_headings(content)
        plan_format = "legacy-task-headings"

    title_line = next((line.strip() for line in content.splitlines() if line.strip().startswith("# ")), plan_file.stem)
    return {
        "plan_path": str(plan_file),
        "plan_format": plan_format,
        "plan_title": title_line.removeprefix("# ").strip(),
        "created_at": utc_now(),
        "updated_at": utc_now(),
        "tasks": tasks,
        "open_agents": [],
    }


def load_state(state_path: str) -> Dict[str, Any]:
    file = Path(state_path).expanduser().resolve()
    return json.loads(file.read_text(encoding="utf-8"))


def save_state(state_path: str, state: Dict[str, Any]) -> None:
    state["updated_at"] = utc_now()
    file = Path(state_path).expanduser().resolve()
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def get_task(state: Dict[str, Any], task_index: int) -> Dict[str, Any]:
    for task in state["tasks"]:
        if task["index"] == task_index:
            return task
    raise OrchestrationError(f"Unknown task index: {task_index}")


def get_cycle(task: Dict[str, Any], cycle_number: Optional[int] = None) -> Dict[str, Any]:
    target = cycle_number or task["current_cycle"]
    for cycle in task["cycles"]:
        if cycle["number"] == target:
            return cycle
    raise OrchestrationError(f"Unknown cycle number {target} for task {task['index']}")


def get_step(task: Dict[str, Any], cycle_number: int, step_name: str) -> Dict[str, Any]:
    cycle = get_cycle(task, cycle_number)
    for step in cycle["steps"]:
        if step["name"] == step_name:
            return step
    raise OrchestrationError(f"Unknown step '{step_name}' for task {task['index']} cycle {cycle_number}")


def open_agents_for_task(state: Dict[str, Any], task_index: int) -> List[Dict[str, Any]]:
    return [agent for agent in state["open_agents"] if agent["task_index"] == task_index]


def open_agent_for_step(state: Dict[str, Any], ref: StepRef) -> Optional[Dict[str, Any]]:
    for agent in state["open_agents"]:
        if (
            agent["task_index"] == ref.task_index
            and agent["cycle_number"] == ref.cycle_number
            and agent["step_name"] == ref.step_name
        ):
            return agent
    return None


def refresh_task_status(task: Dict[str, Any], open_agents: List[Dict[str, Any]]) -> None:
    current_cycle = get_cycle(task, task["current_cycle"])
    steps = {step["name"]: step for step in current_cycle["steps"]}
    self_check = steps["self-check"]

    if self_check["result"] == "APPROVED":
        task["status"] = "awaiting_agent_cleanup" if open_agents else "approved"
        return

    if any(step["status"] != "pending" for step in current_cycle["steps"]) or task["current_cycle"] > 1:
        task["status"] = "in_progress"
    else:
        task["status"] = "pending"


def refresh_all_statuses(state: Dict[str, Any]) -> None:
    for task in state["tasks"]:
        refresh_task_status(task, open_agents_for_task(state, task["index"]))


def step_ready(task: Dict[str, Any], cycle_number: int, step_name: str) -> bool:
    cycle = get_cycle(task, cycle_number)
    steps = {step["name"]: step for step in cycle["steps"]}
    if step_name == "test":
        return steps["test"]["status"] == "pending"
    if step_name == "develop":
        return steps["test"]["result"] == "RED_CONFIRMED" and steps["develop"]["status"] == "pending"
    if step_name == "self-check":
        return steps["develop"]["result"] == "GREEN_CONFIRMED" and steps["self-check"]["status"] == "pending"
    raise OrchestrationError(f"Unsupported step '{step_name}'")


def next_actionable_step(state: Dict[str, Any]) -> Optional[StepRef]:
    refresh_all_statuses(state)
    for task in sorted(state["tasks"], key=lambda item: item["index"]):
        if task["status"] == "approved":
            continue
        cycle_number = task["current_cycle"]
        cycle = get_cycle(task, cycle_number)
        for step in cycle["steps"]:
            if step["status"] == "blocked":
                return None
        for step_name in STEP_ORDER:
            if step_ready(task, cycle_number, step_name):
                return StepRef(task_index=task["index"], cycle_number=cycle_number, step_name=step_name)
        return None
    return None


def blocked_steps(state: Dict[str, Any]) -> List[StepRef]:
    blocked: List[StepRef] = []
    for task in state["tasks"]:
        cycle = get_cycle(task, task["current_cycle"])
        for step in cycle["steps"]:
            if step["status"] == "blocked":
                blocked.append(StepRef(task["index"], cycle["number"], step["name"]))
    return blocked


def parallel_ready_set(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return all steps that are ready to execute in parallel.

    A step is parallel-ready when:
    - Its task is not yet approved
    - All its dependency tasks are approved
    - The step itself is ready (test -> develop -> self-check order per task)
    - No agent is currently open for that step
    """
    refresh_all_statuses(state)
    # Build task_id -> task state map for dependency checks
    task_by_id: Dict[str, Dict[str, Any]] = {}
    for t in state["tasks"]:
        tid = t.get("task_id")
        if tid:
            task_by_id[tid] = t

    ready_steps: List[Dict[str, Any]] = []
    for task in sorted(state["tasks"], key=lambda item: item["index"]):
        if task["status"] == "approved":
            continue
        # Check all dependency tasks are approved
        source = task.get("source_task")
        if source and source.get("depends_on"):
            deps_approved = True
            for dep_id in source["depends_on"]:
                dep_task = task_by_id.get(dep_id)
                if not dep_task or dep_task["status"] != "approved":
                    deps_approved = False
                    break
            if not deps_approved:
                continue
        cycle_number = task["current_cycle"]
        cycle = get_cycle(task, cycle_number)
        if any(step["status"] == "blocked" for step in cycle["steps"]):
            continue
        for step_name in STEP_ORDER:
            if step_ready(task, cycle_number, step_name) and not open_agent_for_step(
                state, StepRef(task["index"], cycle_number, step_name)
            ):
                ready_steps.append(
                    summarize_step(
                        state,
                        StepRef(task["index"], cycle_number, step_name),
                    )
                )
                break
    return ready_steps


def ensure_step_ref(state: Dict[str, Any], task_index: Optional[int], cycle_number: Optional[int], step_name: Optional[str]) -> StepRef:
    if task_index is not None and step_name is not None:
        task = get_task(state, task_index)
        cycle = cycle_number or task["current_cycle"]
        return StepRef(task_index=task_index, cycle_number=cycle, step_name=step_name)

    ref = next_actionable_step(state)
    if ref:
        return ref

    blocked = blocked_steps(state)
    if blocked:
        first = blocked[0]
        raise OrchestrationError(
            f"Workflow is blocked at task {first.task_index} cycle {first.cycle_number} step {first.step_name}. "
            "Use retry-step after providing missing context or resolving the blocker."
        )

    raise OrchestrationError("No actionable step found. The plan may already be complete.")


def register_agent(state: Dict[str, Any], ref: StepRef, agent_id: str) -> Dict[str, Any]:
    task = get_task(state, ref.task_index)
    step = get_step(task, ref.cycle_number, ref.step_name)
    if step["status"] not in {"pending", "in_progress"}:
        raise OrchestrationError(
            f"Cannot register agent for task {ref.task_index} cycle {ref.cycle_number} step {ref.step_name}: "
            f"step status is {step['status']}"
        )
    if not step_ready(task, ref.cycle_number, ref.step_name):
        raise OrchestrationError(
            f"Cannot start task {ref.task_index} cycle {ref.cycle_number} step {ref.step_name} before dependencies are complete."
        )
    if open_agent_for_step(state, ref):
        raise OrchestrationError(
            f"Task {ref.task_index} cycle {ref.cycle_number} step {ref.step_name} already has an open agent."
        )
    for agent in state["open_agents"]:
        if agent["agent_id"] == agent_id:
            raise OrchestrationError(f"Agent ID '{agent_id}' is already registered.")

    step["status"] = "in_progress"
    step["last_agent_id"] = agent_id
    record = {
        "agent_id": agent_id,
        "task_index": ref.task_index,
        "cycle_number": ref.cycle_number,
        "step_name": ref.step_name,
        "registered_at": utc_now(),
    }
    state["open_agents"].append(record)
    refresh_task_status(task, open_agents_for_task(state, task["index"]))
    return record


def create_next_cycle(task: Dict[str, Any]) -> int:
    next_number = max(cycle["number"] for cycle in task["cycles"]) + 1
    task["cycles"].append(new_cycle(next_number))
    task["current_cycle"] = next_number
    return next_number


def validate_review_report(report: Optional[Dict[str, Any]], expected_result: str) -> Dict[str, Any]:
    if report is None:
        raise OrchestrationError("Self-check requires a structured review report.")
    if not isinstance(report, dict):
        raise OrchestrationError("Review report must be a JSON object.")

    verdict = report.get("verdict")
    if verdict != expected_result:
        raise OrchestrationError(f"Review report verdict '{verdict}' must match result '{expected_result}'.")

    summary = report.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        raise OrchestrationError("Review report must include a non-empty summary.")

    inputs = report.get("inputs")
    if not isinstance(inputs, dict):
        raise OrchestrationError("Review report must include an 'inputs' object.")
    missing_inputs = [key for key in REQUIRED_REVIEW_INPUTS if key not in inputs]
    if missing_inputs:
        raise OrchestrationError(
            f"Review report is missing required inputs: {', '.join(missing_inputs)}"
        )
    for key in REQUIRED_REVIEW_INPUTS:
        value = inputs.get(key)
        if key in {"changed_files", "spec_refs"}:
            if not isinstance(value, list) or not value or not all(isinstance(item, str) and item.strip() for item in value):
                raise OrchestrationError(f"Review report input '{key}' must be a non-empty list of file paths.")
            if key == "spec_refs" and any("://" in item for item in value):
                raise OrchestrationError("Review report input 'spec_refs' must contain file paths, not URLs.")
        else:
            if not isinstance(value, str) or not value.strip():
                raise OrchestrationError(f"Review report input '{key}' must be a non-empty string.")

    rules = report.get("rules")
    if not isinstance(rules, list) or not rules:
        raise OrchestrationError("Review report must include a non-empty rules list.")

    seen: Dict[str, Dict[str, Any]] = {}
    for rule in rules:
        if not isinstance(rule, dict):
            raise OrchestrationError("Each review rule entry must be an object.")
        rule_id = rule.get("id")
        if rule_id not in REVIEW_RULE_IDS:
            raise OrchestrationError(f"Unknown review rule id '{rule_id}'.")
        if rule_id in seen:
            raise OrchestrationError(f"Review rule '{rule_id}' appears more than once.")
        status = rule.get("status")
        if status not in {"pass", "fail"}:
            raise OrchestrationError(f"Review rule '{rule_id}' must use status 'pass' or 'fail'.")
        severity = rule.get("severity")
        if severity not in RULE_SEVERITIES:
            raise OrchestrationError(
                f"Review rule '{rule_id}' must use severity in: {', '.join(sorted(RULE_SEVERITIES))}."
            )
        evidence = rule.get("evidence")
        if not isinstance(evidence, str) or not evidence.strip():
            raise OrchestrationError(f"Review rule '{rule_id}' must include non-empty evidence.")
        files = rule.get("files")
        if not isinstance(files, list) or not files or not all(isinstance(item, str) and item.strip() for item in files):
            raise OrchestrationError(f"Review rule '{rule_id}' must include a non-empty files list.")
        seen[rule_id] = rule

    missing_rules = [rule_id for rule_id in REVIEW_RULE_IDS if rule_id not in seen]
    if missing_rules:
        raise OrchestrationError(
            f"Review report is missing required rules: {', '.join(missing_rules)}"
        )

    fails = {rule_id: rule for rule_id, rule in seen.items() if rule["status"] == "fail"}
    spec_fail = any(rule_id in SPEC_RULE_IDS for rule_id in fails)
    quality_fail = any(rule_id not in SPEC_RULE_IDS for rule_id in fails)

    verification_rule = seen["verification-evidence"]
    if expected_result == "APPROVED" and verification_rule["status"] != "pass":
        raise OrchestrationError("APPROVED review report requires verification-evidence to pass.")

    if expected_result == "APPROVED":
        if fails:
            raise OrchestrationError("APPROVED review report cannot contain failing rules.")
    elif expected_result == "SPEC_GAPS":
        if not spec_fail:
            raise OrchestrationError("SPEC_GAPS review report must fail spec-compliance.")
    elif expected_result == "QUALITY_GAPS":
        if spec_fail:
            raise OrchestrationError("QUALITY_GAPS review report cannot fail spec-compliance; use SPEC_GAPS instead.")
        if not quality_fail:
            raise OrchestrationError("QUALITY_GAPS review report must contain at least one non-spec failing rule.")

    return report


def load_review_report(report_path: Optional[str]) -> Optional[Dict[str, Any]]:
    if not report_path:
        return None
    file = Path(report_path).expanduser().resolve()
    try:
        return json.loads(file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise OrchestrationError(f"Review report is not valid JSON: {exc}") from exc


def complete_step(state: Dict[str, Any], agent_id: str, result: str, notes: str, report: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    agent = next((item for item in state["open_agents"] if item["agent_id"] == agent_id), None)
    if not agent:
        raise OrchestrationError(f"No open agent with ID '{agent_id}'")

    task = get_task(state, agent["task_index"])
    step = get_step(task, agent["cycle_number"], agent["step_name"])
    expected = STEP_RESULTS[step["name"]]
    if result not in expected:
        raise OrchestrationError(
            f"Result '{result}' is invalid for step {step['name']}. Allowed: {', '.join(sorted(expected))}"
        )

    if result in {"RED_CONFIRMED", "GREEN_CONFIRMED", "APPROVED"}:
        step["status"] = "completed"
    else:
        step["status"] = "blocked"

    if step["name"] == "self-check":
        report = validate_review_report(report, result)
    elif report is not None:
        raise OrchestrationError("Structured review reports are only valid for self-check steps.")

    step["result"] = result
    step["notes"] = notes or ""
    step["report"] = report
    step["completed_at"] = utc_now()

    if step["name"] == "self-check" and result in {"SPEC_GAPS", "QUALITY_GAPS"}:
        create_next_cycle(task)

    refresh_task_status(task, open_agents_for_task(state, task["index"]))
    return {
        "task_index": task["index"],
        "cycle_number": agent["cycle_number"],
        "step_name": step["name"],
        "result": result,
        "task_status": task["status"],
    }


def close_agent(state: Dict[str, Any], agent_id: str) -> Dict[str, Any]:
    for idx, agent in enumerate(state["open_agents"]):
        if agent["agent_id"] == agent_id:
            removed = state["open_agents"].pop(idx)
            task = get_task(state, removed["task_index"])
            refresh_task_status(task, open_agents_for_task(state, task["index"]))
            return removed
    raise OrchestrationError(f"No open agent with ID '{agent_id}'")


def cancel_agent(state: Dict[str, Any], agent_id: str) -> Dict[str, Any]:
    """Remove an open agent and reset its step to pending.

    Use this when complete-step fails validation and the agent+step
    are left in an unrecoverable in_progress state. Unlike close-agent,
    this also resets the locked step so the workflow can continue.
    """
    for idx, agent in enumerate(state["open_agents"]):
        if agent["agent_id"] == agent_id:
            removed = state["open_agents"].pop(idx)
            task = get_task(state, removed["task_index"])
            step = get_step(task, removed["cycle_number"], removed["step_name"])
            if step["status"] == "in_progress":
                step["status"] = "pending"
                step["result"] = None
                step["notes"] = ""
                step["completed_at"] = None
            refresh_task_status(task, open_agents_for_task(state, task["index"]))
            return {"cancelled": removed, "step_reset": step["status"] == "pending"}
    raise OrchestrationError(f"No open agent with ID '{agent_id}'")


def retry_step(state: Dict[str, Any], ref: StepRef) -> Dict[str, Any]:
    if open_agent_for_step(state, ref):
        raise OrchestrationError("Cannot retry a step while its prior agent is still open.")
    task = get_task(state, ref.task_index)
    step = get_step(task, ref.cycle_number, ref.step_name)
    if step["status"] != "blocked":
        raise OrchestrationError(
            f"Cannot retry task {ref.task_index} cycle {ref.cycle_number} step {ref.step_name}: step is not blocked."
        )
    step["status"] = "pending"
    step["result"] = None
    step["notes"] = ""
    step["completed_at"] = None
    refresh_task_status(task, open_agents_for_task(state, task["index"]))
    return step


def plan_complete(state: Dict[str, Any]) -> bool:
    refresh_all_statuses(state)
    return all(task["status"] == "approved" for task in state["tasks"]) and not state["open_agents"]


def summarize_step(state: Dict[str, Any], ref: StepRef) -> Dict[str, Any]:
    task = get_task(state, ref.task_index)
    step = get_step(task, ref.cycle_number, ref.step_name)
    return {
        "task_index": ref.task_index,
        "task_id": task.get("task_id"),
        "task_title": task["title"],
        "cycle_number": ref.cycle_number,
        "step_name": ref.step_name,
        "step_status": step["status"],
        "required_skills": required_skills_for_step(ref.step_name),
        "task_excerpt": task["body"],
        "required_review_rules": REVIEW_RULE_IDS if ref.step_name == "self-check" else [],
        "required_review_inputs": REQUIRED_REVIEW_INPUTS if ref.step_name == "self-check" else [],
        "prompt": build_prompt(state, ref),
    }


def required_skills_for_step(step_name: str) -> List[str]:
    base = ["superpowers:verification-before-completion"]
    if step_name in {"test", "develop"}:
        return ["superpowers:test-driven-development"] + base
    if step_name == "self-check":
        return ["superpowers:receiving-code-review"] + base
    return base


def build_prompt(state: Dict[str, Any], ref: StepRef) -> str:
    task = get_task(state, ref.task_index)
    task_excerpt = task["body"]
    task_label = f"{task['index']} ({task.get('task_id', 'unknown-id')})"
    prior_cycle = get_cycle(task, ref.cycle_number)
    steps = {step["name"]: step for step in prior_cycle["steps"]}

    if ref.step_name == "test":
        return "\n".join(
            [
                f"You own task {task_label} cycle {ref.cycle_number} step test.",
                "Required skill: superpowers:test-driven-development.",
                "Spec is the only source of truth for test assertions. Use spec refs, spec excerpt, and acceptance checks; do not infer behavior from the implementation plan alone.",
                "If the spec evidence is missing or conflicts with the task, return NEEDS_CONTEXT instead of guessing.",
                "Only touch test files and tightly-scoped test helpers for this task.",
                "Write or refine the next failing test, run it, and prove RED_CONFIRMED before stopping.",
                "Return one of: RED_CONFIRMED, NEEDS_CONTEXT, BLOCKED.",
                "",
                task_excerpt,
            ]
        )

    if ref.step_name == "develop":
        evidence = steps["test"]["notes"] or "(No additional test notes recorded.)"
        return "\n".join(
            [
                f"You own task {task_label} cycle {ref.cycle_number} step develop.",
                "Required skill: superpowers:test-driven-development.",
                "Preserve the spec-derived test intent. Do not redefine behavior from the plan or implementation convenience.",
                "Only touch implementation files for this task unless a minimal test alignment change is unavoidable.",
                "Use the failing-test evidence below, implement the minimum change, run the targeted test, and return GREEN_CONFIRMED only with fresh verification.",
                "",
                "Failing-test evidence:",
                evidence,
                "",
                task_excerpt,
            ]
        )

    review_context = steps["develop"]["notes"] or "(No implementation notes recorded.)"
    return "\n".join(
        [
            f"You own task {task_label} cycle {ref.cycle_number} step self-check.",
            "Run spec review first against the spec refs and spec excerpt. Only if spec review passes, run code quality review second.",
            "Do not merge these into one verdict.",
            "Produce a structured review report JSON with verdict, summary, inputs, and rules.",
            "Return one of: APPROVED, SPEC_GAPS, QUALITY_GAPS, NEEDS_CONTEXT.",
            "Required review inputs: spec_refs, spec_excerpt, task_text, test_evidence, develop_evidence, changed_files, verification_summary, previous_review_deltas.",
            "Required rules: spec-compliance, behavioral-correctness, test-quality, regression-risk, complexity-yagni, interface-contract, verification-evidence.",
            "",
            "Implementation notes:",
            review_context,
            "",
            task_excerpt,
        ]
    )


def state_summary(state: Dict[str, Any]) -> Dict[str, Any]:
    refresh_all_statuses(state)
    summary_tasks = []
    for task in state["tasks"]:
        cycle = get_cycle(task, task["current_cycle"])
        summary_tasks.append(
            {
                "index": task["index"],
                "task_id": task.get("task_id"),
                "title": task["title"],
                "status": task["status"],
                "current_cycle": task["current_cycle"],
                "steps": {step["name"]: {"status": step["status"], "result": step["result"]} for step in cycle["steps"]},
            }
        )

    blocked = [{"task": ref.task_index, "cycle": ref.cycle_number, "step": ref.step_name} for ref in blocked_steps(state)]
    next_ref = next_actionable_step(state)
    next_step = summarize_step(state, next_ref) if next_ref else None

    return {
        "plan_path": state["plan_path"],
        "plan_format": state.get("plan_format", "legacy-task-headings"),
        "plan_title": state["plan_title"],
        "complete": plan_complete(state),
        "open_agents": state["open_agents"],
        "blocked_steps": blocked,
        "next_step": next_step,
        "tasks": summary_tasks,
    }


def print_json(data: Dict[str, Any]) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_init(args: argparse.Namespace) -> int:
    state = parse_plan(args.plan)
    save_state(args.state, state)
    print_json(
        {
            "state_path": normalize_path(args.state),
            "task_count": len(state["tasks"]),
            "task_order": [task.get("task_id") for task in state["tasks"]],
            "plan_format": state["plan_format"],
            "plan_title": state["plan_title"],
        }
    )
    return 0


def cmd_validate_plan(args: argparse.Namespace) -> int:
    state = parse_plan(args.plan)
    print_json(
        {
            "plan_path": state["plan_path"],
            "plan_title": state["plan_title"],
            "plan_format": state["plan_format"],
            "task_count": len(state["tasks"]),
            "task_order": [task.get("task_id") for task in state["tasks"]],
        }
    )
    return 0


def _auto_classify_files(file_list: List[str]) -> Dict[str, List[str]]:
    import re
    test_files: List[str] = []
    impl_files: List[str] = []
    doc_files: List[str] = []

    def _norm(p: str) -> str:
        return p.replace("\\", "/")

    for f in file_list:
        nf = _norm(f)
        name = os_path_basename(f).lower()
        # Test files: paths containing /tests/ or /test/, or files with test/mock naming
        if (re.search(r'(?:^|/)tests?/', nf)
                or name.startswith("test_")
                or name.startswith("tests_")
                or "mock_" in name
                or "_test." in name):
            test_files.append(f)
        elif f.endswith(".md"):
            doc_files.append(f)
        else:
            impl_files.append(f)
    return {"test": test_files, "implementation": impl_files, "docs": doc_files}


def _ensure_non_empty_files(files: Dict[str, List[str]], task_id: str) -> Dict[str, List[str]]:
    result = dict(files)
    normalized_id = task_id.replace("-", "_")
    if not result.get("test"):
        result["test"] = [f"tests/test_{normalized_id}"]
    if not result.get("implementation"):
        result["implementation"] = [f"src/{normalized_id}"]
    if "docs" not in result:
        result["docs"] = []
    return result


def fix_task_graph(graph: Any) -> Dict[str, Any]:
    if not isinstance(graph, dict):
        raise OrchestrationError("Task graph must be a JSON object.")

    fixes_applied: List[str] = []

    version = graph.get("version")
    if isinstance(version, str):
        graph["version"] = 1
        fixes_applied.append("version: converted string to integer 1")
    elif isinstance(version, (int, float)) and version != 1:
        graph["version"] = 1
        fixes_applied.append("version: normalized to integer 1")

    raw_tasks = graph.get("tasks", [])
    if not isinstance(raw_tasks, list):
        raise OrchestrationError("Task graph must include a 'tasks' list.")

    for idx, raw_task in enumerate(raw_tasks):
        if not isinstance(raw_task, dict):
            continue

        task_id = raw_task.get("id", f"tasks[{idx}]")

        reasons = raw_task.get("dependency_reasons", {})
        if isinstance(reasons, list):
            deps = raw_task.get("depends_on", [])
            if not deps:
                raw_task["dependency_reasons"] = {}
            elif len(deps) == 1 and len(reasons) >= 1:
                raw_task["dependency_reasons"] = {deps[0]: "; ".join(str(r) for r in reasons if r)}
            elif len(deps) == len(reasons):
                raw_task["dependency_reasons"] = {dep: str(reason) for dep, reason in zip(deps, reasons)}
            else:
                merged = {dep: (str(reasons[idx]) if idx < len(reasons) else "dependency from plan") for idx, dep in enumerate(deps)}
                raw_task["dependency_reasons"] = merged
            fixes_applied.append(f"{task_id}.dependency_reasons: converted array to object")

        files = raw_task.get("files")
        if isinstance(files, list):
            classified = _auto_classify_files(files)
            raw_task["files"] = _ensure_non_empty_files(classified, task_id)
            fixes_applied.append(f"{task_id}.files: converted array to object")
        elif isinstance(files, dict):
            raw_task["files"] = _ensure_non_empty_files(files, task_id)

        verification = raw_task.get("verification")
        if isinstance(verification, dict):
            for key in ("targeted", "full"):
                val = verification.get(key)
                if isinstance(val, str):
                    verification[key] = [val]
                    fixes_applied.append(f"{task_id}.verification.{key}: converted string to array")

        notes = raw_task.get("notes", [])
        if isinstance(notes, str):
            raw_task["notes"] = [notes]
            fixes_applied.append(f"{task_id}.notes: converted string to array")

        acceptance = raw_task.get("acceptance")
        if isinstance(acceptance, str):
            raw_task["acceptance"] = [acceptance]
            fixes_applied.append(f"{task_id}.acceptance: converted string to array")

    return {"graph": graph, "fixes": fixes_applied}


def cmd_fix_plan(args: argparse.Namespace) -> int:
    plan_path = Path(args.plan)
    if not plan_path.exists():
        raise OrchestrationError(f"Plan file not found: {plan_path}")

    content = plan_path.read_text(encoding="utf-8")

    fence_match = None
    for match in FENCED_BLOCK_RE.finditer(content):
        info = match.group(1).strip().lower()
        if "orchestration-task-graph" in info or info in ("json", "javascript", "js"):
            fence_match = match
            break

    if fence_match is None:
        raise OrchestrationError("No fenced JSON block found in plan file.")

    payload = fence_match.group(2).strip()
    try:
        graph = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise OrchestrationError(f"Task graph JSON is invalid: {exc}") from exc

    result = fix_task_graph(graph)
    fixed_graph = result["graph"]
    fixes = result["fixes"]

    new_payload = json.dumps(fixed_graph, ensure_ascii=False, indent=2)
    new_fence = "```orchestration-task-graph"
    old_fence_start = fence_match.start()
    old_fence_end = fence_match.end()

    new_content = (
        content[:old_fence_start]
        + new_fence + "\n"
        + new_payload + "\n"
        + "```"
        + content[old_fence_end:]
    )

    plan_path.write_text(new_content, encoding="utf-8")

    print_json(
        {
            "plan_path": str(plan_path),
            "fixes_applied": fixes,
            "fix_count": len(fixes),
            "message": "Plan file auto-fixed. Run validate-plan to confirm." if fixes else "No fixes needed.",
        }
    )
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    summary = state_summary(state)
    print_json(summary)
    return 0


def cmd_next(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    ref = ensure_step_ref(state, args.task, args.cycle, args.step)
    print_json(summarize_step(state, ref))
    return 0


def cmd_next_parallel(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    steps = parallel_ready_set(state)
    print_json({"parallel_count": len(steps), "steps": steps})
    return 0


def cmd_register_agent(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    ref = ensure_step_ref(state, args.task, args.cycle, args.step)
    record = register_agent(state, ref, args.agent_id)
    save_state(args.state, state)
    print_json(record)
    return 0


def cmd_complete_step(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    report = load_review_report(args.report)
    result = complete_step(state, args.agent_id, args.result, args.notes or "", report)
    save_state(args.state, state)
    print_json(result)
    return 0


def cmd_close_agent(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    record = close_agent(state, args.agent_id)
    save_state(args.state, state)
    print_json(record)
    return 0


def cmd_cancel_agent(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    record = cancel_agent(state, args.agent_id)
    save_state(args.state, state)
    print_json(record)
    return 0


def cmd_retry_step(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    ref = StepRef(task_index=args.task, cycle_number=args.cycle, step_name=args.step)
    result = retry_step(state, ref)
    save_state(args.state, state)
    print_json(result)
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    summary = state_summary(state)
    if not summary["complete"]:
        raise OrchestrationError("Plan is not complete yet.")
    print_json(summary)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Stateful plan orchestrator for fresh-subagent workflows.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Parse a plan and create orchestration state.")
    init_parser.add_argument("--plan", required=True, help="Path to the implementation plan markdown file.")
    init_parser.add_argument("--state", required=True, help="Path to the state JSON file to create.")
    init_parser.set_defaults(func=cmd_init)

    validate_parser = subparsers.add_parser("validate-plan", help="Validate the normalized task graph and print execution order.")
    validate_parser.add_argument("--plan", required=True, help="Path to the normalized implementation plan markdown file.")
    validate_parser.set_defaults(func=cmd_validate_plan)

    fix_parser = subparsers.add_parser("fix-plan", help="Auto-fix common format deviations in a normalized plan.")
    fix_parser.add_argument("--plan", required=True, help="Path to the normalized implementation plan markdown file to fix in place.")
    fix_parser.set_defaults(func=cmd_fix_plan)

    status_parser = subparsers.add_parser("status", help="Show the current orchestration state.")
    status_parser.add_argument("--state", required=True, help="Path to the state JSON file.")
    status_parser.set_defaults(func=cmd_status)

    next_parser = subparsers.add_parser("next", help="Show the next actionable step and its prompt.")
    next_parser.add_argument("--state", required=True, help="Path to the state JSON file.")
    next_parser.add_argument("--task", type=int, help="Optional explicit task index.")
    next_parser.add_argument("--cycle", type=int, help="Optional explicit cycle number.")
    next_parser.add_argument("--step", choices=STEP_ORDER, help="Optional explicit step name.")
    next_parser.set_defaults(func=cmd_next)

    next_parallel_parser = subparsers.add_parser(
        "next-parallel", help="Show all steps that can execute in parallel."
    )
    next_parallel_parser.add_argument("--state", required=True, help="Path to the state JSON file.")
    next_parallel_parser.set_defaults(func=cmd_next_parallel)

    register_parser = subparsers.add_parser("register-agent", help="Register a fresh agent for a step.")
    register_parser.add_argument("--state", required=True, help="Path to the state JSON file.")
    register_parser.add_argument("--agent-id", required=True, help="External agent identifier to track.")
    register_parser.add_argument("--task", type=int, help="Optional explicit task index.")
    register_parser.add_argument("--cycle", type=int, help="Optional explicit cycle number.")
    register_parser.add_argument("--step", choices=STEP_ORDER, help="Optional explicit step name.")
    register_parser.set_defaults(func=cmd_register_agent)

    complete_parser = subparsers.add_parser("complete-step", help="Record a step result for an open agent.")
    complete_parser.add_argument("--state", required=True, help="Path to the state JSON file.")
    complete_parser.add_argument("--agent-id", required=True, help="Agent identifier previously registered.")
    complete_parser.add_argument("--result", required=True, help="Step result code.")
    complete_parser.add_argument("--notes", help="Optional result notes for the next step.")
    complete_parser.add_argument("--report", help="Path to a structured JSON review report for self-check steps.")
    complete_parser.set_defaults(func=cmd_complete_step)

    close_parser = subparsers.add_parser("close-agent", help="Close an agent after its result is consumed.")
    close_parser.add_argument("--state", required=True, help="Path to the state JSON file.")
    close_parser.add_argument("--agent-id", required=True, help="Agent identifier to close.")
    close_parser.set_defaults(func=cmd_close_agent)

    cancel_parser = subparsers.add_parser("cancel-agent", help="Cancel an open agent and reset its step to pending.")
    cancel_parser.add_argument("--state", required=True, help="Path to the state JSON file.")
    cancel_parser.add_argument("--agent-id", required=True, help="Agent identifier to cancel.")
    cancel_parser.set_defaults(func=cmd_cancel_agent)

    retry_parser = subparsers.add_parser("retry-step", help="Reset a blocked step back to pending.")
    retry_parser.add_argument("--state", required=True, help="Path to the state JSON file.")
    retry_parser.add_argument("--task", type=int, required=True, help="Task index.")
    retry_parser.add_argument("--cycle", type=int, required=True, help="Cycle number.")
    retry_parser.add_argument("--step", required=True, choices=STEP_ORDER, help="Step name.")
    retry_parser.set_defaults(func=cmd_retry_step)

    check_parser = subparsers.add_parser("check", help="Assert that the full plan is complete and clean.")
    check_parser.add_argument("--state", required=True, help="Path to the state JSON file.")
    check_parser.set_defaults(func=cmd_check)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except OrchestrationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
