# Work Orchestration Rule

2+ files need modification or creation → invoke `/work-orchestration` before writing any code.

## Exception: ultracode

When the session is in `ultracode` mode (`/effort ultracode`), do NOT invoke `/work-orchestration`. Multi-agent distribution is handled entirely by the Workflow runtime in that mode — invoking work-orchestration on top of it causes double orchestration. Let ultracode plan and run the workflow instead.
