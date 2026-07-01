---
name: minimal-refactor
description: Упростить Python-код без изменения поведения, сохраняя tests и public contracts.
---

# Minimal Refactor

## When To Use

Используй только если refactor явно нужен для задачи или снижает реальную
сложность текущего patch.

## Rules

- Не менять behavior без теста или явного согласия.
- Не переименовывать public API без migration note.
- Не смешивать refactor с feature creep.
- Сначала закрепить baseline tests.
- Делать маленькие reversible steps.

## Good Refactor Targets

- duplicated pure logic;
- tangled IO and normalization;
- large function with obvious internal stages;
- unclear error/status handling;
- repeated path/string handling that risks Windows bugs.

## Verification

Run the same tests before and after when feasible.
