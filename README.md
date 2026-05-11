# Claude / Codex Config

Claude Code CLI와 Codex를 위한 개인 설정 파일 모음입니다. 여러 환경(Mac/Windows/데스크탑)에서 동일한 에이전트 작업 경험을 제공하기 위한 하네스 설정 저장소입니다.

## 구조

| 경로 | 목적 |
|-|-|
| `rules/` | 모든 작업에 횡단 적용되는 행동 규칙 |
| `skills/` | 재사용 가능한 워크플로 단위 |
| `commands/` | 슬래시 커맨드 정의 |
| `agents/` | 서브에이전트 정의 |
| `settings.json` | Claude Code 런타임 설정 |
| `codex/` | Codex 전역 지시(`AGENTS.md`), rule 모듈, skills, agents |
| `DECISIONS.md` | 의식적으로 배제한 항목과 이유 |
| `AUDIT.md` | 하네스 환경 자가 검토용 프롬프트 모음 |

## 전제

- Claude 설정은 `~/.claude/` 디렉토리에 로드되는 것을 전제로 합니다.
- Codex 설정은 `~/.codex/` 디렉토리에 로드되는 것을 전제로 합니다.
- Claude Code CLI가 설치되어 있어야 합니다.
- 최초 1회는 저장소를 clone한 후 동기화 절차를 수행해야 합니다.

## 동기화 전략 — 두 가지 도구의 역할

본 저장소는 **symlink**와 **`/sync-settings` 스킬**을 병행합니다. 두 도구는 서로 대체하는 관계가 아니라 **다른 가치**를 가집니다.

| 도구 | 역할 | 사용 빈도 |
|-|-|-|
| **Symlink** | 일상 동기화 자동화 (`git pull` 한 번으로 즉시 반영) | 상시 |
| **`/sync-settings`** | 머신 간 diff 확인, 실험적 변경 승급, 머신별 분기 | 가끔 |

병행하는 이유는 [`DECISIONS.md`](DECISIONS.md)의 항목 6을 참고하세요.

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

저장소의 디렉토리/파일을 `~/.claude/`로 symlink 연결합니다.

**macOS / Linux**

```bash
cd ~/code/claude-code-config
ln -s "$PWD/rules"         ~/.claude/rules
ln -s "$PWD/skills"        ~/.claude/skills
ln -s "$PWD/commands"      ~/.claude/commands
ln -s "$PWD/agents"        ~/.claude/agents
ln -s "$PWD/settings.json" ~/.claude/settings.json
```

**Windows (PowerShell, 관리자 권한 또는 개발자 모드 필요)**

```powershell
$src = "$env:USERPROFILE\code\claude-code-config"
$dst = "$env:USERPROFILE\.claude"

New-Item -ItemType SymbolicLink -Path "$dst\rules"         -Target "$src\rules"
New-Item -ItemType SymbolicLink -Path "$dst\skills"        -Target "$src\skills"
New-Item -ItemType SymbolicLink -Path "$dst\commands"      -Target "$src\commands"
New-Item -ItemType SymbolicLink -Path "$dst\agents"        -Target "$src\agents"
New-Item -ItemType SymbolicLink -Path "$dst\settings.json" -Target "$src\settings.json"
```

> Windows에서 symlink 생성 권한이 없다면, 설정 → 개발자 모드를 활성화하면 일반 사용자도 가능합니다.

### 4. 설치 검증

Claude Code 세션을 새로 열고 다음을 확인합니다.

- 규칙이 반영되었는지 (예: 파일 수정 시도 시 `action-guard`가 발동하는지)
- 스킬이 목록에 뜨는지
- 슬래시 커맨드가 작동하는지 (`/inspect`, `/commit` 등)

## Codex 적용

Codex용 설정은 Claude 전용 문법을 그대로 복사하지 않고, Codex가 읽는 전역 지시, rule 모듈, skill, custom agent 형식으로 변환해 `codex/` 아래에 둡니다.

**Windows (PowerShell)**

```powershell
$src = "$env:USERPROFILE\code\claude\config\codex"
$dst = "$env:USERPROFILE\.codex"

Copy-Item -LiteralPath "$src\AGENTS.md" -Destination "$dst\AGENTS.md" -Force
Copy-Item -LiteralPath "$src\rule" -Destination "$dst\rule" -Recurse -Force
Copy-Item -LiteralPath "$src\skills\*" -Destination "$dst\skills" -Recurse -Force
Copy-Item -LiteralPath "$src\agents\*" -Destination "$dst\agents" -Recurse -Force
```

Codex 세션을 새로 열면 다음 항목이 전역으로 적용됩니다.

- `~/.codex/AGENTS.md`
- `~/.codex/rule/*.md`
- `~/.codex/skills/work-orchestration`
- `~/.codex/skills/inspect-dependencies`
- `~/.codex/skills/git-commit-workflow`
- `~/.codex/skills/git-branch-cleanup`
- `~/.codex/skills/codex-settings-sync`
- `~/.codex/agents/code-explorer.toml`
- `~/.codex/agents/file-modifier.toml`
- `~/.codex/agents/file-creator.toml`

### Claude → Codex 매핑

| Claude | Codex |
|-|-|
| `rules/*/RULE.md` | `codex/rule/*.md` + `codex/AGENTS.md` 참조 |
| `skills/work-orchestration` | `codex/skills/work-orchestration` |
| `commands/inspect.md` | `codex/skills/inspect-dependencies` |
| `commands/commit.md` | `codex/skills/git-commit-workflow` |
| `commands/br-clear.md` | `codex/skills/git-branch-cleanup` |
| `commands/sync-settings.md` | `codex/skills/codex-settings-sync` |
| `agents/work-orchestration/*.md` | `codex/agents/*.toml` |
| `settings.json` | `codex/config.toml` + `codex/AGENTS.md` 일부 지시 |

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

### 머신 간 차이 확인 또는 실험 승급 — `/sync-settings`

Symlink로 연결된 환경에서는 `~/.claude/`와 저장소가 동일하므로 일반적으로 `/sync-settings`가 필요 없습니다. 다만 다음 상황에서 사용합니다.

- **머신 간 의도치 않은 분기 발생** — 예: 한 머신에서 symlink가 풀리고 직접 파일을 수정한 경우
- **실험적 변경의 승급** — 어떤 머신에서만 임시로 직접 파일을 두고 검증한 후, 결과가 좋으면 저장소로 올리고 싶을 때
- **머신별 부분 적용** — 일부 규칙만 특정 머신에 다르게 적용하고 싶을 때 (이 경우 해당 항목만 symlink를 풀고 sync-settings로 관리)

Claude Code 세션에서:

```
/sync-settings
```

이 스킬은 양방향 diff를 보여주고 명시적 승인 후에만 변경을 적용합니다. 자세한 동작은 `commands/sync-settings.md`를 참고하세요.

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
