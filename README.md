# Prompt Parser

A simple Python library for parsing LLM prompts.

## Usage

```python

from prompt_parser import Prompt

prompt = Prompt.parse_from_file("PROMPT_FILE_PATH")

# access the attributes
print(prompt.attributes.temperature) # 0.5
print(prompt.attributes.top_p)  # 0.5
print(prompt.attributes.top_k) # 50
print(prompt.attributes.provider) # openai
print(prompt.attributes.model) # gpt-4
print(prompt.attributes.endpoint) # chat
print(prompt.attributes.max_tokens) # 4096
print(prompt.attributes["unknown"]) # blahblah
print(prompt.system) # Hi from system
print(prompt.user) # Hi from user {custom}
print(prompt.assistant) # Hi from assistant
print(prompt.format_user(custom="Alex")) # "Hi from user Alex"
```

This is the output of the given prompt:
```
---
temperature: 0.5
top_p: 0.5
top_k: 50
max_tokens: 4096
provider: openai
model: gpt-4
endpoint: chat
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
```

If you don't have a prompt file, you can use the `Prompt.parse` method to parse a string.

