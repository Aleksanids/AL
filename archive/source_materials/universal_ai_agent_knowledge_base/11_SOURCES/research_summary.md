# Research summary

## Agent systems

Официальные источники OpenAI, Codex, Cursor и GitHub показывают общий тренд: сильные агенты строятся не только через prompt, а через инструкции, tools, skills, subagents, handoffs, guardrails, custom agent profiles и проверяемые workflows.

## Python quality

Современная Python-база должна использовать `pyproject.toml`, `src` layout, `ruff`, type checking, `pytest`, coverage, security scanning и CI. Это снижает ошибки импорта, форматирования, типов, регрессий и неявных зависимостей.

## Security

OWASP, NIST SSDF, SLSA, OpenSSF и GitHub Actions security сходятся в одном: безопасность должна быть частью SDLC, а не финальной ручной проверкой. Для AI-агента особенно важны secrets policy, command policy и защита от untrusted prompt/workflow injection.

## UX

UX-проверка должна быть встроена в задачи, которые меняют интерфейс. Минимум: Nielsen heuristics, WCAG, состояния интерфейса, ошибки, доступность, визуальная иерархия и микротексты.

## Вывод

Универсальный coding-agent должен быть контролёром процесса. Он может использовать Codex/Cursor/Aider/GitHub Copilot как исполнителей, но обязан сам проверять scope, diff, tests, security и UX.
