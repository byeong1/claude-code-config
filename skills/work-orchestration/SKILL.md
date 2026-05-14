---
name: work-orchestration
description: "Invoke this skill whenever a task requires creation of or changes to 2 or more files. Analyzes directional file dependencies, builds a dependency tree, and orchestrates recursive sub-agent distribution. Must be invoked BEFORE writing any code when multi-file creation or changes are detected. Triggers on: multi-file creation, refactor, rename, add feature across modules, API change propagation, type/interface change affecting importers."
compatibility: "Designed for Claude Code. Requires Agent tool with subagent_type support (file-modifier, file-creator, code-explorer, work-verifier)."
allowed-tools: "Agent Read Glob Grep AskUserQuestion"
---

# Work Orchestration Protocol

When receiving a code modification or implementation request, follow this process before starting any actual work.

**CRITICAL: You MUST execute ALL steps (Step 1 → Step 2 → Step 3 → Step 4 → Step 5 → Step 6) in order. Do NOT skip any step. Do NOT jump directly to file creation or modification. Even if the task seems simple (e.g., creating independent files with no dependencies), every step must be performed.**

## Step 1: Analyze Scope

**MUST read [dependency-analysis.md](references/dependency-analysis.md) before proceeding.**

Spawn a `code-explorer` agent (Haiku) to map import/dependency relationships between target files.

## Step 2: Define Acceptance Criteria

**MUST read [acceptance-criteria.md](references/acceptance-criteria.md) before proceeding.**

Based on the Step 1 dependency map, write a single Acceptance Criteria block: `Goal`, `Required outcomes`, `Risk items`, `Out of scope`. This block is the contract for sub-agents and the checklist for Step 6.

## Step 3: Ask User for Work Mode

**MUST read [work-mode-selection.md](references/work-mode-selection.md) before proceeding.**

Output ONLY the minimal dependency tree block + total file count, then immediately call `AskUserQuestion`. No preamble, no recommendation rationale, no section headers. Rationale lives in the option descriptions. See work-mode-selection.md for the exact output format and AskUserQuestion template.

## Step 4: Execute

**MUST read [sub-agent-distribution.md](references/sub-agent-distribution.md) before proceeding (if Sub-agent mode selected).**

- **Sub-agent distribution** → Follow the recursive pattern, prompt template, type selection, and prohibited actions defined in sub-agent-distribution.md. Pass the Step 2 Acceptance Criteria block verbatim to every sub-agent.
- **Direct processing** → Main instance handles all files sequentially, holding the Step 2 Acceptance Criteria as its own contract.

## Step 5: Result Aggregation and Plan Reconciliation

Results bubble up through the agent tree. Main instance presents a consolidated summary matching the dependency tree structure.

Then reconcile the actual change-set against Step 2:

1. List every file actually created / modified / deleted.
2. Compare against Step 2's `Required outcomes` and `Out of scope`.
3. If any file was touched that Step 2 did not anticipate, OR if a planned risk item is now missing/added, **update Step 2** before proceeding to Step 6. Stale acceptance criteria invalidate verification.

Do NOT skip this reconciliation — it is the only defense against Step 2/Step 6 drift when execution surfaces unexpected changes.

## Step 6: Verification

**MUST read [verification-pass.md](references/verification-pass.md) before proceeding.**

Run verification per the mode × risk matrix defined in verification-pass.md. If skipped, output the explicit skip line — never silently omit Step 6.
