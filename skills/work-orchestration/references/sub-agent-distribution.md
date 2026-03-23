# Sub-agent Distribution

## Core Principle

Each agent follows the same recursive pattern:

1. Modify its assigned file
2. Identify files that depend on the modified file
3. Spawn sub-agents for those dependent files (parallel if independent)
4. Wait for all child agents to complete
5. Report results back to parent

## Execution Flow

```
Main Instance (coordinator)
    └── Spawns [Root File Agent(s)]
            ├── Modify root file
            ├── Spawn [Child Agents] for dependents (parallel)
            │       ├── Modify child file
            │       ├── Spawn [Grandchild Agents] (parallel)
            │       │       └── ... (recursive)
            │       └── Report to parent
            └── Report to Main Instance
```

## Sub-agent Type Selection

| Task type | subagent_type |
|-|-|
| Modify existing file | `file-modifier` |
| Create new file | `file-creator` |
| Analyze/explore code (no modification) | `code-explorer` |

## Prompt Template

Sub-agent prompts must be **compact yet unambiguous**:

```
File: {absolute path}

Task: {specific changes — specify function names, signature changes, type changes, etc.}

Rationale: {change summary} occurred in {parent file}, so {affected part} in this file must be aligned

Downstream dependents:
- {file A} → {expected change}
- {file B} → {expected change}
- (if none, "none")
```

### Required Fields

1. **Target file**: absolute path
2. **Task**: specific changes (name exact functions/classes/interfaces)
3. **Rationale**: what changed in the parent file and why this file must be updated
4. **Downstream dependents**: files depending on this file and their expected changes

## Prohibited Actions

- Do NOT instruct refactoring, improvements, or cleanup outside the task scope
- Do NOT give vague instructions like "review the entire file and make necessary changes"
- Do NOT copy the full change history of the parent file — only summarize changes that affect this file
- Do NOT instruct re-modification of already completed parent file changes

## Distribution Example

```
Task: Modify A, B, C, D, F, G
Dependency: B→A, C→A, D→B, F→B, G→C

Main Instance
    └── [A Agent] - assigned: A, children: [B, C]
            ├── Modifies A
            ├── Spawns [B Agent] ──┐
            └── Spawns [C Agent] ──┘ parallel

    [B Agent]               [C Agent]
    assigned: B             assigned: C
    children: [D, F]        children: [G]
        ├── Modifies B          ├── Modifies C
        ├── Spawns [D Agent] ┐  └── Spawns [G Agent]
        └── Spawns [F Agent] ┘ parallel

    [D, F Agents]           [G Agent]
    Modify D, F             Modifies G
    (no children)           (no children)
```

## Result Aggregation

Results bubble up through the tree:

1. Leaf agents (no children) complete and report to parent
2. Parent agents collect all child results, combine with own, report upward
3. Root agent(s) report consolidated result to Main Instance
4. Main Instance presents summary:

```
Work Orchestration Complete:
├── A: [modification summary]
│   ├── B: [modification summary]
│   │   ├── D: [modification summary]
│   │   └── F: [modification summary]
│   └── C: [modification summary]
│       └── G: [modification summary]
└── Any issues or additional modifications needed
```
