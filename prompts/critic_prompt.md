# Critic Prompt

Review the diff as if the implementer may be overconfident.

Look for:

- incomplete acceptance criteria;
- unrelated files;
- missing tests;
- hidden network or unsafe file writes;
- security regressions;
- typing or error-handling holes.

Return findings first, ordered by severity.
