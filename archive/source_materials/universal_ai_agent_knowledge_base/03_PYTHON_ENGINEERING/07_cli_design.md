# CLI design для агента

## Команды

```bash
agent init
agent run task.yaml
agent plan task.yaml
agent verify --last
agent report --last
agent eval
```

## Правила

- dry-run по умолчанию для опасных операций;
- подробный report path;
- machine-readable JSON output;
- human-readable Markdown report;
- понятные exit codes.
