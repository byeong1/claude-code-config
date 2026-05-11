# Coding Conventions

## General

- Avoid abbreviations in variable names. Use descriptive names.
- When iterating over a plural collection, use the singular form for each element.
- Avoid generic names such as `data`, `value`, `item`, `result`, or `response` when a more specific name is available.
- Boolean names should use prefixes such as `is`, `has`, `should`, or `can`.
- Extract magic numbers and repeated magic strings into named constants when doing so improves clarity.
- Prefer positive conditions and early returns over double negatives and deep nesting.

## JavaScript and TypeScript

- Prefer arrow functions for new functions unless local style clearly uses declarations.
- Prefer `if`/`else` over `switch` for new control flow unless the existing codebase uses `switch` heavily.
- Prefer block comments or JSDoc for meaningful comments in JS/TS files.
- Avoid low-value comments that restate the code.
