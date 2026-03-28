# Skills

Open collection of AI agent skills — reusable, framework-agnostic SKILL.md packages for Claude Code and beyond.

## Available Skills

| Skill | Description |
|-------|-------------|
| [skill-sharpen](./skills/skill-sharpen/) | Sharpen, refine, and optimize AI agent skills through real usage — observes execution, analyzes friction points, and proposes concrete improvements to SKILL.md files |

## Install

### As Claude Code plugin

```bash
claude /plugin install crystian/skills
```

Skills are namespaced: `/crystian-skills:skill-sharpen`

### Via skills.sh (any SKILL.md-compatible agent)

Install all skills:

```bash
npx skills add crystian/skills
```

Install a specific skill:

```bash
npx skills add crystian/skills --skill skill-sharpen
```

## License

MIT

---

Made by [Crystian](https://github.com/crystian)
