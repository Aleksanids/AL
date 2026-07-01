# Secrets policy

## Секреты

- API keys;
- tokens;
- passwords;
- private keys;
- cookies;
- connection strings;
- cloud credentials.

## Запреты

1. Не коммитить секреты.
2. Не печатать секреты в логах.
3. Не вставлять секреты в prompt/report.
4. Не менять `.env` без явного approval.
5. Не создавать `.env` с реальными значениями.

## Проверка

Добавить secrets scanner в CI или pre-commit.
