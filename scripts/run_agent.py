import json
import sys
from anthropic import Anthropic

skill_path = sys.argv[1]
output_key = sys.argv[2]

with open(skill_path) as f:
    system_prompt = f.read()

with open("context.json") as f:
    context = json.load(f)

client = Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4000,
    system=system_prompt
    + "\n\nRespond only with a single JSON object matching the format shown in the "
    "SKILL.md Writes section. No prose, no markdown fences.",
    messages=[
        {
            "role": "user",
            "content": json.dumps(context),
        }
    ],
)

text = "".join(block.text for block in message.content if block.type == "text")
result = json.loads(text)

context[output_key] = result[output_key]

with open("context.json", "w") as f:
    json.dump(context, f, indent=2)

print(f"{skill_path} wrote '{output_key}'")
