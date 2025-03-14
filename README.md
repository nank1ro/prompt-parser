# Prompt Parser

[![GitHub LICENSE](https://img.shields.io/github/license/nank1ro/prompt-parser)](https://github.com/nank1ro/prompt-parser/blob/main/LICENSE)
[![Mounthly Download](https://img.shields.io/pypi/dm/prompt-parser)](https://pypistats.org/packages/prompt-parser)
[![latest version](https://img.shields.io/pypi/v/prompt-parser.svg?style=flat)](https://pypi.org/project/prompt-parser/)
[![supported python version](https://img.shields.io/pypi/pyversions/prompt-parser)](https://pypi.org/project/prompt-parser)

**A Python library for parsing, formatting, and managing prompts for Large Language Models (LLMs).**

`prompt-parser` simplifies the process of working with LLM prompts by providing a structured way to define, load, and manipulate prompts. It's designed to handle prompts with attributes (like temperature, model, etc.) and different message roles (system, user, assistant).

## Key Features

*   **Parse Prompts:** Load prompts from strings or files, supporting YAML frontmatter for attributes and tagged sections for different message roles.
*   **Structured Prompt Representation:**  Uses `Prompt` and `PromptAttributes` classes to represent prompts and their settings in an organized way.
*   **Attribute Management:** Easily access and manage prompt attributes like temperature, top\_p, model, and custom parameters.
*   **Safe Attribute Access:**  Provides a `.get()` method to access attributes with default values and `.attribute_forced` properties to ensure required attributes are present.
*   **Prompt Formatting:**  Format prompt messages (system, user, assistant, tools) using variables, with support for partial formatting (handling missing variables gracefully).
*   **Serialization:** Convert `Prompt` objects back into formatted strings for saving or further use.

## Installation

You can install `prompt-parser` using pip:

```bash
pip install prompt-parser
```

## Usage

### Parsing a prompt from a string

The core of prompt-parser is the `Prompt` class. You can parse a prompt string using the `Prompt.parse()` method. The prompt string should follow a specific format:

__YAML Frontmatter (Optional)__: Prompt attributes like `temperature`, `model`, `top_p`, etc., can be defined in YAML format between `---` delimiters at the beginning of the string.

__Tagged Message Sections (Optional)__: Use `<system>`, `<user>`, and `<assistant>` tags to define the content for each message role.

Here's an example prompt string and how to parse it:

```python
from prompt_parser import Prompt

prompt_string = """
---
temperature: 0.5
top_p: 0.5
top_k: 50
max_tokens: 4096
provider: openai
model: gpt-4
endpoint: chat
tools: [{
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
}]
unknown: blablah # custom attributes are also allowed
---

<system>
You are a helpful assistant.
</system>

<user>
Hello, I have a question: {query}
</user>

<assistant>
Okay, I'm ready to help!
</assistant>
"""

prompt = Prompt.parse(prompt_string)

print(prompt) # Print the parsed prompt object in string format
```

### Parsing a Prompt from a file

You can also parse prompts directly from a file using Prompt.parse_from_file(path).
The file should have the same format as the prompt string described above.

```py
from prompt_parser import Prompt

# Assuming you have a file named 'task.prompt' in the same directory
prompt_from_file = Prompt.parse_from_file("task.prompt")

print(prompt_from_file)
```
### Accessing Prompt Components

Once you have parsed a Prompt object, you can access its components:
- __Message Roles (system, user, assistant)__: 
  ```py
  prompt.system      # Returns the system message string, or None if not present
  prompt.user        # Returns the user message string, or None if not present
  prompt.assistant   # Returns the assistant message string, or None if not present
  ```
  You can also use the *_forced properties to access these messages, which will raise an AssertionError if the message is not defined. This is useful when you expect a certain message role to always be present.
  ```py
  prompt.system_forced     # Returns the system message string, raises AssertionError if system message is missing
  prompt.user_forced       # Returns the user message string, raises AssertionError if user message is missing
  prompt.assistant_forced  # Returns the assistant message string, raises AssertionError if assistant message is missing
  ```
- __Prompt Attributes__:
  Prompt attributes defined in the YAML frontmatter are accessible through the prompt.attributes object, which is an instance of `PromptAttributes`.
  ```py
  prompt.attributes.temperature  # Access attribute using dot notation
  prompt.attributes['model']      # Access attribute using dictionary-like notation
  ```
  __Safe Attribute Access with .get()__:
  To safely access attributes and provide a default value if an attribute is not present, use the .get(key, default) method:
  ```py
  temperature = prompt.attributes.get('temperature')       # Returns temperature value or None if not defined
  top_k = prompt.attributes.get('top_k', 50)             # Returns top_k value or 50 if not defined
  unknown_attribute = prompt.attributes.get('unknown', "default_value") # Returns "default_value" if 'unknown' is not defined
  ```

### Formatting Prompt Messages

You can format the system, user, assistant, and tools messages by providing keyword arguments to the format_*() methods. This is useful for injecting dynamic content into your prompts.

- __Formatting User Message__:
  ```py
  formatted_user_prompt = prompt.format_user(query="What is the weather in London?")
  print(formatted_user_prompt) # Output: Hello, I have a question: What is the weather in London?
  ```
  Similarly, you can use `prompt.format_system()` and `prompt.format_assistant()` for the system and assistant messages respectively.
- __Formatting Tools__:
  If your prompt includes a tools attribute (defined as a JSON structure in the frontmatter), you can format it using prompt.attributes.format_tools():
  ```py
  formatted_tools = prompt.attributes.format_tools(location="London", unit="C")
  print(formatted_tools) # Output: Formatted JSON string for tools with "location": "London", "unit": "C"
  ```
- __Partial Formatting__:
  By default, the format_*() methods use partial_format, which means that if a variable in your prompt template is not provided in the formatting arguments, it will be left as is in the output string, instead of raising an error. You can disable partial formatting by setting format_partial=False.
- __Storing Formatted State__:
  If you want to update the Prompt object with the formatted message (e.g., to save the formatted prompt), you can set store_state=True in the format_*() methods. This will modify the prompt.system, prompt.user, prompt.assistant, or prompt.attributes.tools attributes in place.

### Converting Prompt to String

You can easily convert a Prompt object back into a formatted string representation using str(prompt). This is useful for logging, saving prompts to files, or passing them to other systems.
```py
prompt_string_output = str(prompt)
print(prompt_string_output)

# Save the prompt to a file:
with open("formatted_prompt.prompt", "w") as f:
    f.write(str(prompt))
```

## Benefits of Using `prompt-parser`

- __Organization__: Structure your prompts and attributes in a clean and manageable way.
- __Readability__: Prompts are easier to read and understand when separated into attributes and message roles.
- __Flexibility__: Easily load prompts from strings or files, and format them dynamically.
- __Safety__: Use .get() for safe attribute access and .attribute_forced for ensuring required attributes.
- __Maintainability__: Makes prompt management and updates easier in your LLM applications.

## License

This project is licensed under the [MIT License](https://raw.githubusercontent.com/nank1ro/prompt-parser/refs/heads/main/LICENSE).
