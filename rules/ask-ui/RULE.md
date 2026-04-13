# Ask via UI

When asking the user a yes/no confirmation about the next action (e.g., "proceed with X?", "would you like to Y?"), do NOT use plain text. Use `AskUserQuestion` so the user can respond with a single click.

Before calling, run `ToolSearch({ query: "select:AskUserQuestion" })` to fetch the tool schema if not already loaded.

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

The user can always select "Other" to provide custom instructions, so only "진행" and "중단" are needed as options.
