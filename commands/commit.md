## Git Commit & Push

Analyze changed files, commit, and push to remote.

### Procedure

1. Run `git status` and `git diff` to identify all changed files and their contents.
2. If there are no changes, output "No changes to commit." and stop.
3. Show the user a summary of changed files with a brief description of each change.
4. Use the `AskUserQuestion` tool to ask the user to choose a commit strategy:

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

5. Proceed based on the user's choice:

#### Single Commit (Option 1)

- Analyze all changes and draft an appropriate commit message.
- Show the commit message to the user for confirmation.
- Execute `git add` → `git commit` → `git push` in sequence.

#### Individual Commits (Option 2)

- Group changed files by logical units (related files together).
- For each group, draft a commit message and show it to the user for confirmation.
- Execute `git add` → `git commit` for each group.
- After all commits are complete, execute `git push`.

### Post-Commit: Merge Strategy

After all commits are complete and pushed, use the `AskUserQuestion` tool to ask the user to choose a merge strategy:

```
AskUserQuestion({
  questions: [{
    question: "머지 전략을 선택해주세요.",
    header: "Merge",
    options: [
      { label: "Squash merge", description: "모든 커밋을 하나로 합쳐서 머지합니다" },
      { label: "Regular merge", description: "모든 커밋을 그대로 유지합니다" }
    ],
    multiSelect: false
  }]
})
```

#### Squash Merge (Option 1)

- Analyze all commits that were just created (use `git log` to review them).
- Recommend 3 squash merge commit message candidates:
    1. **포괄적**: Covers all change categories broadly
    2. **구체적**: Lists specific components/features changed
    3. **간결**: Short and concise summary
- Follow the same conventional commits format.
- Present all 3 options to the user for reference.

#### Regular Merge (Option 2)

- No additional action needed. Inform the user that all commits are pushed and ready for merge.

### Rules

- Follow conventional commits format (feat, fix, refactor, docs, chore, etc.).
- Write commit messages in Korean.
- Before drafting a commit message, run `git log --oneline -10` to review recent commit history. Match the existing commit message style, tone, and conventions (e.g., prefix usage, language patterns, level of detail) to maintain consistency across the project.
- If sensitive files (.env, credentials, etc.) are detected, warn the user and exclude them.
- If push fails, analyze the cause and inform the user.
- If untracked files exist, ask the user whether to include them in the commit.
