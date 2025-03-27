import unittest

from pathlib import Path
from prompt_parser import Prompt, PromptAttributes


class TestPromptParser(unittest.TestCase):
    def test_prompt_parser(self):
        example_file_path = str(Path(__file__).with_name("example.prompt"))
        prompt = Prompt.parse_from_file(example_file_path)
        self.assertEqual(prompt.attributes.temperature, 0.5)
        self.assertEqual(prompt.attributes.top_p, 0.5)
        self.assertEqual(prompt.attributes.top_k, 50)
        self.assertEqual(prompt.attributes.provider, "openai")
        self.assertEqual(prompt.attributes.model, "gpt-4")
        self.assertEqual(prompt.attributes.max_tokens, 4096)
        self.assertEqual(prompt.attributes["unknown"], "blablah")
        self.assertEqual(prompt.system, "Hi from system")
        self.assertEqual(prompt.user, "Hi from user {custom}")
        self.assertEqual(prompt.assistant, "Hi from assistant")
        formatted_user = prompt.format_user(custom="ciao")
        self.assertEqual(formatted_user, "Hi from user ciao")
        self.assertEqual(
            prompt.attributes.tools,
            [
                {
                    "name": "get_weather",
                    "description": "Fetches the weather in the given location",
                    "strict": True,
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The location to get the weather for",
                            },
                            "unit": {
                                "type": ["string", "null"],
                                "description": "The unit to return the temperature in",
                                "enum": ["F", "C"],
                            },
                        },
                        "additionalProperties": False,
                        "required": ["location", "unit"],
                    },
                }
            ],
        )

    def test_string_representation(self):
        prompt = Prompt(
            attributes=PromptAttributes(
                temperature=0.5,
                top_p=0.5,
                top_k=50,
                provider="openai",
                model="gpt-4",
                max_tokens=4096,
                unknown="blablah",
            ),
            system="Hi from system",
            user="Hi from user {custom}",
            assistant="Hi from assistant",
        )
        self.assertEqual(
            str(prompt),
            """---
temperature: 0.5
top_p: 0.5
top_k: 50
provider: openai
model: gpt-4
max_tokens: 4096
unknown: blablah
---

<system>
Hi from system
</system>

<assistant>
Hi from assistant
</assistant>

<user>
Hi from user {custom}
</user>
""",
        )

    def test_format_tools(self):
        prompt = Prompt(
            attributes=PromptAttributes(tools=[{"name": r"{function_name}"}])
        )
        formatted_tools = prompt.attributes.format_tools(function_name="get_weather")
        self.assertEqual(formatted_tools, '[{"name": "get_weather"}]')

    def test_not_present_attribute(self):
        prompt = Prompt(attributes=PromptAttributes())
        self.assertEqual(prompt.attributes.get("notpresent"), None)

    def test_not_present_attribute_default_value(self):
        prompt = Prompt(attributes=PromptAttributes())
        self.assertEqual(prompt.attributes.get("notpresent", "default"), "default")


if __name__ == "__main__":
    unittest.main()
