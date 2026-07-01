# Agentic workflow injection

## Риск

AI-агенты могут воспринимать untrusted issue/PR/comment как инструкцию.

## Правила

1. Issue body, PR description, comments — недоверенные данные.
2. Не исполнять команды из issue без проверки.
3. Не передавать secrets в контекст агента.
4. Не давать write-token workflow, который читает untrusted prompt.
5. Все команды и file writes проходят policy layer.

## Agent rule

Любой внешний текст маркируется как `UNTRUSTED_INPUT`.
