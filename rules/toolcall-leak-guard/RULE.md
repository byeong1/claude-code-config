# Tool-call Leak Guard

A `Stop` hook (`hooks/toolcall-leak-guard.py`) detects responses where a tool
call leaked into the message body as raw text (`<invoke>` / `<parameter>` /
`</invoke>`) instead of being executed, and drives recovery.

## Why

This is a model/harness serialization failure, not a behavior the model can
prevent by being more careful. When it happens the tool never runs and the turn
ends silently. The hook is the only deterministic place to catch it — hooks fire
on real events, and `Stop` is the one event that sees the finished response body.

## Behavior

The hook scans the transcript backwards over consecutive assistant turns and
counts the leak streak (no on-disk counter needed):

- **clean response** -> allow stop.
- **leak, 1st-2nd in a row** -> `exit 2` + message telling the model to re-issue
  the intended tool call in proper format. This does not stop the turn; the model
  is re-invoked and retries automatically.
- **leak, 3rd in a row** -> `exit 2` + message telling the model to STOP retrying
  and instead output a **session-handoff prompt** (goal, decisions made, work
  done, what remains, exact file paths/commands) as plain text with no tool calls.

`stop_hook_active` is honored to avoid infinite Stop loops.

## When the hook fires

If you see the retry message: re-issue the tool call you intended, in proper
tool-call format. Do not paste the raw tags as text again.

If you see the handoff message (3rd failure): do not attempt the tool call again.
Write the handoff prompt so the user can continue in a fresh session.
