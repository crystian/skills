![skill-sharpen.jpg](../../assets/skill-sharpen.jpg)

# skill-sharpen

> Born from real-world production usage across multiple projects. Every diagnostic category, every proposal flow, and every guardrail exists because it solved a real problem in a real skill.

Kaizen (改善) for AI agent skills. Observe how a skill performed, find what went wrong or could be better, and propose concrete changes to its SKILL.md.

Diagnoses root causes and proposes improvements — you decide each one. Tracks recurrence in LESSONS.md with automatic importance escalation.

## Install

```bash
npx skills add crystian/skills --skill skill-sharpen
```

## Main features

1. **Observation** — monitors how a skill performs during the conversation, collecting friction points, failures, and deviations from expected behavior.
2. **Diagnosis & proposals** — analyzes the collected observations (or the SKILL.md file directly), identifies root causes, and proposes concrete changes. Can be triggered automatically after observation or manually with `--diagnose`.

## Usage flow

1. **Observe then review** — watch a skill run, then analyze what happened.
   ```
   /skill-sharpen
   ```
   _Auto-detect last used skill or start observing the session to use the conversation as input_

   **Do something with the skill to observe** its performance. Then, run:
   ```
   /skill-sharpen --review
   ```

2. **Direct diagnosis** — analyze a SKILL.md without prior execution.
   ```
   /skill-sharpen --diagnose
   /skill-sharpen my-beautiful-skill --diagnose
   ```
   _Finds structural issues, ambiguities, and gaps without needing observation_

Each finding includes a root cause diagnostic and a proposed fix:

```
PROPOSAL 1/3 — high
Source: conversation

Finding: The skill skipped validation step when...
Root cause: specificity gap — no rule for this case
Proposed change: Add validation rule to SKILL.md section...

(a)ccept  (p)ostpone  (r)eject  (d)on't  (s)kip all
```

> Remember you can also be invoked using natural language, e.g. "sharpen the last skill I used" or "review pending lessons".

## LESSONS.md

Findings that you **postpone** or **skip** are saved to a `LESSONS.md` file alongside the analyzed skill's `SKILL.md`. This file acts as a persistent backlog of improvement opportunities:

- Tracks recurrence automatically — repeated patterns increment a `Hits` counter instead of duplicating entries.
- Escalates importance when `Hits >= 3` (`low` → `medium` → `high`).
- Accepted or rejected findings are removed; the file is deleted when empty.
- Use `--review` to revisit accumulated lessons and decide what to apply.

Example entry:

```markdown
### 1 — high | Hits: 1

- **Date**: 2026-03-28
- **Source**: conversation
- **Finding**: line 45 says "if needed" — agent chose wrong path
- **Diagnostic**: ambiguity — line 45 says "if needed" without criteria
- **Proposal**: Replace with explicit condition: "when scope is api or both"
```

## Diagnostics

Every finding is traced back to a root cause in the SKILL.md. These are the diagnostic categories used to classify what went wrong:

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

Full documentation: [SKILL.md](./SKILL.md)
