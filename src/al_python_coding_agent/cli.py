from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from al_python_coding_agent.adapters import adapter_names
from al_python_coding_agent.policy import PathScope, assess_command
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
        result = run_task_file(args.task_file, adapter=args.adapter, execute=args.execute)
        print(format_result(result, as_json=args.json))
        return 0 if result.adapter_result.status not in {"failed", "missing_executable"} else 2

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
