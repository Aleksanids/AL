---
name: test-design
description: Спроектировать focused tests для behavior, edge cases, regressions и safety boundaries.
---

# Test Design

## Principles

- Tests prove behavior, not private implementation.
- One test should fail for one main reason.
- Fixtures must not hide the behavior under test.
- Regression bug requires regression test.
- Filesystem tests use temp dirs.
- Network tests use mocked transport.

## Shape

Arrange, act, assert, cleanup.
