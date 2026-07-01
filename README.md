# AL Python Coding Agent

`AL` - репозиторий с переносимым набором инструкций, ролей, навыков и
проверок для ИИ-агента, который помогает программировать на Python в локальных
репозиториях.

Главная идея: агент не "вайбит" код вслепую, а работает по короткому
проверяемому циклу:

```text
контекст -> маршрут ролей/skills -> план -> минимальное изменение -> проверка -> отчет
```

## Что внутри

- `AGENTS.md` - корневые инструкции для Codex и совместимых coding agents.
- `CLAUDE.md`, `.cursorrules`, `.github/copilot-instructions.md` - адаптеры
  для популярных агентных сред.
- `.agents/python-coding-agent/agent.json` - машинно-читаемый manifest агента.
- `.agents/python-coding-agent/system_prompt.md` - основной системный prompt.
- `.agents/python-coding-agent/roles/` - роли: orchestrator, Python engineer,
  reviewer, test engineer, security guard.
- `.agents/python-coding-agent/skills/` - переиспользуемые skills для Python
  engineering, repository intake, debug/test loop, review, refactor и handoff.
- `.agents/python-coding-agent/workflows/` - closed-loop workflow для задач.
- `.agents/python-coding-agent/checklists/` - quality и safety gates.
- `.agents/python-coding-agent/templates/` - шаблон task card.
- `policies/` - file scope, command, security и UX policies.
- `quality_gates/` - machine-readable gate matrix.
- `evals/` - план оценки качества самого агента.
- `examples/` - пример task card для Python bugfix.
- `archive/source_materials/` - копия и распакованные материалы
  `universal-ai-coding-agent-knowledge-base.zip`, использованные как источник.
- `docs/research-notes.md` - источники и выводы по GitHub, Habr и Python docs.
- `scripts/validate_agent_pack.py` - локальный валидатор структуры без внешних
  зависимостей.
- `src/al_python_coding_agent/autoconnect.py` - auto-connect слой: задача
  классифицируется из текста, route выбирается автоматически, agents/skills
  подключаются к adapter prompt без task card.
- `src/al_python_coding_agent/routing.py` - manifest-backed routing для
  выбора agents/skills по task type.
- `tests/` - smoke, policy, auto-connect, runner и routing tests.

## Быстрый старт

1. Открой репозиторий в coding agent.
2. Скажи агенту: "Следуй `AGENTS.md`; используй
   `.agents/python-coding-agent/agent.json` как manifest".
3. Для конкретной задачи заполни шаблон:
   `.agents/python-coding-agent/templates/task_card.md`.
4. Перед принятием результата запусти:

```powershell
$env:PYTHONPATH = "src"
python scripts/validate_agent_pack.py
python -m unittest discover -s tests
python -m al_python_coding_agent.cli run-task examples/python_bugfix_task.yaml
python -m al_python_coding_agent.cli auto-connect --title "Fix traceback on empty input"
```

## Принципы агента

- Сначала читать локальный контекст, потом менять код.
- Классифицировать задачу: bugfix, hotfix, feature, refactor, tests, docs,
  security, UX, CI или release.
- Для рискованных задач задавать `allowed_paths` и `forbidden_paths`.
- Не создавать новую архитектуру, если хватает существующего кода,
  стандартной библиотеки или уже установленных зависимостей.
- Держать core logic отдельно от CLI, файловой системы, сети и UI.
- Использовать типы как инженерный контракт, а не как декорацию.
- Проверять рисковые места тестами, линтером и type checker, если они
  настроены в целевом проекте.
- Не принимать собственный patch без critic/verifier слоя.
- Не читать секреты, `.env`, cookies, tokens, passwords и browser profiles.
- Не делать commit, push, PR, install, live API, browser automation или
  destructive operations без отдельной прямой команды пользователя.

## Проверки для этого репозитория

Этот репозиторий держит runtime без внешних зависимостей, а dev-инструменты
подключены через optional dependency group `dev`. Минимальная проверка:

