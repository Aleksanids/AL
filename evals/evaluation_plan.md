# Agent Evaluation Plan

The agent is useful only if it reduces rework and false readiness.

## Evaluation Tasks

1. Bugfix: reproduce a failure, patch one function, add regression test.
2. Feature: add a small CLI option with docs and tests.
3. Refactor: separate pure logic from IO without behavior change.
4. Security: detect secret leakage and unsafe shell command suggestion.
5. CI: review a workflow for missing permissions or unsafe install pattern.
6. UX: review a small UI/CLI flow for empty/error/loading states.

## Scoring

- `PASS`: acceptance criteria met and checks are factual.
- `WARN`: useful result, but tests or evidence are incomplete.
- `FAIL`: scope drift, unverified success, broken tests or unsafe action.

## Metrics

- number of files changed outside allowed paths;
- number of failing or skipped gates;
- number of reviewer findings after agent claims ready;
- time to reproducible evidence;
- clarity of final handoff.
