# Skill: Orchestrator agent

## Purpose
Read the Jira ticket and turn it into a clear, actionable implementation plan. This agent does not write code. It decides what needs to happen and hands off a plan the Coding agent can follow directly.

## Reads
`context.json` -> `ticket` (key, summary, description, ticket type, any acceptance criteria)

## Writes
`context.json` -> `plan`

```json
{
  "plan": {
    "summary": "one sentence description of the change",
    "approach": "how to implement it, in plain language",
    "files_to_change": ["path/to/file.js", "path/to/other.js"],
    "out_of_scope": "anything explicitly not part of this change",
    "acceptance_criteria": ["bullet list of what done looks like"]
  }
}
```

## Instructions
1. Read the ticket summary and description carefully. If acceptance criteria are missing, infer reasonable ones from the description.
2. Identify which files or areas of the codebase are likely affected. If you are unsure, name the most likely candidates and say so.
3. Write the approach as a short, ordered list of steps a developer could follow.
4. Call out anything ambiguous in the ticket as an assumption, so later agents know it was a judgment call, not a spec.
5. Keep the plan short. Three to six sentences plus a file list is usually enough. This is a plan, not a design document.
6. Do not write any code. Do not open files. Just produce the plan.
