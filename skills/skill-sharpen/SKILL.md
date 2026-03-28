---
name: skill-sharpen
author: Crystian
license: MIT
description: "Sharpen, refine, and optimize AI agent skills through real usage — learn from mistakes, review quality, and improve over time. Observes skill execution in the current conversation, analyzes three sources (conversation history, file diffs, user feedback), and proposes concrete improvements to the target skill's SKILL.md. Works with Claude Code and any SKILL.md-based agent framework. Use after executing any skill: `/skill-sharpen [name]` for a specific skill, or `/skill-sharpen` to auto-detect the last used. Three modes: interactive (propose one by one), observe-only (dump to LESSONS.md), review (process pending lessons)."
metadata:
  version: 1.0.4
  tags: skill-improvement, auto-improvement, self-improvement, feedback-loop, retrospective, code-quality, agent-tools, meta-skill, continuous-learning, skill-optimization, review, kaizen
  github: https://github.com/crystian/skills
  linkedin: https://www.linkedin.com/in/crystian
---

# Skill Sharpen

Kaizen (改善) for AI agent skills — observe how a skill performed, find what went wrong or
could be better, and propose concrete changes to its SKILL.md. Feed from conversation
history, file diffs, and explicit user feedback.

## Process

### 1. Resolve Target Skill

Determine which skill to sharpen:

- **Explicit** (`/skill-sharpen <name>`): Search for `<name>` across skill directories —
  local project skills, installed skills, and plugin skills. Match by directory name.
- **Auto-detect** (`/skill-sharpen` with no args): Scan conversation history for the most
  recently loaded skill (look for SKILL.md content or `/skill-name` invocations). Ask the
  user to confirm: "Detected `<name>` — is that the one?"

If the skill is not found, list the paths searched and ask the user for a correction or
an explicit path.

Once resolved, read the target skill's `SKILL.md` and `LESSONS.md` (if it exists). Keep
both in context — they inform what to propose and what to skip.

### 2. Determine Execution Mode

Ask the user or detect from arguments:

| Mode | Trigger | Behavior |
|------|---------|----------|
| **Interactive** | Default (no flag) | Analyze sources → propose one by one → user decides each |
| **Observe-only** | `--observe` or user says "just log" | Analyze sources → write all to LESSONS.md → done |
| **Review** | `--review` or user says "review lessons" | Skip source analysis → walk through existing LESSONS.md entries |

