---
name: skill-sharpen
author: Crystian
license: MIT
description: "Sharpen, refine, and optimize AI agent skills through real usage — learn from mistakes, review quality, and improve over time. Observes skill execution in the current conversation, analyzes three sources (conversation history, file diffs, user feedback), and proposes concrete improvements to the target skill's SKILL.md. Works with Claude Code and any SKILL.md-based agent framework. Use after executing any skill: `/skill-sharpen [name]` for a specific skill, or `/skill-sharpen` to auto-detect the last used. Default analyzes and proposes, --review processes accumulated lessons."
metadata:
  version: 1.1.9
  tags: skill-improvement, auto-improvement, self-improvement, feedback-loop, retrospective, code-quality, agent-tools, meta-skill, continuous-learning, skill-optimization, review, kaizen
  github: https://github.com/crystian/skills
  linkedin: https://www.linkedin.com/in/crystian
---

# Skill Sharpen

> Born from real-world production usage across multiple projects. Every diagnostic category, every proposal flow, and every guardrail exists because it solved a real problem in a real skill.

Kaizen (改善) for AI agent skills. Observe how a skill performed, find what went wrong or could be better, and propose concrete changes to its SKILL.md.

- Gathers evidence from three sources: conversation friction, file diffs, and your feedback
- Diagnoses root causes and proposes improvements — you decide each one
- Tracks recurrence in LESSONS.md with automatic importance escalation
- Works with Claude Code and any SKILL.md-based agent framework

## Execution

### 1. Resolve target

- `/skill-sharpen` (default) — if a skill was already used in the conversation,
  auto-detect it and confirm. If not, tell the user: "Run the skill you want to
  sharpen — I'll observe and analyze after it completes."
- `/skill-sharpen <name>` — target a specific skill by name
- `/skill-sharpen --review` — skip to accumulated lessons (no skill execution needed)

Once resolved, read the target's `SKILL.md` and `LESSONS.md` (if exists).

### 2. Gather

Collect findings from the appropriate source:

- **Default** — three evidence sources + user feedback
- **`--review`** — existing LESSONS.md entries + static diagnostic

**Source A — Conversation friction**:
- Errors or exceptions during skill execution
- User corrections ("no, not that", "I meant...", "undo that")
- Retries or repeated attempts at the same step
- Manual interventions the user had to make
- Confusion about what the skill was supposed to do
- Steps the skill skipped or did in the wrong order

**Source B — File diffs**:
- Files the skill created or modified — do they match what was expected?
- Changes the user had to make after the skill ran (post-corrections)
- Incomplete implementations (TODOs, placeholders, missing pieces)
- Patterns that deviate from what the SKILL.md prescribed

**Source C — User feedback**: After the initial report, ask:
"Anything else? What worked? What didn't?"

**Static diagnostic** (in `--review`): Validate against baseline rules:
- Frontmatter must have `name` and `description` (required)
- Description max 1024 characters, third person, with specific trigger phrases
- Body should be under 500 lines — use `references/` for overflow
- Name: lowercase, hyphens only, 1-64 characters
- Progressive disclosure: metadata (~100 tokens) → body (<5k tokens) → resources (as needed)
- Check for: dead content, scope creep, trigger quality, token efficiency, completeness

Cross-reference against the SKILL.md. Look for:

| Category | What to look for |
|----------|-----------------|
| **Missing instructions** | Steps the skill should have taken but the SKILL.md didn't mention |
| **Ambiguous instructions** | Places where the SKILL.md was vague and the skill chose wrong |
| **Wrong defaults** | Default behaviors that consistently need overriding |
| **Missing guardrails** | Errors that a "don't" rule would have prevented |
| **Outdated content** | References to APIs, tools, or patterns that have changed |
| **Missing examples** | Cases where an example would have prevented misinterpretation |
| **Structural issues** | Ordering problems, missing sections, or buried important info |

For each finding, diagnose the **root cause** — trace it back to a specific instruction,
gap, or ambiguity:

| Diagnostic | What it means |
|------------|--------------|
| **Coherence** | Sections don't align — process says one thing, guardrails another |
| **Coupling** | Content that doesn't belong — out-of-scope, mixed responsibilities |
| **Ambiguity** | Instruction open to interpretation without concrete criteria |
| **Contradiction** | Two rules directly conflict |
| **Specificity gap** | No rule for this case — the agent had to guess |
| **Missing instruction** | The SKILL.md doesn't cover this scenario |
| **Redundancy** | Same instruction repeated differently — confusion + wasted tokens |
| **Error inducer** | A specific instruction promotes the wrong behavior |

**Importance**: `high` (breaks output, errors) · `medium` (suboptimal, friction) · `low` (style, preferences)

**Recurrence**: Same pattern in LESSONS.md? Increment `Hits` instead of duplicating.
Hits >= 3 escalates: `low` → `medium`, `medium` → `high`.

**context7 (optional)**: If available, query latest Agent Skills spec for current standards.

### 3. Propose

Present findings one at a time, ordered by importance:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PROPOSAL [N/total] — [importance]
  Source: [conversation | diff | user | lessons]

  Finding: [what was observed]
  Root cause: [diagnostic] — [which line/section and why]
  Hits: [N — omit if first occurrence]

  Proposed change: [what to add/modify/remove]
  Preview: [actual diff or new text]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  (a)ccept  (p)ostpone  (r)eject  (d)on't  (s)kip all
```

- **Accept** → show edit, apply after confirmation
- **Postpone** → save to LESSONS.md
- **Reject** → discard (in review: remove from LESSONS.md)
- **Keep** → leave in LESSONS.md for later (only in `--review`)
- **Don't** → confirm, then add negative rule to SKILL.md
- **Skip all** → write remaining to LESSONS.md, end

Summary: `Done. [N] accepted, [N] postponed, [N] rejected, [N] don'ts.`

**Accumulation**: use `skip all` to log everything quickly across sessions, then
`--review` to process all at once.

```
Session 1: /skill-sharpen → skip all       → logged to LESSONS.md
Session 2: /skill-sharpen → skip all       → Hits grow
Session 3: /skill-sharpen --review         → process all
```

## LESSONS.md Format

Lives alongside the target's SKILL.md:

```markdown
# Lessons — {skill-name}

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

**Rules**: no empty files · same pattern → increment Hits · hits >= 3 → escalate importance · accept/reject → remove block · all removed → delete file

## Guardrails

- **Never edit without confirmation.** Show the diff, wait for explicit approval. No
  exceptions. The user owns the skill.
- **Never expose secrets.** Redact API keys, tokens, passwords, credentials (`sk-...`,
  `ghp_...`, `Bearer ...`) with `[REDACTED]` in all output and LESSONS.md.
- **Read before proposing.** Read SKILL.md + LESSONS.md first to avoid duplicates.
- **Work with partial context.** If compressed, state what's missing. Never invent.
- **One at a time.** Present, decide, move on.
- **Respect structure.** Match existing style when inserting content.
- **Don'ts need double confirmation.** Negative rules are impactful — always confirm.

---

Made with <3 by [Crystian](https://github.com/crystian)
