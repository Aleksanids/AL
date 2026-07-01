# pyproject.toml guidance

`pyproject.toml` — центральный конфиг проекта.

В нём должны быть:

- build-system;
- project metadata;
- dependencies;
- optional dependencies для dev/test;
- ruff config;
- pytest config;
- mypy config;
- coverage config.

## Правило

Не размазывать конфиги по setup.cfg, tox.ini, pytest.ini, mypy.ini без необходимости.
