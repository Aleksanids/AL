from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from al_python_coding_agent.adapters import AdapterName, AdapterResult, run_adapter
from al_python_coding_agent.policy import PathScope
from al_python_coding_agent.task_io import load_task
from al_python_coding_agent.task_model import TaskSpec

PY_COMPILE_COMMAND = " ".join(
    (
        "python -m py_compile",
        "src/al_python_coding_agent/__init__.py",
        "src/al_python_coding_agent/task_model.py",
        "src/al_python_coding_agent/policy.py",
        "src/al_python_coding_agent/task_io.py",
        "src/al_python_coding_agent/adapters.py",
        "src/al_python_coding_agent/runner.py",
        "src/al_python_coding_agent/cli.py",
        "scripts/validate_agent_pack.py",
        "tests/test_agent_pack.py",
        "tests/test_core_policy.py",
        "tests/test_runner.py",
    )
)


QUALITY_GATE_COMMANDS: dict[str, str] = {
    "python_syntax": PY_COMPILE_COMMAND,
    "unit_tests": "python -m unittest discover -s tests",
    "diff_check": "git diff --check",
    "agent_pack_validation": "python scripts/validate_agent_pack.py",
    "forbidden_paths_check": "internal: PathScope.check",
    "secrets_scan": "internal: validate_agent_pack secret-scan",
    "ruff_format_check": "python -m ruff format --check .",
    "ruff_lint": "python -m ruff check .",
    "type_check": "python -m mypy src scripts",
    "security_scan": "python -m bandit -r src scripts -q",
}

DEFAULT_GATES = ("agent_pack_validation", "python_syntax", "unit_tests", "diff_check")


@dataclass(frozen=True)
class TaskRunResult:
    task: TaskSpec
    dry_run: bool
    adapter_result: AdapterResult
    plan_steps: tuple[str, ...]
    quality_gates: tuple[str, ...]
    quality_gate_commands: tuple[str, ...]
    scope_summary: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "title": self.task.title,
            "task_type": self.task.task_type,
            "priority": self.task.priority,
            "dry_run": self.dry_run,
            "adapter": self.adapter_result.adapter,
            "adapter_status": self.adapter_result.status,
            "adapter_command": list(self.adapter_result.command),
            "plan_steps": list(self.plan_steps),
            "quality_gates": list(self.quality_gates),
            "quality_gate_commands": list(self.quality_gate_commands),
            "scope_summary": list(self.scope_summary),
        }


def run_task_file(
    task_path: Path,
    *,
    adapter: AdapterName = "manual",
    execute: bool = False,
) -> TaskRunResult:
    task = load_task(task_path)
    gates = task.quality_gates or DEFAULT_GATES
    plan_steps = build_plan(task)
    gate_commands = tuple(
        QUALITY_GATE_COMMANDS.get(gate, f"unknown gate: {gate}") for gate in gates
    )
    scope_summary = build_scope_summary(task)
    prompt = build_adapter_prompt(task, plan_steps, gate_commands)
    adapter_result = run_adapter(adapter, prompt, execute=execute)
    return TaskRunResult(
        task=task,
        dry_run=not execute,
        adapter_result=adapter_result,
        plan_steps=plan_steps,
        quality_gates=gates,
        quality_gate_commands=gate_commands,
        scope_summary=scope_summary,
    )


def build_plan(task: TaskSpec) -> tuple[str, ...]:
    must_read = ", ".join(task.must_read) if task.must_read else "AGENTS.md, README.md"
    steps = [
        f"Confirm repo root and read: {must_read}",
        f"Classify task as: {task.task_type}",
        "Build context from allowed paths before editing.",
        "Create minimal patch only after scope and acceptance criteria are clear.",
        "Run quality gates and record exact outcomes.",
        "Send diff to critic/verifier before final handoff.",
    ]
    if task.acceptance_criteria:
        steps.insert(2, "Acceptance criteria: " + "; ".join(task.acceptance_criteria))
    return tuple(steps)


def build_scope_summary(task: TaskSpec) -> tuple[str, ...]:
    scope = PathScope(task.allowed_paths, task.forbidden_paths)
    allowed_paths = ", ".join(task.allowed_paths) if task.allowed_paths else "<not constrained>"
    forbidden_paths = ", ".join(task.forbidden_paths) if task.forbidden_paths else "<none>"
    summary = [
        f"allowed_paths: {allowed_paths}",
        f"forbidden_paths: {forbidden_paths}",
    ]
    for path in (*task.allowed_paths, *task.forbidden_paths):
        decision = scope.check(path)
        summary.append(f"{path}: {'allow' if decision.allowed else 'deny'} ({decision.reason})")
    return tuple(summary)


def build_adapter_prompt(
    task: TaskSpec,
    plan_steps: tuple[str, ...],
    quality_gate_commands: tuple[str, ...],
) -> str:
    return "\n".join(
        [
            "You are AL Python Coding Agent implementer.",
            f"Task: {task.title}",
            f"Type: {task.task_type}",
            f"Priority: {task.priority}",
            "Context:",
            task.body or "<empty>",
            "Plan:",
            *[f"{index}. {step}" for index, step in enumerate(plan_steps, start=1)],
            "Quality gates:",
            *[f"- {command}" for command in quality_gate_commands],
            "Do not edit files outside allowed_paths. Do not read secrets.",
        ]
    )


def format_result(result: TaskRunResult, *, as_json: bool = False) -> str:
    if as_json:
        return json.dumps(result.to_dict(), ensure_ascii=False, indent=2)
    lines = [
        f"Task: {result.task.title}",
        f"Type: {result.task.task_type}",
        f"Dry run: {result.dry_run}",
        f"Adapter: {result.adapter_result.adapter} ({result.adapter_result.status})",
        "",
        "Plan:",
        *[f"{index}. {step}" for index, step in enumerate(result.plan_steps, start=1)],
        "",
        "Quality gates:",
        *[f"- {command}" for command in result.quality_gate_commands],
        "",
        "Scope:",
        *[f"- {item}" for item in result.scope_summary],
    ]
    if result.adapter_result.command:
        lines.extend(["", "Adapter command:", " ".join(result.adapter_result.command)])
    return "\n".join(lines)
