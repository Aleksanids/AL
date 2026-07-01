# Архитектурные границы

## Типовые слои

```text
presentation / api / ui
application / use_cases
domain / business rules
infrastructure / db / file system / network
```

## Правила зависимостей

- domain не импортирует infrastructure;
- application знает domain, но не UI;
- UI вызывает application/use cases;
- infrastructure реализует интерфейсы;
- внешние SDK изолируются адаптерами.

## Agent check

Перед изменением агент должен ответить:

1. какой слой затронут;
2. есть ли пересечение слоёв;
3. не тянется ли инфраструктура в домен;
4. не ломается ли публичный контракт модуля.
