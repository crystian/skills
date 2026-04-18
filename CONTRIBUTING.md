# Contributing

Thanks for considering a contribution! This repo is an open collection of AI agent skills. New skills, improvements, bug fixes, and documentation are all welcome.

## Table of Contents

- [Ways to contribute](#ways-to-contribute)
- [Getting started](#getting-started)
- [Adding a new skill](#adding-a-new-skill)
- [SKILL.md standard](#skillmd-standard)
- [Quality checklist](#quality-checklist)
- [Pull request workflow](#pull-request-workflow)
- [Versioning](#versioning)
- [Code of conduct](#code-of-conduct)

## Ways to contribute

- **New skill** — package a repeatable task as a SKILL.md. Start from `skills/_template/`.
- **Improve an existing skill** — tighten instructions, reduce tokens, fix a bug, add examples.
- **Documentation** — clarify `README.md`, add usage notes, fix typos.
- **Tooling** — improve validation (`.github/workflows/validate-skills.yml`) or templates.

Before starting large work, open an issue so we can align on scope.

## Getting started

```bash
git clone https://github.com/crystian/skills.git
cd skills
```

No build step, no dependencies. Each skill is plain markdown.

**Try a skill locally**: install the plugin in Claude Code and invoke `/crystools-skills:<skill-name>`, or copy the skill directory into your own project.

## Adding a new skill

1. Copy the template:
   ```bash
   cp -r skills/_template skills/<your-skill-name>
   ```
2. Pick a name: **lowercase**, **hyphenated**, 1–64 characters, descriptive of what it does.
3. Fill in `SKILL.md` frontmatter and body (see [SKILL.md standard](#skillmd-standard)).
4. Write a user-facing `README.md` for the skill.
5. Put supporting material in a `references/` subdirectory — loaded on demand.
6. Run the validator locally if you can (see [Quality checklist](#quality-checklist)).
7. Open a PR using the "New skill" template.

## SKILL.md standard

Every skill lives at `skills/<name>/SKILL.md` with this shape:

```markdown
---
name: <skill-name>                # lowercase, hyphens only, 1-64 chars
author: <Your Name>
license: MIT
description: >
  Third-person description with concrete trigger phrases. Max 1024 chars.
  Describe what the skill does, when it activates, and the invocation syntax.
metadata:
  version: 0.1.0                  # auto-managed after merge — see Versioning
  tags: tag-one, tag-two, tag-three
  github: https://github.com/crystian/skills
  linkedin: https://www.linkedin.com/in/<your-handle>
---

# <Skill Title>

<Body — under 500 lines / ~5k tokens. Move overflow to references/.>
```

### Rules

- **Frontmatter** fields `name`, `author`, `license`, `description`, `metadata` are all **required**.
- **Body size**: under 500 lines or ~5k tokens. Overflow goes to `references/`.
- **References**: put heavier material in `references/*.md` and load it from the body with explicit instructions (e.g. "Read `references/examples.md` when the user asks for examples.").
- **Independence**: no shared runtime, no global state. A skill must work when copied into another repo.
- **Language**: all code, docs, and SKILL.md content in English.
- **Plugin namespace** once published: `/crystools-skills:<skill-name>`.

### Progressive disclosure

A skill exposes information in three layers, each heavier than the previous:

1. **Frontmatter** (~100 tokens) — what the harness needs to decide whether to activate.
2. **Body** (~5k tokens max) — what the agent needs to do the work.
3. **References** — supporting material loaded on demand.

Respect the budget. Wasted context has a real cost at runtime.

## Quality checklist

Before opening a PR:

- [ ] Directory is `skills/<kebab-case-name>/`.
- [ ] `SKILL.md` has all required frontmatter fields.
- [ ] `name` matches the directory name.
- [ ] `description` is third person and includes explicit trigger phrases.
- [ ] Body is ≤ 500 lines.
- [ ] Heavy material is in `references/` and referenced from the body.
- [ ] `README.md` exists and documents usage from a user's perspective.
- [ ] No absolute local paths; examples use relative paths or placeholders.
- [ ] No secrets, API keys, or personal data.

Run the validator locally before pushing:

```bash
pip install pyyaml    # one-time
python3 scripts/validate-skills.py
```

CI runs the same script on every PR via `.github/workflows/validate-skills.yml`.

## Pull request workflow

1. Fork the repo, branch from `main`.
2. Make your changes — one skill or one coherent change per PR.
3. Keep commit messages descriptive; follow the existing style (short, imperative).
4. Open a PR; the template will prompt for a summary and checklist.
5. CI runs automatically. Fix any failures.
6. A maintainer will review. Expect iteration — this is normal.
7. Once merged, the version bump workflow updates `plugin.json` and all `SKILL.md` versions.

### Scope

- One skill per PR when adding new skills.
- One topic per PR when changing existing material.
- Big refactors: open an issue first.

## Versioning

**Do not bump versions manually.** The `.github/workflows/bump-version.yml` workflow handles it:

- Push to `main` → auto-bumps the patch version.
- Manual trigger (`workflow_dispatch`) → choose minor or major.
- Both `.claude-plugin/plugin.json` and every `SKILL.md` `metadata.version` stay in sync.

Your PR should leave `metadata.version` at whatever it is (or `0.1.0` for new skills); CI rewrites it after merge.

## Code of conduct

This project follows the [Contributor Covenant v2.1](./CODE_OF_CONDUCT.md). By participating, you agree to abide by its terms.

---

Questions? Open a [discussion](https://github.com/crystian/skills/discussions) or file an issue.
