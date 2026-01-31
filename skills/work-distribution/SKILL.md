---
name: work-distribution
description: "Invoke this skill whenever a code modification or implementation task requires changes to 2 or more files. This skill analyzes directional file dependencies, builds a dependency tree, and orchestrates recursive sub-agent distribution where each agent modifies its file then spawns child agents for dependent files. Must be invoked BEFORE writing any code when multi-file changes are detected."
---

# Work Distribution Protocol

When receiving a code modification or implementation request, you MUST follow this process before starting any actual work.

## Step 1: Analyze Scope and Build Dependency Tree

1. Identify all files that need to be modified to fulfill the request.
2. Analyze **directional dependencies** between files:
    - Which file imports/depends on which?
    - Build a tree where parent = depended-on file, child = dependent file
3. Identify **root files**: files that others depend on, but themselves depend on nothing within the modification scope.

### Dependency Tree Example

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

## Step 2: Ask User for Work Mode

If **2 or more files** need modification, present the dependency tree and ask:

> This task requires modifying N files with the following dependency structure:
> [dependency tree visualization]
>
> 1. Recursive sub-agent processing (each agent handles its file, then spawns child agents for dependent files)
> 2. Main instance direct processing

- User selects **1** → Proceed to Step 3 (recursive sub-agent distribution)
- User selects **2** → Main instance handles all work directly

## Step 3: Recursive Sub-agent Distribution (when user selects 1)

### Core Principle

Each agent follows the **same recursive pattern**:

1. Modify its assigned file
2. After modification complete, identify files that depend on the modified file
3. Spawn sub-agents for those dependent files (parallel if multiple independent files)
4. Wait for all child agents to complete
5. Report results back to parent

### Execution Flow

```
Main Instance (coordinator)
    │
    └── Spawns [Root File Agent(s)]
            │
            ├── Modify root file
            ├── Spawn [Child Agents] for files that depend on root (parallel)
            │       │
            │       ├── Modify child file
            │       ├── Spawn [Grandchild Agents] for next level (parallel)
            │       │       └── ... (recursive)
            │       └── Report to parent
            │
            └── Report to Main Instance
```

### Required Sub-agent Prompt

When creating a sub-agent, you MUST include the following in its prompt:

```
[Work Distribution Protocol - Recursive Sub-agent Directive]

## Your Assignment
- File to modify: {assigned_file}
- Files that depend on your file (your children): {dependent_files_list}

## Execution Steps
1. Modify your assigned file ({assigned_file}) according to the task requirements.

2. After your modification is COMPLETE, spawn sub-agents for each dependent file:
   {dependent_files_list}
   - If multiple dependent files exist with no dependencies between them, spawn them in PARALLEL.
   - Pass this same directive template to each child agent.

3. Wait for all child agents to complete.

4. Report back:
   - Your file modification summary
   - Any issues encountered
   - Child agent results

## Rules
- You may ONLY modify your assigned file: {assigned_file}
- Do NOT modify any other file directly.
- If you discover additional files need modification outside your scope, report this instead of modifying.
```

### Distribution Example

```
Task: Modify A, B, C, D, F, G
Dependency: B→A, C→A, D→B, F→B, G→C

Main Instance
    │
    └── [A Agent] - assigned: A, children: [B, C]
            │
            ├── Modifies A
            │
            ├── Spawns [B Agent] ─────────────────┐
            │       │                             │ parallel
            └── Spawns [C Agent] ─────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
    [B Agent]               [C Agent]
    assigned: B             assigned: C
    children: [D, F]        children: [G]
        │                       │
        ├── Modifies B          ├── Modifies C
        │                       │
        ├── Spawns [D Agent] ┐  └── Spawns [G Agent]
        │                    │ parallel      │
        └── Spawns [F Agent] ┘               │
                │                            │
        [D, F Agents]                   [G Agent]
        Modify D, F                     Modifies G
        (no children)                   (no children)
```

## Step 4: Result Aggregation

Results bubble up through the tree:

1. Leaf agents (no children) complete and report to parent
2. Parent agents collect all child results, combine with own result, report to their parent
3. Root agent(s) report final consolidated result to Main Instance
4. Main Instance presents complete summary to user

### Final Report Structure

```
Work Distribution Complete:
├── A: [modification summary]
│   ├── B: [modification summary]
│   │   ├── D: [modification summary]
│   │   └── F: [modification summary]
│   └── C: [modification summary]
│       └── G: [modification summary]
└── Any issues or additional modifications needed
```
