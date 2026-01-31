# Work Distribution Rule

When a code modification or implementation request requires changes to **2 or more files**, perform a quick pre-check before writing any code:

1. Identify all files that need modification.
2. Analyze **directional dependencies** between them (which file is depended on by which).
3. Build a dependency tree and identify the **root files** (files that are depended on by others but depend on nothing within the modification scope).

- If **2+ files** need modification → invoke the `/work-distribution` skill.
- If only **1 file** needs modification → skip the skill and proceed directly.

## Recursive Sub-agent Workflow

Each agent follows this pattern:

1. Modify its assigned file
2. Identify files that depend on the modified file
3. Spawn sub-agents for those dependent files (parallel if multiple)
4. Sub-agents repeat the same pattern recursively

```
Example: A ← B, A ← C, B ← D, B ← F, C ← G

Main Instance
    └── [A Agent]
            ├── Modify A
            └── Spawn [B Agent] [C Agent] in parallel
                    │               │
                    │               ├── Modify C
                    │               └── Spawn [G Agent]
                    │
                    ├── Modify B
                    └── Spawn [D Agent] [F Agent] in parallel
```
