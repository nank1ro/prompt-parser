import unittest
from pathlib import Path

from prompt_parser import Prompt


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


if __name__ == "__main__":
    unittest.main()
