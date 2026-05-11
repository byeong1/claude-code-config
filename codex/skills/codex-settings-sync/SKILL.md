---
name: codex-settings-sync
description: Sync this repository's Codex configuration into the user's Codex home. Use when the user asks to sync, apply, compare, or update Codex settings from this config repository to ~/.codex, including AGENTS.md, rule modules, skills, agents, and optional config fragments.
---

# Codex Settings Sync

Sync only Codex configuration artifacts from this repository. Do not touch runtime state, auth, logs, caches, sessions, history, sqlite files, or sandbox internals.

## Sync Targets

Repository source:

- `codex/AGENTS.md`
- `codex/rule/*.md`
- `codex/skills/*/SKILL.md`
- `codex/agents/*.toml`
- `codex/config.toml` when present

Codex home target:

- `~/.codex/AGENTS.md`
- `~/.codex/rule/*.md`
- `~/.codex/skills/*/SKILL.md`
- `~/.codex/agents/*.toml`
- `~/.codex/config.toml` only after preserving existing unrelated settings

## Procedure

1. List source and target files for sync targets only.
2. Compare content before copying.
3. Report added, modified, and missing target files.
4. Ask before overwriting or deleting anything.
5. Copy confirmed files.
6. Never delete Codex runtime files.

When copying skill folders, copy files into the target skill folder rather than copying a folder onto an existing folder. Avoid creating nested paths such as `~/.codex/skills/work-orchestration/work-orchestration/SKILL.md`.

## Config TOML Handling

Do not overwrite `~/.codex/config.toml` wholesale unless the user explicitly asks.

When applying `codex/config.toml`, merge only the intended Codex configuration sections and preserve unrelated existing settings such as trust records, auth-related configuration, local paths, MCP servers, and user-selected model preferences.

## Windows Notes

Use PowerShell paths:

- repository: `C:\Users\SDIJ\code\claude\config\codex`
- Codex home: `C:\Users\SDIJ\.codex`

Use native PowerShell copy commands with `-LiteralPath` and `-Force`. Avoid destructive recursive deletion.
