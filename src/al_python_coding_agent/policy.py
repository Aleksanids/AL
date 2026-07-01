from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath, PureWindowsPath
from typing import Literal


CommandStatus = Literal["allow", "approval_required", "deny"]


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


def normalize_repo_path(path: str) -> str:
    windows_path = PureWindowsPath(path)
    parts = windows_path.parts if len(windows_path.parts) > 1 else PurePosixPath(path).parts
    clean_parts = [part for part in parts if part not in ("", ".")]
    return "/".join(clean_parts).rstrip("/")


def path_matches(path: str, boundary: str) -> bool:
    normalized_boundary = normalize_repo_path(boundary)
    if not normalized_boundary:
        return False
    return path == normalized_boundary or path.startswith(normalized_boundary.rstrip("/") + "/")


def assess_command(command: str) -> CommandDecision:
    normalized = " ".join(command.casefold().split())
    if any(fragment in normalized for fragment in DENY_COMMAND_FRAGMENTS):
        return CommandDecision("deny", "command matches denylist")
    if any(fragment in normalized for fragment in APPROVAL_COMMAND_FRAGMENTS):
        return CommandDecision("approval_required", "command requires explicit approval")
    if any(normalized.startswith(prefix) for prefix in ALLOW_COMMAND_PREFIXES):
        return CommandDecision("allow", "command matches allowlist")
    return CommandDecision("approval_required", "command is not in allowlist")
