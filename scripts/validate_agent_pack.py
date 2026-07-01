from __future__ import annotations

import argparse
import json
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

REQUIRED_ROOT_FILES = (
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    ".cursorrules",
    ".env.example",
    ".github/copilot-instructions.md",
    ".github/pull_request_template.md",
    ".github/workflows/ci.yml",
    ".gitattributes",
    ".gitignore",
    "docs/research-notes.md",
    "archive/source_materials/SOURCE_PROOF.md",
    "archive/source_materials/universal_ai_agent_knowledge_base/README.md",
    "src/al_python_coding_agent/__init__.py",
    "src/al_python_coding_agent/task_model.py",
    "src/al_python_coding_agent/policy.py",
    "src/al_python_coding_agent/autoconnect.py",
    "src/al_python_coding_agent/routing.py",
    "src/al_python_coding_agent/task_io.py",
    "src/al_python_coding_agent/adapters.py",
    "src/al_python_coding_agent/runner.py",
    "src/al_python_coding_agent/cli.py",
    "tests/test_autoconnect.py",
    "tests/test_core_policy.py",
    "tests/test_routing.py",
    "tests/test_runner.py",
    "pyproject.toml",
)

REQUIRED_AGENT_FILES = (
    ".agents/python-coding-agent/agent.json",
    ".agents/python-coding-agent/system_prompt.md",
    ".agents/python-coding-agent/workflows/closed_loop_python_task.md",
    ".agents/python-coding-agent/checklists/python_quality_gate.md",
    ".agents/python-coding-agent/checklists/security_and_context_gate.md",
    ".agents/python-coding-agent/templates/task_card.md",
)

MIN_TEXT_BYTES = 80
DEFAULT_ROUTE_KEY = "default"
FORBIDDEN_SECRET_MARKERS = (
    "BEGIN " + "RSA PRIVATE KEY",
    "BEGIN " + "OPENSSH PRIVATE KEY",
    "AWS_" + "SECRET_ACCESS_KEY=",
    "OPENAI_" + "API_KEY=",
    "ANTHROPIC_" + "API_KEY=",
    "pass" + "word=",
)

EXCLUDED_SCAN_PARTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "cookies",
    "cookie",
    "dist",
    "env",
    "secrets",
    "secret",
    "tokens",
    "token",
    "venv",
}

KNOWN_QUALITY_GATES = {
    "agent_pack_validation",
    "python_syntax",
    "unit_tests",
    "diff_check",
    "forbidden_paths_check",
    "secrets_scan",
    "ruff_format_check",
    "ruff_lint",
    "type_check",
    "security_scan",
}


@dataclass(frozen=True)
class CheckResult:
    path: str
    ok: bool
    message: str


def default_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_file_exists(
    root: Path,
    relative_path: str,
    *,
    min_bytes: int = MIN_TEXT_BYTES,
) -> CheckResult:
    path = root / relative_path
    if not path.is_file():
        return CheckResult(relative_path, False, "missing")
    try:
        content = read_utf8(path)
    except UnicodeDecodeError as exc:
        return CheckResult(relative_path, False, f"not utf-8: {exc}")
    if len(content.encode("utf-8")) < min_bytes:
        return CheckResult(relative_path, False, f"too small: < {min_bytes} bytes")
    return CheckResult(relative_path, True, "ok")


