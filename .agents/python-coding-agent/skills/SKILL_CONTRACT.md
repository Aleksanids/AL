# Task-Oriented Skill Contract

Each AL skill should describe a repeatable task procedure, not a job title or a
large prompt dump.

## Required Shape

- Frontmatter with `name` and `description`.
- One clear purpose or trigger.
- A bounded workflow, checklist, rules, acceptance criteria, or output shape.
- Explicit forbidden actions when the skill touches risky areas.
- Quality evidence expected from the agent.

## Writing Rules

- Keep the skill small enough to fit into task context.
- Link to scripts, references or policies instead of copying large material.
- Prefer commands and checklists over motivational prose.
- Avoid broad ownership language; describe what the skill does for this task.
- Do not include credentials, private data or environment-specific secrets.

## Review Checklist

- Can the agent tell when to use this skill?
- Can the agent tell when to stop?
- Does the skill name a concrete artifact or evidence output?
- Does it avoid expanding scope beyond the user's task?
