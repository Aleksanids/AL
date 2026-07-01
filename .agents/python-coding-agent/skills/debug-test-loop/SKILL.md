---
name: debug-test-loop
description: Воспроизвести Python-дефект, сузить причину, внести минимальный fix и подтвердить regression test.
---

# Debug Test Loop

## Loop Contract

- `max_iterations`: 3
- Stop if the same failure repeats twice.
- Stop if scope expands beyond the user task.
- Every iteration must produce evidence: command, failure, hypothesis, next
  patch or explicit blocker.

## Procedure

1. Reproduce: получить фактический error/log/test failure.
2. Localize: найти минимальный file/function boundary.
3. Hypothesize: записать проверяемую причину.
4. Patch: изменить только нужный слой.
5. Verify: targeted test first, then relevant wider checks.
6. Generalize: добавить regression test, если дефект может вернуться.

## Output

- Reproduction command.
- Root cause.
- Changed files.
- Tests and outcomes.
- Remaining risk.
