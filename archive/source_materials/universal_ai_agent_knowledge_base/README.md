# Universal AI Coding Agent Knowledge Base

Дата сборки: 2026-07-01

Назначение архива — дать Codex/Cursor/GitHub Copilot Agent максимально полную базу знаний для создания **универсального ИИ-агента по программированию**, который снижает количество ошибок в коде, архитектуре, UX, тестах, CI/CD и безопасности.

Архив **не привязан к конкретному приложению**. Его можно использовать для Python-проектов, web-приложений, desktop-приложений, CLI, backend, frontend и mixed repositories.

## Главная идея

Сильный coding-agent — это не просто LLM, которая пишет код. Это инженерный контур:

```text
задача → контекст → план → ограничение файлов → исполнитель → diff → проверки → critic → verifier → отчёт → handoff
```

Агент должен:

1. не начинать кодить без плана;
2. не менять файлы вне области задачи;
3. не принимать собственные изменения без проверки;
4. запускать статический анализ, тесты и security gates;
5. проверять UX и пользовательские сценарии, если задача затрагивает интерфейс;
6. формировать отчёт, который можно проверить фактами.

## Как использовать

1. Распаковать архив рядом с будущим репозиторием агента.
2. Открыть `00_CODEX_MASTER_PROMPT_CREATE_UNIVERSAL_AGENT.md`.
3. Передать этот файл Codex как основную задачу.
4. В качестве источников проекта приложить весь архив.
5. Попросить Codex создать GitHub-ready репозиторий агента.
6. После генерации репозитория прогнать чек-листы из `12_CHECKLISTS`.

## Важные разделы

| Раздел | Что внутри |
|---|---|
| `01_AGENT_FOUNDATION` | архитектура универсального агента |
| `02_PROGRAMMING_QUALITY` | качество кода, review, архитектура, anti-regression |
| `03_PYTHON_ENGINEERING` | Python best practices, tooling, pyproject, ruff, mypy, pytest |
| `04_TESTING_AND_QA` | тестовая стратегия, unit/integration/e2e, quality gates |
| `05_SECURITY_AND_SUPPLY_CHAIN` | OWASP, NIST SSDF, SLSA, GitHub Actions security |
| `06_UX_UI_DESIGN` | UX, UI, accessibility, heuristics, визуальное качество |
| `07_GITHUB_AND_CI` | GitHub repo, CI, PR, branch strategy, Dependabot |
| `08_AGENT_PROMPTS_AND_SKILLS` | агенты, skills, prompts, Cursor/Codex/GitHub profiles |
| `09_EVALUATION` | как проверять самого агента |
| `10_REPO_TEMPLATES` | готовые шаблоны файлов для будущего репозитория |
| `11_SOURCES` | карта источников и ссылок |
| `12_CHECKLISTS` | чек-листы приёмки |

## Принцип приёмки агента

Агент считается полезным только если он **уменьшает количество доработок после Codex/Cursor**, а не просто генерирует больше текста.
