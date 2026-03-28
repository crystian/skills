# Skills

Open collection of AI agent skills — reusable, framework-agnostic SKILL.md packages for Claude Code and beyond.

## Available Skills

| Skill | Description |
|-------|-------------|
| [skill-sharpen](./skills/skill-sharpen/) | Kaizen for AI agent skills — observes execution, analyzes friction points, and proposes concrete improvements to SKILL.md files |

## Install

### Via skills.sh (any SKILL.md-compatible agent)

Install all skills:

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

Skills are namespaced: `/crystools-skills:<skill-name>`

## Update

```bash
npx skills check                     # check for available updates
npx skills update                    # update all installed skills
npx skills add crystian/skills       # reinstall from repo to latest
```

---

## skill-sharpen

> Born from real-world production usage across multiple projects. Every diagnostic category, every proposal flow, and every guardrail exists because it solved a real problem in a real skill.

Kaizen (改善) for AI agent skills — observe how a skill performed, find what went wrong or could be better, and propose concrete changes to its SKILL.md.

### Quick Start

**1. Use any skill normally**

```
/create-plan
# ... work as usual ...
```

**2. Sharpen it**

```
/skill-sharpen create-plan          # analyze a specific skill
/skill-sharpen                      # auto-detect last used skill
```

If no skill was used yet, it waits for one to complete and then analyzes automatically.

**3. Decide on each proposal**

```
PROPOSAL 1/3 — high
Source: conversation

Finding: The skill skipped validation step when...
Root cause: specificity gap — no rule for this case

Proposed change: Add validation rule to SKILL.md section...

(a)ccept  (p)ostpone  (r)eject  (d)on't  (s)kip all
```

- **Accept** — applies the change to the target SKILL.md
- **Postpone** — saves to LESSONS.md for later review
- **Reject** — discards
- **Don't** — adds a negative rule to the SKILL.md

### Modes

- **Default** (`/skill-sharpen [name]`) — analyze → report → ask for feedback → propose one by one. Use `skip all` to log everything to LESSONS.md at once.
- **Review** (`/skill-sharpen --review`) — process accumulated lessons + static diagnostic

### Accumulation Workflow

Log findings across sessions, review when ready:

```
Session 1: /skill-sharpen → report → skip all     → findings logged to LESSONS.md
Session 2: /skill-sharpen → report → skip all     → more findings, Hits grow
Session 3: /skill-sharpen --review                 → process all at once
```

Lessons are stored in a `LESSONS.md` file next to the target skill:

```markdown
### 1 — high | Hits: 1
- **Date**: 2026-03-28
- **Source**: conversation
- **Diagnostic**: ambiguity — line 45 says "if needed" without criteria
- **Proposal**: Replace with explicit condition: "when scope is api or both"

### 2 — medium | Hits: 3
- **Date**: 2026-03-27
- **Source**: diff
- **Diagnostic**: missing instruction
- **Proposal**: Add validation step before Phase 3
```

### Diagnostic Categories

Each proposal traces the problem back to a root cause:

| Diagnostic | What it means |
|------------|--------------|
| **Coherence** | Sections don't align with each other |
| **Coupling** | Content that doesn't belong — out-of-scope, mixed responsibilities |
| **Ambiguity** | Instruction open to multiple interpretations |
| **Contradiction** | Two rules directly conflict |
| **Specificity gap** | No concrete rule — the agent had to guess |
| **Redundancy** | Same instruction repeated or worded differently across sections |
| **Missing instruction** | The SKILL.md doesn't cover this scenario |
| **Error inducer** | A specific instruction promotes the wrong behavior |

Full documentation: [skills/skill-sharpen/SKILL.md](./skills/skill-sharpen/SKILL.md)

---

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
