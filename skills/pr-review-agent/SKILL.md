# Skill: PR review agent

## Purpose
Do a final quality and correctness pass once QA has passed the code, then open the pull request. This is the last check before a human would normally look at it, so it should be strict about clarity and correctness, not about re-litigating QA's job.

## Reads
`context.json` -> `plan`
`context.json` -> `code_changes`
`context.json` -> `qa_report` (must be `status: pass` before this agent runs)

## Writes
`context.json` -> `pr_review`

```json
{
  "pr_review": {
    "status": "approved",
    "pr_title": "short imperative title, e.g. Fix null check in user lookup",
    "pr_body": "what changed, why, and how it was tested",
    "notes": "anything worth flagging to a human reviewer"
  }
}
```

## Instructions
1. Read the diff as if you were the last line of defense before merge. Check naming, readability, and whether the change matches the ticket's intent, not just its acceptance criteria.
2. Write a clear PR title and a PR body that explains the change for a human skimming it later.
3. Set `status` to `changes_requested` only for real correctness problems QA missed. Do not send it back for style alone; note style comments in `notes` instead.
4. If approved, this agent is also responsible for actually opening the pull request (using the GitHub API or CLI) with the title and body it wrote.
5. Keep the PR body factual: what changed, why, and how someone could verify it. No filler.
