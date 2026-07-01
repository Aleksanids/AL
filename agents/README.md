# Agents

Canonical role files live in:

```text
.agents/python-coding-agent/roles/
```

This top-level folder exists for tools that expect an `agents/` entrypoint.

Recommended route for Python tasks:

```text
chief_orchestrator -> repository_cartographer -> planner -> python_engineer
-> test_engineer -> code_reviewer -> verifier -> handoff_reporter
```

Add `security_guard`, `architect`, `ux_reviewer`, `github_ci_reviewer` or
`documentation_reviewer` only when the task touches those boundaries.
