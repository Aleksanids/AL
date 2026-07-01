---
name: code-review
description: Проверить Python-код на bugs, regressions, missing tests, security и maintainability без ненужного rewrite.
---

# Code Review

## Review Stance

При review сначала выдавай findings, не summary.

## Severity

- `P0`: data loss, security leak, production outage.
- `P1`: likely bug or regression in normal use.
- `P2`: edge-case bug, missing critical test, maintainability risk.
- `P3`: style or clarity issue with low behavioral risk.

## Checklist

- Inputs validated?
- Errors observable?
- Paths Windows-safe?
- Raw files immutable?
- Network explicit and mockable?
- Tests cover behavior and edge cases?
- Typing protects public boundaries?
- Logs redact secrets?

## Output

```text
[P1] path/to/file.py:123 - Finding title
Evidence, impact, suggested fix.
```

If no findings: say so and mention residual test gaps.
