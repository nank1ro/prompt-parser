import re

from typing import Any


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