def check_required_files(root: Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    for relative_path in REQUIRED_ROOT_FILES:
        results.append(check_file_exists(root, relative_path))
    for relative_path in REQUIRED_AGENT_FILES:
        results.append(check_file_exists(root, relative_path))
    return results


def load_manifest(root: Path) -> tuple[dict[str, object] | None, CheckResult]:
    manifest_path = root / ".agents/python-coding-agent/agent.json"
    try:
        manifest = json.loads(read_utf8(manifest_path))
    except FileNotFoundError:
        return None, CheckResult(str(manifest_path.relative_to(root)), False, "missing")
    except json.JSONDecodeError as exc:
        return None, CheckResult(
            str(manifest_path.relative_to(root)),
            False,
            f"invalid json: {exc}",
        )
    return manifest, CheckResult(str(manifest_path.relative_to(root)), True, "json ok")


def iter_manifest_paths(manifest: dict[str, object]) -> Iterable[str]:
    agent_relative_keys = {"roles", "skills", "workflows", "checklists", "templates"}
    root_relative_keys = {
        "policies",
        "quality_gates",
        "evals",
        "examples",
        "prompts",
        "source_materials",
    }
    for key in agent_relative_keys:
        items = manifest.get(key, [])
        if not isinstance(items, list):
            continue
        for item in items:
            if isinstance(item, dict) and isinstance(item.get("path"), str):
                yield ".agents/python-coding-agent/" + item["path"]
    for key in root_relative_keys:
        items = manifest.get(key, [])
        if not isinstance(items, list):
            continue
        for item in items:
            if isinstance(item, dict) and isinstance(item.get("path"), str):
                yield item["path"]


def check_manifest(root: Path) -> list[CheckResult]:
    manifest, manifest_result = load_manifest(root)
    results = [manifest_result]
    if manifest is None:
        return results

    for key in ("id", "name", "version", "language", "mission"):
        value = manifest.get(key)
        if isinstance(value, str) and value.strip():
            results.append(CheckResult(f"agent.json:{key}", True, "ok"))
        else:
            results.append(CheckResult(f"agent.json:{key}", False, "missing or empty"))

    for key in ("roles", "skills"):
        results.extend(check_unique_manifest_ids(manifest, key))

    for relative_path in iter_manifest_paths(manifest):
        results.append(check_file_exists(root, relative_path))
    results.extend(check_agent_routes(manifest))
    return results


def check_agent_routes(manifest: dict[str, object]) -> list[CheckResult]:
    routes = manifest.get("agent_routes")
    if not isinstance(routes, dict):
        return [CheckResult("agent_routes", False, "missing or not an object")]

    task_types = manifest.get("task_types", [])
    role_ids = manifest_item_ids(manifest, "roles")
    skill_ids = manifest_item_ids(manifest, "skills")
    results: list[CheckResult] = []
    if DEFAULT_ROUTE_KEY not in routes:
        results.append(CheckResult("agent_routes", False, "missing default route"))
    if isinstance(task_types, list):
        for task_type in task_types:
            if isinstance(task_type, str) and task_type != "unknown" and task_type not in routes:
                results.append(
                    CheckResult("agent_routes", False, f"missing route for task type: {task_type}")
                )
    for route_name, route_config in routes.items():
        if not isinstance(route_name, str) or not isinstance(route_config, dict):
            results.append(CheckResult("agent_routes", False, "route must be an object"))
            continue
        agents = route_string_items(route_config, "agents")
        skills = route_string_items(route_config, "skills")
        quality_gates = route_string_items(route_config, "quality_gates")
        if not agents:
            results.append(CheckResult(f"agent_routes:{route_name}", False, "empty agents"))
        if not skills:
            results.append(CheckResult(f"agent_routes:{route_name}", False, "empty skills"))
        if not quality_gates:
            results.append(CheckResult(f"agent_routes:{route_name}", False, "empty quality_gates"))
        for agent_id in agents:
            if agent_id not in role_ids:
                results.append(
                    CheckResult(f"agent_routes:{route_name}", False, f"unknown agent: {agent_id}")
                )
        for skill_id in skills:
            if skill_id not in skill_ids:
                results.append(
                    CheckResult(f"agent_routes:{route_name}", False, f"unknown skill: {skill_id}")
                )
        for gate_id in quality_gates:
            if gate_id not in KNOWN_QUALITY_GATES:
                results.append(
                    CheckResult(f"agent_routes:{route_name}", False, f"unknown gate: {gate_id}")
                )
    if not results:
        results.append(CheckResult("agent_routes", True, f"{len(routes)} routes ok"))
    return results


def check_unique_manifest_ids(manifest: dict[str, object], key: str) -> list[CheckResult]:
    items = manifest.get(key, [])
    if not isinstance(items, list):
        return [CheckResult(f"agent.json:{key}", False, "not a list")]
    seen: set[str] = set()
    duplicates: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            continue
        item_id = item.get("id")
        if not isinstance(item_id, str):
            continue
        if item_id in seen:
            duplicates.add(item_id)
        seen.add(item_id)
    if duplicates:
        return [
            CheckResult(
                f"agent.json:{key}",
                False,
                "duplicate ids: " + ", ".join(sorted(duplicates)),
            )
        ]
    return [CheckResult(f"agent.json:{key}", True, f"{len(seen)} unique ids")]


def manifest_item_ids(manifest: dict[str, object], key: str) -> frozenset[str]:
    values: set[str] = set()
    items = manifest.get(key, [])
    if not isinstance(items, list):
        return frozenset()
    for item in items:
        if not isinstance(item, dict):
            continue
        item_id = item.get("id")
        if isinstance(item_id, str):
            values.add(item_id)
    return frozenset(values)


def route_string_items(route_config: dict[object, object], key: str) -> tuple[str, ...]:
    value = route_config.get(key, [])
    if not isinstance(value, list):
        return ()
    return tuple(item for item in value if isinstance(item, str))


def check_secret_markers(root: Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    text_files = [
        path
        for path in root.rglob("*")
        if path.is_file()
        and not is_excluded_from_scan(path, root)
        and path.suffix.lower() in {".md", ".json", ".toml", ".py", ".yaml", ".yml", ""}
    ]
    for path in text_files:
        relative = str(path.relative_to(root))
        try:
            content = read_utf8(path)
        except UnicodeDecodeError as exc:
            results.append(CheckResult(relative, False, f"not utf-8: {exc}"))
            continue
        found = [marker for marker in FORBIDDEN_SECRET_MARKERS if marker in content]
        if found:
            results.append(CheckResult(relative, False, "forbidden marker: " + ", ".join(found)))
    if not results:
        results.append(CheckResult("secret-scan", True, "no forbidden markers"))
    return results


def is_excluded_from_scan(path: Path, root: Path) -> bool:
    relative_parts = {part.casefold() for part in path.relative_to(root).parts}
    file_name = path.name.casefold()
    is_env_file = file_name == ".env" or (
        file_name.startswith(".env.") and file_name != ".env.example"
    )
    return is_env_file or bool(relative_parts & EXCLUDED_SCAN_PARTS)


def run_checks(root: Path) -> list[CheckResult]:
    return [
        *check_required_files(root),
        *check_manifest(root),
        *check_secret_markers(root),
    ]


def print_results(results: Sequence[CheckResult]) -> None:
    for result in results:
        status = "PASS" if result.ok else "FAIL"
        print(f"{status} {result.path} - {result.message}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the AL Python Coding Agent pack.")
    parser.add_argument(
        "--root",
        type=Path,
        default=default_root(),
        help="Repository root. Defaults to the parent directory of this script.",
    )
    args = parser.parse_args(argv)

    root = args.root.resolve()
    results = run_checks(root)
    print_results(results)
    return 0 if all(result.ok for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
