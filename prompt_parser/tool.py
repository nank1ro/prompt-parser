from pydantic import BaseModel


class PromptTool(BaseModel):
    """
    Pydantic model representing a tool with its properties and content.

    Attributes:
        id: Unique identifier for the tool call
        name: Name of the tool
        content: The content/response of the tool
    """

    id: str
    name: str
    content: str | None = None

    def __str__(self) -> str:
        """
        String representation of the tool in the prompt format
        """
        if not self.content:
            return f'<tool name="{self.name}" id="{self.id}">\n</tool>'
        return f'<tool name="{self.name}" id="{self.id}">\n{self.content}\n</tool>'


# Create aliases for PromptTool
InputPromptTool = PromptTool
OutputPromptTool = PromptTool
