# Задача для Codex: создать универсального ИИ-агента по программированию на GitHub

## Цель

Создать новый GitHub-ready репозиторий универсального ИИ-агента по программированию.

Агент должен помогать писать, проверять, улучшать и безопасно изменять программные проекты. Он не должен быть привязан к конкретному приложению, предметной области или стеку, но первая реализация должна быть особенно сильной для Python-проектов.

## Главное требование

Не создавать «промпт-обёртку», которая просто просит LLM писать код.

Нужно создать инженерный агентный контур:

```text
задача → классификация → сбор контекста → план → file scope → исполнитель → diff → quality gates → critic → verifier → отчёт → handoff
```

## Что создать

Создай полноценный репозиторий:

```text
universal-ai-coding-agent/
├─ README.md
├─ AGENTS.md
├─ pyproject.toml
├─ .gitignore
├─ .env.example
├─ src/
├─ tests/
├─ agents/
├─ skills/
├─ prompts/
├─ policies/
├─ quality_gates/
├─ templates/
├─ docs/
├─ evals/
├─ examples/
├─ .github/
│  ├─ workflows/
│  ├─ agents/
│  ├─ ISSUE_TEMPLATE/
│  └─ pull_request_template.md
├─ .cursor/
│  ├─ rules/
│  └─ agents/
└─ .codex/
   └─ skills/
```

## Базовые возможности агента

Агент должен уметь:

1. принимать задачу в YAML/Markdown;
2. классифицировать задачу: bugfix, hotfix, feature, refactor, tests, UX, security, docs, CI;
3. собирать контекст репозитория;
4. строить индекс файлов;
5. определять allowed_paths и forbidden_paths;
6. создавать план изменения;
7. готовить task prompt для исполнителя;
8. поддерживать адаптеры: manual, Codex CLI, Cursor notes, GitHub Copilot agent, Aider;
9. проверять git diff;
10. запускать quality gates;
11. блокировать опасные shell-команды;
12. искать секреты в изменениях;
13. запускать critic review;
14. запускать verifier review;
15. формировать отчёт;
16. формировать handoff.

## Обязательные роли агентов

Создать роли:

1. `orchestrator` — управляет циклом задачи;
2. `planner` — строит план и scope;
3. `architect` — проверяет архитектуру;
4. `implementer` — пишет код;
5. `critic` — ищет ошибки и ложную готовность;
6. `verifier` — принимает только по фактам;
7. `python-quality-reviewer` — проверяет Python;
8. `security-reviewer` — проверяет безопасность;
9. `test-engineer` — проектирует и проверяет тесты;
10. `ux-reviewer` — проверяет UI/UX;
11. `github-ci-reviewer` — проверяет CI/CD и GitHub workflow;
12. `documentation-reviewer` — проверяет README, handoff и developer docs.

## Обязательные skills

Создать skills в формате `SKILL.md`:

1. `hotfix`;
2. `feature-development`;
3. `bug-investigation`;
4. `python-quality`;
5. `test-design`;
6. `security-review`;
7. `ux-review`;
8. `github-ci`;
9. `refactor-safety`;
10. `release-readiness`;
11. `technical-debt-control`;
12. `handoff-update`.

## Python-требования

Использовать современную структуру:

```text
src/<package>/
tests/
pyproject.toml
```

Обязательные инструменты:

- `ruff` для lint/format;
- `mypy` или совместимый type checker;
- `pytest`;
- `coverage`;
- `bandit`;
- опционально `semgrep`;
- `pre-commit`;
- GitHub Actions CI.

## Quality gates

Минимальные gates:

1. formatting check;
2. lint check;
3. type check;
4. unit tests;
5. integration tests, если применимо;
6. security scan;
7. secrets scan;
8. forbidden paths check;
9. dependency vulnerability check;
10. PR template completeness;
11. documentation updated;
12. UX review, если затронут UI.

## Запреты

Агенту запрещено:

- писать «готово» без проверок;
- менять файлы вне scope;
- запускать опасные shell-команды без явного approval;
- делать `curl | bash`;
- менять `.env`, secrets, tokens;
- делать массовый рефакторинг вместе с hotfix;
- удалять тесты ради прохождения CI;
- скрывать failing tests;
- подменять проверку рассуждением;
- принимать свой же код без critic/verifier.

## Security policy

Реализовать политику команд:

- allowlist безопасных команд;
- denylist опасных команд;
- логирование всех shell-команд;
- отдельное approval для установки зависимостей;
- запрет чтения файлов вне target repo;
- запрет записи в пользовательские системные директории;
- запрет публикации секретов в отчётах.

## UX policy

Если задача затрагивает интерфейс, агент должен проверять:

- понятность основного сценария;
- видимость статуса системы;
- предсказуемость действий;
- ошибки и восстановление;
- пустые состояния;
- loading states;
- keyboard navigation;
- доступность по WCAG;
- читаемость текста;
- визуальную иерархию;
- responsive behavior.

## Документация

Создать документацию:

1. как установить агента;
2. как подключить к репозиторию;
3. как создать задачу;
4. как запустить dry-run;
5. как запустить полный цикл;
6. как подключить Codex/Cursor/GitHub agents;
7. как добавлять новые skills;
8. как писать acceptance criteria;
9. как смотреть отчёт;
10. как проводить self-evaluation агента.

## Критерии приёмки

Репозиторий считается готовым, если:

1. устанавливается локально;
2. проходят тесты;
3. есть CI;
4. есть минимум 10 тестов на core logic;
5. есть пример задачи;
6. есть dry-run, который не меняет чужой проект;
7. есть report output;
8. есть agents/skills/prompts;
9. есть правила безопасности;
10. есть понятный README;
11. есть evaluation plan;
12. нет привязки к конкретному приложению.

## Итоговый отчёт Codex

После создания репозитория предоставь:

1. структуру файлов;
2. список реализованных возможностей;
3. какие проверки запущены;
4. результат тестов;
5. как создать GitHub repo;
6. как подключить к существующим проектам;
7. что осталось на v2.
