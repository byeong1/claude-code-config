#!/usr/bin/env python3
"""
cleanup-tmp hook.

Manages `~/.claude/tmp/<session_id>/` — a per-session scratch area that skills
may use for transient artifacts. Three dispatched behaviors based on the
incoming hook event:

- SessionStart (source = startup | resume):
    Create this session's folder + PID lockfile, then sweep orphan folders
    whose recorded PID is no longer alive (kill -0 check).
- SessionStart (source = clear):
    Wipe this session's folder contents but keep the folder and .pid file.
- Stop:
    Delete this session's folder outright.

See `rules/` for the broader configuration context.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

TMP_ROOT = Path.home() / ".claude" / "tmp"
PID_FILENAME = ".pid"


def session_dir(session_id: str) -> Path:
    return TMP_ROOT / session_id


def write_pid_lockfile(directory: Path) -> None:
    (directory / PID_FILENAME).write_text(str(os.getpid()), encoding="utf-8")


def read_pid(directory: Path) -> int | None:
    pid_file = directory / PID_FILENAME
    if not pid_file.is_file():
        return None
    try:
        return int(pid_file.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return None


def is_process_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    if sys.platform == "win32":
        return _is_process_alive_windows(pid)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


def _is_process_alive_windows(pid: int) -> bool:
    import ctypes

    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    STILL_ACTIVE = 259
    kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
    handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not handle:
        return False
    try:
        exit_code = ctypes.c_ulong()
        ok = kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code))
        return bool(ok) and exit_code.value == STILL_ACTIVE
    finally:
        kernel32.CloseHandle(handle)


def sweep_orphans(self_session_id: str) -> None:
    if not TMP_ROOT.is_dir():
        return
    for entry in TMP_ROOT.iterdir():
        if not entry.is_dir():
            continue
        if entry.name == self_session_id:
            continue
        pid = read_pid(entry)
        if pid is not None and is_process_alive(pid):
            continue
        try:
            shutil.rmtree(entry)
        except OSError:
            continue


def handle_session_start_normal(session_id: str) -> None:
    TMP_ROOT.mkdir(parents=True, exist_ok=True)
    directory = session_dir(session_id)
    directory.mkdir(parents=True, exist_ok=True)
    write_pid_lockfile(directory)
    sweep_orphans(session_id)


def handle_session_start_clear(session_id: str) -> None:
    directory = session_dir(session_id)
    if not directory.is_dir():
        directory.mkdir(parents=True, exist_ok=True)
        write_pid_lockfile(directory)
        return
    for entry in directory.iterdir():
        if entry.name == PID_FILENAME:
            continue
        try:
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry)
            else:
                entry.unlink()
        except OSError:
            continue
    write_pid_lockfile(directory)


def handle_stop(session_id: str) -> None:
    directory = session_dir(session_id)
    if not directory.is_dir():
        return
    shutil.rmtree(directory, ignore_errors=True)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    session_id = payload.get("session_id") or ""
    if not session_id:
        return 0

    event = payload.get("hook_event_name", "")

    try:
        if event == "SessionStart":
            source = payload.get("source", "")
            if source == "clear":
                handle_session_start_clear(session_id)
            else:
                handle_session_start_normal(session_id)
        elif event == "Stop":
            handle_stop(session_id)
    except OSError as error:
        print(f"cleanup-tmp: {event} failed: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
