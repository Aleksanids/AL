# Typing policy

## Правила

1. Public functions должны иметь type hints.
2. Dataclasses/Pydantic models использовать для структурированных данных.
3. `Any` допустим только временно и с комментарием.
4. Не использовать mutable defaults.
5. Возвращаемые типы должны быть явными.
6. Ошибки типизации нельзя скрывать массовыми ignores.

## Проверка

```bash
mypy src
```

или совместимый type checker.
