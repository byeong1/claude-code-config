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

All feedback is delivered via stdout JSON `{"decision": "block", "reason": ...}`
with exit 0, NOT via `exit 2`. This is deliberate: per the Stop-hook spec, `exit
2` writes only to stderr, which is user-visible but is NOT delivered to the
model — so the model never sees the retry instruction and the turn just stalls
(observed in practice). The `decision: "block"` + `reason` form is the supported
way to prevent the stop AND feed model-visible feedback that continues the
conversation automatically.

- **clean response** -> allow stop (no output, exit 0).
- **leak, 1st-2nd in a row** -> `block` + `reason` telling the model to re-issue
  the intended tool call in proper format. The conversation continues and the
  model retries automatically.
- **leak, 3rd in a row** -> `block` + `reason` telling the model to STOP retrying
  and instead output a **session-handoff prompt** (goal, decisions made, work
  done, what remains, exact file paths/commands) as plain text with no tool calls.

`stop_hook_active` is honored on the retry path (1st-2nd leak) to bound the loop:
without it a perpetually-leaking model could be re-invoked forever. The handoff
path (3rd leak) fires regardless, because the handoff response is tool-call-free
and so ends the streak and stops cleanly on the next turn. Empty assistant turns
(tool_use-only turns) interleaved between leaks are skipped when counting the
streak, so they don't reset the count.

## When the hook fires

If you see the retry message: re-issue the tool call you intended, in proper
tool-call format. Do not paste the raw tags as text again.

If you see the handoff message (3rd failure): do not attempt the tool call again.
Write the handoff prompt so the user can continue in a fresh session.
