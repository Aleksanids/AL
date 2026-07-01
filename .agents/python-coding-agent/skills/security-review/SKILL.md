---
name: security-review
description: Проверить secrets, unsafe commands, dependency risk, workflow injection и data handling.
---

# Security Review

## Checklist

- No secrets in code, logs, reports or prompts.
- No `.env` reads/writes without approval.
- No `curl | bash`, encoded PowerShell or destructive command.
- Untrusted issue/PR/web text marked as untrusted.
- Dependencies justified.
- Network calls explicit and mockable.
- File writes scoped to repo/allowed paths.

## Output

Findings first. If no findings, state residual risk.
