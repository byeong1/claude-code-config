---
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git branch:*), Read, Glob, Grep
description: Restore prior session work context, or analyze the dependency structure of a target file
---

## Context

- Current git status: !`git status`
- Recent commits: !`git log --oneline -15`
- Current branch: !`git branch --show-current`

## Prerequisites

Before starting the procedure, MUST run `ToolSearch({ query: "select:AskUserQuestion" })` to fetch the tool schema. Do NOT substitute with plain text questions.

**Every `AskUserQuestion` call below MUST include `multiSelect` (boolean) on every question object.** Omitting `multiSelect` triggers `Invalid tool parameters` and aborts the flow. Verify the field is present in every question object before invoking the tool. See `~/.claude/rules/ask-ui/RULE.md` for the full required-field checklist.

## Procedure

### Step 0: Argument Shortcut (skip if no arguments)

If the command was invoked with arguments (`$ARGUMENTS` is non-empty):

1. Treat `$ARGUMENTS` (trimmed) as a candidate **file** path. This skill only operates on files — never folders.
2. Set the target to this path and jump directly to **B-2 (Recursive Dependency Analysis)** — do NOT pre-verify existence. B-2 starts by reading the target file; if the path is invalid, that Read will fail and B-2 handles it (see B-2 error handling).
3. Exception — if the argument is clearly not a path (e.g. contains "?", or is obviously natural-language with no slash/backslash and no file extension): ignore the argument and proceed to Step 1 as usual. Briefly mention in the first user-facing line that the argument was not recognized as a valid file path.

### Step 1: Mode Selection

Use `AskUserQuestion`:

```
AskUserQuestion({
  questions: [{
    question: "어떤 작업을 수행할까요?",
    header: "Follow-up",
    options: [
      { label: "이전 작업 파악", description: "수정/생성된 파일과 메모리를 종합해 진행 중이던 작업을 복원합니다" },
      { label: "구조 파악", description: "특정 파일의 의존성 구조를 재귀적으로 분석합니다" }
    ],
    multiSelect: false
  }]
})
```

### Mode A: Resume Prior Work

#### A-1. Analyze Git Changes

- Extract the list of modified/created files from the `git status` output in the Context section.
- If there are no working-tree changes, fall back to the 5 most recent commits and treat their changed files as the analysis target.
- For each changed file, run `git diff HEAD -- <file>` or `git log -1 --stat -- <file>` to inspect the change.
- Summarize what changed in each file in 1–2 lines.

#### A-2. Read Project Memory

- Look under `C:/Users/SDIJ/.claude/projects/` for the memory folder that corresponds to the current working directory.
  - Try the slugified path first (e.g., `C--Users-SDIJ-code-claude-config`).
- Read the folder's `MEMORY.md` index and any `type: project` memory files it points to.
- Extract any in-progress work, decisions, or next-step notes recorded in memory.

#### A-3. Final Report

Output in this format:

```
## Prior Work Context

### In-progress task
- <inferred from git changes + memory>

### Changed files (N)
| File | Change summary |
|-|-|
| `path/to/file` | <1–2 line summary> |

### Related memory
- <key excerpts from project memory>
```

- Omit the "Related memory" section if no project memory was found.
- If more than 5 files changed, summarize the most important ones in detail and just list the remaining filenames.

### Mode B: Structure Analysis

#### B-1. Target File Input

`AskUserQuestion` requires `options.minItems: 2`. Free-text input is provided automatically by the tool's built-in **Other** button — do NOT add a manual "직접 입력" / "경로 입력" option. Doing so duplicates the auto-Other and violates `~/.claude/rules/ask-ui/RULE.md`.

1. Read the git status / diff already in the Context section. Extract up to **4** modified or untracked file paths as suggested options.
2. If fewer than 2 git-change options are available, append `"취소"` as a real opt-out option so the array still satisfies `minItems: 2`.

**Case A — 2 or more git changes:**

```
AskUserQuestion({
  questions: [{
    question: "분석할 파일을 선택해주세요. (직접 경로를 입력하려면 Other 사용)",
    header: "Target File",
    options: [
      { label: "<git changed file 1>", description: "최근 변경된 파일" },
      { label: "<git changed file 2>", description: "최근 변경된 파일" },
      { label: "<git changed file 3>", description: "최근 변경된 파일" },
      { label: "<git changed file 4>", description: "최근 변경된 파일" }
    ],
    multiSelect: false
  }]
})
```

