# Work Mode Selection

Present the dependency tree as text output first, then use `AskUserQuestion` to ask the user.

## Recommendation Logic

| Condition | Recommendation |
|-|-|
| **4+ files** to modify OR dependency tree depth **≥ 2** | Sub-agent distribution |
| **2–3 files** to modify AND dependency tree depth **≤ 1** | Direct processing |

Append **(Recommended)** only to the recommended option's label.

## AskUserQuestion Examples

### Sub-agent distribution recommended

```
AskUserQuestion({
  questions: [{
    question: "어떤 방식으로 작업을 진행할까요?",
    header: "Work Mode",
    options: [
      { label: "Sub-agent 분산 처리 (Recommended)", description: "각 에이전트가 담당 파일 수정 후 의존 파일에 대해 하위 에이전트를 생성합니다" },
      { label: "직접 처리", description: "메인 인스턴스가 모든 파일을 직접 순차 수정합니다" }
    ],
    multiSelect: false
  }]
})
```

### Direct processing recommended

```
AskUserQuestion({
  questions: [{
    question: "어떤 방식으로 작업을 진행할까요?",
    header: "Work Mode",
    options: [
      { label: "Sub-agent 분산 처리", description: "각 에이전트가 담당 파일 수정 후 의존 파일에 대해 하위 에이전트를 생성합니다" },
      { label: "직접 처리 (Recommended)", description: "메인 인스턴스가 모든 파일을 직접 순차 수정합니다" }
    ],
    multiSelect: false
  }]
})
```

- **Sub-agent 분산 처리** → Step 3 (recursive distribution)
- **직접 처리** → Main instance handles all work directly
