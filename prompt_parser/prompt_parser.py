import re
import yaml
import json

from typing import Any, Optional
from pydantic import BaseModel
from prompt_parser.attributes import PromptAttributes
from prompt_parser.utils import partial_format


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
