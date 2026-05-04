---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git commit:*), Bash(git push:*), Bash(git branch:*), Bash(git merge:*), Bash(git rebase:*), Bash(gh pr create:*)
description: Analyze changed files, commit, and push to remote
---

## Context

- Current git status: !`git status`
- Staged and unstaged changes: !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Prerequisites

Before starting the procedure, MUST run `ToolSearch({ query: "select:AskUserQuestion" })` to fetch the tool schema. Do NOT substitute with plain text questions.

## Procedure

1. If there are no changes, output "No changes to commit." and stop.
2. Show the user a summary of changed files with a brief description of each change.
3. Use the `AskUserQuestion` tool to ask the user to choose a commit strategy:

```
AskUserQuestion({
  questions: [{
    question: "커밋 전략을 선택해주세요.",
    header: "Commit",
    options: [
      { label: "Single commit", description: "모든 변경사항을 하나의 커밋으로 묶습니다" },
      { label: "Individual commits", description: "파일 또는 논리적 그룹별로 커밋을 분리합니다" }
    ],
    multiSelect: false
  }]
})
```

4. Proceed based on the user's choice:

#### Single Commit (Option 1)

- Analyze all changes and draft an appropriate commit message.
- Use `AskUserQuestion` to confirm the commit message before proceeding:

```
AskUserQuestion({
  questions: [{
    question: "<drafted commit message>",
    header: "Commit Message",
    options: [
      { label: "확인", description: "이 메시지로 커밋합니다" },
      { label: "수정", description: "커밋 메시지를 직접 입력합니다" }
    ],
    multiSelect: false
  }]
})
```

- If the user selects "수정", ask the user to provide a new commit message via `AskUserQuestion` with a free-text question, then use that message.
- Execute `git add` → `git commit` in sequence. **Do NOT push yet** — push is decided in the Merge Strategy step below.

#### Individual Commits (Option 2)

- Group changed files by logical units (related files together).
- Draft a commit message for each group, then batch all groups into a single `AskUserQuestion` call using the `questions` array (max 4 per call).

```
AskUserQuestion({
  questions: [
    { question: "<group 1 commit message>", header: "Commit 1/N", options: [
      { label: "확인", description: "이 메시지로 커밋합니다" },
      { label: "수정", description: "커밋 메시지를 직접 입력합니다" }
    ], multiSelect: false },
    { question: "<group 2 commit message>", header: "Commit 2/N", options: [...] },
    ...
  ]
})
```

- If groups exceed 4, split into multiple `AskUserQuestion` calls (max 4 questions each). **All calls must complete before any commit is executed.**
- If the user selects "수정" for any group, follow up with an additional `AskUserQuestion` to collect the corrected message(s) before proceeding.
- After all commit messages are confirmed, execute `git add` → `git commit` for each group in sequence.
- **Do NOT push yet** — push is decided in the Merge Strategy step below.

### Post-Commit: Merge Strategy

After all commits are complete (but **before** pushing), check the current branch:

- Run `git branch --show-current` to determine the current branch name.
- If the current branch is **main** or **master** (i.e., fast-forward workflow), execute `git push` and end the process. **Skip the merge strategy question entirely.**
- If the current branch is a **feature/topic branch**, proceed with the merge strategy question below (push has not been executed yet):

```
AskUserQuestion({
  questions: [{
    question: "머지 전략을 선택해주세요.",
    header: "Merge",
    options: [
      { label: "Merge commit", description: "모든 커밋을 그대로 유지하며 머지합니다" },
      { label: "Squash and merge", description: "모든 커밋을 하나로 합쳐서 머지합니다" },
      { label: "Rebase and merge", description: "커밋을 대상 브랜치 위로 재배치하여 머지합니다" },
      { label: "Commit only", description: "커밋만 하고 푸시/병합 없이 작업을 계속합니다" }
    ],
    multiSelect: false
  }]
})
```

#### Merge Commit (Option 1)

- Execute `git push`, then inform the user that all commits are pushed and ready for merge.

#### Squash and Merge (Option 2)

- Execute `git push` first.
- Analyze all commits that were just created (use `git log` to review them).
- Recommend 3 squash merge commit message candidates:
    1. **포괄적**: Covers all change categories broadly
    2. **구체적**: Lists specific components/features changed
    3. **간결**: Short and concise summary
- Follow the same style used for the individual commits (mirror the existing repo style).
- Present all 3 options to the user for reference.

#### Rebase and Merge (Option 3)

- Execute `git push`, then inform the user that all commits are pushed and ready for rebase merge.

#### Commit Only (Option 4)

- Do **NOT** push or merge. Only inform the user that commits are complete and continue with the work.
- Run `/commit` again later to select a merge strategy at the time of additional commits and push.

### Rules

- **Match the existing commit message style from the Context section's recent commits. This takes priority over any other format convention.** Examples of patterns to detect and mirror: `[REFACTOR] 메시지`, `[FEAT] 메시지`, `refactor(scope): 메시지`, etc.
- Only fall back to conventional commits format (feat, fix, refactor, docs, chore, etc.) when the repository has no prior commit history to mirror.
- Write commit messages in Korean.
- If sensitive files (.env, credentials, etc.) are detected, warn the user and exclude them.
- If push fails, analyze the cause and inform the user.
- If untracked files exist, ask the user whether to include them in the commit.
