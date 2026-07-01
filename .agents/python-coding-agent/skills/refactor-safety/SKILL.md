---
name: refactor-safety
description: Управлять безопасным refactor без изменения поведения и scope drift.
---

# Refactor Safety

## Rules

- Establish baseline checks first.
- Refactor one boundary at a time.
- Preserve public API unless migration is explicit.
- No dependency churn.
- No hidden behavior changes.

## Acceptance

- Same tests pass before/after when feasible.
- Diff is explainable by structure improvement.
- Behavior changes are absent or explicitly approved.
