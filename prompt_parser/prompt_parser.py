import re
import json
from typing import Any
from pydantic import BaseModel


class PromptAttributes(BaseModel, extra="allow"):
    temperature: float | None = None  # eg 0.5
    top_p: float | None = None  # eg 0.5
    top_k: int | None = None  # eg 50
    provider: str | None = None  # eg openai
    endpoint: str | None = None  # eg chat
    model: str | None = None  # eg gpt-4
    max_tokens: int | None = None  # eg 4096

    def __init__(
        self,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)

    @property
    def temperature_forced(self) -> float:
        assert self.temperature is not None, "Temperature is required"
        return self.temperature

    @property
    def top_p_forced(self) -> float:
        assert self.top_p is not None, "Top P is required"
        return self.top_p

    @property
    def top_k_forced(self) -> int:
        assert self.top_k is not None, "Top K is required"
        return self.top_k

    @property
    def provider_forced(self) -> str:
        assert self.provider is not None, "Provider is required"
        return self.provider

    @property
    def model_forced(self) -> str:
        assert self.model is not None, "Model is required"
        return self.model

    @property
    def max_tokens_forced(self) -> int:
        assert self.max_tokens is not None, "Max tokens is required"
        return self.max_tokens

    @property
    def endpoint_forced(self) -> str:
        assert self.endpoint is not None, "Endpoint is required"
        return self.endpoint


class Prompt(BaseModel):
    attributes: PromptAttributes
    system: str | None = None
    user: str | None = None
    assistant: str | None = None

    def format_system(self, *args: object, **kwargs: object) -> str:
        assert self.system is not None, "System prompt is required"
        return self.system.format(*args, **kwargs)

    def format_user(self, *args: object, **kwargs: object) -> str:
        assert self.user is not None, "User prompt is required"
        return self.user.format(*args, **kwargs)

    def format_assistant(self, *args: object, **kwargs: object) -> str:
        assert self.assistant is not None, "Assistant prompt is required"
        return self.assistant.format(*args, **kwargs)

    @staticmethod
    def parse_from_file(path: str) -> "Prompt":
        """
        Parses a prompt file into a Prompt object.

        Example prompt:

        \-\-\-
        temperature: 0.5
        top_p: 0.5
        top_k: 50
        max_tokens: 4096
        provider: openai
        model: gpt-4
        endpoint: chat
        unknown: blablah
        \-\-\-

        <system>
        Hi from system
        </system>

        <user>
        Hi from user {custom}
        </user>

        <assistant>
        Hi from assistant
        </assistant>
        """
        with open(path, "r") as f:
            return Prompt.parse(f.read())

    @staticmethod
    def parse(prompt: str) -> "Prompt":
        """
        Parses a prompt string into a Prompt object.

        Example prompt:

        \-\-\-
        temperature: 0.5
        top_p: 0.5
        top_k: 50
        max_tokens: 4096
        provider: openai
        model: gpt-4
        endpoint: chat
        unknown: blablah
        \-\-\-

        <system>
        Hi from system
        </system>

        <user>
        Hi from user {custom}
        </user>

        <assistant>
        Hi from assistant
        </assistant>
        """
        return Prompt(
            attributes=Prompt.__parse_frontmatter(prompt),
            system=Prompt.__parse_tag(tag="system", s=prompt),
            user=Prompt.__parse_tag(tag="user", s=prompt),
            assistant=Prompt.__parse_tag(tag="assistant", s=prompt),
        )

    @staticmethod
    def __parse_frontmatter(s: str) -> PromptAttributes:
        match = re.search(r"---(.*?)---", s, re.DOTALL)
        if match:
            frontmatter = match.group(1).strip()
            frontmatter_lines = frontmatter.split("\n")
            result = {}
            for line in frontmatter_lines:
                key, value = line.split(":", 1)
                value = value.lstrip(" ")
                try:
                    # try parsing the value as a JSON object
                    parsed_value = json.loads(value)
                except json.decoder.JSONDecodeError:
                    # fallback to string
                    parsed_value = f"{value}"

                result[f"{key.strip()}"] = parsed_value

            return PromptAttributes(**result)
        return PromptAttributes()

    @staticmethod
    def __parse_tag(tag: str, s: str) -> str | None:
        """
        Parses the content between <tag> and </tag>
        """
        match = re.search(r"<{tag}>(.*?)</{tag}>".format(tag=tag), s, re.DOTALL)
        if match:
            content = match.group(1)
            return content.strip()
        return None

    @property
    def system_forced(self) -> str:
        assert self.system is not None, "System prompt is required"
        return self.system

    @property
    def user_forced(self) -> str:
        assert self.user is not None, "User prompt is required"
        return self.user

    @property
    def assistant_forced(self) -> str:
        assert self.assistant is not None, "Assistant prompt is required"
        return self.assistant
