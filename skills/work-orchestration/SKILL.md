---
name: work-orchestration
description: "Invoke this skill whenever a code modification or implementation task requires changes to 2 or more files. Analyzes directional file dependencies, builds a dependency tree, and orchestrates recursive sub-agent distribution. Must be invoked BEFORE writing any code when multi-file changes are detected. Triggers on: refactor, rename, add feature across modules, API change propagation, type/interface change affecting importers."
compatibility: "Designed for Claude Code. Requires Agent tool with subagent_type support (file-modifier, file-creator, code-explorer)."
allowed-tools: "Agent Read Glob Grep AskUserQuestion"
---

# Work Orchestration Protocol

When receiving a code modification or implementation request, follow this process before starting any actual work.

## Step 1: Analyze Scope

Spawn a `code-explorer` agent (Haiku) to map import/dependency relationships between target files. See [dependency-analysis.md](references/dependency-analysis.md) for the prompt template and tree-building instructions.

## Step 2: Ask User for Work Mode

Present the dependency tree, then use `AskUserQuestion` to let the user choose:

| Condition | Recommended mode |
|-|-|
| **4+ files** OR tree depth **≥ 2** | Sub-agent distribution |
| **2–3 files** AND tree depth **≤ 1** | Direct processing |

See [work-mode-selection.md](references/work-mode-selection.md) for AskUserQuestion examples.

## Step 3: Execute

- **Sub-agent distribution** → See [sub-agent-distribution.md](references/sub-agent-distribution.md) for recursive pattern, prompt template, type selection, and prohibited actions.
- **Direct processing** → Main instance handles all files sequentially.

## Step 4: Result Aggregation

Results bubble up through the agent tree. Main instance presents a consolidated summary matching the dependency tree structure.
