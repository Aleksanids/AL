# Pytest policy

## Структура

```text
tests/unit/
tests/integration/
tests/e2e/
```

## Имена

- `test_<module>.py`;
- `test_<behavior>`;
- Arrange / Act / Assert.

## Правила

1. Тест должен проверять поведение, а не реализацию.
2. Один тест — одна причина падения.
3. Fixtures не должны скрывать важную логику.
4. Нельзя удалять тесты ради прохождения CI.
5. Regression bug требует regression test.
