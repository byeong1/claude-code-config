# Work Orchestration Rule

For any task that creates or modifies two or more files, use the `work-orchestration` skill before editing.

Do not modify, create, or delete files until the work mode has been selected by the user.

Apply this rule to:

- multi-file creation or modification
- refactors across modules
- API, type, or interface changes that affect callers
- renames across modules
- configuration changes that require code updates
- feature work spanning multiple files

Minimum behavior:

1. Identify target files and likely dependency direction.
2. Build a minimal dependency tree.
3. Present total file count.
4. Ask the user to choose `Direct` or `Sub-agent distribution`.
5. Wait for the user's mode selection.
6. Execute only after the mode has been selected.
7. State verification checks for non-trivial multi-step work.

Use the most structured user-input UI available in the current Codex environment. If no such UI is available, ask a concise plain-text question and wait.
