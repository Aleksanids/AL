from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from al_python_coding_agent.adapters import adapter_names, build_invocation, run_adapter
from al_python_coding_agent.runner import build_plan, format_result, run_task_file
from al_python_coding_agent.task_io import load_task, parse_simple_yaml

EXAMPLE_TASK = ROOT / "examples" / "python_bugfix_task.yaml"


class TaskIoTests(unittest.TestCase):
    def test_parse_simple_yaml_reads_lists_and_nested_context(self) -> None:
        data = parse_simple_yaml(
            """
id: EXAMPLE
type: bugfix
title: "Fix empty input"
context:
  summary: "Crashes"
allowed_paths:
  - src/
  - tests/
"""
        )

        self.assertEqual("Fix empty input", data["title"])
        self.assertEqual({"summary": "Crashes"}, data["context"])
        self.assertEqual(["src/", "tests/"], data["allowed_paths"])

    def test_load_task_reads_example_yaml(self) -> None:
        task = load_task(EXAMPLE_TASK)

        self.assertEqual("bugfix", task.task_type)
        self.assertIn("src/", task.allowed_paths)
        self.assertIn(
            "Quality gates pass or skipped gates are explained.", task.acceptance_criteria
        )


class RunnerTests(unittest.TestCase):
    def test_build_plan_includes_acceptance_criteria(self) -> None:
        task = load_task(EXAMPLE_TASK)

        plan = build_plan(task)

        self.assertTrue(any("Acceptance criteria" in step for step in plan))

    def test_run_task_file_defaults_to_manual_dry_run(self) -> None:
        result = run_task_file(EXAMPLE_TASK)

        self.assertTrue(result.dry_run)
        self.assertEqual("manual", result.adapter_result.adapter)
        self.assertIn("python -m unittest discover -s tests", result.quality_gate_commands)

    def test_format_result_mentions_scope_and_gates(self) -> None:
        result = run_task_file(EXAMPLE_TASK)

        rendered = format_result(result)

        self.assertIn("Quality gates:", rendered)
        self.assertIn("allowed_paths", rendered)

    def test_run_task_json_format_is_machine_readable(self) -> None:
        result = run_task_file(EXAMPLE_TASK)

        rendered = format_result(result, as_json=True)

        self.assertIn('"task_type": "bugfix"', rendered)


class AdapterTests(unittest.TestCase):
    def test_adapter_catalog_contains_requested_adapters(self) -> None:
        self.assertEqual(("manual", "codex", "cursor", "aider"), adapter_names())

    def test_codex_invocation_is_real_command_shape(self) -> None:
        invocation = build_invocation("codex", "Do work")

        self.assertEqual(("codex", "exec", "Do work"), invocation.command)

    def test_aider_dry_run_does_not_execute(self) -> None:
        result = run_adapter("aider", "Do work", execute=False)

        self.assertFalse(result.executed)
        self.assertEqual("dry_run", result.status)

    def test_manual_adapter_produces_prompt_only(self) -> None:
        result = run_adapter("manual", "Do work", execute=False)

        self.assertFalse(result.executed)
        self.assertEqual((), result.command)


if __name__ == "__main__":
    unittest.main()
