# Workflow: Closed-Loop Python Task

## Goal

Доводить Python-задачу до проверяемого результата без раздувания scope.

## Steps

1. **Intake**
   - Переформулировать задачу.
   - Зафиксировать success criteria.
   - Отметить запреты: secrets, raw data, install, live network, destructive ops.

2. **Root And Context**
   - `git rev-parse --show-toplevel`
   - `git status --short --branch`
   - `rg --files` для инструкций, configs, tests, target files.

3. **Route**
   - Выбрать роли из `agent.json`.
   - Выбрать минимальный набор skills.

4. **Plan**
   - 3-7 шагов.
   - Только один `in_progress`.
   - Обновлять план при смене состояния.

5. **Implement**
   - Минимальный patch.
   - Existing patterns first.
   - Pure logic separated from IO.
   - Public boundaries typed.

6. **Verify**
   - Cheap checks first.
   - Targeted tests before broad tests.
   - Record exact commands and outcomes.

7. **Review**
   - Найти regressions, missing tests, security/data risks.
   - Проверить diff на unrelated changes.

8. **Report**
   - Что сделано.
   - Измененные файлы.
   - Проверки.
   - Ограничения.
   - Следующий шаг.

## Stop Conditions

- Same failure repeats twice.
- Scope expands beyond the task.
- Needed data is missing and guessing is risky.
- A command would read secrets or mutate user/raw data.
