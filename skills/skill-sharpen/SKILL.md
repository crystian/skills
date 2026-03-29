---
name: skill-sharpen
author: Crystian
license: MIT
description: "Sharpens, refines, and optimizes AI agent skills through real usage — learns from mistakes, reviews quality, and improves over time. Observes skill execution in the current conversation, analyzes up to four sources (conversation friction, file diffs, user feedback, static diagnostic), and proposes concrete improvements to the target skill's SKILL.md. Works with Claude Code and any SKILL.md-based agent framework. Use after executing any skill: `/skill-sharpen [name]` or `/skill-sharpen` to auto-detect. `--review` processes accumulated lessons."
metadata:
  version: 1.2.0
  tags: skill-improvement, feedback-loop, retrospective, code-quality, agent-tools, meta-skill, continuous-learning, review, kaizen, efficiency, optimization, improvements
  github: https://github.com/crystian/skills
  linkedin: https://www.linkedin.com/in/crystian
---

# Skill Sharpen

> Born from real-world production usage across multiple projects. Every diagnostic category, every proposal flow, and every guardrail exists because it solved a real problem in a real skill.

Kaizen (改善) for AI agent skills. Observe how a skill performed, find what went wrong or could be better, and propose concrete changes to its SKILL.md.

Diagnoses root causes and proposes improvements — you decide each one. Tracks recurrence in LESSONS.md with automatic importance escalation.

## Execution

### 1. Resolve target

- `/skill-sharpen` (default) — detect the last skill used in the conversation by
  looking for `<command-name>` tags or Skill tool calls. Confirm the target with
  the user. If no skill was used, tell the user: "Run the skill you want to
  sharpen — I'll observe and analyze after it completes."
- `/skill-sharpen <name>` — target a specific skill by name
- `/skill-sharpen --review` — skip to accumulated lessons (no skill execution needed).
  If no target can be resolved (no name, no prior skill in conversation), ask the
  user: "Which skill do you want to review? Provide the name or path."
  If no `LESSONS.md` exists, inform the user: "No accumulated lessons found. Run
  `/skill-sharpen` after a skill execution to start collecting." Then ask the
  user: "Want me to run a static diagnostic on the SKILL.md instead?"
- `/skill-sharpen <name> --review` — review accumulated lessons for the named skill.
  Combines target resolution with `--review` mode. If no `LESSONS.md` exists,
  apply the same fallback: inform the user and offer a static diagnostic.

Argument order does not matter — `--review <name>` is equivalent to `<name> --review`.

Once resolved, read the target's `SKILL.md` and `LESSONS.md` (if exists).

**Skill resolution**: Search for `<name>/SKILL.md` in these paths (first match wins):
1. `.claude/skills/`
2. `.agents/skills/`
3. The parent directory of the skill that invoked sharpen (peer skills are
   expected as sibling folders — e.g., `../other-skill/SKILL.md`)
4. Current working directory

If not found in any path, tell the user: "Could not find `<name>/SKILL.md`.
Check the skill name or provide the full path." Do not guess or search outside
these paths.

**Path input**: If `<name>` contains `/` (e.g., `./my-skill`, `../other-skill`,
or an absolute path), treat it as a direct path — read `<name>/SKILL.md` (or
`<name>` if it already ends in `SKILL.md`). Skip the 4-path search. If the file
does not exist, report: "File not found at `<path>`. Check the path and try again."

**Extra arguments**: Any arguments beyond `<name>` or `--review`
are ignored. Inform the user: "Extra arguments ignored: [args]."

**Self-sharpening**: When the target is `skill-sharpen` itself, always use static
diagnostic as primary source (full self-observation is unreliable).
The agent may observe obvious friction from the current session but must not create
findings from it — self-observation is unreliable as evidence. Skip conversation
friction and file diffs — run
static diagnostic, then user feedback, then Propose.

**Fallback without prior run**: If the target skill was not executed in this
conversation (e.g., `/skill-sharpen <name>` without prior run), fall back to
static diagnostic + user feedback. State this to the user before proceeding.

