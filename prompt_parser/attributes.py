import json

from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from prompt_parser.utils import partial_format


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
