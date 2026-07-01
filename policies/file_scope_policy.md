# File Scope Policy

Every task should define file boundaries before edits.

## Required Fields

```yaml
allowed_paths:
  - src/
  - tests/
forbidden_paths:
  - .env
  - secrets/
  - dist/
  - build/
```

## Rules

- Files outside `allowed_paths` are read-only unless the plan explicitly
  expands scope.
- Files inside `forbidden_paths` are blocked.
- Hotfix scope cannot silently become a broad refactor.
- UI scope cannot silently mutate backend contracts.
- If a needed change crosses scope, stop and report why.