### 2. Gather

Collect findings from the appropriate source:

**Sources**: conversation friction, file diffs, user feedback, static diagnostic

- **Default** — conversation, diffs, user feedback
- **`<name>` without prior run** — static diagnostic, user feedback
- **`--review`** — existing LESSONS.md entries + static diagnostic + user feedback (deferred to Propose)

**Conversation friction**:
- Errors or exceptions during skill execution
- User corrections ("no, not that", "I meant...", "undo that")
- Retries or repeated attempts at the same step
- Manual interventions the user had to make
- Confusion about what the skill was supposed to do
- Steps the skill skipped or did in the wrong order

**File diffs**:
Use `git diff` (or `git diff --cached`) to inspect changes made during the
skill's execution. If not in a git repo, compare file contents against the
SKILL.md's expected output. Look for:
- Files the skill created or modified — do they match what was expected?
- Changes the user had to make after the skill ran (post-corrections)
- Incomplete implementations (TODOs, placeholders, missing pieces)
- Patterns that deviate from what the SKILL.md prescribed

**User feedback**:
After gathering findings, ask the user:
"Want to add anything, or should we review the findings?"

**Static diagnostic** (used in `--review` and `<name>` without prior run):
Validate against baseline rules:
- Frontmatter must have `name` and `description` (required)
- Description max 1024 characters, third person, with specific trigger phrases
- Body should be under 500 lines — use `references/` for overflow
- Name: lowercase, hyphens only, 1-64 characters
- Progressive disclosure: metadata (~100 tokens) → body (<5k tokens) → resources (as needed)
- Check for: dead content (unreferenced sections, commented-out blocks, instructions
  that no longer match the skill's actual behavior), scope creep (sections that belong
  in a different skill or exceed the stated purpose), trigger quality (description
  contains specific verbs and contexts that help the harness match user intent — not
  just generic terms), token efficiency (redundant paragraphs, verbose phrasing that
  could be tightened without losing meaning), completeness (all stated flows have
  matching instructions — no "TODO" or undocumented branches)
