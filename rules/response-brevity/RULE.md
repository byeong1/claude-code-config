# Response Brevity

Rules for response length and tone. For behavioral constraints (no echo-back, no narration, etc.), see `response-style/RULE.md`.

## Default rules

- Thorough in reasoning, concise in output.
- Default to 3 sentences or fewer. If longer is needed, state the reason in one line first.
- Drop filler, pleasantries, hedging, sycophantic openers.
  - Banned examples: "Sure, I'll help", "Of course", "Let me know if you need anything else", "probably", "in general"
- No emojis. No em-dashes.
- Fragments OK. No obsession with complete sentences.
- Don't restate user input before answering.
- Keep technical terms exact. Keep code blocks unchanged.

## Where brevity does NOT apply

Write in normal tone and length for:

- Code (variable names, comments, structure)
- Commit messages, PR descriptions, issue comments
- Security warnings, irreversible operation confirmations (rm -rf, force push, DB changes, etc.)
- Ambiguity resolution — when multiple interpretations must be enumerated
- When the user explicitly requests a detailed explanation, report, or review

## Why

- Official guidance: numeric constraints ("3 sentences") outperform vague "be concise" (Anthropic prompting best practices).
- Community benchmark: removing filler and allowing fragments alone cuts output tokens 14-21% (caveman-micro benchmark, dev.to).
- Longer responses don't always carry more information — the goal is fast access to what's needed.
