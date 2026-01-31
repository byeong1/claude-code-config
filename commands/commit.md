## Git Commit & Push

Analyze changed files, commit, and push to remote.

### Procedure

1. Run `git status` and `git diff` to identify all changed files and their contents.
2. If there are no changes, output "No changes to commit." and stop.
3. Show the user a summary of changed files with a brief description of each change.
4. Ask the user to choose a commit strategy:
    - **1. Single commit**: Bundle all changes into one commit
    - **2. Individual commits**: Split changes into separate commits per file or logical group

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

### Rules

- Follow conventional commits format (feat, fix, refactor, docs, chore, etc.).
- Write commit messages in Korean.
- If sensitive files (.env, credentials, etc.) are detected, warn the user and exclude them.
- Always append the following to the end of every commit message:
    ```
    Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
    ```
- If push fails, analyze the cause and inform the user.
- If untracked files exist, ask the user whether to include them in the commit.
