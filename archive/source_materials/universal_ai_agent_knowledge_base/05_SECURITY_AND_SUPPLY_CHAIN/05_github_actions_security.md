# GitHub Actions security

## Правила

1. Минимальные permissions.
2. Не запускать опасные workflows на untrusted PR без ограничений.
3. Pin third-party actions по SHA или доверенной версии.
4. Не передавать secrets в pull_request from forks.
5. Разделять build/test/deploy.
6. Проверять workflow injection через issue/PR body/comment.
7. Использовать Dependabot для actions/dependencies.

## Agent rule

Если агент меняет `.github/workflows`, нужен `github-ci-reviewer` и `security-reviewer`.
