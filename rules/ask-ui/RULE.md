# Ask via UI

**Default rule**: When asking the user *anything* that requires a response, use `AskUserQuestion` — not plain text. The user should be able to respond with a single click in the vast majority of cases.

This applies to:
- Yes/no confirmations ("proceed with X?", "would you like to Y?")
- Multiple-choice questions ("A / B / C 중에?")
- Questions where you expect *some* free-form answer is possible — `AskUserQuestion` automatically provides an "Other" option for custom text input. **Do NOT fall back to plain text just because the answer might be open-ended.**

The only acceptable exceptions:
- Pure information requests where there are no discrete options to present (e.g., "paste the error log").
- Questions embedded inside an analysis/report where the user is expected to redirect freely, not pick from options.

**Answer before asking** (see `user-intent` rule): if the user's message is itself a question ("~하면 되나요?", "이게 맞나요?"), answer it in plain text FIRST. This rule governs *how* to ask, not *whether* to ask — it never justifies replacing an answer with a question. Use `AskUserQuestion` only if a genuine decision remains after the answer. Never respond to a question with only a question.

When in doubt, use `AskUserQuestion`. Plain-text questions are the exception, not the default.

## How to call

Before calling, run `ToolSearch({ query: "select:AskUserQuestion" })` to fetch the tool schema if not already loaded.

For yes/no confirmations:

```
AskUserQuestion({
  questions: [{
    question: "<what you're proposing to do next>",
    header: "Confirm",
    options: [
      { label: "진행", description: "제안된 작업을 진행합니다" },
      { label: "중단", description: "작업을 진행하지 않습니다" }
    ],
    multiSelect: false
  }]
})
```

For multiple-choice or partially open-ended questions:

```
AskUserQuestion({
  questions: [{
    question: "<the question>",
    header: "<short label>",
    options: [
      { label: "<option A>", description: "<what this means>" },
      { label: "<option B>", description: "<what this means>" },
      { label: "<option C>", description: "<what this means>" }
    ],
    multiSelect: false
  }]
})
```

The user can always select "Other" to provide custom instructions, so only list the discrete options you actually want to surface. Do not add an "Other" or "직접 입력" option yourself — it is provided automatically by the tool.
