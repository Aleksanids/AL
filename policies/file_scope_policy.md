# File Scope Policy

Every task should define file boundaries before edits.

The compact default boundary source is `.agentignore`. Task cards can add
stricter `allowed_paths` / `forbidden_paths`, but they should not remove hard
boundaries from `.agentignore`.

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
- `.agentignore` `deny_read_write` and `generated` entries are default blocked
  paths for auto-connected tasks.
- `.agentignore` `read_only` entries can be read when relevant but require
  explicit scope before writes.
- Hotfix scope cannot silently become a broad refactor.
- UI scope cannot silently mutate backend contracts.
- If a needed change crosses scope, stop and report why.
