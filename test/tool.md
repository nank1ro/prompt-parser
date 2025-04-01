---
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
---

<assistant>
  <tool name="get_weather" id="call_1ZUCTfyeDnpqiZbIwpF6fLGt">
  {
    "location": "New York",
    "unit": "C"
  }
  </tool>
</assistant>

<tool name="get_weather" id="call_1ZUCTfyeDnpqiZbIwpF6fLGt">
</tool>

