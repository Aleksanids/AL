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
    allowed_paths: tuple[str, ...] = field(default_factory=tuple)
    forbidden_paths: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def from_text(
        cls,
        title: str,
        body: str = "",
        *,
        allowed_paths: tuple[str, ...] = (),
        forbidden_paths: tuple[str, ...] = (),
    ) -> "TaskSpec":
        return cls(
            title=title,
            body=body,
            task_type=classify_task(title, body),
            allowed_paths=allowed_paths,
            forbidden_paths=forbidden_paths,
        )


def classify_task(title: str, body: str = "") -> TaskType:
    text = f"{title}\n{body}".casefold()
    for task_type, keywords in KEYWORD_RULES:
        if any(keyword.casefold() in text for keyword in keywords):
            return task_type
    return "unknown"
