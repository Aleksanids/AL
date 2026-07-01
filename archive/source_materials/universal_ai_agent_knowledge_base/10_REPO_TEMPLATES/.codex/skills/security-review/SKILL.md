---
name: security-review
description: Review code for security, secrets, dependency and workflow risks.
---

# security-review

## Purpose

Review code for security, secrets, dependency and workflow risks.

## Workflow

1. Confirm task type and scope.
2. Read required context.
3. Produce a short plan.
4. Identify allowed and forbidden files.
5. Execute only the necessary steps.
6. Run relevant quality gates.
7. Produce a factual report.

## Forbidden

- Do not expand scope without stating why.
- Do not hide failing checks.
- Do not remove tests to pass CI.
- Do not change secrets or environment files.
- Do not claim success without evidence.

## Report

```markdown
## Status

## Files changed

## Checks run

## Risks

## Next step
```
