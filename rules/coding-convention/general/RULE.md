# General Coding Convention

**Naming:**
- Avoid abbreviations in variable names. Use descriptive, full-word names.
  - Bad: `const t = templates.find((t: any) => t.id === id);`
  - Good: `const template = templates.find((template) => template.id === id);`
- When iterating over a plural-named collection, use the singular form of the collection name.
  - `cptSortedTemplates` → iterate as `cptSortedTemplate`
  - `users` → iterate as `user`
  - `filteredItems` → iterate as `filteredItem`
- Avoid using reserved words (`data`, `value`, `item`, `result`, `response`, etc.) as variable names. Choose names that describe what the variable actually represents.
- Boolean variables must use `is`, `has`, `should`, `can` prefixes.
  - Bad: `visible`, `loading`, `disabled`
  - Good: `isVisible`, `isLoading`, `isDisabled`

**Constants:**
- Avoid magic numbers and magic strings. Extract them into named constants.
  - Bad: `if (status === 3)`
  - Good: `if (status === STATUS_COMPLETE)`

**Conditions:**
- Avoid double negation. Use positive naming and conditions.
  - Bad: `if (!isNotValid)`, `if (!isDisabled)`
  - Good: `if (isValid)`, `if (isEnabled)`
- Prefer early return over deep nesting.
  - Bad: `if (condition) { ... long logic ... } else { return; }`
  - Good: `if (!condition) return; ... long logic ...`
