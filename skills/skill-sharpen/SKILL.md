---
name: skill-sharpen
author: Crystian
license: MIT
description: "Sharpen, refine, and optimize AI agent skills through real usage — learn from mistakes, review quality, and improve over time. Observes skill execution in the current conversation, analyzes three sources (conversation history, file diffs, user feedback), and proposes concrete improvements to the target skill's SKILL.md. Works with Claude Code and any SKILL.md-based agent framework. Use after executing any skill: `/skill-sharpen [name]` for a specific skill, or `/skill-sharpen` to auto-detect the last used. Three modes: interactive (propose one by one), observe-only (dump to LESSONS.md), review (process pending lessons)."
metadata:
  version: 1.1.5
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
| **Interactive** | Default (no flag) | Analyze sources → diagnose root cause → propose one by one → user decides each |
| **Observe-only** | `--observe` or "just log" | Analyze sources → diagnose → write all to LESSONS.md → done |
| **Watch** | `--watch <skill>` or "run X and observe" | Execute the target skill first, then analyze the results (interactive or with `--observe`) |
| **Review** | `--review` or "review lessons" | Skip source analysis → walk through existing LESSONS.md entries |
| **Audit** | `--audit` or "audit the skill" | Skip sources → full static diagnostic of the SKILL.md → propose fixes |

If mode is **Review**, jump directly to [Step 6: Review Mode](#6-review-mode).

**Watch mode**: Also detects natural language: "ejecutá /create-plan y después observemos"
triggers watch + interactive. The skill being watched becomes the target for analysis.

**Accumulation workflow**: Use `--observe` (or `--watch --observe`) repeatedly across
sessions to accumulate lessons in LESSONS.md. Each run adds new findings or increments
Hits on existing ones. When ready to process, run `--review` to walk through everything
and decide what to apply.

```
Session 1: /skill-sharpen --watch create-plan --observe  → runs skill, logs findings
Session 2: /skill-sharpen --observe                      → logs more findings, Hits grow
Session 3: /skill-sharpen --review                       → process all accumulated lessons
```

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

For each finding, **diagnose the root cause** in the SKILL.md. Don't just describe what
went wrong — explain *why* it happened by tracing it back to a specific instruction,
gap, or ambiguity. Use these diagnostic categories:

| Diagnostic | What it means |
|------------|--------------|
| **Coherence** | Sections don't align — the process says one thing, the guardrails another |
| **Coupling** | Content that doesn't belong in this skill — leaks from another domain, out-of-scope instructions, or mixed responsibilities that caused the agent to act outside its purpose. If it's not cohesive with the skill's core goal, it shouldn't be there |
| **Ambiguity** | Instruction open to interpretation — "if needed", "as appropriate" without criteria |
| **Contradiction** | Two rules directly conflict |
| **Specificity gap** | No concrete rule exists for this case — the agent had to guess |
| **Missing instruction** | The SKILL.md simply doesn't cover this scenario |
| **Redundancy** | Same instruction repeated in different sections or worded differently — causes confusion about which one to follow, wastes context window |
| **Error inducer** | A specific instruction actively promotes the wrong behavior |

Each proposal must include a short **root cause** line. Format:

```
Finding: [what happened]
Root cause: [diagnostic] — [which line/section caused it and why]
Proposed change: [concrete fix]
```

**`--audit` mode:** When invoked with `--audit`, run a full static diagnostic of the
SKILL.md without requiring execution evidence. Validate against these baseline rules
(from Agent Skills spec + Anthropic best practices):
- Frontmatter must have `name` and `description` (required)
- Description max 1024 characters, third person, with specific trigger phrases
- Body should be under 500 lines — use `references/` for overflow
- Name: lowercase, hyphens only, 1-64 characters
- Progressive disclosure: metadata (~100 tokens) → body (<5k tokens) → resources (as needed)
- Check for: dead content, scope creep, trigger quality, token efficiency, completeness

**Enrich with context7 (optional):** If the `context7` MCP server is available, query
the latest Agent Skills specification and Anthropic skill authoring best practices to
ensure rules reflect the most current standards. If not available, use the baseline
rules above — they cover the stable core.

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
  Root cause: [diagnostic] — [which line/section and why]
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

### 1 — high | Hits: 1
- **Date**: 2026-03-28
- **Source**: conversation
- **Diagnostic**: ambiguity — line 45 says "if needed" without criteria
- **Proposal**: Replace "if needed" with explicit condition: "when scope is api or both"

### 2 — medium | Hits: 3
- **Date**: 2026-03-27
- **Source**: diff
- **Diagnostic**: missing instruction
- **Proposal**: Add validation step before Phase 3 for skill-scoped plans
```

**Fields:**
- **Heading**: entry number + importance + hits count
- **Date**: when first generated (YYYY-MM-DD), updated to latest occurrence on hit
- **Source**: `conversation`, `diff`, or `user`
- **Diagnostic**: root cause category + short explanation
- **Proposal**: concise description of finding + proposed change

**Rules:**
- Never create an empty LESSONS.md — only create it when there's at least one entry
- When the same pattern is detected again, increment `Hits` in the heading instead of
  adding a duplicate. Update `Date` to the latest occurrence
- When hits reach 3+, escalate importance: `low` → `medium`, `medium` → `high`
- When accepting or rejecting an entry, remove the entire block
- When all entries are removed, delete the file

## Guardrails

- **Never edit without confirmation.** Always show the proposed diff and wait for explicit
  user approval before modifying any SKILL.md. This is non-negotiable — no exceptions,
  not even in observe-only mode (which writes to LESSONS.md, never to SKILL.md).
  Always ask the user what they want to do. The user owns the skill.
- **Never expose secrets.** When analyzing conversation history, diffs, or files, redact
  any sensitive content before displaying it in proposals, previews, or LESSONS.md entries.
  This includes: API keys, tokens, passwords, connection strings, private URLs, and any
  value that looks like a credential (e.g., `sk-...`, `ghp_...`, `Bearer ...`). Replace
  with `[REDACTED]` in all output. Never write secrets to LESSONS.md.
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
