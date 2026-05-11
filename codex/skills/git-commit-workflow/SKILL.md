---
name: git-commit-workflow
description: Review changed files, prepare commits, and optionally push using the repository's existing commit style. Use when the user asks to commit, create commits, split commits, prepare a PR-ready branch, or run a commit workflow.
---

# Git Commit Workflow

Use non-destructive git commands first.

## Preflight

1. Run `git status --short`.
2. Inspect staged and unstaged diffs with the smallest useful command.
3. Check the current branch.
4. Review recent commit message style.
5. Look for sensitive files such as `.env`, credentials, tokens, generated secrets, or private keys.

If there are no changes, report `No changes to commit.`

## Commit Strategy

Summarize changed files and recommend either:

- Single commit: one coherent logical change.
- Multiple commits: unrelated or independently reviewable changes.

Ask before committing if:

- untracked files are present,
- sensitive-looking files are present,
- the commit grouping is ambiguous,
- the user has not already approved the commit message.

## Commit Message

- Write commit messages in Korean unless the repository's history uses another language.
- Match the existing repository style before falling back to conventional commits.
- Keep the subject specific and concise.

## Execution

Stage only files that belong to the approved commit.
Create commits in the approved order.
Do not push from a feature branch unless the user explicitly confirms.

If on `main` or `master` and the user asked for commit-and-push, push after committing.
If on a feature branch, ask whether to push, keep local only, or prepare for merge.

## Reporting

Report:

- commit hash and subject
- files included
- whether anything was intentionally left uncommitted
- push status, if applicable
