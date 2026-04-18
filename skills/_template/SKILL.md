---
name: your-skill-name
author: Your Name
license: MIT
description: >
  Third-person description of what this skill does, when it should activate, and how to invoke it.
  Include concrete trigger phrases the agent can match against. Max 1024 characters.
  Example: "Reviews SQL migrations for destructive operations and suggests safer alternatives.
  Activates when the user asks to review a migration, or runs `/crystools-skills:your-skill-name`."
metadata:
  version: 0.1.0
  tags: tag-one, tag-two, tag-three
  github: https://github.com/crystian/skills
  linkedin: https://www.linkedin.com/in/your-handle
---

# Your Skill Name

> One-line elevator pitch. What problem does this skill solve?

A short paragraph of context: who the skill is for, when it fires, and what the user should expect.

## When to use this skill

- Trigger phrase 1.
- Trigger phrase 2.
- Explicit invocation: `/crystools-skills:your-skill-name`.

## When NOT to use it

- Clearly state what's out of scope. This prevents overlap with other skills.

## Execution

### 1. Resolve inputs

Explain how the skill picks up its inputs (conversation, arguments, files).

### 2. Do the work

Step-by-step instructions. Keep them imperative and concrete.

### 3. Present results

How the skill should present output to the user. Format, verbosity, confirmation prompts.

## Guardrails

- Never edit files without user confirmation.
- Never run destructive operations.
- Add any skill-specific guardrails here.

## References

Heavier material lives in `references/` and is loaded on demand:

- `references/examples.md` — read when the user asks for examples.
- `references/rubric.md` — read when running the quality review.

<!--
Body size budget: ≤ 500 lines / ~5k tokens.
If this file grows past that, move detail into `references/` and link from here.
-->
