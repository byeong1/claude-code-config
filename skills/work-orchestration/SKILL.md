---
name: work-orchestration
description: "Invoke this skill whenever a code modification or implementation task requires changes to 2 or more files. This skill analyzes directional file dependencies, builds a dependency tree, and orchestrates recursive sub-agent distribution where each agent modifies its file then spawns child agents for dependent files. Must be invoked BEFORE writing any code when multi-file changes are detected."
---

# Work Orchestration Protocol

When receiving a code modification or implementation request, you MUST follow this process before starting any actual work.

## Step 1: Analyze Scope via code-explorer

Analyze the user's request to identify target files, then spawn a `code-explorer` agent (Haiku) to investigate inter-file dependencies. This saves Opus tokens by avoiding direct file reads from the main instance.

### 1-1. Delegate Dependency Analysis to code-explorer

Spawn `code-explorer` with the following prompt:

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

### 1-2. Main Instance Builds Dependency Tree

Based on the code-explorer's report, the main instance builds the dependency tree and formulates the execution plan.

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

If **2 or more files** need modification, first present the dependency tree visualization as text output, then use the `AskUserQuestion` tool to ask the user which work mode to use.

**You MUST use the `AskUserQuestion` tool** (not plain text) to present the choice.

### Recommendation Logic

Dynamically determine the **(Recommended)** label based on analysis results:

| Condition | Recommendation |
|---|---|
| **4+ files** to modify OR dependency tree depth **≥ 2** | Sub-agent distribution |
| **2–3 files** to modify AND dependency tree depth **≤ 1** | Direct processing |

Append **(Recommended)** only to the recommended option's label.

### Example (Sub-agent distribution recommended)

```
AskUserQuestion({
  questions: [{
    question: "어떤 방식으로 작업을 진행할까요?",
    header: "Work Mode",
    options: [
      { label: "Sub-agent 분산 처리 (Recommended)", description: "각 에이전트가 담당 파일 수정 후 의존 파일에 대해 하위 에이전트를 생성합니다" },
      { label: "직접 처리", description: "메인 인스턴스가 모든 파일을 직접 순차 수정합니다" }
    ],
    multiSelect: false
  }]
})
```

### Example (Direct processing recommended)

```
AskUserQuestion({
  questions: [{
    question: "어떤 방식으로 작업을 진행할까요?",
    header: "Work Mode",
    options: [
      { label: "Sub-agent 분산 처리", description: "각 에이전트가 담당 파일 수정 후 의존 파일에 대해 하위 에이전트를 생성합니다" },
      { label: "직접 처리 (Recommended)", description: "메인 인스턴스가 모든 파일을 직접 순차 수정합니다" }
    ],
    multiSelect: false
  }]
})
```

- User selects **Sub-agent 분산 처리** → Proceed to Step 3 (recursive sub-agent distribution)
- User selects **직접 처리** → Main instance handles all work directly

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

### Sub-agent Type Selection

Select the appropriate `subagent_type` based on the task:

| Task type | subagent_type |
|---|---|
| Modify existing file | `file-modifier` |
| Create new file | `file-creator` |
| Analyze/explore code (no modification) | `code-explorer` |

### Sub-agent Prompt Guidelines

Sub-agent prompts must be **compact yet unambiguous**. Follow this structure strictly.

#### Required Fields

```
1. Target file: absolute path of the file to modify
2. Task: specific changes to make (name exact functions/classes/interfaces)
3. Rationale: what changed in the parent file and why this file must be updated
4. Downstream dependents: files that depend on this file and their expected changes
```

#### Prompt Template

```
File: {absolute path}

Task: {specific changes — specify function names, signature changes, type changes, etc.}

Rationale: {change summary} occurred in {parent file}, so {affected part} in this file must be aligned

Downstream dependents:
- {file A} → {expected change}
- {file B} → {expected change}
- (if none, "none")
```

#### Prohibited Actions

- Do NOT instruct refactoring, improvements, or cleanup outside the task scope
- Do NOT give vague instructions like "review the entire file and make necessary changes"
- Do NOT copy the full change history of the parent file — only summarize changes that affect this file
- Do NOT instruct re-modification of already completed parent file changes

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
Work Orchestration Complete:
├── A: [modification summary]
│   ├── B: [modification summary]
│   │   ├── D: [modification summary]
│   │   └── F: [modification summary]
│   └── C: [modification summary]
│       └── G: [modification summary]
└── Any issues or additional modifications needed
```
