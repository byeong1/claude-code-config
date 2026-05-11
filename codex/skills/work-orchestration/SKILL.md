---
name: work-orchestration
description: Plan and coordinate multi-file code changes in Codex. Use when a task creates or modifies two or more files, performs a refactor, propagates API/type/interface changes, renames across modules, or requires dependency-aware sequencing and optional subagent distribution.
---

# Work Orchestration

Use this skill before writing code for any task that touches two or more files.

Do not modify, create, or delete files until the user selects a work mode.

## Workflow

1. Identify the target files and expected change in each file.
2. Map directional dependencies between target files using imports, references, routes, exports, generated types, configuration links, or call flow.
3. Build a dependency order:
   - Root files are depended on by others and do not depend on other target files.
   - Change roots first, then direct dependents, then deeper dependents.
   - If files are independent, group them by responsibility.
4. Present the minimal dependency tree and total file count.
5. Ask the user to choose a work mode.
6. Execute with scoped edits only after mode selection.
7. Verify with the smallest reliable command set available, then broaden verification if shared behavior changed.

## Work Mode Selection

Before editing, output only:

```text
<minimal dependency tree>

Total: N files
```

Then ask the user to choose one mode with the structured user-input UI when available:

- `Direct`: the main instance handles all files sequentially.
- `Sub-agent distribution`: agents handle assigned files according to dependency direction.

Preferred structured question:

```text
Question: 어떤 방식으로 작업을 진행할까요?
Header: Work Mode
Options:
- Direct (Recommended when applicable): 메인 인스턴스가 모든 파일을 직접 순차 처리합니다
- Sub-agent distribution (Recommended when applicable): 각 에이전트가 담당 파일을 처리하고 의존 파일에 대해 하위 에이전트를 생성합니다
```

If the UI tool supports option descriptions, include the descriptions above. If it supports a free-form fallback, allow it so the user can change scope or give custom instructions.

If no structured UI is available in the current Codex runtime, ask the same choice as a concise plain-text question and wait for the answer.

Recommendation logic:

| Condition | Recommendation |
|-|-|
| 2-3 files, dependency depth <= 1, and work per file is small | Direct |
| All other 2+ file cases | Sub-agent distribution |

Put the recommended option first and mark it as recommended.

If the user provides a scope change or custom instruction instead of selecting a mode, re-run dependency analysis or mode selection as needed. Do not proceed until a mode is selected.

## Subagent Distribution

For multi-file work where dependency depth is greater than 1, or where four or more files are involved, prefer dependency-tree subagent distribution when the current Codex environment permits subagents.

Recursive distribution pattern:

1. The main instance builds the dependency tree.
2. The main instance spawns agents for root files.
3. Each root agent modifies or creates its assigned file.
4. That agent spawns child agents for direct dependents when depth budget permits.
5. Child agents repeat the same pattern for their dependents.
6. Results bubble up to the parent, then to the main instance.

If subagent recursion is unavailable or blocked by the current runtime, the parent or main instance handles the remaining dependent files directly in dependency order.

Available custom agents:

- `code_explorer`: read-only dependency and code path exploration.
- `file_modifier`: scoped edits to assigned existing files.
- `file_creator`: scoped creation of assigned new files.

Good subagent tasks:

- Read-only exploration of separate modules.
- Independent file or module updates with disjoint write ownership.
- Parallel verification of a specific risk while the main thread continues implementation.

Avoid subagents when:

- The next local step depends on the result immediately.
- The files are tightly coupled and need one coherent edit.
- The task is small enough that delegation overhead is larger than the work.

When spawning a subagent, give it:

- Agent type to use when custom agents are available.
- Exact file or module ownership.
- The specific requested change.
- Relevant upstream change summary.
- Downstream dependents and whether the child may spawn further agents for them.
- A requirement to list changed paths and verification performed.
- The instruction that other agents may be working in the codebase and it must not revert others' edits.

## Dependency Tree Format

Use a compact ASCII tree when helpful:

```text
A (root)
  B depends on A
    D depends on B
  C depends on A
```

Do not use decorative box-drawing tables or large diagrams.

## Verification

Prefer deterministic checks:

- Existing unit tests for touched modules.
- Typecheck or lint for affected packages.
- Focused build command for changed workspace.
- Manual file diff review when no executable check exists.

If verification cannot be run, state why and describe the residual risk.
