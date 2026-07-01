---
name: github-ci
description: Проверить или создать минимальный GitHub Actions CI с безопасными permissions и Python gates.
---

# GitHub CI

## Rules

- `permissions: contents: read` by default.
- No deploy/publish without approval.
- Pin official actions by major version at minimum.
- Run install, lint, type, test and security gates only if dependencies exist.
- Do not expose secrets to PRs from untrusted forks.

## Suggested Gates

- `ruff format --check`;
- `ruff check`;
- `mypy`;
- tests;
- security scan if configured.
