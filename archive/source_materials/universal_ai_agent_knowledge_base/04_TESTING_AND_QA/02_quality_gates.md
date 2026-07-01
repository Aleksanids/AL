# Quality gates

## Минимальный набор

1. `format_check`;
2. `lint`;
3. `type_check`;
4. `unit_tests`;
5. `integration_tests`;
6. `security_scan`;
7. `secrets_scan`;
8. `forbidden_paths_check`;
9. `diff_size_check`;
10. `docs_check`.

## Правило

Если gate не запущен, отчёт должен явно указать причину.
