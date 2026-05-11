# Ask UI

When asking the user for a decision, prefer the most structured interaction available in the current Codex environment.

Use this order:

1. If a dedicated user-input UI tool is available, use it for discrete choices.
2. If no such tool is available, ask a concise plain-text question.
3. For yes/no confirmations, present the default recommendation and the consequence of each choice.
4. For multiple-choice questions, keep choices mutually exclusive and avoid adding a vague "Other" option unless free-form input is truly needed.

For `work-orchestration` mode selection, always ask and wait. Do not proceed on assumption.

For `work-orchestration`, use this option shape when a structured user-input UI is available:

- Question: `어떤 방식으로 작업을 진행할까요?`
- Header: `Work Mode`
- Options:
  - `Direct (Recommended)` or `Direct`
    - Description: `메인 인스턴스가 모든 파일을 직접 순차 처리합니다`
  - `Sub-agent distribution (Recommended)` or `Sub-agent distribution`
    - Description: `각 에이전트가 담당 파일을 처리하고 의존 파일에 대해 하위 에이전트를 생성합니다`

Put the recommended option first.

For other questions, do not block when a conservative, low-risk assumption is clearly implied by the codebase and the user's request.
