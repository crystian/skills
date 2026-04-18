# crystools-skills

> Open collection of AI agent skills — reusable, framework-agnostic SKILL.md packages for Claude Code and compatible agents.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Plugin version](https://img.shields.io/github/v/tag/crystian/skills?label=version)](./.claude-plugin/plugin.json)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)

## Table of Contents

- [What's a skill?](#whats-a-skill)
- [Available skills](#available-skills)
- [Install](#install)
- [Update](#update)
- [Contributing](#contributing)
- [Project layout](#project-layout)
- [Documents](#documents)
- [License](#license)

## What's a skill?

A **skill** is a self-contained directory with a `SKILL.md` file. It packages "how to do X" in a way any SKILL.md-aware agent can execute, with no shared runtime and no global state. Copy it, fork it, move it between projects — it just works.

Skills follow a three-layer progressive disclosure model: lightweight frontmatter (for activation), a bounded body (for execution), and optional references (loaded on demand). See [HUMAN.md](./HUMAN.md) for the design philosophy.

## Available skills

| Skill | Description | Docs |
|-------|-------------|------|
| [skill-optimizer](./skills/skill-optimizer/) | Kaizen for AI agent skills — observes execution, diagnoses friction, proposes concrete SKILL.md improvements | [README](./skills/skill-optimizer/README.md) |

More coming. Want to add one? Jump to [Contributing](#contributing).

## Install

```bash
# All skills via Claude Code plugin
claude /plugin install crystian/skills

# All skills via npx
npx skills add crystian/skills

# A single skill
npx skills add crystian/skills --skill skill-optimizer
```

Once installed, invoke with the plugin namespace: `/crystools-skills:<skill-name>`.

## Update

```bash
npx skills check                     # check for updates
npx skills update                    # update all
npx skills add crystian/skills       # reinstall latest
```

## Contributing

Contributions are welcome — new skills, improvements, bug fixes, docs. Start here:

1. Read [CONTRIBUTING.md](./CONTRIBUTING.md).
2. For a new skill, open a [New skill proposal](https://github.com/crystian/skills/issues/new?template=new_skill.yml) first to align on scope.
3. Copy `skills/_template/` as your starting point.
4. Open a PR; CI validates SKILL.md structure automatically.

Quick start for a new skill:

```bash
cp -r skills/_template skills/my-new-skill
# edit skills/my-new-skill/SKILL.md and README.md
```

## Project layout

```
.claude-plugin/
  plugin.json             # plugin manifest
.github/
  ISSUE_TEMPLATE/         # issue forms
  workflows/              # CI (validate + auto-bump version)
  pull_request_template.md
scripts/
  validate-skills.py      # SKILL.md linter (used by CI and locally)
skills/
  _template/              # starting point for new skills
  skill-optimizer/
    SKILL.md              # skill definition (frontmatter + body)
    README.md             # user-facing docs
    references/           # optional, loaded on demand
CONTRIBUTING.md           # how to contribute
CODE_OF_CONDUCT.md        # community standards
SECURITY.md               # how to report vulnerabilities
CHANGELOG.md              # release notes
HUMAN.md                  # design notes for humans (not for agents)
CLAUDE.md                 # instructions for Claude / agents
```

## Documents

- [CONTRIBUTING.md](./CONTRIBUTING.md) — how to contribute, skill standard, PR workflow.
- [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) — community standards (Contributor Covenant v2.1).
- [SECURITY.md](./SECURITY.md) — vulnerability reporting policy.
- [CHANGELOG.md](./CHANGELOG.md) — release history.
- [HUMAN.md](./HUMAN.md) — design principles and project vision (for humans).
- [LICENSE](./LICENSE) — MIT.

## License

MIT. See [LICENSE](./LICENSE).

---

Made by [Crystian](https://github.com/crystian) · [LinkedIn](https://www.linkedin.com/in/crystian)
