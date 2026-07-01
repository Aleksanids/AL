---
name: python-engineering
description: Писать, исправлять и проверять Python-код с typed boundaries, minimal diff, tests и quality gates.
---

# Python Engineering

## When To Use

Используй для Python modules, CLI, parsers, data processing, automation,
adapters, tests, typing, linting, packaging и refactor.

## Principles

- Local style first.
- Standard library before new dependency.
- Pure core, thin shell.
- Typed public boundaries.
- Explicit errors.
- Deterministic IO.
- Tests for behavior and risk.

## Procedure

1. Прочитай nearby code, tests, configs и docs.
2. Сформулируй contract: input, output, side effects, errors, performance.
3. Выбери минимальное изменение.
4. Реализуй core отдельно от IO/CLI/API.
5. Добавь focused tests или объясни, почему они не нужны/недоступны.
6. Запусти доступные checks.
7. Перед финалом проверь diff и status.

## Preferred Checks

```powershell
python -m py_compile <changed .py files>
python -m unittest discover -s tests
pytest <targeted tests>
ruff format --check <paths>
ruff check <paths>
mypy <paths>
git diff --check
```

Запускай только то, что реально применимо и доступно.
