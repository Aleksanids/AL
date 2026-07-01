# Ruff policy

## Минимальные команды

```bash
ruff format .
ruff check .
ruff check . --fix
```

## Для CI

```bash
ruff format --check .
ruff check .
```

## Рекомендуемые группы правил

- `E`, `F` — pycodestyle/pyflakes;
- `I` — import sorting;
- `B` — bugbear;
- `UP` — modern Python upgrades;
- `SIM` — simplifications;
- `PL` — pylint-like checks;
- `RUF` — Ruff-specific checks.

## Agent rule

Агент не должен отключать правило Ruff без объяснения.
