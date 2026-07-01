## Goal

What problem does this change solve?

## Scope

Allowed paths:

- ...

Forbidden paths:

- `.env`
- `secrets/`
- `dist/`
- `build/`

## Checks

- [ ] `python scripts/validate_agent_pack.py`
- [ ] `python -m py_compile src/al_python_coding_agent/__init__.py src/al_python_coding_agent/task_model.py src/al_python_coding_agent/policy.py src/al_python_coding_agent/task_io.py src/al_python_coding_agent/adapters.py src/al_python_coding_agent/runner.py src/al_python_coding_agent/cli.py scripts/validate_agent_pack.py tests/test_agent_pack.py tests/test_core_policy.py tests/test_runner.py`
- [ ] `python -m unittest discover -s tests`
- [ ] `python -m ruff format --check .`
- [ ] `python -m ruff check .`
- [ ] `python -m mypy src scripts`
- [ ] `python -m bandit -r src scripts -q`
- [ ] `git diff --check`

## Risks

Known risks or skipped gates:

- ...
