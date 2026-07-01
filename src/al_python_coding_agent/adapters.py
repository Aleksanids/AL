from __future__ import annotations

import shutil
import subprocess  # nosec B404
from dataclasses import dataclass
from typing import Literal

AdapterName = Literal["manual", "codex", "cursor", "aider"]


@dataclass(frozen=True)
class AdapterInvocation:
    adapter: AdapterName
    command: tuple[str, ...]
    prompt: str


@dataclass(frozen=True)
class AdapterResult:
    adapter: AdapterName
    executed: bool
    status: str
    message: str
    command: tuple[str, ...] = ()
    returncode: int | None = None


def adapter_names() -> tuple[AdapterName, ...]:
    return ("manual", "codex", "cursor", "aider")


def build_invocation(adapter: AdapterName, prompt: str) -> AdapterInvocation:
    if adapter == "manual":
        return AdapterInvocation(adapter, (), prompt)
    if adapter == "codex":
        return AdapterInvocation(adapter, ("codex", "exec", prompt), prompt)
    if adapter == "cursor":
        return AdapterInvocation(adapter, ("cursor-agent", "-p", prompt), prompt)
    if adapter == "aider":
        return AdapterInvocation(adapter, ("aider", "--yes", "--message", prompt), prompt)
    raise ValueError(f"Unsupported adapter: {adapter}")


def run_adapter(
    adapter: AdapterName,
    prompt: str,
    *,
    execute: bool,
    timeout_seconds: int = 120,
) -> AdapterResult:
    invocation = build_invocation(adapter, prompt)
    if adapter == "manual":
        return AdapterResult(adapter, False, "dry_run", "Manual adapter produced a prompt only.")
    if not execute:
        return AdapterResult(
            adapter,
            False,
            "dry_run",
            "Adapter command was built but not executed.",
            invocation.command,
        )
    executable = invocation.command[0]
    if shutil.which(executable) is None:
        return AdapterResult(
            adapter,
            False,
            "missing_executable",
            f"Executable not found on PATH: {executable}",
            invocation.command,
        )
    # Adapter command is explicit argv and shell is never used.
    completed = subprocess.run(  # nosec B603
        invocation.command,
        capture_output=True,
        check=False,
        encoding="utf-8",
        errors="replace",
        timeout=timeout_seconds,
    )
    output = completed.stdout.strip() or completed.stderr.strip()
    return AdapterResult(
        adapter,
        True,
        "completed" if completed.returncode == 0 else "failed",
        output,
        invocation.command,
        completed.returncode,
    )
