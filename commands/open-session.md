## Open Session

새 터미널 창에 독립적인 Claude Code 대화형 세션을 띄웁니다. 띄운 세션은
`SendMessage`로 주소 지정이 가능한 별개 세션이 됩니다.

### Procedure

1. 세션 이름을 결정한다.
   - 인자로 이름이 주어졌으면 그대로 사용한다.
   - 없으면 작업 맥락에서 유추한 kebab-case 이름을 제안하고 `AskUserQuestion`으로 확인받는다.
2. 대상 저장소 경로를 결정한다. 기본값은 현재 작업 디렉터리.
3. 플랫폼을 확인하고(win32 / darwin / linux) 해당 분기의 명령을 실행한다.
4. 실행 후 `ListAgents`로 새 세션이 주소 목록에 나타나는지 확인한다.
   - 즉시 나타나지 않을 수 있다. 세션 부팅에 몇 초 걸리므로 한 번 재확인한다.
   - 끝내 나타나지 않으면 새 창의 `/status`에서 inbox 소켓 바인딩 여부를 확인하도록 사용자에게 안내한다.

### Launch commands

공통 환경변수와 인자:

- `CLAUDE_CODE_CHILD_SESSION=` (빈 값) — 부모 세션 종속 해제
- `CLAUDE_CODE_FORCE_SESSION_PERSISTENCE=1` — 세션 영속화 강제
- `claude -n <이름> --permission-mode auto`

**win32 (PowerShell)**

```powershell
Start-Process cmd.exe -ArgumentList '/k','cd /d <저장소> && set CLAUDE_CODE_CHILD_SESSION= && set CLAUDE_CODE_FORCE_SESSION_PERSISTENCE=1 && claude -n <이름> --permission-mode auto'
```

**darwin (Terminal.app)**

```bash
osascript -e 'tell application "Terminal" to do script "cd <저장소> && CLAUDE_CODE_CHILD_SESSION= CLAUDE_CODE_FORCE_SESSION_PERSISTENCE=1 claude -n <이름> --permission-mode auto"' -e 'tell application "Terminal" to activate'
```

iTerm2를 쓰는 환경이면 `tell application "iTerm"` → `create window with default profile` →
`write text "<명령>"` 형태로 대체한다.

**linux**

사용 가능한 터미널 에뮬레이터를 순서대로 탐색하여 첫 번째로 존재하는 것을 쓴다.

```bash
CMD='cd <저장소> && CLAUDE_CODE_CHILD_SESSION= CLAUDE_CODE_FORCE_SESSION_PERSISTENCE=1 claude -n <이름> --permission-mode auto; exec $SHELL'
gnome-terminal -- bash -lc "$CMD"      # 또는
konsole -e bash -lc "$CMD"             # 또는
xfce4-terminal -e "bash -lc '$CMD'"    # 또는
x-terminal-emulator -e bash -lc "$CMD"
```

전부 없으면 사용자에게 수동 실행용 명령 문자열을 출력하고 종료한다.

### Rules

- **subagent로 띄우지 않는다.** `Agent` 도구로 생성한 세션은 부모 대화에 종속되어
  다른 세션이 `SendMessage`로 주소 지정할 수 없다. 반드시 새 터미널 프로세스여야 한다.
- **`--permission-mode`를 생략하지 않는다.** 생략하면 새 세션이 첫 권한 프롬프트에서
  멈춘 채 아무도 보지 않는 창에서 대기한다.
- **세션 확인은 `ListAgents`로 한다.** `claude agents`는 백그라운드 세션 뷰라
  이렇게 띄운 대화형 세션이 나타나지 않는다. 여기서 안 보인다고 "불가능"으로
  결론내지 말 것.
- `CLAUDE_CODE_CHILD_SESSION` / `CLAUDE_CODE_FORCE_SESSION_PERSISTENCE`는
  공식 문서에 없는 미문서화 변수다. CLI 버전업 시 동작이 바뀔 수 있으므로,
  세션이 예상대로 뜨지 않으면 이 둘을 먼저 의심한다.
