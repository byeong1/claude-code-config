# Execution

How to run a task: verifying multi-step work, and deciding what to delegate.

## Multi-step tasks need per-step verify

For tasks with 3+ steps, state each step with its verification check before
executing.

```
1. <step> → verify: <how you'll know it worked>
2. <step> → verify: <...>
3. <step> → verify: <...>
```

- Verify is concrete: a command output, a file diff, a passing test, a visible UI
  state. Not "looks right."
- Skip for single-step or trivial tasks — keep it proportional (the `response`
  rule still applies).
- This does not require writing tests first; it requires knowing in advance what
  "done" looks like for each step.

## Delegating to subagents

**Single-file or non-code tasks:**

- Under ~50k context: prefer inline work for tasks under ~5 tool calls.
- Over ~50k context: prefer subagents for self-contained tasks, even simple ones
  — the per-call token tax on large contexts adds up fast.

**Multi-file code modifications:**

- Defer to the `work-orchestration` rule, which handles user prompting and mode
  selection.
- Sub-agents invoked by work-orchestration MUST still follow the output rules
  below.

**Output rules for all sub-agents:**

- Include in every sub-agent prompt: "Final response under 2000 characters. List
  outcomes, not process."
- Never call TaskOutput twice for the same subagent. If it times out, increase
  the timeout — don't re-read.
