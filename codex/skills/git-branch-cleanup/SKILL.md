---
name: git-branch-cleanup
description: Clean up local git branches whose remote tracking branches are gone. Use when the user asks to prune, clear, delete gone branches, or clean old local branches.
---

# Git Branch Cleanup

This workflow can delete local branches. Require explicit confirmation before deletion.

## Procedure

1. Run `git fetch --prune`.
2. Identify the current branch and default branch (`main` or `master` when present).
3. List local branches whose tracking branch is gone.
4. Exclude the current branch and default branch from deletion candidates.
5. If there are no candidates, report `정리할 브랜치가 없습니다.`
6. Show candidates and ask which branches to preserve.
7. Confirm the final delete list.
8. Delete only confirmed branches.
9. Report deleted branches and any failures.

## Safety Rules

- Never delete the current branch.
- Never delete `main` or `master`.
- Prefer normal delete when safe; use force delete only after confirmation.
- If a branch contains unmerged work, call that out before deletion.
