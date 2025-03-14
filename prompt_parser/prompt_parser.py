import re
from typing import Any, Dict, List, Optional

from pydantic import BaseModel
import yaml
import json

"""
This module defines classes for managing and formatting prompts for language models.

It includes:

- `partial_format`: A utility function for safely formatting strings with partial template parameters.
- `PromptAttributes`: A Pydantic model to structure and manage attributes for language model prompts (like temperature, model, etc.).
- `Prompt`: A Pydantic model to represent a complete prompt, including attributes and system, user, and assistant message components.

The module provides functionalities for:

- Parsing prompts from strings and files (YAML frontmatter and tag-based content).
- Formatting prompt messages with variables.
- Accessing prompt attributes in a safe and convenient way.
"""


def partial_format(template: str, **kwargs: Any) -> str:
    """
    Partially formats a template string, replacing placeholders with provided keyword arguments.

    If a placeholder is not found in `kwargs`, it is left unchanged in the output string.
    This is useful when you have templates with optional parameters and don't want formatting to fail
    if some parameters are missing.

    Args:
        template: The template string containing placeholders in the format `{placeholder_name}`.
        **kwargs: Keyword arguments where keys are placeholder names and values are their replacements.

    Returns:
        The formatted string with placeholders replaced by values from `kwargs` where available.
        Unresolved placeholders remain in the string.

    Example:
        >>> partial_format("Hello {name}, you are {age} years old.", name="Alice")
        'Hello Alice, you are {age} years old.'
    """

    def replace(match):
        key = match.group(1)
        return str(kwargs.get(key, match.group(0)))  # Return original if key not found

    pattern = r"\{(\w+)\}"  # Matches placeholders like {placeholder}
    return re.sub(pattern, replace, template)


