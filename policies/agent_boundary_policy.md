# Agent Boundary Policy

`AL` uses `.agentignore` as the compact source of truth for repository
read/write boundaries. The goal is to keep always-on instructions short while
still making boundaries machine-readable for `auto-connect` and validator gates.

## Sections

- `deny_read_write`: never read, write, summarize or pass these paths into
  prompts.
- `read_only`: reading is allowed when relevant; writing requires explicit
  task scope and user-visible rationale.
- `generated`: skip by default; regenerate through commands instead of manual
  edits.

## Runtime Rules

- `auto-connect` loads `.agentignore` from the confirmed agent root.
- `deny_read_write` and `generated` paths are added to task `forbidden_paths`.
- `read_only` paths are shown in the adapter prompt as write boundaries.
- Explicit task scope may narrow access further but must not remove hard
  boundaries.

## Authoring Rules

- Keep `.agentignore` compact and stable.
- Prefer directories over long file lists.
- Add a short policy note here when a new section or interpretation is needed.
- Do not put credentials or private values into boundary examples.
