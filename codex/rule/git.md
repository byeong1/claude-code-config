# Git

- Never revert user changes unless the user explicitly asks.
- Before committing, inspect `git status`, relevant diffs, current branch, and recent commit style.
- Stage only files that belong to the approved commit.
- Write commit messages in Korean unless the repository history clearly uses another language.
- Match the repository's existing commit message style before falling back to conventional commits.
- Do not push from a feature branch without explicit user confirmation.
- Treat branch deletion, reset, force push, and rebase as destructive or history-changing actions that require confirmation.
- If sensitive files are present, warn before staging and exclude them unless the user explicitly confirms inclusion.
