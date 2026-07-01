# Python Quality Gate

Используй перед финальным ответом по Python-задаче.

## Context

- [ ] Repo root подтвержден.
- [ ] Branch/status проверены.
- [ ] Project instructions прочитаны.
- [ ] Existing patterns найдены.
- [ ] Scope не расширен.

## Code

- [ ] Core logic отделена от IO/CLI/API.
- [ ] Public boundaries typed.
- [ ] Errors explicit.
- [ ] Paths через `pathlib.Path`.
- [ ] UTF-8 указан для text IO.
- [ ] Нет hidden network.
- [ ] Нет silent `except Exception: pass`.

## Tests

- [ ] Есть focused tests или объяснение, почему они не нужны.
- [ ] Проверены edge cases/error paths.
- [ ] Raw inputs не мутируются.
- [ ] Targeted checks запущены.

## Tooling

- [ ] `py_compile` или equivalent syntax check.
- [ ] Unit tests.
- [ ] `ruff` if configured.
- [ ] `mypy`/type checker if configured.
- [ ] `git diff --check`.

## Report

- [ ] Файлы перечислены.
- [ ] Команды и outcomes фактические.
- [ ] Ограничения честно названы.
- [ ] Next step не запускается без приемки, если он новый scope.
