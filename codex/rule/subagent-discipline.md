# Subagent Discipline

Use subagents only when they materially improve the work.

Prefer inline work when:

- the task is small,
- the next local step depends immediately on the result,
- the files are tightly coupled,
- the coordination overhead is larger than the work.

Prefer subagents when:

- exploration can run in parallel,
- independent files or modules have disjoint write ownership,
- verification can run while implementation continues,
- context is large and a self-contained side task can be isolated.
- recursive dependency-tree distribution is required by the `work-orchestration` skill and the current runtime permits it.

For every subagent prompt:

- State exact file or module ownership.
- State whether the agent is read-only or may edit files.
- Tell the agent that other agents may be working in the codebase.
- Tell the agent not to revert others' edits.
- State whether the agent may spawn child agents for downstream dependents.
- Ask for outcomes, changed paths, verification performed, and blockers.

Do not ask two agents to edit the same file unless the user explicitly accepts the conflict risk.
