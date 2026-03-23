# Dependency Analysis

## Step 1-1: Delegate to code-explorer

Spawn `code-explorer` (Haiku) with this prompt:

```
Analyze the import/require/include relationships between the following files and report a dependency map.

Target files:
- {file_1}
- {file_2}
- ...

Report format:
1. For each file, list which other target files it imports (exclude external packages)
2. Directional dependency list: "{file} → {file it depends on}" format
3. Identify root files: files that are depended on by others but depend on nothing within the target list
```

## Step 1-2: Build Dependency Tree

Based on the code-explorer's report, build a dependency tree.

### Example

```
Files to modify: A, B, C, D, F, G
Dependencies: B→A, C→A, D→B, F→B, G→C (arrow means "depends on")

Dependency Tree:
A (root)
├── B
│   ├── D
│   └── F
└── C
    └── G
```

Root files = depended on by others, depend on nothing within the target list. These are modified first; dependents follow.
