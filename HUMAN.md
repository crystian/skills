# HUMAN.md

Notes for humans about this project. Context, vision, decisions, and what doesn't fit in a README.

## Why does this project exist?

AI agents are only as good as the instructions they receive. The problem is those instructions live scattered: in ad-hoc prompts, in CLAUDE.md files mixed with config, in the user's head. There's no standard, portable, versionable format for packaging "how to do X" in a way any agent can execute.

## Design principles

### Progressive disclosure

A skill has three layers of information, each heavier than the last:
1. **Frontmatter** (~100 tokens) — name, description, metadata. What the harness needs to decide whether to activate the skill.
2. **Body** (~5k tokens max) — execution instructions. What the agent needs to do the work.
3. **References** (no limit) — supporting material loaded on demand. Tables, examples, templates.

This isn't arbitrary: agent context windows are finite. A skill that loads 10k tokens of reference tables to solve a case that needs 200 tokens of instructions is wasting context.

### Each skill is independent

No shared runtime, no global state, no orchestrator. A skill is a directory with a SKILL.md and optionally supporting material. You can copy it to another project, move it between agents, fork it without consequences.

### The human decides

Skills propose, they don't impose. skill-sharpen shows diffs and waits for confirmation. It never edits without approval. This isn't a technical limitation — it's a design decision. The user owns their skills.

## Technical decisions

## Mental roadmap (not a commitment)

- More skills: the project's value scales with the quantity and quality of available skills
- Improve skill-sharpen: it's the most complex and most used skill, there's always room to refine it
- Explore skill composition: let a skill invoke or reference others in a structured way
- Community contributions: make it easy for others to publish compatible skills

---

Questions, ideas, or feedback: [github.com/crystian/skills](https://github.com/crystian/skills)
