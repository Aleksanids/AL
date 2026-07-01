from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from al_python_coding_agent.adapters import adapter_names
from al_python_coding_agent.autoconnect import auto_connect_task, format_auto_connect
from al_python_coding_agent.policy import PathScope, assess_command
from al_python_coding_agent.routing import (
    RouteSelection,
    find_agent_root,
    load_agent_manifest,
    manifest_entries,
    route_task,
)
from al_python_coding_agent.runner import format_result, run_task_file
from al_python_coding_agent.task_model import classify_task


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="al-agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    classify = subparsers.add_parser("classify", help="Classify a task from title/body text.")
    classify.add_argument("--title", required=True)
    classify.add_argument("--body", default="")

    check_command = subparsers.add_parser("check-command", help="Assess shell command policy.")
    check_command.add_argument("shell_command")

    check_path = subparsers.add_parser("check-path", help="Check a path against scope policy.")
    check_path.add_argument("path")
    check_path.add_argument("--allow", action="append", default=[])
    check_path.add_argument("--forbid", action="append", default=[])

    run_task = subparsers.add_parser(
        "run-task",
        help="Build a task plan and optional adapter invocation.",
    )
    run_task.add_argument("task_file", type=Path)
    run_task.add_argument("--adapter", choices=adapter_names(), default="manual")
    run_task.add_argument(
        "--execute",
        action="store_true",
        help="Run the selected adapter command.",
    )
    run_task.add_argument("--json", action="store_true", help="Print machine-readable JSON.")

    auto_connect = subparsers.add_parser(
        "auto-connect",
        help="Auto-connect AL agents/skills from task text without a task card.",
    )
    auto_connect.add_argument("--title", required=True)
    auto_connect.add_argument("--body", default="")
    auto_connect.add_argument("--root", type=Path, default=Path.cwd())
    auto_connect.add_argument("--adapter", choices=adapter_names(), default="manual")
    auto_connect.add_argument("--allow", action="append", default=[])
    auto_connect.add_argument("--forbid", action="append")
    auto_connect.add_argument(
        "--execute",
        action="store_true",
        help="Run the selected adapter command.",
    )
    auto_connect.add_argument("--json", action="store_true", help="Print machine-readable JSON.")

    list_agents = subparsers.add_parser("list-agents", help="List connected agent roles.")
    list_agents.add_argument("--root", type=Path, default=Path.cwd())

    list_skills = subparsers.add_parser("list-skills", help="List connected skills.")
    list_skills.add_argument("--root", type=Path, default=Path.cwd())

    inspect_route = subparsers.add_parser("inspect-route", help="Inspect agent/skill route.")
    inspect_route.add_argument("--type", default="unknown", dest="task_type")
    inspect_route.add_argument("--root", type=Path, default=Path.cwd())
    inspect_route.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "classify":
        print(classify_task(args.title, args.body))
        return 0
    if args.command == "check-command":
        command_decision = assess_command(args.shell_command)
        print(f"{command_decision.status}: {command_decision.reason}")
        return 0 if command_decision.status == "allow" else 2
    if args.command == "check-path":
        scope = PathScope(tuple(args.allow), tuple(args.forbid))
        path_decision = scope.check(args.path)
        print(f"{'allow' if path_decision.allowed else 'deny'}: {path_decision.reason}")
        return 0 if path_decision.allowed else 2
    if args.command == "run-task":
        task_result = run_task_file(args.task_file, adapter=args.adapter, execute=args.execute)
        print(format_result(task_result, as_json=args.json))
        return 0 if task_result.adapter_result.status not in {"failed", "missing_executable"} else 2
    if args.command == "auto-connect":
        connect_result = auto_connect_task(
            args.title,
            args.body,
            root=args.root,
            adapter=args.adapter,
            execute=args.execute,
            allowed_paths=tuple(args.allow),
            forbidden_paths=tuple(args.forbid) if args.forbid is not None else None,
        )
        print(format_auto_connect(connect_result, as_json=args.json))
        return (
            0
            if connect_result.task_run.adapter_result.status not in {"failed", "missing_executable"}
            else 2
        )
    if args.command == "list-agents":
        print_manifest_entries(args.root, "roles")
        return 0
    if args.command == "list-skills":
        print_manifest_entries(args.root, "skills")
        return 0
    if args.command == "inspect-route":
        manifest = load_agent_manifest(find_agent_root(args.root))
        route = route_task(args.task_type, manifest)
        print(format_route(route, as_json=args.json))
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


def print_manifest_entries(root: Path, key: str) -> None:
    manifest = load_agent_manifest(find_agent_root(root))
    for entry in manifest_entries(manifest, key):
        print(f"{entry.id}\t{entry.path}")


def format_route(route: RouteSelection, *, as_json: bool = False) -> str:
    if as_json:
        return json.dumps(route.to_dict(), ensure_ascii=False, indent=2)
    lines = [
        "Agents:",
        *[f"- {agent}" for agent in route.agents],
        "",
        "Agent instruction files:",
        *[f"- {path}" for path in route.agent_paths],
        "",
        "Skills:",
        *[f"- {skill}" for skill in route.skills],
        "",
        "Skill instruction files:",
        *[f"- {path}" for path in route.skill_paths],
        "",
        "Quality gates:",
        *[f"- {gate}" for gate in route.quality_gates],
    ]
    if route.warnings:
        lines.extend(["", "Warnings:", *[f"- {warning}" for warning in route.warnings]])
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
