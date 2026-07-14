# Action Guard

When the user requests review, verification, cleanup, research, or any investigative action:

1. **MUST** run `ToolSearch({ query: "select:AskUserQuestion" })` to fetch the tool schema first.
2. **MUST** use `AskUserQuestion` to ask the user before starting the work:

```
AskUserQuestion({
  questions: [{
    question: "작업 방식을 선택해주세요.",
    header: "Action Guard",
    options: [
      { label: "결과만 보고", description: "검토/확인/리서치 결과만 보고하고, 파일 수정이나 생성은 하지 않습니다" },
      { label: "바로 수정 진행", description: "검토 후 발견된 사항을 즉시 수정/생성/적용합니다" }
    ],
    multiSelect: false
  }]
})
```

3. If the user selects "결과만 보고": report findings only. Do NOT modify, create, or delete any files. Wait for the user to explicitly request modifications.
4. If the user selects "바로 수정 진행": proceed with modifications after reporting findings.

**Trigger keywords**: 검토, 확인, 정리, 리서치, 분석, 조사, 점검, 살펴, 파악, review, check, audit, investigate, research, analyze, explore, inspect

**Non-trigger — information questions**: this guard applies to *work requests* only. If the user's message is a question asking for information or validation ("이 방식으로 확인하면 되나요?", "어떤 문제로 보이나요?"), answer it directly — do NOT fire the guard, even when the message contains a trigger keyword. See the `user-intent` rule.
