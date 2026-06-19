#!/usr/bin/env python3
"""
convention-review PostToolUse hook.

After a Write/Edit/MultiEdit/NotebookEdit on a *code* file succeeds, inject an
`additionalContext` reminder telling the model to re-review the file it just
wrote against the coding-convention rules and fix any violations.

This is a post-write nudge, not a hard block. PostToolUse fires AFTER the write
completes, so it cannot prevent a write — it can only feed the model a follow-up
instruction. Naming-convention rules (e.g. "iterate `users` as `user`,
not `row`/`a`/`b`") are semantic and cannot be reliably caught by a regex, so
the judgement is delegated back to the model.

See `rules/coding-convention/general/RULE.md` for the rules being enforced.
"""

from __future__ import annotations

import json
import os
import sys

# Extensions that the coding-convention rules apply to. Non-code files
# (docs, config, data) are skipped so the reminder does not fire on every save.
CODE_EXTENSIONS = (
    ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs",
    ".py", ".rb", ".go", ".rs", ".java", ".kt",
    ".c", ".cc", ".cpp", ".h", ".hpp", ".cs",
    ".php", ".swift", ".vue", ".svelte",
)

REVIEW_INSTRUCTION = (
    "convention-review: You just wrote to a code file. Before doing anything "
    "else, re-read the changed region of this file and check it against the "
    "coding-convention rules (rules/coding-convention/general/RULE.md). "
    "Pay special attention to: (1) collection iteration must use the SINGULAR "
    "form of the collection name as the callback argument — `users.map(user => …)`, "
    "NOT `row`, `item`, `a`, `b`, or any generic/short name; "
    "(2) no double negation (prefer `every` over `some(=> !…)`); "
    "(3) boolean variables use is/has/should/can prefixes; "
    "(4) no abbreviations or reserved words (data/value/item/result) as names; "
    "(5) no magic numbers/strings. "
    "If you find a violation, fix it now with Edit. If the file is clean, do "
    "nothing and continue."
)


def extract_target_path(tool_name: str, tool_input: dict) -> str:
    if tool_name in ("Write", "Edit", "MultiEdit"):
        return tool_input.get("file_path", "") or ""
    if tool_name == "NotebookEdit":
        return tool_input.get("notebook_path", "") or tool_input.get("file_path", "") or ""
    return ""


def is_code_file(target: str) -> bool:
    if not target:
        return False
    _, ext = os.path.splitext(target)
    return ext.lower() in CODE_EXTENSIONS


def emit_review(target: str) -> None:
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": f"{REVIEW_INSTRUCTION}\n\nFile: {target}",
        }
    }
    print(json.dumps(output, ensure_ascii=False))


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {}) or {}
    target = extract_target_path(tool_name, tool_input)

    if not is_code_file(target):
        return 0

    emit_review(target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
