---
name: repository-intake
description: Быстро подтвердить root, scope, инструкции, структуру и доступные проверки перед изменениями.
---

# Repository Intake

## When To Use

Используй в начале любой non-trivial задачи в репозитории.

## Procedure

1. Подтверди root:
   `git rev-parse --show-toplevel`.
2. Проверь branch/status:
   `git status --short --branch`.
3. Найди инструкции:
   `rg --files -g "AGENTS.md" -g "CLAUDE.md" -g "README*"`.
4. Найди Python/config/test files:
   `rg --files -g "*.py" -g "pyproject.toml" -g "requirements*.txt" -g "tests/**"`.
5. Определи существующие patterns и доступные checks.
6. Зафиксируй forbidden paths и raw user data, если они есть.

## Output

- root;
- branch/status summary;
- relevant files;
- available checks;
- risks/unknowns.
