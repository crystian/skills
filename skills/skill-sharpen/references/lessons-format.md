# LESSONS.md Format

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

## Rules

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
