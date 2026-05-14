# Acceptance Criteria (Step 2)

Define what "done" looks like *after Step 1's dependency analysis, before mode selection and execution*. These criteria become the contract sub-agents must satisfy and the checklist Step 6 verifies against.

## Required Output Format

Produce a single block with these four sections. Keep each line short — this becomes part of every sub-agent's prompt and the verification input.

```
Goal: <one-sentence summary of the work>

Required outcomes:
- <observable result 1>
- <observable result 2>

Risk items (must verify in Step 6):
- <risk 1>
- <risk 2>

Out of scope (do not touch):
- <thing 1>
- <thing 2>
```

## What Counts as a Risk Item

Mark as a risk item if the work includes any of:

- File deletion
- Function / class / variable rename
- `export` removal or change
- Public API signature change
- Dependency (import) removal
- Database schema or migration change
- Config-key removal or rename

Risk items determine whether Step 6 runs in Full or Lightweight mode. A change-set with zero risk items in Direct mode skips Step 6.

## Required Outcomes — Be Concrete

Bad:
- "Refactor the OMR module"
- "Clean up dead code"

Good:
- "All `IPCScannerResultServiceHandler` references removed from `core/index.ts` and the file is deleted"
- "`extract_marking_answers` is callable from `omr_service.py` after the rename"

Required outcomes must be **observable** — checkable by grep, typecheck, or file existence. "Looks cleaner" is not an outcome.

## Out of Scope — Defensive Boundary

List anything a sub-agent might be tempted to touch but must not. Examples:

- "Do not modify `result_management_service.py` — used by other modules"
- "Do not change Python files; this is a TS-only refactor"
- "Do not touch test fixtures"

This block is the most effective defense against the "while I'm here" cleanup that breaks unrelated code.

## When to Re-evaluate

Re-run Step 2 if any of these happen during execution:

- Sub-agent surfaces a dependency you did not anticipate
- User redirects the goal mid-work
- A risk item is added or removed (Step 6 mode may change)

Do NOT proceed past Step 5 with stale acceptance criteria. Step 5 explicitly reconciles actual changes against this block and feeds Step 2 updates back here when drift is detected.
