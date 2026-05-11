# Personal Codex Instructions

Respond in Korean unless the user explicitly asks for another language.

This file is the global instruction entry point. Detailed rule modules live in `~/.codex/rule/*.md`; read the relevant module before acting when a task matches its trigger.

## Always-On Rules

- Follow `~/.codex/rule/response-style.md` for every response.
- Follow `~/.codex/rule/file-reading.md` whenever reading or searching files.
- Follow `~/.codex/rule/coding-discipline.md` whenever changing files.
- Follow `~/.codex/rule/action-guard.md` before review, verification, cleanup, research, analysis, audit, investigation, or inspection requests.
- Follow `~/.codex/rule/ask-ui.md` whenever asking the user for a decision.

## Conditional Rules

- Follow `~/.codex/rule/work-orchestration.md` before any task that creates or modifies two or more files.
- Follow `~/.codex/rule/subagent-discipline.md` whenever spawning, steering, waiting for, or closing subagents.
- Follow `~/.codex/rule/coding-conventions.md` when writing or changing code.
- Follow `~/.codex/rule/review.md` for review, audit, inspect, analyze, research, or verification requests.
- Follow `~/.codex/rule/git.md` for git status, branch, commit, push, merge, or cleanup tasks.

## Skills

- Use the `work-orchestration` skill for dependency-aware multi-file changes.
- Use the `inspect-dependencies` skill for file dependency inspection.
- Use the `git-commit-workflow` skill for commit preparation and commit execution.
- Use the `git-branch-cleanup` skill for pruning local branches whose remote tracking branches are gone.
- Use the `codex-settings-sync` skill for syncing this repository's Codex configuration into `~/.codex`.

## Custom Agents

- Use `code_explorer` for read-only codebase and dependency exploration.
- Use `file_modifier` for scoped implementation in existing files.
- Use `file_creator` for scoped creation of new files.
