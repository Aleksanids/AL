# CI pipeline

## Минимальный Python CI

1. checkout;
2. setup Python;
3. install deps;
4. ruff format check;
5. ruff lint;
6. mypy;
7. pytest;
8. coverage;
9. bandit;
10. artifacts: reports.

## Agent rule

Если CI падает, агент не может писать `done`.
