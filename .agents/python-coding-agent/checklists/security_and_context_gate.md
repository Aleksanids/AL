# Security And Context Gate

## Secrets

- [ ] `.env` не читался.
- [ ] Tokens/cookies/passwords/browser profiles не читались.
- [ ] Authorization headers и private URLs не выводились.
- [ ] Logs не содержат secrets or PII.

## Files

- [ ] Raw user data не изменялись.
- [ ] Generated artifacts не смешаны с source без причины.
- [ ] Recursive delete/move не выполнялись.
- [ ] Windows paths verified with literal paths where needed.

## Network And Tools

- [ ] No live API unless explicitly requested.
- [ ] No package install unless explicitly requested.
- [ ] No browser automation/OCR/Selenium unless explicitly requested.
- [ ] No commit/push/PR unless explicitly requested.

## Agent Context

- [ ] Task-relevant context loaded.
- [ ] No broad skill/catalog scan without need.
- [ ] Assumptions marked.
- [ ] Missing data reported instead of invented.