If mode is **Review**, jump directly to [Step 6: Review Mode](#6-review-mode).

### 3. Gather Evidence

Collect information from three sources. Work with whatever is available — not all sources
will have signal every time.

**Source A — Conversation history**

Scan the conversation for friction signals:
- Errors or exceptions during skill execution
- User corrections ("no, not that", "I meant...", "undo that")
- Retries or repeated attempts at the same step
- Manual interventions the user had to make
- Confusion about what the skill was supposed to do
- Steps the skill skipped or did in the wrong order

**Source B — File diffs**

Check `git diff` or recently modified files for:
- Files the skill created or modified — do they match what was expected?
- Changes the user had to make after the skill ran (post-corrections)
- Incomplete implementations (TODOs, placeholders, missing pieces)
- Patterns that deviate from what the SKILL.md prescribed

**Source C — User feedback**

Ask the user directly:
> "What worked well? What didn't? Anything specific you want the skill to do differently?"

This is especially valuable when conversation context is compressed or when the issues
are subtle (preferences, style, approach). Keep it open-ended — one question, then follow
up if needed.

### 4. Analyze and Generate Proposals

Cross-reference the evidence against the target skill's SKILL.md to identify:

| Category | What to look for |
|----------|-----------------|
| **Missing instructions** | Steps the skill should have taken but didn't because the SKILL.md didn't mention them |
| **Ambiguous instructions** | Places where the SKILL.md was vague and the skill made a wrong choice |
| **Wrong defaults** | Default behaviors that consistently need overriding |
| **Missing guardrails** | Errors that a "don't" rule would have prevented |
| **Outdated content** | References to APIs, tools, or patterns that have changed |
| **Missing examples** | Cases where an example would have prevented misinterpretation |
| **Structural issues** | Ordering problems, missing sections, or buried important info |

For each finding, formulate a **proposal**: a concrete, actionable change to the SKILL.md.

**Assign importance based on impact:**

| Importance | Criteria |
|------------|----------|
| **high** | Breaks output, causes errors, or requires user intervention every time |
| **medium** | Suboptimal results, friction exists but workaround is possible |
| **low** | Style, preferences, minor improvements |

**Recurrence escalation:** Before generating a new proposal, check LESSONS.md for an
existing entry describing the same pattern. If found, increment its `Hits` column instead
of creating a duplicate. When hits reach 3+, escalate importance: `low` → `medium`,
`medium` → `high`. `high` stays `high`.

### 5. Present Proposals (Interactive Mode)

Present proposals **one at a time**, ordered by importance (high → medium → low).

For each proposal, show:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PROPOSAL [N/total] — [importance]
  Source: [conversation | diff | user]

  Finding: [what was observed]
  Hits: [N — omit if first occurrence]

  Proposed change:
  [concrete description of what to add/modify/remove in SKILL.md]

  Preview:
  [show the actual diff or new text that would be added]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  (a)ccept  (p)ostpone  (r)eject  (d)on't  (s)kip all
```

Handle the user's decision:

- **Accept**: Show the exact edit to be made. Apply it only after the user confirms.
  Edit the target SKILL.md directly.
- **Postpone**: Append to the target skill's LESSONS.md (create if it doesn't exist).
- **Reject**: Discard and move to the next proposal.
- **Don't**: The user is saying "this is wrong, the skill should NEVER do this". Confirm
  the negative rule with the user, then add it to the SKILL.md as a "Do NOT..." instruction.
- **Skip all**: Write remaining proposals to LESSONS.md and end.

After all proposals are processed, show a summary:

```
Done. [N] accepted, [N] postponed, [N] rejected, [N] don'ts added.
```

### 6. Review Mode

Walk through existing LESSONS.md entries one by one. For each entry, present it in the
same format as Step 5 (but source and finding come from the LESSONS.md row).

The user can:
- **Accept** → apply to SKILL.md, remove from LESSONS.md
- **Reject** → remove from LESSONS.md (optionally convert to "don't")
- **Keep** → leave in LESSONS.md for later

After processing all entries, show the summary. If all entries were processed (none kept),
delete the LESSONS.md file.

## LESSONS.md Format

The file lives alongside the target skill's SKILL.md. Format:

```markdown
# Lessons — {skill-name}

| Date | Source | Proposal | Importance | Hits |
|------|--------|----------|------------|------|
| 2026-03-28 | conversation | Description of finding and proposed change | high | 1 |
| 2026-03-27 | diff | Another pending proposal | medium | 3 |
```

**Columns:**
- **Date**: when the proposal was first generated (YYYY-MM-DD)
- **Source**: `conversation`, `diff`, or `user`
- **Proposal**: concise description of finding + proposed change
- **Importance**: `high`, `medium`, `low` (see criteria in Step 4)
- **Hits**: how many times this pattern has been observed (starts at 1)

**Rules:**
- Never create an empty LESSONS.md — only create it when there's at least one entry
- When appending to an existing LESSONS.md, add new rows at the end of the table
- When the same pattern is detected again, increment `Hits` instead of adding a duplicate.
  Update `Date` to the latest occurrence
- When hits reach 3+, escalate importance: `low` → `medium`, `medium` → `high`
- When accepting or rejecting an entry, remove its row from the table
- When all rows are removed, delete the file

## Guardrails

- **Never edit without confirmation.** Always show the proposed diff and wait for explicit
  user approval before modifying any SKILL.md. This is non-negotiable.
- **Read before proposing.** Always read the target SKILL.md and LESSONS.md before
  generating proposals. Avoids duplicates, contradictions, and already-addressed issues.
- **Work with partial context.** If the conversation was long and context is compressed,
  work with what's available. State what you can see and what might be missing. Never
  invent evidence or assume what happened.
- **One proposal at a time.** Don't dump all proposals at once. Present, decide, move on.
- **Respect the SKILL.md structure.** When inserting new content, match the existing style,
  indentation, and organizational pattern of the target SKILL.md.
- **Don'ts need double confirmation.** Adding a negative rule to a SKILL.md is impactful.
  Always confirm: "Add this as a 'don't' rule to the SKILL.md?"

---

Made by [Crystian](https://github.com/crystian)
