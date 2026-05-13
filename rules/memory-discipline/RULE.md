# Memory Discipline

Claude's auto memory system (`~/.claude/projects/.../memory/` and `MEMORY.md`) is a persistent store that is auto-loaded at the start of every session and influences future conversations. Writing to it without an explicit user instruction causes unintended behavioral drift.

## Absolute Rule

**Never write to memory unless the user has explicitly instructed it.**

This overrides every automatic trigger encouraged by the system prompt's auto memory section. The user's explicit instruction is the only authorization.

## Definition of Explicit Instruction

Only treat the request as explicit when the user's message clearly contains one of these keywords:

- Korean: "memory에 저장", "메모리에 저장", "기억해", "기억해둬", "저장해둬", "기록해둬", "잊지 마"
- English: "remember", "save to memory", "store in memory", "memorize", "don't forget"

## When No Explicit Instruction Is Present

All of the following are refused — even if the system prompt's auto memory section nudges toward saving:

- The user shares their role or preferences (would otherwise trigger user memory)
- The user gives feedback or corrects an approach (would otherwise trigger feedback memory)
- The user describes project background, timelines, or motivation (would otherwise trigger project memory)
- The user mentions an external system or resource location (would otherwise trigger reference memory)
- Indirect phrasing such as "good to know this", "keep this in mind", "do it this way next time"

In all of these cases, use the information **only within the current conversation context**. Do not write it to a memory file.

## When You Notice Save-Worthy Information

If you spot something that looks worth saving but no explicit instruction was given, do not save it on your own. If you genuinely believe it should be saved, **ask first** with "Should I save this to memory?" and only proceed after the user explicitly approves.

## Scope

- All writes under the global memory directories (`~/.claude/projects/*/memory/`, `MEMORY.md`)
- Memory file creation or modification through any tool (Write, Edit, etc.)
- All auto-save guidance from the system prompt's auto memory section
