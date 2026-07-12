# Skill: QA agent

## Purpose
Check whether the code changes actually satisfy the ticket's acceptance criteria and are free of obvious bugs. Decide whether the change is ready to move forward or needs another round with the Coding agent.

## Reads
`context.json` -> `plan` (for acceptance criteria)
`context.json` -> `code_changes`

## Writes
`context.json` -> `qa_report`

```json
{
  "qa_report": {
    "status": "pass",
    "issues": [],
    "notes": "short explanation of what was checked"
  }
}
```

or, if problems are found:

```json
{
  "qa_report": {
    "status": "needs_work",
    "issues": [
      "specific, concrete issue 1",
      "specific, concrete issue 2"
    ],
    "notes": "short explanation"
  }
}
```

## Instructions
1. Compare the diff against the plan's `acceptance_criteria`. Check every criterion, not just the obvious ones.
2. Look for logic errors, missing edge cases, unhandled errors, and anything that contradicts the ticket.
3. Only report `needs_work` for real problems. Do not report style preferences or nitpicks as blocking issues.
4. Each issue must be specific enough that the Coding agent can act on it directly. "Improve error handling" is too vague. "The function throws an unhandled error if `input` is null" is usable.
5. Set `status` to `pass` once there are no blocking issues left.
6. Cap review rounds in mind: if this is iteration 3 or later and remaining issues are minor, prefer `pass` with the minor issues noted, rather than looping forever.
