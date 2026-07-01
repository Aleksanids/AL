# Research Notes

Дата проверки: 2026-07-01.

Этот agent pack собран после просмотра похожих GitHub-проектов, Habr-материалов
и официальных источников Python tooling. Ниже - не копия чужих инструкций, а
синтез применимых паттернов для компактного Python coding agent.

## GitHub Patterns

- Aider: terminal pair programming, работа внутри локального git repo,
  codebase map и git-aware изменения.
  Source: https://github.com/aider-ai/aider
- SWE-agent: issue-to-fix workflow, автономное использование инструментов,
  фиксация результата через проверку.
  Source: https://github.com/swe-agent/swe-agent
- mini-swe-agent: минималистичный агентный core вместо большой конфигурации.
  Source: https://github.com/SWE-agent/mini-swe-agent
- OpenHands: local-first/remote-capable agent backends, контроль среды и
  automation boundaries.
  Source: https://github.com/OpenHands/openhands
- smolagents: простые code agents, минимальные абстракции и tool-agnostic
  design.
  Source: https://github.com/huggingface/smolagents

## Habr Patterns

- "Настройка проекта для AI-агентов": держать проектные инструкции в
  явных файлах и делать их переносимыми между агентами.
  Source: https://habr.com/ru/articles/1015252/
- "От хаоса Vibe Coding к системной разработке с AI-агентами": заменить
  интуитивный vibe coding на structured onboarding, workflows и knowledge base.
  Source: https://habr.com/ru/articles/934806/
- "Как создавать AI-агентов на практике": агент должен уметь читать кодовую
  базу, искать проблемы, давать структурированную обратную связь и отслеживать
  собственный progress.
  Source: https://habr.com/ru/articles/984160/
- "Python, RAG и внешние инструменты через MCP": полезен ReAct loop
  "задача -> решение о действии -> инструмент -> наблюдение -> повтор", но
  для coding tasks он должен быть bounded и проверяемым.
  Source: https://habr.com/ru/articles/1025428/

## Python Tooling Sources

- PEP 8: project-specific style has priority; readability and consistency
  matter more than blind rule following.
  Source: https://peps.python.org/pep-0008/
- PEP 20: explicitness, readability and visible errors are core Python design
  signals.
  Source: https://peps.python.org/pep-0020/
- PyPA `pyproject.toml`: central place for build and tool configuration.
  Source: https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
- Python `typing`: annotations are a contract for tools, not runtime
  enforcement by default.
  Source: https://docs.python.org/3/library/typing.html
- pytest good practices: conventional test discovery and `src/` plus `tests/`
  layout are mature defaults for larger projects.
  Source: https://docs.pytest.org/en/stable/explanation/goodpractices.html
- mypy: gradual typing helps find bugs before runtime while staying compatible
  with normal Python execution.
  Source: https://mypy.readthedocs.io/
- Ruff: fast linting and formatting for Python projects.
  Source: https://docs.astral.sh/ruff/

## Design Decisions For AL

- Keep the agent pack file-based and portable.
- Use one machine-readable manifest plus human-readable instructions.
- Provide adapters for Codex, Claude, Cursor and Copilot without making one
  tool the only target.
- Keep roles small and composable.
- Use skills as reusable procedures, not as vague slogans.
- Add a local validator so the repo can prove its own structure.
- Avoid external runtime dependencies until the user explicitly wants a real
  executable LLM client.

## User Archive Integration

User-provided source:

```text
C:\Users\Александр\Downloads\universal-ai-coding-agent-knowledge-base.zip
```

Repo copy and extracted materials:

```text
archive/source_materials/
```

Integrated patterns:

- task lifecycle: intake, classification, context, plan, file scope,
  implementation, verification, report;
- file-scope policy with allowed and forbidden paths;
- independent critic and verifier layers;
- error-prevention layers: static analysis, type checking, tests, security
  scan, diff review and handoff;
- Python defaults: `src` layout for new packages, Ruff, typing, pytest;
- security policy: secrets, unsafe shell commands and workflow injection;
- UX/CI/release review as optional role layers selected by task type;
- evaluation plan for measuring the agent by reduced rework and factual gates.
