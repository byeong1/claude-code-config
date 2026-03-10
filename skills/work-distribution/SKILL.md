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

If **2 or more files** need modification, first present the dependency tree visualization as text output, then use the `AskUserQuestion` tool to ask the user which work mode to use.

**You MUST use the `AskUserQuestion` tool** (not plain text) to present the choice.

### Recommendation Logic

분석 결과를 토대로 **(Recommended)** 표시를 동적으로 결정한다:

| 조건 | 추천 |
|---|---|
| 수정 파일 **4개 이상** 또는 의존성 트리 깊이 **2 이상** | Sub-agent 분산 처리 |
| 수정 파일 **2~3개**이고 의존성 트리 깊이 **1 이하** | 직접 처리 |

**(Recommended)** 는 추천되는 옵션의 label 끝에만 붙인다.

### Example (분산 처리 추천 시)

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

### Example (직접 처리 추천 시)

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
