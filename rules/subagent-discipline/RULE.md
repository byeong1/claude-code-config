# Subagent Discipline

**Context-aware delegation (single-file or non-code tasks):**
 - Under ~50k context: prefer inline work for tasks under ~5 tool calls.
 - Over ~50k context: prefer subagents for self-contained tasks, even simple ones — the per-call token tax on large contexts adds up fast.

**Multi-file code modifications:**
 - Defer to the work-orchestration rule. That rule handles user prompting and mode selection.
 - When work-orchestration invokes sub-agents, those sub-agents MUST still follow this discipline's output rules below.

**Output rules for all sub-agents:**
 - Include in every sub-agent prompt: "Final response under 2000 characters. List outcomes, not process."
 - Never call TaskOutput twice for the same subagent. If it times out, increase the timeout — don't re-read.
