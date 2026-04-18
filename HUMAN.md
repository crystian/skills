# HUMAN.md

Notes for humans about this project. Context, vision, decisions — the things that don't fit in a `README.md` and that agents don't need to execute their work.

> If you're an AI agent reading this: you *may* read it when useful for context, but the source of truth for your behavior is `CLAUDE.md`, `CONTRIBUTING.md`, and each skill's own `SKILL.md`.

## Why this project exists

AI agents are only as good as the instructions they receive. The problem is that those instructions live scattered — in ad-hoc prompts, in `CLAUDE.md` files mixed with config, in the user's head, in Slack threads.

There's no standard, portable, versionable format for packaging "how to do X" in a way any agent can execute. This project is an attempt at that: a public, MIT-licensed collection of skills as plain markdown files with a strict structure.

## Design principles

### Progressive disclosure

A skill has three layers of information, each heavier than the last:

1. **Frontmatter** (~100 tokens) — `name`, `description`, `metadata`. What the harness needs to decide whether to activate.
2. **Body** (~5k tokens max) — execution instructions. What the agent needs to do the work.
3. **References** (no hard limit) — supporting material loaded on demand. Tables, examples, templates.

This isn't arbitrary: agent context windows are finite and have a real token cost. A skill that loads 10k tokens of reference tables to solve a case that needs 200 tokens of instructions is wasting context, money, and latency.

### Each skill is independent

No shared runtime, no global state, no orchestrator. A skill is a directory with a `SKILL.md` and optionally supporting material. You can copy it to another project, move it between agents, fork it without consequences.

This also means there's no "core" to break. Skills evolve independently.

### The human decides

Skills propose, they don't impose. `skill-optimizer` shows diffs and waits for confirmation. It never edits without approval. This isn't a technical limitation — it's a design decision. The user owns their skills.

### Public and portable by default

Everything in this repo is MIT-licensed. Nothing depends on a private runtime, a paid service, or a specific vendor lock. If Claude Code disappears tomorrow, the skills still run wherever SKILL.md is understood.

## Technical decisions

- **Plain markdown, no build step.** Skills are authored, reviewed, and shipped as `.md` files. No compilation, no bundler, no package manifest per skill.
- **Versioning is centralized.** All skill versions are bumped in lockstep with the plugin version by GitHub Actions. This trades per-skill granularity for consistency.
- **CI enforces the standard.** `validate-skills.yml` rejects PRs that break the frontmatter contract, name conventions, or size budget. The structure is the contract.
- **`_template/` is the onboarding surface.** New contributors start from a scaffold, not from a blank file.

## Mental roadmap (not a commitment)

- **More skills.** The project's value scales with the quantity and quality of available skills.
- **Improve `skill-optimizer`.** It's the most complex and most used skill; there's always room to refine it.
- **Explore skill composition.** Let a skill invoke or reference others in a structured way, without breaking independence.
- **Community contributions.** Make it as easy as possible for others to publish compatible skills — templates, docs, CI, issue forms.
- **Cross-agent compatibility.** SKILL.md is designed to be agent-agnostic. Validate that more agents than Claude Code can execute these as-is.

## What this project is NOT

- **Not a framework.** No orchestration, no DSL, no runtime library.
- **Not opinionated about what agents do.** Skills are instructions; the agent decides how to execute them.
- **Not a drop-in replacement for careful prompting.** A bad SKILL.md is worse than no SKILL.md.

## Credits and contact

Questions, ideas, or feedback: [github.com/crystian/skills](https://github.com/crystian/skills) — open an issue or a discussion.

Maintained by [Crystian](https://github.com/crystian).
