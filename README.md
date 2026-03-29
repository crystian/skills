# Skills

Open collection of AI agent skills — reusable, framework-agnostic SKILL.md packages for Claude Code and beyond.

## Available Skills

| Skill | Description |
|-------|-------------|
| [skill-sharpen](./skills/skill-sharpen/) | Kaizen for AI agent skills — observes execution, analyzes friction points, and proposes concrete improvements to SKILL.md files |

## Install

```bash
npx skills add crystian/skills                          # all skills (skills.sh)
npx skills add crystian/skills --skill skill-sharpen    # specific skill
claude /plugin install crystian/skills                  # Claude Code plugin
```

Plugin namespace: `/crystools-skills:<skill-name>`

## Update

```bash
npx skills check                     # check for updates
npx skills update                    # update all
npx skills add crystian/skills       # reinstall latest
```

---

## skill-sharpen

> Born from real-world production usage across multiple projects. Every diagnostic category, every proposal flow, and every guardrail exists because it solved a real problem in a real skill.

Kaizen (改善) for AI agent skills — observe how a skill performed, find what went wrong, and propose concrete changes to its SKILL.md.

### Usage
   
#### As command-line
```
/skill-sharpen                      # auto-detect last used skill
/skill-sharpen create-plan          # analyze a specific skill
/skill-sharpen --review             # process accumulated lessons
```
#### or just ask naturally:
```
"sharpen the last skill I used"
"what could we improve in create-plan?"
"review pending lessons"
```

Each finding includes a root cause diagnostic and a proposed fix:

```
PROPOSAL 1/3 — high
Source: conversation

Finding: The skill skipped validation step when...
Root cause: specificity gap — no rule for this case
Proposed change: Add validation rule to SKILL.md section...

(a)ccept  (p)ostpone  (r)eject  (d)on't  (s)kip all
```

### Diagnostics

| Diagnostic | What it means |
|------------|--------------|
| Coherence | Sections don't align with each other |
| Coupling | Content that doesn't belong — out-of-scope, mixed responsibilities |
| Ambiguity | Instruction open to multiple interpretations |
| Contradiction | Two rules directly conflict |
| Specificity gap | No concrete rule — the agent had to guess |
| Redundancy | Same instruction repeated or worded differently |
| Missing instruction | The SKILL.md doesn't cover this scenario |
| Error inducer | A specific instruction promotes the wrong behavior |
| Inference trap | Text invites a wrong conclusion the agent wasn't meant to draw |

Full documentation: [skills/skill-sharpen/SKILL.md](./skills/skill-sharpen/SKILL.md)

---

## Contributing

After cloning: `./setup.sh` — configures git hooks for version bump on each commit.

## License

MIT

---

Made by [Crystian](https://github.com/crystian)
