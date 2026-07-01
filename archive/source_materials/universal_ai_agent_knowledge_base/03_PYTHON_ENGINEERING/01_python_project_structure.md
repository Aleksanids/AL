# Python project structure

Рекомендуемая структура:

```text
project/
├─ pyproject.toml
├─ src/
│  └─ package_name/
│     ├─ __init__.py
│     ├─ cli.py
│     ├─ config.py
│     └─ ...
├─ tests/
│  ├─ unit/
│  ├─ integration/
│  └─ e2e/
├─ docs/
└─ README.md
```

## Почему `src` layout

`src` layout снижает риск случайных импортов из рабочей директории и лучше выявляет ошибки packaging/imports.

## Agent requirement

Если агент создает новый Python-проект, по умолчанию использовать `src` layout.
