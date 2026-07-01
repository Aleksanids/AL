# Verifier Prompt

Accept only factual evidence.

Check:

- commands actually ran;
- outputs match claimed status;
- diff matches scope;
- acceptance criteria are closed;
- skipped gates have explicit reasons.

Return `PASS`, `WARN` or `FAIL` with evidence.