```powershell
python -m py_compile src/al_python_coding_agent/__init__.py src/al_python_coding_agent/task_model.py src/al_python_coding_agent/policy.py src/al_python_coding_agent/autoconnect.py src/al_python_coding_agent/routing.py src/al_python_coding_agent/task_io.py src/al_python_coding_agent/adapters.py src/al_python_coding_agent/runner.py src/al_python_coding_agent/cli.py scripts/validate_agent_pack.py tests/test_agent_pack.py tests/test_autoconnect.py tests/test_core_policy.py tests/test_routing.py tests/test_runner.py
python scripts/validate_agent_pack.py
python -m unittest discover -s tests
```

Минимальный deterministic CLI core можно проверить так:

```powershell
$env:PYTHONPATH = "src"
python -m al_python_coding_agent.cli classify --title "Fix traceback on empty input"
python -m al_python_coding_agent.cli check-command "git status --short"
python -m al_python_coding_agent.cli check-path "src/package/module.py" --allow "src/" --forbid ".env"
python -m al_python_coding_agent.cli auto-connect --title "Fix traceback on empty input" --json
python -m al_python_coding_agent.cli run-task examples/python_bugfix_task.yaml
python -m al_python_coding_agent.cli list-agents
python -m al_python_coding_agent.cli list-skills
python -m al_python_coding_agent.cli inspect-route --type bugfix --json
```

## V0.3 Runner

Dry-run task planning:

```powershell
$env:PYTHONPATH = "src"
python -m al_python_coding_agent.cli run-task examples/python_bugfix_task.yaml
```

Adapter dry-run:

```powershell
$env:PYTHONPATH = "src"
python -m al_python_coding_agent.cli run-task examples/python_bugfix_task.yaml --adapter codex
python -m al_python_coding_agent.cli run-task examples/python_bugfix_task.yaml --adapter cursor
python -m al_python_coding_agent.cli run-task examples/python_bugfix_task.yaml --adapter aider
```

`--execute` запускает внешний CLI adapter только если он установлен в `PATH`.
По умолчанию runner ничего не меняет в проекте.

## V0.4 Agent/Skill Routing

`run-task` теперь читает `.agents/python-coding-agent/agent.json`, выбирает
route по `type` задачи и показывает подключенных agents/skills в dry-run:

```powershell
$env:PYTHONPATH = "src"
python -m al_python_coding_agent.cli run-task examples/python_bugfix_task.yaml
python -m al_python_coding_agent.cli run-task examples/python_bugfix_task.yaml --json
```

Для task cards можно явно добавить дополнительные роли и skills:

```yaml
agents:
  - security_guard
skills:
  - security-review
```

Manifest route matrix валидируется локальным validator: битые ссылки на
roles/skills считаются ошибкой pack-а.

Модель исполнения честная и переносимая: AL выбирает roles/skills, выводит их
instruction paths и добавляет их в adapter prompt. Начиная с v0.5 это можно
делать без task card через auto-connect. Отдельный запуск локальных subagents
зависит от host-среды (например, Codex/Cursor), но route/prompt подключение
теперь автоматическое.

Discovery:

```powershell
python -m al_python_coding_agent.cli list-agents
python -m al_python_coding_agent.cli list-skills
python -m al_python_coding_agent.cli inspect-route --type bugfix
```

## V0.5 Auto-connect

`auto-connect` подключает AL автоматически по тексту задачи: находит root с
manifest, классифицирует задачу, выбирает agent route, добавляет instruction
paths и собирает adapter prompt.

```powershell
$env:PYTHONPATH = "src"
python -m al_python_coding_agent.cli auto-connect --title "Fix traceback on empty input"
python -m al_python_coding_agent.cli auto-connect --title "Fix traceback on empty input" --adapter codex --json
```

По умолчанию команда работает как dry-run и не запускает внешний adapter.
`--execute` нужен явно. Для ограничения scope можно добавить `--allow src/`
и `--allow tests/`.

Dev tooling:

```powershell
python -m pip install -e ".[dev]"
python -m pytest
python -m ruff format --check .
python -m ruff check .
python -m mypy src scripts
python -m bandit -r src scripts -q
```
