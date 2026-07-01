# Универсальная архитектура агента

```text
User task
  ↓
TaskSpec parser
  ↓
Task classifier
  ↓
Context builder
  ↓
Plan + file scope
  ↓
Executor adapter
  ↓
Patch / diff
  ↓
Quality gates
  ↓
Critic review
  ↓
Verifier review
  ↓
Report + handoff
```

## Принцип

Каждый этап должен иметь вход, выход и проверяемый результат.

## Почему так

Большинство ошибок AI-кодинга возникает не из-за одного плохого промпта, а из-за отсутствия инженерного контура: нет scope, нет тестов, нет diff-review, нет независимого critic.
