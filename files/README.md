# Automated Git workflow with AI agents

This project turns a Linear ticket into a merged pull request, using five small AI agents chained together in a GitHub Actions workflow.

## The flow

1. A Linear issue is created or moved to a trigger status.
2. A webhook relay forwards that event to GitHub as a `repository_dispatch`, which starts the workflow (or you trigger it manually).
3. The workflow fetches the issue details from Linear.
4. The **Orchestrator agent** reads the ticket and writes a short implementation plan.
5. The **Coding agent** implements the plan as real code changes.
6. The **QA agent** reviews the changes. If it finds problems, it sends notes back to the Coding agent, and steps 5-6 repeat until QA is satisfied.
7. The **PR Review agent** does a final quality pass and opens the pull request.
8. The **Merge agent** reads the approved PR and merges it with a clean commit message.

## Why SKILL.md files

Each agent is just a role with instructions, an input, and an output. A `SKILL.md` file is the simplest way to write that down: no framework, no code, just a plain markdown file that tells the agent what to do. You hand that file to Claude (or any model) as its system prompt for that step.

Every skill file follows the same shape:

```
# Skill: <name>

## Purpose
One paragraph on what this agent is responsible for.

## Reads
What it receives as input.

## Writes
What it must produce as output, and in what format.

## Instructions
Step by step, how it should do its job.
```

## How data moves between agents

All agents read and write to one shared JSON file, `context.json`. Each agent only adds its own section, never touches the others. This is the entire "state machine" for the pipeline.

```json
{
  "ticket": { "key": "...", "summary": "...", "description": "..." },
  "plan": { "summary": "...", "files_to_change": [], "approach": "..." },
  "code_changes": { "summary": "...", "diff": "...", "branch": "..." },
  "qa_report": { "status": "pass | needs_work", "issues": [] },
  "pr_review": { "status": "approved | changes_requested", "notes": "..." },
  "merge": { "commit_message": "...", "merged_sha": "..." }
}
```

`context.json` is passed between GitHub Actions jobs as a build artifact. Each job downloads it, adds to it, and re-uploads it for the next job.

## Files in this project

```
.github/workflows/agent-pipeline.yml   the GitHub Actions workflow
skills/orchestrator/SKILL.md           orchestrator agent instructions
skills/coding-agent/SKILL.md           coding agent instructions
skills/qa-agent/SKILL.md               qa agent instructions
skills/pr-review-agent/SKILL.md        pr review agent instructions
skills/merge-agent/SKILL.md            merge agent instructions
scripts/fetch_linear_ticket.py         fetches the issue from Linear and starts context.json
scripts/run_agent.py                   small script that runs one agent step
webhook-relay/                         tiny relay that turns a Linear webhook into a repository_dispatch
```

## How to implement this in your own project

1. Copy the `skills/` folder and `.github/workflows/agent-pipeline.yml` into your repo.
2. Add these repo secrets: `ANTHROPIC_API_KEY`, `LINEAR_API_KEY`.
3. Create a Linear personal API key (Settings > API) and give it read access to issues.
4. Wire up the trigger. This is the one place Linear and Jira differ: Jira Automation can call a webhook directly, but Linear webhooks only push events, they can't call the GitHub API themselves. So you need a tiny relay in between:
   - Linear sends a webhook (issue updated, e.g. moved to "Ready for dev") to a URL you host.
   - That relay checks the new status, then calls GitHub's `repository_dispatch` API with the issue identifier.
   - A minimal relay (a few lines, deployable to something like a Cloudflare Worker or a small serverless function) is included in `webhook-relay/`.
5. In Linear, go to Settings > API > Webhooks, point it at your relay's URL, and subscribe to "Issues" events.
6. Fill in `scripts/run_agent.py` with your actual Anthropic API call (a working example is included).
7. Push. Create an issue, move it to the trigger status, and watch the Actions tab.

Start with `workflow_dispatch` (a manual "Run workflow" button with an issue identifier input) instead of the Linear webhook while you are testing. Once the pipeline works end to end, deploy the relay and connect the real webhook.

## Keeping it simple

You do not need a multi-agent framework for this. Each "agent" is just:

- a `SKILL.md` file (its system prompt)
- a chunk of `context.json` it reads
- one API call to Claude
- a chunk of `context.json` it writes

That's the whole pattern. The QA loop is the only part with actual logic: a small script counts iterations and stops after a max (say 3) even if QA keeps failing, so the pipeline can't loop forever.
