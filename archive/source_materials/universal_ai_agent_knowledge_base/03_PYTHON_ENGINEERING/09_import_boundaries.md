# Import boundaries

## Зачем

Линтер и типизатор не всегда ловят архитектурные нарушения.

## Проверять

- domain не импортирует infrastructure;
- core не импортирует adapters;
- tests не зависят от приватных деталей без причины;
- CLI не содержит business logic.

## Инструменты

Можно использовать import-linter или собственный checker.
