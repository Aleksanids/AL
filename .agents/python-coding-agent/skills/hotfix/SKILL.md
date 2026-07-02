---
name: hotfix
description: Срочно исправить узкий дефект без превращения в refactor или feature.
---

# Hotfix

## Trigger

Production-breaking or user-blocking defect with narrow expected behavior.

## Workflow

1. Reproduce or identify exact failing path.
2. Define allowed paths.
3. Patch the smallest layer.
4. Add regression test if feasible.
5. Run targeted checks.
6. Report what remains unverified.

## Forbidden

- broad refactor;
- dependency churn;
- unrelated cleanup;
- deleting tests to pass CI.

## Output

- exact failing path or user-visible symptom;
- changed files;
- targeted checks and outcomes;
- unverified risks after the urgent fix.