class PromptAttributes(BaseModel, extra="allow"):
    """
    Pydantic model for structuring and managing attributes for language model prompts.

    This class defines common attributes used when interacting with language models,
    such as temperature, top_p, model name, etc. It uses Pydantic's BaseModel for
    data validation and type hinting.  The `extra="allow"` configuration allows for
    passing additional attributes that are not explicitly defined, which can be useful
    for provider-specific or custom parameters.

    Attributes:
        temperature: Temperature for sampling (0.0 to 1.0, higher values more random).
        top_p: Top-p sampling parameter (nucleus sampling).
        top_k: Top-k sampling parameter.
        provider: Name of the language model provider (e.g., "openai", "anthropic").
        endpoint: Specific endpoint for the provider (e.g., "chat", "completions").
        model: Name of the language model to use (e.g., "gpt-4", "claude-v1.3").
        max_tokens: Maximum number of tokens to generate.
        tools: A list of dictionaries defining tools or functions available to the model.
    """

    temperature: Optional[float] = None  # eg 0.5
    top_p: Optional[float] = None  # eg 0.5
    top_k: Optional[int] = None  # eg 50
    provider: Optional[str] = None  # eg openai
    endpoint: Optional[str] = None  # eg chat
    model: Optional[str] = None  # eg gpt-4

    max_tokens: Optional[int] = None  # eg 4096
    tools: Optional[List[Dict[Any, Any]]] = None

    def __init__(
        self,
        **kwargs: Any,
    ):
        """
        Initializes a PromptAttributes object.

        Uses Pydantic BaseModel's initialization, which automatically handles setting
        attributes based on keyword arguments.  The `extra="allow"` configuration in the
        class definition ensures that extra keyword arguments not explicitly defined as
        attributes are also accepted and stored.

        Args:
            **kwargs: Keyword arguments to initialize the PromptAttributes.
        """
        super().__init__(**kwargs)
        self.__dict__.update(kwargs)

    def __getitem__(self, item: str) -> Any:
        """
        Allows accessing attributes using dictionary-like syntax (e.g., `attributes['temperature']`).

        This method enables accessing attributes of the PromptAttributes object using string keys,
        similar to accessing items in a dictionary. It uses `getattr` internally to retrieve
        the attribute value.

        Args:
            item: The name of the attribute to retrieve (string).

        Returns:
            The value of the attribute.

        Raises:
            AttributeError: If the attribute `item` does not exist.
        """
        return getattr(self, item)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves an attribute value by key, returning a default value if not found.

        This method provides a safe way to access attributes, similar to Python's dictionary `get` method.
        If the attribute with the given `key` exists, its value is returned. If not, the provided `default`
        value is returned instead of raising an AttributeError.

        Args:
            key: The attribute name (string).
            default: The value to return if the attribute is not found. Defaults to None.

        Returns:
            The attribute value if found, otherwise the default value.
        """
        return getattr(self, key, default)

    @property
    def temperature_forced(self) -> float:
        """
        Property to access the 'temperature' attribute, raising an AssertionError if it's None.

        This property is used to enforce that the 'temperature' attribute is set. If it's None,
        accessing this property will raise an AssertionError, indicating that the attribute is required.

        Returns:
            The value of the 'temperature' attribute (float).

        Raises:
            AssertionError: If the 'temperature' attribute is None.
        """
        assert self.temperature is not None, "Temperature is required"
        return self.temperature

    @property
    def top_p_forced(self) -> float:
        """
        Property to access the 'top_p' attribute, raising an AssertionError if it's None.

        Similar to `temperature_forced`, this property ensures that the 'top_p' attribute is set.

        Returns:
            The value of the 'top_p' attribute (float).

        Raises:
            AssertionError: If the 'top_p' attribute is None.
        """
        assert self.top_p is not None, "Top P is required"
        return self.top_p

    @property
    def top_k_forced(self) -> int:
        """
        Property to access the 'top_k' attribute, raising an AssertionError if it's None.

        Ensures the 'top_k' attribute is set.

        Returns:
            The value of the 'top_k' attribute (int).

        Raises:
            AssertionError: If the 'top_k' attribute is None.
        """
        assert self.top_k is not None, "Top K is required"
        return self.top_k

    @property
    def provider_forced(self) -> str:
        """
        Property to access the 'provider' attribute, raising an AssertionError if it's None.

        Ensures the 'provider' attribute is set.

        Returns:
            The value of the 'provider' attribute (str).

        Raises:
            AssertionError: If the 'provider' attribute is None.
        """
        assert self.provider is not None, "Provider is required"
        return self.provider

    @property
    def model_forced(self) -> str:
        """
        Property to access the 'model' attribute, raising an AssertionError if it's None.

        Ensures the 'model' attribute is set.

        Returns:
            The value of the 'model' attribute (str).

        Raises:
            AssertionError: If the 'model' attribute is None.
        """
        assert self.model is not None, "Model is required"
        return self.model

    @property
    def max_tokens_forced(self) -> int:
        """
        Property to access the 'max_tokens' attribute, raising an AssertionError if it's None.

        Ensures the 'max_tokens' attribute is set.

        Returns:
            The value of the 'max_tokens' attribute (int).

        Raises:
            AssertionError: If the 'max_tokens' attribute is None.
        """
        assert self.max_tokens is not None, "Max tokens is required"
        return self.max_tokens

    @property
    def endpoint_forced(self) -> str:
        """
        Property to access the 'endpoint' attribute, raising an AssertionError if it's None.

        Ensures the 'endpoint' attribute is set.

        Returns:
            The value of the 'endpoint' attribute (str).

        Raises:
            AssertionError: If the 'endpoint' attribute is None.
        """
        assert self.endpoint is not None, "Endpoint is required"
        return self.endpoint

    @property
    def tools_forced(self) -> List[Dict[Any, Any]]:
        """
        Property to access the 'tools' attribute, raising an AssertionError if it's None.

        Ensures the 'tools' attribute is set.

        Returns:
            The value of the 'tools' attribute (List[Dict[Any, Any]]).

        Raises:
            AssertionError: If the 'tools' attribute is None.
        """
        assert self.tools is not None, "Tools is required"
        return self.tools

    def format_tools(
        self,
        format_partial: bool = True,
        store_state: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        """
        Formats the 'tools' attribute (which is expected to be a JSON string) using provided arguments.

        This method first converts the `tools` attribute (which is assumed to be a list of dictionaries
        and is serialized to JSON) into a string. Then, it formats this string using either `partial_format`
        or standard string formatting based on the `format_partial` parameter.

        Args:
            format_partial: Whether to use partial formatting (using `partial_format`) which doesn't fail
                            if not all placeholders are provided. Defaults to True.
            store_state: Whether to update the `tools` attribute with the formatted version after formatting.
                         Defaults to False.
            *args: Positional arguments passed to the formatting function.
            **kwargs: Keyword arguments passed to the formatting function.

        Returns:
            The formatted tools string.

        Raises:
            AssertionError: If the 'tools' attribute is None.
        """
        assert self.tools is not None, "Tools is required"

        tools_str = json.dumps(self.tools)

        s: str
        # Format the string partially, without being forced to provide all the parameters
        if format_partial:
            s = partial_format(tools_str, *args, **kwargs)
        else:
            s = tools_str.format(*args, **kwargs)

        if store_state:
            self.tools = json.loads(
                s
            )  # Parse back into a list of dicts after formatting

        return s


class Prompt(BaseModel):
    """
    Pydantic model representing a complete prompt for a language model.

    This class encapsulates all components of a prompt: attributes (using `PromptAttributes`),
    and separate messages for system, user, and assistant roles. It provides methods for
    formatting these messages and parsing prompts from strings and files.

    Attributes:
        attributes: An instance of `PromptAttributes` holding prompt settings.
        system: The system prompt message (optional).
        user: The user prompt message (optional).
        assistant: The assistant prompt message (optional).
    """

    attributes: PromptAttributes
    system: Optional[str] = None
    user: Optional[str] = None
    assistant: Optional[str] = None

    def format_system(
        self,
        format_partial: bool = True,
        store_state: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        """
        Formats the system prompt message using provided arguments.

        This method formats the `system` message using either `partial_format` or standard
        string formatting based on the `format_partial` parameter.

        Args:
            format_partial: Whether to use partial formatting (using `partial_format`). Defaults to True.
            store_state: Whether to update the `system` attribute with the formatted message. Defaults to False.
            *args: Positional arguments passed to the formatting function.
            **kwargs: Keyword arguments passed to the formatting function.

        Returns:
            The formatted system prompt message.

        Raises:
            AssertionError: If the 'system' attribute is None.
        """
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
        format_partial: bool = True,
        store_state: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        """
        Formats the user prompt message using provided arguments.

        Similar to `format_system`, but for the `user` message.

        Args:
            format_partial: Whether to use partial formatting. Defaults to True.
            store_state: Whether to update the `user` attribute with the formatted message. Defaults to False.
            *args: Positional arguments passed to the formatting function.
            **kwargs: Keyword arguments passed to the formatting function.

        Returns:
            The formatted user prompt message.

        Raises:
            AssertionError: If the 'user' attribute is None.
        """
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
        format_partial: bool = True,
        store_state: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        """
        Formats the assistant prompt message using provided arguments.

        Similar to `format_system` and `format_user`, but for the `assistant` message.

        Args:
            format_partial: Whether to use partial formatting. Defaults to True.
            store_state: Whether to update the `assistant` attribute with the formatted message. Defaults to False.
            *args: Positional arguments passed to the formatting function.
            **kwargs: Keyword arguments passed to the formatting function.

        Returns:
            The formatted assistant prompt message.

        Raises:
            AssertionError: If the 'assistant' attribute is None.
        """
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
        Parses a prompt from a file path into a Prompt object.

        The file should be formatted with YAML frontmatter for attributes and tags `<system>`, `<user>`, `<assistant>`
        to delineate the different prompt components.

        Example prompt file content:
        ```yaml
        ---
        temperature: 0.5
        top_p: 0.5
        model: gpt-4
        ---

        <system>
        You are a helpful assistant.
        </system>

        <user>
        Hello, how are you?
        </user>
        ```

        Args:
            path: The path to the prompt file (string).

        Returns:
            A Prompt object parsed from the file content.
        """
        with open(path, "r") as f:
            return Prompt.parse(f.read())

    @staticmethod
    def parse(prompt: str) -> "Prompt":
        """
        Parses a prompt string into a Prompt object.

        The prompt string should be formatted with YAML frontmatter (between `---`) for attributes and tags
        `<system>`, `<user>`, `<assistant>` to delineate the different prompt components.

        Example prompt string:
        ```
        ---
        temperature: 0.5
        top_p: 0.5
        model: gpt-4
        ---

        <system>
        You are a helpful assistant.
        </system>

        <user>
        Hello, how are you?
        </user>
        ```

        Args:
            prompt: The prompt string to parse.

        Returns:
            A Prompt object parsed from the prompt string.
        """
        return Prompt(
            attributes=Prompt.__parse_frontmatter(prompt),
            system=Prompt.__parse_tag(tag="system", s=prompt),
            user=Prompt.__parse_tag(tag="user", s=prompt),
            assistant=Prompt.__parse_tag(tag="assistant", s=prompt),
        )

    @staticmethod
    def __parse_frontmatter(s: str) -> PromptAttributes:
        """
        Parses the YAML frontmatter from a prompt string.

        Extracts the content between `---` delimiters and parses it as YAML to create a `PromptAttributes` object.

        Args:
            s: The prompt string containing YAML frontmatter.

        Returns:
            A PromptAttributes object populated from the parsed frontmatter, or an empty PromptAttributes
            object if no frontmatter is found.
        """
        match = re.search(r"---(.*?)---", s, re.DOTALL)
        if match:
            frontmatter_raw = match.group(1).strip()
            frontmatter = yaml.safe_load(frontmatter_raw)
            return PromptAttributes(**frontmatter)
        return PromptAttributes()  # Return empty attributes if no frontmatter found

    @staticmethod
    def __parse_tag(tag: str, s: str) -> Optional[str]:
        """
        Parses the content within a specific tag (e.g., <system>, <user>, <assistant>) from a prompt string.

        Extracts the content between `<tag>` and `</tag>` delimiters for the given tag.

        Args:
            tag: The tag name to parse (e.g., "system", "user", "assistant").
            s: The prompt string to search within.

        Returns:
            The content within the tags as a string, or None if the tag is not found.
        """
        match = re.search(r"<{tag}>(.*?)</{tag}>".format(tag=tag), s, re.DOTALL)
        if match:
            content = match.group(1)
            return content.strip()
        return None  # Return None if tag not found

    @property
    def system_forced(self) -> str:
        """
        Property to access the 'system' message, raising an AssertionError if it's None.

        Ensures the 'system' message is set.

        Returns:
            The system prompt message (str).

        Raises:
            AssertionError: If the 'system' message is None.
        """
        assert self.system is not None, "System prompt is required"
        return self.system

    @property
    def user_forced(self) -> str:
        """
        Property to access the 'user' message, raising an AssertionError if it's None.

        Ensures the 'user' message is set.

        Returns:
            The user prompt message (str).

        Raises:
            AssertionError: If the 'user' message is None.
        """
        assert self.user is not None, "User prompt is required"
        return self.user

    @property
    def assistant_forced(self) -> str:
        """
        Property to access the 'assistant' message, raising an AssertionError if it's None.

        Ensures the 'assistant' message is set.

        Returns:
            The assistant prompt message (str).

        Raises:
            AssertionError: If the 'assistant' message is None.
        """
        assert self.assistant is not None, "Assistant prompt is required"
        return self.assistant

    def __str__(self) -> str:
        """
        Converts the Prompt object back into a formatted prompt string representation.

        This method generates a string representation of the Prompt object, including:
        - YAML frontmatter for attributes (excluding attributes with None values).
        - Tagged blocks for system, assistant, and user messages if they are set.

        Returns:
            A string representation of the Prompt object, formatted for easy parsing.
        """
        # Write frontmatter
        s = "---\n"

        for attr in self.attributes.__dict__:
            # ignore None attributes
            attr_value = getattr(self.attributes, attr)
            if attr_value is None:
                continue

            if attr == "tools":
                s += "tools: "
                s += json.dumps(
                    self.attributes.tools, indent=2, ensure_ascii=False
                )  # ensure_ascii=False to handle non-ascii chars
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
