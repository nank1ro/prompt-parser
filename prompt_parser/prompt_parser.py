import re
from typing import Any, Dict
from pydantic import BaseModel
import yaml
import json


def partial_format(template, **kwargs):
    def replace(match):
        key = match.group(1)
        return str(kwargs.get(key, match.group(0)))

    pattern = r"\{(\w+)\}"
    return re.sub(pattern, replace, template)


class PromptAttributes(BaseModel, extra="allow"):
    temperature: float | None = None  # eg 0.5
    top_p: float | None = None  # eg 0.5
    top_k: int | None = None  # eg 50
    provider: str | None = None  # eg openai
    endpoint: str | None = None  # eg chat
    model: str | None = None  # eg gpt-4
    max_tokens: int | None = None  # eg 4096
    tools: Dict[str, Any] | None = None

    def __init__(
        self,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.__dict__.update(kwargs)

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

    @property
    def tools_forced(self) -> Dict[str, Any]:
        assert self.tools is not None, "Tools is required"
        return self.tools

    def format_tools(
        self,
        # Whether to partially format the prompt without throwing if some templates are missing, defaults to true.
        format_partial: bool = True,
        # Whether to store the formatted variable, defaults to `False`.
        store_state: bool = False,
        *args: object,
        **kwargs: object,
    ) -> str:
        assert self.tools is not None, "Tools is required"

        tools_str = json.dumps(self.tools)

        s: str
        # Format the string partially, without being forced to provide all the parameters
        if format_partial:
            s = partial_format(tools_str, *args, **kwargs)
        else:
            s = tools_str.format(*args, **kwargs)

        if store_state:
            self.tools = json.loads(s)

        return s


class Prompt(BaseModel):
    attributes: PromptAttributes
    system: str | None = None
    user: str | None = None
    assistant: str | None = None

    def format_system(
        self,
        # Whether to partially format the prompt without throwing if some templates are missing, defaults to true.
        format_partial: bool = True,
        # Whether to store the formatted variable, defaults to `False`.
        store_state: bool = False,
        *args: object,
        **kwargs: object,
    ) -> str:
        assert self.system is not None, "System prompt is required"

        s: str
        # Format the string partially, without being forced to provide all the parameters
        if format_partial:
            s = partial_format(self.system, *args, **kwargs)
        else:
            s = self.system.format(*args, **kwargs)

        if store_state:
            self.system = s

        return s

    def format_user(
        self,
        # Whether to partially format the prompt without throwing if some templates are missing, defaults to true.
        format_partial: bool = True,
        # Whether to store the formatted variable, defaults to `False`.
        store_state: bool = False,
        *args: object,
        **kwargs: object,
    ) -> str:
        assert self.user is not None, "User prompt is required"

        s: str
        # Format the string partially, without being forced to provide all the parameters
        if format_partial:
            s = partial_format(self.user, *args, **kwargs)
        else:
            s = self.user.format(*args, **kwargs)

        if store_state:
            self.user = s

        return s

    def format_assistant(
        self,
        # Whether to partially format the prompt without throwing if some templates are missing, defaults to true.
        format_partial: bool = True,
        # Whether to store the formatted variable, defaults to `False`.
        store_state: bool = False,
        *args: object,
        **kwargs: object,
    ) -> str:
        assert self.assistant is not None, "Assistant prompt is required"

        s: str
        # Format the string partially, without being forced to provide all the parameters
        if format_partial:
            s = partial_format(self.assistant, *args, **kwargs)
        else:
            s = self.assistant.format(*args, **kwargs)

        if store_state:
            self.assistant = s

        return s

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
            frontmatter_raw = match.group(1).strip()
            frontmatter = yaml.safe_load(frontmatter_raw)
            return PromptAttributes(**frontmatter)
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

    def __str__(self) -> str:
        # Write frontmatter
        s = "---\n"

        for attr in self.attributes.__dict__:
            print("attr", attr)
            # ignore None attributes
            attr_value = getattr(self.attributes, attr)
            if attr_value is None:
                continue

            if attr == "tools":
                s += "tools: "
                s += json.dumps(self.attributes.tools, indent=2)
                s += "\n"
            else:
                s += f"{attr}: {getattr(self.attributes, attr)}\n"
        s += "---\n\n"

        # Write system prompt
        if self.system:
            s += "<system>\n"
            s += self.system.strip() + "\n"
            s += "</system>\n\n"

        # Write assistant prompt
        if self.assistant:
            s += "<assistant>\n"
            s += self.assistant.strip() + "\n"
            s += "</assistant>\n\n"

        # Write user prompt
        if self.user:
            s += "<user>\n"
            s += self.user.strip() + "\n"
            s += "</user>\n"

        return s
