import os
from anthropic import Anthropic

api_key="sk-d5918a97d7e6aec660557fbb6049a1c84a91283784b7a4abbbcb4dd291e2aa1c"
base_url="https://aiapi.tcredit.com"

ENVIRONMENT_PROMPT = (
    "Windows: the bash tool runs through cmd.exe; use cmd.exe syntax, not Unix "
    "Bash or PowerShell syntax"
    if os.name == "nt"
    else "Unix-like: the bash tool runs the system shell"
)
SYSTEM = (
    f"You are a coding agent at {os.getcwd()}. Environment: {ENVIRONMENT_PROMPT}. "
    "Use bash to solve tasks. Act, don't explain."
)

# -- Tool definition: just bash --
TOOLS = [{
    "name": "bash",
    "description": "Run a shell command.",
    "input_schema": {
        "type": "object",
        "properties": {"command": {"type": "string"}},
        "required": ["command"],
    },
}]

MODEL='claude-sonnet-5-5'

client = Anthropic(api_key=api_key, base_url=base_url)


if __name__ == "__main__":
    messages = []
    messages.append({"role": "user", "content": "hello"})

    response = client.messages.create(
            model=MODEL, system=SYSTEM, messages=messages,
            tools=TOOLS, max_tokens=8000,
        )

    # # Append assistant turn
    # messages.append({"role": "assistant", "content": response.content})

    print(response.content)

    for block in response.content:
        if block.type == "text":
            print(block.text)
        elif block.type == "tool_use":
            print(block.name, block.input)   # input 是 dict，如 {"command": "ls"}

    print(response.stop_reason)

    pass
