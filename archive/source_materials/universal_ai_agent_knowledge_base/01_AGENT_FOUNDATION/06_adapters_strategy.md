# Adapter strategy

Агент должен быть независим от одного инструмента.

## Адаптеры

| Adapter | Назначение |
|---|---|
| `manual` | Создаёт промпт и план без автозапуска |
| `codex-cli` | Передаёт задачу Codex CLI |
| `cursor-notes` | Формирует инструкцию для Cursor |
| `github-copilot-agent` | Готовит issue/agent profile/PR workflow |
| `aider-cli` | Передаёт задачу Aider |
| `dry-run` | Проверяет план без изменения файлов |

## Правило

Первый релиз должен иметь надежный `manual` и `dry-run`. Автоматическое изменение кода — только после стабильной проверки scope/security.
