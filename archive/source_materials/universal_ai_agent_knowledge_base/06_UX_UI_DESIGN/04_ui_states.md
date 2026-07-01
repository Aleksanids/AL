# UI states

Любой экран должен иметь состояния:

1. initial;
2. loading;
3. loaded;
4. empty;
5. error;
6. partial data;
7. disabled;
8. success;
9. warning;
10. offline/timeout, если есть сеть.

## Agent rule

Если агент добавляет компонент без этих состояний, UX review не проходит.
