# Changelog

## 0.2.0

- **FEAT**: Add `tools` attribute to `PromptAttributes`
- **FEAT**: Add `format_tools` attribute to `PromptAttributes`
- **BREAKING CHANGE**: The format methods now accept a `format_partial` (whether to partially format the prompt without throwing if some templates are missing, defaults to `True`) and `store_state` (whether to store the formatted variable in the `Prompt` object, defaults to `True`)
- **REFACTOR**: Use `yaml` module to parse the front matter
