# Verification Pass (Step 6)

Mode-dependent verification of the change-set against Step 2's acceptance criteria (after Step 5 reconciliation).

## Mode Selection

```
Sub-agent mode + any risk item   → Full Verification (work-verifier sub-agent)
Sub-agent mode + zero risk items → Lightweight Verification (main self-check)
Direct mode    + any risk item   → Full Verification (work-verifier sub-agent)
Direct mode    + zero risk items → Skip
```

Rationale for Direct + risk → sub-agent: a fresh-context verifier avoids inheriting the same reasoning errors the main instance just made. Risk items always get an independent eye, regardless of execution mode.

If skipped, output a single line: `Step 6: skipped (Direct mode, no risk items)`. Do NOT silently omit Step 6.

## Full Verification (any mode + risk items)

Spawn a `work-verifier` sub-agent with this prompt template:

```
Acceptance criteria:
<paste Step 2 block verbatim (post Step 5 reconciliation)>

Change-set:
- <file 1>: <created | modified | deleted>
- <file 2>: ...

Risk items to verify (one check per item):
<for each risk item from Step 2, list the specific check>
- Deletion of <path>: grep for any remaining import/usage of removed symbols
- Rename of <old_name> → <new_name>: grep for stale references to old_name
- Export removal of <symbol> from <file>: grep for imports of symbol
- API signature change of <fn>: grep callers, verify each updated
- Schema/migration change: list affected modules

Required checks:
1. For each risk item: run the specific check, report count and locations
2. Confirm "Out of scope" items in acceptance criteria were not modified

Output format:
PASS  | <check name> | <evidence (count, command output, etc.)>
FAIL  | <check name> | <what was found and where>
SKIP  | <check name> | <why>

End with: VERDICT: PASS | FAIL | NEEDS_USER_REVIEW
```

Work-verifier is a fresh-context sub-agent — it has not seen the work being verified. This is intentional: it cannot inherit the same reasoning errors that produced the change-set.

## Lightweight Verification (Sub-agent mode, zero risk items)

Main instance performs in its own context:

1. **Re-read acceptance criteria** — output the Step 2 block to refresh attention
2. **For each risk item**: run the specific check inline (grep, file existence, etc.)
3. **Confirm out-of-scope items not touched** — `git diff --stat` or equivalent

Report in the same `PASS | FAIL | SKIP` format as Full Verification.

## Handling FAIL

If any check returns FAIL:

1. Stop. Do NOT proceed to "task complete" framing.
2. Report all failures to the user with the verification output.
3. Propose remediation (rollback, fix-forward, scope adjustment).
4. Use `AskUserQuestion` per the `ask-ui` rule for the user's decision.

Never silently fix a FAIL and re-run verification — surface it first.

## Handling NEEDS_USER_REVIEW

Used when a check is ambiguous (e.g., dynamic call patterns that grep cannot fully resolve). Surface the specific concern and let the user judge.

## Output Discipline

After Step 6 completes (or is skipped), produce a single consolidated summary that includes:

- The Step 5 result tree (what changed, with any Step 2 reconciliation noted)
- The Step 6 verification verdict and evidence
- Any FAIL or NEEDS_USER_REVIEW items prominently flagged

Do not bury verification results inside the change summary — they are the most important output of the orchestration.
