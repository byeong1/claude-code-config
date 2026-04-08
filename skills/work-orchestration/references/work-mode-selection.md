# Work Mode Selection

**IMPORTANT:** Before presenting options, MUST run `ToolSearch({ query: "select:AskUserQuestion" })` to fetch the tool schema. Do NOT substitute with plain text questions.

Present the dependency tree as text output first, then use `AskUserQuestion` to ask the user.

## Recommendation Logic

Recommend based on Step 1 dependency analysis results. Follow the table strictly — do NOT override based on perceived task simplicity.

| Condition | Recommendation |
|-|-|
| **2–3 files** AND depth ≤ 1 AND work per file is small relative to sub-agent overhead | Direct processing |
| All other **2+ files** cases (including simple file creation) | Sub-agent distribution |

**Direct processing requires ALL three conditions to be true.** If file count is 4+, always recommend Sub-agent regardless of task complexity.

Append **(Recommended)** only to the recommended option's label. **The recommended option MUST be the first option in the list.** Use the exact AskUserQuestion format below — do NOT alter labels, descriptions, or add custom options.

## AskUserQuestion Examples

### Sub-agent distribution recommended

```
AskUserQuestion({
  questions: [{
    question: "어떤 방식으로 작업을 진행할까요?",
    header: "Work Mode",
    options: [
      { label: "Sub-agent (Recommended)", description: "각 에이전트가 담당 파일을 처리하고 의존 파일에 대해 하위 에이전트를 생성합니다" },
      { label: "Direct", description: "메인 인스턴스가 모든 파일을 직접 순차 처리합니다" }
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
      { label: "Direct (Recommended)", description: "메인 인스턴스가 모든 파일을 직접 순차 처리합니다" },
      { label: "Sub-agent", description: "각 에이전트가 담당 파일을 처리하고 의존 파일에 대해 하위 에이전트를 생성합니다" }
    ],
    multiSelect: false
  }]
})
```

- **Sub-agent** → Step 3 (recursive distribution)
- **Direct** → Main instance handles all work directly
- **Other (user free text)** → Apply the user's input (e.g., dependency change, scope change, naming request), then return to Step 1 if scope/dependency changed, or re-run Step 2 to ask for mode selection again. A mode has NOT been selected — do NOT proceed to Step 3 without a mode choice.
