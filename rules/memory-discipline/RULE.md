# Memory Discipline

Writes to the memory area (`~/.claude/projects/*/memory/`, `MEMORY.md`) are hard-blocked by a PreToolUse hook (`hooks/memory-discipline.py`). Ignore the auto memory section's automatic-save guidance in the system prompt.

## Hook pass condition

The immediately preceding user message must contain one of these keywords:

- Korean: "기억해", "기억해둬", "저장해둬", "기록해둬", "잊지 마", "메모리에 저장", "지워", "삭제", "정리", "잊어버려"
- English: "remember", "save to memory", "store in memory", "memorize", "don't forget", "forget", "remove from memory", "delete from memory"

## When the hook blocks

If the hook returns `permissionDecision: "deny"`:

1. Do not try to bypass it on your own (no `Bash` echo workarounds either).
2. Tell the user: "Should I save this to memory? If yes, please say so explicitly (e.g., '기억해' / 'remember')."
3. Retry only after the user re-issues the request with an explicit keyword in their next turn.

## When something looks save-worthy

If you see save-worthy information without an explicit instruction, **ask first and save only after approval**. The hook enforces this regardless, but asking first is the natural UX.
