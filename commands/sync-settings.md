---
allowed-tools: Bash(diff:*), Bash(find:*), Bash(cp:*), Bash(mkdir:*), Bash(ls:*), Read, Write, Glob
description: Sync claude settings between project repo and local ~/.claude
---

## Context

- Project root: current working directory (this config repo)
- Local claude home: `~/.claude/`

## Exclusions

The following are NOT sync targets — never copy, compare, or touch them:

- `.git/` and all contents
- `README.md`
- `settings.local.json`
- Any non-config runtime files in `~/.claude/` (e.g., `history.jsonl`, `*.json` caches, `sessions/`, `projects/`, `backups/`, `cache/`, `channels/`, `debug/`, `downloads/`, `file-history/`, `ide/`, `paste-cache/`, `plans/`, `plugins/`, `shell-snapshots/`, `tasks/`, `telemetry/`)

## Prerequisites

Before starting the procedure, MUST run `ToolSearch({ query: "select:AskUserQuestion" })` to fetch the tool schema. Do NOT substitute with plain text questions.

## Procedure

### Step 1: Choose Sync Direction

Use `AskUserQuestion` to ask the user:

```
AskUserQuestion({
  questions: [{
    question: "동기화 방향을 선택해주세요.",
    header: "Sync",
    options: [
      { label: "프로젝트 → 로컬", description: "프로젝트 설정을 ~/.claude에 반영합니다" },
      { label: "로컬 → 프로젝트", description: "~/.claude 설정을 프로젝트에 반영합니다" }
    ],
    multiSelect: false
  }]
})
```

Based on the user's choice, define:
- **Source**: the side to read from
- **Target**: the side to write to

### Step 2: Diff Comparison

1. List all files in **both** source and target (excluding items listed in Exclusions).
2. Run `diff` on each matching file pair.
3. Identify:
   - **Modified**: file exists on both sides but content differs
   - **Added**: file exists only on source side (will be created on target)
   - **Deleted**: file exists only on target side (will be removed from target)

4. Present findings as a table:

| File | Status |
|-|-|
| `path/to/file` | Modified / Added / Deleted |

5. If no differences found, output "이미 동기화 상태입니다." and stop.

### Step 3: Confirm and Execute

Use `AskUserQuestion` to confirm:

```
AskUserQuestion({
  questions: [{
    question: "위 변경사항을 적용할까요?",
    header: "Confirm",
    options: [
      { label: "전체 적용", description: "모든 변경사항을 적용합니다" },
      { label: "취소", description: "동기화를 취소합니다" }
    ],
    multiSelect: false
  }]
})
```

- **전체 적용**: Copy/create/delete files from source to target.
  - For new files, create parent directories with `mkdir -p` first.
  - For deleted files, remove them from target.
- **취소**: Stop without changes.

### Step 4: Report

Output a summary of what was synced.

### Rules

- Use `~/.claude/` path (works on macOS, Linux, Windows with Git Bash/WSL).
- Always use `diff` for comparison, never assume files are identical without checking.
- Never touch files listed in Exclusions.
- If encoding issues (broken characters) are detected in a file, warn the user before syncing that file.