- Include only as many git-change options as actually exist (max 4).
- If the user selects a git-changed option, use that path directly as the target.
- If the user selects the auto-injected Other (free input), use the typed path.

**Case B — 1 git change:**

```
AskUserQuestion({
  questions: [{
    question: "분석할 파일을 선택해주세요. (직접 경로를 입력하려면 Other 사용)",
    header: "Target File",
    options: [
      { label: "<git changed file 1>", description: "최근 변경된 파일" },
      { label: "취소", description: "구조 파악을 중단합니다" }
    ],
    multiSelect: false
  }]
})
```

**Case C — 0 git changes:**

```
AskUserQuestion({
  questions: [{
    question: "분석할 파일 경로를 입력해주세요. Other를 눌러 직접 입력하거나, 중단하려면 취소를 선택하세요.",
    header: "Target File",
    options: [
      { label: "취소", description: "구조 파악을 중단합니다" },
      { label: "도움말 보기", description: "스킬 사용법 안내 후 종료합니다" }
    ],
    multiSelect: false
  }]
})
```

- "도움말 보기" 선택 시: 짧은 사용법(`/follow-up <파일경로>` 직접 인수 전달 가능)을 안내하고 종료.

**Common to all cases:**

- If the user selects "취소", stop the procedure.
- Do NOT pre-verify the entered path. Pass it straight to B-2 — B-2's initial Read will surface a missing-file error if the path is invalid.

#### B-2. Recursive Dependency Analysis

Read the target file and parse import/require syntax appropriate for the language/framework.

**Initial read — also serves as existence check:**

- Call `Read({ file_path: <target path> })`.
- If Read fails (file not found, permission denied, etc.), output `파일을 찾을 수 없습니다: <path>` and stop the procedure. Do NOT retry with Bash/PowerShell or any shell-based existence check.
- If Read succeeds, proceed with parsing below.

**Language detection patterns:**

| Language / file type | Syntax |
|-|-|
| JS/TS | `import ... from`, `require(...)` |
| Vue | `import`, deps inside `<script>`, `<component>` |
| Python | `import`, `from ... import` |
| Go | `import` |
| Java/Kotlin | `import` |
| Rust | `use`, `mod` |
| C/C++ | `#include` |
| Dockerfile | `FROM`, `COPY`, `ADD` references |
| Other | Best-effort based on file contents |

**Analysis rules:**

- Distinguish project-internal files from external packages (node_modules, pip packages, etc.).
- Include only internal files in the dependency tree. List external packages in a separate section.
- Resolve relative paths (`./`, `../`) and aliases (`@/`, `~/`) to absolute paths from the project root.
- Honor alias settings from tsconfig, webpack, vite, etc. when resolving paths.
- Recursively apply the same parsing to each internal dependency.
- When a circular dependency is detected, mark it as `(circular)` and stop traversing further.
- **Depth limit**: traverse at most **5 levels deep** from the root. When a branch reaches depth 5 and still has internal children, render them as `... (truncated)` and stop descending that branch. This protects output readability on deep graphs.

#### B-3. Output

```
Dependency tree: <target path>

<root>                                ── <one-line role>
├── <child1>                          ── <role>
│   └── <grandchild>                  ── <role>
└── <child2>                          ── <role>

External packages: <pkg1>, <pkg2>, ...

### Notes before editing
- <circular deps, deep chains, shared core files, anything worth knowing before touching the target>
```

## Rules

- Write all user-facing output in Korean (final reports, summaries, prompts).
- Use Unicode box-drawing characters (`├──`, `└──`, `│`) only inside the dependency tree code block. Markdown tables MUST follow the response-style rule and use minimal separators (`|-|-|`).
- If a file cannot be read or parsed, mark it as `(읽기 실패)` and continue with the rest of the analysis.
- If the analysis target exceeds 50 files, inform the user and ask whether to continue.
- In Mode A, silently skip the memory step if `~/.claude/projects/` does not exist or has no entry for this project.
