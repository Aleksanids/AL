from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from al_python_coding_agent.adapters import AdapterName
from al_python_coding_agent.routing import find_agent_root
from al_python_coding_agent.runner import TaskRunResult, format_result, run_task
from al_python_coding_agent.task_model import TaskSpec, classify_task

DEFAULT_AUTOCONNECT_FORBIDDEN_PATHS = (
    ".env",
    ".env.*",
    "secrets/",
    "dist/",
    "build/",
)
DEFAULT_AUTOCONNECT_MUST_READ = ("AGENTS.md", "README.md")


@dataclass(frozen=True)
class AutoConnectResult:
    root: Path
    task_run: TaskRunResult

    def to_dict(self) -> dict[str, object]:
        task_data = self.task_run.to_dict()
        return {
            "auto_connected": True,
            "root": str(self.root),
            "task_type": self.task_run.task.task_type,
            "adapter": self.task_run.adapter_result.adapter,
            "adapter_status": self.task_run.adapter_result.status,
            "route": self.task_run.route_selection.to_dict(),
            "agents": task_data["agents"],
            "skills": task_data["skills"],
            "agent_instruction_paths": task_data["agent_instruction_paths"],
            "skill_instruction_paths": task_data["skill_instruction_paths"],
            "quality_gates": task_data["quality_gates"],
            "quality_gate_commands": task_data["quality_gate_commands"],
            "adapter_command": task_data["adapter_command"],
            "plan_steps": task_data["plan_steps"],
            "scope_summary": task_data["scope_summary"],
        }


def auto_connect_task(
    title: str,
    body: str = "",
    *,
    root: Path | None = None,
    adapter: AdapterName = "manual",
    execute: bool = False,
    allowed_paths: Sequence[str] = (),
    forbidden_paths: Sequence[str] | None = None,
) -> AutoConnectResult:
    agent_root = find_agent_root(root or Path.cwd())
    effective_forbidden_paths = (
        tuple(forbidden_paths)
        if forbidden_paths is not None
        else DEFAULT_AUTOCONNECT_FORBIDDEN_PATHS
    )
    task = TaskSpec(
        title=title,
        body=body,
        task_type=classify_task(title, body),
        allowed_paths=tuple(allowed_paths),
        forbidden_paths=effective_forbidden_paths,
        must_read=DEFAULT_AUTOCONNECT_MUST_READ,
    )
    task_run = run_task(task, task_root=agent_root, adapter=adapter, execute=execute)
    return AutoConnectResult(root=agent_root, task_run=task_run)


def format_auto_connect(result: AutoConnectResult, *, as_json: bool = False) -> str:
    if as_json:
        return json.dumps(result.to_dict(), ensure_ascii=False, indent=2)
    return "\n".join(
        [
            "AL auto-connect: connected",
            f"Root: {result.root}",
            "",
            format_result(result.task_run),
        ]
    )
