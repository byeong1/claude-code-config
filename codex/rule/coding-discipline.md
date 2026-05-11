# Coding Discipline

- Before editing, state briefly what files or areas will change and why.
- If a request has multiple plausible meanings, stop and ask which interpretation is intended.
- If the user proposes an approach with a meaningfully simpler, safer, or more correct alternative, state the alternative briefly before proceeding.
- For tasks with three or more implementation steps, list each step with a concrete verification check before executing.
- Modify only what the task requires.
- Do not perform adjacent cleanup, formatting churn, or unrelated refactors.
- Preserve local style, naming, formatting, and file organization unless the task requires changing them.
- Prefer small, direct changes over new abstractions.
- After writing code, shrink it if the same behavior can be expressed much more simply.
- Remove imports, variables, functions, and files only when your own changes made them unused.
- Mention unrelated dead code instead of deleting it.
- Never revert user changes unless the user explicitly asks.
