#!/usr/bin/env python3
"""
toolcall-leak-guard Stop hook.

Detects the failure mode where a model's tool call is not serialized as a real
tool invocation but leaks into the assistant response body as raw text
(`<invoke ...>`, `<parameter ...>`, `</invoke>` ...). The hook fires on Stop,
inspects the last assistant message, and:

  - clean response         -> exit 0 (allow stop)
  - leak, 1st-2nd in a row -> exit 2, tell the model to retry the intended
                              tool call in proper format
  - leak, 3rd in a row     -> exit 2, tell the model to STOP retrying and instead
                              write a session-handoff prompt (no tool calls)

The streak is computed by scanning the transcript backwards over consecutive
assistant turns, so no on-disk counter state is needed.

See `rules/toolcall-leak-guard/RULE.md` for rationale.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MAX_RETRIES = 3

# Code fences (```...```) and inline code (`...`) where tags are quoted for
# explanation, not leaked. Stripped before leak detection to avoid false positives.
CODE_FENCE_PATTERN = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_PATTERN = re.compile(r"`[^`\n]*`")

# Any invoke/parameter tag — opening (<invoke ...) or closing (</invoke>) — that
# survives code-span stripping is a leaked tool call. A real tool call never
# appears as text in the response body, so we don't require a name= attribute or
# a matched open/close pair: a partial/truncated leak (e.g. just `<invoke name=`)
# must still be caught. Quoted tags inside code fences/inline code are stripped
# first (strip_code) so prose that documents these tags isn't flagged.
LEAK_TAG = re.compile(
    r"</?(?:antml:)?(?:invoke|parameter)\b",
    re.IGNORECASE,
)


def strip_code(text: str) -> str:
    """Remove fenced and inline code spans so quoted tags aren't flagged."""
    text = CODE_FENCE_PATTERN.sub("", text)
    text = INLINE_CODE_PATTERN.sub("", text)
    return text


def stringify_content(content) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    parts.append(block.get("text", ""))
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts)
    return ""


def iter_messages(transcript_path: str):
    """Yield (role, text) for each transcript entry, oldest to newest."""
    if not transcript_path or not Path(transcript_path).is_file():
        return
    try:
        with open(transcript_path, "r", encoding="utf-8") as transcript_file:
            lines = transcript_file.readlines()
    except OSError:
        return

    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue

        message = entry.get("message")
        if isinstance(message, dict):
            role = message.get("role")
            content = message.get("content")
        else:
            role = entry.get("role")
            content = entry.get("content")

        yield role, stringify_content(content)


def has_leak(text: str) -> bool:
    if not text:
        return False
    stripped = strip_code(text)
    return bool(LEAK_TAG.search(stripped))


def leak_streak(transcript_path: str) -> int:
    """Count consecutive trailing assistant messages that contain a leak."""
    assistant_texts = [
        text for role, text in iter_messages(transcript_path) if role == "assistant"
    ]
    streak = 0
    for text in reversed(assistant_texts):
        # Empty assistant turns (tool_use-only turns with no text body) are
        # interleaved with leaks in the transcript. Skip them so they don't
        # break the streak — only a real, non-leaking text turn ends it.
        if not text.strip():
            continue
        if has_leak(text):
            streak += 1
        else:
            break
    return streak


RETRY_MESSAGE = (
    "toolcall-leak-guard: Your last response leaked raw tool-call tags "
    "(<invoke>/<parameter>) into the message body as text — the tool call was "
    "NOT executed. Re-issue the intended tool call(s) now in proper tool-call "
    "format. Do not repeat the raw tags as text."
)

HANDOFF_MESSAGE = (
    "toolcall-leak-guard: The tool call has now leaked into the response body "
    f"{MAX_RETRIES} times in a row. STOP retrying the tool call. Instead, write a "
    "concise session-handoff prompt the user can paste into a fresh session: "
    "summarize the current goal, decisions already made, work completed, what "
    "remains, and the exact file paths / commands involved. Do NOT make any tool "
    "calls in this response — output the handoff prompt as plain text only."
)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    # NOTE: we intentionally do NOT early-return on stop_hook_active. This hook's
    # whole purpose is to re-invoke the model (exit 2) until the leak clears, so
    # honoring that flag would disable retries after the first one. The infinite
    # loop is instead bounded by MAX_RETRIES: once the streak hits the cap we ask
    # for a tool-call-free handoff, which is a clean turn that ends the streak.
    transcript_path = payload.get("transcript_path", "")
    streak = leak_streak(transcript_path)

    if streak == 0:
        return 0

    message = HANDOFF_MESSAGE if streak >= MAX_RETRIES else RETRY_MESSAGE
    print(message, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
