# Sub-agent Distribution

## Core Principle

Each agent follows the same recursive pattern:

1. Modify its assigned file
2. Spawn sub-agents for the child files specified in the prompt's `Downstream dependents` section (parallel if independent). Do NOT re-analyze dependencies — the parent has already resolved them in Step 1 and embedded the child specs in this prompt.
3. Wait for all child agents to complete
4. Report results back to parent

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
- {child file A absolute path}
  Task: {specific changes for child A}
  Rationale: {why A must change given this file's change}
  Downstream dependents: {grandchild specs in the same nested format, or "none"}
- {child file B absolute path}
  Task: ...
  Rationale: ...
  Downstream dependents: ...
- (if none, write "none")

Response constraint: Final response under {N} characters. List outcomes only, not process.
```

### Required Fields

1. **Target file**: absolute path
2. **Task**: specific changes (name exact functions/classes/interfaces)
3. **Rationale**: what changed in the parent file and why this file must be updated
4. **Downstream dependents**: full nested spec (File / Task / Rationale / Downstream dependents) for every child the sub-agent must spawn. The parent — not the sub-agent — resolves dependencies in Step 1 and writes the child specs here. Sub-agents spawn children verbatim from this list without re-analyzing imports.
5. **Response constraint**: maximum character count and "outcomes only" directive, per the global `execution` rule

## Prohibited Actions

- Do NOT instruct refactoring, improvements, or cleanup outside the task scope
- Do NOT give vague instructions like "review the entire file and make necessary changes"
- Do NOT copy the full change history of the parent file — only summarize changes that affect this file
- Do NOT instruct re-modification of already completed parent file changes
- Do NOT instruct sub-agents to run typecheck, lint, tests, or any whole-project verification — these are the main instance's responsibility, performed after all sub-agents complete. Sub-agents work on partial state, may run in parallel, and would expand their Read scope beyond their assigned file to interpret errors.

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
