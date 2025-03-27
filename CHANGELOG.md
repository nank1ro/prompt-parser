# Changelog

## 0.3.3

- **REFACTOR**: Refactor the code.

## 0.3.2

- **DOCS**: Fix typo in README.

## 0.3.1

- **FEAT**: Add `get` to `PromptAttributes` to safely get attributes.
- **DOCS**: Update the README.

## 0.3.0

- **FIX**: Treat `tools` as a List, not a Dict.

## 0.2.0

- **FEAT**: Add `tools` attribute to `PromptAttributes`.
- **FEAT**: Add `format_tools` attribute to `PromptAttributes`.
- **BREAKING CHANGE**: The format methods now accept a `format_partial` (whether to partially format the prompt without throwing if some templates are missing, defaults to `True`) and `store_state` (whether to store the formatted variable in the `Prompt` object, defaults to `False`).
- **REFACTOR**: Use `yaml` module to parse the front matter.
