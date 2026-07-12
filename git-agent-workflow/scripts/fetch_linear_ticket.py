import json
import os
import requests

ticket_key = os.environ["TICKET_KEY"]
api_key = os.environ["LINEAR_API_KEY"]

query = """
query($id: String!) {
  issue(id: $id) {
    identifier
    title
    description
    state { name }
  }
}
"""

response = requests.post(
    "https://api.linear.app/graphql",
    json={"query": query, "variables": {"id": ticket_key}},
    headers={"Authorization": api_key, "Content-Type": "application/json"},
)
response.raise_for_status()
data = response.json()

if "errors" in data:
    raise RuntimeError(data["errors"])

issue = data["data"]["issue"]

context = {
    "ticket": {
        "key": issue["identifier"],
        "summary": issue["title"],
        "description": issue.get("description") or "",
        "status": issue["state"]["name"],
    }
}

with open("context.json", "w") as f:
    json.dump(context, f, indent=2)

print(f"Fetched {issue['identifier']}: {issue['title']}")
