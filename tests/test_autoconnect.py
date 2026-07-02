from __future__ import annotations

import json
import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from al_python_coding_agent.autoconnect import auto_connect_task, format_auto_connect
from al_python_coding_agent.cli import main


class AutoConnectTests(unittest.TestCase):
    def test_auto_connect_selects_route_without_task_card(self) -> None:
        result = auto_connect_task(
            "Fix traceback on empty input",
            root=ROOT,
            adapter="codex",
            allowed_paths=("src/", "tests/"),
        )

        self.assertTrue(result.task_run.dry_run)
        self.assertEqual("bugfix", result.task_run.task.task_type)
        self.assertIn("python_engineer", result.task_run.route_selection.agents)
        self.assertIn("bug-investigation", result.task_run.route_selection.skills)
        self.assertIn("roles/python_engineer.md", result.task_run.route_selection.agent_paths)
        self.assertIn(
            "skills/bug-investigation/SKILL.md",
            result.task_run.route_selection.skill_paths,
        )
        self.assertIn(
            "Before editing, read every listed",
            result.task_run.adapter_result.command[-1],
        )

    def test_auto_connect_has_default_safe_scope(self) -> None:
        result = auto_connect_task("Add new CLI command", root=ROOT)

        self.assertIn(".env: deny", "\n".join(result.task_run.scope_summary))
        self.assertIn(".venv/: deny", "\n".join(result.task_run.scope_summary))
        self.assertIn("build/: deny", "\n".join(result.task_run.scope_summary))

    def test_format_auto_connect_json_is_machine_readable(self) -> None:
        result = auto_connect_task("Write documentation", root=ROOT)

        rendered = format_auto_connect(result, as_json=True)
        data = json.loads(rendered)

        self.assertTrue(data["auto_connected"])
        self.assertEqual(str(ROOT), data["root"])
        self.assertIn("agents", data)
        self.assertIn("skill_instruction_paths", data)
        self.assertIn("boundary_policy", data)

    def test_cli_auto_connect_outputs_route_json(self) -> None:
        output = StringIO()

        with redirect_stdout(output):
            exit_code = main(
                [
                    "auto-connect",
                    "--title",
                    "Fix traceback on empty input",
                    "--root",
                    str(ROOT),
                    "--json",
                ]
            )

        data = json.loads(output.getvalue())

        self.assertEqual(0, exit_code)
        self.assertTrue(data["auto_connected"])
        self.assertEqual("bugfix", data["task_type"])
        self.assertIn("python_engineer", data["agents"])


if __name__ == "__main__":
    unittest.main()
