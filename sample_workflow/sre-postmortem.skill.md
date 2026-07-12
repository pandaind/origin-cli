---
name: SRE Post-Mortem Generator
description: Generates a structured blameless post-mortem document after an incident is resolved.
---

# SRE Post-Mortem Skill

When invoked, guide the user through generating a complete, blameless post-mortem document. Ask for the following information step by step:

## Required Inputs

1. **Incident Title:** A short, descriptive title (e.g., "Database connection pool exhaustion - 2025-07-13")
2. **Severity:** SEV-1 through SEV-4
3. **Timeline:** Key events with timestamps (incident declared, root cause identified, mitigated, resolved)
4. **Impact:** Number of users affected, duration, and business impact
5. **Root Cause:** The fundamental reason the incident occurred (technical, process, or tooling)
6. **Contributing Factors:** Secondary conditions that allowed the incident to happen
7. **Detection:** How was the incident detected? (alert, customer report, monitoring)
8. **Resolution:** What steps were taken to resolve the incident?

## Output Format

Generate a post-mortem document in this structure:

```markdown
# Post-Mortem: [Incident Title]

**Date:** [Date]
**Severity:** [SEV Level]
**Duration:** [Start] → [End] ([total duration])
**Author(s):** [Names]

## Summary
[2-3 sentence summary of what happened and its impact.]

## Impact
- **Users Affected:** [Number/Percentage]
- **Duration:** [Duration]
- **Revenue Impact:** [If applicable]

## Timeline
| Time (UTC) | Event |
|---|---|
| HH:MM | Incident declared |
| HH:MM | Root cause identified |
| HH:MM | Mitigation applied |
| HH:MM | Incident resolved |

## Root Cause
[Detailed explanation of the root cause.]

## Contributing Factors
- [Factor 1]
- [Factor 2]

## Detection
[How was this incident detected?]

## Resolution
[Steps taken to resolve the incident.]

## Action Items
| Action | Owner | Due Date |
|---|---|---|
| [Preventive action] | [Team/Person] | [Date] |

## Lessons Learned
[Key takeaways from this incident.]
```

## Blameless Culture Reminder
Post-mortems focus on **systems and processes**, not individuals. Frame findings as "the system lacked X" rather than "person Y failed to do Z."
