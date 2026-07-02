from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatchcase
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Literal

CommandStatus = Literal["allow", "approval_required", "deny"]

AGENTIGNORE_FILE = ".agentignore"
AGENTIGNORE_SECTIONS = ("deny_read_write", "read_only", "generated")


DENY_COMMAND_FRAGMENTS = (
    "rm -rf /",
    "curl",
    "| bash",
    "wget",
    "| sh",
    "invoke-webrequest",
    "| iex",
    "encodedcommand",
    "chmod -r 777",
    "cat .env",
    "git reset --hard",
    "git checkout --",
)

APPROVAL_COMMAND_FRAGMENTS = (
    "pip install",
    "uv add",
    "poetry add",
    "npm install",
    "playwright",
    "selenium",
    "docker run",
    "git push",
    "gh pr create",
    "deploy",
)

ALLOW_COMMAND_PREFIXES = (
    "git status",
    "git diff",
    "python -m py_compile",
    "python -m unittest",
    "pytest",
    "ruff check",
    "ruff format --check",
    "mypy",
)


@dataclass(frozen=True)
class CommandDecision:
    status: CommandStatus
    reason: str


@dataclass(frozen=True)
class PathDecision:
    allowed: bool
    reason: str


@dataclass(frozen=True)
class PathScope:
    allowed_paths: tuple[str, ...] = ()
    forbidden_paths: tuple[str, ...] = ()

    def check(self, path: str) -> PathDecision:
        normalized = normalize_repo_path(path)
        if any(path_matches(normalized, forbidden) for forbidden in self.forbidden_paths):
            return PathDecision(False, f"forbidden path: {path}")
        if not self.allowed_paths:
            return PathDecision(True, "no allowed_paths constraint")
        if any(path_matches(normalized, allowed) for allowed in self.allowed_paths):
            return PathDecision(True, "within allowed_paths")
        return PathDecision(False, f"outside allowed_paths: {path}")


@dataclass(frozen=True)
class AgentBoundaryPolicy:
    deny_read_write: tuple[str, ...] = ()
    read_only: tuple[str, ...] = ()
    generated: tuple[str, ...] = ()
    source: str = AGENTIGNORE_FILE

    def blocked_paths(self) -> tuple[str, ...]:
        return dedupe_paths((*self.deny_read_write, *self.generated))

    def prompt_lines(self) -> tuple[str, ...]:
        return (
            f"source: {self.source}",
            "deny_read_write: " + format_paths(self.deny_read_write),
            "read_only: " + format_paths(self.read_only),
            "generated: " + format_paths(self.generated),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "source": self.source,
            "deny_read_write": list(self.deny_read_write),
            "read_only": list(self.read_only),
            "generated": list(self.generated),
            "blocked_paths": list(self.blocked_paths()),
        }


def normalize_repo_path(path: str) -> str:
    windows_path = PureWindowsPath(path)
    parts = windows_path.parts if len(windows_path.parts) > 1 else PurePosixPath(path).parts
    clean_parts = [part for part in parts if part not in ("", ".")]
    return "/".join(clean_parts).rstrip("/")


def path_matches(path: str, boundary: str) -> bool:
    normalized_boundary = normalize_repo_path(boundary)
    if not normalized_boundary:
        return False
    if "*" in normalized_boundary:
        pattern = normalized_boundary.rstrip("/")
        return fnmatchcase(path, pattern) or any(
            fnmatchcase(part, pattern) for part in path.split("/")
        )
    return path == normalized_boundary or path.startswith(normalized_boundary.rstrip("/") + "/")


def load_agentignore(root: Path) -> AgentBoundaryPolicy:
    agentignore_path = root / AGENTIGNORE_FILE
    if not agentignore_path.is_file():
        return default_agent_boundary_policy()
    return parse_agentignore(
        agentignore_path.read_text(encoding="utf-8"),
        source=AGENTIGNORE_FILE,
    )


def default_agent_boundary_policy() -> AgentBoundaryPolicy:
    return AgentBoundaryPolicy(
        deny_read_write=(".env", ".env.*", "secrets/"),
        generated=(".venv/", ".mypy_cache/", ".pytest_cache/", ".ruff_cache/", "build/", "dist/"),
        source="<built-in>",
    )


def parse_agentignore(content: str, *, source: str = AGENTIGNORE_FILE) -> AgentBoundaryPolicy:
    sections: dict[str, list[str]] = {section: [] for section in AGENTIGNORE_SECTIONS}
    current_section: str | None = None
    for line_number, raw_line in enumerate(content.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip()
            if section not in sections:
                raise ValueError(f"Unknown {source} section at line {line_number}: {section}")
            current_section = section
            continue
        if current_section is None:
            raise ValueError(f"Pattern outside section in {source} at line {line_number}: {line}")
        sections[current_section].append(line)
    return AgentBoundaryPolicy(
        deny_read_write=dedupe_paths(tuple(sections["deny_read_write"])),
        read_only=dedupe_paths(tuple(sections["read_only"])),
        generated=dedupe_paths(tuple(sections["generated"])),
        source=source,
    )


def dedupe_paths(paths: tuple[str, ...]) -> tuple[str, ...]:
    seen: set[str] = set()
    result: list[str] = []
    for path in paths:
        normalized = normalize_repo_path(path)
        if normalized and normalized not in seen:
            result.append(path)
            seen.add(normalized)
    return tuple(result)


def format_paths(paths: tuple[str, ...]) -> str:
    return ", ".join(paths) if paths else "<none>"


def assess_command(command: str) -> CommandDecision:
    normalized = " ".join(command.casefold().split())
    if any(fragment in normalized for fragment in DENY_COMMAND_FRAGMENTS):
        return CommandDecision("deny", "command matches denylist")
    if any(fragment in normalized for fragment in APPROVAL_COMMAND_FRAGMENTS):
        return CommandDecision("approval_required", "command requires explicit approval")
    if any(normalized.startswith(prefix) for prefix in ALLOW_COMMAND_PREFIXES):
        return CommandDecision("allow", "command matches allowlist")
    return CommandDecision("approval_required", "command is not in allowlist")
