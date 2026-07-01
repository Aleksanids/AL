from __future__ import annotations

import json
from pathlib import Path

from al_python_coding_agent.task_model import TaskSpec


def load_task(path: Path) -> TaskSpec:
    content = path.read_text(encoding="utf-8")
    if path.suffix.casefold() == ".json":
        data = json.loads(content)
        if not isinstance(data, dict):
            raise ValueError("Task JSON must contain an object at the top level.")
        return TaskSpec.from_mapping(data)
    return TaskSpec.from_mapping(parse_simple_yaml(content))


def parse_simple_yaml(content: str) -> dict[str, object]:
    """Parse the small YAML subset used by AL task cards.

    The parser intentionally supports only top-level scalars, top-level lists,
    and one-level mappings. This keeps runtime dependencies at zero while still
    supporting `examples/python_bugfix_task.yaml`.
    """

    result: dict[str, object] = {}
    current_key: str | None = None
    for raw_line in content.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()
        if indent == 0:
            key, value = split_key_value(line)
            current_key = key
            result[key] = parse_scalar(value) if value else {}
            continue
        if current_key is None:
            raise ValueError(f"Indented YAML line without parent key: {raw_line!r}")
        if line.startswith("- "):
            current = result.get(current_key)
            if not isinstance(current, list):
                current = []
                result[current_key] = current
            current.append(parse_scalar(line[2:].strip()))
            continue
        key, value = split_key_value(line)
        current = result.get(current_key)
        if not isinstance(current, dict):
            current = {}
            result[current_key] = current
        current[key] = parse_scalar(value)
    return result


def split_key_value(line: str) -> tuple[str, str]:
    if ":" not in line:
        raise ValueError(f"Expected YAML key/value line: {line!r}")
    key, value = line.split(":", 1)
    key = key.strip()
    if not key:
        raise ValueError(f"Empty YAML key in line: {line!r}")
    return key, value.strip()


def parse_scalar(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value