- When recommending `references/`: this is a subdirectory alongside SKILL.md
  that holds supporting material (tables, examples, templates) the agent loads
  on demand. Files should be markdown, named descriptively (e.g.,
  `references/diagnostic-tables.md`), and referenced from the body with
  explicit load instructions (e.g., "Read `references/diagnostic-tables.md`
  for the full list").
- If the target SKILL.md is missing frontmatter or required fields (`name`,
  `description`), report it as a `high` finding and propose adding the
  missing structure — infer values from the body content.

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
| **Inference trap** | Text is clear but invites a wrong conclusion — the agent infers something not stated or not intended |

**Static diagnostic output**: Present results as a single unified checklist before proposals:
- One line per baseline rule: ✅ for pass, ❌ for findings (include importance + short description)
- Cross-reference findings go in the same list with ❌ — no separate section, no numbering
- End with finding count: "Found N findings." or "No issues found."

**Importance**: `high` (breaks output, errors) · `medium` (suboptimal, friction) · `low` (style, preferences)

**Recurrence**: Same pattern in LESSONS.md? Increment `Hits` instead of duplicating.
Hits >= 3 escalates: `low` → `medium`, `medium` → `high`.

**context7 (optional)**: If the target skill references a specific
library or framework (e.g., Angular, NestJS, React), use context7
to verify that code patterns, API calls, or config examples in the
SKILL.md match current docs. Report mismatches as findings with
diagnostic `outdated content`. If the skill does not reference any
library, skip — the baseline rules are sufficient. If context7 is not
available in the environment, skip this step — the baseline rules are
sufficient.

### 3. Propose

If no findings were identified, report: "No issues found. The skill looks solid."
If user feedback was not yet collected (e.g., `--review` mode), ask for it
now. If the user has none, end with no proposals.

Before the first proposal, show the sources legend listing only the
sources actually used in the current run (e.g.,
`Sources: static diagnostic, user feedback`).

Present findings one at a time, ordered by importance.
For `--review` findings from LESSONS.md, verify the root cause still exists
in the current SKILL.md before proposing. If resolved, mark as
`(resolved)` and recommend rejecting to clean up the entry.
If there are more than 7 findings, present the top 7 (by importance) and
offer to log the rest to LESSONS.md: "There are [N] more remaining
findings — want me to log them to LESSONS.md for later review?"
If the user declines, discard the remaining findings.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PROPOSAL [N/total] — [importance]
  Source: [conversation | diff | user | lessons | diagnostic]

  Finding: [what was observed]
  Root cause: [diagnostic] — [which line/section and why]
  Hits: [N — omit if first occurrence]

  Proposed change: [what to add/modify/remove]
  Preview:
  - [old line]
  + [new line]
  For additions, show only `+` lines with surrounding context.
  For removals, show only `-` lines.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  (a)ccept  (p)ostpone  (r)eject  (d)on't  (s)kip all
  In --review mode: (a)ccept  (k)eep  (r)eject  (d)on't  (s)kip all
```

- **Accept** → apply the edit
- **Postpone** → save to LESSONS.md
- **Reject** → discard (in review: remove from LESSONS.md)
- **Keep** (only in `--review`):
    - Existing LESSONS.md entry → leave it for later
    - New finding (from diagnostic or user feedback) → add to LESSONS.md
- **Don't** → ask "This will add a permanent negative rule. Confirm? (y/n)",
    then on `y`, append a negative rule at the end of the target's SKILL.md Guardrails
    section (create one if absent — place it as the last section before
    any footer like `---`) using the format:
    `- **Never [action].** [reason from the finding]`
- **Skip all** → write current and all remaining to LESSONS.md, end

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
- **Finding**: line 45 says "if needed" — agent chose wrong path
- **Diagnostic**: ambiguity — line 45 says "if needed" without criteria
- **Proposal**: Replace with explicit condition: "when scope is api or both"

### 2 — medium | Hits: 3
- **Date**: 2026-03-27
- **Source**: diff
- **Finding**: validation skipped before Phase 3, causing downstream error
- **Diagnostic**: missing instruction
- **Proposal**: Add validation step before Phase 3
```

**Rules**:
- Create the file when the first entry is added (postpone or skip all)
- No empty files
- New entries start with `Hits: 1`
- Same pattern (same diagnostic + same root cause location) → increment Hits
  (do not duplicate). Different symptoms from the same root cause count as one entry.
- When incrementing Hits, update the Date to the current date
- Hits >= 3 → escalate importance (`low` → `medium`, `medium` → `high`)
- Accept or reject → remove the entry from LESSONS.md
- Renumber remaining entries sequentially after any removal
- All entries removed → delete the file
- Warn the user when entries exceed 20 and suggest `--review`

## Guardrails

- **Never edit without confirmation.** Show the diff, wait for explicit approval. No
  exceptions. The user owns the skill.
- **Never expose secrets.** Redact API keys, tokens, passwords, credentials (`sk-...`,
  `ghp_...`, `Bearer ...`) with `[REDACTED]` in all output and LESSONS.md.
- **Read before proposing.** Read SKILL.md + LESSONS.md first to avoid duplicates.
- **Never invent.** Zero findings is a valid outcome. Never fabricate findings or fill gaps with guesses — if you don't know, say "I don't know".
- **One at a time.** Present, decide, move on.
- **Respect structure.** Match existing style when inserting content.
- **Don'ts need double confirmation.** Negative rules are impactful — always confirm.
- **Never bump versions.** Version management is the user's responsibility — do not
  modify version fields in frontmatter.
- **Don't duplicate sources definitions across sections.** If a sources configuration
  maps to an existing one (e.g., self-sharpening = `<name>` without prior run), the
  Resolve section is enough. Don't repeat it in Gather.

---

Made with <3 by [Crystian](https://github.com/crystian)
