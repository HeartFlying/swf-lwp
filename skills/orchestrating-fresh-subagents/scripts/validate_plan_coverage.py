#!/usr/bin/env python3
"""Post-normalization semantic checks for plan coverage.

Run after validate-plan passes to catch issues the structural validator
cannot detect (e.g., spec refs not pointing to existing files, overly
generic acceptance criteria).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

FENCED_BLOCK_RE = re.compile(r"```([^\n`]*)\n(.*?)\n```", re.DOTALL)


def extract_graph(plan_path: Path) -> dict:
    content = plan_path.read_text(encoding="utf-8")
    for match in FENCED_BLOCK_RE.finditer(content):
        info = match.group(1).strip().lower()
        if "orchestration-task-graph" in info:
            return json.loads(match.group(2))
    raise ValueError("No orchestration-task-graph fenced block found")


def check_coverage(plan_path: Path) -> list[str]:
    """Return a list of warnings. Empty list means all checks passed."""
    warnings: list[str] = []
    graph = extract_graph(plan_path)
    root = plan_path.parent

    seen_ids: set[str] = set()
    for idx, task in enumerate(graph.get("tasks", [])):
        tid = task.get("id", f"tasks[{idx}]")

        if tid in seen_ids:
            warnings.append(f"[{tid}] duplicate task id")
        seen_ids.add(tid)

        for ref in task.get("spec_refs", []):
            if not (root / ref).exists():
                warnings.append(f"[{tid}] spec_ref '{ref}' file not found")

        for f in task.get("files", {}).get("test", []):
            if not (root / f).exists():
                warnings.append(f"[{tid}] test file '{f}' does not exist (will be created)")

        for f in task.get("files", {}).get("implementation", []):
            ext = Path(f).suffix
            known_exts = {".py", ".go", ".ts", ".tsx", ".js", ".cpp", ".h", ".rs", ".java"}
            if ext and ext not in known_exts:
                warnings.append(f"[{tid}] impl file '{f}' has unrecognized extension '{ext}'")

        for label, cmds in task.get("verification", {}).items():
            for cmd in cmds:
                if not cmd.strip():
                    warnings.append(f"[{tid}] verification.{label} contains empty command")

        generic_acceptance = {"done", "works", "passes", "complete", "finished", "ok"}
        for ac in task.get("acceptance", []):
            if ac.strip().lower() in generic_acceptance:
                warnings.append(f"[{tid}] acceptance criterion '{ac}' is too generic")

    for task in graph.get("tasks", []):
        for dep in task.get("depends_on", []):
            if dep not in seen_ids:
                warnings.append(f"[{task.get('id')}] depends on unknown task '{dep}'")

    return warnings


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: validate_plan_coverage.py <plan-file>", file=sys.stderr)
        return 2
    plan_path = Path(sys.argv[1])
    if not plan_path.exists():
        print(f"error: plan file not found: {plan_path}", file=sys.stderr)
        return 1

    warnings = check_coverage(plan_path)
    if warnings:
        print(f"Coverage warnings ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")
        print("\nReview these warnings before proceeding. Fix real issues, ignore false positives.")
        return 0
    else:
        print("Coverage check passed: no warnings.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
