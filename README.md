# Claude Code Config

Claude Code CLI를 위한 개인 설정 파일 모음입니다. 여러 환경(Mac/Windows/데스크탑)에서 동일한 Claude Code 경험을 제공하기 위한 하네스 설정 저장소입니다.

## 구조

| 경로 | 목적 |
|-|-|
| `rules/` | 모든 작업에 횡단 적용되는 행동 규칙 |
| `skills/` | 재사용 가능한 워크플로 단위 |
| `commands/` | 슬래시 커맨드 정의 |
| `agents/` | 서브에이전트 정의 |
| `settings.json` | Claude Code 런타임 설정 |
| `DECISIONS.md` | 의식적으로 배제한 항목과 이유 |
| `AUDIT.md` | 하네스 환경 자가 검토용 프롬프트 모음 |

## 전제

- 본 설정은 `~/.claude/` 디렉토리에 로드되는 것을 전제로 합니다.
- Claude Code CLI가 설치되어 있어야 합니다.
- 최초 1회는 저장소를 clone한 후 동기화 절차를 수행해야 합니다.

## 동기화 전략

본 저장소는 **symlink** 기반으로 동기화합니다. 저장소의 디렉토리/파일을 `~/.claude/`로 연결해두면 `git pull` 한 번으로 모든 머신에 즉시 반영됩니다.

## 설치 — 최초 clone

### 1. 저장소 clone

원하는 경로에 clone합니다. 본 예시는 `~/code/claude-code-config`을 사용합니다.

**macOS / Linux**

```bash
git clone git@github.com:byeong1/claude-code-config.git ~/code/claude-code-config
```

**Windows (PowerShell)**

```powershell
git clone git@github.com:byeong1/claude-code-config.git $env:USERPROFILE\code\claude-code-config
```

### 2. 기존 `~/.claude/` 백업

기존 `~/.claude/` 디렉토리에 설정 파일이 있다면 백업합니다. Symlink는 기존 파일/디렉토리를 덮어쓸 수 없습니다.

**macOS / Linux**

```bash
mv ~/.claude/rules         ~/.claude/rules.bak         2>/dev/null
mv ~/.claude/skills        ~/.claude/skills.bak        2>/dev/null
mv ~/.claude/commands      ~/.claude/commands.bak      2>/dev/null
mv ~/.claude/agents        ~/.claude/agents.bak        2>/dev/null
mv ~/.claude/settings.json ~/.claude/settings.json.bak 2>/dev/null
```

**Windows (PowerShell)**

```powershell
$claude = "$env:USERPROFILE\.claude"
foreach ($name in @('rules','skills','commands','agents','settings.json')) {
    $path = Join-Path $claude $name
    if (Test-Path $path) { Rename-Item $path "$name.bak" }
}
```

### 3. Symlink 생성 — 일상 동기화

각 머신(macOS/Windows)에서 직접 아래 명령을 실행해 저장소의 디렉토리/파일을 `~/.claude/`로 symlink 연결합니다. symlink 자체는 git에 담기지 않으므로 **머신마다 1회씩 수동으로 만들어야 합니다.**

**macOS / Linux**

```bash
cd ~/code/claude-code-config
ln -s "$PWD/rules"         ~/.claude/rules
ln -s "$PWD/skills"        ~/.claude/skills
ln -s "$PWD/commands"      ~/.claude/commands
ln -s "$PWD/agents"        ~/.claude/agents
ln -s "$PWD/settings.json" ~/.claude/settings.json
```

**Windows (관리자 권한 PowerShell)**

```powershell
$src = "$env:USERPROFILE\code\claude-code-config"
$dst = "$env:USERPROFILE\.claude"

foreach ($name in @('rules','skills','commands','agents','settings.json')) {
    New-Item -ItemType SymbolicLink -Path "$dst\$name" -Target "$src\$name" | Out-Null
}
```

> Windows는 symlink 생성에 관리자 권한이 필요합니다. 개발자 모드만 켜져 있어도 일부 환경에서는 권한이 부여되지 않으므로, 시작 메뉴에서 PowerShell을 우클릭 → "관리자 권한으로 실행"으로 여는 것이 가장 확실합니다.

### 4. 설치 검증

Claude Code 세션을 새로 열고 다음을 확인합니다.

- 규칙이 반영되었는지 (예: 검토 요청 시 `interaction` 규칙의 action guard가 발동하는지)
- 스킬이 목록에 뜨는지
- 슬래시 커맨드가 작동하는지 (`/follow-up`, `/commit` 등)

## 일상 사용 — 업데이트와 동기화

### 다른 머신에서 푸시한 변경 가져오기

Symlink가 연결되어 있으므로 `git pull` 한 번으로 끝납니다.

```bash
cd ~/code/claude-code-config
git pull
```

이후 Claude Code 세션을 재시작하면 새 규칙·스킬이 반영됩니다.

### 로컬에서 규칙을 수정하고 다른 머신에 공유

Symlink로 연결되어 있으므로 `~/.claude/rules/...` 또는 `~/code/claude-code-config/rules/...` **어디서 수정하든 같은 파일**입니다. 일반적인 git 워크플로를 따릅니다.

```bash
cd ~/code/claude-code-config
git status                    # 변경사항 확인
git add rules/some-rule/RULE.md
git commit -m "..."
git push
```

## 설계 철학

본 저장소는 다음 원칙을 따릅니다.

1. **단순성 우선** — 규칙·스킬을 무분별하게 늘리지 않음. 모델이 이미 잘 하는 것은 규칙으로 만들지 않음
2. **가정의 명시성** — 모든 구성 요소는 "모델이 이것을 혼자 못 한다"는 가정을 전제로 함. 그 가정을 주기적으로 재평가함
3. **배제의 기록** — 도입하지 않기로 한 결정도 문서화함
4. **외부 도구 선호** — 결정론적 검증(린터, 타입체커)이 가능하면 규칙보다 hooks로 연결

설계 배경과 배제한 항목은 [`DECISIONS.md`](DECISIONS.md)를 참고하세요.
환경이 잘 구성되어 있는지 주기적으로 검토하고 싶다면 [`AUDIT.md`](AUDIT.md)의 프롬프트를 사용하세요.

## 참고

- Anthropic — Harness Design for Long-Running Claude Agent Applications: <https://www.anthropic.com/engineering/harness-design-long-running-apps>
