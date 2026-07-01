from __future__ import annotations

import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from al_python_coding_agent.cli import main
from al_python_coding_agent.routing import (
    find_agent_root,
    load_agent_manifest,
    manifest_entries,
    route_matrix,
    route_task,
)


class RoutingTests(unittest.TestCase):
    def test_find_agent_root_from_example_task(self) -> None:
        task_path = ROOT / "examples" / "python_bugfix_task.yaml"

        self.assertEqual(ROOT, find_agent_root(task_path))

    def test_manifest_exposes_roles_and_skills(self) -> None:
        manifest = load_agent_manifest(ROOT)

        role_ids = {entry.id for entry in manifest_entries(manifest, "roles")}
        skill_ids = {entry.id for entry in manifest_entries(manifest, "skills")}

        self.assertIn("python_engineer", role_ids)
        self.assertIn("python-engineering", skill_ids)

    def test_bugfix_route_connects_agents_and_skills(self) -> None:
        manifest = load_agent_manifest(ROOT)

        route = route_task("bugfix", manifest)

        self.assertIn("python_engineer", route.agents)
        self.assertIn("test_engineer", route.agents)
        self.assertIn("roles/python_engineer.md", route.agent_paths)
        self.assertIn("bug-investigation", route.skills)
        self.assertIn("skills/bug-investigation/SKILL.md", route.skill_paths)
        self.assertEqual((), route.warnings)

    def test_requested_agents_and_skills_extend_route(self) -> None:
        manifest = load_agent_manifest(ROOT)

        route = route_task(
            "feature",
            manifest,
            requested_agents=("python_engineer", "security_guard"),
            requested_skills=("python-engineering", "security-review"),
        )

        self.assertEqual(1, route.agents.count("python_engineer"))
        self.assertIn("security_guard", route.agents)
        self.assertEqual(1, route.skills.count("python-engineering"))
        self.assertIn("security-review", route.skills)

    def test_unknown_route_falls_back_to_default(self) -> None:
        manifest = load_agent_manifest(ROOT)

        route = route_task("unknown", manifest)

        self.assertIn("chief_orchestrator", route.agents)
        self.assertIn("repository-intake", route.skills)

    def test_route_warns_for_unknown_links(self) -> None:
        manifest = {
            "roles": [{"id": "known_agent", "path": "roles/known_agent.md"}],
            "skills": [{"id": "known-skill", "path": "skills/known-skill/SKILL.md"}],
            "agent_routes": {
                "bugfix": {
                    "agents": ["known_agent", "missing_agent"],
                    "skills": ["known-skill", "missing-skill"],
                }
            },
        }

        route = route_task("bugfix", manifest)

        self.assertIn("unknown agent role: missing_agent", route.warnings)
        self.assertIn("unknown skill: missing-skill", route.warnings)

    def test_manifest_route_matrix_covers_core_task_types(self) -> None:
        manifest = load_agent_manifest(ROOT)
        routes = route_matrix(manifest)

        for task_type in ("bugfix", "hotfix", "feature", "refactor", "tests", "docs"):
            self.assertIn(task_type, routes)

    def test_cli_lists_agents(self) -> None:
        output = StringIO()

        with redirect_stdout(output):
            exit_code = main(["list-agents", "--root", str(ROOT)])

        self.assertEqual(0, exit_code)
        self.assertIn("python_engineer", output.getvalue())

    def test_cli_lists_skills(self) -> None:
        output = StringIO()

        with redirect_stdout(output):
            exit_code = main(["list-skills", "--root", str(ROOT)])

        self.assertEqual(0, exit_code)
        self.assertIn("python-engineering", output.getvalue())

    def test_cli_inspects_route(self) -> None:
        output = StringIO()

        with redirect_stdout(output):
            exit_code = main(["inspect-route", "--type", "bugfix", "--root", str(ROOT)])

        self.assertEqual(0, exit_code)
        self.assertIn("python_engineer", output.getvalue())
        self.assertIn("skills/bug-investigation/SKILL.md", output.getvalue())


if __name__ == "__main__":
    unittest.main()
