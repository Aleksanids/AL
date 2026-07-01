# Branching strategy

## Рекомендация

- main всегда рабочий;
- короткие feature branches;
- PR обязателен;
- squash merge для небольших задач;
- release tags;
- protected branch rules.

## Для AI-агента

Каждая задача агента создаёт отдельную ветку:

```text
agent/<task-id>-short-title
```
