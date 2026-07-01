# Copilot Instructions

Use `AGENTS.md` as the canonical repository instruction file.

This repository defines `AL Python Coding Agent`, a Russian-language coding
agent profile for Python development. Prefer:

- local context before new code;
- existing project patterns before new abstractions;
- typed public boundaries;
- pure core logic separated from IO/CLI/network/UI;
- `pathlib.Path` for filesystem work;
- focused tests for behavior and edge cases;
- explicit errors instead of silent fallbacks.

Never suggest reading secrets, `.env`, cookies, tokens, passwords, browser
profiles, or private URLs. Do not suggest package installs, live API calls,
browser automation, commits, pushes, PRs, or destructive git commands unless
the user explicitly asks for them.
