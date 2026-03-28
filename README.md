# Skills

Open collection of AI agent skills — reusable, framework-agnostic SKILL.md packages for Claude Code and beyond.

## Quick Start

### 1. Install

```bash
npx skills add crystian/skills
```

### 2. Use any skill normally

```bash
/create-plan
# ... work as usual ...
```

### 3. Sharpen it

After running a skill, analyze what worked and what didn't:

```bash
/skill-sharpen create-plan          # target a specific skill
/skill-sharpen                      # auto-detect last used skill
```

The skill analyzes the conversation, diffs, and your feedback, then proposes improvements one by one:

```
PROPOSAL 1/3 — high
Source: conversation

Finding: The skill skipped validation step when...

Proposed change: Add validation rule to SKILL.md section...

(a)ccept  (p)ostpone  (r)eject  (d)on't  (s)kip all
```

- **Accept** — applies the change to the target SKILL.md
- **Postpone** — saves to LESSONS.md for later review
- **Reject** — discards
- **Don't** — adds a negative rule to the SKILL.md

### Modes

| Mode | Command | When to use |
|------|---------|-------------|
| **Interactive** | `/skill-sharpen [name]` | Default — proposes one by one, you decide each |
| **Observe-only** | `/skill-sharpen --observe` | In a hurry — dumps all proposals to LESSONS.md |
| **Review** | `/skill-sharpen --review` | Got 5 min — walks through pending LESSONS.md entries |

## Available Skills

| Skill | Description |
|-------|-------------|
| [skill-sharpen](./skills/skill-sharpen/) | Kaizen for AI agent skills — observes execution, analyzes friction points, and proposes concrete improvements to SKILL.md files |

## Install

### Via skills.sh (any SKILL.md-compatible agent)

```bash
npx skills add crystian/skills
```

Install a specific skill:

```bash
npx skills add crystian/skills --skill skill-sharpen
```

### As Claude Code plugin

```bash
claude /plugin install crystian/skills
```

Skills are namespaced: `/crystools-skills:skill-sharpen`

## Contributing

After cloning, run the setup script to configure git hooks:

```bash
./setup.sh
```

This sets `core.hooksPath` to `hooks/`, enabling the version bump prompt on every commit (patch / minor / major / skip).

## License

MIT

---

Made by [Crystian](https://github.com/crystian)
