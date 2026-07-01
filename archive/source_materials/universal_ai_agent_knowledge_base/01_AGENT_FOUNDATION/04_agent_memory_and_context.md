# Память и контекст агента

## Контекст бывает трех типов

1. **Project context** — README, AGENTS.md, architecture docs.
2. **Task context** — issue, bug report, stack trace, expected behavior.
3. **Historical context** — предыдущие решения, handoff, known issues.

## Правило контекста

Агент не должен тащить весь репозиторий в промпт. Он должен строить минимальный релевантный контекст.

## Индекс репозитория

Нужен `repo_index.json`:

- path;
- file type;
- size;
- last modified;
- imports;
- test coverage relation;
- owner module;
- risk level.

## Handoff

После каждой задачи агент обновляет `HANDOFF.md`:

- что сделано;
- где проверено;
- что не проверено;
- следующий безопасный шаг.
