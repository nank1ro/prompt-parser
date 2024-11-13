# Prompt Parser

[![GitHub LICENSE](https://img.shields.io/github/license/nank1ro/prompt-parser)](https://github.com/nank1ro/prompt-parser/blob/main/LICENSE)
[![Mounthly Download](https://img.shields.io/pypi/dm/prompt-parser)](https://pypistats.org/packages/prompt-parser)
[![latest version](https://img.shields.io/pypi/v/prompt-parser.svg?style=flat)](https://pypi.org/project/prompt-parser/)
[![supported python version](https://img.shields.io/pypi/pyversions/prompt-parser)](https://pypi.org/project/prompt-parser)

A simple Python library for parsing LLM prompts.

## Usage

```python
from prompt_parser import Prompt

prompt = Prompt.parse("""
---
temperature: 0.5
top_p: 0.5
top_k: 50
max_tokens: 4096
provider: openai
model: gpt-4
endpoint: chat
tools: {
    "name": "get_weather",
    "description": "Fetches the weather in the given location",
    "strict": true,
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The location to get the weather for"
            },
            "unit": {
                "type": ["string", "null"],
                "description": "The unit to return the temperature in",
                "enum": ["F", "C"]
            }
        },
        "additionalProperties": false,
        "required": [
            "location", "unit"
        ]
    }
}
unknown: blablah
---

<system>
Hi from system
</system>

<user>
Hi from user {custom}
</user>

<assistant>
Hi from assistant
</assistant>
""")


# getters
prompt.system  # Hi from system
# or
prompt.system_forced  # "Hi from system" -> will throw an error if not present

prompt.user  # Hi from user {custom}
# or
prompt.user_forced  # "Hi from user {custom}" -> will throw an error if not present

prompt.assistant  # Hi from assistant
# or
prompt.assistant_forced  # "Hi from assistant" -> will throw an error if not present

prompt.format_user(custom="Alex")  # "Hi from user Alex"
# check also `format_system` and `format_assistant`

# access the attributes
prompt.attributes.temperature  # 0.5
prompt.attributes.top_p  # 0.5
prompt.attributes.top_k  # 50
prompt.attributes.provider  # openai
prompt.attributes.model  # gpt-4
prompt.attributes.endpoint  # chat
prompt.attributes.max_tokens  # 4096
prompt.attributes["unknown"]  # blahblah
```

You can also use the `Prompt.parse_from_file(path)` method to parse a prompt file given its path.

### You can convert back a prompt to a string
```python
print(str(prompt))

# or store it in a file
with open("task.prompt", "w") as f:
  f.write(str(prompt))
```
