---
paths:
  - "**/*.{ts,tsx,js,jsx,mjs,cjs,vue,svelte,py,rb,go,rs,java,kt,c,cc,cpp,h,hpp,cs,php,swift,sql,sh,bash}"
---

# Editing Discipline

Applies while writing or modifying code. Loaded only when a code file is in play.

## 1. Self-Check Code Volume

After writing code, ask: "Could this be half the size?" If yes, rewrite before
showing it.

- The system prompt forbids *adding* unnecessary abstractions; this rule
  additionally requires *shrinking* what was already written.
- Concrete trigger: 200 lines that could be 50 → rewrite.

## 2. Don't Touch Adjacent Code

When editing a file, modify only what the task requires. Leave neighboring code,
comments, and formatting alone — even if you'd write them differently.

- No "while I'm here" cleanup of unrelated code.
- No silent style/formatting changes to lines you didn't need to touch.
- Match the file's existing style even if it conflicts with your preference.
- **This rule overrides global `coding-convention/*` rules.** When a file or
  project already has an established style, follow it instead of the global
  convention. Global conventions apply only to new files or solo projects with no
  prior style.

## 3. Dead Code Cleanup Scope

Remove imports/variables/functions that **your changes** rendered unused. Do NOT
remove pre-existing dead code unless the user asked.

- If you spot unrelated dead code, mention it in your response — don't delete it.
- The system prompt allows deleting unused code; this rule narrows the scope to
  "orphans created by this change."
