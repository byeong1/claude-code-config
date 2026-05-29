# Coding Discipline

These rules sharpen behaviors that the system prompt already encourages but does not enforce strongly enough. They apply to all coding tasks, not just exploratory questions.

## 1. Surface Interpretations — Don't Pick Silently

If the user's request has multiple plausible interpretations, list them and ask. Do NOT pick one quietly and proceed.

- Applies even when the request is phrased as a command ("add validation", "fix the bug"). The system prompt's "present a recommendation with tradeoffs" rule covers exploratory questions only.
- Format: name each interpretation in one line, then ask which one.
- Use `AskUserQuestion` per the `ask-ui` rule, not plain text.

## 2. Push Back on Suboptimal Approaches

If the user has already decided on an approach but you see a meaningfully simpler/safer/correct path, say so in one or two sentences before implementing. Don't comply silently with a worse plan.

- Frame as a short proposal, not a lecture. The user can override.
- Skip this for trivial style/preference choices — only push back when it materially affects correctness, complexity, or maintenance.
- When the user must decide between approaches, use `AskUserQuestion` per the `ask-ui` rule.

## 3. Stop on Ambiguity

If something is unclear mid-task, stop. Name what's confusing in one sentence. Ask. Do NOT pick a plausible-looking interpretation and continue.

- This is the catch-all when interpretations aren't even crisp enough to enumerate (rule 1 covers the case where you can list them).
- Bias: "I'll just assume X" is exactly the moment to stop.

## 4. Self-Check Code Volume

After writing code, ask: "Could this be half the size?" If yes, rewrite before showing it.

- The system prompt forbids *adding* unnecessary abstractions; this rule additionally requires *shrinking* what was already written.
- Concrete trigger: 200 lines that could be 50 → rewrite.

## 5. Don't Touch Adjacent Code

When editing a file, modify only what the task requires. Leave neighboring code, comments, and formatting alone — even if you'd write them differently.

- No "while I'm here" cleanup of unrelated code.
- No silent style/formatting changes to lines you didn't need to touch.
- Match the file's existing style even if it conflicts with your preference.
- **This rule overrides global `coding-convention/*` rules.** When a file or project already has an established style, follow it instead of the global convention. Global conventions apply only to new files or solo projects with no prior style.

## 6. Dead Code Cleanup Scope

Remove imports/variables/functions that **your changes** rendered unused. Do NOT remove pre-existing dead code unless the user asked.

- If you spot unrelated dead code, mention it in your response — don't delete it.
- The system prompt allows deleting unused code; this rule narrows the scope to "orphans created by this change."

## 7. Multi-Step Tasks Need Per-Step Verify

For tasks with 3+ steps, state each step with its verification check before executing.

```
1. <step> → verify: <how you'll know it worked>
2. <step> → verify: <...>
3. <step> → verify: <...>
```

- Verify is concrete: a command output, a file diff, a passing test, a visible UI state. Not "looks right."
- Skip for single-step or trivial tasks — keep it proportional (response-style/RULE.md still applies).
- This does not require writing tests first; it requires knowing in advance what "done" looks like for each step.
