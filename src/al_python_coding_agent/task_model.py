from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

TaskType = Literal[
    "bugfix",
    "hotfix",
    "feature",
    "refactor",
    "tests",
    "docs",
    "security",
    "ux",
    "ci",
    "release",
    "unknown",
]


KEYWORD_RULES: tuple[tuple[TaskType, tuple[str, ...]], ...] = (
    ("hotfix", ("hotfix", "urgent", "critical", "production", "prod", "срочно")),
    ("bugfix", ("bug", "fix", "traceback", "exception", "ошибка", "падает", "сломано")),
    ("feature", ("feature", "add", "implement", "new", "добавь", "реализуй")),
    ("refactor", ("refactor", "cleanup", "simplify", "рефактор")),
    ("tests", ("test", "pytest", "unittest", "coverage", "тест")),
    ("docs", ("doc", "readme", "documentation", "документ")),
    ("security", ("security", "secret", "token", "vulnerability", "безопас")),
    ("ux", ("ux", "ui", "interface", "accessibility", "интерфейс")),
    ("ci", ("ci", "github actions", "workflow", "pipeline")),
    ("release", ("release", "version", "changelog", "publish", "релиз")),
)


@dataclass(frozen=True)
class TaskSpec:
    title: str
    body: str = ""
    task_type: TaskType = "unknown"
    priority: str = "normal"
    context: dict[str, str] = field(default_factory=dict)
    allowed_paths: tuple[str, ...] = field(default_factory=tuple)
    forbidden_paths: tuple[str, ...] = field(default_factory=tuple)
    must_read: tuple[str, ...] = field(default_factory=tuple)
    requested_agents: tuple[str, ...] = field(default_factory=tuple)
    requested_skills: tuple[str, ...] = field(default_factory=tuple)
    acceptance_criteria: tuple[str, ...] = field(default_factory=tuple)
    quality_gates: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def from_text(
        cls,
        title: str,
        body: str = "",
        *,
        allowed_paths: tuple[str, ...] = (),
        forbidden_paths: tuple[str, ...] = (),
        acceptance_criteria: tuple[str, ...] = (),
        quality_gates: tuple[str, ...] = (),
    ) -> TaskSpec:
        return cls(
            title=title,
            body=body,
            task_type=classify_task(title, body),
            allowed_paths=allowed_paths,
            forbidden_paths=forbidden_paths,
            acceptance_criteria=acceptance_criteria,
            quality_gates=quality_gates,
        )

    @classmethod
    def from_mapping(cls, data: dict[str, object]) -> TaskSpec:
        title = string_value(data.get("title"), default="Untitled task")
        body = context_summary(data.get("context"))
        requested_type = string_value(data.get("type"), default="unknown")
        task_type = normalize_task_type(requested_type, title, body)
        return cls(
            title=title,
            body=body,
            task_type=task_type,
            priority=string_value(data.get("priority"), default="normal"),
            context=string_dict(data.get("context")),
            allowed_paths=string_tuple(data.get("allowed_paths")),
            forbidden_paths=string_tuple(data.get("forbidden_paths")),
            must_read=string_tuple(data.get("must_read")),
            requested_agents=first_string_tuple(data, "agents", "requested_agents"),
            requested_skills=first_string_tuple(data, "skills", "requested_skills"),
            acceptance_criteria=string_tuple(data.get("acceptance_criteria")),
            quality_gates=string_tuple(data.get("quality_gates")),
        )


def classify_task(title: str, body: str = "") -> TaskType:
    text = f"{title}\n{body}".casefold()
    for task_type, keywords in KEYWORD_RULES:
        if any(keyword.casefold() in text for keyword in keywords):
            return task_type
    return "unknown"


def normalize_task_type(value: str, title: str, body: str = "") -> TaskType:
    normalized = value.casefold()
    valid_types = {task_type for task_type, _keywords in KEYWORD_RULES}
    if normalized in valid_types:
        return normalized
    return classify_task(title, body)


def string_value(value: object, *, default: str = "") -> str:
    return value if isinstance(value, str) and value else default


def string_tuple(value: object) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    return tuple(item for item in value if isinstance(item, str))


def first_string_tuple(data: dict[str, object], *keys: str) -> tuple[str, ...]:
    for key in keys:
        values = string_tuple(data.get(key))
        if values:
            return values
    return ()


def string_dict(value: object) -> dict[str, str]:
    if not isinstance(value, dict):
        return {}
    return {
        str(key): item
        for key, item in value.items()
        if isinstance(key, str) and isinstance(item, str)
    }


def context_summary(value: object) -> str:
    context = string_dict(value)
    if not context:
        return ""
    return "\n".join(f"{key}: {item}" for key, item in context.items())
