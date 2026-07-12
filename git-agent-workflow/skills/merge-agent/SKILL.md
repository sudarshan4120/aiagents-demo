# Skill: Merge agent

## Purpose
Merge the approved pull request with a proper commit message. This is the final, mechanical step. No judgment calls about code quality happen here, that already happened in PR review.

## Reads
`context.json` -> `pr_review` (must be `status: approved`)
`context.json` -> `code_changes`
`context.json` -> `ticket`

## Writes
`context.json` -> `merge`

```json
{
  "merge": {
    "commit_message": "TICKET-KEY: short imperative summary\n\nlonger explanation if needed",
    "merged": true,
    "merged_sha": "abc1234"
  }
}
```

## Instructions
1. Refuse to run unless `pr_review.status` is `approved`. If it is not, write `merged: false` and stop.
2. Build the commit message from the ticket key and the PR title, following your team's commit convention (e.g. Conventional Commits, or just `TICKET-KEY: summary`).
3. Use squash merge by default so the PR history stays clean, unless the project convention says otherwise.
4. Actually perform the merge using the GitHub API or CLI, then record the resulting commit SHA.
5. Do not rewrite or reinterpret the code changes. This agent merges what was approved, nothing else.
