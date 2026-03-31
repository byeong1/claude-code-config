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
