---
name: python-quality
description: Проверить Python-код по formatting, lint, typing, tests, imports и runtime-safety.
---

# Python Quality

## Checks

- Syntax: `python -m py_compile`.
- Tests: targeted `unittest` or `pytest`.
- Format/lint: `ruff format --check`, `ruff check` when available.
- Typing: `mypy` or configured checker when available.
- Imports: no accidental cwd-only imports.
- Errors: no silent broad exceptions.

## Rule

Do not disable lint/type rules without a local explanation.
