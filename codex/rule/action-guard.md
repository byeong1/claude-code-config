# Action Guard

For review, verification, cleanup, research, analysis, audit, investigation, or inspection requests, default to read-only work.

Apply this rule when the user uses intent such as:

- 검토, 확인, 정리, 리서치, 분석, 조사, 점검, 살펴, 파악
- review, check, audit, investigate, research, analyze, explore, inspect

Behavior:

1. Report findings first.
2. Do not modify, create, delete, stage, commit, or push files unless the user explicitly asks for action.
3. If the user asks to both inspect and fix, report the intended fix scope before editing.
4. If the requested action is destructive or broad, ask for confirmation.
