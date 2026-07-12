import argparse
import json
import os
import subprocess
import sys
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser(description="Run the full agent pipeline for one ticket.")
parser.add_argument(
    "ticket_key",
    nargs="?",
    help="Linear issue identifier, e.g. AIA-5. If omitted, falls back to TICKET_KEY in .env.",
)
args = parser.parse_args()

if args.ticket_key:
    os.environ["TICKET_KEY"] = args.ticket_key
elif not os.environ.get("TICKET_KEY"):
    parser.error("no ticket key given, and TICKET_KEY isn't set in .env either")

print(f"Running pipeline for ticket: {os.environ.get('TICKET_KEY') or args.ticket_key}")


def run(cmd):
    print(f"\n=== {' '.join(cmd)} ===")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"\nStep failed: {' '.join(cmd)}")
        sys.exit(1)


def read_context_key(key):
    with open("context.json") as f:
        return json.load(f).get(key)


# Make sure we're starting from a clean branch, not whatever feature branch a
# previous run left checked out.
run(["git", "checkout", "main"])
run(["git", "pull", "origin", "main"])

# fetch_linear_ticket.py overwrites context.json from scratch, so this is also
# what resets any leftover state from a previous ticket.
run(["python3", "scripts/fetch_linear_ticket.py"])

run(["python3", "scripts/run_agent.py", "skills/orchestrator/SKILL.md", "plan"])

MAX_ROUNDS = 3
approved = False

for round_number in range(1, MAX_ROUNDS + 1):
    print(f"\n--- round {round_number} of {MAX_ROUNDS} ---")
    run(["python3", "scripts/run_agent.py", "skills/coding-agent/SKILL.md", "code_changes"])
    run(["python3", "scripts/run_agent.py", "skills/qa-agent/SKILL.md", "qa_report"])

    if read_context_key("qa_report")["status"] != "pass":
        print("QA requested changes, looping back to the Coding agent.")
        continue

    run(["python3", "scripts/apply_code_changes.py"])
    run(["python3", "scripts/run_agent.py", "skills/pr-review-agent/SKILL.md", "pr_review"])

    if read_context_key("pr_review")["status"] == "approved":
        approved = True
        break

    print("PR review requested changes, looping back to the Coding agent.")

if not approved:
    print(f"\nDid not get an approved PR after {MAX_ROUNDS} rounds. Stopping here.")
    print("Check qa_report and pr_review in context.json to see what's still unresolved.")
    sys.exit(1)

run(["python3", "scripts/open_pull_request.py"])
run(["python3", "scripts/merge_pull_request.py"])

print("\nDone. Ticket implemented, reviewed, and merged.")