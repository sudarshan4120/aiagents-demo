# Skill: Coding agent

## Purpose
Implement the plan as real code changes. On the first run, work from the Orchestrator's plan. On later runs (if QA sent it back), fix the specific issues QA listed, without redoing unrelated work.

## Reads
`context.json` -> `plan`
`context.json` -> `qa_report` (only present after the first QA pass; contains issues to fix)

## Writes
`context.json` -> `code_changes`

```json
{
  "code_changes": {
    "summary": "what was changed and why",
    "branch": "feature/TICKET-KEY-short-slug",
    "files_changed": ["path/to/file.js"],
    "diff": "unified diff or full file contents",
    "iteration": 1
  }
}
```

## Instructions
1. If `qa_report` exists and its status is `needs_work`, treat its `issues` list as the only things you need to fix. Do not touch unrelated code.
2. If this is the first run, implement the plan's `files_to_change` following its `approach`.
3. Make the smallest change that satisfies the plan or fixes the QA issues. Avoid unrelated refactors.
4. Write a commit-friendly summary of what changed.
5. Increment `iteration` by 1 each time this agent runs so the pipeline can track how many rounds happened.
6. If something in the plan is genuinely impossible or contradictory, say so clearly in `summary` instead of guessing silently.
