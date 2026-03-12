# Work Distribution Rule

When a code modification or implementation request requires changes to **2 or more files**, perform a quick pre-check before writing any code:

1. Identify all files that need modification.
2. Analyze **directional dependencies** between them (which file is depended on by which).
3. Build a dependency tree and identify the **root files** (files that are depended on by others but depend on nothing within the modification scope).

- If **2+ files** need modification → invoke the `/work-distribution` skill.
- If only **1 file** needs modification → skip the skill and proceed directly.

## Recursive Sub-agent Workflow

Each agent follows this pattern:

1. Modify its assigned file
2. Identify files that depend on the modified file
3. Spawn sub-agents for those dependent files (parallel if multiple)
4. Sub-agents repeat the same pattern recursively

```
Example: A ← B, A ← C, B ← D, B ← F, C ← G

Main Instance
    └── [A Agent]
            ├── Modify A
            └── Spawn [B Agent] [C Agent] in parallel
                    │               │
                    │               ├── Modify C
                    │               └── Spawn [G Agent]
                    │
                    ├── Modify B
                    └── Spawn [D Agent] [F Agent] in parallel
```

## Sub-agent Prompt Guidelines

서브에이전트를 spawn할 때 프롬프트는 **컴팩트하면서 명확**해야 한다. 아래 구조를 반드시 따른다:

### 필수 포함 항목

```
1. 대상 파일: 수정할 파일의 절대 경로
2. 작업 지시: 해당 파일에서 수행할 변경 내용 (구체적인 함수/클래스/인터페이스 명시)
3. 변경 근거: 상위 파일에서 무엇이 바뀌었고, 이 파일이 왜 수정되어야 하는지
4. 하위 전파: 이 파일을 수정한 뒤 의존하는 파일 목록과 각각의 예상 변경 사항
```

### 프롬프트 템플릿

```
파일: {절대 경로}

작업: {구체적 변경 내용 — 함수명, 시그니처 변경, 타입 변경 등을 명시}

근거: {상위 파일}에서 {변경 요약}이 발생하여 이 파일의 {영향받는 부분}을 맞춰야 함

하위 의존:
- {파일 A} → {예상 변경}
- {파일 B} → {예상 변경}
- (없으면 "없음")
```

### 금지 사항

- 작업 범위 밖의 리팩토링, 개선, 정리를 지시하지 않는다
- "전체 파일을 검토하고 필요한 수정을 하라" 같은 모호한 지시를 하지 않는다
- 상위 파일의 전체 변경 내역을 그대로 복사해서 전달하지 않는다 — 해당 파일에 영향을 주는 변경만 요약한다
- 이미 완료된 상위 파일 수정을 반복하도록 지시하지 않는다
