# Skills

Open collection of AI agent skills — reusable, framework-agnostic SKILL.md packages for Claude Code and beyond.

## Available Skills

| Skill | Description | Docs |
|-------|-------------|------|
| [skill-optimizer](./skills/skill-optimizer/) | Kaizen for AI agent skills — observes execution, analyzes friction points, and proposes concrete improvements to SKILL.md files | [README](./skills/skill-optimizer/README.md) |

## Install

```bash
npx skills add crystian/skills                          # all skills
npx skills add crystian/skills --skill skill-optimizer    # specific skill
claude /plugin install crystian/skills                  # Claude Code plugin
```

Plugin namespace: `/crystools-skills:<skill-name>`

## Update

```bash
npx skills check                     # check for updates
npx skills update                    # update all
npx skills add crystian/skills       # reinstall latest
```

## Contributing

After cloning: `./setup.sh` — configures git hooks for version bump on each commit.

See [HUMAN.md](./HUMAN.md) for humans only.

## License

MIT

---

Made by [Crystian](https://github.com/crystian)
