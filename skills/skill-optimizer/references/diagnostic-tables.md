# Diagnostic Tables

## Cross-reference categories

| Category                   | What to look for                                                  |
| -------------------------- | ----------------------------------------------------------------- |
| **Missing instructions**   | Steps the skill should have taken but the SKILL.md didn't mention |
| **Ambiguous instructions** | Places where the SKILL.md was vague and the skill chose wrong     |
| **Wrong defaults**         | Default behaviors that consistently need overriding               |
| **Missing guardrails**     | Errors that a "don't" rule would have prevented                   |
| **Outdated content**       | References to APIs, tools, or patterns that have changed          |
| **Missing examples**       | Cases where an example would have prevented misinterpretation     |
| **Structural issues**      | Ordering problems, missing sections, or buried important info     |
| **Missing task tracking**  | Skill has enumerable steps but no instruction to track progress via harness task tools |

## Root-cause diagnostics

| Diagnostic              | What it means                                                                                        |
| ----------------------- | ---------------------------------------------------------------------------------------------------- |
| **Coherence**           | Sections don't align — process says one thing, guardrails another                                    |
| **Coupling**            | Content that doesn't belong — out-of-scope, mixed responsibilities                                   |
| **Ambiguity**           | Instruction open to interpretation without concrete criteria                                         |
| **Contradiction**       | Two rules directly conflict                                                                          |
| **Specificity gap**     | No rule for this case — the agent had to guess                                                       |
| **Missing instruction** | The SKILL.md doesn't cover this scenario                                                             |
| **Redundancy**          | Same instruction repeated differently — confusion + wasted tokens                                    |
| **Error inducer**       | A specific instruction promotes the wrong behavior                                                   |
| **Inference trap**      | Text is clear but invites a wrong conclusion — the agent infers something not stated or not intended |
