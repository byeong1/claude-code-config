#!/usr/bin/env python3
"""
memory-discipline PreToolUse hook.

Blocks Write/Edit/MultiEdit/NotebookEdit on memory paths
(`~/.claude/projects/*/memory/*` or any `MEMORY.md` under that tree)
unless the immediately preceding user message contains an explicit
save/delete keyword.

See `rules/memory-discipline/RULE.md` for the rationale and the keyword list.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

KEYWORDS = (
    "memory에 저장",
    "메모리에 저장",
    "기억해",
    "기억해둬",
    "저장해둬",
    "기록해둬",
    "잊지 마",
    "지워",
    "삭제",
    "정리",
    "잊어버려",
    "remember",
    "save to memory",
    "store in memory",
    "memorize",
    "don't forget",
    "forget",
    "remove from memory",
    "delete from memory",
)

HOME = os.path.expanduser("~")
MEMORY_DIR_PATTERN = re.compile(
    rf"^{re.escape(HOME)}/\.claude/projects/[^/]+/memory(/|$)"
)


def is_memory_path(target: str) -> bool:
    if not target:
        return False
    if MEMORY_DIR_PATTERN.match(target):
        return True
    if target.endswith("/MEMORY.md") and "/.claude/projects/" in target:
        return True
    return False


def extract_target_path(tool_name: str, tool_input: dict) -> str:
    if tool_name in ("Write", "Edit", "MultiEdit"):
        return tool_input.get("file_path", "") or ""
    if tool_name == "NotebookEdit":
        return tool_input.get("notebook_path", "") or tool_input.get("file_path", "") or ""
    return ""


def last_user_message_text(transcript_path: str) -> str:
    if not transcript_path or not Path(transcript_path).is_file():
        return ""
    try:
        with open(transcript_path, "r", encoding="utf-8") as transcript_file:
            lines = transcript_file.readlines()
    except OSError:
        return ""

    for line in reversed(lines):
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

        if role != "user":
            continue

        text = stringify_content(content)
        if not text:
            continue
        if is_synthetic_user_text(text):
            return ""
        return text

    return ""


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
                elif block.get("type") == "tool_result":
                    return ""
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts)
    return ""


def is_synthetic_user_text(text: str) -> bool:
    stripped = text.lstrip()
    if stripped.startswith("<system-reminder>"):
        return True
    if stripped.startswith("<command-name>"):
        return True
    if stripped.startswith("<local-command-stdout>"):
        return True
    return False


def has_explicit_keyword(text: str) -> bool:
    if not text:
        return False
    lowered = text.lower()
    for keyword in KEYWORDS:
        needle = keyword.lower()
        if needle in lowered:
            return True
    return False


def emit_block(reason: str) -> None:
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
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

    if not is_memory_path(target):
        return 0

    user_text = last_user_message_text(payload.get("transcript_path", ""))
    if has_explicit_keyword(user_text):
        return 0

    emit_block(
        "memory-discipline: User has not explicitly authorized a save or delete. "
        "Writing to the memory area (~/.claude/projects/*/memory/, MEMORY.md) requires "
        "an explicit keyword in the immediately preceding user message — for example "
        "'기억해', '저장해둬', '지워', 'remember', 'forget'. "
        "Ask the user to confirm before retrying."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
