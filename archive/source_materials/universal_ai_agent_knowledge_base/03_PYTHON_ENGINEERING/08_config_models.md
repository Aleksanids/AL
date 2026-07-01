# Конфиги и модели данных

## Использовать модели

Для задач, политик и отчётов нужны схемы:

- `TaskSpec`;
- `ProjectConfig`;
- `QualityGateConfig`;
- `AgentRunReport`;
- `CommandResult`;
- `DiffSummary`.

## Правило

Не передавать важные структуры как сырые dict без валидации.
