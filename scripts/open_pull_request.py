import json
import os
import subprocess
import sys

import requests
from dotenv import load_dotenv

print("1. starting open_pull_request.py", flush=True)

load_dotenv()
print("2. loaded .env", flush=True)

with open("context.json") as f:
    context = json.load(f)
print("3. loaded context.json", flush=True)

pr_review = context["pr_review"]
print(f"4. pr_review.status = {pr_review['status']}", flush=True)

if pr_review["status"] != "approved":
    print(f"pr_review.status is '{pr_review['status']}', not opening a PR.", flush=True)
    sys.exit(1)

owner_repo = subprocess.run(
    ["git", "config", "--get", "remote.origin.url"],
    capture_output=True,
    text=True,
).stdout.strip()
print(f"5. remote url = {owner_repo}", flush=True)

owner_repo = owner_repo.split("github.com")[-1].lstrip(":/").removesuffix(".git")
print(f"6. owner/repo = {owner_repo}", flush=True)

token = os.environ.get("GITHUB_TOKEN", "")
print(f"7. GITHUB_TOKEN present: {bool(token)}, length: {len(token)}", flush=True)

branch = context["code_changes"]["branch"]
print(f"8. branch = {branch}", flush=True)

print("9. calling GitHub API to open the PR...", flush=True)
response = requests.post(
    f"https://api.github.com/repos/{owner_repo}/pulls",
    headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    },
    json={
        "title": pr_review["pr_title"],
        "body": pr_review["pr_body"],
        "head": branch,
        "base": "main",
    },
)
print(f"10. response status: {response.status_code}", flush=True)
print(f"11. response body: {response.text}", flush=True)

response.raise_for_status()
pr = response.json()

context["pr_review"]["pr_number"] = pr["number"]
context["pr_review"]["html_url"] = pr["html_url"]

with open("context.json", "w") as f:
    json.dump(context, f, indent=2)

print(f"Opened PR #{pr['number']}: {pr['html_url']}", flush=True)