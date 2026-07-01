# Shell command policy

## Denylist

Блокировать без approval:

```text
rm -rf /
curl ... | bash
wget ... | sh
Invoke-WebRequest ... | iex
powershell -EncodedCommand
chmod -R 777
sudo
scp secrets
cat .env
```

## Allowlist

Обычно безопасно:

```text
git status
git diff
python -m pytest
ruff check .
ruff format --check .
mypy src
```

## Правило

Все команды логируются с working directory, exit code и duration.
